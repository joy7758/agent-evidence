from __future__ import annotations

import json

from click.testing import CliRunner

from agent_evidence.cli.main import main


def test_aep_media_cli_commands_are_registered() -> None:
    runner = CliRunner()
    result = runner.invoke(main, ["--help"])

    assert result.exit_code == 0, result.output
    for command in [
        "validate-media-profile",
        "build-media-bundle",
        "verify-media-bundle",
        "validate-media-time-profile",
        "run-media-evaluation",
        "build-aep-media-release-pack",
    ]:
        assert command in result.output


def test_aep_media_validate_profile_cli_smoke() -> None:
    runner = CliRunner()
    result = runner.invoke(
        main,
        ["validate-media-profile", "examples/media/minimal-valid-media-evidence.json"],
    )

    assert result.exit_code == 0, result.output
    report = json.loads(result.output)
    assert report["ok"] is True
    assert report["profile"] == "aep-media-evidence-profile@0.1"
