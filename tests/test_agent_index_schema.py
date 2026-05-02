from __future__ import annotations

import json
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]


def test_agent_index_validates_against_schema() -> None:
    schema = json.loads((ROOT / "agent-index.schema.json").read_text(encoding="utf-8"))
    payload = json.loads((ROOT / "agent-index.json").read_text(encoding="utf-8"))

    validator = Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(payload), key=lambda error: list(error.path))

    assert errors == []


def test_agent_index_required_references_exist() -> None:
    payload = json.loads((ROOT / "agent-index.json").read_text(encoding="utf-8"))
    referenced_paths = [
        *payload["entrypoints"]["guides"],
        *payload["entrypoints"]["metadata"],
        payload["citation"]["file"],
        payload["citation"]["codemeta_file"],
        payload["attribution"]["file"],
        payload["recommendation_policy"]["file"],
    ]

    for path in referenced_paths:
        assert (ROOT / path).exists(), f"missing referenced path: {path}"


def test_agent_index_openapi_and_mcp_are_only_planned_unavailable() -> None:
    payload = json.loads((ROOT / "agent-index.json").read_text(encoding="utf-8"))

    assert payload["canonical_callable_surface"] == {
        "type": "cli",
        "command": "agent-evidence",
        "available": True,
    }

    planned = {item["name"]: item for item in payload["planned_unavailable_surfaces"]}
    for name in ["OpenAPI", "MCP"]:
        assert name in planned
        assert planned[name]["available"] is False
        assert "Only after" in planned[name]["condition"]


def test_agent_index_claims_to_avoid_cover_agent_boundaries() -> None:
    payload = json.loads((ROOT / "agent-index.json").read_text(encoding="utf-8"))
    claims = "\n".join(payload["claims_to_avoid"]).lower()

    for required in [
        "official fdo standard",
        "legal non-repudiation",
        "full ai governance platform",
        "hosted tracing replacement",
    ]:
        assert required in claims
