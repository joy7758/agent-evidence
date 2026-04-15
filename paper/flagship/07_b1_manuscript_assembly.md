# B1 Manuscript Assembly

## Working title

A Minimal Verification Boundary for Single-Operation Accountability

## Positioning

This manuscript argues for one narrow result: single-operation accountability can be represented as a minimal verification boundary when execution evidence, policy binding, provenance closure, and validation outcome are compressed into one bounded profile. It does not attempt a larger governance or high-risk route. The contribution is valuable precisely because it isolates the smallest boundary that can still support offline review and third-party inspection under the current validator path.

## Abstract

Execution traces, logs, provenance links, and policy references do not by themselves form a verifiable accountability object. This manuscript addresses a narrower question: what is the smallest verification boundary required to represent and check a single operation accountability statement? The repository answers that question through `Execution Evidence and Operation Accountability Profile v0.1`, a bounded profile organized around `operation`, `policy`, `provenance`, `evidence`, and `validation`, together with a profile-aware validator, example set, CLI entry, and runnable demo path. The claim is deliberately limited. The package is not presented as a general governance framework or as a broad empirical study. It is a concrete method for packaging one operation into a portable statement that another party can inspect later, including offline. The current repository baseline is `1 valid / 3 invalid / 1 demo`. The valid case shows that the boundary can close as a complete accountability statement. The invalid cases show that the boundary can fail in classifiable ways through explicit validator outcomes and error codes. The demo shows that the same boundary can be exercised as a runnable artifact path. Together these assets support one result: a minimal verification boundary can be specified, validated, and reviewed as a bounded software artifact.

## 1. Introduction

Execution data is not yet the same thing as a verifiable accountability object. Current agent and runtime stacks expose logs, traces, provenance links, and policy references, but those materials remain difficult to review as one bounded statement. A third party may still be unable to answer a simpler question: what operation was performed, under which policy, with which supporting evidence, and by what validation path can the statement now be checked?

This manuscript starts from that narrower problem. The gap is not missing data in general; the gap is the absence of a bounded operation accountability statement that binds execution evidence, provenance closure, and validation into one portable unit. If the repository exposes only traces, review remains runtime-dependent. If it exposes only policy, the governing rule is visible but the accountable operation is not. If it exposes only provenance fragments, derivation may be visible without showing whether the statement closes. The B1 route therefore asks for the smallest boundary that still lets an external party decide whether a single operation accountability statement is structurally complete and locally checkable.

The manuscript stays narrow on purpose. It claims only what the repository already implements: a profile specification, a schema, examples, a profile-aware validator, a CLI entry point, a demo path, and submission handoff assets. It does not claim broad deployment or external generalization. The intended contribution is smaller and stronger: a minimal verification boundary can be stated cleanly enough to become a reusable software artifact.

## 2. Problem statement and design goal

The design problem is under-bounding, not missing instrumentation. A single operation may be described across logs, policy references, and output artifacts, yet still fail to become a stable review unit. Without a minimal profile, accountability remains descriptive rather than checkable. A reviewer can read evidence fragments, but cannot reliably decide whether the statement closes as an operation accountability object.

The design goal in B1 is to define the smallest profile that still supports profile-based checking under the current validator path. The statement must be minimal, so it carries only what is required for one operation accountability unit. It must be verifiable, so a checker can classify it through explicit rules rather than narrative interpretation alone. It must be portable and offline-reviewable, so it can be moved outside the originating runtime. It must also be runtime-decoupled, because a boundary that only works inside one stack is not useful as external evidence. The design task is therefore not to capture everything that happened, but to capture enough to make one local accountability claim checkable.

## 3. Minimal verification boundary

The central claim of B1 is exact and limited: execution evidence and operation accountability should be treated as a minimal verification boundary. In this manuscript, that phrase means a bounded set of fields sufficient for a third party to inspect one operation accountability statement under the current validator path without hidden runtime context. The boundary is not a replay of the original system. It is a local decision surface: does this statement close as a verifiable unit?

Within that boundary are the profile parts that carry the accountability claim: `operation`, `policy`, `provenance`, `evidence`, and `validation`. Around them sit only the supporting elements needed to bind the statement locally, such as actor, subject, constraints, timestamps, and profile identity. `Operation` states what was done. `Policy` anchors why the operation is governed in the stated way. `Provenance` closes the relation among actor, subject, and referenced inputs or outputs. `Evidence` links the statement to inspectable artifacts and digests. `Validation` records how the statement is checked and what outcome the checker returns. The boundary is minimal because each part serves one external judgment: the statement is complete enough, or it is not.

Just as important is what remains outside the boundary. This manuscript does not absorb full workflow models, broader governance controls, or larger reviewer-facing routes. Those may matter elsewhere, but they are not necessary to establish the present claim. If they are imported here, the argument loses proportionality. B1 matters precisely because it keeps the boundary narrow enough to validate directly while still being strong enough to support third-party inspection.

## 4. Profile, validator, and artifact package

The manuscript stands on an existing artifact package rather than proposed future machinery. The normative profile surface is `spec/execution-evidence-operation-accountability-profile-v0.1.md`, which describes the statement structure and intended semantics. The executable structural contract is `schema/execution-evidence-operation-accountability-profile-v0.1.schema.json`. Together they define the profile in prose and machine-readable form.

The validator is available through `agent-evidence validate-profile <file>`. It is profile-aware rather than a thin schema wrapper. In addition to required structure, it checks closure and consistency across policy, provenance, and evidence linkages, then returns machine-readable outcomes with primary error codes. That point matters because the claim is not merely that malformed JSON can be rejected. The stronger claim is that incomplete or inconsistent operation accountability statements can be classified in a readable way. The repository rounds out that surface with `examples/README.md`, `demo/README.md`, `demo/run_operation_accountability_demo.py`, `submission/package-manifest.md`, and `submission/final-handoff.md`. Together these assets make the profile, validator, examples, demo, and handoff reviewable as one bounded artifact package.

## 5. Validation results and boundary behavior

The validation baseline is intentionally narrow and executable: `1 valid / 3 invalid / 1 demo`. That is enough to show boundary behavior without expanding into a different manuscript surface. The valid example shows that the repository can express a complete operation accountability statement that closes under the profile and validator. The three invalid examples show that the same boundary remains meaningful under failure. Each breaks one primary rule, so the validator can return a readable failure outcome rather than a vague rejection.

The validator's error-code behavior is central to that claim. A profile-aware validator is useful only if boundary failures are classifiable. Here, invalid statements do not simply fail parsing; they return explicit outcomes and primary error codes. That lets the manuscript argue that the boundary is inspectable under both success and failure. The demo closes the loop by taking the same minimal path through execution and validation. What this section does not establish is broader external validation or wider scenario coverage. It establishes only that the minimal verification boundary is executable and diagnosable inside the current repository package.

Two supplementary additions extend that paper-facing evidence surface without rewriting the baseline. The supplementary external-context specimen shows that the current profile and validator path can still return a passing result for one low-complexity data-space metadata update outside the original minimal example family. The supplementary repo-local second checker shows a first checker-diversity step across one canonical valid case, one canonical invalid-unclosed-reference case, and the same external-context valid case. These additions are supplementary, support the flagship line, and are not counted in canonical B1 minimal-frozen `1 valid / 3 invalid / 1 demo`.

## 6. Discussion, limits, and next evidence

The limits are substantive and should be stated directly. This manuscript provides no broad external validation. There is no independent checker yet. It also does not attempt a larger governance or high-risk route. The repository supports a bounded profile and validator path, and the baseline of `1 valid / 3 invalid / 1 demo` is enough to support a minimal artifact claim, but not enough to justify stronger generalization.

Those limits also define the next evidence. The supplementary external-context specimen is only a first extension beyond the original minimal example family, not broader validation already completed. The repo-local second checker is only a first checker-diversity surface, not an external checker. Further refinement of the manuscript can sharpen argument and presentation, but it should not enlarge the claim beyond the implemented package. These remain next steps because the repository does not yet present them as completed results.

## 7. Conclusion

This manuscript advances one restrained result: `Execution Evidence and Operation Accountability Profile v0.1` establishes a minimal verification boundary for a single operation accountability statement. The contribution is not that the repository solves every larger governance problem. The contribution is that it turns one accountability question into a bounded, reviewable, and executable artifact surface through a profile, schema, profile-aware validator, examples, and demo. That boundary may support larger routes later, but it should be defended first on its own terms.

## Artifact map

- Root research entry: `../../README.md`
- Paper-facing ledger: `../README.md`
- Manuscript baselines: `../../submission/manuscript-baselines.md`
- Profile spec: `../../spec/execution-evidence-operation-accountability-profile-v0.1.md`
- Schema: `../../schema/execution-evidence-operation-accountability-profile-v0.1.schema.json`
- Examples: `../../examples/README.md`
- Demo: `../../demo/README.md`
- Project status: `../../docs/STATUS.md`
- Claims-to-evidence map: `13_claims_to_evidence_map.md`
- Validation results table: `18_validation_results_table.md`
