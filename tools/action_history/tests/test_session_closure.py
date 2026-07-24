from __future__ import annotations

import os
import threading
import time
from pathlib import Path

import pytest

from tools.action_history.decorators import tracked_mcp_action
from tools.action_history.history import ActionHistory
from tools.action_history.lifecycle import (
    SessionClosedError,
    begin_session_once,
    end_session_once,
)
from tools.action_history.tracked_file_ops import TrackedFileOps


def test_closed_session_blocks_file_side_effect_and_records_audit_event(tmp_path: Path):
    root = tmp_path / "werkraum"
    root.mkdir()
    os.environ["FLEXTRAWURST_HISTORY_ALLOWED_ROOTS"] = str(root)

    history = ActionHistory(tmp_path / "history.jsonl", actor="GPT-5.6-sol-hoch")
    files = TrackedFileOps(history)
    session_id = "closed-file-session"
    first = root / "first.md"
    forbidden = root / "forbidden.md"

    begin_session_once(history, session_id)
    files.write_text(str(first), "vor ende\n", session_id=session_id)
    end_session_once(history, session_id)

    with pytest.raises(SessionClosedError, match="bereits geschlossen"):
        files.write_text(str(forbidden), "nach ende\n", session_id=session_id)

    assert first.exists()
    assert not forbidden.exists()
    assert [
        event["action"]
        for event in history.list_events(session_id=session_id, limit=20)
    ] == ["session.begin", "write_file", "session.end"]

    audit = history.list_events(session_id="system-audit", limit=20)
    assert len(audit) == 1
    assert audit[0]["action"] == "session.closed_action_blocked"
    assert audit[0]["status"] == "blocked"
    assert audit[0]["details"]["attempted_action"] == "write_file"
    assert audit[0]["details"]["closed_session_id"] == session_id
    assert history.verify()["ok"] is True


def test_closed_session_blocks_wrapped_tool_before_function_runs(tmp_path: Path):
    history = ActionHistory(tmp_path / "history.jsonl", actor="GPT-5.6-sol-hoch")
    session_id = "closed-tool-session"
    calls = []

    @tracked_mcp_action(history, action="legacy.side_effect")
    def side_effect(session_id: str) -> None:
        calls.append("executed")

    begin_session_once(history, session_id)
    end_session_once(history, session_id)

    with pytest.raises(SessionClosedError):
        side_effect(session_id)

    assert calls == []
    assert history.list_events(session_id=session_id, action="legacy.side_effect") == []
    assert history.list_events(session_id="system-audit")[-1]["status"] == "blocked"


def test_session_end_waits_for_running_tool_then_becomes_final_event(tmp_path: Path):
    history = ActionHistory(tmp_path / "history.jsonl", actor="GPT-5.6-sol-hoch")
    session_id = "race-session"
    tool_started = threading.Event()
    release_tool = threading.Event()
    end_finished = threading.Event()

    @tracked_mcp_action(history, action="slow.tool")
    def slow_tool(session_id: str) -> str:
        tool_started.set()
        if not release_tool.wait(timeout=5):
            raise TimeoutError("Testwerkzeug wurde nicht freigegeben")
        return "done"

    begin_session_once(history, session_id)

    tool_thread = threading.Thread(target=slow_tool, args=(session_id,))

    def end_worker() -> None:
        end_session_once(history, session_id)
        end_finished.set()

    end_thread = threading.Thread(target=end_worker)
    tool_thread.start()
    assert tool_started.wait(timeout=5)
    end_thread.start()

    time.sleep(0.1)
    assert not end_finished.is_set()

    release_tool.set()
    tool_thread.join(timeout=5)
    end_thread.join(timeout=5)

    assert not tool_thread.is_alive()
    assert not end_thread.is_alive()
    assert end_finished.is_set()
    events = history.list_events(session_id=session_id, limit=20)
    assert [event["action"] for event in events] == [
        "session.begin",
        "slow.tool",
        "session.end",
    ]
    assert events[-1]["details"]["summary"]["by_action"] == {
        "session.begin": 1,
        "slow.tool": 1,
    }
    assert history.verify()["ok"] is True
