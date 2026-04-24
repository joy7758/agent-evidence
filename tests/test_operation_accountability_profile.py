import copy
import json
from pathlib import Path

import pytest
from click.testing import CliRunner

from agent_evidence.cli.main import main
from agent_evidence.oap import build_validation_report, load_profile, validate_profile_file

EXAMPLES = Path(__file__).resolve().parents[1] / "examples"


@pytest.mark.parametrize(
    "filename",
    [
        "minimal-valid-evidence.json",
        "valid-retention-review-evidence.json",
        "valid-high-risk-payment-review-evidence.json",
    ],
)
def test_valid_operation_accountability_profile_passes(filename: str) -> None:
    report = validate_profile_file(EXAMPLES / filename)

    assert report["ok"] is True
    assert report["issue_count"] == 0


@pytest.mark.parametrize(
    ("filename", "expected_code", "expected_issue_count"),
    [
        ("invalid-missing-required.json", "schema_violation", 1),
        ("invalid-unclosed-reference.json", "unresolved_output_ref", 1),
        ("invalid-policy-link-broken.json", "unresolved_evidence_policy_ref", 1),
        ("invalid-provenance-output-mismatch.json", "provenance_output_refs_mismatch", 1),
        (
            "invalid-validation-provenance-link-broken.json",
            "unresolved_validation_provenance_ref",
            1,
        ),
        ("invalid-high-risk-unclosed-reference.json", "unresolved_output_ref", 1),
        (
            "invalid-high-risk-policy-link-broken.json",
            "unresolved_evidence_policy_ref",
            1,
        ),
    ],
)
def test_invalid_operation_accountability_profiles_fail(
    filename: str, expected_code: str, expected_issue_count: int
) -> None:
    report = validate_profile_file(EXAMPLES / filename)

    assert report["ok"] is False
    assert report["issue_count"] == expected_issue_count
    assert report["primary_error_code"] == expected_code
    assert report["issues"]
    assert report["issue_summary"]["by_code"][expected_code] >= 1
    issue_codes = {issue["code"] for stage in report["stages"] for issue in stage["issues"]}
    assert expected_code in issue_codes


def test_validation_report_exposes_flattened_issues_and_summary_counts() -> None:
    report = validate_profile_file(EXAMPLES / "invalid-unclosed-reference.json")

    assert report["ok"] is False
    assert report["fail_fast"] is True
    assert report["issues"] == [issue for stage in report["stages"] for issue in stage["issues"]]
    assert report["primary_error_code"] == "unresolved_output_ref"
    assert report["issue_summary"] == {
        "by_stage": {"references": 1},
        "by_code": {"unresolved_output_ref": 1},
    }
    assert "Stages with issues: references=1" in report["summary"]


def test_validation_fail_fast_stops_after_first_failed_semantic_stage() -> None:
    profile = load_profile(EXAMPLES / "minimal-valid-evidence.json")
    profile["operation"]["output_refs"] = ["missing-output"]
    profile["evidence"]["integrity"]["statement_digest"] = "sha256:" + "0" * 64

    report = build_validation_report(profile, fail_fast=True)

    assert report["issue_count"] == 1
    assert report["primary_error_code"] == "unresolved_output_ref"
    skipped = {stage["name"]: stage["skipped"] for stage in report["stages"]}
    assert skipped == {
        "schema": False,
        "references": False,
        "consistency": True,
        "integrity": True,
    }


def test_validation_can_aggregate_structurally_safe_later_stage_errors() -> None:
    profile = load_profile(EXAMPLES / "minimal-valid-evidence.json")
    profile["operation"]["output_refs"] = ["missing-output"]
    profile["evidence"]["integrity"]["statement_digest"] = "sha256:" + "0" * 64

    report = build_validation_report(profile, fail_fast=False)

    assert report["fail_fast"] is False
    issue_codes = {issue["code"] for issue in report["issues"]}
    assert {
        "unresolved_output_ref",
        "provenance_output_refs_mismatch",
        "statement_digest_mismatch",
    } <= issue_codes
    assert report["issue_summary"]["by_stage"] == {
        "consistency": 1,
        "integrity": 1,
        "references": 1,
    }
    assert not any(stage["skipped"] for stage in report["stages"])


def test_schema_failure_skips_dependent_stages_even_when_aggregating() -> None:
    profile = copy.deepcopy(load_profile(EXAMPLES / "minimal-valid-evidence.json"))
    del profile["actor"]

    report = build_validation_report(profile, fail_fast=False)

    assert report["primary_error_code"] == "schema_violation"
    assert report["issue_summary"]["by_stage"] == {"schema": 1}
    skipped = {stage["name"]: stage["skipped"] for stage in report["stages"]}
    assert skipped == {
        "schema": False,
        "references": True,
        "consistency": True,
        "integrity": True,
    }


@pytest.mark.parametrize(
    "filename",
    [
        "minimal-valid-evidence.json",
        "valid-high-risk-payment-review-evidence.json",
    ],
)
def test_validate_profile_cli_command(filename: str) -> None:
    runner = CliRunner()

    result = runner.invoke(
        main,
        ["validate-profile", str(EXAMPLES / filename)],
    )

    assert result.exit_code == 0, result.output
    payload = json.loads(result.output)
    assert payload["ok"] is True
