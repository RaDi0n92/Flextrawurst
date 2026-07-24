from __future__ import annotations

from collections import Counter
from typing import Any

from .history import ActionHistory


def _clean(value: Any) -> str:
    return "" if value is None else str(value).replace("|", "\\|").replace("\n", " ")


def build_session_report(history: ActionHistory, session_id: str) -> dict[str, Any]:
    events = history.list_events(session_id=session_id, limit=5000)
    integrity = history.verify()
    counts = Counter(str(event.get("action") or "unknown") for event in events)
    reads = [event for event in events if event.get("action") in {"read_file", "reread_own_file"}]
    writes = [event for event in events if event.get("action") in {"write_file", "append_file"}]
    failures = [event for event in events if event.get("status") != "success"]
    incomplete = [event for event in events if event.get("completeness") in {"partial", "unknown", "aborted"}]

    lines = [
        f"# Tätigkeitsbericht — {session_id}",
        "",
        f"- Akteur: `{history.actor}`",
        f"- Ereignisse: **{len(events)}**",
        f"- Hash-Kette: **{'intakt' if integrity.get('ok') else 'gebrochen'}**",
        f"- Letzter Hash: `{integrity.get('last_hash') or 'noch keiner'}`",
        "",
        "## Aktionsbilanz",
    ]
    lines.extend(f"- `{name}`: {count}" for name, count in sorted(counts.items()))
    if not counts:
        lines.append("- Keine protokollierten Aktionen.")

    lines.extend(["", "## Gelesen"])
    for event in reads:
        details = event.get("details") or {}
        lines.append(
            f"- `{event.get('action')}` `{event.get('target')}` — {event.get('completeness')}, "
            f"{details.get('returned_line_count', '?')}/{details.get('line_count_total', '?')} Zeilen, "
            f"SHA-256 `{details.get('sha256', 'unbekannt')}`"
        )
    if not reads:
        lines.append("- Keine Lesung protokolliert.")

    lines.extend(["", "## Geschrieben"])
    for event in writes:
        details = event.get("details") or {}
        size = details.get("bytes_written", details.get("bytes_appended", "?"))
        lines.append(
            f"- `{event.get('action')}` `{event.get('target')}` — {size} Bytes, "
            f"SHA-256 `{details.get('sha256', 'unbekannt')}`"
        )
    if not writes:
        lines.append("- Keine Schreibaktion protokolliert.")

    lines.extend(["", "## Fehlgeschlagen, blockiert oder unvollständig"])
    for event in failures + [item for item in incomplete if item not in failures]:
        details = event.get("details") or {}
        lines.append(
            f"- **{event.get('status')}** `{event.get('action')}` `{event.get('target')}` — "
            f"{event.get('completeness') or ''} {_clean(details.get('error') or details.get('reason'))}".rstrip()
        )
    if not failures and not incomplete:
        lines.append("- Keine problematische Aktion.")

    lines.extend([
        "",
        "## Chronologie",
        "",
        "| Zeitpunkt UTC | Status | Aktion | Ziel | Vollständigkeit |",
        "|---|---|---|---|---|",
    ])
    for event in events:
        lines.append(
            f"| {_clean(event.get('timestamp_utc'))} | {_clean(event.get('status'))} | "
            f"{_clean(event.get('action'))} | {_clean(event.get('target'))} | "
            f"{_clean(event.get('completeness'))} |"
        )

    return {
        "session_id": session_id,
        "summary": history.summary(session_id=session_id),
        "integrity": integrity,
        "markdown": "\n".join(lines).rstrip() + "\n",
        "event_count": len(events),
        "failure_count": len(failures),
        "incomplete_count": len(incomplete),
    }
