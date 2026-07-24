#!/usr/bin/env bash
set -euo pipefail

ROOT="${1:-/root/werkraum}"
VENV="${FLEXTRAWURST_ACTION_HISTORY_VENV:-$ROOT/.venv-action-history}"

cd "$ROOT"
python3 -m venv "$VENV"
"$VENV/bin/python" -m pip install --upgrade pip
"$VENV/bin/python" -m pip install -r tools/action_history/requirements.txt
"$VENV/bin/python" -m compileall -q tools/action_history
"$VENV/bin/python" -m pytest -q tools/action_history/tests
"$VENV/bin/python" -m tools.action_history.verify_install
"$VENV/bin/python" -m tools.action_history.verify_fastmcp

cat <<EOF
INSTALLATION_VERIFIED
runner=$VENV/bin/python -m tools.action_history.mcp_server
history=/root/werkraum/_gpt/session_history.jsonl
actor=GPT-5.6-sol-hoch
integration=from tools.action_history import register_action_history_tools
EOF
