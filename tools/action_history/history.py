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
    pass


class ActionHistory:
    """Append-only, hash-chained action history for AI work streams."""

    def __init__(self, path: str | Path = DEFAULT_HISTORY_PATH, actor: str = DEFAULT_ACTOR):
        self.path = Path(path)
        self.actor = actor
        self.path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
        if not self.path.exists():
            self.path.touch(mode=0o600)
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
                events.append(json.loads(line))
            except json.JSONDecodeError as exc:
                raise HistoryIntegrityError(
                    f"Ungültiges JSON in Zeile {line_number}: {exc}"
                ) from exc
        return events

    def _all_events(self) -> list[dict[str, Any]]:
        with self.path.open("r", encoding="utf-8") as handle:
            fcntl.flock(handle.fileno(), fcntl.LOCK_SH)
            events = self._read_unlocked(handle)
            fcntl.flock(handle.fileno(), fcntl.LOCK_UN)
        return events

    def verify(self) -> dict[str, Any]:
        events = self._all_events()
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
