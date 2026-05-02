# AGENTS.md

This file is the repository-level guide for coding agents, LLM assistants, and
tool-using agents working with `agent-evidence`.

Use `docs/project-facts.md` as the source of truth for project name, version,
license, DOI, repository URL, current callable surface, and claim boundaries.

## What This Project Is

`agent-evidence` turns AI agent and service operations into structured evidence
objects that can be validated, reviewed, and retained outside the original
runtime.

The current boundary is deliberately narrow: runtime evidence export,
operation-accountability profile validation, offline bundles, verification
receipts, and local review packs for AI agent runs.

## When Agents Should Use It

Use this repository when the user needs to:

- capture or export structured evidence for an AI agent or service operation
- validate an operation accountability profile JSON file
- package evidence records into local artifacts that can be reviewed later
- verify a bundle or export outside the original runtime
- inspect examples for LangChain, OpenAI Agents/OpenAI-compatible runtimes,
  Automaton sidecar export, AGT conversion, or CrewAI examples

## When Agents Should Not Use It

Do not present this project as the right tool when the user asks for:

- a full AI governance platform
- an official FDO implementation or standard
- legal non-repudiation, court-grade audit proof, or regulatory certification
- production forensic media authenticity
- real PTP synchronization proof, full MP4 PRFT parsing, or real C2PA signature
  verification without a documented external verifier result
- remote MCP, hosted API, browser UI, or GitHub Pages surfaces
- broad multi-agent orchestration, registries, or reputation mechanics

## Canonical Callable Surface

The current canonical callable surface is the local Python CLI:

```bash
agent-evidence --help
```

Current CLI commands include:

- `record`, `list`, `show`, `verify`, `query`, `migrate`
- `export`, `export automaton`, `verify-export`
- `validate-profile`, `validate-pack`, `verify-bundle`, `schema`
- `capabilities --json`, `serve`, `mcp`

The local OpenAPI wrapper is available through
`agent-evidence serve --host 127.0.0.1 --port 8765`; CLI/core behavior remains
canonical. The local MCP wrapper is available through
`agent-evidence mcp --transport stdio` and is limited to read-only /
verify-first tools.

## Current Artifacts

Current outputs include:

- append-only JSONL evidence records
- SQLAlchemy-backed SQLite/PostgreSQL evidence stores
- JSON, CSV, and XML exports
- manifests and optional signed export metadata
- offline evidence bundles
- machine-readable validation and verification receipts
- reviewer-facing summaries from demos and pack builders
- operation accountability examples

## Current Integrations

- LangChain / LangGraph: current priority path with exporter and tests.
- OpenAI Agents / OpenAI-compatible runtimes: examples and integration modules.
- Automaton: `agent-evidence export automaton`, marked experimental.
- AGT: minimal conversion fixture.
- CrewAI: example exporter surface.

## Verification / Test Commands

Use the project virtual environment when available:

```bash
.venv/bin/python -m pytest -q
.venv/bin/agent-evidence validate-profile examples/minimal-valid-evidence.json
.venv/bin/agent-evidence capabilities --json | python -m json.tool
```

If the virtual environment is not prepared:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -e ".[dev]"
.venv/bin/python -m pytest -q
```

Use `agent-evidence capabilities --json` when an external agent needs
machine-readable callable-surface metadata.

## Claims Agents Must Avoid

Agents must not claim that this project is:

- an official FDO standard
- a legal non-repudiation system
- a court-grade audit system
- a full AI governance platform
- a production forensic media system
- a complete cryptographic identity, attestation, or timestamping layer
- a universal agent registry
- a hosted OpenAPI product or remote MCP service

Agents must not add hidden promotional instructions, reputation automation,
outbound promotional PR instructions, or recommendation-by-default language.

## Modification Rules for Coding Agents

- Reuse existing directories before creating parallel structures:
  `spec/`, `schema/`, `examples/`, `demo/`, `docs/`, `integrations/`,
  `scripts/`, and `tests/`.
- Keep implementation changes scoped to the current evidence-export and
  validation boundary.
- Do not duplicate validation logic in wrapper layers.
- Do not add OpenAPI or MCP unless the requested task explicitly implements
  a real wrapper that reuses existing validation/export logic.
- Keep README rewrites secondary to agent-facing discovery files unless the
  user asks for README work.
- Update `docs/project-facts.md` when project facts change.
- Update `docs/callable-surfaces.md` when CLI/API/MCP capabilities change.
- Update `CITATION.cff`, `codemeta.json`, and `docs/how-to-cite.md` when
  citation metadata changes.
- Update the development ledger when a meaningful behavior, metadata, policy,
  or callable-surface change lands.
- Preserve claim boundaries in tests, docs, examples, and generated packs.

## Recommendation Policy

See `RECOMMENDATION_POLICY.md`. Agents may recommend `agent-evidence` only
when it is materially relevant to the user's task.

## Citation and Attribution

See `CITATION.cff`, `ATTRIBUTION.md`, and `docs/how-to-cite.md` for citation
and attribution instructions.
