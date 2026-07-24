from __future__ import annotations

import json
from pathlib import Path

import pytest

from tools.action_history.history import ActionHistory, HistoryIntegrityError


def make_history(tmp_path: Path) -> ActionHistory:
    history = ActionHistory(tmp_path / "history.jsonl", actor="GPT-5.6-sol-hoch")
    history.append(action="one", session_id="checkpoint-session")
    history.append(action="two", session_id="checkpoint-session")
    history.append(action="three", session_id="checkpoint-session")
    return history


def test_empty_history_may_start_without_checkpoint(tmp_path: Path):
    history = ActionHistory(tmp_path / "history.jsonl", actor="GPT-5.6-sol-hoch")

    verification = history.verify()

    assert verification["ok"] is True
    assert verification["events"] == 0
    assert verification["checkpoint_status"] == "missing-empty"
    assert not history.checkpoint_path.exists()


def test_checkpoint_is_created_and_matches_chain_tail(tmp_path: Path):
    history = make_history(tmp_path)

    verification = history.verify()
    checkpoint = json.loads(history.checkpoint_path.read_text(encoding="utf-8"))

    assert verification["checkpoint_status"] == "verified"
    assert verification["events"] == 3
    assert checkpoint["event_count"] == 3
    assert checkpoint["last_hash"] == verification["last_hash"]
    assert checkpoint["last_event_id"] == history.list_events(limit=1)[-1]["event_id"]


def test_clean_tail_truncation_is_detected_even_when_remaining_chain_is_valid(tmp_path: Path):
    history = make_history(tmp_path)
    lines = history.path.read_text(encoding="utf-8").splitlines()
    history.path.write_text("\n".join(lines[:-1]) + "\n", encoding="utf-8")

    with pytest.raises(HistoryIntegrityError, match="Checkpoint-Abweichung"):
        history.verify()


def test_rehashed_checkpoint_lie_is_still_rejected(tmp_path: Path):
    history = make_history(tmp_path)
    checkpoint = json.loads(history.checkpoint_path.read_text(encoding="utf-8"))
    checkpoint["event_count"] = 999
    checkpoint.pop("checkpoint_hash")
    checkpoint["checkpoint_hash"] = history._calculate_hash(checkpoint)
    history.checkpoint_path.write_text(
        json.dumps(checkpoint, ensure_ascii=False, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    with pytest.raises(HistoryIntegrityError, match="event_count"):
        history.verify()


def test_missing_checkpoint_blocks_existing_history_and_future_append(tmp_path: Path):
    history = make_history(tmp_path)
    history.checkpoint_path.unlink()

    with pytest.raises(HistoryIntegrityError, match="Checkpoint fehlt"):
        history.verify()

    with pytest.raises(HistoryIntegrityError, match="Checkpoint fehlt"):
        history.append(action="four", session_id="checkpoint-session")

    assert len(history.path.read_text(encoding="utf-8").splitlines()) == 3


def test_corrupted_checkpoint_hash_is_detected(tmp_path: Path):
    history = make_history(tmp_path)
    checkpoint = json.loads(history.checkpoint_path.read_text(encoding="utf-8"))
    checkpoint["last_hash"] = "0" * 64
    history.checkpoint_path.write_text(
        json.dumps(checkpoint, ensure_ascii=False, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    with pytest.raises(HistoryIntegrityError, match="Checkpoint-Hash"):
        history.verify()
