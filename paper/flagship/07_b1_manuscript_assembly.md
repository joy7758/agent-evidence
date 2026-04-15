# B1 Manuscript Assembly

## Working title

Execution Evidence and Operation Accountability: A Minimal Verification Boundary for Single-Operation Accountability

## Positioning

This assembly is limited to one claim: a single operation can be packaged as a minimal, independently checkable accountability unit when execution evidence, policy binding, provenance closure, and validation outcome are held inside one bounded profile. The draft does not try to absorb larger reviewer-facing routes or broader governance narratives. Its value is that it isolates the smallest boundary that can still support offline review and external checking.

## Abstract

Agent and runtime systems can emit abundant traces, logs, provenance links, and policy references, yet those materials do not automatically form a verifiable accountability object. This manuscript assembly addresses a narrower question: what is the smallest verification boundary required to represent and check a single operation accountability statement? The repository answers that question through `Execution Evidence and Operation Accountability Profile v0.1`, a bounded profile organized around `operation`, `policy`, `provenance`, `evidence`, and `validation`, together with a profile-aware validator, example set, CLI entry, and runnable demo path. The contribution claimed here is deliberately small. It is not a governance platform, not a full audit plane, and not a broad empirical survey. It is a concrete method for packaging one operation into a portable statement that another party can inspect later, including offline. The current repository baseline supports that claim through `1 valid / 3 invalid / 1 demo`. The valid case shows that the boundary can close as a complete statement. The invalid cases show that boundary failure can be classified through explicit validator outcomes and error codes. The demo shows that the same boundary can be exercised as a runnable artifact path. Together these assets establish a minimal verification boundary rather than a larger system claim.

## 1. Introduction

Current agent and runtime stacks already expose many forms of operational evidence. Event logs show what happened, traces show sequencing, provenance links show derivation, and policy surfaces describe intended constraints. Those materials are useful for debugging and retrospective analysis, but they do not by themselves create a minimal accountability object that another party can validate later. A reviewer may still be unable to answer a simpler question: what operation was performed, under which policy, with which supporting evidence, and by what validation path can the statement now be checked?

This manuscript takes that narrower problem as its starting point. The gap is not the absence of execution data in general. The gap is the absence of a bounded operation accountability statement that binds execution evidence, provenance closure, and validation into one portable unit. If the repository exposes only traces, then review remains runtime-dependent. If it exposes only policy, then the governing rule is visible but the accountable operation is not. If it exposes only provenance fragments, then derivation may be visible without showing whether the local statement closes. The B1 route therefore asks for the smallest boundary that still lets an external party decide whether a single operation accountability statement is structurally complete and locally checkable.

The manuscript stays narrow on purpose. It claims only what the repository already implements: a profile specification, a schema, examples, a profile-aware validator, a CLI entry point, a demo path, and submission handoff assets. It does not claim broad deployment or external generalization. The intended contribution is smaller and more defensible: a minimal verification boundary can be stated cleanly enough to become a reusable software artifact.

## 2. Problem statement and design goal

The problem is that execution materials are often plentiful but weakly bounded. A single operation may be described across logs, policy references, and output artifacts, yet still fail to become an independently reviewable unit. Without a minimal profile, accountability remains descriptive rather than checkable. A reviewer can read evidence fragments, but cannot reliably decide whether the statement closes as an operation accountability object.

The design goal in B1 is to define the smallest profile that still supports independent verification. The statement must be minimal, so it carries only what is required for one operation accountability unit. It must be verifiable, so a checker can classify it through explicit rules rather than narrative interpretation alone. It must be portable and offline-reviewable, so it can be moved outside the originating runtime. It must also be runtime-decoupled, because a boundary that only works inside one stack is not useful as external evidence. The design task is therefore not to capture everything that happened. It is to capture enough to make one local accountability claim checkable.

## 3. Minimal verification boundary

The central claim of B1 is that execution evidence and operation accountability should be treated as a minimal verification boundary. In this manuscript, that phrase means a bounded set of fields sufficient for a third party to decide whether one operation accountability statement is checkable without hidden runtime context. The boundary is not a replay of the original system. It is a local decision surface: does this statement close as a verifiable unit?

Within that boundary are the profile parts that carry the accountability claim: `operation`, `policy`, `provenance`, `evidence`, and `validation`. Around them sit only the supporting elements needed to bind the statement locally, such as actor, subject, constraints, timestamps, and profile identity. `Operation` states what was done. `Policy` anchors why the operation is governed in the stated way. `Provenance` closes the relation among actor, subject, and referenced inputs or outputs. `Evidence` links the accountable statement to inspectable artifacts and digests. `Validation` records how the statement is checked and what outcome the checker returns. The boundary is minimal because each part exists to support one external judgment: the statement is complete enough, or it is not.

Just as important is what remains outside the boundary. This draft does not absorb full workflow models, broader governance controls, or larger reviewer-facing scenario surfaces. Those are valid topics for later routes, but they are not necessary to establish the present claim. If they are imported here, the argument loses proportionality. B1 matters precisely because it keeps the boundary narrow enough to validate directly while still being strong enough to support independent review.

## 4. Profile, validator, and artifact package

The repository already exposes the assets required for this manuscript. The normative profile surface is `spec/execution-evidence-operation-accountability-profile-v0.1.md`, which describes the statement structure and intended semantics. The executable structural contract is `schema/execution-evidence-operation-accountability-profile-v0.1.schema.json`. Together they define the profile in both prose and machine-readable form.

The validator is available through `agent-evidence validate-profile <file>`. It is profile-aware rather than a thin schema wrapper. In addition to required structure, it checks closure and consistency across policy, provenance, and evidence linkages, then returns machine-readable outcomes with primary error codes. This matters because the manuscript does not merely claim that malformed JSON can be rejected. It claims that incomplete or inconsistent operation accountability statements can be classified in a readable way. The repository rounds out that surface with `examples/README.md`, `demo/README.md`, `demo/run_operation_accountability_demo.py`, `submission/package-manifest.md`, and `submission/final-handoff.md`. Those assets make the profile, validator, examples, demo, and handoff reviewable as one bounded artifact package.

## 5. Validation results and boundary behavior

The B1 validation claim is intentionally small: `1 valid / 3 invalid / 1 demo`. That baseline is enough to show boundary behavior without expanding into a different manuscript surface. The valid example shows that the repository can express a complete operation accountability statement that closes under the profile and validator. The three invalid examples show that the same boundary remains meaningful under failure. Each breaks one primary rule, so the validator can return a readable failure outcome rather than a vague rejection.

The validator's error-code behavior is central to that boundary claim. A profile-aware validator is useful only if boundary failures are classifiable. Here, invalid statements do not simply fail parsing; they return explicit outcomes and primary error codes. That lets the manuscript argue that the boundary is inspectable under both success and failure. The demo closes the loop by taking the same minimal path through execution and validation. What this section does not establish is broader cross-framework validation or larger scenario coverage. It establishes only that the minimal verification boundary is executable and diagnosable inside the current repository package.

## 6. Discussion, limits, and next evidence

The first limit of this manuscript is scope. The repository supports a bounded profile and validator path, not a full governance ecosystem. The second limit is evidence breadth. A baseline of `1 valid / 3 invalid / 1 demo` is enough to support a minimal artifact claim, but not enough to justify stronger generalization. The third limit is checker diversity. The present package relies on the repository's current validation path rather than a stronger independent checker surface.

Those limits also define the next evidence. External-context evidence would test whether the same boundary holds outside the current example family. A third-party checker would reduce dependence on a single implementation and strengthen the claim that the boundary is stable under more than one validation path. More manuscript assembly across introduction, discussion, and conclusion would make the B1 route easier to revise without expanding its claim. These remain next steps because the repository does not yet present them as completed results.

## 7. Conclusion

This assembly advances one restrained result: `Execution Evidence and Operation Accountability Profile v0.1` establishes a minimal verification boundary for a single operation accountability statement. The contribution is not that the repository solves every larger governance problem. The contribution is that it turns one accountability question into a bounded, reviewable, and executable artifact surface through a profile, schema, profile-aware validator, examples, and demo. That boundary may support larger manuscript routes later, but it should be defended first on its own terms.

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
