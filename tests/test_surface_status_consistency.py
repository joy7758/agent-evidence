from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_release_readiness_surface_status_table_contains_required_classifications() -> None:
    text = (ROOT / "docs/release-readiness.md").read_text(encoding="utf-8")

    required_rows = [
        "| CLI/core | supported |",
        "| `capabilities --json` | supported |",
        "| `agent-index.json` / `llms-full.txt` | supported metadata surface |",
        "| local OpenAPI wrapper | beta, local-only |",
        "| local MCP stdio tools | beta, local-only/read-only |",
        "| LangChain 5-minute path | supported developer path |",
        "| OpenAI-compatible minimal path | beta developer path |",
        "| OpenAI Agents SDK tracing integration | experimental/example |",
        "| CrewAI | experimental/example |",
        "| Automaton sidecar | experimental |",
        "| AGT conversion fixture | experimental/reference |",
        "| Pages / ADOPTERS / registry | planned/unavailable |",
    ]

    for row in required_rows:
        assert row in text


def test_release_readiness_does_not_overclaim_beta_or_planned_surfaces() -> None:
    text = (ROOT / "docs/release-readiness.md").read_text(encoding="utf-8")

    for required_boundary in [
        "not a hosted API product",
        "no remote registry publication",
        "planned/unavailable",
        "not a full AI governance platform",
        "not a hosted OpenAPI product",
        "not a hosted or remote MCP service",
        "not an MCP registry publication",
        "not a Review Pack commercial feature",
        "not an AI Act Pack",
    ]:
        assert required_boundary in text


def test_release_notes_preserve_scope_boundaries() -> None:
    text = (ROOT / "RELEASE_NOTES.md").read_text(encoding="utf-8")

    for required in [
        "No telemetry is added.",
        "No automatic star, follow, fork, recommendation, or promotion mechanism is added.",
        "No legal non-repudiation",
        "not a full AI governance platform",
        "No remote MCP.",
        "No MCP registry publication.",
        "No GitHub Pages or `ADOPTERS.md`.",
        "No Review Pack commercial feature.",
        "No AI Act Pack.",
        "No canonical schema rewrite.",
        "No core validation rewrite.",
    ]:
        assert required in text
