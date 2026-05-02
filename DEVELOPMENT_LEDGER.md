# Development Ledger

This ledger records meaningful project changes that affect humans or agents
trying to understand, cite, validate, or call `agent-evidence`.

It is not a typo log. Record changes when they alter behavior, callable
surfaces, metadata, policies, artifact semantics, validation expectations, or
agent-facing discovery.

## Current Focus

The current wave adds agent-native discovery, citation, attribution,
recommendation policy, development-ledger discipline, metadata validation,
structured CLI capabilities metadata, integration terminology alignment, and
generated agent metadata surfaces.

## What Changes Should Be Recorded

- CLI, API, MCP, or other callable-surface changes
- schema, profile, validator, or evidence-integrity changes
- citation, attribution, DOI, license, version, or repository metadata changes
- recommendation, promotion, or claim-boundary policy changes
- agent-facing discovery changes in `AGENTS.md`, `llms.txt`, or docs
- meaningful integration maturity changes
- release, archival, or reproducibility evidence changes

## Ledger

| Date | Change ID | Area | Summary | Agent-Facing Impact | Verification | Evidence Integrity Impact | Next Action |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 2026-05-03 | agent-native-p0-project-facts | discovery | Added `docs/project-facts.md` as the canonical source for project facts. | Agents have one source for name, version, DOI, license, repository, CLI, integrations, and boundaries. | Metadata and tests checked in this PR wave. | Reduces drift between docs and callable metadata. | Keep this file updated when project facts change. |
| 2026-05-03 | agent-native-p1-discovery | discovery | Added agent-facing discovery guidance in `AGENTS.md`, `llms.txt`, and `docs/for-agents.md`. | External agents can decide when to use or avoid the project. | `pytest -q` and metadata validation in this PR wave. | Improves correct use of validation and export boundaries. | Keep discovery docs aligned with `docs/project-facts.md`. |
| 2026-05-03 | agent-native-p2-citation-attribution | metadata | Added citation, CodeMeta, attribution, and recommendation policy files. | Agents can cite and attribute the project without inventing metadata or promotion mechanics. | CFF/YAML and JSON parsing checks. | Makes derived work attribution auditable and explicit. | Update citation metadata when DOI, version, or author metadata changes. |
| 2026-05-03 | agent-native-p3-ledger-ci | governance | Added development ledger, PR template, and metadata validation CI. | Agents and reviewers get machine-checkable discovery and policy invariants. | Local metadata script and GitHub Actions workflow. | Preserves metadata integrity and claim boundaries. | Extend checks when callable surfaces change. |
| 2026-05-03 | agent-native-p4-cli-capabilities | callable-surface | Add structured `agent-evidence capabilities --json` output and callable-surface docs. | Agents can inspect current capabilities without scraping README prose. | `agent-evidence capabilities --json \| python -m json.tool` and `pytest -q`. | Keeps wrappers and external agents aligned with implemented surfaces. | Keep OpenAPI and MCP marked unavailable until real wrappers exist. |
| 2026-05-03 | p5-integration-terminology-normalization | integrations | Normalized LangChain, OpenAI Agents, and CrewAI integration terminology around the agent-native discovery layer. | Agents reading integration docs see the same runtime evidence exporter boundary as `AGENTS.md` and `llms.txt`. | `pytest -q`, targeted integration terminology checks, `agent-evidence capabilities --json \| python -m json.tool`, and ruff. | Reduces drift between example integrations and canonical evidence/export boundaries. | Keep integration docs aligned when maturity or callable surfaces change. |
| 2026-05-03 | p6-generated-agent-metadata | metadata | Added generated `agent-index.json`, `llms-full.txt`, schema, generation scripts, and drift tests. | Agents get deterministic machine-readable and expanded LLM-readable metadata derived from existing project facts and capabilities. | `pytest -q`, generation `--check` commands, schema validation, metadata validation, capabilities JSON parsing, and ruff. | Reduces metadata drift across project facts, citation metadata, policy files, and callable-surface metadata. | Keep generated metadata checked whenever facts, policy, citation, or callable surfaces change. |
| 2026-05-03 | p7-lite-local-openapi-wrapper | callable-surface | Added a stdlib local OpenAPI wrapper with `agent-evidence serve`, health, capabilities, profile validation, and bundle verification endpoints. | Agents can call a local HTTP wrapper while CLI/core behavior remains canonical. | `pytest -q`, `agent-evidence capabilities --json \| python -m json.tool`, generation `--check` commands, OpenAPI contract tests, local API tests, and ruff. | Keeps callable HTTP access aligned with existing validation and verification logic without changing evidence semantics. | MCP remains unavailable; no telemetry, auth system, hosted mode, or Review Pack endpoint was added. |
