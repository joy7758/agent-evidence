# Operation Accountability as a First-Class Verification Boundary for Machine-Actionable Object Systems

## Abstract

In this framing, runtime traces and logs are useful but insufficient when a
reviewer needs to check what a machine-actionable object system actually did,
under which policy, and with which evidence links. This paper frames one
operation accountability statement as a first-class verification boundary. We
introduce Execution Evidence and Operation Accountability Profile v0.1, a
deliberately small JSON profile for binding actor, subject, operation, policy,
constraints, provenance, evidence, and validation metadata into one reviewable
object. The artifact includes a JSON Schema, a profile-aware validator, one
valid example, three controlled invalid examples, a metadata-enrichment demo, a
clean rerun, and a paper-minimal review package. The validator checks schema
conformance, reference closure, cross-field consistency, and integrity digest
recomputation. The valid example is expected to pass with no issues, while the
invalid examples ground representative failures for missing required structure,
unclosed output references, and broken policy-evidence linkage. The demo shows
the profile in a single metadata-enrichment operation, and the review package
freezes the inspection surface with a manifest and claim boundary. The
contribution is narrow: it makes a small operation-level evidence claim
independently checkable, with explicit non-claims about registries,
orchestration, complete interoperability, legal assurance, deployment, platform
governance, and runtime coverage.

## Contributions

1. Problem framing: operation accountability as a first-class verification boundary for machine-actionable object systems.
2. Minimal profile: Execution Evidence and Operation Accountability Profile v0.1 as a bounded statement format for independently checkable execution evidence.
3. Profile-aware validator: schema, references, consistency, and integrity checks exposed through the repository validator path.
4. Reproducible artifact package: examples, demo, rerun script, and paper-minimal review package for inspection and rerun.

## Scope and Non-claims

The paper studies a bounded operation accountability statement and its
paper-minimal artifact path. It does not claim:

- registry design
- multi-agent orchestration
- full FDO interoperability
- full cryptographic trust fabric
- legal non-repudiation
- production deployment
- broad platform governance
- broad runtime integration coverage
- compliance approval

The profile uses FDO-oriented object language only as a local framing device for
object references and reviewable evidence links. It does not define a universal
object standard, a multi-party trust infrastructure, or an operated service.

## Artifact Package Paragraph

The paper-minimal review package includes boundary docs, tables,
schema/profile material, examples, the metadata-enrichment demo, the
reproduction script, generated metadata, a manifest, and a claim boundary. The
package records file paths, file sizes, and SHA-256 digests in `MANIFEST.json`.
`MANIFEST.json` excludes itself to avoid a self-referential digest. The package
is an inspection package, not a standalone software distribution. Reproduction
commands are intended to be run from the repository root after installing
agent-evidence.

## Evaluation Paragraph

The evaluation is limited to the paper-minimal path. The valid example,
`examples/minimal-valid-evidence.json`, is expected to return `ok: true` and
`issue_count: 0`. The three invalid examples are expected to exit nonzero with
stable primary codes: `schema_violation` for
`examples/invalid-missing-required.json`, `unresolved_output_ref` for
`examples/invalid-unclosed-reference.json`, and
`unresolved_evidence_policy_ref` for
`examples/invalid-policy-link-broken.json`. The metadata-enrichment demo is
expected to end with a `PASS` summary line. A clean rerun supports bounded
reproducibility for this profile, validator, example set, demo, and package
surface only. It does not support a broad cross-framework claim or a deployment
claim.

## Reviewer Note

This package is intentionally small. Reviewers should inspect closure rather
than scale: whether the statement fields are present, references close,
policy-evidence links agree, integrity digests are recomputed, and the rerun
surface matches the stated boundary. Adjacent materials are preserved in the
repository for continuity, but they are not part of the current claim.

## Chinese Summary

这篇论文声称的是一个很小的、可复查的操作问责边界。它把一次机器可执行对象系统中的操作整理成一个 `operation accountability statement`，再用 EEOAP v0.1、JSON Schema、校验器、示例、演示和复跑脚本固定下来。有效示例应该通过，三个无效示例分别覆盖缺字段、引用不闭合和策略-证据链接错误。审阅包的作用是让审稿人检查当前材料是否闭合，而不是把仓库包装成完整软件发行版。论文不声称注册表设计、多智能体编排、完整 FDO 互操作、法律不可抵赖、生产部署、广义平台治理、广泛运行时覆盖或合规批准。相邻研究材料可以作为背景存在，但不属于当前主张。核心判断标准是闭环是否小、清楚、可复跑、可审计。
