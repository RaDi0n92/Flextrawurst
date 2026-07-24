from __future__ import annotations

from pathlib import Path

import pytest

from tools.action_history.decorators import tracked_mcp_action
from tools.action_history.history import ActionHistory


def test_wrapped_tool_default_unknown_session_is_blocked(tmp_path: Path):
    history = ActionHistory(tmp_path / "history.jsonl", actor="GPT-5.6-sol-hoch")

    @tracked_mcp_action(history, action="legacy.inspect", target_argument="path")
    def inspect(path: str, session_id: str = "unknown-session") -> str:
        return path

    with pytest.raises(ValueError, match="echte session_id"):
        inspect("/root/werkraum")

    blocked = history.list_events(session_id="unassigned")
    assert len(blocked) == 1
    assert blocked[0]["action"] == "legacy.inspect"
    assert blocked[0]["target"] == "/root/werkraum"
    assert blocked[0]["status"] == "blocked"
    assert blocked[0]["completeness"] == "aborted"
    assert blocked[0]["details"]["reason"] == "missing_or_unknown_session_id"
    assert history.list_events(session_id="unknown-session") == []
    assert history.verify()["ok"] is True


def test_session_requirement_can_only_be_disabled_explicitly(tmp_path: Path):
    history = ActionHistory(tmp_path / "history.jsonl", actor="GPT-5.6-sol-hoch")

    @tracked_mcp_action(
        history,
        action="bootstrap.probe",
        require_session_id=False,
    )
    def bootstrap() -> str:
        return "ok"

    assert bootstrap() == "ok"
    event = history.list_events(session_id="unassigned")[-1]
    assert event["status"] == "success"
    assert event["details"]["mode"] == "sync"
