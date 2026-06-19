#!/usr/bin/env python3
"""Validate the local AFAC2026 TRPS productization pack."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "outputs"


REQUIRED_FILES = [
    "README.md",
    "00_inventory.md",
    "01_positioning.md",
    "02_demo_storyboard.md",
    "03_decision_schema.json",
    "04_action_ontology.json",
    "05_policy_constraints.json",
    "06_receipt_schema.json",
    "07_demo_scenarios.json",
    "08_metrics_plan.md",
    "09_governance_note.md",
    "10_pitch_outline.md",
    "scripts/run_afac_trps_demo.py",
    "scripts/validate_afac_pack.py",
    "outputs/.gitkeep",
    "outputs/demo_receipts.json",
    "outputs/demo_metrics.json",
    "outputs/demo_summary.md",
]


JSON_FILES = [
    "03_decision_schema.json",
    "04_action_ontology.json",
    "05_policy_constraints.json",
    "06_receipt_schema.json",
    "07_demo_scenarios.json",
    "outputs/demo_receipts.json",
    "outputs/demo_metrics.json",
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


def iter_text_files(root: Path) -> Iterable[Path]:
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        if path.suffix.lower() in {".md", ".json", ".py", ".txt"}:
            yield path


def find_hits(terms: list[str]) -> list[dict[str, object]]:
    hits: list[dict[str, object]] = []
    for path in iter_text_files(ROOT):
        text = path.read_text(encoding="utf-8", errors="ignore").lower()
        for term in terms:
            term_lower = term.lower()
            if term_lower in text:
                hits.append(
                    {
                        "path": str(path.relative_to(ROOT)),
                        "term_hash": abs(hash(term_lower)) % 1000000,
                        "count": text.count(term_lower),
                    }
                )
    return hits


def required_receipt_fields() -> list[str]:
    schema = load_json(ROOT / "06_receipt_schema.json")
    assert isinstance(schema, dict)
    return list(schema["required"])


def validate_receipts(report: dict[str, object]) -> None:
    scenarios = load_json(ROOT / "07_demo_scenarios.json")
    receipts = load_json(OUTPUT_DIR / "demo_receipts.json")
    metrics = load_json(OUTPUT_DIR / "demo_metrics.json")
    assert isinstance(scenarios, dict)
    assert isinstance(receipts, dict)
    assert isinstance(metrics, dict)

    scenario_ids = {scenario["scenario_id"] for scenario in scenarios["scenarios"]}
    decisions = receipts.get("decisions", [])
    decision_scenario_ids = {decision.get("scenario_id") for decision in decisions}
    report["scenario_count"] = len(scenario_ids)
    report["decision_count"] = len(decisions)
    report["scenario_receipt_coverage_ok"] = scenario_ids == decision_scenario_ids

    missing_fields: list[dict[str, object]] = []
    fields = required_receipt_fields()
    actual_transaction_count = 0
    external_execution_connected = False
    for decision in decisions:
        receipt = decision.get("receipt", {})
        missing = [field for field in fields if not receipt.get(field)]
        if missing:
            missing_fields.append({"decision_id": decision.get("decision_id"), "missing": missing})
        simulated = decision.get("simulated_execution", {})
        if simulated.get("actual_transaction_generated"):
            actual_transaction_count += 1
        if simulated.get("external_execution_connected"):
            external_execution_connected = True

    report["receipt_missing_fields"] = missing_fields
    report["receipt_completeness_ok"] = not missing_fields
    report["policy_violation_count"] = int(metrics.get("policy_violation_count", -1))
    report["actual_transaction_generated_count"] = actual_transaction_count
    report["external_execution_connected"] = external_execution_connected


def write_reports(report: dict[str, object]) -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUTPUT_DIR / "validation_report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    lines = [
        "# AFAC2026 TRPS Productization Validation Report",
        "",
        f"- `ok`: `{report['ok']}`",
        f"- `scenario_count`: `{report.get('scenario_count')}`",
        f"- `decision_count`: `{report.get('decision_count')}`",
        f"- `scenario_receipt_coverage_ok`: `{report.get('scenario_receipt_coverage_ok')}`",
        f"- `receipt_completeness_ok`: `{report.get('receipt_completeness_ok')}`",
        f"- `policy_violation_count`: `{report.get('policy_violation_count')}`",
        f"- `forbidden_claim_hit_count`: `{report.get('forbidden_claim_hit_count')}`",
        f"- `real_api_keyword_hit_count`: `{report.get('real_api_keyword_hit_count')}`",
        "- `actual_transaction_generated_count`: "
        f"`{report.get('actual_transaction_generated_count')}`",
        f"- `external_execution_connected`: `{report.get('external_execution_connected')}`",
        "",
        "Affected local EEOAP clauses: `EEOAP-001`, `EEOAP-003`, `EEOAP-004`, `EEOAP-005`.",
        "",
    ]
    if report.get("errors"):
        lines.extend(["## Errors", ""])
        lines.extend(f"- `{error}`" for error in report["errors"])
        lines.append("")
    (OUTPUT_DIR / "validation_report.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    errors: list[str] = []
    missing_files = [path for path in REQUIRED_FILES if not (ROOT / path).exists()]
    if missing_files:
        errors.append(f"missing_required_files:{','.join(missing_files)}")

    json_parse_errors: list[str] = []
    for relative_path in JSON_FILES:
        path = ROOT / relative_path
        if not path.exists():
            continue
        try:
            load_json(path)
        except Exception as exc:  # pragma: no cover - command-line guard.
            json_parse_errors.append(f"{relative_path}:{exc}")
    if json_parse_errors:
        errors.append("json_parse_errors")

    report: dict[str, object] = {
        "ok": False,
        "required_file_count": len(REQUIRED_FILES),
        "missing_required_files": missing_files,
        "json_parse_errors": json_parse_errors,
        "errors": errors,
        "affected_eeoap_clauses": ["EEOAP-001", "EEOAP-003", "EEOAP-004", "EEOAP-005"],
    }

    if not missing_files and not json_parse_errors:
        validate_receipts(report)

    forbidden_claim_hits = find_hits(guarded_claim_terms())
    real_api_hits = find_hits(guarded_execution_terms())
    report["forbidden_claim_hit_count"] = sum(int(hit["count"]) for hit in forbidden_claim_hits)
    report["real_api_keyword_hit_count"] = sum(int(hit["count"]) for hit in real_api_hits)
    report["forbidden_claim_hits"] = forbidden_claim_hits
    report["real_api_keyword_hits"] = real_api_hits

    if report["forbidden_claim_hit_count"]:
        errors.append("forbidden_claim_hits")
    if report["real_api_keyword_hit_count"]:
        errors.append("real_api_keyword_hits")
    if report.get("scenario_receipt_coverage_ok") is False:
        errors.append("scenario_receipt_coverage_failed")
    if report.get("receipt_completeness_ok") is False:
        errors.append("receipt_completeness_failed")
    if report.get("policy_violation_count", 0) != 0:
        errors.append("policy_violation_count_nonzero")
    if report.get("actual_transaction_generated_count", 0) != 0:
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
                "actual_transaction_generated_count": report.get(
                    "actual_transaction_generated_count"
                ),
                "external_execution_connected": report.get("external_execution_connected"),
            },
            sort_keys=True,
        )
    )
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
