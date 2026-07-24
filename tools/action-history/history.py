from __future__ import annotations

import contextlib
import datetime as dt
import fcntl
import hashlib
import json
import os
import uuid
from pathlib import Path
from typing import Any, Iterator

DEFAULT_HISTORY_PATH = Path(
    os.environ.get(
        "FLEXTRAWURST_ACTION_HISTORY",
        "/root/werkraum/_gpt/session_history.jsonl",
    )
)
DEFAULT_ACTOR = os.environ.get("FLEXTRAWURST_ACTION_ACTOR", "GPT-5.6-sol-hoch")


class HistoryIntegrityError(RuntimeError):
    """Raised when the append-only hash chain is damaged."""


class ActionHistory:
    """Append-only, hash-chained action history for AI work streams."""

    def __init__(self, path: str | Path = DEFAULT_HISTORY_PATH, actor: str = DEFAULT_ACTOR):
        self.path = Path(path)
        self.actor = actor
        self.path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
        if not self.path.exists():
            self.path.touch(mode=0o600)
        else:
            os.chmod(self.path, 0o600)

    @staticmethod
    def _canonical_json(value: dict[str, Any]) -> bytes:
        return json.dumps(
            value,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")

    @classmethod
    def _calculate_hash(cls, event_without_hash: dict[str, Any]) -> str:
        return hashlib.sha256(cls._canonical_json(event_without_hash)).hexdigest()

    def _read_unlocked(self, handle) -> list[dict[str, Any]]:
        handle.seek(0)
        events: list[dict[str, Any]] = []
        for line_number, raw_line in enumerate(handle, start=1):
            line = raw_line.strip()
            if not line:
                continue
            try:
                event = json.loads(line)
            except json.JSONDecodeError as exc:
                raise HistoryIntegrityError(
                    f"Ungültiges JSON in Zeile {line_number}: {exc}"
                ) from exc
            events.append(event)
        return events

    def verify(self) -> dict[str, Any]:
        with self.path.open("r", encoding="utf-8") as handle:
            fcntl.flock(handle.fileno(), fcntl.LOCK_SH)
            events = self._read_unlocked(handle)
            fcntl.flock(handle.fileno(), fcntl.LOCK_UN)

        previous_hash: str | None = None
        for index, event in enumerate(events):
            actual_hash = event.get("event_hash")
            payload = dict(event)
            payload.pop("event_hash", None)
            expected_hash = self._calculate_hash(payload)
            if actual_hash != expected_hash:
                raise HistoryIntegrityError(
                    f"Hashfehler bei Ereignis {index + 1} ({event.get('event_id')})"
                )
            if payload.get("previous_hash") != previous_hash:
                raise HistoryIntegrityError(
                    f"Kettenfehler bei Ereignis {index + 1} ({event.get('event_id')})"
                )
            previous_hash = actual_hash

        return {
            "ok": True,
            "events": len(events),
            "last_hash": previous_hash,
            "path": str(self.path),
        }

    def append(
        self,
        *,
        action: str,
        target: str | None = None,
        status: str = "success",
        session_id: str | None = None,
        completeness: str | None = None,
        details: dict[str, Any] | None = None,
        actor: str | None = None,
        parent_event_id: str | None = None,
    ) -> dict[str, Any]:
        now = dt.datetime.now(dt.timezone.utc).isoformat()
        event: dict[str, Any] = {
            "event_id": str(uuid.uuid4()),
            "timestamp_utc": now,
            "session_id": session_id or "unknown-session",
            "actor": actor or self.actor,
            "action": action,
            "target": target,
            "status": status,
            "completeness": completeness,
            "details": details or {},
            "parent_event_id": parent_event_id,
            "previous_hash": None,
        }

        with self.path.open("a+", encoding="utf-8") as handle:
            fcntl.flock(handle.fileno(), fcntl.LOCK_EX)
            events = self._read_unlocked(handle)
            if events:
                event["previous_hash"] = events[-1].get("event_hash")
            event["event_hash"] = self._calculate_hash(event)
            handle.seek(0, os.SEEK_END)
            handle.write(json.dumps(event, ensure_ascii=False, sort_keys=True) + "\n")
            handle.flush()
            os.fsync(handle.fileno())
            fcntl.flock(handle.fileno(), fcntl.LOCK_UN)
        return event

    def list_events(
        self,
        *,
        session_id: str | None = None,
        action: str | None = None,
        status: str | None = None,
        limit: int = 100,
    ) -> list[dict[str, Any]]:
        if limit < 1 or limit > 5000:
            raise ValueError("limit muss zwischen 1 und 5000 liegen")

        with self.path.open("r", encoding="utf-8") as handle:
            fcntl.flock(handle.fileno(), fcntl.LOCK_SH)
            events = self._read_unlocked(handle)
            fcntl.flock(handle.fileno(), fcntl.LOCK_UN)

        filtered = [
            event
            for event in events
            if (session_id is None or event.get("session_id") == session_id)
            and (action is None or event.get("action") == action)
            and (status is None or event.get("status") == status)
        ]
        return filtered[-limit:]

    def summary(self, *, session_id: str | None = None) -> dict[str, Any]:
        events = self.list_events(session_id=session_id, limit=5000)
        by_action: dict[str, int] = {}
        by_status: dict[str, int] = {}
        targets: list[str] = []

        for event in events:
            action = str(event.get("action") or "unknown")
            status = str(event.get("status") or "unknown")
            by_action[action] = by_action.get(action, 0) + 1
            by_status[status] = by_status.get(status, 0) + 1
            target = event.get("target")
            if target and target not in targets:
                targets.append(target)

        return {
            "session_id": session_id,
            "event_count": len(events),
            "by_action": by_action,
            "by_status": by_status,
            "targets": targets[-100:],
            "last_event": events[-1] if events else None,
        }

    def startup_context(
        self,
        *,
        session_id: str | None = None,
        recent_limit: int = 30,
    ) -> dict[str, Any]:
        recent = self.list_events(session_id=session_id, limit=recent_limit)
        failed = [event for event in recent if event.get("status") != "success"]
        incomplete = [
            event
            for event in recent
            if event.get("completeness") in {"partial", "unknown", "aborted"}
        ]
        return {
            "actor": self.actor,
            "history_path": str(self.path),
            "session_id": session_id,
            "recent_actions": recent,
            "failed_or_blocked": failed,
            "partial_or_unknown": incomplete,
            "integrity": self.verify(),
        }

    @contextlib.contextmanager
    def recorded_action(
        self,
        *,
        action: str,
        target: str | None = None,
        session_id: str | None = None,
        completeness: str | None = None,
        details: dict[str, Any] | None = None,
    ) -> Iterator[dict[str, Any]]:
        state: dict[str, Any] = {}
        try:
            yield state
        except Exception as exc:
            self.append(
                action=action,
                target=target,
                status="failed",
                session_id=session_id,
                completeness=completeness,
                details={**(details or {}), **state, "error": repr(exc)},
            )
            raise
        else:
            self.append(
                action=action,
                target=target,
                status="success",
                session_id=session_id,
                completeness=completeness,
                details={**(details or {}), **state},
            )
