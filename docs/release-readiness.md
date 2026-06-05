# Release Readiness for v0.6.0

This document records post-release status for `agent-evidence` v0.6.0 after
Review Pack V0.3 was released and post-release audited.

This is a release-state document. It records the current released state and is
not an active release authorization gate.

## Current Assessment

Status: v0.6.0 released and post-release audited after metadata, release
notes, checklist, generated metadata, install smoke, and Review Pack V0.3
smoke checks.

- GitHub Release v0.6.0: completed.
- Zenodo v0.6.0 archive: completed.
- Zenodo v0.6.0 version DOI: `10.5281/zenodo.20013667`.
- TestPyPI v0.6.0: completed.
- PyPI v0.6.0: published and latest.
- Post-release install smoke: completed.
- Review Pack V0.3 smoke: completed.
- Urgent code or packaging hotfix: not currently known.

Current package metadata version: `0.6.0`.

Current primary project DOI: `10.5281/zenodo.19334061`.

Do not invent a new DOI. The primary DOI is the Zenodo concept DOI. Exact
release citations should use the relevant version DOI after that release is
archived.

## DOI Strategy

- Primary project DOI: `10.5281/zenodo.19334061`
- Exact v0.3.0 version DOI: `10.5281/zenodo.19998176`
- Exact v0.3.1 version DOI: `10.5281/zenodo.19998690`
- Exact v0.4.0 version DOI: `10.5281/zenodo.20004271`
- Exact v0.5.0 version DOI: `10.5281/zenodo.20011103`
- Exact v0.6.0 version DOI: `10.5281/zenodo.20013667`

Use the concept DOI in `CITATION.cff`, `codemeta.json`, `README.md`, and
generated agent metadata. Use version DOIs only when citing or reproducing a
specific archived release.

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
| Review Pack V0.3 | beta, local-only/offline reviewer package | Verifies signed exports before packaging; not legal, compliance, AI Act, or DLP certification. |
| OpenAI Agents SDK tracing integration | experimental/example | Narrow exporter example, not a platform surface. |
| CrewAI | experimental/example | Example exporter surface. |
| Automaton sidecar | experimental | Read-only sidecar export; live data contract still settling. |
| AGT conversion fixture | experimental/reference | Synthetic/reference conversion fixture. |
| Pages / ADOPTERS / registry | planned/unavailable | Out of scope for v0.6.0. |

## Claims Boundary

The release must clearly state these boundaries:

- not an official FDO standard
- not a legal non-repudiation system
- not a court-grade audit system
- not a full AI governance platform
- not a hosted OpenAPI product
- not a hosted or remote MCP service
- not an MCP registry publication
- Review Pack V0.3 is local/offline reviewer packaging, not a hosted service
- Review Pack V0.3 is not compliance certification
- Review Pack V0.3 is not AI Act approval
- Review Pack V0.3 is not a legal/compliance product
- Review Pack V0.3 is not comprehensive DLP
- not an AI Act Pack

## Metadata Alignment

- `pyproject.toml`, `CITATION.cff`, `codemeta.json`,
  `docs/project-facts.md`, `agent-index.json`, and `llms-full.txt` align on
  version `0.6.0`.
- Keep the Zenodo concept DOI as primary project DOI in active citation
  metadata.
- Keep `docs/project-facts.md` as the canonical factual source for project
  name, version, DOI, callable surfaces, and claim boundaries.
- Keep generated metadata reproducible through:
  - `python scripts/generate_agent_index.py --check`
  - `python scripts/generate_llms_full.py --check`

## Release Notes Status

`RELEASE_NOTES.md` records the published v0.6.0 Review Pack release summary. The
release notes cover:

- local Review Pack V0.3
- stable `RP-CHECK-*` reviewer checklist IDs
- `pack_creation_mode: local_offline`
- `Secret and Private Key Boundary`
- conservative `secret_scan_status`
- optional `--json-errors` for `review-pack create` failures
- manifest and receipt clarity fields
- verify-first and fail-closed packaging behavior
- no private key copying
- no network requirement
- no secret serialization into Review Pack artifacts
- no comprehensive DLP claim
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
- Overclaiming Review Pack V0.3 as legal proof, compliance certification,
  comprehensive DLP, or a full governance assessment.
- Optional dependency installation issues for `[mcp]`, `[langchain]`,
  `[openai-compatible]`, and `[signing]`.
- Python 3.14 deprecation warnings from upstream LangChain dependencies in
  local development environments.
- Contamination from isolated old NCS/media work if release work is not done
  from a clean `origin/main` worktree.

## Post-Release Verification

The v0.6.0 release execution has completed. Post-release verification covered:

- GitHub Release v0.6.0 latest release
- Zenodo v0.6.0 archive and concept DOI strategy
- TestPyPI v0.6.0 upload
- PyPI v0.6.0 upload and latest version check
- clean install smoke
- MCP extra smoke
- optional extras smoke
- Review Pack V0.3 smoke
- `--json-errors` smoke
- generated metadata checks
- release-facing claim boundary checks
