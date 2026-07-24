from __future__ import annotations

import json
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from tools.action_history import ActionHistory


def test_parallel_appends_keep_one_valid_chain_and_checkpoint(tmp_path: Path):
    history = ActionHistory(tmp_path / "parallel.jsonl", actor="GPT-5.6-sol-hoch")

    def append_one(index: int):
        return history.append(
            action="parallel",
            target=str(index),
            session_id="parallel-session",
        )

    with ThreadPoolExecutor(max_workers=16) as pool:
        list(pool.map(append_one, range(200)))

    verification = history.verify()
    events = history.list_events(session_id="parallel-session", limit=500)
    checkpoint = json.loads(history.checkpoint_path.read_text(encoding="utf-8"))

    assert verification["events"] == 200
    assert verification["checkpoint_status"] == "verified"
    assert len(events) == 200
    assert checkpoint["event_count"] == 200
    assert checkpoint["last_hash"] == verification["last_hash"]
    assert checkpoint["last_event_id"] == events[-1]["event_id"]
