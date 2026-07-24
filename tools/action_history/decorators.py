from __future__ import annotations

import functools
import inspect
import time
from collections.abc import Callable
from typing import Any, ParamSpec, TypeVar, cast

from .history import ActionHistory

P = ParamSpec("P")
R = TypeVar("R")


def _target_from_call(
    signature: inspect.Signature,
    args: tuple[Any, ...],
    kwargs: dict[str, Any],
    target_argument: str | None,
) -> str | None:
    if target_argument is None:
        return None
    bound = signature.bind_partial(*args, **kwargs)
    value = bound.arguments.get(target_argument)
    return None if value is None else str(value)


def tracked_mcp_action(
    history: ActionHistory,
    *,
    action: str,
    session_argument: str = "session_id",
    target_argument: str | None = None,
    completeness: str | None = "complete",
    static_details: dict[str, Any] | None = None,
) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """Umschließt bestehende sync/async MCP-Funktionen mit beweisbarer Aktionshistorie."""

    def decorator(function: Callable[P, R]) -> Callable[P, R]:
        signature = inspect.signature(function)

        def call_metadata(args: tuple[Any, ...], kwargs: dict[str, Any]) -> tuple[str, str | None]:
            bound = signature.bind_partial(*args, **kwargs)
            session_value = bound.arguments.get(session_argument, "unknown-session")
            session_id = str(session_value or "unknown-session")
            target = _target_from_call(signature, args, kwargs, target_argument)
            return session_id, target

        if inspect.iscoroutinefunction(function):

            @functools.wraps(function)
            async def async_wrapper(*args: P.args, **kwargs: P.kwargs):
                session_id, target = call_metadata(args, kwargs)
                started = time.monotonic()
                with history.recorded_action(
                    action=action,
                    target=target,
                    session_id=session_id,
                    completeness=completeness,
                    details={
                        **(static_details or {}),
                        "function": function.__qualname__,
                        "mode": "async",
                    },
                ) as state:
                    try:
                        result = await function(*args, **kwargs)
                    except Exception:
                        state["duration_ms"] = round((time.monotonic() - started) * 1000, 3)
                        state["result_type"] = "exception"
                        raise
                    state["duration_ms"] = round((time.monotonic() - started) * 1000, 3)
                    state["result_type"] = type(result).__name__
                    return result

            return cast(Callable[P, R], async_wrapper)

        @functools.wraps(function)
        def sync_wrapper(*args: P.args, **kwargs: P.kwargs):
            session_id, target = call_metadata(args, kwargs)
            started = time.monotonic()
            with history.recorded_action(
                action=action,
                target=target,
                session_id=session_id,
                completeness=completeness,
                details={
                    **(static_details or {}),
                    "function": function.__qualname__,
                    "mode": "sync",
                },
            ) as state:
                try:
                    result = function(*args, **kwargs)
                except Exception:
                    state["duration_ms"] = round((time.monotonic() - started) * 1000, 3)
                    state["result_type"] = "exception"
                    raise
                state["duration_ms"] = round((time.monotonic() - started) * 1000, 3)
                state["result_type"] = type(result).__name__
                return result

        return cast(Callable[P, R], sync_wrapper)

    return decorator
