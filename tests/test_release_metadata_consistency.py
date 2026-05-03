from __future__ import annotations

import json
import tomllib
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


def _project_version() -> str:
    pyproject = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    return str(pyproject["project"]["version"])


def test_release_versions_are_aligned() -> None:
    version = _project_version()

    citation = yaml.safe_load((ROOT / "CITATION.cff").read_text(encoding="utf-8"))
    codemeta = json.loads((ROOT / "codemeta.json").read_text(encoding="utf-8"))
    agent_index = json.loads((ROOT / "agent-index.json").read_text(encoding="utf-8"))
    project_facts = (ROOT / "docs/project-facts.md").read_text(encoding="utf-8")
    llms_full = (ROOT / "llms-full.txt").read_text(encoding="utf-8")

    assert version == "0.3.0"
    assert str(citation["version"]) == version
    assert str(codemeta["version"]) == version
    assert str(agent_index["current_status"]["version"]) == version
    assert f"`{version}`" in project_facts
    assert f"- Version: `{version}`" in llms_full


def test_release_metadata_uses_existing_doi_without_inventing_new_one() -> None:
    citation = yaml.safe_load((ROOT / "CITATION.cff").read_text(encoding="utf-8"))
    codemeta = json.loads((ROOT / "codemeta.json").read_text(encoding="utf-8"))
    readiness = (ROOT / "docs/release-readiness.md").read_text(encoding="utf-8")

    assert citation["doi"] == "10.5281/zenodo.19334062"
    assert codemeta["identifier"] == "https://doi.org/10.5281/zenodo.19334062"
    assert "Do not invent a new DOI." in readiness
    assert "release-specific archive metadata" in " ".join(readiness.split())


def test_release_docs_and_stale_callable_statements_are_present() -> None:
    for path in [
        "RELEASE_NOTES.md",
        "docs/release-readiness.md",
        "docs/release-checklist.md",
    ]:
        assert (ROOT / path).exists(), f"missing {path}"

    local_openapi = (ROOT / "docs/cookbooks/local-openapi-wrapper.md").read_text(encoding="utf-8")
    assert "There is no MCP server yet" not in local_openapi
    assert "MCP is available separately as a local stdio read-only / verify-first wrapper" in (
        local_openapi
    )


def test_release_checklist_covers_major_release_checks() -> None:
    checklist = (ROOT / "docs/release-checklist.md").read_text(encoding="utf-8")

    for required in [
        "pytest -q",
        "ruff check",
        "ruff format --check",
        "agent-evidence capabilities --json | python -m json.tool",
        "python scripts/generate_agent_index.py --check",
        "python scripts/generate_llms_full.py --check",
        "CITATION.cff",
        "codemeta.json",
        "DEVELOPMENT_LEDGER.jsonl",
        "GET /healthz",
        "GET /v1/capabilities",
        "agent-evidence mcp --transport stdio --help",
        "python examples/langchain_minimal_evidence.py",
        "python examples/openai_compatible_minimal_evidence.py",
        "secret sentinel check",
        "DOI handling",
        "PyPI",
        "GitHub release",
    ]:
        assert required in checklist
