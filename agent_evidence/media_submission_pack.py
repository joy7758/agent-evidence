from __future__ import annotations

import json
import shutil
from hashlib import sha256
from pathlib import Path
from typing import Any

from agent_evidence.media_release_pack import build_aep_media_release_pack

SUBMISSION_PROFILE = "aep-media-submission-pack@0.1"
GENERATED_UTC = "2026-04-26T00:00:00Z"
SUBMISSION_STATUS = "prepared_locally_" + "not_submitted"
FORBIDDEN_WORKSPACE_LABEL = "paper-ncs-" + "execution-evidence"

TEXT_SUFFIXES = {".csv", ".json", ".md", ".txt"}


def _write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def _sha256_file(path: Path) -> str:
    digest = sha256()
    with path.open("rb") as file_obj:
        for chunk in iter(lambda: file_obj.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _read_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"expected JSON object: {path}")
    return payload


def _sanitize_text(text: str, *, repo_root: Path, out_dir: Path) -> str:
    replacements = {
        str(repo_root.resolve()): ".",
        str(out_dir.resolve()): "<submission-pack>",
        str(Path.home()): "<home>",
        str(Path("/", "Users", "zhangbin")): "<home>",
        FORBIDDEN_WORKSPACE_LABEL: "unrelated paper workspace",
    }
    sanitized = text
    for source, target in replacements.items():
        sanitized = sanitized.replace(source, target)
    return sanitized


def _copy_text(source: Path, target: Path, *, repo_root: Path, out_dir: Path) -> None:
    text = source.read_text(encoding="utf-8")
    _write_text(target, _sanitize_text(text, repo_root=repo_root, out_dir=out_dir))


def _checksums(out_dir: Path) -> None:
    checksum_path = out_dir / "checksums.sha256"
    entries: list[tuple[str, str]] = []
    for path in sorted(out_dir.rglob("*")):
        if path.is_file() and path != checksum_path:
            entries.append((_sha256_file(path), path.relative_to(out_dir).as_posix()))
    checksum_path.write_text(
        "".join(f"{digest}  {relative_path}\n" for digest, relative_path in entries),
        encoding="utf-8",
    )


def _scan_non_claims(text: str) -> dict[str, bool]:
    lower = text.lower()
    return {
        "legal_admissibility_boundary": "legal admissibility" in lower,
        "non_repudiation_boundary": "non-repudiation" in lower,
        "trusted_timestamping_boundary": "trusted timestamp" in lower,
        "real_ptp_boundary": "real ptp" in lower,
        "ffmpeg_prft_boundary": "mp4 prft" in lower or "ffmpeg prft" in lower,
        "c2pa_signature_boundary": "c2pa signature" in lower,
        "production_boundary": "production" in lower,
    }


def _submission_readme() -> str:
    return """# AEP-Media v0.1 Submission Pack

This directory is a local submission-preparation package. It is not an
external journal submission record.

Contents:

- `manuscript/`: paper draft and standalone section files.
- `supplement/`: appendix, release summary, claim boundary, reproducibility checklist.
- `format/`: IEEE/TSE preflight checklist and submission checklist.
- `release-pack/`: generated AEP-Media v0.1 research artifact pack.
- `pack-manifest.json`: machine-readable inventory for this submission pack.
- `checksums.sha256`: checksums for ordinary files in the pack.

The pack preserves the core claim boundary: local validation, fixture ingestion,
offline bundle verification, strict declared time-trace checking, optional tool
detection, and bounded evaluation. It does not claim real PTP synchronization,
full MP4 PRFT parsing, real C2PA signature verification, legal admissibility,
non-repudiation, trusted timestamping, or production deployment.
"""


def build_aep_media_submission_pack(
    out_dir: str | Path,
    repo_root: str | Path | None = None,
) -> dict[str, Any]:
    resolved_repo_root = (
        Path(repo_root).resolve() if repo_root is not None else Path(__file__).resolve().parents[1]
    )
    resolved_out_dir = Path(out_dir).resolve()
    if resolved_out_dir.exists():
        shutil.rmtree(resolved_out_dir)
    resolved_out_dir.mkdir(parents=True, exist_ok=True)

    release_pack_dir = resolved_out_dir / "release-pack"
    release_summary = build_aep_media_release_pack(release_pack_dir, repo_root=resolved_repo_root)

    paper_dir = resolved_repo_root / "docs" / "paper"
    report_dir = resolved_repo_root / "docs" / "reports"
    paper_files = [
        "aep_media_tse_submission_draft.md",
        "aep_media_abstract.md",
        "aep_media_methods_section.md",
        "aep_media_evaluation_section.md",
        "aep_media_threats_to_validity.md",
        "aep_media_related_work_notes.md",
    ]
    for paper_file in paper_files:
        source = paper_dir / paper_file
        if source.exists():
            _copy_text(
                source,
                resolved_out_dir / "manuscript" / paper_file,
                repo_root=resolved_repo_root,
                out_dir=resolved_out_dir,
            )

    supplement_files = [
        ("aep_media_submission_appendix.md", "aep_media_submission_appendix.md"),
        ("aep_media_final_claim_boundary.md", "claim-boundary.md"),
        ("aep_media_final_reproducibility_checklist.md", "reproducibility-checklist.md"),
        ("aep_media_final_evaluation_summary.md", "evaluation-summary.md"),
        ("aep_media_final_artifact_inventory.md", "artifact-inventory.md"),
        ("aep_media_mission008_report.md", "mission008-report.md"),
    ]
    for source_name, target_name in supplement_files:
        source = paper_dir / source_name
        if not source.exists():
            source = report_dir / source_name
        if source.exists():
            _copy_text(
                source,
                resolved_out_dir / "supplement" / target_name,
                repo_root=resolved_repo_root,
                out_dir=resolved_out_dir,
            )

    format_files = [
        "aep_media_tse_format_preflight.md",
        "aep_media_submission_checklist.md",
        "aep_media_cover_letter_draft.md",
    ]
    for format_file in format_files:
        source = paper_dir / format_file
        if source.exists():
            _copy_text(
                source,
                resolved_out_dir / "format" / format_file,
                repo_root=resolved_repo_root,
                out_dir=resolved_out_dir,
            )

    _write_text(resolved_out_dir / "README.md", _submission_readme())

    manuscript_path = resolved_out_dir / "manuscript" / "aep_media_tse_submission_draft.md"
    manuscript_text = (
        manuscript_path.read_text(encoding="utf-8") if manuscript_path.exists() else ""
    )
    non_claim_checks = _scan_non_claims(manuscript_text)
    text_files = [
        path.relative_to(resolved_out_dir).as_posix()
        for path in sorted(resolved_out_dir.rglob("*"))
        if path.is_file() and path.suffix in TEXT_SUFFIXES
    ]
    manifest = {
        "profile": SUBMISSION_PROFILE,
        "generated_utc": GENERATED_UTC,
        "ok": bool(release_summary.get("ok")) and all(non_claim_checks.values()),
        "release_pack_ok": bool(release_summary.get("ok")),
        "manuscript": "manuscript/aep_media_tse_submission_draft.md",
        "supplement": "supplement/aep_media_submission_appendix.md",
        "format_preflight": "format/aep_media_tse_format_preflight.md",
        "submission_checklist": "format/aep_media_submission_checklist.md",
        "file_count": len(text_files),
        "text_files": text_files,
        "non_claim_checks": non_claim_checks,
        "claim_boundary": {
            "local_validation": True,
            "fixture_ingestion": True,
            "optional_external_tool_detection": True,
            "real_ptp_proof": False,
            "real_ffmpeg_prft_proof": False,
            "real_c2pa_signature_proof": False,
            "legal_admissibility": False,
            "non_repudiation": False,
        },
        "journal_target": {
            "name": "IEEE Transactions on Software Engineering",
            "submission_status": SUBMISSION_STATUS,
        },
    }
    manifest["summary"] = (
        f"{'PASS' if manifest['ok'] else 'FAIL'} {SUBMISSION_PROFILE} "
        "status=prepared_locally_"
        "not_submitted"
    )
    _write_json(resolved_out_dir / "pack-manifest.json", manifest)
    _checksums(resolved_out_dir)
    return manifest


def main(argv: list[str] | None = None) -> int:
    import argparse

    parser = argparse.ArgumentParser(description="Build the AEP-Media submission pack.")
    parser.add_argument("--out", required=True, type=Path)
    args = parser.parse_args(argv)
    report = build_aep_media_submission_pack(args.out)
    print(report["summary"])
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
