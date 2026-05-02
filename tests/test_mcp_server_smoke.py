from __future__ import annotations

import asyncio
import json
from pathlib import Path

from agent_evidence.aep import verify_bundle as verify_bundle_core
from agent_evidence.cli.main import build_capabilities_payload
from agent_evidence.mcp.server import (
    RESOURCE_URIS,
    SCHEMA_FILES,
    TOOL_NAMES,
    create_mcp_server,
    list_capabilities,
    list_schemas,
    read_resource,
    validate_profile,
    verify_bundle,
)
from agent_evidence.oap import build_validation_report, load_profile

ROOT = Path(__file__).resolve().parents[1]


def run_async(coro):
    return asyncio.run(coro)


def test_mcp_server_exposes_only_approved_tools_resources_and_no_prompts() -> None:
    server = create_mcp_server()

    tools = run_async(server.list_tools())
    resources = run_async(server.list_resources())
    prompts = run_async(server.list_prompts())

    assert {tool.name for tool in tools} == set(TOOL_NAMES)
    assert {str(resource.uri) for resource in resources} == set(RESOURCE_URIS)
    assert prompts == []


def test_list_capabilities_matches_cli_payload_builder() -> None:
    assert list_capabilities() == build_capabilities_payload()


def test_list_schemas_defaults_to_metadata_only() -> None:
    payload = list_schemas()

    assert payload["ok"] is True
    assert [schema["path"] for schema in payload["schemas"]] == [
        item["path"] for item in SCHEMA_FILES
    ]
    assert all("content" not in schema for schema in payload["schemas"])


def test_list_schemas_can_include_contents_for_fixed_files_only() -> None:
    payload = list_schemas(include_contents=True)

    assert payload["ok"] is True
    assert {schema["path"] for schema in payload["schemas"]} == {
        item["path"] for item in SCHEMA_FILES
    }
    assert all(schema["content"] for schema in payload["schemas"])


def test_validate_profile_matches_core_for_inline_profile() -> None:
    profile = load_profile(ROOT / "examples/minimal-valid-evidence.json")
    expected = build_validation_report(profile, source="request.profile", fail_fast=True)

    assert validate_profile(profile=profile) == expected


def test_validate_profile_matches_core_for_profile_path() -> None:
    profile_path = ROOT / "examples/minimal-valid-evidence.json"
    profile = load_profile(profile_path)
    expected = build_validation_report(profile, source=str(profile_path), fail_fast=True)

    assert validate_profile(profile_path=str(profile_path)) == expected


def test_validate_profile_rejects_unsupported_shapes() -> None:
    assert validate_profile()["error"]["code"] == "invalid_request"
    assert (
        validate_profile(profile_path="examples/minimal-valid-evidence.json", profile={})["error"][
            "code"
        ]
        == "invalid_request"
    )


def test_verify_bundle_matches_core_behavior() -> None:
    bundle_path = ROOT / "tests/fixtures/agent_evidence_profile/valid/basic-bundle"

    assert verify_bundle(str(bundle_path)) == verify_bundle_core(bundle_path)


def test_read_resources_return_fixed_content() -> None:
    capabilities = json.loads(read_resource("agent-evidence://capabilities"))
    assert capabilities == build_capabilities_payload()

    for uri in RESOURCE_URIS:
        content = read_resource(uri)
        assert isinstance(content, str)
        assert content
