from __future__ import annotations

import contextlib
import datetime as dt
import fcntl
import os
import uuid
from collections.abc import Iterator
from pathlib import Path
from typing import Any

from .history import ActionHistory


@contextlib.contextmanager
def _lifecycle_lock(history: ActionHistory) -> Iterator[None]:
    lock_path = Path(f"{history.path}.lifecycle.lock")
    lock_path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    with lock_path.open("a+", encoding="utf-8") as handle:
        os.chmod(lock_path, 0o600)
        fcntl.flock(handle.fileno(), fcntl.LOCK_EX)
        try:
            yield
        finally:
            fcntl.flock(handle.fileno(), fcntl.LOCK_UN)


def generate_session_id(prefix: str = "chatgpt") -> str:
    timestamp = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    return f"{prefix}-{timestamp}-{uuid.uuid4().hex[:12]}"


def begin_session_once(
    history: ActionHistory,
    session_id: str,
    *,
    details: dict[str, Any] | None = None,
) -> dict[str, Any]:
    if not session_id or session_id == "unknown-session":
        raise ValueError("Eine echte session_id ist erforderlich")
    with _lifecycle_lock(history):
        return history.begin_session(session_id, details=details)


def end_session_once(
    history: ActionHistory,
    session_id: str,
    *,
    details: dict[str, Any] | None = None,
) -> dict[str, Any]:
    if not session_id or session_id == "unknown-session":
        raise ValueError("Eine echte session_id ist erforderlich")
    with _lifecycle_lock(history):
        return history.end_session(session_id, details=details)


def startup_session(
    history: ActionHistory,
    *,
    session_id: str | None = None,
    recent_limit: int = 30,
    details: dict[str, Any] | None = None,
) -> dict[str, Any]:
    generated = not session_id or session_id == "unknown-session"
    resolved_session_id = generate_session_id() if generated else str(session_id)
    session_begin = begin_session_once(
        history,
        resolved_session_id,
        details={"source": "history_startup", "generated_session_id": generated, **(details or {})},
    )
    context = history.startup_context(
        session_id=resolved_session_id,
        recent_limit=recent_limit,
    )
    return {
        "session_begin": session_begin,
        "generated_session_id": generated,
        **context,
    }
