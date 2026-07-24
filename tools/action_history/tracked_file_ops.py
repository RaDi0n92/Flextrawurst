from __future__ import annotations

import hashlib
import os
import tempfile
from pathlib import Path
from typing import Any

from .history import ActionHistory


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


class TrackedFileOps:
    """Werkraum-Dateioperationen, die jede echte oder blockierte Aktion protokollieren."""

    def __init__(self, history: ActionHistory):
        self.history = history
        roots = os.environ.get(
            "FLEXTRAWURST_HISTORY_ALLOWED_ROOTS",
            "/root/werkraum,/root/visionen",
        )
        self.allowed_roots = [Path(root).resolve() for root in roots.split(",") if root.strip()]

    def _resolve(self, path: str, *, action: str, session_id: str | None) -> Path:
        candidate = Path(path).expanduser().resolve()
        if not any(candidate == root or root in candidate.parents for root in self.allowed_roots):
            self.history.append(
                action=action,
                target=str(candidate),
                status="blocked",
                session_id=session_id,
                completeness="aborted",
                details={
                    "reason": "path_outside_allowed_roots",
                    "allowed_roots": [str(root) for root in self.allowed_roots],
                },
            )
            raise PermissionError(f"Pfad liegt außerhalb erlaubter Wurzeln: {candidate}")
        return candidate

    def read_text(
        self,
        path: str,
        *,
        session_id: str | None = None,
        start_line: int = 1,
        max_lines: int | None = None,
        action: str = "read_file",
    ) -> dict[str, Any]:
        target = self._resolve(path, action=action, session_id=session_id)
        completeness = "complete" if start_line == 1 and max_lines is None else "partial"
        with self.history.recorded_action(
            action=action,
            target=str(target),
            session_id=session_id,
            completeness=completeness,
            details={"start_line": start_line, "max_lines": max_lines},
        ) as state:
            raw = target.read_bytes()
            text = raw.decode("utf-8")
            lines = text.splitlines()
            start_index = max(start_line - 1, 0)
            selected = lines[start_index:] if max_lines is None else lines[start_index : start_index + max_lines]
            rendered = "\n".join(selected)
            state.update(
                {
                    "bytes_total": len(raw),
                    "line_count_total": len(lines),
                    "returned_line_count": len(selected),
                    "sha256": _sha256(raw),
                }
            )
            return {
                "path": str(target),
                "content": rendered,
                "complete": completeness == "complete",
                **state,
            }

    def write_text(
        self,
        path: str,
        content: str,
        *,
        session_id: str | None = None,
        overwrite: bool = False,
        action: str = "write_file",
    ) -> dict[str, Any]:
        target = self._resolve(path, action=action, session_id=session_id)
        if target.exists() and not overwrite:
            self.history.append(
                action=action,
                target=str(target),
                status="blocked",
                session_id=session_id,
                completeness="aborted",
                details={"reason": "overwrite_not_explicit"},
            )
            raise FileExistsError(f"Datei existiert bereits: {target}")

        encoded = content.encode("utf-8")
        old_sha = _sha256(target.read_bytes()) if target.exists() else None
        with self.history.recorded_action(
            action=action,
            target=str(target),
            session_id=session_id,
            completeness="complete",
            details={"overwrite": overwrite, "old_sha256": old_sha},
        ) as state:
            target.parent.mkdir(parents=True, exist_ok=True)
            fd, temp_path = tempfile.mkstemp(prefix=f".{target.name}.", dir=str(target.parent))
            try:
                with os.fdopen(fd, "wb") as handle:
                    handle.write(encoded)
                    handle.flush()
                    os.fsync(handle.fileno())
                os.replace(temp_path, target)
            except Exception:
                try:
                    os.unlink(temp_path)
                except FileNotFoundError:
                    pass
                raise
            state.update(
                {
                    "bytes_written": len(encoded),
                    "sha256": _sha256(encoded),
                    "created": old_sha is None,
                }
            )
            return {"path": str(target), **state}

    def append_text(
        self,
        path: str,
        content: str,
        *,
        session_id: str | None = None,
        action: str = "append_file",
    ) -> dict[str, Any]:
        target = self._resolve(path, action=action, session_id=session_id)
        encoded = content.encode("utf-8")
        with self.history.recorded_action(
            action=action,
            target=str(target),
            session_id=session_id,
            completeness="complete",
        ) as state:
            target.parent.mkdir(parents=True, exist_ok=True)
            with target.open("ab") as handle:
                handle.write(encoded)
                handle.flush()
                os.fsync(handle.fileno())
            raw = target.read_bytes()
            state.update(
                {
                    "bytes_appended": len(encoded),
                    "bytes_total": len(raw),
                    "sha256": _sha256(raw),
                }
            )
            return {"path": str(target), **state}

    def reread_text(self, path: str, *, session_id: str | None = None) -> dict[str, Any]:
        return self.read_text(
            path,
            session_id=session_id,
            action="reread_own_file",
        )
