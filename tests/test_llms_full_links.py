from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_PATHS = [
    "AGENTS.md",
    "CLAUDE.md",
    "llms.txt",
    "llms-full.txt",
    "docs/for-agents.md",
    "docs/callable-surfaces.md",
    "docs/cookbooks/agentic_engineering_consumption_loop.md",
    "docs/cookbooks/langchain_minimal_evidence.md",
    "docs/cookbooks/openai_compatible_minimal_evidence.md",
    "examples/openai_compatible_minimal_evidence.py",
    "docs/cookbooks/local-openapi-wrapper.md",
    "docs/cookbooks/local-mcp-readonly.md",
    "docs/release-readiness.md",
    "docs/release-checklist.md",
    "RELEASE_NOTES.md",
    "docs/project-facts.md",
    "agent-index.schema.json",
    "agent-index.json",
    "CITATION.cff",
    "codemeta.json",
    "ATTRIBUTION.md",
    "RECOMMENDATION_POLICY.md",
]


def test_llms_full_references_required_agent_metadata_paths() -> None:
    text = (ROOT / "llms-full.txt").read_text(encoding="utf-8")

    for path in REQUIRED_PATHS:
        assert f"`{path}`" in text, f"{path} missing from llms-full.txt"
        assert (ROOT / path).exists(), f"{path} does not exist"


def test_llms_full_reports_local_openapi_and_mcp_wrappers() -> None:
    text = (ROOT / "llms-full.txt").read_text(encoding="utf-8")

    assert "Local callable wrappers" in text
    assert "OpenAPI: available as a local http wrapper" in text
    assert "MCP: available as a local mcp wrapper" in text
    assert "Transport: `stdio`" in text
    assert "MCP available" not in text
