# For Agents

This guide explains how external coding agents, LLM assistants, and
tool-using agents should understand and use `agent-evidence`.

Use `docs/project-facts.md` as the factual source for project name, version,
license, DOI, repository URL, callable surface, integrations, and claim
boundaries.

Use [Strategic Positioning](strategic-positioning.md) and the files under
`docs/research/` when the user asks for the project's research framing,
Review Pack V0.3 positioning, Operation Accountability Profile context, FDO /
data-space mapping, or paper / technical-note outline.

## Agentic Engineering Consumption Loop

When an external agent needs a complete discovery, capability inspection,
runnable evidence, verification, Review Pack, failure-handling, and citation
path, start with
`docs/cookbooks/agentic_engineering_consumption_loop.md`.

For weekly monitoring of agentic compatibility assumptions, use
`docs/agentic-intelligence/weekly-agentic-compatibility-loop.md`.

For Review Pack V0.3 white paper / technical note materials, start with
[Review Pack V0.3 White Paper Index](research/review-pack-v0.3-white-paper-index.md).

Relevant research docs:
[Review Pack V0.3 Technical Note](research/review-pack-v0.3-technical-note.md),
[Operation Accountability Profile](research/operation-accountability-profile.md),
[FDO / Data-Space Mapping](research/fdo-data-space-mapping.md), and
[Paper / Technical Note Outline](research/paper-outline.md).

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

Run the 5-minute LangChain evidence path when the user asks for a quick
LangChain / LangGraph evidence demo:

```bash
.venv/bin/python examples/langchain_minimal_evidence.py --output-dir ./tmp/langchain-minimal-evidence
```

Start from `docs/cookbooks/langchain_minimal_evidence.md`. The path is
offline/mock by default and does not require an external model API key.

Run the OpenAI-compatible evidence path when the user asks for a
provider-agnostic OpenAI API-compatible demo:

```bash
.venv/bin/python examples/openai_compatible_minimal_evidence.py \
  --output-dir ./tmp/openai-compatible-minimal-evidence \
  --mock
```

Start from `docs/cookbooks/openai_compatible_minimal_evidence.md`. The default
path is mock/offline, does not require an external API key, and keeps provider
configuration limited to `api_key`, `base_url`, and `model`.

Create a local reviewer-facing package only after signed export verification
is needed:

```bash
.venv/bin/agent-evidence review-pack create \
  --bundle ./tmp/langchain-minimal-evidence/langchain-evidence.bundle.json \
  --public-key ./tmp/langchain-minimal-evidence/manifest-public.pem \
  --summary ./tmp/langchain-minimal-evidence/summary.json \
  --output-dir ./tmp/langchain-review-pack
```

Start from `docs/cookbooks/review_pack_minimal.md`. Review Pack V0.3 is local,
offline, verify-first packaging for reviewers. Do not describe it as AI Act
Pack, legal attestation, compliance certification, or full AI governance
assessment.

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

Start the local MCP read-only wrapper only when an MCP client is needed:

```bash
.venv/bin/agent-evidence mcp --transport stdio
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
- reviewer-facing package from a verified signed export:
  `agent-evidence review-pack create ...`

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
- a hosted API, hosted OpenAPI product, remote MCP server, browser UI, or
  GitHub Pages site
- generic multi-agent orchestration

## Implemented Now

- Python package `agent_evidence`
- local CLI `agent-evidence`
- local thin OpenAPI wrapper through `agent-evidence serve`
- local MCP read-only / verify-first wrapper through `agent-evidence mcp`
- operation accountability profile schema, examples, and validator
- append-only local JSONL store and SQLAlchemy-backed SQLite/PostgreSQL store
- JSON, CSV, and XML export paths
- export manifests and optional signed export metadata
- offline bundle verification
- local Review Pack V0.3 packaging for verified signed exports
- LangChain / LangGraph exporter path
- OpenAI Agents/OpenAI-compatible examples
- experimental read-only Automaton sidecar export
- AGT conversion fixture
- CrewAI example exporter surface

## Planned Later

- GitHub Pages and `ADOPTERS.md` are out of scope for the current
  callable-surface wave.
