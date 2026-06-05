from __future__ import annotations

import json
import sys
import tomllib
from pathlib import Path

from click.testing import CliRunner

from agent_evidence.cli.main import main
from agent_evidence.mcp.server import RESOURCE_URIS, TOOL_NAMES

ROOT = Path(__file__).resolve().parents[1]

FORBIDDEN_TOOLS = {
    "create_review_pack",
    "explain_receipt",
    "sign_bundle",
    "upload_bundle",
    "record_event",
    "shell_exec",
    "run_command",
    "write_file",
    "github_star",
    "github_follow",
    "github_fork",
    "github_pr",
    "telemetry",
}


def _pyproject() -> dict:
    return tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))


def test_mcp_dependency_is_optional_not_core() -> None:
    project = _pyproject()["project"]

    assert "mcp>=1.27,<2" in project["optional-dependencies"]["mcp"]
    assert all(not dependency.startswith("mcp") for dependency in project["dependencies"])


def test_mcp_tool_boundary_contains_no_forbidden_tools() -> None:
    tools = set(TOOL_NAMES)

    assert tools == {
        "list_capabilities",
        "list_schemas",
        "validate_profile",
        "verify_bundle",
    }
    assert tools.isdisjoint(FORBIDDEN_TOOLS)


def test_mcp_resource_boundary_contains_only_fixed_agent_evidence_uris() -> None:
    resources = set(RESOURCE_URIS)

    assert resources == {
        "agent-evidence://capabilities",
        "agent-evidence://schema/agent-index",
        "agent-evidence://schema/openapi",
        "agent-evidence://docs/for-agents",
        "agent-evidence://docs/callable-surfaces",
        "agent-evidence://citation",
        "agent-evidence://recommendation-policy",
    }
    assert all(uri.startswith("agent-evidence://") for uri in resources)


def test_mcp_cli_help_is_stdio_only() -> None:
    result = CliRunner().invoke(main, ["mcp", "--help"])

    assert result.exit_code == 0, result.output
    assert "--transport" in result.output
    assert "stdio" in result.output
    assert "sse" not in result.output.lower()
    assert "streamable" not in result.output.lower()


def test_mcp_module_help_is_available() -> None:
    import subprocess

    result = subprocess.run(
        [sys.executable, "-m", "agent_evidence.mcp.server", "--help"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )

    assert "--transport" in result.stdout
    assert "stdio" in result.stdout


def test_mcp_metadata_reports_local_stdio_wrapper_only() -> None:
    result = CliRunner().invoke(main, ["capabilities", "--json"])

    assert result.exit_code == 0, result.output
    payload = json.loads(result.output)
    wrappers = {item["name"]: item for item in payload["local_callable_wrappers"]}

    assert wrappers["MCP"]["available"] is True
    assert wrappers["MCP"]["scope"] == "local"
    assert wrappers["MCP"]["transport"] == "stdio"
    assert wrappers["MCP"]["tools"] == list(TOOL_NAMES)
    assert wrappers["MCP"]["prompts"] == []
    assert {item["name"] for item in payload["planned_but_unavailable_surfaces"]} == {
        "GitHub Pages"
    }


def test_mcp_files_contain_no_forbidden_implementation_terms() -> None:
    text = (ROOT / "agent_evidence/mcp/server.py").read_text(encoding="utf-8").lower()

    for forbidden in FORBIDDEN_TOOLS:
        assert forbidden not in text
    for forbidden in [
        "registry publication",
        "remote transport",
        "0.0.0.0",
    ]:
        assert forbidden not in text
