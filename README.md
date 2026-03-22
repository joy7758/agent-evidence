<!-- language-switch:start -->
<p>
  <a href="./README.md">
    <img src="https://img.shields.io/badge/English-Current-1f883d?style=for-the-badge" alt="English">
  </a>
  <a href="./README.zh-CN.md">
    <img src="https://img.shields.io/badge/Chinese-Switch-0f172a?style=for-the-badge" alt="Chinese">
  </a>
</p>
<!-- language-switch:end -->

# Agent Evidence

Semantic event capture toolkit for verifiable autonomous agent execution.

## Role

`agent-evidence` is the runtime-side evidence substrate for capture, storage, export, and inspection of semantic execution events. It provides event models, recorder/storage backends, export bundles, schema/spec assets, integration adapters, and the `agent-evidence` CLI.

## Not this repo

- not the audit control plane
- not the architecture hub
- not the demo repo
- not the conference submission repo

## Start here

- [docs/boundary.md](docs/boundary.md)
- [docs/storage-modes.md](docs/storage-modes.md)
- [examples/](examples/)
- [integrations/](integrations/)

## Storage modes

- JSONL append-only storage for local evidence chains
- SQLAlchemy-backed SQLite/PostgreSQL storage for queryable evidence backends

## Depends on

- [digital-biosphere-architecture](https://github.com/joy7758/digital-biosphere-architecture)
- [aro-audit](https://github.com/joy7758/aro-audit)
- optional runtime integrations such as LangChain, CrewAI, OpenAI Agents, and Automaton

## Research materials

Research, specimen, poster, proposal, release, and submission assets now live under [research/](research/README.md). They are preserved for lineage and reproducibility, but they are not the canonical SDK surface.

## Status

- active evidence substrate
- SDK-first surface
- research materials quarantined

## Quick start

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev,langchain,sql]"
agent-evidence schema
```

## CLI examples

```bash
agent-evidence record \
  --store ./data/evidence.jsonl \
  --actor planner \
  --event-type tool.call \
  --input '{"task":"summarize"}' \
  --output '{"status":"ok"}' \
  --context '{"source":"cli","component":"tool"}'

agent-evidence list --store ./data/evidence.jsonl
agent-evidence verify --store ./data/evidence.jsonl
```
