from __future__ import annotations

from pathlib import Path

from tools.action_history.history import ActionHistory
from tools.action_history.lifecycle import (
    begin_session_once,
    end_session_once,
    startup_session,
)


def test_audit_and_unassigned_events_never_replace_previous_real_session(tmp_path: Path):
    history = ActionHistory(tmp_path / "history.jsonl", actor="GPT-5.6-sol-hoch")

    begin_session_once(history, "real-old")
    history.append(action="build", target="welt", session_id="real-old")
    end_session_once(history, "real-old")
    history.append(
        action="session.closed_action_blocked",
        target="real-old",
        status="blocked",
        session_id="system-audit",
        completeness="aborted",
    )
    history.append(
        action="read_file",
        target="ohne-session.md",
        status="blocked",
        session_id="unassigned",
        completeness="aborted",
    )

    startup = startup_session(history, session_id="real-new")

    assert startup["previous_session_id"] == "real-old"
    assert [event["action"] for event in startup["previous_session_actions"]] == [
        "session.begin",
        "build",
        "session.end",
    ]
    assert {
        event["session_id"] for event in startup["failed_or_blocked"]
    } == {"system-audit", "unassigned"}


def test_startup_with_closed_session_id_creates_fresh_session(tmp_path: Path):
    history = ActionHistory(tmp_path / "history.jsonl", actor="GPT-5.6-sol-hoch")

    begin_session_once(history, "already-closed")
    history.append(action="work", session_id="already-closed")
    end_session_once(history, "already-closed")

    startup = startup_session(history, session_id="already-closed")
    fresh_id = startup["session_id"]

    assert startup["generated_session_id"] is True
    assert startup["replaced_closed_session_id"] == "already-closed"
    assert fresh_id != "already-closed"
    assert fresh_id.startswith("chatgpt-")
    assert startup["previous_session_id"] == "already-closed"
    assert [event["action"] for event in startup["current_session_actions"]] == [
        "session.begin",
    ]
    assert [event["action"] for event in startup["previous_session_actions"]] == [
        "session.begin",
        "work",
        "session.end",
    ]
    assert history.verify()["ok"] is True
