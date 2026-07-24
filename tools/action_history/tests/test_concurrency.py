from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from tools.action_history import ActionHistory


def test_parallel_appends_keep_one_valid_chain(tmp_path: Path):
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
    assert verification["events"] == 200
    assert len(history.list_events(session_id="parallel-session", limit=500)) == 200
