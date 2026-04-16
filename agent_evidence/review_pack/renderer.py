from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping

_PRIMARY_ORDER = ("bundle", "receipt", "summary")
_SUPPORTING_ORDER = ("manifest", "public_key", "runtime_events", "private_key")
_SUMMARY_ORIENTATION_KEYS = (
    "provider_label",
    "model",
    "base_url",
    "record_count",
    "signature_count",
    "call_count",
    "verify_command",
)
_RECEIPT_FACT_KEYS = (
    "ok",
    "format",
    "profile",
    "source",
    "record_count",
    "issue_count",
    "signature_present",
    "signature_count",
    "required_signature_count",
    "signature_verified",
    "latest_chain_hash",
)


@dataclass(frozen=True)
class RenderedReviewReport:
    """Deterministic reviewer-facing report output."""

    markdown: str
    taxonomy_labels: tuple[str, ...]


def _receipt_issues(receipt: Mapping[str, Any]) -> tuple[str, ...]:
    issues = receipt.get("issues", [])
    if not isinstance(issues, list):
        return ()
    return tuple(str(issue) for issue in issues)


def _append_label(labels: list[str], label: str) -> None:
    if label not in labels:
        labels.append(label)


def _taxonomy_labels(
    receipt: Mapping[str, Any],
    *,
    missing_supporting: list[str],
) -> tuple[str, ...]:
    labels: list[str] = []
    issues = _receipt_issues(receipt)
    issue_text = "\n".join(issues).lower()

    if receipt.get("ok") is True:
        _append_label(labels, "Verification passed")
    else:
        _append_label(labels, "Verification issues present")

    if "chain" in issue_text:
        _append_label(labels, "Chain continuity failed")
    if "signature" in issue_text or receipt.get("signature_verified") is False:
        _append_label(labels, "Signature failure")
    if any(word in issue_text for word in ("integrity", "manifest", "artifact digest")):
        _append_label(labels, "Integrity failure")
    if receipt.get("profile") or "validation" in issue_text:
        _append_label(labels, "Profile validation failure")
    if missing_supporting:
        _append_label(labels, "Optional support material missing")
    return tuple(labels)


def _overall_explanation(
    receipt: Mapping[str, Any],
    *,
    missing_supporting: list[str],
) -> str:
    if receipt.get("ok") is True and not missing_supporting:
        return "Verification passed and the primary artifacts are reviewable as packaged."
    if receipt.get("ok") is True and missing_supporting:
        return (
            "Verification passed, but some optional supporting material was not included in "
            "this pack."
        )
    return "Verification reported issues that require reviewer attention."


def _path_text(value: str | Path) -> str:
    return str(value)


class ReviewPackRenderer:
    """Render a deterministic reviewer-facing report from current pack inputs."""

    def render(
        self,
        *,
        bundle: Mapping[str, Any],
        receipt: Mapping[str, Any],
        summary: Mapping[str, Any],
        primary_files: Mapping[str, str | Path],
        supporting_files: Mapping[str, str | Path],
        missing_supporting: list[str],
    ) -> RenderedReviewReport:
        taxonomy_labels = _taxonomy_labels(receipt, missing_supporting=missing_supporting)
        explanation = _overall_explanation(receipt, missing_supporting=missing_supporting)
        verdict = "PASS" if receipt.get("ok") else "FAIL"

        lines = [
            "# Review Report",
            "",
            "## Overall Status",
            f"- Result: `{verdict}`",
            f"- `receipt.ok`: `{receipt.get('ok')}`",
            f"- Renderer labels: {', '.join(f'`{label}`' for label in taxonomy_labels)}",
            f"- Explanation: {explanation}",
            "",
            "## Artifact Inventory",
        ]
        lines.extend(
            self._artifact_inventory_lines(
                summary,
                primary_files,
                supporting_files,
                missing_supporting,
            )
        )
        lines.extend(["", "## Verification Facts"])
        lines.extend(self._verification_fact_lines(receipt))
        lines.extend(["", "## Issue / Failure Summary"])
        lines.extend(self._issue_summary_lines(receipt, taxonomy_labels, missing_supporting))
        lines.extend(["", "## Evidence References"])
        lines.extend(self._evidence_reference_lines(bundle, primary_files))
        lines.extend(
            [
                "",
                "## Reviewer Notes",
                "- Placeholder: add reviewer notes here.",
                (
                    "- Suggested path: inspect `primary/receipt.json`, then "
                    "`primary/bundle.json`, then `primary/summary.json`."
                ),
                "",
            ]
        )
        return RenderedReviewReport(markdown="\n".join(lines), taxonomy_labels=taxonomy_labels)

    def _artifact_inventory_lines(
        self,
        summary: Mapping[str, Any],
        primary_files: Mapping[str, str | Path],
        supporting_files: Mapping[str, str | Path],
        missing_supporting: list[str],
    ) -> list[str]:
        lines: list[str] = []
        for name in _PRIMARY_ORDER:
            if name in primary_files:
                lines.append(f"- Primary `{name}`: `{_path_text(primary_files[name])}`")
        for name in _SUPPORTING_ORDER:
            if name in supporting_files:
                lines.append(f"- Supporting `{name}`: `{_path_text(supporting_files[name])}`")
        for name in sorted(name for name in supporting_files if name not in _SUPPORTING_ORDER):
            lines.append(f"- Supporting `{name}`: `{_path_text(supporting_files[name])}`")
        for name in sorted(missing_supporting):
            lines.append(f"- Missing optional support: `{name}`")
        for key in _SUMMARY_ORIENTATION_KEYS:
            value = summary.get(key)
            if value is not None:
                lines.append(f"- `summary.{key}`: `{value}`")
        if not lines:
            lines.append("- No artifact inventory details were available.")
        return lines

    def _verification_fact_lines(self, receipt: Mapping[str, Any]) -> list[str]:
        lines: list[str] = []
        for key in _RECEIPT_FACT_KEYS:
            if key in receipt:
                lines.append(f"- `receipt.{key}`: `{receipt[key]}`")
        if not lines:
            lines.append("- No receipt verification facts were present.")
        return lines

    def _issue_summary_lines(
        self,
        receipt: Mapping[str, Any],
        taxonomy_labels: tuple[str, ...],
        missing_supporting: list[str],
    ) -> list[str]:
        lines = [
            f"- Renderer taxonomy labels: {', '.join(f'`{label}`' for label in taxonomy_labels)}"
        ]
        issues = _receipt_issues(receipt)
        if issues:
            lines.extend(f"- Raw receipt issue: `{issue}`" for issue in issues)
        else:
            lines.append("- No receipt issues were reported.")
        for name in sorted(missing_supporting):
            lines.append(f"- Missing optional support: `{name}`")
        return lines

    def _evidence_reference_lines(
        self,
        bundle: Mapping[str, Any],
        primary_files: Mapping[str, str | Path],
    ) -> list[str]:
        manifest = bundle.get("manifest")
        if not isinstance(manifest, Mapping):
            manifest = {}
        records = bundle.get("records")
        if not isinstance(records, list):
            records = []
        signatures = bundle.get("signatures")
        if not isinstance(signatures, list):
            signatures = []

        lines: list[str] = []
        if "bundle" in primary_files:
            lines.append(f"- Bundle artifact: `{_path_text(primary_files['bundle'])}`")
        for key in ("export_format", "record_count", "artifact_digest", "latest_chain_hash"):
            if key in manifest:
                lines.append(f"- `bundle.manifest.{key}`: `{manifest[key]}`")
        lines.append(f"- `bundle.records`: `{len(records)}`")
        lines.append(f"- `bundle.signatures`: `{len(signatures)}`")
        for index, record in enumerate(records[:3]):
            if not isinstance(record, Mapping):
                continue
            event = record.get("event")
            if not isinstance(event, Mapping):
                continue
            event_id = event.get("event_id")
            event_type = event.get("event_type")
            if event_id is None and event_type is None:
                continue
            lines.append(
                f"- `bundle.record[{index}]`: `event_id={event_id}` `event_type={event_type}`"
            )
        if len(records) > 3:
            lines.append(f"- Additional bundle records not listed: `{len(records) - 3}`")
        return lines
