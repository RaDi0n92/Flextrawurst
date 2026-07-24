from __future__ import annotations

import os
from pathlib import Path

from tools.action_history.history import ActionHistory
from tools.action_history.reporting import build_session_report
from tools.action_history.tracked_file_ops import TrackedFileOps


def test_report_is_derived_from_real_read_write_and_failure_events(tmp_path: Path):
    root = tmp_path / "werkraum"
    root.mkdir()
    os.environ["FLEXTRAWURST_HISTORY_ALLOWED_ROOTS"] = str(root)

    history = ActionHistory(tmp_path / "history.jsonl", actor="GPT-5.6-sol-hoch")
    files = TrackedFileOps(history)
    session_id = "report-session"
    target = root / "_gpt" / "report-proof.md"

    history.begin_session(session_id)
    files.write_text(str(target), "eins\nzwei\n", session_id=session_id)
    files.read_text(str(target), session_id=session_id)
    files.read_text(str(target), session_id=session_id, start_line=2, max_lines=1)
    try:
        files.read_text(str(root / "missing.md"), session_id=session_id)
    except FileNotFoundError:
        pass
    history.end_session(session_id)

    report = build_session_report(history, session_id)

    assert report["event_count"] == 6
    assert report["failure_count"] == 1
    assert report["incomplete_count"] == 1
    assert report["integrity"]["ok"] is True
    assert "# Tätigkeitsbericht — report-session" in report["markdown"]
    assert "## Gelesen" in report["markdown"]
    assert "## Geschrieben" in report["markdown"]
    assert "missing.md" in report["markdown"]
    assert "partial" in report["markdown"]
    assert "eins" not in report["markdown"]
    assert "zwei" not in report["markdown"]
