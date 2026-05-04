from __future__ import annotations

import json
import tomllib
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
VERSION = "0.6.0"
CONCEPT_DOI = "10.5281/zenodo.19334061"
STALE_V020_DOI = "10.5281/zenodo.19334062"
V030_VERSION_DOI = "10.5281/zenodo.19998176"
V031_VERSION_DOI = "10.5281/zenodo.19998690"
V040_VERSION_DOI = "10.5281/zenodo.20004271"
V050_VERSION_DOI = "10.5281/zenodo.20011103"
V060_VERSION_DOI = "10.5281/zenodo.20013667"


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

    assert version == VERSION
    assert str(citation["version"]) == version
    assert str(codemeta["version"]) == version
    assert str(agent_index["current_status"]["version"]) == version
    assert f"`{version}`" in project_facts
    assert f"- Version: `{version}`" in llms_full


def test_release_metadata_uses_concept_doi_as_primary_project_doi() -> None:
    citation = yaml.safe_load((ROOT / "CITATION.cff").read_text(encoding="utf-8"))
    codemeta = json.loads((ROOT / "codemeta.json").read_text(encoding="utf-8"))
    agent_index = json.loads((ROOT / "agent-index.json").read_text(encoding="utf-8"))
    readiness = (ROOT / "docs/release-readiness.md").read_text(encoding="utf-8")

    assert citation["doi"] == CONCEPT_DOI
    assert codemeta["identifier"] == f"https://doi.org/{CONCEPT_DOI}"
    assert codemeta["citation"] == f"https://doi.org/{CONCEPT_DOI}"
    assert agent_index["current_status"]["doi"] == CONCEPT_DOI
    assert agent_index["citation"]["doi"] == CONCEPT_DOI
    assert "Do not invent a new DOI." in readiness
    assert "Zenodo concept DOI" in readiness


def test_stale_v020_doi_is_not_active_citation_metadata() -> None:
    for path in [
        "CITATION.cff",
        "codemeta.json",
        "README.md",
        "docs/project-facts.md",
        "agent-index.json",
        "llms-full.txt",
    ]:
        assert STALE_V020_DOI not in (ROOT / path).read_text(encoding="utf-8"), path


def test_prior_version_dois_are_release_specific_documentation_only() -> None:
    release_specific_docs = [
        "RELEASE_NOTES.md",
        "docs/how-to-cite.md",
        "docs/project-facts.md",
        "docs/release-readiness.md",
    ]
    combined = "\n".join(
        (ROOT / path).read_text(encoding="utf-8") for path in release_specific_docs
    )
    assert V030_VERSION_DOI in combined
    assert V031_VERSION_DOI in combined
    assert V040_VERSION_DOI in combined
    assert V050_VERSION_DOI in combined
    assert V060_VERSION_DOI in combined

    for path in [
        "CITATION.cff",
        "codemeta.json",
        "README.md",
        "agent-index.json",
        "llms-full.txt",
    ]:
        text = (ROOT / path).read_text(encoding="utf-8")
        assert V030_VERSION_DOI not in text, path
        assert V031_VERSION_DOI not in text, path
        assert V040_VERSION_DOI not in text, path
        assert V050_VERSION_DOI not in text, path
        assert V060_VERSION_DOI not in text, path


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
        "agent-evidence review-pack create",
        "Review Pack V0.3",
        "review_pack_version",
        "RP-CHECK-001",
        "secret_scan_status",
        "--json-errors",
        "tampered bundle fail-closed",
        "Review Pack secret sentinel check",
        "secret sentinel check",
        "DOI handling",
        "PyPI",
        "GitHub release",
    ]:
        assert required in checklist


def test_review_pack_v03_release_prep_docs_are_aligned() -> None:
    notes = (ROOT / "RELEASE_NOTES.md").read_text(encoding="utf-8")
    readiness = (ROOT / "docs/release-readiness.md").read_text(encoding="utf-8")
    checklist = (ROOT / "docs/release-checklist.md").read_text(encoding="utf-8")

    for required in [
        "v0.6.0",
        "Review Pack V0.3",
        "stable `RP-CHECK-*` reviewer checklist IDs",
        "`pack_creation_mode: local_offline`",
        "conservative `secret_scan_status`",
        "optional `--json-errors`",
        "not comprehensive DLP",
        "does not change OpenAPI or MCP behavior",
        "No AI Act Pack.",
        "No PDF or HTML report generator.",
        "No dashboard.",
        "No hosted or remote review service.",
    ]:
        assert required in notes

    for required in [
        "| Review Pack V0.3 | beta, local-only/offline reviewer package |",
        "Review Pack V0.3 is not a legal/compliance product",
        "Review Pack V0.3 is not comprehensive DLP",
        "not an AI Act Pack",
        "v0.6.0 released and post-release audited",
        "PyPI v0.6.0: published and latest",
        "Post-release verification covered",
    ]:
        assert required in readiness

    for required in [
        "Review Pack V0.3 Smoke",
        "review_pack_version",
        '"0.3"',
        "RP-CHECK-001",
        "Secret and Private Key Boundary",
        "not comprehensive DLP",
        "secret_scan_status",
        "--json-errors",
        "Reviewer Checklist",
        "Verification Details",
        "Artifact Inventory",
        "Recommended Reviewer Actions",
        "What This Does Not Prove",
        "tampered bundle fail-closed",
        "no OpenAPI or MCP Review Pack endpoint/tool",
    ]:
        assert required in checklist


def test_post_release_docs_do_not_retain_stale_v060_release_prep_wording() -> None:
    checked = [
        "README.md",
        "docs/how-to-cite.md",
        "docs/release-readiness.md",
        "docs/project-facts.md",
        "RELEASE_NOTES.md",
    ]
    combined = "\n".join((ROOT / path).read_text(encoding="utf-8") for path in checked)

    for stale in [
        "v0.4.0 Review Pack release preparation",
        "v0.6.0 release-prep",
        "prepared but not released",
        "GitHub Release v0.6.0: not created",
        "PyPI v0.6.0: not uploaded",
        "final release no-go",
        "release-prep only",
        "Version 0.4.0",
        "version = {0.4.0}",
        "Version 0.5.0",
        "version = {0.5.0}",
    ]:
        assert stale not in combined

    how_to_cite = (ROOT / "docs/how-to-cite.md").read_text(encoding="utf-8")
    assert "Version 0.6.0" in how_to_cite
    assert "version = {0.6.0}" in how_to_cite
    assert CONCEPT_DOI in how_to_cite
    assert V060_VERSION_DOI in how_to_cite
