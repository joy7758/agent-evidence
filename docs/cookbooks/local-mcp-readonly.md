# Local MCP Read-Only Tools

The local MCP server exposes a narrow read-only / verify-first wrapper for
agents that use Model Context Protocol clients. CLI/core behavior remains
canonical; MCP delegates to existing capability, validation, and verification
logic.

## Install MCP Support

From a local checkout:

```bash
pip install -e ".[mcp]"
```

For development and tests:

```bash
pip install -e ".[dev,mcp]"
```

## Run

```bash
agent-evidence mcp --transport stdio
```

Equivalent module entrypoint:

```bash
python -m agent_evidence.mcp.server --transport stdio
```

Only stdio transport is supported in this phase.

## Tools

- `list_capabilities`
- `list_schemas`
- `validate_profile`
- `verify_bundle`

## Resources

- `agent-evidence://capabilities`
- `agent-evidence://schema/agent-index`
- `agent-evidence://schema/openapi`
- `agent-evidence://docs/for-agents`
- `agent-evidence://docs/callable-surfaces`
- `agent-evidence://citation`
- `agent-evidence://recommendation-policy`

Resources are fixed and read-only. They do not provide dynamic filesystem
browsing.

## Limitations

- No prompts in P8.
- No Review Pack tools.
- No telemetry.
- No remote mode.
- No registry publication.
- No GitHub star, follow, fork, or write tools.
- No shell tools.
- No sign or upload tools.
- No schema or core validation changes.
