from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from tools.action_history.history import ActionHistory
from tools.action_history.lifecycle import begin_session_once, end_session_once


def test_parallel_session_begin_and_end_create_exactly_one_event_each(tmp_path: Path):
    history = ActionHistory(tmp_path / "history.jsonl", actor="GPT-5.6-sol-hoch")

    with ThreadPoolExecutor(max_workers=20) as pool:
        begin_results = list(
            pool.map(
                lambda _: begin_session_once(history, "parallel-lifecycle"),
                range(50),
            )
        )

    assert sum(1 for result in begin_results if result["created"]) == 1
    assert len(history.list_events(session_id="parallel-lifecycle", action="session.begin")) == 1

    history.append(action="work", session_id="parallel-lifecycle")

    with ThreadPoolExecutor(max_workers=20) as pool:
        end_results = list(
            pool.map(
                lambda _: end_session_once(history, "parallel-lifecycle"),
                range(50),
            )
        )

    assert sum(1 for result in end_results if result["created"]) == 1
    assert len(history.list_events(session_id="parallel-lifecycle", action="session.end")) == 1
    assert history.summary(session_id="parallel-lifecycle")["event_count"] == 3
    assert history.verify()["ok"] is True
