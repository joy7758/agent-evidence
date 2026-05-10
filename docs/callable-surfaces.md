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
boundaries, and planned but unavailable surfaces.

## CLI Boundary

The CLI calls the repository's existing validation, export, storage, bundle,
and pack-building logic. New wrappers should reuse these same implementation
paths instead of duplicating validation logic.

## AEP-Media CLI Surface

Mission 018 registered the AEP-Media commands that back the SoftwareX
reproducibility path:

- `agent-evidence validate-media-profile`
- `agent-evidence build-media-bundle`
- `agent-evidence verify-media-bundle`
- `agent-evidence validate-media-time-profile`
- `agent-evidence ingest-linuxptp-trace`
- `agent-evidence ingest-ffmpeg-prft`
- `agent-evidence ingest-c2pa-manifest`
- `agent-evidence run-media-evaluation`
- `agent-evidence build-aep-media-release-pack`
- `agent-evidence build-aep-media-submission-pack`
- `agent-evidence build-aep-media-ieee-word-pack`
- `agent-evidence build-aep-media-high-revision-pack`

These commands call existing AEP-Media modules. They do not add real PTP proof,
full MP4 PRFT parsing, real C2PA signature verification, legal admissibility,
non-repudiation, trusted timestamping, production deployment, or chain of
custody.

## OpenAPI Status

OpenAPI is planned only after a real local HTTP wrapper exists.

Until then:

- do not claim OpenAPI availability
- do not generate OpenAPI metadata from docs alone
- do not duplicate validator or export semantics in an HTTP layer
- do not treat README examples as an HTTP contract

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
- OpenAPI server
- MCP server
- browser UI
- GitHub Pages callable documentation site
- automated reputation mechanics
