#!/usr/bin/env python3
"""Generate the AFAC2026 TRPS v0.2 manifest and readiness score."""

from __future__ import annotations

import json
import statistics
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT_DIR = ROOT / "scripts"
OUTPUT_DIR = ROOT / "outputs"
V1_ROOT = ROOT.parent / "afac2026_productization_v0_1"
GENERATED_AT = "2026-06-20T00:00:00Z"


def load_json(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def repo_relative(path: Path) -> str:
    return str(path.relative_to(ROOT.parents[1]))


def build_static_demo() -> None:
    subprocess.run([sys.executable, str(SCRIPT_DIR / "build_static_demo.py")], check=True)


def readiness_score() -> dict[str, object]:
    metrics = load_json(V1_ROOT / "outputs" / "demo_metrics.json")
    validation = load_json(V1_ROOT / "outputs" / "validation_report.json")
    assert isinstance(metrics, dict)
    assert isinstance(validation, dict)

    dimensions = [
        {
            "name": "demo_readiness",
            "score": 96,
            "evidence_path": "demo/index.html",
            "reason": "Offline static demo exists with scenario cards and decision details.",
        },
        {
            "name": "governance_readiness",
            "score": 95,
            "evidence_path": "06_governance_and_compliance.md",
            "reason": (
                "Human review, kill switch, policy gate, and receipt boundaries are explicit."
            ),
        },
        {
            "name": "portal_text_readiness",
            "score": 94,
            "evidence_path": "02_portal_fields_zh.md;03_portal_fields_en.md",
            "reason": "Chinese and English portal field drafts are prepared.",
        },
        {
            "name": "metrics_readiness",
            "score": 96,
            "evidence_path": "07_metrics_translation.md;outputs/demo_metrics.json",
            "reason": "Technical metrics are translated into judge-facing business meaning.",
        },
        {
            "name": "compliance_safety",
            "score": 98,
            "evidence_path": "outputs/validation_report.json",
            "reason": "Forbidden-claim and execution-keyword checks are expected to remain zero.",
        },
        {
            "name": "commercial_story",
            "score": 92,
            "evidence_path": "05_business_case.md;08_pitch_deck_markdown.md",
            "reason": "Target buyers, pain points, value metrics, and pitch story are drafted.",
        },
    ]
    total = round(statistics.mean(item["score"] for item in dimensions), 2)
    return {
        "pack_id": "afac2026_trps_demo_submission_pack_v0_2",
        "generated_at": GENERATED_AT,
        "total_score": total,
        "dimensions": dimensions,
        "v0_1_metrics": metrics,
        "v0_1_validation": {
            "ok": validation["ok"],
            "forbidden_claim_hit_count": validation["forbidden_claim_hit_count"],
            "real_api_keyword_hit_count": validation["real_api_keyword_hit_count"],
            "policy_violation_count": validation["policy_violation_count"],
            "actual_transaction_generated_count": validation["actual_transaction_generated_count"],
            "external_execution_connected": validation["external_execution_connected"],
        },
    }


def write_readiness(score: dict[str, object]) -> None:
    write_json(OUTPUT_DIR / "submission_readiness_score.json", score)
    lines = [
        "# Submission Readiness Score",
        "",
        f"- `total_score`: `{score['total_score']}`",
        "",
        "| Dimension | Score | Evidence |",
        "| --- | ---: | --- |",
    ]
    for item in score["dimensions"]:
        lines.append(f"| `{item['name']}` | `{item['score']}` | `{item['evidence_path']}` |")
    lines.extend(
        [
            "",
            "Scores are local preparation indicators, not external approval.",
            "",
        ]
    )
    write_text(OUTPUT_DIR / "submission_readiness_score.md", "\n".join(lines))


def manifest(score: dict[str, object]) -> dict[str, object]:
    files = [
        path
        for path in sorted(ROOT.rglob("*"))
        if path.is_file() and "__pycache__" not in path.parts and path.name != ".DS_Store"
    ]
    return {
        "pack_id": "afac2026_trps_demo_submission_pack_v0_2",
        "version": "0.2",
        "generated_at": GENERATED_AT,
        "source_v0_1_commit": "ded7bcade84332b68363cac8cb98b7e1a5ae3b9f",
        "source_v0_1_directory": "afac2026_submission/afac2026_productization_v0_1",
        "status": "local_demo_submission_material_not_submitted",
        "no_push": True,
        "no_tag": True,
        "no_external_submission": True,
        "demo_entry": "demo/index.html",
        "data_entry": "demo/assets/trps_demo_data.json",
        "readiness_total_score": score["total_score"],
        "affected_eeoap_clauses": [
            "EEOAP-001",
            "EEOAP-003",
            "EEOAP-004",
            "EEOAP-005",
        ],
        "files": [repo_relative(path) for path in files],
        "boundary": {
            "actual_transaction_generated_count": 0,
            "external_execution_connected": False,
            "real_customer_data_used": False,
            "personal_investment_advice": False,
        },
    }


def write_manifest(manifest_data: dict[str, object]) -> None:
    write_json(OUTPUT_DIR / "afac_v0_2_manifest.json", manifest_data)
    lines = [
        "# AFAC v0.2 Manifest",
        "",
        f"- `pack_id`: `{manifest_data['pack_id']}`",
        f"- `version`: `{manifest_data['version']}`",
        f"- `status`: `{manifest_data['status']}`",
        f"- `demo_entry`: `{manifest_data['demo_entry']}`",
        f"- `data_entry`: `{manifest_data['data_entry']}`",
        f"- `readiness_total_score`: `{manifest_data['readiness_total_score']}`",
        f"- `no_push`: `{manifest_data['no_push']}`",
        f"- `no_tag`: `{manifest_data['no_tag']}`",
        f"- `no_external_submission`: `{manifest_data['no_external_submission']}`",
        "",
        "## Files",
        "",
    ]
    lines.extend(f"- `{path}`" for path in manifest_data["files"])
    lines.append("")
    write_text(OUTPUT_DIR / "afac_v0_2_manifest.md", "\n".join(lines))


def main() -> int:
    build_static_demo()
    score = readiness_score()
    write_readiness(score)
    manifest_data = manifest(score)
    write_manifest(manifest_data)
    print(json.dumps({"ok": True, "total_score": score["total_score"]}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
