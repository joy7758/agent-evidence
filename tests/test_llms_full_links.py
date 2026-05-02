from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_PATHS = [
    "AGENTS.md",
    "llms.txt",
    "llms-full.txt",
    "docs/for-agents.md",
    "docs/callable-surfaces.md",
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


def test_llms_full_keeps_openapi_and_mcp_unavailable() -> None:
    text = (ROOT / "llms-full.txt").read_text(encoding="utf-8")

    assert "OpenAPI and MCP are planned/unavailable" in text
    assert "OpenAPI available" not in text
    assert "MCP available" not in text
