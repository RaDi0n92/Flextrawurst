from __future__ import annotations

import contextlib
import datetime as dt
import fcntl
import hashlib
import os
import uuid
from collections.abc import Iterator
from contextvars import ContextVar
from pathlib import Path
from typing import Any

from .history import ActionHistory

_HELD_LOCKS: ContextVar[frozenset[str]] = ContextVar(
    "action_history_held_locks",
    default=frozenset(),
)


class SessionClosedError(RuntimeError):
    pass


def _lock_path(history: ActionHistory, session_id: str | None = None) -> Path:
    if session_id is None:
        return Path(f"{history.path}.lifecycle.lock")
    digest = hashlib.sha256(session_id.encode("utf-8")).hexdigest()[:24]
    return Path(f"{history.path}.session-{digest}.lock")


@contextlib.contextmanager
def _file_lock(path: Path) -> Iterator[None]:
    key = str(path)
    held = _HELD_LOCKS.get()
    if key in held:
        yield
        return

    path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    with path.open("a+", encoding="utf-8") as handle:
        os.chmod(path, 0o600)
        fcntl.flock(handle.fileno(), fcntl.LOCK_EX)
        token = _HELD_LOCKS.set(held | {key})
        try:
            yield
        finally:
            _HELD_LOCKS.reset(token)
            fcntl.flock(handle.fileno(), fcntl.LOCK_UN)


@contextlib.contextmanager
def _lifecycle_lock(history: ActionHistory) -> Iterator[None]:
    with _file_lock(_lock_path(history)):
        yield


@contextlib.contextmanager
def _session_lock(history: ActionHistory, session_id: str) -> Iterator[None]:
    with _file_lock(_lock_path(history, session_id)):
        yield


def generate_session_id(prefix: str = "chatgpt") -> str:
    timestamp = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    return f"{prefix}-{timestamp}-{uuid.uuid4().hex[:12]}"


def _require_real_session_id(session_id: str | None) -> str:
    if not session_id or session_id == "unknown-session":
        raise ValueError("Eine echte session_id ist erforderlich")
    return session_id


def _session_is_closed(history: ActionHistory, session_id: str) -> bool:
    return bool(history.list_events(session_id=session_id, action="session.end", limit=1))


def _real_session_ids(history: ActionHistory) -> list[str]:
    sessions: list[str] = []
    for event in history.list_events(limit=5000):
        if event.get("action") != "session.begin":
            continue
        session_id = str(event.get("session_id") or "")
        if session_id and session_id not in sessions:
            sessions.append(session_id)
    return sessions


def _previous_real_session_id(history: ActionHistory, current_session_id: str) -> str | None:
    candidates = [
        session_id
        for session_id in _real_session_ids(history)
        if session_id != current_session_id
    ]
    return candidates[-1] if candidates else None


def _record_closed_attempt(
    history: ActionHistory,
    session_id: str,
    *,
    action: str,
    target: str | None,
) -> None:
    history.append(
        action="session.closed_action_blocked",
        target=session_id,
        status="blocked",
        session_id="system-audit",
        completeness="aborted",
        details={
            "attempted_action": action,
            "attempted_target": target,
            "closed_session_id": session_id,
        },
    )


@contextlib.contextmanager
def session_action(
    history: ActionHistory,
    session_id: str,
    *,
    action: str,
    target: str | None = None,
) -> Iterator[str]:
    """Verhindert Rennen zwischen laufender Arbeit und Sessionabschluss."""
    active_session_id = _require_real_session_id(session_id)
    with _session_lock(history, active_session_id):
        if _session_is_closed(history, active_session_id):
            _record_closed_attempt(
                history,
                active_session_id,
                action=action,
                target=target,
            )
            raise SessionClosedError(
                f"Session ist bereits geschlossen: {active_session_id}"
            )
        yield active_session_id


def begin_session_once(
    history: ActionHistory,
    session_id: str,
    *,
    details: dict[str, Any] | None = None,
) -> dict[str, Any]:
    active_session_id = _require_real_session_id(session_id)
    with _lifecycle_lock(history), _session_lock(history, active_session_id):
        return history.begin_session(active_session_id, details=details)


def end_session_once(
    history: ActionHistory,
    session_id: str,
    *,
    details: dict[str, Any] | None = None,
) -> dict[str, Any]:
    active_session_id = _require_real_session_id(session_id)
    with _lifecycle_lock(history), _session_lock(history, active_session_id):
        return history.end_session(active_session_id, details=details)


def _startup_context(
    history: ActionHistory,
    session_id: str,
    recent_limit: int,
) -> dict[str, Any]:
    current = history.list_events(session_id=session_id, limit=recent_limit)
    previous_session_id = _previous_real_session_id(history, session_id)
    previous = (
        history.list_events(session_id=previous_session_id, limit=recent_limit)
        if previous_session_id
        else []
    )
    global_recent = history.list_events(limit=recent_limit)
    relevant = previous + current + [
        event
        for event in global_recent
        if event.get("session_id") in {"system-audit", "unassigned"}
    ]
    return {
        "actor": history.actor,
        "history_path": str(history.path),
        "checkpoint_path": str(history.checkpoint_path),
        "session_id": session_id,
        "current_session_actions": current,
        "previous_session_id": previous_session_id,
        "previous_session_actions": previous,
        "global_recent_actions": global_recent,
        "failed_or_blocked": [
            event for event in relevant if event.get("status") != "success"
        ],
        "partial_or_unknown": [
            event
            for event in relevant
            if event.get("completeness") in {"partial", "unknown", "aborted"}
        ],
        "integrity": history.verify(),
    }


def startup_session(
    history: ActionHistory,
    *,
    session_id: str | None = None,
    recent_limit: int = 30,
    details: dict[str, Any] | None = None,
) -> dict[str, Any]:
    requested_session_id = session_id
    replaced_closed_session_id: str | None = None
    generated = not session_id or session_id == "unknown-session"

    if session_id and session_id != "unknown-session" and _session_is_closed(history, session_id):
        replaced_closed_session_id = session_id
        generated = True

    resolved_session_id = generate_session_id() if generated else str(session_id)
    session_begin = begin_session_once(
        history,
        resolved_session_id,
        details={
            "source": "history_startup",
            "generated_session_id": generated,
            "requested_session_id": requested_session_id,
            "replaced_closed_session_id": replaced_closed_session_id,
            **(details or {}),
        },
    )
    context = _startup_context(
        history,
        resolved_session_id,
        recent_limit,
    )
    return {
        "session_begin": session_begin,
        "generated_session_id": generated,
        "replaced_closed_session_id": replaced_closed_session_id,
        **context,
    }
