from __future__ import annotations

import os
import tempfile
from pathlib import Path

from mcp.server.fastmcp import FastMCP

from .history import ActionHistory
from .toolset import REQUIRED_TOOLS, register_action_history_tools
from .tracked_file_ops import TrackedFileOps


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="flextrawurst-fastmcp-") as tmp:
        root = Path(tmp)
        os.environ["FLEXTRAWURST_HISTORY_ALLOWED_ROOTS"] = str(root)
        history = ActionHistory(root / "history.jsonl", actor="GPT-5.6-sol-hoch")
        files = TrackedFileOps(history)
        server = FastMCP("flextrawurst-action-history-verification")
        registered = register_action_history_tools(server, history=history, files=files)

        if tuple(registered) != REQUIRED_TOOLS:
            raise RuntimeError(
                f"FastMCP-Werkzeugvertrag abweichend: {tuple(registered)!r}"
            )

        startup = registered["history_startup"]("fastmcp-verification")
        second = registered["history_startup"]("fastmcp-verification")
        report = registered["history_end_session"]("fastmcp-verification")

        if not startup["session_begin"]["created"]:
            raise RuntimeError("Erster FastMCP-Sessionstart wurde nicht erzeugt")
        if second["session_begin"]["created"]:
            raise RuntimeError("Zweiter FastMCP-Sessionstart erzeugte ein Duplikat")
        if not report["created"] or not report["report"]["integrity"]["ok"]:
            raise RuntimeError("FastMCP-Sessionabschluss oder Bericht ist ungültig")

        print(
            f"FASTMCP_VERIFIED tools={len(REQUIRED_TOOLS)} "
            f"events={report['report']['event_count']}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
