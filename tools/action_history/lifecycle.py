from __future__ import annotations

import contextlib
import fcntl
import os
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


def begin_session_once(
    history: ActionHistory,
    session_id: str,
    *,
    details: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Erzeugt auch bei parallelen Aufrufen höchstens ein session.begin-Ereignis."""
    with _lifecycle_lock(history):
        return history.begin_session(session_id, details=details)


def end_session_once(
    history: ActionHistory,
    session_id: str,
    *,
    details: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Erzeugt auch bei parallelen Aufrufen höchstens ein session.end-Ereignis."""
    with _lifecycle_lock(history):
        return history.end_session(session_id, details=details)


def startup_session(
    history: ActionHistory,
    *,
    session_id: str,
    recent_limit: int = 30,
    details: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Eröffnet eine Session rennsicher und liefert danach ihren vollständigen Startkontext."""
    session_begin = begin_session_once(
        history,
        session_id,
        details={"source": "history_startup", **(details or {})},
    )
    context = history.startup_context(
        session_id=session_id,
        recent_limit=recent_limit,
    )
    return {"session_begin": session_begin, **context}
