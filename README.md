<!-- language-switch:start -->
[English](./README.md) | [中文](./README.zh-CN.md)
<!-- language-switch:end -->

# agent-evidence

`agent-evidence` turns an AI agent run into a portable evidence package.

## What You Get

After one run, the primary outputs are:

- `bundle` — the exported evidence package you can hand off, verify, and retain outside the original runtime.
- `receipt` — the machine-readable verification result returned by `agent-evidence validate-profile`, `agent-evidence verify-bundle`, or `agent-evidence verify-export`.
- `summary` — the reviewer-facing summary output produced by the current demo and example surfaces.

This repository keeps the output surface intentionally narrow: `bundle`, `receipt`, and `summary`.

## Install

For the current LangChain-first path:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[langchain,signing]"
```

For local development in this repository:

```bash
pip install -e ".[dev]"
```

## Minimal Run Path

The first-run flow in this repository is organized around:

1. install
2. run one minimal example
3. export a `bundle`
4. verify the `bundle` to produce a `receipt`
5. review the generated `summary`

Current entry surfaces for this flow:

- [demo/README.md](./demo/README.md)
- [examples/README.md](./examples/README.md)
- [docs/cookbooks/langchain_minimal_evidence.md](./docs/cookbooks/langchain_minimal_evidence.md)

## Why This Is Different From Ordinary Traces

Ordinary traces help you inspect a run inside the system that produced it.

`agent-evidence` is for teams that need the run to leave behind a portable artifact boundary:

- a `bundle` that can be exported and moved
- a `receipt` that records what verified and what failed
- a `summary` that another engineer or reviewer can read without replaying the original runtime

The current verification surface is bounded and local-first. This repository does not claim a hosted tracing plane, a full audit plane, or a generic governance platform.

## Integration Priorities

Current priority order:

1. LangChain / LangGraph
2. OpenAI-compatible runtimes

The goal is one narrow evidence handoff surface, not many adapters at once.

## Related Surfaces

- Architecture: [digital-biosphere-architecture](https://github.com/joy7758/digital-biosphere-architecture)
- Demo: [verifiable-agent-demo](https://github.com/joy7758/verifiable-agent-demo)
- Audit: [aro-audit](https://github.com/joy7758/aro-audit)
- EDC spike: [frozen/reference asset](https://github.com/joy7758/agent-evidence/blob/main/docs/edc-java-spike/README.md)

## Scope Boundaries

`agent-evidence` is the active code surface here for `bundle`, `receipt`, and `summary`.

It is not:

- the full Digital Biosphere Architecture stack
- the audit control plane
- the current EDC implementation line
- an exporter proliferation project
- a generic agent governance platform

Historical proposal, submission, poster, roadmap, and lineage materials remain in this repository for context, not as the primary developer entry path.

## Status

The current primary package line in this repository is `Execution Evidence and Operation Accountability Profile v0.1`.

This repository is being tightened into a developer-product entry page:

- installable from source
- runnable on a minimal path
- able to produce `bundle`, `receipt`, and `summary`
- explicit about active versus frozen/reference surfaces

For the current repo boundary, see [docs/reports/repo-map-audit.md](./docs/reports/repo-map-audit.md).
