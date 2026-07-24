from __future__ import annotations

from typing import Any

from .history import ActionHistory
from .lifecycle import begin_session_once, end_session_once, startup_session
from .reporting import build_session_report
from .tracked_file_ops import TrackedFileOps

REQUIRED_TOOLS = (
    "history_begin_session",
    "history_startup",
    "history_recent",
    "history_summary",
    "history_session_report",
    "history_verify",
    "history_capabilities",
    "history_record_action",
    "history_end_session",
    "tracked_read_file",
    "tracked_write_file",
    "tracked_append_file",
    "tracked_reread_own_file",
)


def register_action_history_tools(
    mcp: Any,
    *,
    history: ActionHistory | None = None,
    files: TrackedFileOps | None = None,
) -> dict[str, Any]:
    """Registriert den Action-History-Körper in einem bestehenden FastMCP-kompatiblen Server."""
    active_history = history or ActionHistory()
    active_files = files or TrackedFileOps(active_history)
    registered: dict[str, Any] = {}

    def register(function):
        decorated = mcp.tool()(function)
        registered[function.__name__] = decorated
        return decorated

    def history_begin_session(
        session_id: str,
        details: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Eröffnet eine Session rennsicher und schreibt höchstens ein session.begin-Ereignis."""
        return begin_session_once(active_history, session_id, details=details)

    def history_startup(
        session_id: str = "unknown-session",
        recent_limit: int = 30,
    ) -> dict[str, Any]:
        """Eröffnet die Session selbst und liefert aktuelle, vorherige und globale Aktionen."""
        return startup_session(
            active_history,
            session_id=session_id,
            recent_limit=recent_limit,
        )

    def history_recent(
        session_id: str | None = None,
        action: str | None = None,
        status: str | None = None,
        limit: int = 100,
    ) -> list[dict[str, Any]]:
        """Liest die letzten protokollierten Aktionen."""
        return active_history.list_events(
            session_id=session_id,
            action=action,
            status=status,
            limit=limit,
        )

    def history_summary(session_id: str | None = None) -> dict[str, Any]:
        """Erzeugt eine kompakte Bilanz ausschließlich aus protokollierten Aktionen."""
        return active_history.summary(session_id=session_id)

    def history_session_report(session_id: str) -> dict[str, Any]:
        """Erzeugt ein menschenlesbares Chat-Fazit ohne Dateiinhalte aus der Hash-Kette."""
        return build_session_report(active_history, session_id)

    def history_verify() -> dict[str, Any]:
        """Prüft die vollständige Hash-Kette der append-only Historie."""
        return active_history.verify()

    def history_capabilities() -> dict[str, Any]:
        """Liefert den verpflichtenden Werkzeugvertrag für die Client-Integration."""
        return {
            "actor": active_history.actor,
            "required_tools": list(REQUIRED_TOOLS),
            "history_path": str(active_history.path),
            "rule": "Alle Dateiaktionen über tracked_*; alle übrigen Aktionen über history_record_action.",
            "startup_rule": "history_startup eröffnet die Session automatisch, rennsicher und idempotent.",
            "report_rule": "history_end_session und history_session_report erzeugen das Fazit aus der Hash-Kette.",
            "integration": "register_action_history_tools(existing_mcp) bindet den Körper in den bestehenden Server ein.",
        }

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
        return active_history.append(
            action=action,
            target=target,
            status=status,
            session_id=session_id,
            completeness=completeness,
            details=details,
            parent_event_id=parent_event_id,
        )

    def history_end_session(
        session_id: str,
        details: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Schließt die Session rennsicher und liefert sofort ihr protokollbasiertes Fazit."""
        ended = end_session_once(active_history, session_id, details=details)
        return {**ended, "report": build_session_report(active_history, session_id)}

    def tracked_read_file(
        path: str,
        session_id: str = "unknown-session",
        start_line: int = 1,
        max_lines: int | None = None,
    ) -> dict[str, Any]:
        """Liest eine Werkraum-Datei und protokolliert Vollständigkeit, Hash und Umfang."""
        return active_files.read_text(
            path,
            session_id=session_id,
            start_line=start_line,
            max_lines=max_lines,
        )

    def tracked_write_file(
        path: str,
        content: str,
        session_id: str = "unknown-session",
        overwrite: bool = False,
    ) -> dict[str, Any]:
        """Schreibt atomar und protokolliert Pfad, Umfang und Hash."""
        return active_files.write_text(
            path,
            content,
            session_id=session_id,
            overwrite=overwrite,
        )

    def tracked_append_file(
        path: str,
        content: str,
        session_id: str = "unknown-session",
    ) -> dict[str, Any]:
        """Hängt Text an und protokolliert die resultierende Datei."""
        return active_files.append_text(path, content, session_id=session_id)

    def tracked_reread_own_file(
        path: str,
        session_id: str = "unknown-session",
    ) -> dict[str, Any]:
        """Liest eine gerade geschriebene Datei vollständig erneut und protokolliert dies separat."""
        return active_files.reread_text(path, session_id=session_id)

    for function in (
        history_begin_session,
        history_startup,
        history_recent,
        history_summary,
        history_session_report,
        history_verify,
        history_capabilities,
        history_record_action,
        history_end_session,
        tracked_read_file,
        tracked_write_file,
        tracked_append_file,
        tracked_reread_own_file,
    ):
        register(function)

    actual = tuple(registered)
    if actual != REQUIRED_TOOLS:
        raise RuntimeError(
            f"Werkzeugvertrag beim Registrieren abweichend: erwartet={REQUIRED_TOOLS!r}, erhalten={actual!r}"
        )

    return registered
