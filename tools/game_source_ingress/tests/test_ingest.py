from __future__ import annotations

import hashlib
import json
import zipfile
from pathlib import Path

import pytest

from tools.game_source_ingress.ingest import IngressError, run


def make_zip(path: Path, members: dict[str, bytes]) -> tuple[int, str]:
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for name, data in members.items():
            zf.writestr(name, data)
    data = path.read_bytes()
    return len(data), hashlib.sha256(data).hexdigest()


def write_manifest(path: Path, archive: Path, size: int, digest: str, expected_md: int = 1) -> None:
    payload = {
        "manifest_version": "test",
        "target_root": str(path.parent / "target"),
        "default_queue": str(path.parent / "queue"),
        "archives": [
            {
                "filename": archive.name,
                "size_bytes": size,
                "sha256": digest,
                "extract_to": "sources/markdown/333md",
                "strip_top_level": True,
                "expected_markdown_files": expected_md,
            }
        ],
    }
    path.write_text(json.dumps(payload), encoding="utf-8")


def test_audit_and_apply_are_idempotent(tmp_path: Path) -> None:
    queue = tmp_path / "queue"
    target = tmp_path / "target"
    queue.mkdir()
    target.mkdir()
    (target / "GAME_MANIFEST.json").write_text('{"old": true}\n', encoding="utf-8")
    archive = queue / "source.zip"
    size, digest = make_zip(archive, {"wrapper/a.md": b"eins", "wrapper/data.json": b"{}"})
    manifest = tmp_path / "manifest.json"
    write_manifest(manifest, archive, size, digest)

    audit = run(queue, target, manifest, apply=False)
    assert audit["status"] == "audit_ok"
    applied = run(queue, target, manifest, apply=True)
    assert applied["status"] == "applied_ok"
    assert (target / "sources/markdown/333md/a.md").read_bytes() == b"eins"
    second = run(queue, target, manifest, apply=True)
    assert second["archives"][0]["archive_action"] == "already_present"
    assert second["archives"][0]["extract"]["identical_files"] == 2


def test_refuses_changed_destination(tmp_path: Path) -> None:
    queue = tmp_path / "queue"
    target = tmp_path / "target"
    queue.mkdir()
    target.mkdir()
    archive = queue / "source.zip"
    size, digest = make_zip(archive, {"wrapper/a.md": b"eins"})
    manifest = tmp_path / "manifest.json"
    write_manifest(manifest, archive, size, digest)
    run(queue, target, manifest, apply=True)
    (target / "sources/markdown/333md/a.md").write_bytes(b"anders")
    with pytest.raises(IngressError, match="Extraktionskonflikt"):
        run(queue, target, manifest, apply=True)


def test_rejects_zip_traversal(tmp_path: Path) -> None:
    queue = tmp_path / "queue"
    target = tmp_path / "target"
    queue.mkdir()
    target.mkdir()
    archive = queue / "source.zip"
    size, digest = make_zip(archive, {"wrapper/../escape.md": b"nein"})
    manifest = tmp_path / "manifest.json"
    write_manifest(manifest, archive, size, digest)
    with pytest.raises(IngressError, match="Unsicherer ZIP-Pfad"):
        run(queue, target, manifest, apply=True)
