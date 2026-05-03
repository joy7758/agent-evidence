# Release Readiness for v0.4.0

This document records release-prep status for `agent-evidence` v0.4.0 after
Review Pack V0.1 was merged.

This is a release-prep document. It does not publish a release.

## Current Assessment

Recommendation: go for a v0.4.0 release-prep PR; no-go for final GitHub,
TestPyPI, or PyPI publication until release authorization is explicit.

Current package metadata target: `0.4.0`.

Current primary project DOI: `10.5281/zenodo.19334061`.

Do not invent a new DOI. The primary DOI is the Zenodo concept DOI. Exact
release citations should use the relevant version DOI.

## DOI Strategy

- Primary project DOI: `10.5281/zenodo.19334061`
- Exact v0.3.0 version DOI: `10.5281/zenodo.19998176`
- Exact v0.3.1 version DOI: `10.5281/zenodo.19998690`

Use the concept DOI in `CITATION.cff`, `codemeta.json`, `README.md`, and
generated agent metadata. Use version DOIs only when citing or reproducing a
specific archived release. Confirm Zenodo behavior after a v0.4.0 GitHub
release before deciding whether any follow-up DOI metadata patch is needed.

## Surface Status

| Surface | Status | Release boundary |
|---|---|---|
| CLI/core | supported | Canonical implementation and callable surface. |
| `capabilities --json` | supported | Machine-readable project and callable-surface metadata. |
| `agent-index.json` / `llms-full.txt` | supported metadata surface | Generated agent-readable metadata, checked for drift. |
| local OpenAPI wrapper | beta, local-only | Thin wrapper over CLI/core; not a hosted API product. |
| local MCP stdio tools | beta, local-only/read-only | Stdio, fixed tools/resources, no remote registry publication. |
| LangChain 5-minute path | supported developer path | Offline/mock runnable path with bundle verification. |
| OpenAI-compatible minimal path | beta developer path | Provider-agnostic mock/offline default path with hardening tests. |
| Review Pack V0.1 | beta, local-only/offline reviewer package | Verifies signed exports before packaging; not legal or compliance certification. |
| OpenAI Agents SDK tracing integration | experimental/example | Narrow exporter example, not a platform surface. |
| CrewAI | experimental/example | Example exporter surface. |
| Automaton sidecar | experimental | Read-only sidecar export; live data contract still settling. |
| AGT conversion fixture | experimental/reference | Synthetic/reference conversion fixture. |
| Pages / ADOPTERS / registry | planned/unavailable | Out of scope for v0.4.0 release prep. |

## Claims Boundary

The release must clearly state these boundaries:

- not an official FDO standard
- not a legal non-repudiation system
- not a court-grade audit system
- not a full AI governance platform
- not a hosted OpenAPI product
- not a hosted or remote MCP service
- not an MCP registry publication
- Review Pack V0.1 is local/offline reviewer packaging, not a hosted service
- Review Pack V0.1 is not compliance certification
- Review Pack V0.1 is not AI Act approval
- not an AI Act Pack

## Metadata Alignment Plan

- Keep `pyproject.toml`, `CITATION.cff`, `codemeta.json`,
  `docs/project-facts.md`, `agent-index.json`, and `llms-full.txt` aligned on
  version `0.4.0`.
- Keep the Zenodo concept DOI as primary project DOI in active citation
  metadata.
- Keep `docs/project-facts.md` as the canonical factual source for project
  name, version, DOI, callable surfaces, and claim boundaries.
- Keep generated metadata reproducible through:
  - `python scripts/generate_agent_index.py --check`
  - `python scripts/generate_llms_full.py --check`

## Release Notes Outline

Use `RELEASE_NOTES.md` for the v0.4.0 Review Pack release-prep summary. Release
notes should cover:

- local Review Pack V0.1
- verify-first and fail-closed packaging behavior
- no private key copying
- no network requirement
- no secret serialization into Review Pack artifacts
- Review Pack cookbook and tests
- agent-native discovery metadata
- local OpenAPI and MCP boundaries
- LangChain and OpenAI-compatible runnable paths
- safety boundaries and non-goals

## Release Risks

- Version drift between package metadata, citation metadata, generated
  metadata, and docs.
- DOI drift if a version DOI is used as active citation metadata for a later
  release.
- Overclaiming Review Pack V0.1 as legal proof, compliance certification, or a
  full governance assessment.
- Optional dependency installation issues for `[mcp]`, `[langchain]`,
  `[openai-compatible]`, and `[signing]`.
- Python 3.14 deprecation warnings from upstream LangChain dependencies in
  local development environments.
- Contamination from isolated old NCS/media work if release work is not done
  from a clean `origin/main` worktree.

## Release Go / No-Go

Go for v0.4.0 release-prep implementation when:

- metadata versions are aligned
- release notes exist
- Review Pack status is explicit
- generated metadata checks pass
- release checklist includes Review Pack smoke
- stale callable-surface statements remain fixed

No-go for final release publication until:

- GitHub release body is finalized
- PyPI publication intent is confirmed
- TestPyPI credentials are ready if TestPyPI is used
- release smoke tests have run from a clean checkout
- Zenodo DOI handling is confirmed after GitHub release
