from __future__ import annotations

import json
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping

from .pdf_export import write_review_report_pdf
from .renderer import ReviewPackRenderer

PRIMARY_FILENAMES = {
    "bundle": "bundle.json",
    "receipt": "receipt.json",
    "summary": "summary.json",
}
SUPPORTING_FILENAMES = {
    "manifest": "manifest.json",
    "public_key": "manifest-public.pem",
    "runtime_events": "runtime-events.jsonl",
    "private_key": "manifest-private.pem",
}
PACK_INDEX_FILENAME = "index.json"
REPORT_FILENAME = "report.md"
REPORT_PDF_FILENAME = "report.pdf"
PRIMARY_DIRNAME = "primary"
REVIEW_DIRNAME = "review"
SUPPORTING_DIRNAME = "supporting"


@dataclass(frozen=True)
class ReviewPackResult:
    """Normalized Review Pack output paths."""

    pack_dir: Path
    primary_files: dict[str, Path]
    supporting_files: dict[str, Path]
    index_path: Path
    report_path: Path
    report_pdf_path: Path


def _load_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"Expected a JSON object at {path}")
    return payload


def _copy_file(source: Path, destination: Path) -> Path:
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, destination)
    return destination


def _receipt_facts(receipt: Mapping[str, Any]) -> dict[str, Any]:
    issues = receipt.get("issues", [])
    if not isinstance(issues, list):
        issues = []
    facts: dict[str, Any] = {
        "ok": receipt.get("ok"),
        "issues": list(issues),
    }
    for key in (
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
    ):
        if key in receipt:
            facts[key] = receipt[key]
    return facts


def _summary_orientation(summary: Mapping[str, Any]) -> dict[str, Any]:
    orientation: dict[str, Any] = {}
    for key in (
        "ok",
        "record_count",
        "signature_count",
        "call_count",
        "provider_label",
        "model",
        "base_url",
        "verify_command",
    ):
        orientation[key] = summary.get(key)
    return orientation


class ReviewPackAssembler:
    """Package current primary artifacts into one review-oriented pack."""

    def __init__(self, *, output_dir: Path) -> None:
        self.output_dir = output_dir

    @classmethod
    def for_output_dir(cls, output_dir: str | Path) -> "ReviewPackAssembler":
        resolved_output_dir = Path(output_dir)
        if resolved_output_dir.exists():
            if resolved_output_dir.is_dir():
                shutil.rmtree(resolved_output_dir)
            else:
                resolved_output_dir.unlink()
        resolved_output_dir.mkdir(parents=True, exist_ok=True)
        return cls(output_dir=resolved_output_dir)

    def assemble(
        self,
        *,
        bundle_path: str | Path,
        receipt_path: str | Path,
        summary_path: str | Path,
        supporting_files: Mapping[str, str | Path] | None = None,
        include_private_key: bool = False,
    ) -> ReviewPackResult:
        primary_sources = {
            "bundle": Path(bundle_path),
            "receipt": Path(receipt_path),
            "summary": Path(summary_path),
        }
        for name, path in primary_sources.items():
            if not path.exists():
                raise FileNotFoundError(f"{name} source file was not found: {path}")

        primary_dir = self.output_dir / PRIMARY_DIRNAME
        review_dir = self.output_dir / REVIEW_DIRNAME
        supporting_dir = self.output_dir / SUPPORTING_DIRNAME
        primary_dir.mkdir(parents=True, exist_ok=True)
        review_dir.mkdir(parents=True, exist_ok=True)

        copied_primary = {
            name: _copy_file(path, primary_dir / PRIMARY_FILENAMES[name])
            for name, path in primary_sources.items()
        }

        bundle = _load_json(copied_primary["bundle"])
        receipt = _load_json(copied_primary["receipt"])
        summary = _load_json(copied_primary["summary"])

        copied_supporting: dict[str, Path] = {}
        missing_supporting: list[str] = []
        for name, raw_path in (supporting_files or {}).items():
            if name == "private_key" and not include_private_key:
                continue
            source = Path(raw_path)
            if not source.exists():
                missing_supporting.append(name)
                continue
            destination_name = SUPPORTING_FILENAMES.get(name, source.name)
            copied_supporting[name] = _copy_file(source, supporting_dir / destination_name)

        primary_refs = {
            name: str(path.relative_to(self.output_dir)) for name, path in copied_primary.items()
        }
        supporting_refs = {
            name: str(path.relative_to(self.output_dir)) for name, path in copied_supporting.items()
        }
        report_path = review_dir / REPORT_FILENAME
        report_pdf_path = review_dir / REPORT_PDF_FILENAME
        rendered_report = ReviewPackRenderer().render(
            bundle=bundle,
            receipt=receipt,
            summary=summary,
            primary_files=primary_refs,
            supporting_files=supporting_refs,
            missing_supporting=missing_supporting,
        )
        report_path.write_text(rendered_report.markdown, encoding="utf-8")
        write_review_report_pdf(rendered_report.markdown, report_pdf_path)

        index_path = self.output_dir / PACK_INDEX_FILENAME
        index_payload = {
            "primary_files": primary_refs,
            "supporting_files": supporting_refs,
            "excluded_supporting_files": (
                ["private_key"]
                if supporting_files
                and "private_key" in supporting_files
                and not include_private_key
                else []
            ),
            "missing_supporting_files": missing_supporting,
            "report_path": str(report_path.relative_to(self.output_dir)),
            "receipt_facts": _receipt_facts(receipt),
            "summary_orientation": _summary_orientation(summary),
        }
        index_path.write_text(
            json.dumps(index_payload, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )

        return ReviewPackResult(
            pack_dir=self.output_dir,
            primary_files=copied_primary,
            supporting_files=copied_supporting,
            index_path=index_path,
            report_path=report_path,
            report_pdf_path=report_pdf_path,
        )
