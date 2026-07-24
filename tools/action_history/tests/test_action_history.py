from __future__ import annotations

import json
import os
import sys
from pathlib import Path

import pytest

PACKAGE_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = PACKAGE_ROOT.parents[1]
sys.path.insert(0, str(REPO_ROOT))

from tools.action_history import ActionHistory, HistoryIntegrityError, TrackedFileOps


def make_ops(tmp_path: Path):
    history_path = tmp_path / "history.jsonl"
    workroot = tmp_path / "werkraum"
    workroot.mkdir()
    os.environ["FLEXTRAWURST_HISTORY_ALLOWED_ROOTS"] = str(workroot)
    history = ActionHistory(history_path, actor="GPT-5.6-sol-hoch")
    return history, TrackedFileOps(history), workroot


def test_write_read_reread_and_summary(tmp_path: Path):
    history, ops, root = make_ops(tmp_path)
    target = root / "_gpt" / "spiegel.md"

    written = ops.write_text(str(target), "eins\nzwei\n", session_id="s1")
    assert written["created"] is True
    assert target.read_text(encoding="utf-8") == "eins\nzwei\n"

    read = ops.read_text(str(target), session_id="s1")
    assert read["complete"] is True
    assert read["line_count_total"] == 2

    reread = ops.reread_text(str(target), session_id="s1")
    assert reread["complete"] is True

    summary = history.summary(session_id="s1")
    assert summary["event_count"] == 3
    assert summary["by_action"] == {
        "read_file": 1,
        "reread_own_file": 1,
        "write_file": 1,
    }
    assert history.verify()["ok"] is True


def test_partial_read_is_visible_at_startup(tmp_path: Path):
    history, ops, root = make_ops(tmp_path)
    target = root / "large.md"
    target.write_text("a\nb\nc\nd\n", encoding="utf-8")

    ops.read_text(str(target), session_id="s2", start_line=2, max_lines=1)
    startup = history.startup_context(session_id="s2")
    assert len(startup["partial_or_unknown"]) == 1
    assert startup["partial_or_unknown"][0]["completeness"] == "partial"


def test_failed_action_is_logged(tmp_path: Path):
    history, ops, root = make_ops(tmp_path)
    missing = root / "missing.md"

    with pytest.raises(FileNotFoundError):
        ops.read_text(str(missing), session_id="s3")

    events = history.list_events(session_id="s3")
    assert len(events) == 1
    assert events[0]["status"] == "failed"
    assert "FileNotFoundError" in events[0]["details"]["error"]


def test_path_escape_is_rejected_without_fake_success(tmp_path: Path):
    history, ops, _ = make_ops(tmp_path)
    outside = tmp_path / "outside.txt"
    outside.write_text("nope", encoding="utf-8")

    with pytest.raises(PermissionError):
        ops.read_text(str(outside), session_id="s4")

    assert history.list_events(session_id="s4") == []


def test_history_tampering_is_detected(tmp_path: Path):
    history, _, _ = make_ops(tmp_path)
    history.append(action="one", session_id="s5")
    history.append(action="two", session_id="s5")

    lines = history.path.read_text(encoding="utf-8").splitlines()
    event = json.loads(lines[0])
    event["action"] = "manipulated"
    lines[0] = json.dumps(event, ensure_ascii=False, sort_keys=True)
    history.path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    with pytest.raises(HistoryIntegrityError):
        history.verify()


def test_existing_file_requires_explicit_overwrite(tmp_path: Path):
    history, ops, root = make_ops(tmp_path)
    target = root / "protected.md"
    target.write_text("alt", encoding="utf-8")

    with pytest.raises(FileExistsError):
        ops.write_text(str(target), "neu", session_id="s6")

    assert history.list_events(session_id="s6") == []
    overwritten = ops.write_text(str(target), "neu", session_id="s6", overwrite=True)
    assert overwritten["created"] is False
    assert target.read_text(encoding="utf-8") == "neu"
