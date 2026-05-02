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
    assert "docs/cookbooks/local-openapi-wrapper.md" in payload["entrypoints"]["guides"]
