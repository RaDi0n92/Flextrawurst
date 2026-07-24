from __future__ import annotations

import os

from .history import ActionHistory
from .toolset import REQUIRED_TOOLS, register_action_history_tools
from .tracked_file_ops import TrackedFileOps

try:
    from mcp.server.fastmcp import FastMCP
except ImportError as exc:  # pragma: no cover
    raise SystemExit(
        "Das Python-Paket 'mcp' fehlt. Installiere es im VPS-Venv, bevor der Server gestartet wird."
    ) from exc

mcp = FastMCP("flextrawurst-action-history")
history = ActionHistory()
files = TrackedFileOps(history)
REGISTERED_TOOLS = register_action_history_tools(
    mcp,
    history=history,
    files=files,
)


if __name__ == "__main__":
    transport = os.environ.get("FLEXTRAWURST_ACTION_HISTORY_TRANSPORT", "stdio")
    mcp.run(transport=transport)
