# ruff: noqa: E501,I001

from __future__ import annotations

from functools import lru_cache
import json
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / "reports"

CASE_EXPECTATIONS = [
    ("issue_pr_metadata", 1, 5),
    ("doc_data_transform", 1, 5),
    ("test_result_summary", 1, 5),
]

BASELINE_EXPECTATIONS = [
    ("schema-only", 15),
    ("log-only", 15),
    ("policy-only", 13),
]

INVALID_VARIANT_EXPECTATIONS = [
    ("issue_pr_metadata", "invalid_label_transition", "invalid_label_transition"),
    ("issue_pr_metadata", "missing_policy_ref", "unresolved_evidence_policy_ref"),
    (
        "issue_pr_metadata",
        "provenance_output_mismatch",
        "provenance_output_refs_mismatch",
    ),
    ("issue_pr_metadata", "unresolved_issue_input_ref", "unresolved_input_ref"),
    (
        "issue_pr_metadata",
        "validation_provenance_missing",
        "unresolved_validation_provenance_ref",
    ),
    ("doc_data_transform", "digest_mismatch", "statement_digest_mismatch"),
    ("doc_data_transform", "missing_policy_link", "unresolved_evidence_policy_ref"),
    ("doc_data_transform", "provenance_mismatch", "provenance_output_refs_mismatch"),
    ("doc_data_transform", "stale_source_hash", "stale_source_digest"),
    ("doc_data_transform", "wrong_derived_output_ref", "provenance_output_refs_mismatch"),
    ("test_result_summary", "digest_mismatch", "statement_digest_mismatch"),
    ("test_result_summary", "missing_failed_test", "test_summary_count_mismatch"),
    ("test_result_summary", "policy_threshold_violation", "test_summary_count_mismatch"),
    ("test_result_summary", "unresolved_test_artifact_ref", "unresolved_input_ref"),
    ("test_result_summary", "wrong_count", "test_summary_count_mismatch"),
]

TOP_LEVEL_RELEASE_DOCS = [
    "CLAIM_BOUNDARY.md",
    "ENVIRONMENT.md",
    "REPRODUCIBILITY.md",
    "ARCHIVE_NOTES.md",
    "AI_DISCLOSURE.md",
]


@lru_cache(maxsize=1)
def _run_all_cases() -> list[dict[str, object]]:
    result = subprocess.run(
        [sys.executable, "scripts/run_all_se_cases.py", "--bootstrap-fixtures"],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )

    assert result.returncode == 0, result.stderr + result.stdout
    matrix_path = REPORTS / "se_case_matrix.json"
    assert matrix_path.exists()
    return json.loads(matrix_path.read_text(encoding="utf-8"))


def _baseline_summary() -> list[dict[str, object]]:
    path = REPORTS / "baseline_comparison.json"
    assert path.exists()
    return json.loads(path.read_text(encoding="utf-8"))


def test_se_workflow_case_runner_generates_expected_matrix() -> None:
    matrix = _run_all_cases()
    assert len(matrix) == 18
    assert all(row["diagnostic_match"] for row in matrix)
    assert {row["case_id"] for row in matrix} == {
        "issue_pr_metadata",
        "doc_data_transform",
        "test_result_summary",
    }


@pytest.mark.parametrize(("case_id", "valid_count", "invalid_count"), CASE_EXPECTATIONS)
def test_case_distribution(case_id: str, valid_count: int, invalid_count: int) -> None:
    rows = [row for row in _run_all_cases() if row["case_id"] == case_id]
    assert len([row for row in rows if row["expected_validity"]]) == valid_count
    assert len([row for row in rows if not row["expected_validity"]]) == invalid_count


@pytest.mark.parametrize(("baseline", "missed_count"), BASELINE_EXPECTATIONS)
def test_baseline_missed_invalid_counts(baseline: str, missed_count: int) -> None:
    summaries = {row["baseline"]: row for row in _baseline_summary()}
    assert summaries[baseline]["missed_invalid_count"] == missed_count


@pytest.mark.parametrize(
    ("case_id", "variant_id", "expected_code"),
    INVALID_VARIANT_EXPECTATIONS,
)
def test_invalid_variant_diagnostic_code(
    case_id: str,
    variant_id: str,
    expected_code: str,
) -> None:
    matches = [
        row
        for row in _run_all_cases()
        if row["case_id"] == case_id and row["variant_id"] == variant_id
    ]
    assert len(matches) == 1
    row = matches[0]
    assert row["diagnostic_match"] is True
    assert row["observed_primary_error_code"] == expected_code


@pytest.mark.parametrize("doc_name", TOP_LEVEL_RELEASE_DOCS)
def test_top_level_release_document_exists(doc_name: str) -> None:
    path = ROOT / doc_name
    assert path.exists()
    assert path.read_text(encoding="utf-8").strip()


def test_release_docs_do_not_claim_forbidden_scope() -> None:
    combined = "\n".join(
        (ROOT / doc_name).read_text(encoding="utf-8") for doc_name in TOP_LEVEL_RELEASE_DOCS
    ).lower()
    assert "tse v3 ready" in combined
    assert "industrial real-world evaluation" in combined
    assert "production deployment" in combined
    assert "benchmark superiority" in combined
    assert "legal or compliance sufficiency" in combined
    assert "no private" in (ROOT / "README_SE_CASES.md").read_text(encoding="utf-8").lower()
