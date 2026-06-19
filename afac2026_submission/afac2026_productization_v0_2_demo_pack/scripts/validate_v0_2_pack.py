#!/usr/bin/env python3
"""Validate the local AFAC2026 TRPS v0.2 demo and submission pack."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "outputs"
V1_ROOT = ROOT.parent / "afac2026_productization_v0_1"


REQUIRED_FILES = [
    "README.md",
    "00_v0_1_acceptance.md",
    "01_static_demo_guide.md",
    "02_portal_fields_zh.md",
    "03_portal_fields_en.md",
    "04_project_solution.md",
    "05_business_case.md",
    "06_governance_and_compliance.md",
    "07_metrics_translation.md",
    "08_pitch_deck_markdown.md",
    "09_qa_defense_30_questions.md",
    "10_claim_evidence_map.md",
    "11_submission_checklist.md",
    "demo/index.html",
    "demo/style.css",
    "demo/app.js",
    "demo/assets/trps_demo_data.json",
    "scripts/build_static_demo.py",
    "scripts/generate_submission_pack.py",
    "scripts/validate_v0_2_pack.py",
    "scripts/run_all.sh",
    "outputs/.gitkeep",
    "outputs/afac_v0_2_manifest.json",
    "outputs/afac_v0_2_manifest.md",
    "outputs/submission_readiness_score.json",
    "outputs/submission_readiness_score.md",
]

V1_REQUIRED_OUTPUTS = [
    "demo_receipts.json",
    "demo_metrics.json",
    "demo_summary.md",
    "validation_report.json",
]

PORTAL_ZH_HEADINGS = [
    "## 中文项目名称",
    "## 中文一句话简介（120 字以内）",
    "## 中文项目摘要（500 字以内）",
    "## 中文技术创新（500 字以内）",
    "## 中文应用场景（500 字以内）",
    "## 中文商业价值（500 字以内）",
    "## 中文合规边界（300 字以内）",
    "## 中文关键词",
]

PORTAL_EN_HEADINGS = [
    "## Project Name",
    "## One-Sentence Summary",
    "## Project Abstract",
    "## Technical Innovation",
    "## Application Scenarios",
    "## Business Value",
    "## Governance Boundary",
    "## Keywords",
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
    return path.read_text(encoding="utf-8")


def iter_text_files() -> list[Path]:
    paths: list[Path] = []
    for path in sorted(ROOT.rglob("*")):
        if not path.is_file() or "__pycache__" in path.parts:
            continue
        if path.suffix.lower() in {".html", ".css", ".js", ".json", ".md", ".py", ".sh"}:
            paths.append(path)
    return paths


def allowed_execution_context(path: Path, line: str) -> bool:
    lowered = line.lower()
    if path.name == "validate_v0_2_pack.py":
        return True
    markers = [
        "forbidden",
        "禁止",
        "不能",
        "不得",
        "不接",
        "不连接",
        "does not",
        "do not",
        "no ",
        "keyword",
        "allowlist",
    ]
    return any(marker in lowered for marker in markers)


def find_claim_hits(terms: list[str]) -> list[dict[str, object]]:
    hits: list[dict[str, object]] = []
    for path in iter_text_files():
        text = read_text(path).lower()
        for term in terms:
            count = text.count(term.lower())
            if count:
                hits.append({"path": str(path.relative_to(ROOT)), "term": term, "count": count})
    return hits


def find_execution_hits(terms: list[str]) -> tuple[list[dict[str, object]], int]:
    hits: list[dict[str, object]] = []
    total = 0
    for path in iter_text_files():
        for lineno, line in enumerate(read_text(path).splitlines(), start=1):
            lowered = line.lower()
            for term in terms:
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
                    total += count
    return hits, total


def json_files_ok(errors: list[str]) -> list[str]:
    parsed: list[str] = []
    for path in sorted(ROOT.rglob("*.json")):
        if "__pycache__" in path.parts:
            continue
        try:
            load_json(path)
            parsed.append(str(path.relative_to(ROOT)))
        except Exception as exc:  # pragma: no cover - command-line guard.
            errors.append(f"json_parse_error:{path.relative_to(ROOT)}:{exc}")
    return parsed


def validate_v1_outputs(report: dict[str, object], errors: list[str]) -> None:
    missing = [name for name in V1_REQUIRED_OUTPUTS if not (V1_ROOT / "outputs" / name).exists()]
    if missing:
        errors.append(f"missing_v0_1_outputs:{','.join(missing)}")
        report["v0_1_outputs_readable"] = False
        return
    metrics = load_json(V1_ROOT / "outputs" / "demo_metrics.json")
    validation = load_json(V1_ROOT / "outputs" / "validation_report.json")
    assert isinstance(metrics, dict)
    assert isinstance(validation, dict)
    report["v0_1_outputs_readable"] = True
    report["policy_violation_count"] = int(metrics.get("policy_violation_count", -1))
    report["actual_transaction_generated_count"] = int(
        metrics.get("actual_transaction_generated_count", -1)
    )
    report["external_execution_connected"] = bool(metrics.get("external_execution_connected", True))
    report["v0_1_validation_ok"] = bool(validation.get("ok"))


def validate_content(report: dict[str, object], errors: list[str]) -> None:
    zh_text = read_text(ROOT / "02_portal_fields_zh.md")
    en_text = read_text(ROOT / "03_portal_fields_en.md")
    missing_zh = [heading for heading in PORTAL_ZH_HEADINGS if heading not in zh_text]
    missing_en = [heading for heading in PORTAL_EN_HEADINGS if heading not in en_text]
    if missing_zh:
        errors.append(f"missing_portal_zh_headings:{len(missing_zh)}")
    if missing_en:
        errors.append(f"missing_portal_en_headings:{len(missing_en)}")
    report["portal_zh_fields_ok"] = not missing_zh
    report["portal_en_fields_ok"] = not missing_en

    pitch_pages = len(
        re.findall(
            r"^## Page \d+\.",
            read_text(ROOT / "08_pitch_deck_markdown.md"),
            re.M,
        )
    )
    qa_count = len(
        re.findall(
            r"^### Q\d+\.",
            read_text(ROOT / "09_qa_defense_30_questions.md"),
            re.M,
        )
    )
    report["pitch_page_count"] = pitch_pages
    report["qa_question_count"] = qa_count
    if pitch_pages != 12:
        errors.append(f"pitch_page_count_not_12:{pitch_pages}")
    if qa_count < 30:
        errors.append(f"qa_question_count_lt_30:{qa_count}")

    claim_map_exists = (ROOT / "10_claim_evidence_map.md").exists()
    report["claim_evidence_map_exists"] = claim_map_exists
    if not claim_map_exists:
        errors.append("claim_evidence_map_missing")


def write_reports(report: dict[str, object]) -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUTPUT_DIR / "validation_report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    lines = [
        "# AFAC2026 TRPS v0.2 Validation Report",
        "",
        f"- `ok`: `{report['ok']}`",
        f"- `required_files_ok`: `{report['required_files_ok']}`",
        f"- `demo_index_exists`: `{report['demo_index_exists']}`",
        f"- `demo_data_exists`: `{report['demo_data_exists']}`",
        f"- `portal_zh_fields_ok`: `{report.get('portal_zh_fields_ok')}`",
        f"- `portal_en_fields_ok`: `{report.get('portal_en_fields_ok')}`",
        f"- `pitch_page_count`: `{report.get('pitch_page_count')}`",
        f"- `qa_question_count`: `{report.get('qa_question_count')}`",
        f"- `forbidden_claim_hit_count`: `{report['forbidden_claim_hit_count']}`",
        f"- `real_api_keyword_hit_count`: `{report['real_api_keyword_hit_count']}`",
        f"- `policy_violation_count`: `{report.get('policy_violation_count')}`",
        "- `actual_transaction_generated_count`: "
        f"`{report.get('actual_transaction_generated_count')}`",
        f"- `external_execution_connected`: `{report.get('external_execution_connected')}`",
        "",
        "Affected local EEOAP clauses: `EEOAP-001`, `EEOAP-003`, `EEOAP-004`, `EEOAP-005`.",
        "",
    ]
    if report["errors"]:
        lines.extend(["## Errors", ""])
        lines.extend(f"- `{error}`" for error in report["errors"])
        lines.append("")
    (OUTPUT_DIR / "validation_report.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    errors: list[str] = []
    missing_required = [path for path in REQUIRED_FILES if not (ROOT / path).exists()]
    if missing_required:
        errors.append(f"missing_required_files:{','.join(missing_required)}")

    report: dict[str, object] = {
        "ok": False,
        "required_file_count": len(REQUIRED_FILES),
        "missing_required_files": missing_required,
        "required_files_ok": not missing_required,
        "demo_index_exists": (ROOT / "demo" / "index.html").exists(),
        "demo_data_exists": (ROOT / "demo" / "assets" / "trps_demo_data.json").exists(),
        "errors": errors,
        "affected_eeoap_clauses": [
            "EEOAP-001",
            "EEOAP-003",
            "EEOAP-004",
            "EEOAP-005",
        ],
    }

    report["json_files_parsed"] = json_files_ok(errors)
    validate_v1_outputs(report, errors)
    if not missing_required:
        validate_content(report, errors)

    claim_hits = find_claim_hits(guarded_claim_terms())
    execution_hits, execution_unallowed_count = find_execution_hits(guarded_execution_terms())
    report["forbidden_claim_hits"] = claim_hits
    report["forbidden_claim_hit_count"] = sum(int(hit["count"]) for hit in claim_hits)
    report["real_api_keyword_hits"] = execution_hits
    report["real_api_keyword_hit_count"] = execution_unallowed_count

    if report["forbidden_claim_hit_count"]:
        errors.append("forbidden_claim_hits")
    if report["real_api_keyword_hit_count"]:
        errors.append("real_api_keyword_hits")
    if report.get("policy_violation_count") != 0:
        errors.append("policy_violation_count_nonzero")
    if report.get("actual_transaction_generated_count") != 0:
        errors.append("actual_transaction_generated")
    if report.get("external_execution_connected"):
        errors.append("external_execution_connected")

    report["errors"] = errors
    report["ok"] = not errors
    write_reports(report)
    print(
        json.dumps(
            {
                "ok": report["ok"],
                "forbidden_claim_hit_count": report["forbidden_claim_hit_count"],
                "real_api_keyword_hit_count": report["real_api_keyword_hit_count"],
                "policy_violation_count": report.get("policy_violation_count"),
            },
            sort_keys=True,
        )
    )
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
