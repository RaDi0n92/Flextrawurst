#!/usr/bin/env python3
"""Kollisionssicherer Einzug ausgewählter Flextrawurst-Spielquellen."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import sys
import tempfile
import zipfile
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
from typing import Any

HERE = Path(__file__).resolve().parent
DEFAULT_MANIFEST = HERE / "manifest.json"
ARCHIVE_DEST_REL = Path("sources/original_archives")
REPORT_REL = Path("SOURCE_INGRESS_REPORT.json")


class IngressError(RuntimeError):
    pass


@dataclass(frozen=True)
class ArchiveSpec:
    filename: str
    size_bytes: int
    sha256: str
    extract_to: str
    strip_top_level: bool = False
    expected_markdown_files: int | None = None


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_manifest(path: Path) -> tuple[dict[str, Any], list[ArchiveSpec]]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    specs = [ArchiveSpec(**item) for item in raw["archives"]]
    return raw, specs


def safe_member_relative(name: str, strip_top_level: bool) -> Path | None:
    pure = PurePosixPath(name)
    if pure.is_absolute() or ".." in pure.parts:
        raise IngressError(f"Unsicherer ZIP-Pfad: {name}")
    parts = list(pure.parts)
    if strip_top_level:
        if len(parts) <= 1:
            return None
        parts = parts[1:]
    if not parts:
        return None
    return Path(*parts)


def atomic_copy_verified(source: Path, destination: Path, expected_sha256: str) -> str:
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.exists():
        current = sha256_file(destination)
        if current == expected_sha256:
            return "already_present"
        raise IngressError(f"Zielkonflikt mit abweichendem Hash: {destination}")

    tmp = destination.with_name(destination.name + ".partial")
    if tmp.exists():
        tmp.unlink()
    with source.open("rb") as src, tmp.open("xb") as dst:
        shutil.copyfileobj(src, dst, length=1024 * 1024)
        dst.flush()
        os.fsync(dst.fileno())
    copied_hash = sha256_file(tmp)
    if copied_hash != expected_sha256:
        tmp.unlink(missing_ok=True)
        raise IngressError(f"Hash nach Kopie falsch: {destination.name}")
    os.replace(tmp, destination)
    return "copied"


def extract_verified(archive: Path, destination: Path, strip_top_level: bool) -> dict[str, int]:
    destination.mkdir(parents=True, exist_ok=True)
    extracted = 0
    identical = 0
    directories = 0
    with zipfile.ZipFile(archive) as zf:
        bad = zf.testzip()
        if bad is not None:
            raise IngressError(f"Defekter ZIP-Eintrag in {archive.name}: {bad}")
        for info in zf.infolist():
            relative = safe_member_relative(info.filename, strip_top_level)
            if relative is None:
                continue
            target = destination / relative
            if info.is_dir():
                target.mkdir(parents=True, exist_ok=True)
                directories += 1
                continue
            target.parent.mkdir(parents=True, exist_ok=True)
            with zf.open(info, "r") as src:
                data = src.read()
            incoming_hash = hashlib.sha256(data).hexdigest()
            if target.exists():
                if sha256_file(target) == incoming_hash:
                    identical += 1
                    continue
                raise IngressError(f"Extraktionskonflikt: {target}")
            fd, temp_name = tempfile.mkstemp(prefix=target.name + ".", suffix=".partial", dir=target.parent)
            try:
                with os.fdopen(fd, "wb") as handle:
                    handle.write(data)
                    handle.flush()
                    os.fsync(handle.fileno())
                os.replace(temp_name, target)
            except Exception:
                Path(temp_name).unlink(missing_ok=True)
                raise
            extracted += 1
    return {"extracted_files": extracted, "identical_files": identical, "directories": directories}


def patch_game_manifest(target_root: Path, ingress_summary: dict[str, Any]) -> str:
    path = target_root / "GAME_MANIFEST.json"
    if not path.exists():
        return "not_present"
    try:
        current = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        raise IngressError(f"GAME_MANIFEST.json ist nicht gültig: {exc}") from exc
    if not isinstance(current, dict):
        raise IngressError("GAME_MANIFEST.json muss ein JSON-Objekt sein")
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    backup = path.with_name(f"GAME_MANIFEST.before_source_ingress.{stamp}.json")
    shutil.copy2(path, backup)
    current["source_ingress"] = ingress_summary
    temp = path.with_suffix(".json.partial")
    temp.write_text(json.dumps(current, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    os.replace(temp, path)
    return str(backup)


def run(queue: Path, target_root: Path, manifest_path: Path, apply: bool) -> dict[str, Any]:
    raw, specs = load_manifest(manifest_path)
    result: dict[str, Any] = {
        "status": "audit_ok",
        "applied": apply,
        "started_at_utc": datetime.now(timezone.utc).isoformat(),
        "queue": str(queue),
        "target_root": str(target_root),
        "archives": [],
    }

    for spec in specs:
        source = queue / spec.filename
        item: dict[str, Any] = {"filename": spec.filename}
        if not source.is_file():
            raise IngressError(f"Quelle fehlt: {source}")
        actual_size = source.stat().st_size
        actual_hash = sha256_file(source)
        item.update(size_bytes=actual_size, sha256=actual_hash)
        if actual_size != spec.size_bytes:
            raise IngressError(f"Größe falsch für {spec.filename}: {actual_size} != {spec.size_bytes}")
        if actual_hash != spec.sha256:
            raise IngressError(f"SHA256 falsch für {spec.filename}")
        with zipfile.ZipFile(source) as zf:
            bad = zf.testzip()
            if bad is not None:
                raise IngressError(f"ZIP defekt {spec.filename}: {bad}")
            md_count_in_zip = sum(
                1 for info in zf.infolist() if not info.is_dir() and info.filename.lower().endswith(".md")
            )
        item["zip_markdown_files"] = md_count_in_zip
        if spec.expected_markdown_files is not None and md_count_in_zip != spec.expected_markdown_files:
            raise IngressError(
                f"Markdown-Anzahl falsch für {spec.filename}: {md_count_in_zip} != {spec.expected_markdown_files}"
            )
        if apply:
            archive_destination = target_root / ARCHIVE_DEST_REL / spec.filename
            item["archive_action"] = atomic_copy_verified(source, archive_destination, spec.sha256)
            extract_destination = target_root / spec.extract_to
            item["extract"] = extract_verified(archive_destination, extract_destination, spec.strip_top_level)
        result["archives"].append(item)

    if apply:
        verified_markdown_targets: dict[str, int] = {}
        for spec in specs:
            if spec.expected_markdown_files is None:
                continue
            markdown_root = target_root / spec.extract_to
            markdown_count = sum(1 for path in markdown_root.rglob("*.md") if path.is_file())
            if markdown_count != spec.expected_markdown_files:
                raise IngressError(
                    f"Ziel {markdown_root} enthält nach Einzug {markdown_count} "
                    f"statt {spec.expected_markdown_files} Markdown-Dateien"
                )
            verified_markdown_targets[spec.extract_to] = markdown_count
        result["verified_markdown_targets"] = verified_markdown_targets
        result["markdown_333_target_count"] = verified_markdown_targets.get("sources/markdown/333md")
        result["status"] = "applied_ok"
        result["completed_at_utc"] = datetime.now(timezone.utc).isoformat()
        target_root.mkdir(parents=True, exist_ok=True)
        report_path = target_root / REPORT_REL
        report_path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        summary = {
            "status": result["status"],
            "completed_at_utc": result["completed_at_utc"],
            "archive_count": len(specs),
            "markdown_333_target_count": result.get("markdown_333_target_count"),
            "report": str(report_path),
            "manifest_version": raw.get("manifest_version"),
        }
        result["game_manifest_backup"] = patch_game_manifest(target_root, summary)
        report_path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return result


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--queue", type=Path, default=None)
    parser.add_argument("--target", type=Path, default=None)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--apply", action="store_true", help="Nach erfolgreichem Audit wirklich kopieren und extrahieren")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    raw, _ = load_manifest(args.manifest)
    queue = args.queue or Path(raw["default_queue"])
    target = args.target or Path(raw["target_root"])
    try:
        result = run(queue.resolve(), target.resolve(), args.manifest.resolve(), args.apply)
    except (IngressError, OSError, zipfile.BadZipFile, json.JSONDecodeError) as exc:
        print(json.dumps({"status": "failed", "error": str(exc)}, ensure_ascii=False, indent=2), file=sys.stderr)
        return 1
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
