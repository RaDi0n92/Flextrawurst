from __future__ import annotations

import json
import os
import tempfile
from pathlib import Path

from .history import ActionHistory
from .tracked_file_ops import TrackedFileOps


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="flextrawurst-action-history-") as tmp:
        root = Path(tmp) / "werkraum"
        root.mkdir()
        os.environ["FLEXTRAWURST_HISTORY_ALLOWED_ROOTS"] = str(root)
        history = ActionHistory(Path(tmp) / "history.jsonl", actor="GPT-5.6-sol-hoch")
        ops = TrackedFileOps(history)
        target = root / "_gpt" / "install_probe.md"
        history.begin_session("install-verification")
        ops.write_text(str(target), "probe\n", session_id="install-verification")
        ops.read_text(str(target), session_id="install-verification")
        ops.reread_text(str(target), session_id="install-verification")
        history.end_session("install-verification")
        verification = history.verify()
        summary = history.summary(session_id="install-verification")
        if verification["events"] != 5 or summary["event_count"] != 5:
            raise RuntimeError("Installations-Gegenprobe hat nicht exakt fünf Ereignisse erzeugt")
        print(json.dumps({"ok": True, "verification": verification, "summary": summary}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
