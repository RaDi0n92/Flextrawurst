from __future__ import annotations

from typing import Any

from .history import ActionHistory


def startup_session(
    history: ActionHistory,
    *,
    session_id: str,
    recent_limit: int = 30,
    details: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Eröffnet eine Session idempotent und liefert danach ihren vollständigen Startkontext."""
    session_begin = history.begin_session(
        session_id,
        details={"source": "history_startup", **(details or {})},
    )
    context = history.startup_context(
        session_id=session_id,
        recent_limit=recent_limit,
    )
    return {"session_begin": session_begin, **context}
