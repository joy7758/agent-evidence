# Codex for Open Source Maintainer Use

`agent-evidence` is a narrow open-source maintainer project. It is not a full
agent platform, hosted service, compliance product, reputation system, or
official FDO standard. Its maintainable surface is local evidence packaging,
profile validation, signed export metadata, offline bundle verification,
verification receipts, and reviewer-facing review packs.

This narrow boundary makes the project a good fit for Codex-assisted
maintenance because many maintainer tasks are repetitive, evidence-oriented,
and reviewable as small pull requests.

## How Codex Can Reduce Maintainer Load

Codex can help maintainers by:

- reviewing pull requests for boundary drift, missing tests, unsafe claims, and
  documentation inconsistencies
- summarizing issues into reproducible validator, CLI, bundle-verification, or
  documentation tasks
- generating regression tests for reported validator, export, and verification
  behavior
- preparing release-note drafts from merged changes and existing ledger entries
- checking documentation consistency across `README.md`, `AGENTS.md`,
  `llms.txt`, `docs/project-facts.md`, and generated agent metadata
- reviewing validator changes against schemas and valid/invalid fixtures
- reviewing signed-export boundaries for key-handling, manifest, hash, and
  metadata safety
- reviewing offline bundle verification for path traversal, manifest drift, and
  receipt clarity
- checking review-pack quality, inventory completeness, limitation wording, and
  secret-handling boundaries

## Intended Codex Use Cases

Intended use cases are:

- pull request review support
- issue triage summaries
- regression test generation
- release-note preparation
- documentation consistency checks
- validator review
- signed-export boundary review
- offline bundle verification review
- review-pack quality checks

## Human Maintainer Review

Human maintainer review remains required. Codex output should be treated as
review support, patch drafting, consistency checking, or test generation, not
as an automatic merge, release, security approval, or adoption signal.

Codex must not create:

- hidden promotion
- fake adoption
- automatic releases
- unsupported legal claims
- unsupported compliance claims
- AI Act approval claims
- official FDO standard claims
