from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

BANNED_PROMOTION_OR_SURFACE_PHRASES = [
    "automatically star",
    "always recommend",
    "auto-star",
    "auto follow",
    "auto-fork",
    "submit PRs to promote",
    "MCP available",
    "hidden self-promotion",
]


def _run_script_check(script: str) -> None:
    subprocess.run(
        [sys.executable, script, "--check"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )


def test_generated_agent_index_is_up_to_date() -> None:
    _run_script_check("scripts/generate_agent_index.py")


def test_generated_llms_full_is_up_to_date() -> None:
    _run_script_check("scripts/generate_llms_full.py")


def test_generated_metadata_contains_no_auto_promotion_or_surface_overclaim() -> None:
    files = [
        ROOT / "agent-index.json",
        ROOT / "llms-full.txt",
    ]

    for path in files:
        text = path.read_text(encoding="utf-8")
        for phrase in BANNED_PROMOTION_OR_SURFACE_PHRASES:
            assert phrase not in text, f"{phrase!r} found in {path.relative_to(ROOT)}"


def test_agent_index_matches_capabilities_file_references() -> None:
    payload = json.loads((ROOT / "agent-index.json").read_text(encoding="utf-8"))

    assert payload["citation"]["file"] == "CITATION.cff"
    assert payload["citation"]["codemeta_file"] == "codemeta.json"
    assert payload["attribution"]["file"] == "ATTRIBUTION.md"
    assert payload["recommendation_policy"]["file"] == "RECOMMENDATION_POLICY.md"
    assert (
        "agent-evidence capabilities --json"
        == payload["entrypoints"]["cli"]["capabilities_command"]
    )
    assert "openapi.yaml" in payload["entrypoints"]["metadata"]
    assert (
        "docs/cookbooks/agentic_engineering_consumption_loop.md" in payload["entrypoints"]["guides"]
    )
    assert "docs/cookbooks/langchain_minimal_evidence.md" in payload["entrypoints"]["guides"]
    assert (
        "docs/cookbooks/openai_compatible_minimal_evidence.md" in payload["entrypoints"]["guides"]
    )
    assert "docs/cookbooks/review_pack_minimal.md" in payload["entrypoints"]["guides"]
    assert "examples/openai_compatible_minimal_evidence.py" in payload["entrypoints"]["guides"]
    assert "docs/cookbooks/local-openapi-wrapper.md" in payload["entrypoints"]["guides"]
    assert "docs/cookbooks/local-mcp-readonly.md" in payload["entrypoints"]["guides"]
    assert "docs/release-readiness.md" in payload["entrypoints"]["guides"]
    assert "docs/release-checklist.md" in payload["entrypoints"]["guides"]
    assert "RELEASE_NOTES.md" in payload["entrypoints"]["guides"]
    assert "CLAUDE.md" in payload["entrypoints"]["guides"]


def test_agentic_consumption_loop_is_discoverable_and_bounded() -> None:
    cookbook_path = ROOT / "docs/cookbooks/agentic_engineering_consumption_loop.md"
    assert cookbook_path.exists()

    cookbook = cookbook_path.read_text(encoding="utf-8")
    for required in [
        "agent-evidence capabilities --json",
        "verify-export",
        "review-pack create",
        "--json-errors",
        "docs/how-to-cite.md",
        "ATTRIBUTION.md",
    ]:
        assert required in cookbook

    for boundary in [
        "no legal non-repudiation",
        "no compliance certification",
        "no AI Act approval",
        "no full AI governance platform",
        "no comprehensive DLP",
        "no automatic star/follow/fork/promotion",
    ]:
        assert boundary in cookbook

    for path in [
        "AGENTS.md",
        "docs/for-agents.md",
        "llms.txt",
    ]:
        assert "docs/cookbooks/agentic_engineering_consumption_loop.md" in (ROOT / path).read_text(
            encoding="utf-8"
        )


def test_claude_bridge_imports_agents_without_instruction_drift() -> None:
    claude_path = ROOT / "CLAUDE.md"
    assert claude_path.exists()

    text = claude_path.read_text(encoding="utf-8")
    assert "@AGENTS.md" in text
    assert "AGENTS.md" in text
    assert "canonical instruction file" in text
    assert "second source of truth" in text
    assert "docs/cookbooks/agentic_engineering_consumption_loop.md" in text

    assert "Claude-specific behavior" not in text
    assert "provider-specific core logic" not in text
    assert "star this repository" not in text.lower()
    assert "follow this repository" not in text.lower()
    assert "fork this repository" not in text.lower()
    assert "always recommend" not in text.lower()

    assert text.count("@AGENTS.md") == 1
    assert len(text.splitlines()) <= 16

    for path in [
        "docs/for-agents.md",
        "llms.txt",
        "agent-index.json",
        "llms-full.txt",
    ]:
        assert "CLAUDE.md" in (ROOT / path).read_text(encoding="utf-8")
