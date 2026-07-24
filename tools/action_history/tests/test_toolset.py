from __future__ import annotations

import os
from pathlib import Path

from tools.action_history.history import ActionHistory
from tools.action_history.toolset import REQUIRED_TOOLS, register_action_history_tools
from tools.action_history.tracked_file_ops import TrackedFileOps


class FakeMCP:
    def __init__(self):
        self.tools = {}

    def tool(self):
        def decorator(function):
            if function.__name__ in self.tools:
                raise RuntimeError(f"Werkzeug doppelt registriert: {function.__name__}")
            self.tools[function.__name__] = function
            return function

        return decorator


def test_toolset_grows_into_existing_mcp_and_records_real_actions(tmp_path: Path):
    root = tmp_path / "werkraum"
    root.mkdir()
    os.environ["FLEXTRAWURST_HISTORY_ALLOWED_ROOTS"] = str(root)

    history = ActionHistory(tmp_path / "history.jsonl", actor="GPT-5.6-sol-hoch")
    files = TrackedFileOps(history)
    existing_mcp = FakeMCP()

    registered = register_action_history_tools(
        existing_mcp,
        history=history,
        files=files,
    )

    assert tuple(registered) == REQUIRED_TOOLS
    assert tuple(existing_mcp.tools) == REQUIRED_TOOLS

    startup = existing_mcp.tools["history_startup"]("session-a")
    second_startup = existing_mcp.tools["history_startup"]("session-a")
    assert startup["session_begin"]["created"] is True
    assert second_startup["session_begin"]["created"] is False

    target = root / "_gpt" / "proof.md"
    existing_mcp.tools["tracked_write_file"](
        str(target),
        "gebaut\n",
        session_id="session-a",
    )
    existing_mcp.tools["tracked_read_file"](
        str(target),
        session_id="session-a",
    )
    existing_mcp.tools["tracked_reread_own_file"](
        str(target),
        session_id="session-a",
    )
    existing_mcp.tools["history_record_action"](
        "connector.probe",
        "session-a",
        target="@flextrawurst",
        details={"result": "visible"},
    )
    ended = existing_mcp.tools["history_end_session"]("session-a")

    assert ended["created"] is True
    summary = history.summary(session_id="session-a")
    assert summary["by_action"] == {
        "connector.probe": 1,
        "read_file": 1,
        "reread_own_file": 1,
        "session.begin": 1,
        "session.end": 1,
        "write_file": 1,
    }
    assert history.verify()["ok"] is True


def test_duplicate_registration_is_rejected(tmp_path: Path):
    history = ActionHistory(tmp_path / "history.jsonl", actor="GPT-5.6-sol-hoch")
    existing_mcp = FakeMCP()

    register_action_history_tools(existing_mcp, history=history)

    try:
        register_action_history_tools(existing_mcp, history=history)
    except RuntimeError as exc:
        assert "doppelt registriert" in str(exc)
    else:
        raise AssertionError("Doppelte Werkzeugregistrierung wurde nicht blockiert")
