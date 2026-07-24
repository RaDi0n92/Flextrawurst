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

        startup = registered["history_startup"]()
        session_id = startup["session_id"]
        second = registered["history_startup"](session_id)
        target = root / "_gpt" / "fastmcp-proof.md"
        registered["tracked_write_file"](
            str(target),
            "proof\n",
            session_id,
        )
        registered["tracked_read_file"](str(target), session_id)
        registered["tracked_reread_own_file"](str(target), session_id)
        report = registered["history_end_session"](session_id)

        if not startup["generated_session_id"] or session_id == "unknown-session":
            raise RuntimeError("FastMCP-Start hat keine echte Session-ID erzeugt")
        if not startup["session_begin"]["created"]:
            raise RuntimeError("Erster FastMCP-Sessionstart wurde nicht erzeugt")
        if second["session_begin"]["created"]:
            raise RuntimeError("Zweiter FastMCP-Sessionstart erzeugte ein Duplikat")
        if not report["created"] or not report["report"]["integrity"]["ok"]:
            raise RuntimeError("FastMCP-Sessionabschluss oder Bericht ist ungültig")
        if report["report"]["event_count"] != 5:
            raise RuntimeError(
                f"FastMCP-Gegenprobe erwartete 5 Ereignisse, erhielt {report['report']['event_count']}"
            )

        print(
            f"FASTMCP_VERIFIED tools={len(REQUIRED_TOOLS)} "
            f"session={session_id} events={report['report']['event_count']}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
