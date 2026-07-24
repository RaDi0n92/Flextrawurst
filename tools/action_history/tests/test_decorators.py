from __future__ import annotations

import asyncio
from pathlib import Path

import pytest

from tools.action_history.decorators import tracked_mcp_action
from tools.action_history.history import ActionHistory


def test_sync_tool_success_is_recorded_with_target_and_duration(tmp_path: Path):
    history = ActionHistory(tmp_path / "history.jsonl", actor="GPT-5.6-sol-hoch")

    @tracked_mcp_action(
        history,
        action="vps.inspect",
        target_argument="path",
        static_details={"source": "existing-mcp"},
    )
    def inspect(path: str, session_id: str = "unknown-session") -> dict[str, str]:
        return {"path": path}

    result = inspect("/root/werkraum", session_id="sync-session")
    event = history.list_events(session_id="sync-session")[-1]

    assert result == {"path": "/root/werkraum"}
    assert event["action"] == "vps.inspect"
    assert event["target"] == "/root/werkraum"
    assert event["status"] == "success"
    assert event["details"]["mode"] == "sync"
    assert event["details"]["source"] == "existing-mcp"
    assert event["details"]["result_type"] == "dict"
    assert event["details"]["duration_ms"] >= 0


def test_sync_tool_failure_is_recorded_with_error_and_duration(tmp_path: Path):
    history = ActionHistory(tmp_path / "history.jsonl", actor="GPT-5.6-sol-hoch")

    @tracked_mcp_action(history, action="vps.break", target_argument="path")
    def break_tool(path: str, session_id: str = "unknown-session") -> None:
        raise RuntimeError("absichtlicher Gegenfehler")

    with pytest.raises(RuntimeError, match="absichtlicher Gegenfehler"):
        break_tool("/root/kaputt", session_id="failed-session")

    event = history.list_events(session_id="failed-session")[-1]
    assert event["status"] == "failed"
    assert event["target"] == "/root/kaputt"
    assert "absichtlicher Gegenfehler" in event["details"]["error"]
    assert event["details"]["result_type"] == "exception"
    assert event["details"]["duration_ms"] >= 0


def test_async_tool_success_and_failure_are_both_recorded(tmp_path: Path):
    history = ActionHistory(tmp_path / "history.jsonl", actor="GPT-5.6-sol-hoch")

    @tracked_mcp_action(history, action="async.success", target_argument="name")
    async def succeed(name: str, session_id: str = "unknown-session") -> str:
        await asyncio.sleep(0)
        return name.upper()

    @tracked_mcp_action(history, action="async.failure", target_argument="name")
    async def fail(name: str, session_id: str = "unknown-session") -> None:
        await asyncio.sleep(0)
        raise ValueError(name)

    assert asyncio.run(succeed("wesen", session_id="async-session")) == "WESEN"
    with pytest.raises(ValueError, match="bruch"):
        asyncio.run(fail("bruch", session_id="async-session"))

    events = history.list_events(session_id="async-session")
    assert [event["status"] for event in events] == ["success", "failed"]
    assert [event["details"]["mode"] for event in events] == ["async", "async"]
    assert events[0]["details"]["result_type"] == "str"
    assert events[1]["details"]["result_type"] == "exception"
    assert history.verify()["ok"] is True
