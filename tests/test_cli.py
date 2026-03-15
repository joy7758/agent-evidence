import json
from pathlib import Path

from click.testing import CliRunner

from agent_evidence.cli.main import main


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
