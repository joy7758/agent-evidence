# ruff: noqa: E501,I001

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_se_workflow_case_runner_generates_expected_matrix() -> None:
    result = subprocess.run(
        [sys.executable, "scripts/run_all_se_cases.py", "--bootstrap-fixtures"],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )

    assert result.returncode == 0, result.stderr + result.stdout
    matrix_path = ROOT / "reports" / "se_case_matrix.json"
    assert matrix_path.exists()
    matrix = json.loads(matrix_path.read_text(encoding="utf-8"))
    assert len(matrix) == 18
    assert all(row["diagnostic_match"] for row in matrix)
    assert {row["case_id"] for row in matrix} == {
        "issue_pr_metadata",
        "doc_data_transform",
        "test_result_summary",
    }


def test_schema_only_misses_relation_or_semantic_invalid_variants() -> None:
    matrix = json.loads((ROOT / "reports" / "se_case_matrix.json").read_text(encoding="utf-8"))
    invalid_rows = [row for row in matrix if not row["expected_validity"]]
    missed_by_schema = [row for row in invalid_rows if row["baseline_results"]["schema_only"]["ok"]]

    assert len(missed_by_schema) >= 10
    assert any(row["observed_primary_error_code"] == "invalid_label_transition" for row in matrix)
    assert any(
        row["observed_primary_error_code"] == "test_summary_count_mismatch" for row in matrix
    )
