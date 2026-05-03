from __future__ import annotations

import json
import os
import re
import shutil
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from pydantic import ValidationError

from agent_evidence.export import verify_json_bundle

REVIEW_PACK_VERSION = "0.1"

ALLOWED_FINDING_SEVERITIES = {"pass", "warning", "fail", "unknown"}
ALLOWED_FINDING_TYPES = {
    "verification_passed",
    "signature_verified",
    "summary_loaded",
    "missing_optional_summary",
    "bundle_parse_error",
    "signature_verification_failed",
    "verification_failed",
    "unsupported_artifact",
    "redaction_warning",
}

BOUNDARIES = [
    "not legal non-repudiation",
    "not compliance certification",
    "not AI Act approval",
    "not full AI governance assessment",
]

SECRET_LIKE_PATTERNS = [
    re.compile(r"Authorization", re.IGNORECASE),
    re.compile(r"Bearer\s+[A-Za-z0-9._~+/=-]+"),
    re.compile(r"pypi-[A-Za-z0-9._~+/=-]{8,}"),
    re.compile(r"sk-[A-Za-z0-9._~+/=-]{8,}"),
    re.compile(r"OPENAI(?:_COMPATIBLE)?_API_KEY"),
    re.compile(r"TWINE_PASSWORD"),
]


class ReviewPackError(RuntimeError):
    """Raised when Review Pack creation cannot proceed safely."""


class ReviewPackVerificationError(ReviewPackError):
    """Raised when verification fails before packaging."""

    def __init__(self, message: str, receipt: dict[str, Any] | None = None) -> None:
        super().__init__(message)
        self.receipt = receipt or {"ok": False, "issues": [message]}


def _json_text(payload: dict[str, Any]) -> str:
    return json.dumps(payload, indent=2, sort_keys=True) + "\n"


def _relative_artifact(path: str) -> str:
    return f"artifacts/{path}"


def _copy_file(source: Path, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, destination)


def _assert_no_secret_like_content(path: Path, *, root: Path) -> None:
    content = path.read_text(encoding="utf-8", errors="replace")
    for pattern in SECRET_LIKE_PATTERNS:
        if pattern.search(content):
            relative = path.relative_to(root)
            raise ReviewPackError(
                f"secret-like content detected in Review Pack artifact: {relative}"
            )


def _assert_staging_contains_no_secret_like_content(staging: Path) -> None:
    for path in sorted(item for item in staging.rglob("*") if item.is_file()):
        _assert_no_secret_like_content(path, root=staging)


def _validate_output_dir(output_dir: Path) -> None:
    if output_dir.exists() and any(output_dir.iterdir()):
        raise ReviewPackError(f"output directory already exists and is not empty: {output_dir}")


def _verify_export_bundle(bundle_path: Path, public_key_path: Path) -> dict[str, Any]:
    try:
        result = verify_json_bundle(
            bundle_path,
            public_key_pem=public_key_path.read_bytes(),
        )
    except (OSError, json.JSONDecodeError, ValidationError, ValueError) as exc:
        receipt = {
            "ok": False,
            "review_pack_version": REVIEW_PACK_VERSION,
            "source": {
                "bundle": bundle_path.name,
                "public_key": public_key_path.name,
            },
            "verification": {
                "ok": False,
                "issues": [str(exc)],
            },
        }
        raise ReviewPackVerificationError("Bundle verification failed.", receipt) from exc

    if not result.get("ok"):
        receipt = {
            "ok": False,
            "review_pack_version": REVIEW_PACK_VERSION,
            "source": {
                "bundle": bundle_path.name,
                "public_key": public_key_path.name,
            },
            "verification": result,
        }
        raise ReviewPackVerificationError("Bundle verification failed.", receipt)

    if not result.get("signature_present") or not result.get("signature_verified"):
        receipt = {
            "ok": False,
            "review_pack_version": REVIEW_PACK_VERSION,
            "source": {
                "bundle": bundle_path.name,
                "public_key": public_key_path.name,
            },
            "verification": result,
            "issues": ["signed export bundle verification is required"],
        }
        raise ReviewPackVerificationError("Signed export bundle verification is required.", receipt)

    return result


def _build_findings(
    verification_result: dict[str, Any],
    *,
    summary_path: Path | None,
) -> dict[str, Any]:
    findings = [
        {
            "severity": "pass",
            "type": "verification_passed",
            "message": "Existing export verification returned ok true.",
        },
        {
            "severity": "pass",
            "type": "signature_verified",
            "message": ("Signed export metadata was verified with the provided public key."),
        },
    ]
    if summary_path is None:
        findings.append(
            {
                "severity": "warning",
                "type": "missing_optional_summary",
                "message": "No source summary.json was provided.",
            }
        )
    else:
        findings.append(
            {
                "severity": "pass",
                "type": "summary_loaded",
                "message": "Source summary.json was included as a reviewer aid.",
            }
        )

    return {
        "ok": True,
        "review_pack_version": REVIEW_PACK_VERSION,
        "verification_ok": verification_result.get("ok") is True,
        "findings": findings,
    }


def _render_summary_markdown(
    *,
    receipt: dict[str, Any],
    findings: dict[str, Any],
    bundle_filename: str,
    public_key_filename: str,
    summary_filename: str | None,
) -> str:
    verification = receipt["verification"]
    issue_lines = verification.get("issues") or []
    if not issue_lines:
        issue_lines = ["No verification issues were reported."]
    finding_lines = [
        f"- {item['severity']}: {item['type']} - {item['message']}" for item in findings["findings"]
    ]
    source_summary = (
        f"- source summary: `{_relative_artifact(summary_filename)}`"
        if summary_filename
        else "- source summary: not provided"
    )
    return "\n".join(
        [
            "# Agent Evidence Review Pack",
            "",
            "## Verification Outcome",
            "",
            "- outcome: pass",
            f"- record count: {verification.get('record_count')}",
            f"- signature count: {verification.get('signature_count')}",
            f"- verified signature count: {verification.get('verified_signature_count')}",
            "",
            "## Source Artifacts",
            "",
            f"- evidence bundle: `{_relative_artifact(bundle_filename)}`",
            f"- manifest public key: `{_relative_artifact(public_key_filename)}`",
            source_summary,
            "",
            "## What Was Checked",
            "",
            "- the exported JSON evidence bundle was parsed by existing core verification",
            "- evidence chain and manifest consistency were checked by existing core verification",
            "- signed export metadata was checked against the provided public key",
            "",
            "## Findings",
            "",
            *finding_lines,
            "",
            "## Verification Issues",
            "",
            *[f"- {issue}" for issue in issue_lines],
            "",
            "## Limitations",
            "",
            "- This review pack is not legal non-repudiation.",
            "- This review pack is not compliance certification.",
            "- This review pack is not AI Act approval.",
            "- This review pack is not full AI governance assessment.",
            "",
        ]
    )


def _build_manifest(
    *,
    bundle_path: Path,
    public_key_path: Path,
    summary_path: Path | None,
    included_artifacts: list[str],
) -> dict[str, Any]:
    return {
        "review_pack_version": REVIEW_PACK_VERSION,
        "created_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "source": {
            "bundle_filename": bundle_path.name,
            "public_key_filename": public_key_path.name,
            "summary_filename": summary_path.name if summary_path is not None else None,
        },
        "included_artifacts": included_artifacts,
        "receipt": "receipt.json",
        "findings": "findings.json",
        "summary": "summary.md",
        "boundaries": BOUNDARIES,
    }


def create_review_pack(
    *,
    bundle_path: str | Path,
    public_key_path: str | Path,
    output_dir: str | Path,
    summary_path: str | Path | None = None,
) -> dict[str, Any]:
    """Create a local offline Review Pack from a verified signed export bundle."""

    bundle = Path(bundle_path)
    public_key = Path(public_key_path)
    summary = Path(summary_path) if summary_path is not None else None
    output = Path(output_dir)

    if not bundle.exists() or not bundle.is_file():
        raise ReviewPackError(f"bundle path is not a file: {bundle}")
    if not public_key.exists() or not public_key.is_file():
        raise ReviewPackError(f"public key path is not a file: {public_key}")
    if summary is not None and (not summary.exists() or not summary.is_file()):
        raise ReviewPackError(f"summary path is not a file: {summary}")

    _validate_output_dir(output)
    verification_result = _verify_export_bundle(bundle, public_key)

    output_parent = output.parent
    output_parent.mkdir(parents=True, exist_ok=True)
    staging = Path(tempfile.mkdtemp(prefix=f".{output.name}.", dir=output_parent))
    try:
        artifact_dir = staging / "artifacts"
        bundle_artifact = artifact_dir / "evidence.bundle.json"
        public_key_artifact = artifact_dir / "manifest-public.pem"
        summary_artifact = artifact_dir / "summary.json" if summary is not None else None

        _copy_file(bundle, bundle_artifact)
        _copy_file(public_key, public_key_artifact)
        included_artifacts = [
            _relative_artifact(bundle_artifact.name),
            _relative_artifact(public_key_artifact.name),
        ]
        if summary is not None and summary_artifact is not None:
            _copy_file(summary, summary_artifact)
            included_artifacts.append(_relative_artifact(summary_artifact.name))

        receipt = {
            "ok": True,
            "review_pack_version": REVIEW_PACK_VERSION,
            "source": {
                "bundle": bundle.name,
                "public_key": public_key.name,
                "summary": summary.name if summary is not None else None,
            },
            "artifacts": {
                "bundle": _relative_artifact(bundle_artifact.name),
                "public_key": _relative_artifact(public_key_artifact.name),
                "summary": (
                    _relative_artifact(summary_artifact.name)
                    if summary_artifact is not None
                    else None
                ),
            },
            "verification": verification_result,
            "boundaries": BOUNDARIES,
        }
        findings = _build_findings(verification_result, summary_path=summary)
        manifest = _build_manifest(
            bundle_path=bundle,
            public_key_path=public_key,
            summary_path=summary,
            included_artifacts=included_artifacts,
        )
        markdown = _render_summary_markdown(
            receipt=receipt,
            findings=findings,
            bundle_filename=bundle_artifact.name,
            public_key_filename=public_key_artifact.name,
            summary_filename=summary_artifact.name if summary_artifact is not None else None,
        )

        (staging / "receipt.json").write_text(_json_text(receipt), encoding="utf-8")
        (staging / "findings.json").write_text(_json_text(findings), encoding="utf-8")
        (staging / "manifest.json").write_text(_json_text(manifest), encoding="utf-8")
        (staging / "summary.md").write_text(markdown, encoding="utf-8")

        _assert_staging_contains_no_secret_like_content(staging)

        if output.exists():
            output.rmdir()
        os.replace(staging, output)
        return {
            "ok": True,
            "review_pack_version": REVIEW_PACK_VERSION,
            "output_dir": str(output),
            "manifest": str(output / "manifest.json"),
            "receipt": str(output / "receipt.json"),
            "findings": str(output / "findings.json"),
            "summary": str(output / "summary.md"),
            "artifacts": included_artifacts,
        }
    except Exception:
        if staging.exists():
            shutil.rmtree(staging)
        raise
