from __future__ import annotations

import contextlib
import datetime as dt
import fcntl
import hashlib
import json
import os
import tempfile
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
CHECKPOINT_VERSION = 1


class HistoryIntegrityError(RuntimeError):
    pass


class ActionHistory:
    """Append-only, hash-chained action history with an independent atomic tail checkpoint."""

    def __init__(self, path: str | Path = DEFAULT_HISTORY_PATH, actor: str = DEFAULT_ACTOR):
        self.path = Path(path)
        self.checkpoint_path = Path(f"{self.path}.checkpoint.json")
        self.actor = actor
        self.path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
        if not self.path.exists():
            self.path.touch(mode=0o600)
        os.chmod(self.path, 0o600)
        if self.checkpoint_path.exists():
            os.chmod(self.checkpoint_path, 0o600)

    @staticmethod
    def _canonical_json(value: dict[str, Any]) -> bytes:
        return json.dumps(
            value,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")

    @classmethod
    def _calculate_hash(cls, value_without_hash: dict[str, Any]) -> str:
        return hashlib.sha256(cls._canonical_json(value_without_hash)).hexdigest()

    def _read_unlocked(self, handle) -> list[dict[str, Any]]:
        handle.seek(0)
        events: list[dict[str, Any]] = []
        for line_number, raw_line in enumerate(handle, start=1):
            line = raw_line.strip()
            if not line:
                continue
            try:
                events.append(json.loads(line))
            except json.JSONDecodeError as exc:
                raise HistoryIntegrityError(
                    f"Ungültiges JSON in Zeile {line_number}: {exc}"
                ) from exc
        return events

    def _all_events(self) -> list[dict[str, Any]]:
        with self.path.open("r", encoding="utf-8") as handle:
            fcntl.flock(handle.fileno(), fcntl.LOCK_SH)
            try:
                return self._read_unlocked(handle)
            finally:
                fcntl.flock(handle.fileno(), fcntl.LOCK_UN)

    def _verify_event_chain(self, events: list[dict[str, Any]]) -> str | None:
        previous_hash: str | None = None
        for index, event in enumerate(events, start=1):
            actual_hash = event.get("event_hash")
            payload = dict(event)
            payload.pop("event_hash", None)
            expected_hash = self._calculate_hash(payload)
            if actual_hash != expected_hash:
                raise HistoryIntegrityError(
                    f"Hashfehler bei Ereignis {index} ({event.get('event_id')})"
                )
            if payload.get("previous_hash") != previous_hash:
                raise HistoryIntegrityError(
                    f"Kettenfehler bei Ereignis {index} ({event.get('event_id')})"
                )
            previous_hash = actual_hash
        return previous_hash

    def _read_checkpoint(self) -> dict[str, Any]:
        try:
            checkpoint = json.loads(self.checkpoint_path.read_text(encoding="utf-8"))
        except FileNotFoundError:
            raise
        except json.JSONDecodeError as exc:
            raise HistoryIntegrityError(f"Ungültiger Checkpoint: {exc}") from exc

        actual_hash = checkpoint.get("checkpoint_hash")
        payload = dict(checkpoint)
        payload.pop("checkpoint_hash", None)
        expected_hash = self._calculate_hash(payload)
        if actual_hash != expected_hash:
            raise HistoryIntegrityError("Checkpoint-Hash ist ungültig")
        if payload.get("checkpoint_version") != CHECKPOINT_VERSION:
            raise HistoryIntegrityError(
                f"Unbekannte Checkpoint-Version: {payload.get('checkpoint_version')}"
            )
        return checkpoint

    def _verify_checkpoint(
        self,
        events: list[dict[str, Any]],
        last_hash: str | None,
    ) -> str:
        if not self.checkpoint_path.exists():
            if events:
                raise HistoryIntegrityError(
                    "Historie enthält Ereignisse, aber der unabhängige Checkpoint fehlt"
                )
            return "missing-empty"

        checkpoint = self._read_checkpoint()
        expected_last_event_id = events[-1].get("event_id") if events else None
        expected = {
            "history_path": str(self.path),
            "event_count": len(events),
            "last_hash": last_hash,
            "last_event_id": expected_last_event_id,
        }
        for key, expected_value in expected.items():
            if checkpoint.get(key) != expected_value:
                raise HistoryIntegrityError(
                    f"Checkpoint-Abweichung bei {key}: "
                    f"erwartet={expected_value!r}, gefunden={checkpoint.get(key)!r}"
                )
        return "verified"

    def _write_checkpoint(self, event_count: int, last_event: dict[str, Any]) -> None:
        payload: dict[str, Any] = {
            "checkpoint_version": CHECKPOINT_VERSION,
            "history_path": str(self.path),
            "event_count": event_count,
            "last_hash": last_event.get("event_hash"),
            "last_event_id": last_event.get("event_id"),
            "updated_at_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
        }
        payload["checkpoint_hash"] = self._calculate_hash(payload)
        encoded = (
            json.dumps(payload, ensure_ascii=False, sort_keys=True) + "\n"
        ).encode("utf-8")

        fd, temp_path = tempfile.mkstemp(
            prefix=f".{self.checkpoint_path.name}.",
            dir=str(self.checkpoint_path.parent),
        )
        try:
            with os.fdopen(fd, "wb") as handle:
                handle.write(encoded)
                handle.flush()
                os.fsync(handle.fileno())
            os.chmod(temp_path, 0o600)
            os.replace(temp_path, self.checkpoint_path)
            os.chmod(self.checkpoint_path, 0o600)
            directory_fd = os.open(
                self.checkpoint_path.parent,
                os.O_RDONLY | getattr(os, "O_DIRECTORY", 0),
            )
            try:
                os.fsync(directory_fd)
            finally:
                os.close(directory_fd)
        except Exception:
            try:
                os.unlink(temp_path)
            except FileNotFoundError:
                pass
            raise

    def verify(self) -> dict[str, Any]:
        with self.path.open("r", encoding="utf-8") as handle:
            fcntl.flock(handle.fileno(), fcntl.LOCK_SH)
            try:
                events = self._read_unlocked(handle)
                last_hash = self._verify_event_chain(events)
                checkpoint_status = self._verify_checkpoint(events, last_hash)
            finally:
                fcntl.flock(handle.fileno(), fcntl.LOCK_UN)

        return {
            "ok": True,
            "events": len(events),
            "last_hash": last_hash,
            "path": str(self.path),
            "checkpoint_path": str(self.checkpoint_path),
            "checkpoint_status": checkpoint_status,
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
        event: dict[str, Any] = {
            "event_id": str(uuid.uuid4()),
            "timestamp_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
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
            try:
                events = self._read_unlocked(handle)
                last_hash = self._verify_event_chain(events)
                self._verify_checkpoint(events, last_hash)
                event["previous_hash"] = last_hash
                event["event_hash"] = self._calculate_hash(event)
                handle.seek(0, os.SEEK_END)
                handle.write(json.dumps(event, ensure_ascii=False, sort_keys=True) + "\n")
                handle.flush()
                os.fsync(handle.fileno())
                self._write_checkpoint(len(events) + 1, event)
            finally:
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
        if not 1 <= limit <= 5000:
            raise ValueError("limit muss zwischen 1 und 5000 liegen")

        events = self._all_events()
        filtered = [
            event
            for event in events
            if (session_id is None or event.get("session_id") == session_id)
            and (action is None or event.get("action") == action)
            and (status is None or event.get("status") == status)
        ]
        return filtered[-limit:]

    def session_ids(self, *, limit: int = 100) -> list[str]:
        sessions: list[str] = []
        for event in self._all_events():
            session_id = str(event.get("session_id") or "unknown-session")
            if session_id not in sessions:
                sessions.append(session_id)
        return sessions[-limit:]

    def previous_session_id(self, current_session_id: str | None) -> str | None:
        sessions = self.session_ids(limit=5000)
        candidates = [session for session in sessions if session != current_session_id]
        return candidates[-1] if candidates else None

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

    def begin_session(
        self,
        session_id: str,
        *,
        details: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        existing = self.list_events(session_id=session_id, action="session.begin", limit=1)
        if existing:
            return {"created": False, "event": existing[-1]}
        event = self.append(
            action="session.begin",
            session_id=session_id,
            completeness="complete",
            details=details,
        )
        return {"created": True, "event": event}

    def end_session(
        self,
        session_id: str,
        *,
        details: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        existing = self.list_events(session_id=session_id, action="session.end", limit=1)
        if existing:
            return {"created": False, "event": existing[-1]}
        event = self.append(
            action="session.end",
            session_id=session_id,
            completeness="complete",
            details={**(details or {}), "summary": self.summary(session_id=session_id)},
        )
        return {"created": True, "event": event}

    def startup_context(
        self,
        *,
        session_id: str | None = None,
        recent_limit: int = 30,
    ) -> dict[str, Any]:
        current = self.list_events(session_id=session_id, limit=recent_limit)
        global_recent = self.list_events(limit=recent_limit)
        previous_session_id = self.previous_session_id(session_id)
        previous = (
            self.list_events(session_id=previous_session_id, limit=recent_limit)
            if previous_session_id
            else []
        )
        visible = current or previous or global_recent
        return {
            "actor": self.actor,
            "history_path": str(self.path),
            "session_id": session_id,
            "current_session_actions": current,
            "previous_session_id": previous_session_id,
            "previous_session_actions": previous,
            "global_recent_actions": global_recent,
            "failed_or_blocked": [
                event for event in visible if event.get("status") != "success"
            ],
            "partial_or_unknown": [
                event
                for event in visible
                if event.get("completeness") in {"partial", "unknown", "aborted"}
            ],
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
