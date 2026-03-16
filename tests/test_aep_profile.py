import json
from pathlib import Path

import pytest
from click.testing import CliRunner

from agent_evidence.aep import EvidenceBundleBuilder, verify_bundle
from agent_evidence.cli.main import main

FIXTURE_ROOT = Path(__file__).parent / "fixtures" / "agent_evidence_profile"


def _write_bundle(bundle_dir: Path) -> Path:
    builder = EvidenceBundleBuilder(
        run_id="profile-run-001",
        source_runtime="langchain",
        trace_ref="trace-profile-run-001",
        redaction={"omit_request": False, "omit_response": False},
    )
    builder.add_record(
        event_type="chain.start",
        timestamp="2026-03-17T00:00:00+00:00",
        payload={
            "actor": "planner",
            "source": "langchain",
            "component": "chain",
            "attributes": {
                "openinference": {"span_kind": "CHAIN"},
                "gen_ai": {
                    "system": "langchain",
                    "operation_name": "chain.start",
                },
            },
            "request": {"mode": "digest_only", "digest": "sha256:" + "1" * 64},
            "response": {"mode": "absent"},
        },
    )
    builder.add_record(
        event_type="tool.end",
        timestamp="2026-03-17T00:00:01+00:00",
        payload={
            "actor": "calculator",
            "source": "langchain",
            "component": "tool",
            "attributes": {
                "openinference": {"span_kind": "TOOL"},
                "gen_ai": {
                    "system": "langchain",
                    "operation_name": "tool.end",
                },
            },
            "request": {"mode": "digest_only", "digest": "sha256:" + "2" * 64},
            "response": {"mode": "digest_only", "digest": "sha256:" + "3" * 64},
        },
    )
    return builder.write_bundle(bundle_dir)


def test_bundle_root_hash_is_deterministic_for_same_input(tmp_path: Path) -> None:
    first_dir = _write_bundle(tmp_path / "bundle-a")
    second_dir = _write_bundle(tmp_path / "bundle-b")

    first_manifest = json.loads((first_dir / "manifest.json").read_text(encoding="utf-8"))
    second_manifest = json.loads((second_dir / "manifest.json").read_text(encoding="utf-8"))

    assert first_manifest["bundle_root_hash"] == second_manifest["bundle_root_hash"]


def test_verify_bundle_detects_record_tampering(tmp_path: Path) -> None:
    bundle_dir = _write_bundle(tmp_path / "tampered-bundle")
    records_path = bundle_dir / "records.jsonl"
    records = [json.loads(line) for line in records_path.read_text(encoding="utf-8").splitlines()]
    records[1]["event_type"] = "tool.error"
    records_path.write_text(
        "\n".join(json.dumps(record, sort_keys=True) for record in records) + "\n",
        encoding="utf-8",
    )

    report = verify_bundle(bundle_dir)

    assert report["ok"] is False
    integrity_stage = next(stage for stage in report["stages"] if stage["name"] == "integrity")
    issue_codes = {issue["code"] for issue in integrity_stage["issues"]}
    assert "record_hash_mismatch" in issue_codes


def test_cli_verify_bundle_command(tmp_path: Path) -> None:
    bundle_dir = _write_bundle(tmp_path / "cli-bundle")
    runner = CliRunner()

    result = runner.invoke(main, ["verify-bundle", "--bundle-dir", str(bundle_dir)])

    assert result.exit_code == 0, result.output
    payload = json.loads(result.output)
    assert payload["ok"] is True


@pytest.mark.parametrize(
    ("fixture_name", "runtime_version_expected"),
    [
        ("basic-bundle", False),
        ("live-automaton-bundle", False),
        ("live-automaton-runtime-root-bundle", True),
    ],
)
def test_valid_profile_fixtures_verify(fixture_name: str, runtime_version_expected: bool) -> None:
    bundle_dir = FIXTURE_ROOT / "valid" / fixture_name
    report = verify_bundle(bundle_dir)

    assert report["ok"] is True

    manifest = json.loads((bundle_dir / "manifest.json").read_text(encoding="utf-8"))
    if runtime_version_expected:
        assert manifest["source_runtime_version"]
        assert manifest["source_runtime_commit"]
        assert manifest["source_runtime_dirty"] is True
    else:
        if fixture_name.startswith("live-automaton"):
            assert manifest["source_runtime_version"] is None
            assert manifest["source_runtime_commit"] is None
            assert manifest["source_runtime_dirty"] is None


@pytest.mark.parametrize(
    "fixture_name",
    [
        "tampered-bundle",
        "live-automaton-tampered-bundle",
        "live-automaton-runtime-root-tampered-bundle",
    ],
)
def test_invalid_profile_fixtures_fail(fixture_name: str) -> None:
    report = verify_bundle(FIXTURE_ROOT / "invalid" / fixture_name)

    assert report["ok"] is False
    integrity_stage = next(stage for stage in report["stages"] if stage["name"] == "integrity")
    issue_codes = {issue["code"] for issue in integrity_stage["issues"]}
    assert "record_hash_mismatch" in issue_codes
