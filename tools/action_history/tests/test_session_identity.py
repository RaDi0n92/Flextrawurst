from __future__ import annotations

import os
from pathlib import Path

import pytest

from tools.action_history.history import ActionHistory
from tools.action_history.lifecycle import startup_session
from tools.action_history.tracked_file_ops import TrackedFileOps


def test_startup_without_id_generates_one_real_isolated_session(tmp_path: Path):
    history = ActionHistory(tmp_path / "history.jsonl", actor="GPT-5.6-sol-hoch")

    startup = startup_session(history)
    generated_id = startup["session_id"]

    assert startup["generated_session_id"] is True
    assert generated_id.startswith("chatgpt-")
    assert generated_id != "unknown-session"
    assert history.list_events(session_id=generated_id, action="session.begin")
    assert history.list_events(session_id="unknown-session") == []


def test_unknown_session_is_blocked_before_file_access(tmp_path: Path):
    root = tmp_path / "werkraum"
    root.mkdir()
    os.environ["FLEXTRAWURST_HISTORY_ALLOWED_ROOTS"] = str(root)

    history = ActionHistory(tmp_path / "history.jsonl", actor="GPT-5.6-sol-hoch")
    files = TrackedFileOps(history)
    target = root / "exists.md"
    target.write_text("sichtbar", encoding="utf-8")

    with pytest.raises(ValueError, match="echte session_id"):
        files.read_text(str(target), session_id="unknown-session")

    blocked = history.list_events(session_id="unassigned")
    assert len(blocked) == 1
    assert blocked[0]["status"] == "blocked"
    assert blocked[0]["completeness"] == "aborted"
    assert blocked[0]["details"]["reason"] == "missing_or_unknown_session_id"
    assert history.list_events(session_id="unknown-session") == []
    assert history.verify()["ok"] is True
