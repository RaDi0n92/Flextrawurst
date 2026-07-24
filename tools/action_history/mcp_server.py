from __future__ import annotations

import os
from typing import Any

from .history import ActionHistory
from .lifecycle import startup_session
from .tracked_file_ops import TrackedFileOps

try:
    from mcp.server.fastmcp import FastMCP
except ImportError as exc:  # pragma: no cover
    raise SystemExit(
        "Das Python-Paket 'mcp' fehlt. Installiere es im VPS-Venv, bevor der Server gestartet wird."
    ) from exc

REQUIRED_TOOLS = [
    "history_begin_session",
    "history_startup",
    "history_recent",
    "history_summary",
    "history_verify",
    "history_capabilities",
    "history_record_action",
    "history_end_session",
    "tracked_read_file",
    "tracked_write_file",
    "tracked_append_file",
    "tracked_reread_own_file",
]

mcp = FastMCP("flextrawurst-action-history")
history = ActionHistory()
files = TrackedFileOps(history)


@mcp.tool()
def history_begin_session(session_id: str, details: dict[str, Any] | None = None) -> dict[str, Any]:
    """Eröffnet eine Session idempotent und schreibt genau ein session.begin-Ereignis."""
    return history.begin_session(session_id, details=details)


@mcp.tool()
def history_startup(session_id: str = "unknown-session", recent_limit: int = 30) -> dict[str, Any]:
    """Eröffnet die Session selbst und liefert aktuelle, vorherige und globale Aktionen."""
    return startup_session(
        history,
        session_id=session_id,
        recent_limit=recent_limit,
    )


@mcp.tool()
def history_recent(
    session_id: str | None = None,
    action: str | None = None,
    status: str | None = None,
    limit: int = 100,
) -> list[dict[str, Any]]:
    """Liest die letzten protokollierten Aktionen."""
    return history.list_events(
        session_id=session_id,
        action=action,
        status=status,
        limit=limit,
    )


@mcp.tool()
def history_summary(session_id: str | None = None) -> dict[str, Any]:
    """Erzeugt ein Fazit ausschließlich aus protokollierten Aktionen."""
    return history.summary(session_id=session_id)


@mcp.tool()
def history_verify() -> dict[str, Any]:
    """Prüft die vollständige Hash-Kette der append-only Historie."""
    return history.verify()


@mcp.tool()
def history_capabilities() -> dict[str, Any]:
    """Liefert den verpflichtenden Werkzeugvertrag für die Client-Integration."""
    return {
        "actor": history.actor,
        "required_tools": REQUIRED_TOOLS,
        "history_path": str(history.path),
        "rule": "Alle Dateiaktionen über tracked_*; alle übrigen Aktionen über history_record_action.",
        "startup_rule": "history_startup eröffnet die Session automatisch und idempotent.",
    }


@mcp.tool()
def history_record_action(
    action: str,
    session_id: str,
    target: str | None = None,
    status: str = "success",
    completeness: str | None = None,
    details: dict[str, Any] | None = None,
    parent_event_id: str | None = None,
) -> dict[str, Any]:
    """Protokolliert eine Nicht-Dateiaktion eines anderen MCP-Werkzeugs."""
    return history.append(
        action=action,
        target=target,
        status=status,
        session_id=session_id,
        completeness=completeness,
        details=details,
        parent_event_id=parent_event_id,
    )


@mcp.tool()
def history_end_session(session_id: str, details: dict[str, Any] | None = None) -> dict[str, Any]:
    """Schließt eine Session idempotent und speichert ihr protokollbasiertes Fazit."""
    return history.end_session(session_id, details=details)


@mcp.tool()
def tracked_read_file(
    path: str,
    session_id: str = "unknown-session",
    start_line: int = 1,
    max_lines: int | None = None,
) -> dict[str, Any]:
    """Liest eine Werkraum-Datei und protokolliert Vollständigkeit, Hash und Umfang."""
    return files.read_text(
        path,
        session_id=session_id,
        start_line=start_line,
        max_lines=max_lines,
    )


@mcp.tool()
def tracked_write_file(
    path: str,
    content: str,
    session_id: str = "unknown-session",
    overwrite: bool = False,
) -> dict[str, Any]:
    """Schreibt atomar und protokolliert Pfad, Umfang und Hash."""
    return files.write_text(
        path,
        content,
        session_id=session_id,
        overwrite=overwrite,
    )


@mcp.tool()
def tracked_append_file(
    path: str,
    content: str,
    session_id: str = "unknown-session",
) -> dict[str, Any]:
    """Hängt Text an und protokolliert die resultierende Datei."""
    return files.append_text(path, content, session_id=session_id)


@mcp.tool()
def tracked_reread_own_file(
    path: str,
    session_id: str = "unknown-session",
) -> dict[str, Any]:
    """Liest eine gerade geschriebene Datei vollständig erneut und protokolliert dies separat."""
    return files.reread_text(path, session_id=session_id)


if __name__ == "__main__":
    transport = os.environ.get("FLEXTRAWURST_ACTION_HISTORY_TRANSPORT", "stdio")
    mcp.run(transport=transport)
