#!/usr/bin/env python3
"""Validate the AFAC2026 TRPS final submission pack."""

from __future__ import annotations

import json
import re
import subprocess
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "outputs"
ZIP_PATH = OUTPUT_DIR / "TRPS_AFAC2026_FINAL_SUBMISSION_PACK.zip"
SHA_PATH = OUTPUT_DIR / "TRPS_AFAC2026_FINAL_SUBMISSION_PACK.sha256"
STAGING_ROOT = OUTPUT_DIR / "final_pack_staging" / "TRPS_AFAC2026_FINAL_SUBMISSION_PACK"

REQUIRED_FILES = [
    "README.md",
    "00_acceptance_from_v0_2.md",
    "01_final_submission_overview.md",
    "02_portal_copybook_final.md",
    "03_project_solution_final.md",
    "04_business_plan_final.md",
    "05_governance_note_final.md",
    "06_demo_guide_final.md",
    "07_pitch_script_8min.md",
    "08_demo_script_3min.md",
    "09_qa_defense_final.md",
    "10_slide_deck_content_final.md",
    "11_final_submission_checklist.md",
    "12_manual_submission_steps.md",
    "13_risk_register.md",
    "14_claim_evidence_map_final.md",
    "15_file_manifest_final.md",
    "scripts/collect_final_pack.py",
    "scripts/build_final_zip.py",
    "scripts/validate_final_pack.py",
    "scripts/run_all.sh",
    "outputs/final_pack_manifest.json",
    "outputs/final_pack_manifest.md",
    "outputs/final_submission_readiness_score.json",
    "outputs/final_submission_readiness_score.md",
]


def guarded_claim_terms() -> list[str]:
    return [
        "live-market " + "validated",
        "production-ready autonomous " + "trading",
        "guaranteed " + "profit",
        "regulatory " + "certified",
        "bank-" + "approved",
        "regulator-" + "approved",
        "outperforms real bank " + "systems",
        "real-market profitability " + "evidence",
    ]


def guarded_execution_terms() -> list[str]:
    return [
        "bro" + "ker",
        "live" + "_order",
        "real" + "_order",
        "place" + "_order",
        "submit" + "_order",
        "trading" + "_api",
    ]


def load_json(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def iter_text_files() -> list[Path]:
    paths = []
    for path in sorted(ROOT.rglob("*")):
        if not path.is_file() or "final_pack_staging" in path.parts:
            continue
        if "__pycache__" in path.parts:
            continue
        if path.suffix.lower() in {".md", ".json", ".py", ".sh", ".html", ".js", ".css"}:
            paths.append(path)
    return paths


def allowed_execution_context(path: Path, line: str) -> bool:
    lowered = line.lower()
    if path.name == "validate_final_pack.py":
        return True
    return any(
        marker in lowered
        for marker in [
            "forbidden",
            "禁止",
            "不能",
            "不接",
            "不连接",
            "does not",
            "do not",
            "no ",
            "keyword",
        ]
    )


def find_claim_hits() -> list[dict[str, object]]:
    hits = []
    for path in iter_text_files():
        text = read_text(path).lower()
        for term in guarded_claim_terms():
            count = text.count(term.lower())
            if count:
                hits.append({"path": str(path.relative_to(ROOT)), "term": term, "count": count})
    return hits


def find_execution_hits() -> tuple[list[dict[str, object]], int]:
    hits = []
    unallowed_count = 0
    for path in iter_text_files():
        for lineno, line in enumerate(read_text(path).splitlines(), start=1):
            lowered = line.lower()
            for term in guarded_execution_terms():
                if term.lower() not in lowered:
                    continue
                count = lowered.count(term.lower())
                allowed = allowed_execution_context(path, line)
                hits.append(
                    {
                        "path": str(path.relative_to(ROOT)),
                        "line": lineno,
                        "term": term,
                        "count": count,
                        "allowed_context": allowed,
                    }
                )
                if not allowed:
                    unallowed_count += count
    return hits, unallowed_count


def zip_checks(report: dict[str, object], errors: list[str]) -> None:
    report["zip_exists"] = ZIP_PATH.exists()
    if not ZIP_PATH.exists():
        errors.append("zip_missing")
        return
    forbidden_parts = [".git", ".venv", "node_modules", "__pycache__"]
    forbidden_names = [".env", "afac2026_final_submission.zip", "presentation.pptx"]
    with zipfile.ZipFile(ZIP_PATH) as archive:
        names = archive.namelist()
        report["zip_file_count"] = len(names)
        report["zip_root_ok"] = all(
            name.startswith("TRPS_AFAC2026_FINAL_SUBMISSION_PACK/") for name in names
        )
        bad = [
            name
            for name in names
            if any(part in name.split("/") for part in forbidden_parts)
            or any(name.endswith(forbidden) for forbidden in forbidden_names)
        ]
        report["zip_forbidden_entries"] = bad
        report["zip_demo_index_found"] = any(
            name.endswith("v0_2_demo/demo/index.html") for name in names
        )
        report["zip_portal_copybook_found"] = any(
            name.endswith("final_docs/02_portal_copybook_final.md") for name in names
        )
    if not report["zip_root_ok"]:
        errors.append("zip_root_not_expected")
    if report["zip_forbidden_entries"]:
        errors.append("zip_forbidden_entries")
    if not report["zip_demo_index_found"]:
        errors.append("zip_demo_index_missing")
    if not report["zip_portal_copybook_found"]:
        errors.append("zip_portal_copybook_missing")


def detect_python_warning() -> list[str]:
    command = [
        ".venv/bin/agent-evidence",
        "validate-profile",
        "examples/minimal-valid-evidence.json",
    ]
    try:
        completed = subprocess.run(
            command,
            cwd=ROOT.parents[1],
            text=True,
            capture_output=True,
            check=False,
        )
    except Exception as exc:  # pragma: no cover - environment guard.
        return [f"profile_validator_warning_check_failed:{exc}"]
    combined = completed.stdout + completed.stderr
    warnings = []
    if "Pydantic V1" in combined or "Python 3.14" in combined:
        warnings.append("Python 3.14/Pydantic warning observed in profile validator")
    return warnings


def write_reports(report: dict[str, object]) -> None:
    def write_json(path: Path, data: dict[str, object]) -> None:
        path.write_text(
            json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )

    write_json(OUTPUT_DIR / "validation_report.json", report)
    lines = [
        "# Final Pack Validation Report",
        "",
        f"- `ok`: `{report['ok']}`",
        f"- `zip_exists`: `{report.get('zip_exists')}`",
        f"- `zip_size_bytes`: `{report.get('zip_size_bytes')}`",
        f"- `zip_sha256`: `{report.get('zip_sha256')}`",
        f"- `readiness_score`: `{report.get('readiness_score')}`",
        f"- `qa_question_count`: `{report.get('qa_question_count')}`",
        f"- `forbidden_claim_hit_count`: `{report['forbidden_claim_hit_count']}`",
        f"- `real_api_keyword_hit_count`: `{report['real_api_keyword_hit_count']}`",
        f"- `true_order_count`: `{report.get('true_order_count')}`",
        f"- `external_execution_connected`: `{report.get('external_execution_connected')}`",
        f"- `policy_violation_count`: `{report.get('policy_violation_count')}`",
        "",
        "## Non-Blocking Warnings",
        "",
    ]
    lines.extend(f"- `{warning}`" for warning in report["non_blocking_warnings"])
    if report["errors"]:
        lines.extend(["", "## Errors", ""])
        lines.extend(f"- `{error}`" for error in report["errors"])
    lines.append("")
    (OUTPUT_DIR / "validation_report.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    errors: list[str] = []
    missing = [path for path in REQUIRED_FILES if not (ROOT / path).exists()]
    if missing:
        errors.append(f"missing_required_files:{','.join(missing)}")

    report: dict[str, object] = {
        "ok": False,
        "missing_required_files": missing,
        "errors": errors,
        "non_blocking_warnings": detect_python_warning(),
        "affected_eeoap_clauses": [
            "EEOAP-001",
            "EEOAP-003",
            "EEOAP-004",
            "EEOAP-005",
        ],
    }

    zip_checks(report, errors)
    score = load_json(OUTPUT_DIR / "final_submission_readiness_score.json")
    v1_metrics = load_json(
        ROOT.parent / "afac2026_productization_v0_1" / "outputs" / "demo_metrics.json"
    )
    assert isinstance(score, dict)
    assert isinstance(v1_metrics, dict)
    report["readiness_score"] = score["total_score"]
    report["policy_violation_count"] = int(v1_metrics.get("policy_violation_count", -1))
    report["true_order_count"] = int(v1_metrics.get("actual_transaction_generated_count", -1))
    report["external_execution_connected"] = bool(
        v1_metrics.get("external_execution_connected", True)
    )
    report["qa_question_count"] = len(
        re.findall(r"^## Q\d+\.", read_text(ROOT / "09_qa_defense_final.md"), re.M)
    )
    report["final_pack_sha256_exists"] = SHA_PATH.exists()
    report["zip_size_bytes"] = ZIP_PATH.stat().st_size if ZIP_PATH.exists() else 0
    report["zip_sha256"] = (
        SHA_PATH.read_text(encoding="utf-8").split()[0] if SHA_PATH.exists() else None
    )

    claim_hits = find_claim_hits()
    execution_hits, execution_hit_count = find_execution_hits()
    report["forbidden_claim_hits"] = claim_hits
    report["forbidden_claim_hit_count"] = sum(int(hit["count"]) for hit in claim_hits)
    report["real_api_keyword_hits"] = execution_hits
    report["real_api_keyword_hit_count"] = execution_hit_count

    if report["qa_question_count"] < 50:
        errors.append("qa_question_count_lt_50")
    if report["forbidden_claim_hit_count"] != 0:
        errors.append("forbidden_claim_hits")
    if report["real_api_keyword_hit_count"] != 0:
        errors.append("real_api_keyword_hits")
    if report["true_order_count"] != 0:
        errors.append("true_order_count_nonzero")
    if report["external_execution_connected"]:
        errors.append("external_execution_connected")
    if report["policy_violation_count"] != 0:
        errors.append("policy_violation_count_nonzero")
    if float(report["readiness_score"]) < 90:
        errors.append("readiness_score_lt_90")
    if not report["final_pack_sha256_exists"]:
        errors.append("final_pack_sha256_missing")
    if not report["non_blocking_warnings"]:
        errors.append("python_314_pydantic_warning_not_recorded")

    report["errors"] = errors
    report["ok"] = not errors
    write_reports(report)
    print(
        json.dumps(
            {
                "ok": report["ok"],
                "zip_size_bytes": report["zip_size_bytes"],
                "zip_sha256": report["zip_sha256"],
                "readiness_score": report["readiness_score"],
                "forbidden_claim_hit_count": report["forbidden_claim_hit_count"],
                "real_api_keyword_hit_count": report["real_api_keyword_hit_count"],
                "true_order_count": report["true_order_count"],
            },
            sort_keys=True,
        )
    )
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
