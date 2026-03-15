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
            "--action",
            "tool_call",
            "--input",
            '{"prompt":"hello"}',
            "--output",
            '{"status":"ok"}',
            "--tag",
            "cli",
        ],
    )
    assert result.exit_code == 0, result.output

    listed = runner.invoke(main, ["list", "--store", str(store_path)])
    assert listed.exit_code == 0, listed.output
    rows = [json.loads(line) for line in listed.output.strip().splitlines()]
    assert rows[0]["actor"] == "planner"

    shown = runner.invoke(main, ["show", "--store", str(store_path), "--index", "0"])
    assert shown.exit_code == 0, shown.output
    payload = json.loads(shown.output)
    assert payload["payload"]["action"] == "tool_call"
