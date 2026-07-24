from __future__ import annotations

from pathlib import Path

from tools.action_history.history import ActionHistory
from tools.action_history.lifecycle import startup_session


def test_startup_opens_session_once_and_keeps_previous_context(tmp_path: Path):
    history = ActionHistory(tmp_path / "history.jsonl", actor="GPT-5.6-sol-hoch")

    history.begin_session("old")
    history.append(action="build", target="old-target", session_id="old")
    history.end_session("old")

    first = startup_session(history, session_id="new", recent_limit=30)
    second = startup_session(history, session_id="new", recent_limit=30)

    assert first["session_begin"]["created"] is True
    assert second["session_begin"]["created"] is False
    assert first["previous_session_id"] == "old"
    assert [event["action"] for event in first["previous_session_actions"]] == [
        "session.begin",
        "build",
        "session.end",
    ]
    assert [event["action"] for event in first["current_session_actions"]] == [
        "session.begin",
    ]
    assert [event["action"] for event in second["current_session_actions"]] == [
        "session.begin",
    ]
    assert history.verify()["ok"] is True
