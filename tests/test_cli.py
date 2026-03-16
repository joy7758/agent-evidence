import json
from pathlib import Path

from click.testing import CliRunner

from agent_evidence.aep import verify_bundle
from agent_evidence.cli.main import main
from tests.test_automaton_integration import _create_git_repo, _create_state_db


def test_cli_record_and_show(tmp_path: Path) -> None:
    store_path = tmp_path / "evidence.jsonl"
    runner = CliRunner()

    result = runner.invoke(
        main,
        [
            "record",
            "--store",
            str(store_path),
            "--actor",
            "planner",
            "--event-type",
            "tool.call",
            "--input",
            '{"prompt":"hello"}',
            "--output",
            '{"status":"ok"}',
            "--context",
            '{"source":"cli","component":"tool"}',
            "--tag",
            "cli",
        ],
    )
    assert result.exit_code == 0, result.output

    listed = runner.invoke(main, ["list", "--store", str(store_path)])
    assert listed.exit_code == 0, listed.output
    rows = [json.loads(line) for line in listed.output.strip().splitlines()]
    assert rows[0]["actor"] == "planner"
    assert rows[0]["event_type"] == "tool.call"

    shown = runner.invoke(main, ["show", "--store", str(store_path), "--index", "0"])
    assert shown.exit_code == 0, shown.output
    payload = json.loads(shown.output)
    assert payload["event"]["event_type"] == "tool.call"
    assert payload["event"]["context"]["component"] == "tool"

    verified = runner.invoke(main, ["verify", "--store", str(store_path)])
    assert verified.exit_code == 0, verified.output
    result = json.loads(verified.output)
    assert result["ok"] is True


def test_cli_record_rejects_invalid_json_option(tmp_path: Path) -> None:
    store_path = tmp_path / "evidence.jsonl"
    runner = CliRunner()

    result = runner.invoke(
        main,
        [
            "record",
            "--store",
            str(store_path),
            "--actor",
            "planner",
            "--event-type",
            "tool.call",
            "--input",
            '{"prompt":',
        ],
    )

    assert result.exit_code != 0
    assert "Invalid JSON" in result.output


def test_cli_export_automaton_help_marks_experimental() -> None:
    runner = CliRunner()

    result = runner.invoke(main, ["export", "automaton", "--help"])

    assert result.exit_code == 0, result.output
    assert "Experimental: export a read-only Automaton snapshot" in result.output
    assert "--state-db" in result.output
    assert "--repo" in result.output
    assert "--runtime-root" in result.output
    assert "--out" in result.output


def test_cli_export_automaton_generates_bundle(tmp_path: Path) -> None:
    state_db = tmp_path / "state.db"
    repo_root = tmp_path / "state-repo"
    output_dir = tmp_path / "out" / "automaton-bundle"
    _create_state_db(state_db)
    _create_git_repo(repo_root)

    runner = CliRunner()
    result = runner.invoke(
        main,
        [
            "export",
            "automaton",
            "--state-db",
            str(state_db),
            "--repo",
            str(repo_root),
            "--runtime-root",
            str(repo_root),
            "--out",
            str(output_dir),
        ],
    )

    assert result.exit_code == 0, result.output
    payload = json.loads(result.output)
    assert payload["experimental"] is True
    assert payload["verified"] is True
    assert payload["manifest"]["capture_mode"] == "readonly"
    assert payload["manifest"]["source_runtime"] == "automaton"
    assert payload["manifest"]["source_runtime_version"]
    assert payload["manifest"]["source_runtime_commit"]
    assert payload["manifest"]["source_runtime_dirty"] is False
    assert payload["manifest"]["source_schema_fingerprint"].startswith("sha256:")

    verify_report = verify_bundle(output_dir)
    assert verify_report["ok"] is True
