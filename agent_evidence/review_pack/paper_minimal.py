from __future__ import annotations

import hashlib
import json
import os
import subprocess
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

PROFILE_NAME = "execution-evidence-operation-accountability-profile"
PROFILE_VERSION = "0.1"
PACKAGE_NAME = "review-pack-paper-minimal"

PAPER_MINIMAL_REQUIRED_FILES = [
    "README.md",
    "docs/PAPER_BOUNDARY_FREEZE.md",
    "docs/PAPER_MAINLINE.md",
    "docs/REPRODUCE_PAPER_MINIMAL.md",
    "docs/HISTORICAL_AND_ADJACENT_SURFACES.md",
    "paper/tables/minimal_profile_tables.md",
    "scripts/reproduce_paper_minimal.sh",
    "spec/execution-evidence-operation-accountability-profile-v0.1.md",
    "schema/execution-evidence-operation-accountability-profile-v0.1.schema.json",
    "examples/minimal-valid-evidence.json",
    "examples/invalid-missing-required.json",
    "examples/invalid-unclosed-reference.json",
    "examples/invalid-policy-link-broken.json",
    "demo/run_operation_accountability_demo.py",
]

PAPER_MINIMAL_EXAMPLES = [
    "examples/minimal-valid-evidence.json",
    "examples/invalid-missing-required.json",
    "examples/invalid-unclosed-reference.json",
    "examples/invalid-policy-link-broken.json",
]

NON_CLAIMS = [
    "registry design",
    "multi-agent orchestration",
    "full FDO interoperability",
    "full cryptographic trust fabric",
    "legal non-repudiation",
    "production deployment",
    "broad platform governance",
    "broad runtime integration coverage",
    "no compliance approval",
]

REPRODUCE_TEXT = """# Reproduce Paper-Minimal Review Package

This review package is a paper-minimal inspection package. Reproduction
commands are intended to be run from the repository root after installing
agent-evidence.

Core command:

```bash
bash scripts/reproduce_paper_minimal.sh
```

The command validates one valid example, three controlled invalid examples, and
the metadata-enrichment demo for Execution Evidence and Operation
Accountability Profile v0.1.
"""

CLAIM_BOUNDARY_TEXT = """# Claim Boundary

This review package supports only the paper-minimal path for Execution Evidence
and Operation Accountability Profile v0.1.

It does not claim:

- registry design
- multi-agent orchestration
- full FDO interoperability
- full cryptographic trust fabric
- legal non-repudiation
- production deployment
- broad platform governance
- broad runtime integration coverage
- no compliance approval

The package is intended for inspection of the current profile, schema,
controlled examples, validator entrypoint, demo, rerun script, paper tables,
and boundary documents. It is not a complete standalone software release.
"""


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def current_git_commit(repo_root: Path) -> str:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "--short", "HEAD"],
            cwd=repo_root,
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
    except (OSError, subprocess.CalledProcessError):
        return "unknown"


def package_info(repo_root: Path, created_at_utc: str | None = None) -> dict[str, Any]:
    return {
        "package_name": PACKAGE_NAME,
        "created_at_utc": created_at_utc
        or datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "git_commit": current_git_commit(repo_root),
        "profile_name": PROFILE_NAME,
        "profile_version": PROFILE_VERSION,
        "paper_minimal": True,
        "included_examples": PAPER_MINIMAL_EXAMPLES,
        "non_claims": NON_CLAIMS,
    }


def _source_payloads(repo_root: Path) -> list[tuple[str, bytes, int]]:
    payloads: list[tuple[str, bytes, int]] = []
    missing: list[str] = []
    for relative_path in PAPER_MINIMAL_REQUIRED_FILES:
        source = repo_root / relative_path
        if not source.is_file():
            missing.append(relative_path)
            continue
        mode = source.stat().st_mode & 0o777
        if relative_path == "scripts/reproduce_paper_minimal.sh":
            mode |= 0o111
        payloads.append((relative_path, source.read_bytes(), mode))
    if missing:
        raise FileNotFoundError(f"Missing paper-minimal review package files: {missing}")
    return payloads


def _generated_payloads(repo_root: Path) -> list[tuple[str, bytes, int]]:
    info = package_info(repo_root)
    return [
        ("CLAIM_BOUNDARY.md", CLAIM_BOUNDARY_TEXT.encode("utf-8"), 0o644),
        ("REPRODUCE.md", REPRODUCE_TEXT.encode("utf-8"), 0o644),
        (
            "PACKAGE_INFO.json",
            json.dumps(info, indent=2, sort_keys=True).encode("utf-8") + b"\n",
            0o644,
        ),
    ]


def _manifest_payload(entries: list[dict[str, Any]]) -> bytes:
    manifest = {
        "manifest_version": 1,
        "package_name": PACKAGE_NAME,
        "paper_minimal": True,
        "profile_name": PROFILE_NAME,
        "profile_version": PROFILE_VERSION,
        "manifest_scope": (
            "All package payload files are listed. MANIFEST.json is excluded "
            "from its own digest list to avoid a self-referential checksum."
        ),
        "file_count": len(entries),
        "files": entries,
    }
    return json.dumps(manifest, indent=2, sort_keys=True).encode("utf-8") + b"\n"


def _zip_info(path: str, mode: int) -> zipfile.ZipInfo:
    info = zipfile.ZipInfo(path)
    info.compress_type = zipfile.ZIP_DEFLATED
    info.external_attr = ((0o100000 | mode) & 0xFFFF) << 16
    return info


def create_paper_minimal_review_pack(repo_root: Path, output_path: Path) -> dict[str, Any]:
    """Create the bounded paper-minimal review package zip."""

    repo_root = repo_root.resolve()
    output_path = output_path.resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)

    payloads = _source_payloads(repo_root) + _generated_payloads(repo_root)
    entries = [
        {
            "path": relative_path,
            "size_bytes": len(payload),
            "sha256": sha256_bytes(payload),
        }
        for relative_path, payload, _mode in payloads
    ]
    manifest_payload = _manifest_payload(entries)

    if output_path.exists():
        output_path.unlink()

    with zipfile.ZipFile(output_path, "w") as archive:
        for relative_path, payload, mode in payloads:
            archive.writestr(_zip_info(relative_path, mode), payload)
        archive.writestr(_zip_info("MANIFEST.json", 0o644), manifest_payload)

    return {
        "ok": True,
        "output": str(output_path),
        "package_name": PACKAGE_NAME,
        "git_commit": current_git_commit(repo_root),
        "manifest_entry_count": len(entries),
        "zip_file_count": len(entries) + 1,
        "sha256": sha256_file(output_path),
    }


def verify_review_pack_manifest(package_path: Path, extract_dir: Path) -> dict[str, Any]:
    """Extract a review package and verify manifest-listed SHA-256 digests."""

    package_path = package_path.resolve()
    extract_dir = extract_dir.resolve()
    extract_dir.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(package_path) as archive:
        archive.extractall(extract_dir)
        for info in archive.infolist():
            mode = (info.external_attr >> 16) & 0o777
            if mode:
                os.chmod(extract_dir / info.filename, mode)

    manifest_path = extract_dir / "MANIFEST.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    issues: list[str] = []
    checked_files = 0
    for entry in manifest.get("files", []):
        relative_path = entry["path"]
        target = extract_dir / relative_path
        if not target.is_file():
            issues.append(f"missing:{relative_path}")
            continue
        checked_files += 1
        size_bytes = target.stat().st_size
        if size_bytes != entry["size_bytes"]:
            issues.append(f"size_mismatch:{relative_path}")
        digest = sha256_file(target)
        if digest != entry["sha256"]:
            issues.append(f"sha256_mismatch:{relative_path}")

    script_path = extract_dir / "scripts/reproduce_paper_minimal.sh"
    if not script_path.is_file():
        issues.append("missing:scripts/reproduce_paper_minimal.sh")
    elif not os.access(script_path, os.X_OK):
        issues.append("not_executable:scripts/reproduce_paper_minimal.sh")

    for required_path in ("CLAIM_BOUNDARY.md", "REPRODUCE.md", "PACKAGE_INFO.json"):
        if not (extract_dir / required_path).is_file():
            issues.append(f"missing:{required_path}")

    return {
        "ok": not issues,
        "manifest_entry_count": len(manifest.get("files", [])),
        "checked_files": checked_files,
        "issues": issues,
    }
