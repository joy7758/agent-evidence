#!/usr/bin/env python3
"""Build the AFAC2026 TRPS final submission ZIP."""

from __future__ import annotations

import hashlib
import json
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "outputs"
STAGING_ROOT = OUTPUT_DIR / "final_pack_staging" / "TRPS_AFAC2026_FINAL_SUBMISSION_PACK"
ZIP_PATH = OUTPUT_DIR / "TRPS_AFAC2026_FINAL_SUBMISSION_PACK.zip"
SHA_PATH = OUTPUT_DIR / "TRPS_AFAC2026_FINAL_SUBMISSION_PACK.sha256"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def should_include(path: Path) -> bool:
    parts = set(path.parts)
    if {".git", ".venv", "node_modules", "__pycache__"} & parts:
        return False
    if path.name in {".env", ".DS_Store"}:
        return False
    if path.suffix == ".pyc":
        return False
    return True


def main() -> int:
    if not STAGING_ROOT.exists():
        raise SystemExit(f"missing staging root: {STAGING_ROOT}")
    if ZIP_PATH.exists():
        ZIP_PATH.unlink()
    with zipfile.ZipFile(ZIP_PATH, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(STAGING_ROOT.rglob("*")):
            if path.is_file() and should_include(path):
                archive.write(path, path.relative_to(STAGING_ROOT.parent))
    sha = sha256_file(ZIP_PATH)
    SHA_PATH.write_text(f"{sha}  {ZIP_PATH.name}\n", encoding="utf-8")
    summary = {
        "ok": True,
        "zip_path": str(ZIP_PATH),
        "zip_size_bytes": ZIP_PATH.stat().st_size,
        "sha256": sha,
    }
    print(json.dumps(summary, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
