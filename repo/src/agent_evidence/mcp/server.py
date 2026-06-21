from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from agent_evidence.aep import verify_bundle as verify_bundle_core
from agent_evidence.cli.main import build_capabilities_payload
from agent_evidence.oap import build_validation_report, load_profile

ROOT = Path(__file__).resolve().parents[2]

TOOL_NAMES = (
    "list_capabilities",
    "list_schemas",
    "validate_profile",
    "verify_bundle",
)

RESOURCE_URIS = (
    "agent-evidence://capabilities",
    "agent-evidence://schema/agent-index",
    "agent-evidence://schema/openapi",
    "agent-evidence://docs/for-agents",
    "agent-evidence://docs/callable-surfaces",
    "agent-evidence://citation",
    "agent-evidence://recommendation-policy",
)

SCHEMA_FILES = (
    {
        "name": "agent-index.schema",
        "path": "agent-index.schema.json",
        "description": "JSON Schema for agent-index.json.",
        "mime_type": "application/schema+json",
    },
    {
        "name": "agent-index",
        "path": "agent-index.json",
        "description": "Generated agent-facing repository index.",
        "mime_type": "application/json",
    },
    {
        "name": "openapi",
        "path": "openapi.yaml",
        "description": "OpenAPI contract for the local thin HTTP wrapper.",
        "mime_type": "application/yaml",
    },
    {
        "name": "citation",
        "path": "CITATION.cff",
        "description": "Citation File Format metadata.",
        "mime_type": "application/yaml",
    },
    {
        "name": "codemeta",
        "path": "codemeta.json",
        "description": "CodeMeta software metadata.",
        "mime_type": "application/json",
    },
)

RESOURCE_FILES = {
    "agent-evidence://schema/agent-index": ("agent-index.schema.json", "application/schema+json"),
    "agent-evidence://schema/openapi": ("openapi.yaml", "application/yaml"),
    "agent-evidence://docs/for-agents": ("docs/for-agents.md", "text/markdown"),
    "agent-evidence://docs/callable-surfaces": ("docs/callable-surfaces.md", "text/markdown"),
    "agent-evidence://citation": ("CITATION.cff", "application/yaml"),
    "agent-evidence://recommendation-policy": ("RECOMMENDATION_POLICY.md", "text/markdown"),
}


def _read_committed_file(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def _error(code: str, message: str) -> dict[str, Any]:
    return {
        "ok": False,
        "error": {
            "code": code,
            "message": message,
        },
    }


def list_capabilities() -> dict[str, Any]:
    return build_capabilities_payload()


def list_schemas(include_contents: bool = False) -> dict[str, Any]:
    schemas: list[dict[str, Any]] = []
    for item in SCHEMA_FILES:
        schema = dict(item)
        if include_contents:
            schema["content"] = _read_committed_file(item["path"])
        schemas.append(schema)
    return {
        "ok": True,
        "schemas": schemas,
    }


def validate_profile(
    profile_path: str | None = None,
    profile: dict[str, Any] | None = None,
    fail_fast: bool = True,
) -> dict[str, Any]:
    if profile_path and profile is not None:
        return _error("invalid_request", "Request must include profile_path or profile, not both.")
    if profile is not None:
        if not isinstance(profile, dict):
            return _error("invalid_request", "profile must be a JSON object.")
        return build_validation_report(
            profile,
            source="request.profile",
            fail_fast=fail_fast,
        )
    if profile_path:
        try:
            loaded_profile = load_profile(Path(profile_path))
        except (OSError, ValueError):
            return _error("invalid_request", "Unable to read or parse profile_path.")
        return build_validation_report(
            loaded_profile,
            source=profile_path,
            fail_fast=fail_fast,
        )
    return _error("invalid_request", "Request must include profile_path or profile.")


def verify_bundle(bundle_path: str | None = None) -> dict[str, Any]:
    if not bundle_path:
        return _error("invalid_request", "bundle_path must be a non-empty string.")
    try:
        return verify_bundle_core(Path(bundle_path))
    except OSError:
        return _error("invalid_request", "Unable to read bundle_path.")


def read_resource(uri: str) -> str:
    if uri == "agent-evidence://capabilities":
        return json.dumps(list_capabilities(), indent=2, sort_keys=True)
    path_and_mime = RESOURCE_FILES.get(uri)
    if path_and_mime is None:
        raise ValueError("Unknown agent-evidence resource URI.")
    path, _mime_type = path_and_mime
    return _read_committed_file(path)


def create_mcp_server() -> Any:
    try:
        from mcp.server.fastmcp import FastMCP
    except ModuleNotFoundError as exc:
        if exc.name == "mcp":
            raise RuntimeError(
                "Install MCP support with `pip install 'agent-evidence[mcp]'`."
            ) from exc
        raise

    server = FastMCP(
        "agent-evidence",
        instructions=(
            "Local read-only / verify-first MCP wrapper for agent-evidence. "
            "CLI/core behavior remains canonical."
        ),
    )

    server.tool()(list_capabilities)
    server.tool()(list_schemas)
    server.tool()(validate_profile)
    server.tool()(verify_bundle)

    @server.resource(
        "agent-evidence://capabilities",
        mime_type="application/json",
        description="Structured capabilities payload.",
    )
    def capabilities_resource() -> str:
        return read_resource("agent-evidence://capabilities")

    for uri, (_path, mime_type) in RESOURCE_FILES.items():

        def make_resource_reader(bound_uri: str):
            def resource_reader() -> str:
                return read_resource(bound_uri)

            return resource_reader

        server.resource(
            uri,
            name=uri.rsplit("/", 1)[-1],
            mime_type=mime_type,
        )(make_resource_reader(uri))

    return server


def run_mcp_server(transport: str = "stdio") -> None:
    if transport != "stdio":
        raise ValueError("Only stdio transport is supported.")
    create_mcp_server().run(transport="stdio")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run the local agent-evidence MCP server.")
    parser.add_argument(
        "--transport",
        default="stdio",
        choices=["stdio"],
        help="MCP transport. Only stdio is supported.",
    )
    args = parser.parse_args(argv)
    try:
        run_mcp_server(transport=args.transport)
    except RuntimeError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
