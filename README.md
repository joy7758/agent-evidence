# agent-evidence

把 AI Agent / service operation 转换为可验证、可审计、可复核的 evidence object。<br>
Turn AI agent operations into auditable and verifiable evidence objects.

## Why this matters

普通 AI workflow 通常只留下聊天记录、trace 页面或零散日志。它们能帮助开发者排查问题，但很难直接交给审查者、客户、治理团队或后续系统复核。

`agent-evidence` 关注的是一次 Agent / service operation 结束之后，能不能留下结构化证据：input / output hashes、operation type、policy reference、provenance chain、verification result，以及可以被 validator 检查的 evidence object。

这个仓库的目标不是再做一个通用 Agent 平台，而是提供一个最小、可运行、可验证的 operation evidence 路径。

## What it provides

- `FDO_OPERATION_EVIDENCE_PROFILE_V0_1`
- JSON Schema
- profile-aware validator
- minimal valid / invalid examples
- registration pack
- FDO Testbed registration draft
- outreach draft for FDO discussion
- LangChain / LangGraph 优先的 evidence handoff 思路

## Quick Start

Install from source:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev,langchain,signing]"
```

Validate a minimal valid evidence profile:

```bash
agent-evidence validate-profile examples/minimal-valid-evidence.json
```

Check that an intentionally invalid example fails:

```bash
agent-evidence validate-profile examples/invalid-missing-required.json
```

The console command is provided by the package entry point after `pip install -e ...`.

## Example Evidence Fields

- `operation_id` — one operation or run that needs to be reviewed
- `operation_type` — what kind of operation was performed
- `input_hashes` — hashes for inputs or source artifacts
- `output_hashes` — hashes for generated outputs
- `policy_reference` — policy, rule, or governance checkpoint used during the run
- `provenance_chain` — links between inputs, actions, outputs, and evidence
- `verification_result` — machine-readable result from profile validation or bundle verification

## Demo Screenshots

Real screenshots are intentionally not generated in this README. Add them under:

- `assets/profile-validator.png`
- `assets/evidence-object.png`
- `assets/fdo-testbed-registration.png`

See [assets/README.md](./assets/README.md) for the capture checklist.

## Relation to FDO

`agent-evidence` is an experimental, minimal, discussion-oriented operation evidence profile. It explores how AI / Agent operation evidence can be expressed with an FDO-style profile, schema, examples, validator, and registration pack.

It is not an official FDO standard. The current public claim is narrower: this repository provides a working profile and validator surface that can support FDO-facing discussion and a minimal FDO Testbed registration draft.

Start here for the FDO-facing pack:

- [FDO Operation Evidence Profile Registration Pack](./docs/fdo-mapping/fdo-operation-evidence-profile-registration-pack.md)
- [FDO Testbed registration draft](./submission/fdo-testbed-registration-draft.md)
- [FDO outreach draft](./submission/peter-sven-outreach-draft.md)
- [LDT4SSC / DS4SSCC module pitch](./submission/ldt4ssc-ds4sscc-module-pitch.md)

Current external naming relationship:

- `FDO_OPERATION_EVIDENCE_PROFILE_V0_1` = operation-level evidence profile
- `ARO_AUDIT_PROFILE_V1` = audit-facing sibling profile

## For hiring managers

This repository shows that I can:

- turn LangChain / Agent workflow thinking into a concrete evidence boundary
- design JSON Schema and validator logic for high-responsibility AI workflows
- model audit trail, provenance, hashes, and verification results as deliverable artifacts
- connect trustworthy AI governance ideas to runnable examples
- package technical work as open-source documentation, examples, and CLI validation

## Minimal Run Path

The first-run flow in this repository is organized around:

1. install
2. run or inspect one minimal example
3. validate the profile
4. export or verify an evidence bundle when needed
5. review the generated `bundle`, `receipt`, and `summary`

Current entry surfaces:

- [demo/README.md](./demo/README.md)
- [examples/README.md](./examples/README.md)
- [LangChain minimal evidence cookbook](./docs/cookbooks/langchain_minimal_evidence.md)
- [OpenAI-compatible minimal cookbook](./docs/cookbooks/openai_compatible_minimal.md)
- [Review pack minimal cookbook](./docs/cookbooks/review_pack_minimal.md)

## What You Get

After one run, the primary outputs are intentionally narrow:

- `bundle` — exported evidence package that can be handed off, verified, and retained outside the original runtime
- `receipt` — machine-readable verification result returned by `agent-evidence validate-profile`, `agent-evidence verify-bundle`, or `agent-evidence verify-export`
- `summary` — reviewer-facing summary output produced by the current demo and example surfaces

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

## English Summary

`agent-evidence` turns AI agent operations into structured evidence objects that can be validated, reviewed, and retained outside the original runtime. The project focuses on a minimal operation evidence profile, JSON Schema, validator, examples, and FDO-facing discussion material. It is experimental and discussion-oriented, not an official FDO standard.
