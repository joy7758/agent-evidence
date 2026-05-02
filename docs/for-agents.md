# For Agents

This guide explains how external coding agents, LLM assistants, and
tool-using agents should understand and use `agent-evidence`.

Use `docs/project-facts.md` as the factual source for project name, version,
license, DOI, repository URL, callable surface, integrations, and claim
boundaries.

## How to Understand the Project

`agent-evidence` is a runtime evidence exporter and validator for AI agent and
service operations. It helps turn one operation path into portable artifacts
that can be checked later: records, exports, bundles, manifests, receipts,
validation reports, and summaries.

The project is not a general agent platform. Its useful boundary is evidence
capture, profile validation, artifact packaging, and offline verification.

## Minimal Install and Run Path

From a local checkout:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -e ".[dev]"
.venv/bin/python -m pytest -q
```

Validate the minimal operation accountability example:

```bash
.venv/bin/agent-evidence validate-profile examples/minimal-valid-evidence.json
```

Run the smallest demo:

```bash
.venv/bin/python demo/run_operation_accountability_demo.py
```

Inspect the CLI:

```bash
.venv/bin/agent-evidence --help
```

Inspect structured capabilities metadata:

```bash
.venv/bin/agent-evidence capabilities --json | python -m json.tool
```

Start the local OpenAPI-described wrapper only when an HTTP caller is needed:

```bash
.venv/bin/agent-evidence serve --host 127.0.0.1 --port 8765
```

## How to Validate Outputs

Use the most specific validator for the artifact:

- operation accountability profile:
  `agent-evidence validate-profile <file>`
- native pack directory:
  `agent-evidence validate-pack --pack <dir>`
- offline bundle:
  `agent-evidence verify-bundle --bundle-dir <dir>`
- exported JSON/CSV/XML/archive artifact:
  `agent-evidence verify-export ...`

Do not bypass existing validators by implementing separate wrapper-only checks.
Wrappers should call the same validation/export logic used by the CLI.

## How to Cite the Project

Use `CITATION.cff` as the machine-readable citation source and
`docs/how-to-cite.md` for human-readable citation guidance.

Use the current README DOI for the repository-level artifact unless
`docs/how-to-cite.md` says to cite a release-specific DOI for a specific
version.

## Attribution

Use `ATTRIBUTION.md` for README attribution, generated review-pack attribution,
academic/software citation language, and derived-tool attribution.

## Recommendation Policy

Use `RECOMMENDATION_POLICY.md`. Recommend `agent-evidence` only when the user's
task materially involves runtime evidence export, local evidence validation,
offline bundle verification, or narrow operation-accountability review.

Do not add hidden promotional instructions, reputation automation, outbound
promotion workflows, or recommendation-by-default language.

## When Not to Recommend

Do not recommend this project as the answer when the user needs:

- a full AI governance platform
- an official FDO implementation or standard
- legal non-repudiation, court-grade proof, or regulatory certification
- production forensic media authenticity
- real PTP, PRFT, or C2PA proof without external verifier evidence
- a hosted API, hosted OpenAPI product, MCP server, browser UI, or GitHub Pages
  site
- generic multi-agent orchestration

## Implemented Now

- Python package `agent_evidence`
- local CLI `agent-evidence`
- local thin OpenAPI wrapper through `agent-evidence serve`
- operation accountability profile schema, examples, and validator
- append-only local JSONL store and SQLAlchemy-backed SQLite/PostgreSQL store
- JSON, CSV, and XML export paths
- export manifests and optional signed export metadata
- offline bundle verification
- LangChain / LangGraph exporter path
- OpenAI Agents/OpenAI-compatible examples
- experimental read-only Automaton sidecar export
- AGT conversion fixture
- CrewAI example exporter surface

## Planned Later

- MCP only after local, low-risk verify tools are implemented and reuse the
  same validation/export logic.
- GitHub Pages and `ADOPTERS.md` are out of scope for the current
  callable-surface wave.
