# Release Notes

## v0.3.1 Metadata-Only Patch Prep

This metadata-only patch prepares `agent-evidence` v0.3.1 after GitHub Release
v0.3.0 was archived by Zenodo.

### Changed

- Primary project citation now uses the Zenodo concept DOI:
  `10.5281/zenodo.19334061`.
- The exact v0.3.0 version DOI is documented for release-specific citation:
  `10.5281/zenodo.19998176`.
- Release metadata, citation guidance, generated agent metadata, and release
  readiness docs are aligned on version `0.3.1`.

### Scope

- Metadata-only patch.
- No code behavior changes.
- No OpenAPI, MCP, schema, or core validation changes.
- No PyPI/TestPyPI release was made for `0.3.0`.

## v0.3.0 Release Prep

This release-prep entry summarizes the agent-native discovery and local
callable-surface work merged after v0.2.0. This file prepares the repository
for a v0.3.0 release; it does not publish the release by itself.

### Added

- Agent-native discovery surfaces:
  - `AGENTS.md`
  - `llms.txt`
  - `llms-full.txt`
  - `agent-index.json`
  - `agent-index.schema.json`
  - `docs/for-agents.md`
- Citation, attribution, and recommendation-policy metadata:
  - `CITATION.cff`
  - `codemeta.json`
  - `ATTRIBUTION.md`
  - `RECOMMENDATION_POLICY.md`
  - `docs/how-to-cite.md`
- Development ledger and metadata validation workflow.
- `agent-evidence capabilities --json` for machine-readable callable-surface
  metadata.
- Generated agent metadata checks for `agent-index.json` and `llms-full.txt`.
- Local OpenAPI thin wrapper:
  - `openapi.yaml`
  - `agent-evidence serve --host 127.0.0.1 --port 8765`
  - local endpoints for health, capabilities, profile validation, and bundle
    verification.
- Local MCP stdio read-only / verify-first wrapper:
  - `agent-evidence mcp --transport stdio`
  - fixed tools: `list_capabilities`, `list_schemas`, `validate_profile`,
    `verify_bundle`
  - fixed read-only resources under `agent-evidence://`.
- LangChain 5-minute runnable path with offline/mock behavior and
  `verify-export` coverage.
- OpenAI-compatible minimal evidence path with mock/offline default behavior.
- OpenAI-compatible hardening tests for live configuration errors,
  no-network mock behavior, and no provider-secret leakage into artifacts.

### Safety Boundaries

- No telemetry is added.
- No automatic star, follow, fork, recommendation, or promotion mechanism is added.
- No legal non-repudiation, court-grade proof, or regulatory certification
  claim is made.
- `agent-evidence` is not a full AI governance platform.
- The CLI/core remains canonical; local OpenAPI and MCP surfaces are wrappers.
- OpenAPI is local-only and is not a hosted API product.
- MCP is local stdio only and is not a remote or registry-published service.

### Non-Goals

- No remote MCP.
- No MCP registry publication.
- No GitHub Pages or `ADOPTERS.md`.
- No Review Pack commercial feature.
- No AI Act Pack.
- No canonical schema rewrite.
- No core validation rewrite.
- No old NCS/media work.

### Release Actions Still Required

- Confirm final version and release date.
- Confirm whether the existing DOI remains the concept/repository DOI or
  whether release-specific archive metadata should be added after publication.
- Create the GitHub release if approved.
- Publish to PyPI if approved.
- Confirm release notes and package metadata after publication.
