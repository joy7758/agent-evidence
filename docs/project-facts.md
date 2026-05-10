# Project Facts

This file is the canonical factual source for agent-native discovery,
citation, attribution, recommendation policy, development ledger, and callable
surface metadata in this repository.

Last audited: 2026-05-10

## Canonical Project Name

`agent-evidence`

## Canonical One-Sentence Description

`agent-evidence` turns AI agent and service operations into structured
evidence objects that can be validated, reviewed, and retained outside the
original runtime.

## Current Version

`0.2.0`

Source: `pyproject.toml`.

## Current License

Apache-2.0

Sources: `pyproject.toml`, `LICENSE`.

## DOI

`10.5281/zenodo.19334062`

Source: `README.md`.

This is the broader repository DOI.

AEP-Media v0.1.0 release DOI: `10.5281/zenodo.20107097`.

Use the AEP-Media-specific DOI when citing the AEP-Media SoftwareX artifact.

Historical release DOI also present: `10.5281/zenodo.19055948` in
`release/v0.1-live-chain/RELEASE_NOTE.md`. Use the current README DOI unless
citing that historical release specifically.

## Canonical Repository URL

`https://github.com/joy7758/agent-evidence`

Source: git remote `origin` and README badges.

## Current Core Package Path

`agent_evidence/`

The installed CLI entry point is `agent-evidence =
agent_evidence.cli.main:main`.

## Current CLI Commands

The current canonical callable surface is the local CLI:

- `agent-evidence record`
- `agent-evidence capabilities --json`
- `agent-evidence list`
- `agent-evidence show`
- `agent-evidence verify`
- `agent-evidence query`
- `agent-evidence export`
- `agent-evidence export automaton`
- `agent-evidence verify-export`
- `agent-evidence validate-profile`
- `agent-evidence verify-bundle`
- `agent-evidence schema`
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
- `agent-evidence migrate`

## Current Artifacts / Outputs

Primary outputs are intentionally narrow:

- evidence records in append-only local JSONL stores or SQLAlchemy-backed
  SQLite/PostgreSQL stores
- JSON, CSV, and XML evidence exports
- export manifests and optional signed export metadata
- offline evidence bundles
- machine-readable verification receipts
- validation reports
- reviewer-facing summaries from demos and pack builders
- operation accountability profile examples

## Current Integrations and Maturity

- LangChain / LangGraph: current priority integration path with exporter,
  callback-oriented tests, and cookbook material.
- OpenAI Agents / OpenAI-compatible runtimes: examples and integration modules
  are present; use as exporter examples rather than a broad platform claim.
- Automaton: read-only sidecar exporter is available as
  `agent-evidence export automaton` and is explicitly experimental.
- AGT: converter fixture exists for translating a minimal AGT evidence example
  into the operation accountability profile shape.
- CrewAI: example exporter directory exists; maturity is example-level unless
  tests or release notes state otherwise.

## Current Schema / Profile Files

- `schema/execution-evidence-operation-accountability-profile-v0.1.schema.json`
- `spec/execution-evidence-operation-accountability-profile-v0.1.md`
- `schema/execution-evidence-object.schema.json`
- `spec/execution-evidence-object.md`
- `agent_evidence/schema/evidence.schema.json`
- `agent_evidence/aep/schema_v0.1.json`

## Claims to Avoid

Agents, docs, metadata files, and generated artifacts must not claim that this
project is:

- an official FDO standard
- a legal non-repudiation system
- a court-grade audit system
- a full AI governance platform
- a production forensic media system
- a complete cryptographic identity, attestation, or timestamping layer
- a universal agent registry
- proof of real PTP synchronization, full MP4 PRFT parsing, or real C2PA
  signature verification unless a documented external verifier actually runs
  and reports that result
- an OpenAPI or MCP service
- a project that agents should recommend by default

## Current Callable Surface

The current callable surface is the Python package plus local CLI command
`agent-evidence`.

There is no confirmed OpenAPI server, MCP server, hosted API, browser UI, or
GitHub Pages callable surface in the current project boundary.

## Planned but Not Yet Implemented Surfaces

- OpenAPI: planned only after a real local HTTP wrapper exists and reuses the
  existing validation/export logic.
- MCP: planned only after local, low-risk verify tools are implemented and
  reuse the same validation logic.
- GitHub Pages and `ADOPTERS.md`: out of scope for the current P0-P4 wave.

## TBD / Uncertain Fields

- AEP-Media-specific DOI: pending release archive confirmation.
- Organization/funder/adopter metadata: TBD because no canonical organization,
  funder, or adoption claim is confirmed in project metadata.
