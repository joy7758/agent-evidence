# Callable Surfaces

This document records which `agent-evidence` surfaces are implemented and which
are planned but unavailable.

## Current Canonical Surface

The local CLI is the current canonical callable surface:

```bash
agent-evidence --help
agent-evidence capabilities --json
```

Use `agent-evidence capabilities --json` when an external agent needs
machine-readable metadata about implemented commands, artifact types,
integrations, citation files, attribution files, recommendation policy, claim
boundaries, local callable wrappers, and planned but unavailable surfaces.

## CLI Boundary

The CLI calls the repository's existing validation, export, storage, bundle,
and pack-building logic. New wrappers should reuse these same implementation
paths instead of duplicating validation logic.

## OpenAPI Status

`openapi.yaml` now describes a local thin HTTP wrapper over existing CLI/core
behavior.

Start it with:

```bash
agent-evidence serve --host 127.0.0.1 --port 8765
```

Implemented endpoints:

- `GET /healthz`
- `GET /v1/capabilities`
- `POST /v1/profiles/validate`
- `POST /v1/bundles/verify`

The wrapper:

- keeps CLI/core behavior canonical
- calls `agent_evidence.cli.main.build_capabilities_payload()`
- calls existing profile validation behavior for validate requests
- calls `agent_evidence.aep.verify_bundle()` for bundle verification
- does not add Review Pack endpoints
- does not introduce new evidence semantics

## MCP Status

MCP is planned only after local, low-risk verify tools are implemented.

Until then:

- do not claim MCP availability
- do not expose write-heavy tools as a first MCP surface
- do not duplicate validation logic in MCP handlers
- do not add promotion, star, follow, fork, or outbound promotion tools

## Wrapper Rules

Any future callable wrapper must:

- reuse existing validation/export logic
- preserve `docs/project-facts.md` claim boundaries
- keep evidence-export scope narrow
- return machine-readable receipts for validation or verification
- update `AGENTS.md`, `llms.txt`, this file, and
  `agent-evidence capabilities --json`
- update tests for changed callable behavior

## Explicit Non-Surfaces

The current repository does not provide:

- hosted API
- MCP server
- browser UI
- GitHub Pages callable documentation site
- automated reputation mechanics
