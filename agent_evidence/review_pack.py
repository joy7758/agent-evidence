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

REVIEW_PACK_VERSION = "0.3"
PACK_CREATION_MODE = "local_offline"

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
    "bundle_tampered",
    "public_key_mismatch",
    "private_key_excluded",
    "secret_scan_passed",
    "artifact_inventory_recorded",
    "limitation_notice_present",
    "reviewer_checklist_present",
    "review_pack_manifest_complete",
    "secret_scan_status_recorded",
}

BOUNDARIES = [
    "not legal non-repudiation",
    "not compliance certification",
    "not AI Act approval",
    "not full AI governance assessment",
]

SECRET_SCAN_LIMITATIONS = [
    "not comprehensive DLP",
    "does not prove all possible secrets are absent",
]

REVIEWER_CHECKLIST = [
    {
        "id": "RP-CHECK-001",
        "text": "Confirm verification outcome is pass.",
    },
    {
        "id": "RP-CHECK-002",
        "text": "Review the included evidence bundle.",
    },
    {
        "id": "RP-CHECK-003",
        "text": "Review the public key used for verification.",
    },
    {
        "id": "RP-CHECK-004",
        "text": "Review findings and warnings.",
    },
    {
        "id": "RP-CHECK-005",
        "text": "Review limitations before relying on the pack.",
    },
    {
        "id": "RP-CHECK-006",
        "text": "Escalate fail or unknown findings.",
    },
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


def _verification_details(verification_result: dict[str, Any]) -> dict[str, Any]:
    return {
        "verification_ok": verification_result.get("ok") is True,
        "record_count": verification_result.get("record_count"),
        "signature_count": verification_result.get("signature_count"),
        "verified_signature_count": verification_result.get("verified_signature_count"),
    }


def _secret_scan_status() -> dict[str, Any]:
    return {
        "status": "passed",
        "scope": "configured_secret_sentinel_patterns",
        "limitations": SECRET_SCAN_LIMITATIONS,
    }


def _build_artifact_inventory(included_artifacts: list[str]) -> list[dict[str, str]]:
    roles = {
        "manifest.json": "Review Pack manifest",
        "receipt.json": "Machine-readable verification receipt",
        "findings.json": "Structured reviewer findings",
        "summary.md": "Reviewer-facing markdown summary",
        "artifacts/evidence.bundle.json": "Copied signed evidence bundle",
        "artifacts/manifest-public.pem": "Copied public key used for verification",
        "artifacts/summary.json": "Copied source summary, when provided",
    }
    paths = [
        "manifest.json",
        "receipt.json",
        "findings.json",
        "summary.md",
        *included_artifacts,
    ]
    return [
        {"path": path, "role": roles.get(path, "Included Review Pack artifact")} for path in paths
    ]


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
    verification = _verification_details(verification_result)
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
        {
            "severity": "pass",
            "type": "private_key_excluded",
            "message": "Only public artifacts are copied; private signing keys are excluded.",
        },
        {
            "severity": "pass",
            "type": "secret_scan_passed",
            "message": (
                "Review Pack artifacts passed configured secret sentinel pattern checks "
                "before finalization."
            ),
        },
        {
            "severity": "pass",
            "type": "artifact_inventory_recorded",
            "message": "Review Pack manifest records the generated and copied artifacts.",
        },
        {
            "severity": "pass",
            "type": "limitation_notice_present",
            "message": "Reviewer summary includes explicit non-claim limitations.",
        },
        {
            "severity": "pass",
            "type": "reviewer_checklist_present",
            "message": "Reviewer summary and manifest include stable reviewer checklist items.",
        },
        {
            "severity": "pass",
            "type": "review_pack_manifest_complete",
            "message": "Review Pack manifest records reviewer-facing package metadata.",
        },
        {
            "severity": "pass",
            "type": "secret_scan_status_recorded",
            "message": "Review Pack metadata records conservative secret scan status and limits.",
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
        **verification,
        "findings": findings,
    }


def _markdown_table(headers: list[str], rows: list[list[Any]]) -> list[str]:
    rendered = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        rendered.append(
            "| "
            + " | ".join("not provided" if value is None else str(value) for value in row)
            + " |"
        )
    return rendered


def _render_summary_markdown(
    *,
    receipt: dict[str, Any],
    findings: dict[str, Any],
    artifact_inventory: list[dict[str, str]],
) -> str:
    verification = receipt["verification"]
    issue_lines = verification.get("issues") or []
    if not issue_lines:
        issue_lines = ["No verification issues were reported."]
    verification_rows = [
        ["verification_ok", receipt["verification_ok"]],
        ["record_count", receipt.get("record_count")],
        ["signature_count", receipt.get("signature_count")],
        ["verified_signature_count", receipt.get("verified_signature_count")],
        ["bundle", receipt["source"]["bundle"]],
        ["public_key", receipt["source"]["public_key"]],
        ["summary_attached", receipt["source"]["summary"] is not None],
    ]
    artifact_rows = [[f"`{item['path']}`", item["role"]] for item in artifact_inventory]
    finding_rows = [
        [item["severity"], item["type"], item["message"]] for item in findings["findings"]
    ]
    checklist_lines = [f"- [ ] {item['id']}: {item['text']}" for item in REVIEWER_CHECKLIST]
    return "\n".join(
        [
            "# Agent Evidence Review Pack",
            "",
            "## Verification Outcome",
            "",
            "- outcome: pass",
            *[f"- {issue}" for issue in issue_lines],
            "",
            "## Reviewer Checklist",
            "",
            *checklist_lines,
            "",
            "## Verification Details",
            "",
            *_markdown_table(["Field", "Value"], verification_rows),
            "",
            "## Artifact Inventory",
            "",
            *_markdown_table(["Path", "Role"], artifact_rows),
            "",
            "## Findings",
            "",
            *_markdown_table(["Severity", "Type", "Message"], finding_rows),
            "",
            "## Secret and Private Key Boundary",
            "",
            "- private keys are not copied into the Review Pack.",
            "- configured secret sentinel patterns are checked during pack creation.",
            "- this is not comprehensive DLP.",
            "- this does not prove that all possible secrets are absent.",
            "",
            "## Pack Creation Mode",
            "",
            f"- `{PACK_CREATION_MODE}`",
            "",
            "## Recommended Reviewer Actions",
            "",
            "- Retain `receipt.json`, `findings.json`, `manifest.json`, and `summary.md` together.",
            "- Inspect the copied evidence bundle before making reviewer decisions.",
            "- Compare warnings or unknown findings with the source evidence workflow.",
            "- Re-run source verification if the bundle, public key, or summary changes.",
            "- Treat fail or unknown findings as escalation inputs, not approvals.",
            "",
            "## What This Does Not Prove",
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
    artifact_inventory: list[dict[str, str]],
    verification_result: dict[str, Any],
) -> dict[str, Any]:
    verification = _verification_details(verification_result)
    return {
        "review_pack_version": REVIEW_PACK_VERSION,
        "pack_creation_mode": PACK_CREATION_MODE,
        "created_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        **verification,
        "source": {
            "bundle_filename": bundle_path.name,
            "public_key_filename": public_key_path.name,
            "summary_filename": summary_path.name if summary_path is not None else None,
        },
        "included_artifacts": included_artifacts,
        "artifact_inventory": artifact_inventory,
        "reviewer_checklist": REVIEWER_CHECKLIST,
        "secret_scan_status": _secret_scan_status(),
        "receipt": "receipt.json",
        "findings": "findings.json",
        "summary": "summary.md",
        "boundaries": BOUNDARIES,
        "non_claims": BOUNDARIES,
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

        verification = _verification_details(verification_result)
        artifact_inventory = _build_artifact_inventory(included_artifacts)
        receipt = {
            "ok": True,
            "review_pack_version": REVIEW_PACK_VERSION,
            "pack_creation_mode": PACK_CREATION_MODE,
            **verification,
            "source": {
                "bundle": bundle.name,
                "public_key": public_key.name,
                "summary": summary.name if summary is not None else None,
            },
            "included_artifacts": included_artifacts,
            "artifact_inventory": artifact_inventory,
            "reviewer_checklist_reference": "manifest.json#/reviewer_checklist",
            "secret_scan_status": _secret_scan_status(),
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
            "non_claims": BOUNDARIES,
        }
        findings = _build_findings(verification_result, summary_path=summary)
        manifest = _build_manifest(
            bundle_path=bundle,
            public_key_path=public_key,
            summary_path=summary,
            included_artifacts=included_artifacts,
            artifact_inventory=artifact_inventory,
            verification_result=verification_result,
        )
        markdown = _render_summary_markdown(
            receipt=receipt,
            findings=findings,
            artifact_inventory=artifact_inventory,
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
