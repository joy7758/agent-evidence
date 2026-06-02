from __future__ import annotations

# ruff: noqa: E501,E402,I001

import argparse
import copy
import hashlib
import json
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from agent_evidence.oap import (
    PROFILE_NAME,
    PROFILE_VERSION,
    SCHEMA_PATH,
    validate_profile_file,
    with_recomputed_integrity,
)

CASES_ROOT = ROOT / "cases" / "se_workflows"
REPORTS_ROOT = ROOT / "reports"


@dataclass(frozen=True)
class CaseInfo:
    slug: str
    name: str
    runner_name: str
    operation_type: str


CASES = {
    "issue_pr_metadata": CaseInfo(
        slug="issue_pr_metadata",
        name="Issue / PR metadata operation",
        runner_name="run_case_issue_pr_metadata.py",
        operation_type="repository.issue_metadata_update",
    ),
    "doc_data_transform": CaseInfo(
        slug="doc_data_transform",
        name="Documentation / data transformation operation",
        runner_name="run_case_doc_data_transform.py",
        operation_type="documentation.metadata_transform",
    ),
    "test_result_summary": CaseInfo(
        slug="test_result_summary",
        name="Test-result summarization operation",
        runner_name="run_case_test_result_summary.py",
        operation_type="test.result_summarize",
    ),
}


def canonical_json_bytes(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode(
        "utf-8"
    )


def sha256_digest(value: Any) -> str:
    return "sha256:" + hashlib.sha256(canonical_json_bytes(value)).hexdigest()


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value, encoding="utf-8")


def object_ref(
    ref_id: str, role: str, object_id: str, payload: Any, locator: str
) -> dict[str, str]:
    return {
        "ref_id": ref_id,
        "role": role,
        "object_id": object_id,
        "digest": sha256_digest(payload),
        "locator": locator,
    }


def artifact_ref(
    artifact_id: str, artifact_type: str, payload: Any, locator: str
) -> dict[str, str]:
    return {
        "artifact_id": artifact_id,
        "type": artifact_type,
        "digest": sha256_digest(payload),
        "locator": locator,
    }


def build_statement(fixture: dict[str, Any]) -> dict[str, Any]:
    case_id = fixture["case_id"]
    variant_id = fixture["variant_id"]
    ids = fixture["ids"]
    payloads = fixture["payloads"]
    input_payload = payloads["input"]
    output_payload = payloads["output"]
    policy_payload = fixture["policy_payload"]
    operation_log = fixture["operation_payload"]["log"]
    evidence_payload = fixture["evidence_payload"]

    input_ref = object_ref(
        "ref:input",
        "input",
        ids["subject"],
        input_payload,
        f"urn:se-case:{case_id}:{variant_id}:input",
    )
    output_ref = object_ref(
        "ref:output",
        "output",
        ids["output"],
        output_payload,
        f"urn:se-case:{case_id}:{variant_id}:output",
    )
    artifacts = [
        artifact_ref(
            "artifact:operation-log",
            "operation-log",
            operation_log,
            f"urn:se-case:{case_id}:{variant_id}:operation-log",
        ),
        artifact_ref(
            "artifact:policy",
            "policy",
            policy_payload,
            f"urn:se-case:{case_id}:{variant_id}:policy",
        ),
        artifact_ref(
            "artifact:evidence",
            "case-evidence",
            evidence_payload,
            f"urn:se-case:{case_id}:{variant_id}:evidence",
        ),
    ]

    statement = {
        "profile": {"name": PROFILE_NAME, "version": PROFILE_VERSION},
        "statement_id": f"eeoap:{case_id}:{variant_id}",
        "timestamp": "2026-06-02T00:00:00Z",
        "actor": {
            "id": ids["actor"],
            "type": "automation",
            "name": fixture["actor"]["name"],
            "runtime": "representative-local-fixture",
        },
        "subject": {
            "id": ids["subject"],
            "type": fixture["subject"]["type"],
            "digest": sha256_digest(input_payload),
            "locator": f"urn:se-case:{case_id}:{variant_id}:subject",
        },
        "operation": {
            "id": ids["operation"],
            "type": fixture["operation_type"],
            "description": fixture["case_name"],
            "subject_ref": ids["subject"],
            "policy_ref": ids["policy"],
            "input_refs": ["ref:input"],
            "output_refs": ["ref:output"],
            "result": {
                "status": "succeeded",
                "summary": fixture["operation_payload"]["summary"],
            },
        },
        "policy": {
            "id": ids["policy"],
            "name": fixture["policy_payload"]["name"],
            "constraint_refs": ["constraint:case-rule"],
        },
        "constraints": [
            {
                "id": "constraint:case-rule",
                "description": fixture["policy_payload"]["description"],
            }
        ],
        "provenance": {
            "id": ids["provenance"],
            "actor_ref": ids["actor"],
            "operation_ref": ids["operation"],
            "subject_ref": ids["subject"],
            "input_refs": ["ref:input"],
            "output_refs": ["ref:output"],
        },
        "evidence": {
            "id": ids["evidence"],
            "subject_ref": ids["subject"],
            "operation_ref": ids["operation"],
            "policy_ref": ids["policy"],
            "references": [input_ref, output_ref],
            "artifacts": artifacts,
            "integrity": {
                "references_digest": "sha256:" + "0" * 64,
                "artifacts_digest": "sha256:" + "0" * 64,
                "statement_digest": "sha256:" + "0" * 64,
            },
        },
        "validation": {
            "id": ids["validation"],
            "evidence_ref": ids["evidence"],
            "provenance_ref": ids["provenance"],
            "policy_ref": ids["policy"],
            "validator": "agent-evidence validate-profile",
            "method": "schema+reference+consistency+integrity+case-adapter",
            "status": "verifiable",
        },
    }
    statement = with_recomputed_integrity(statement)
    return apply_mutation(statement, fixture.get("mutation"))


def apply_mutation(statement: dict[str, Any], mutation: dict[str, Any] | None) -> dict[str, Any]:
    if not mutation:
        return statement
    mutated = copy.deepcopy(statement)
    kind = mutation["kind"]
    if kind == "missing_policy_ref":
        mutated["evidence"]["policy_ref"] = "policy:missing"
        mutated = with_recomputed_integrity(mutated)
    elif kind == "unresolved_input_ref":
        mutated["operation"]["input_refs"] = ["ref:missing-input"]
        mutated["provenance"]["input_refs"] = ["ref:missing-input"]
        mutated = with_recomputed_integrity(mutated)
    elif kind == "provenance_output_mismatch":
        mutated["provenance"]["output_refs"] = ["ref:stale-output"]
        mutated = with_recomputed_integrity(mutated)
    elif kind == "validation_provenance_missing":
        mutated["validation"]["provenance_ref"] = "prov:missing"
        mutated = with_recomputed_integrity(mutated)
    elif kind == "wrong_derived_output_ref":
        mutated["provenance"]["output_refs"] = ["ref:wrong-derived-output"]
        mutated = with_recomputed_integrity(mutated)
    elif kind == "missing_policy_link":
        mutated["evidence"]["policy_ref"] = "policy:missing"
        mutated = with_recomputed_integrity(mutated)
    elif kind == "digest_mismatch":
        mutated["evidence"]["integrity"]["statement_digest"] = "sha256:" + "f" * 64
    elif kind in {
        "invalid_label_transition",
        "stale_source_hash",
        "missing_failed_test",
        "wrong_count",
        "policy_threshold_violation",
    }:
        # Case-semantic variants remain core-profile valid. The case adapter reports them.
        mutated = with_recomputed_integrity(mutated)
    else:
        raise ValueError(f"unknown mutation kind: {kind}")
    return mutated


def schema_only(statement: dict[str, Any]) -> dict[str, Any]:
    schema = read_json(SCHEMA_PATH)
    validator = Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(statement), key=lambda item: list(item.path))
    issues = [
        {
            "path": ".".join(str(part) for part in error.path) or "root",
            "message": error.message,
        }
        for error in errors
    ]
    return {
        "baseline": "schema-only",
        "ok": not issues,
        "issues": issues,
        "capability_boundary": (
            "Structural JSON Schema validation only; no reference, policy/evidence, "
            "provenance/output, validation/provenance, digest, or case-semantic checks."
        ),
    }


def log_only(fixture: dict[str, Any]) -> dict[str, Any]:
    event_present = bool(fixture["operation_payload"]["log"].get("event_present", False))
    return {
        "baseline": "log-only",
        "ok": event_present,
        "event_present": event_present,
        "issues": [] if event_present else [{"code": "operation_event_missing"}],
        "capability_boundary": (
            "Checks whether the operation event is present in the fixture log. It does not "
            "prove policy/evidence linkage, provenance/output closure, or integrity."
        ),
    }


def policy_only(fixture: dict[str, Any]) -> dict[str, Any]:
    case_id = fixture["case_id"]
    payload = fixture["payloads"]
    policy = fixture["policy_payload"]
    issues: list[dict[str, str]] = []
    if case_id == "issue_pr_metadata":
        after_label = payload["output"]["label"]
        if after_label not in policy["allowed_labels"]:
            issues.append({"code": "invalid_label_transition"})
    elif case_id == "doc_data_transform":
        if policy.get("required_rule") != payload["output"].get("rule"):
            issues.append({"code": "missing_transform_rule"})
    elif case_id == "test_result_summary":
        if payload["output"]["summary"]["failed"] > policy["max_failed_tests"]:
            issues.append({"code": "policy_threshold_violation"})
    return {
        "baseline": "policy-only",
        "ok": not issues,
        "issues": issues,
        "capability_boundary": (
            "Checks only local policy rule fields. It does not prove evidence, provenance, "
            "output closure, validation closure, or digest consistency."
        ),
    }


def case_semantic_checks(fixture: dict[str, Any]) -> list[dict[str, str]]:
    case_id = fixture["case_id"]
    payload = fixture["payloads"]
    policy = fixture["policy_payload"]
    issues: list[dict[str, str]] = []
    if case_id == "issue_pr_metadata":
        after_label = payload["output"]["label"]
        if after_label not in policy["allowed_labels"]:
            issues.append(
                {
                    "stage": "case_semantics",
                    "code": "invalid_label_transition",
                    "path": "payloads.output.label",
                    "message": "output label is not allowed by the triage policy.",
                }
            )
    elif case_id == "doc_data_transform":
        expected_source_hash = sha256_digest(payload["input"])
        if payload["output"].get("source_digest") != expected_source_hash:
            issues.append(
                {
                    "stage": "case_semantics",
                    "code": "stale_source_digest",
                    "path": "payloads.output.source_digest",
                    "message": "output source digest does not match the current source artifact.",
                }
            )
    elif case_id == "test_result_summary":
        tests = payload["input"]["tests"]
        observed = {
            "passed": sum(1 for item in tests if item["outcome"] == "passed"),
            "failed": sum(1 for item in tests if item["outcome"] == "failed"),
            "skipped": sum(1 for item in tests if item["outcome"] == "skipped"),
        }
        summary = payload["output"]["summary"]
        for key, value in observed.items():
            if summary.get(key) != value:
                issues.append(
                    {
                        "stage": "case_semantics",
                        "code": "test_summary_count_mismatch",
                        "path": f"payloads.output.summary.{key}",
                        "message": f"summary {key} count does not match raw test result.",
                    }
                )
                break
        if summary.get("failed", 0) > policy["max_failed_tests"]:
            issues.append(
                {
                    "stage": "case_semantics",
                    "code": "policy_threshold_violation",
                    "path": "payloads.output.summary.failed",
                    "message": "summary violates the declared maximum failed-test threshold.",
                }
            )
    return issues


def run_fixture(fixture_path: Path, reports_dir: Path) -> dict[str, Any]:
    fixture = read_json(fixture_path)
    statement = build_statement(fixture)
    variant_id = fixture["variant_id"]
    reports_dir.mkdir(parents=True, exist_ok=True)
    statement_path = reports_dir / f"{variant_id}.statement.json"
    profile_report_path = reports_dir / f"{variant_id}.profile-aware.json"
    summary_path = reports_dir / f"{variant_id}.summary.md"
    write_json(statement_path, statement)

    core_report = validate_profile_file(statement_path)
    semantic_issues = [] if not core_report["ok"] else case_semantic_checks(fixture)
    overall_ok = core_report["ok"] and not semantic_issues
    primary_error_code = core_report["primary_error_code"]
    if core_report["ok"] and semantic_issues:
        primary_error_code = semantic_issues[0]["code"]

    schema_result = schema_only(statement)
    log_result = log_only(fixture)
    policy_result = policy_only(fixture)
    expected_code = fixture["expected_primary_error_code"]
    diagnostic_match = (
        fixture["expected_validity"] == overall_ok and expected_code == primary_error_code
    )

    report = {
        "case_id": fixture["case_id"],
        "case_name": fixture["case_name"],
        "variant_id": variant_id,
        "operation_type": fixture["operation_type"],
        "expected_validity": fixture["expected_validity"],
        "observed_validity": overall_ok,
        "expected_primary_error_code": expected_code,
        "observed_primary_error_code": primary_error_code,
        "diagnostic_match": diagnostic_match,
        "profile_aware_result": {
            "ok": overall_ok,
            "primary_error_code": primary_error_code,
            "core_profile_ok": core_report["ok"],
            "core_profile_primary_error_code": core_report["primary_error_code"],
            "case_semantic_issues": semantic_issues,
        },
        "core_profile_report": core_report,
        "baseline_results": {
            "schema_only": schema_result,
            "log_only": log_result,
            "policy_only": policy_result,
        },
        "privacy_classification": fixture["privacy_classification"],
        "source_type": fixture["source_type"],
        "interpretation": fixture["interpretation"],
    }
    write_json(profile_report_path, report)
    write_text(summary_path, render_variant_summary(report))
    return report


def render_variant_summary(report: dict[str, Any]) -> str:
    baselines = report["baseline_results"]
    return "\n".join(
        [
            f"# {report['case_id']} / {report['variant_id']}",
            "",
            f"- expected validity: `{report['expected_validity']}`",
            f"- observed validity: `{report['observed_validity']}`",
            f"- expected primary code: `{report['expected_primary_error_code']}`",
            f"- observed primary code: `{report['observed_primary_error_code']}`",
            f"- diagnostic match: `{report['diagnostic_match']}`",
            f"- schema-only ok: `{baselines['schema_only']['ok']}`",
            f"- log-only ok: `{baselines['log_only']['ok']}`",
            f"- policy-only ok: `{baselines['policy_only']['ok']}`",
            "",
            report["interpretation"],
            "",
        ]
    )


def run_case(case_slug: str) -> list[dict[str, Any]]:
    case_dir = CASES_ROOT / case_slug
    reports_dir = case_dir / "reports"
    fixtures = sorted((case_dir / "fixtures" / "valid").glob("*.json")) + sorted(
        (case_dir / "fixtures" / "invalid").glob("*.json")
    )
    if not fixtures:
        raise FileNotFoundError(f"no fixtures found for {case_slug}")
    reports = [run_fixture(path, reports_dir) for path in fixtures]
    write_json(case_dir / "expected" / "latest_case_results.json", reports)
    write_text(case_dir / "reports" / "case_summary.md", render_case_summary(case_slug, reports))
    if not all(report["diagnostic_match"] for report in reports):
        raise SystemExit(f"{case_slug}: one or more fixtures did not match expectations")
    return reports


def render_case_summary(case_slug: str, reports: list[dict[str, Any]]) -> str:
    lines = [f"# {CASES[case_slug].name}", ""]
    lines.append("| Variant | Expected | Observed | Primary code | Match |")
    lines.append("|---|---|---|---|---|")
    for report in reports:
        lines.append(
            "| {variant} | {expected} | {observed} | {code} | {match} |".format(
                variant=report["variant_id"],
                expected=report["expected_validity"],
                observed=report["observed_validity"],
                code=report["observed_primary_error_code"],
                match=report["diagnostic_match"],
            )
        )
    lines.append("")
    return "\n".join(lines)


def run_all_cases() -> list[dict[str, Any]]:
    all_reports: list[dict[str, Any]] = []
    for case_slug in ("issue_pr_metadata", "doc_data_transform", "test_result_summary"):
        all_reports.extend(run_case(case_slug))
    REPORTS_ROOT.mkdir(parents=True, exist_ok=True)
    write_json(REPORTS_ROOT / "se_case_matrix.json", all_reports)
    write_text(REPORTS_ROOT / "se_case_matrix.md", render_matrix(all_reports))
    write_json(REPORTS_ROOT / "baseline_comparison.json", build_baseline_comparison(all_reports))
    write_text(
        REPORTS_ROOT / "baseline_comparison.md",
        render_baseline_comparison(build_baseline_comparison(all_reports)),
    )
    write_json(REPORTS_ROOT / "failure_code_coverage.json", build_failure_coverage(all_reports))
    write_text(
        REPORTS_ROOT / "failure_code_coverage.md",
        render_failure_coverage(build_failure_coverage(all_reports)),
    )
    return all_reports


def render_matrix(reports: list[dict[str, Any]]) -> str:
    lines = [
        "# SE Case Matrix",
        "",
        "| Case | Variant | Expected | Profile-aware | Primary code | Schema-only | Log-only | Policy-only | Match |",
        "|---|---|---|---|---|---|---|---|---|",
    ]
    for report in reports:
        baselines = report["baseline_results"]
        lines.append(
            "| {case} | {variant} | {expected} | {observed} | {code} | {schema} | {log} | {policy} | {match} |".format(
                case=report["case_id"],
                variant=report["variant_id"],
                expected=report["expected_validity"],
                observed=report["observed_validity"],
                code=report["observed_primary_error_code"],
                schema=baselines["schema_only"]["ok"],
                log=baselines["log_only"]["ok"],
                policy=baselines["policy_only"]["ok"],
                match=report["diagnostic_match"],
            )
        )
    lines.append("")
    lines.append(
        "These are representative reproducible SE workflow fixtures, not industrial real-world cases."
    )
    lines.append("")
    return "\n".join(lines)


def build_baseline_comparison(reports: list[dict[str, Any]]) -> list[dict[str, Any]]:
    invalid_reports = [report for report in reports if not report["expected_validity"]]
    return [
        {
            "baseline": "schema-only",
            "detects": "JSON structural violations.",
            "misses": "Relation, policy/evidence, provenance/output, validation/provenance, digest, and case-semantic failures.",
            "missed_invalid_count": sum(
                1 for report in invalid_reports if report["baseline_results"]["schema_only"]["ok"]
            ),
            "safe_claim": "Schema-only validation is insufficient for relation-level operation-accountability review.",
        },
        {
            "baseline": "log-only",
            "detects": "Presence of a fixture operation event.",
            "misses": "Policy/evidence linkage, output/provenance closure, validation closure, and integrity.",
            "missed_invalid_count": sum(
                1 for report in invalid_reports if report["baseline_results"]["log_only"]["ok"]
            ),
            "safe_claim": "Logs are useful event evidence but do not close the accountability boundary.",
        },
        {
            "baseline": "policy-only",
            "detects": "Local policy rule mismatches represented in the policy file.",
            "misses": "Evidence, provenance, output closure, and digest failures.",
            "missed_invalid_count": sum(
                1 for report in invalid_reports if report["baseline_results"]["policy_only"]["ok"]
            ),
            "safe_claim": "Policy-only review is partial and does not prove operation evidence closure.",
        },
    ]


def render_baseline_comparison(rows: list[dict[str, Any]]) -> str:
    lines = [
        "# Baseline Comparison",
        "",
        "| Baseline | Detects | Misses | Missed invalid variants | Safe claim |",
        "|---|---|---|---|---|",
    ]
    for row in rows:
        lines.append(
            f"| {row['baseline']} | {row['detects']} | {row['misses']} | {row['missed_invalid_count']} | {row['safe_claim']} |"
        )
    lines.append("")
    return "\n".join(lines)


def build_failure_coverage(reports: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows = []
    for report in reports:
        code = report["observed_primary_error_code"]
        if code is None:
            continue
        rows.append(
            {
                "diagnostic_code": code,
                "case_id": report["case_id"],
                "variant_id": report["variant_id"],
                "expected": report["expected_primary_error_code"],
                "observed": code,
                "coverage_status": "covered" if report["diagnostic_match"] else "mismatch",
            }
        )
    return rows


def render_failure_coverage(rows: list[dict[str, Any]]) -> str:
    lines = [
        "# Failure Code Coverage",
        "",
        "| Diagnostic code | Case | Variant | Expected | Observed | Coverage |",
        "|---|---|---|---|---|---|",
    ]
    for row in rows:
        lines.append(
            f"| {row['diagnostic_code']} | {row['case_id']} | {row['variant_id']} | {row['expected']} | {row['observed']} | {row['coverage_status']} |"
        )
    lines.append("")
    return "\n".join(lines)


def base_ids(case_id: str) -> dict[str, str]:
    return {
        "actor": f"actor:{case_id}:runner",
        "subject": f"obj:{case_id}:subject",
        "output": f"obj:{case_id}:output",
        "operation": f"op:{case_id}",
        "policy": f"policy:{case_id}",
        "provenance": f"prov:{case_id}",
        "evidence": f"evidence:{case_id}",
        "validation": f"validation:{case_id}",
    }


def fixture(
    *,
    case_id: str,
    variant_id: str,
    case_name: str,
    operation_type: str,
    actor_name: str,
    subject_type: str,
    input_payload: dict[str, Any],
    output_payload: dict[str, Any],
    policy_payload: dict[str, Any],
    log_payload: dict[str, Any],
    evidence_payload: dict[str, Any],
    expected_validity: bool,
    expected_primary_error_code: str | None,
    interpretation: str,
    mutation: dict[str, Any] | None = None,
) -> dict[str, Any]:
    return {
        "case_id": case_id,
        "case_name": case_name,
        "variant_id": variant_id,
        "operation_id": f"op:{case_id}:{variant_id}",
        "ids": base_ids(f"{case_id}:{variant_id}"),
        "actor": {"name": actor_name},
        "subject": {"type": subject_type},
        "operation_type": operation_type,
        "input_refs": ["ref:input"],
        "output_refs": ["ref:output"],
        "policy_refs": ["policy:case"],
        "evidence_refs": ["artifact:operation-log", "artifact:policy", "artifact:evidence"],
        "provenance_refs": ["prov:case"],
        "validation_refs": ["validation:case"],
        "integrity_refs": ["evidence.integrity"],
        "expected_validity": expected_validity,
        "expected_primary_error_code": expected_primary_error_code,
        "baseline_expectations": {
            "schema_only": "structural only",
            "log_only": "event presence only",
            "policy_only": "local policy fields only",
        },
        "privacy_classification": "generated-public-style-fixture",
        "source_type": "representative reproducible SE workflow fixture",
        "reproducibility_notes": "Generated locally; no private, clinical, customer, or scraped issue data.",
        "operation_payload": {
            "summary": case_name,
            "log": log_payload,
        },
        "policy_payload": policy_payload,
        "evidence_payload": evidence_payload,
        "provenance_payload": {
            "relation": "derived_from",
            "input_ref": "ref:input",
            "output_ref": "ref:output",
        },
        "payloads": {
            "input": input_payload,
            "output": output_payload,
        },
        "mutation": mutation,
        "interpretation": interpretation,
    }


def build_fixture_catalog() -> dict[str, list[dict[str, Any]]]:
    issue_before = {"issue_id": "ISSUE-101", "label": "needs-triage", "state": "open"}
    issue_after_valid = {"issue_id": "ISSUE-101", "label": "bug", "state": "open"}
    issue_policy = {
        "name": "repository-triage-policy",
        "description": "Only allowed triage labels may be applied to the issue fixture.",
        "allowed_labels": ["bug", "documentation", "enhancement"],
    }
    issue_log = {"event_present": True, "event": "issue.label.update", "issue_id": "ISSUE-101"}

    doc_source = {"doc_id": "DOC-7", "title": "Release notes", "body": "Feature A fixed."}
    doc_policy = {
        "name": "documentation-metadata-policy",
        "description": "Generated metadata must be derived from the current source document.",
        "required_rule": "extract-title-and-digest",
    }
    doc_output_valid = {
        "doc_id": "DOC-7",
        "title": "Release notes",
        "rule": "extract-title-and-digest",
        "source_digest": sha256_digest(doc_source),
    }
    doc_log = {"event_present": True, "event": "doc.metadata.generate", "doc_id": "DOC-7"}

    test_input = {
        "run_id": "RUN-12",
        "tests": [
            {"name": "test_schema", "outcome": "passed"},
            {"name": "test_references", "outcome": "passed"},
            {"name": "test_policy_gate", "outcome": "failed"},
            {"name": "test_report", "outcome": "skipped"},
        ],
    }
    test_policy = {
        "name": "test-summary-policy",
        "description": "Test summary must match the raw test result and release gate threshold.",
        "max_failed_tests": 1,
    }
    test_output_valid = {
        "run_id": "RUN-12",
        "summary": {"passed": 2, "failed": 1, "skipped": 1},
    }
    test_log = {"event_present": True, "event": "test.summary.generate", "run_id": "RUN-12"}

    return {
        "issue_pr_metadata": [
            fixture(
                case_id="issue_pr_metadata",
                variant_id="valid_label_update",
                case_name="Valid issue metadata update under triage policy",
                operation_type=CASES["issue_pr_metadata"].operation_type,
                actor_name="repo-triage-bot",
                subject_type="repository-issue",
                input_payload=issue_before,
                output_payload=issue_after_valid,
                policy_payload=issue_policy,
                log_payload=issue_log,
                evidence_payload={"change": "label needs-triage -> bug"},
                expected_validity=True,
                expected_primary_error_code=None,
                interpretation="Valid metadata update closes policy, input, output, evidence, and provenance refs.",
            ),
            fixture(
                case_id="issue_pr_metadata",
                variant_id="missing_policy_ref",
                case_name="Issue update with missing evidence policy reference",
                operation_type=CASES["issue_pr_metadata"].operation_type,
                actor_name="repo-triage-bot",
                subject_type="repository-issue",
                input_payload=issue_before,
                output_payload=issue_after_valid,
                policy_payload=issue_policy,
                log_payload=issue_log,
                evidence_payload={"change": "label needs-triage -> bug"},
                expected_validity=False,
                expected_primary_error_code="unresolved_evidence_policy_ref",
                mutation={"kind": "missing_policy_ref"},
                interpretation="Schema/log baselines can pass while profile-aware policy/evidence linkage fails.",
            ),
            fixture(
                case_id="issue_pr_metadata",
                variant_id="invalid_label_transition",
                case_name="Issue update with disallowed label transition",
                operation_type=CASES["issue_pr_metadata"].operation_type,
                actor_name="repo-triage-bot",
                subject_type="repository-issue",
                input_payload=issue_before,
                output_payload={
                    "issue_id": "ISSUE-101",
                    "label": "security-critical",
                    "state": "open",
                },
                policy_payload=issue_policy,
                log_payload=issue_log,
                evidence_payload={"change": "label needs-triage -> security-critical"},
                expected_validity=False,
                expected_primary_error_code="invalid_label_transition",
                mutation={"kind": "invalid_label_transition"},
                interpretation="Core profile structure passes, but the case adapter catches a policy-rule violation.",
            ),
            fixture(
                case_id="issue_pr_metadata",
                variant_id="unresolved_issue_input_ref",
                case_name="Issue update with unresolved input reference",
                operation_type=CASES["issue_pr_metadata"].operation_type,
                actor_name="repo-triage-bot",
                subject_type="repository-issue",
                input_payload=issue_before,
                output_payload=issue_after_valid,
                policy_payload=issue_policy,
                log_payload=issue_log,
                evidence_payload={"change": "label needs-triage -> bug"},
                expected_validity=False,
                expected_primary_error_code="unresolved_input_ref",
                mutation={"kind": "unresolved_input_ref"},
                interpretation="Schema/log baselines pass while local reference closure fails.",
            ),
            fixture(
                case_id="issue_pr_metadata",
                variant_id="provenance_output_mismatch",
                case_name="Issue update with provenance/output mismatch",
                operation_type=CASES["issue_pr_metadata"].operation_type,
                actor_name="repo-triage-bot",
                subject_type="repository-issue",
                input_payload=issue_before,
                output_payload=issue_after_valid,
                policy_payload=issue_policy,
                log_payload=issue_log,
                evidence_payload={"change": "label needs-triage -> bug"},
                expected_validity=False,
                expected_primary_error_code="provenance_output_refs_mismatch",
                mutation={"kind": "provenance_output_mismatch"},
                interpretation="Broken provenance output cannot close over the declared output reference.",
            ),
            fixture(
                case_id="issue_pr_metadata",
                variant_id="validation_provenance_missing",
                case_name="Issue update with missing validation/provenance link",
                operation_type=CASES["issue_pr_metadata"].operation_type,
                actor_name="repo-triage-bot",
                subject_type="repository-issue",
                input_payload=issue_before,
                output_payload=issue_after_valid,
                policy_payload=issue_policy,
                log_payload=issue_log,
                evidence_payload={"change": "label needs-triage -> bug"},
                expected_validity=False,
                expected_primary_error_code="unresolved_validation_provenance_ref",
                mutation={"kind": "validation_provenance_missing"},
                interpretation="The validation path no longer closes over the provenance material.",
            ),
        ],
        "doc_data_transform": [
            fixture(
                case_id="doc_data_transform",
                variant_id="valid_doc_metadata",
                case_name="Valid documentation metadata generation",
                operation_type=CASES["doc_data_transform"].operation_type,
                actor_name="doc-metadata-generator",
                subject_type="source-document",
                input_payload=doc_source,
                output_payload=doc_output_valid,
                policy_payload=doc_policy,
                log_payload=doc_log,
                evidence_payload={"transform": "extract title and source digest"},
                expected_validity=True,
                expected_primary_error_code=None,
                interpretation="Valid transformation links source, rule, generated metadata, provenance, and digest.",
            ),
            fixture(
                case_id="doc_data_transform",
                variant_id="stale_source_hash",
                case_name="Documentation metadata generated from stale source digest",
                operation_type=CASES["doc_data_transform"].operation_type,
                actor_name="doc-metadata-generator",
                subject_type="source-document",
                input_payload=doc_source,
                output_payload={**doc_output_valid, "source_digest": "sha256:" + "1" * 64},
                policy_payload=doc_policy,
                log_payload=doc_log,
                evidence_payload={"transform": "extract title and stale source digest"},
                expected_validity=False,
                expected_primary_error_code="stale_source_digest",
                mutation={"kind": "stale_source_hash"},
                interpretation="Core profile structure passes, but case semantics catch stale source binding.",
            ),
            fixture(
                case_id="doc_data_transform",
                variant_id="wrong_derived_output_ref",
                case_name="Documentation metadata with wrong derived output reference",
                operation_type=CASES["doc_data_transform"].operation_type,
                actor_name="doc-metadata-generator",
                subject_type="source-document",
                input_payload=doc_source,
                output_payload=doc_output_valid,
                policy_payload=doc_policy,
                log_payload=doc_log,
                evidence_payload={"transform": "extract title and source digest"},
                expected_validity=False,
                expected_primary_error_code="provenance_output_refs_mismatch",
                mutation={"kind": "wrong_derived_output_ref"},
                interpretation="Output derivation cannot be reviewed because provenance names an unresolved output.",
            ),
            fixture(
                case_id="doc_data_transform",
                variant_id="missing_policy_link",
                case_name="Documentation metadata with missing policy link",
                operation_type=CASES["doc_data_transform"].operation_type,
                actor_name="doc-metadata-generator",
                subject_type="source-document",
                input_payload=doc_source,
                output_payload=doc_output_valid,
                policy_payload=doc_policy,
                log_payload=doc_log,
                evidence_payload={"transform": "extract title and source digest"},
                expected_validity=False,
                expected_primary_error_code="unresolved_evidence_policy_ref",
                mutation={"kind": "missing_policy_link"},
                interpretation="Evidence no longer links to the declared transformation policy.",
            ),
            fixture(
                case_id="doc_data_transform",
                variant_id="provenance_mismatch",
                case_name="Documentation metadata with provenance mismatch",
                operation_type=CASES["doc_data_transform"].operation_type,
                actor_name="doc-metadata-generator",
                subject_type="source-document",
                input_payload=doc_source,
                output_payload=doc_output_valid,
                policy_payload=doc_policy,
                log_payload=doc_log,
                evidence_payload={"transform": "extract title and source digest"},
                expected_validity=False,
                expected_primary_error_code="provenance_output_refs_mismatch",
                mutation={"kind": "provenance_output_mismatch"},
                interpretation="Provenance points away from the declared generated output.",
            ),
            fixture(
                case_id="doc_data_transform",
                variant_id="digest_mismatch",
                case_name="Documentation metadata with digest mismatch",
                operation_type=CASES["doc_data_transform"].operation_type,
                actor_name="doc-metadata-generator",
                subject_type="source-document",
                input_payload=doc_source,
                output_payload=doc_output_valid,
                policy_payload=doc_policy,
                log_payload=doc_log,
                evidence_payload={"transform": "extract title and source digest"},
                expected_validity=False,
                expected_primary_error_code="statement_digest_mismatch",
                mutation={"kind": "digest_mismatch"},
                interpretation="Integrity stage detects mutation after the statement was constructed.",
            ),
        ],
        "test_result_summary": [
            fixture(
                case_id="test_result_summary",
                variant_id="valid_test_summary",
                case_name="Valid test-result summarization",
                operation_type=CASES["test_result_summary"].operation_type,
                actor_name="test-summary-generator",
                subject_type="test-run",
                input_payload=test_input,
                output_payload=test_output_valid,
                policy_payload=test_policy,
                log_payload=test_log,
                evidence_payload={"summary": "2 passed, 1 failed, 1 skipped"},
                expected_validity=True,
                expected_primary_error_code=None,
                interpretation="Valid test summary matches raw test counts and threshold policy.",
            ),
            fixture(
                case_id="test_result_summary",
                variant_id="missing_failed_test",
                case_name="Test summary omits a failed test",
                operation_type=CASES["test_result_summary"].operation_type,
                actor_name="test-summary-generator",
                subject_type="test-run",
                input_payload=test_input,
                output_payload={
                    "run_id": "RUN-12",
                    "summary": {"passed": 3, "failed": 0, "skipped": 1},
                },
                policy_payload=test_policy,
                log_payload=test_log,
                evidence_payload={"summary": "3 passed, 0 failed, 1 skipped"},
                expected_validity=False,
                expected_primary_error_code="test_summary_count_mismatch",
                mutation={"kind": "missing_failed_test"},
                interpretation="Schema/log baselines can pass while case semantics catch omitted failure.",
            ),
            fixture(
                case_id="test_result_summary",
                variant_id="wrong_count",
                case_name="Test summary has wrong count",
                operation_type=CASES["test_result_summary"].operation_type,
                actor_name="test-summary-generator",
                subject_type="test-run",
                input_payload=test_input,
                output_payload={
                    "run_id": "RUN-12",
                    "summary": {"passed": 2, "failed": 1, "skipped": 0},
                },
                policy_payload=test_policy,
                log_payload=test_log,
                evidence_payload={"summary": "2 passed, 1 failed, 0 skipped"},
                expected_validity=False,
                expected_primary_error_code="test_summary_count_mismatch",
                mutation={"kind": "wrong_count"},
                interpretation="Count mismatch is outside plain JSON shape and requires case semantics.",
            ),
            fixture(
                case_id="test_result_summary",
                variant_id="unresolved_test_artifact_ref",
                case_name="Test summary with unresolved test artifact reference",
                operation_type=CASES["test_result_summary"].operation_type,
                actor_name="test-summary-generator",
                subject_type="test-run",
                input_payload=test_input,
                output_payload=test_output_valid,
                policy_payload=test_policy,
                log_payload=test_log,
                evidence_payload={"summary": "2 passed, 1 failed, 1 skipped"},
                expected_validity=False,
                expected_primary_error_code="unresolved_input_ref",
                mutation={"kind": "unresolved_input_ref"},
                interpretation="The summary statement cannot resolve its raw test-result input.",
            ),
            fixture(
                case_id="test_result_summary",
                variant_id="policy_threshold_violation",
                case_name="Test summary violates failed-test threshold",
                operation_type=CASES["test_result_summary"].operation_type,
                actor_name="test-summary-generator",
                subject_type="test-run",
                input_payload=test_input,
                output_payload={
                    "run_id": "RUN-12",
                    "summary": {"passed": 1, "failed": 2, "skipped": 1},
                },
                policy_payload=test_policy,
                log_payload=test_log,
                evidence_payload={"summary": "1 passed, 2 failed, 1 skipped"},
                expected_validity=False,
                expected_primary_error_code="test_summary_count_mismatch",
                mutation={"kind": "policy_threshold_violation"},
                interpretation="Case semantics first catch the inconsistent raw-summary count before threshold interpretation.",
            ),
            fixture(
                case_id="test_result_summary",
                variant_id="digest_mismatch",
                case_name="Test summary with digest mismatch",
                operation_type=CASES["test_result_summary"].operation_type,
                actor_name="test-summary-generator",
                subject_type="test-run",
                input_payload=test_input,
                output_payload=test_output_valid,
                policy_payload=test_policy,
                log_payload=test_log,
                evidence_payload={"summary": "2 passed, 1 failed, 1 skipped"},
                expected_validity=False,
                expected_primary_error_code="statement_digest_mismatch",
                mutation={"kind": "digest_mismatch"},
                interpretation="Integrity stage detects tampering in the generated statement digest.",
            ),
        ],
    }


def bootstrap_fixtures() -> None:
    catalog = build_fixture_catalog()
    for case_slug, fixtures in catalog.items():
        case_dir = CASES_ROOT / case_slug
        for subdir in ("fixtures/valid", "fixtures/invalid", "expected", "reports"):
            (case_dir / subdir).mkdir(parents=True, exist_ok=True)
        write_text(case_dir / "README.md", render_case_readme(case_slug))
        for item in fixtures:
            bucket = "valid" if item["expected_validity"] else "invalid"
            write_json(case_dir / "fixtures" / bucket / f"{item['variant_id']}.json", item)
    write_reproducibility_files()


def render_case_readme(case_slug: str) -> str:
    info = CASES[case_slug]
    return "\n".join(
        [
            f"# {info.name}",
            "",
            "This directory contains representative reproducible SE workflow fixtures.",
            "It contains no private, clinical, customer, or scraped issue data.",
            "",
            f"Run with `python scripts/{info.runner_name} --all` from the repository root.",
            "",
        ]
    )


def write_reproducibility_files() -> None:
    write_text(
        ROOT / "README_SE_CASES.md",
        "\n".join(
            [
                "# Representative SE Workflow Cases",
                "",
                "This package implements representative reproducible SE workflow fixtures for operation-accountability validation.",
                "",
                "Implemented cases:",
                "",
                "- issue / PR metadata operation;",
                "- documentation / data transformation operation;",
                "- test-result summarization operation.",
                "",
                "These are not industrial real-world cases. They are local public-style fixtures with no private, clinical, customer, or scraped issue data.",
                "",
            ]
        ),
    )
    write_text(
        ROOT / "RUN_COMMANDS.md",
        "\n".join(
            [
                "# Run Commands",
                "",
                "```bash",
                "python scripts/run_case_issue_pr_metadata.py --all",
                "python scripts/run_case_doc_data_transform.py --all",
                "python scripts/run_case_test_result_summary.py --all",
                "python scripts/run_all_se_cases.py",
                "```",
                "",
            ]
        ),
    )
    write_text(
        ROOT / "EXPECTED_RESULTS.md",
        "\n".join(
            [
                "# Expected Results",
                "",
                "All valid variants must pass. All invalid variants must fail with their expected primary diagnostic code.",
                "",
                "The cross-case matrix is written to `reports/se_case_matrix.md` and `reports/se_case_matrix.json`.",
                "",
            ]
        ),
    )
    write_text(
        ROOT / "CASE_MANIFEST.md",
        "\n".join(
            [
                "# Case Manifest",
                "",
                "| Case | Runner | Fixture directory |",
                "|---|---|---|",
                "| issue_pr_metadata | `scripts/run_case_issue_pr_metadata.py` | `cases/se_workflows/issue_pr_metadata/` |",
                "| doc_data_transform | `scripts/run_case_doc_data_transform.py` | `cases/se_workflows/doc_data_transform/` |",
                "| test_result_summary | `scripts/run_case_test_result_summary.py` | `cases/se_workflows/test_result_summary/` |",
                "",
            ]
        ),
    )


def compute_checksums() -> None:
    paths = []
    for rel_root in (
        "cases/se_workflows",
        "reports",
        "scripts",
        "baselines",
        "docs/validator_semantics.md",
        "docs/formal_model_alignment.md",
        "docs/case_protocol.md",
        "README_SE_CASES.md",
        "RUN_COMMANDS.md",
        "EXPECTED_RESULTS.md",
        "CASE_MANIFEST.md",
    ):
        path = ROOT / rel_root
        if path.is_file():
            paths.append(path)
        elif path.is_dir():
            paths.extend(sorted(item for item in path.rglob("*") if item.is_file()))
    lines = []
    for path in sorted(set(paths)):
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        lines.append(f"{digest}  {path.relative_to(ROOT)}")
    write_text(ROOT / "CHECKSUMS.sha256", "\n".join(lines) + "\n")


def run_command(args: list[str]) -> int:
    result = subprocess.run(args, cwd=ROOT, text=True)
    return int(result.returncode)


def main_case_runner(case_slug: str) -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--all", action="store_true", help="Run all fixtures for this case.")
    parser.add_argument("--bootstrap-fixtures", action="store_true")
    args = parser.parse_args()
    if args.bootstrap_fixtures:
        bootstrap_fixtures()
    if args.all:
        run_case(case_slug)
    compute_checksums()


def main_all_cases() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--bootstrap-fixtures", action="store_true")
    args = parser.parse_args()
    if args.bootstrap_fixtures:
        bootstrap_fixtures()
    run_all_cases()
    compute_checksums()


if __name__ == "__main__":
    main_all_cases()
