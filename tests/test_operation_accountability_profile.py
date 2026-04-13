import json
from pathlib import Path

import pytest
from click.testing import CliRunner

from agent_evidence.cli.main import main
from agent_evidence.oap import validate_profile_file

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
    issue_codes = {issue["code"] for stage in report["stages"] for issue in stage["issues"]}
    assert expected_code in issue_codes


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
