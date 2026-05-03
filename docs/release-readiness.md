# Release Readiness for v0.3.0

This document records release-prep status for `agent-evidence` v0.3.0 after
the P0-P11 agent-native discovery, local callable surface, LangChain, and
OpenAI-compatible work.

This is a release-prep document. It does not publish a release.

## Current Assessment

Recommendation: go for a v0.3.0 release-prep PR; no-go for final publication
until the maintainer confirms DOI handling, GitHub release metadata, and PyPI
publication intent.

Current package metadata target: `0.3.0`.

Current DOI: `10.5281/zenodo.19334062`.

Do not invent a new DOI. During release execution, confirm whether the current
DOI should remain the concept/repository DOI or whether release-specific
archive metadata should be added after publication.

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
| OpenAI Agents SDK tracing integration | experimental/example | Narrow exporter example, not a platform surface. |
| CrewAI | experimental/example | Example exporter surface. |
| Automaton sidecar | experimental | Read-only sidecar export; live data contract still settling. |
| AGT conversion fixture | experimental/reference | Synthetic/reference conversion fixture. |
| Pages / ADOPTERS / registry | planned/unavailable | Out of scope for v0.3.0 release prep. |

## Claims Boundary

The release must clearly state these boundaries:

- not an official FDO standard
- not a legal non-repudiation system
- not a court-grade audit system
- not a full AI governance platform
- not a hosted OpenAPI product
- not a hosted or remote MCP service
- not an MCP registry publication
- not a Review Pack commercial feature
- not an AI Act Pack

## Metadata Alignment Plan

- Keep `pyproject.toml`, `CITATION.cff`, `codemeta.json`,
  `docs/project-facts.md`, `agent-index.json`, and `llms-full.txt` aligned on
  version `0.3.0`.
- Keep the existing DOI until release execution confirms archive metadata.
- Keep `docs/project-facts.md` as the canonical factual source for project
  name, version, DOI, callable surfaces, and claim boundaries.
- Keep generated metadata reproducible through:
  - `python scripts/generate_agent_index.py --check`
  - `python scripts/generate_llms_full.py --check`

## Release Notes Outline

Use `RELEASE_NOTES.md` for the v0.3.0 release-prep summary. The final release
notes should cover:

- agent-native discovery metadata
- citation, attribution, and recommendation policy
- development ledger and metadata validation
- `capabilities --json`
- generated `agent-index.json` and `llms-full.txt`
- local OpenAPI thin wrapper
- local MCP stdio read-only / verify-first wrapper
- LangChain 5-minute runnable path
- OpenAI-compatible minimal path and hardening
- safety boundaries and non-goals

## Release Risks

- Version drift between package metadata, citation metadata, generated
  metadata, and docs.
- DOI drift if a release-specific archive DOI is created after publication.
- Overclaiming beta or experimental surfaces as supported.
- Optional dependency installation issues for `[mcp]`, `[langchain]`,
  `[openai-compatible]`, and `[signing]`.
- Python 3.14 deprecation warnings from upstream LangChain dependencies in
  local development environments.
- Contamination from isolated old NCS/media work if release work is not done
  from a clean `origin/main` worktree.

## Release Go / No-Go

Go for v0.3.0 release-prep implementation when:

- metadata versions are aligned
- release notes exist
- surface statuses are explicit
- generated metadata checks pass
- release checklist exists
- stale callable-surface statements are fixed

No-go for final release publication until:

- DOI handling is confirmed
- GitHub release body is finalized
- PyPI publication intent is confirmed
- release smoke tests have run from a clean checkout
