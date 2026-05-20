# Execution Evidence and Operation Accountability Profile for Verifiable AI Agent Operations

## 1. Abstract

AI agent and service operations increasingly affect data handling, decision support, and organizational workflows, yet many systems still expose only chat transcripts, trace views, or local logs after an operation completes. These records are useful for debugging, but they are difficult for an independent reviewer to validate as bounded execution evidence. This paper introduces the Execution Evidence and Operation Accountability Profile (EEOAP), a minimal profile for packaging one AI agent operation as a verifiable evidence object. EEOAP binds the actor, action, subject, policy, output references, provenance, integrity fingerprints, and validation result into one reviewable JSON artifact. The accompanying repository implements a schema, validator, reproducible `paper_case`, boundary documentation, and a one-command demo. In the demo, a valid aggregate-only evidence object passes validation, while a tampered output case fails with the concrete validator code `references_digest_mismatch`. The work is intentionally narrow: it does not prove semantic correctness of the AI output, legal sufficiency of the policy, perfect runtime security, uncompromised signing identity, official FDO adoption, or privacy-preserving ZKP support. Instead, it shows that a small execution evidence profile can make operation claims independently replayable and falsifiable offline.

## 2. Introduction

AI agent operations are often evaluated through the immediate output they produce: a response, a tool result, a generated file, or a workflow state change. After the operation is complete, however, downstream reviewers often need a different kind of object. They need to know who or what acted, which subject was acted on, what policy was referenced, what output was produced, which references were bound into the record, and whether the record has been altered since it was created.

Traditional logs and traces only partially address this need. A log can say that an event happened. A trace can help a developer reconstruct control flow. A screenshot can show a user-facing result. None of these artifacts, by default, provides a compact external review object with schema validation, reference closure, provenance consistency, and integrity checking. In cross-organization review, data-space workflows, or research artifact evaluation, the problem is not simply observability. It is whether an operation can be represented as evidence that another party can inspect and replay without trusting the original runtime.

The Execution Evidence and Operation Accountability Profile (EEOAP) is a minimal answer to that problem. It models an operation as a structured evidence object with explicit fields for actor, subject, operation, policy, constraints, provenance, references, artifacts, integrity, and validation. The profile does not try to be a complete governance platform. It focuses on one important boundary: an operation statement should be independently checkable as a bounded object. If the output reference is changed after the fact, the validator should detect that the integrity binding no longer matches.

The current repository artifact demonstrates this boundary with a reproducible paper case. The case models an aggregate-only analysis operation over an FDO-style dataset descriptor. The valid evidence object passes the EEOAP validator. A paired tampered case changes the output digest and leaves the integrity binding stale. The validator rejects that object with `references_digest_mismatch`, and the demo script also confirms that the output hash no longer matches the declared operation output.

This paper makes three contributions. First, it defines a minimal profile shape for execution evidence and operation accountability. Second, it implements a validator path that checks schema, references, consistency, and integrity. Third, it packages a reproducible artifact that can be replayed with `make paper-demo`, producing both a positive case and a negative tamper-detection case.

## 3. Problem Statement

The motivating problem is independent review of AI agent operations after execution. A reviewer may not have access to the original runtime, credentials, logs, or infrastructure. The reviewer may also be outside the team that ran the operation. In that setting, the artifact must answer a small set of accountability questions:

- Which actor or agent performed the operation?
- What action was recorded?
- Which subject or target object was involved?
- Which policy was referenced?
- Which output object was produced?
- Which references and artifacts were bound into evidence?
- Did the integrity binding match the evidence object under review?

An ordinary log can answer some of these questions informally, but it does not usually encode them as a reusable verification object. A trace can be rich but environment-specific. A signed file can prove possession of a key at a point in time but still fail to express the internal relationship among actor, subject, policy, output, and validation. EEOAP treats these relationships as first-class review targets.

The problem is bounded. EEOAP does not attempt to determine whether the AI result is semantically correct. It does not prove that the referenced policy is legally sufficient for a regulator, institution, or data-space operator. It does not prove that the runtime was perfectly secure, that a signer was never compromised, or that a particular standards body has adopted the format. It also does not implement Zero-Knowledge Proof (ZKP) mechanisms in this version. These are important future concerns, but they are separate from the minimal question addressed here: can one operation be packaged so that structural completeness, reference binding, and tamper evidence are independently checkable?

## 4. EEOAP Profile Design

The EEOAP profile is designed around a single accountable operation statement. The current profile version used in the repository is intentionally compact. It includes the following conceptual fields:

- `actor`: the agent, service, or runtime identity associated with the operation.
- `subject`: the primary object acted on, including a digest and locator.
- `operation`: the action, subject reference, input references, output references, policy reference, and result summary.
- `policy`: the policy object referenced by the operation.
- `constraints`: named constraints that the policy binds to the operation.
- `provenance`: links among actor, operation, subject, inputs, and outputs.
- `evidence`: references, artifacts, and integrity digests.
- `validation`: the validator method, status, and references to evidence, provenance, and policy.

The design goal is not maximum expressiveness. The goal is to make the minimum accountability path explicit. The actor must be bound to the operation. The subject reference must resolve to the subject. The operation input and output references must resolve to evidence references with the expected roles. The policy reference must remain consistent across operation, evidence, and validation. The integrity block must match a canonical recomputation over the evidence references, artifacts, and statement core.

This structure separates EEOAP from a passive log entry. A log line can describe what happened, but the EEOAP object binds the operation's parts and exposes the binding to validation. In the `paper_case`, the output reference digest is not merely descriptive text. It is part of the object whose integrity digest is recomputed by the validator. When the output digest is changed in the tampered case, the recomputed references digest no longer matches the stored integrity value.

The profile also keeps policy and provenance visible without making broad legal or security claims. In the demo, the policy is an aggregate-only descriptor. It records allowed actions such as reading dataset descriptor metadata and emitting aggregate summaries, and denied outputs such as row-level records, personal data, raw prompts, and unredacted runtime logs. The evidence object can show that the operation referenced this policy. It cannot prove that the policy is legally sufficient in every jurisdiction or deployment context.

## 5. Validator and Evidence Bundle

The repository validator checks the EEOAP evidence object through multiple stages. First, schema validation ensures that required fields are present and that fields have the expected basic structure. Second, reference validation checks that internal identifiers resolve: operation references must point to existing subject and policy identifiers; policy constraint references must resolve to declared constraints; input and output references must resolve to declared evidence references; validation references must resolve to the evidence, provenance, and policy objects. Third, consistency validation checks relationships such as input and output roles and policy-reference alignment. Fourth, integrity validation recomputes digests over canonical JSON structures and compares them with the stored integrity values.

The reproducible paper case lives in `examples/paper_case/`. It contains:

- `fdo-dataset.json`: an FDO-style dataset descriptor for discussion.
- `policy-aggregate-only.json`: an aggregate-only policy descriptor.
- `agent-operation.json`: an operation descriptor with actor, action, subject, output, timestamp, policy reference, and provenance notes.
- `evidence-valid.json`: the valid EEOAP evidence object.
- `evidence-invalid-tampered-output.json`: the paired tampered object.
- `expected-validator-pass.json`: expected positive-case outcome.
- `expected-validator-fail.json`: expected negative-case outcome.

The one-command validation path is:

```bash
make paper-demo
```

The Makefile target calls `scripts/reproduce_paper_demo.sh`. The script resolves the repository root, locates the paper case, prefers the existing `agent-evidence validate-profile` command when available, and then performs a local fallback check. The fallback check loads the JSON files, confirms required files exist, validates the positive evidence object, checks dataset and policy linkage, confirms that the valid output digest matches the operation output content hash, and confirms that the tampered output digest does not match.

The required visible output includes:

```text
PASS valid evidence bundle
FAIL tampered output hash mismatch
```

The negative case is important. The tampered evidence object changes the output reference digest to a different value and keeps the old references integrity digest. The validator therefore reports `references_digest_mismatch`. This is the central distinction between the EEOAP evidence object and a simple JSON-shaped log: the object contains an integrity binding that can make a changed output reference detectable.

## 6. FDO/Data-space Mapping

EEOAP is also intended to support discussion with FAIR Digital Object (FDO) and data-space communities. The `paper_case` includes `fdo-dataset.json`, which models the input as an FDO-style dataset descriptor with an identity, type, owner, content hash, policy reference, and metadata. The mapping is deliberately phrased as FDO-style rather than FDO-standard. It is a discussion artifact, not a claim of official FDO adoption, certification, or conformance.

The mapping is useful because FDO and data-space contexts often need persistent identity, typed metadata, policy references, provenance, and integrity. EEOAP aligns with those concerns at the operation level. It can represent an AI agent operation as an evidence object that points to a subject object, links a policy, and records output references and integrity information.

This relationship is complementary. FDO-style object descriptors can help identify and describe data objects. EEOAP can describe an operation performed against such an object. Data-space policy mechanisms can express access, reuse, or processing rules. EEOAP can record that an operation referenced a given policy and can bind the resulting output into a validation object. The present artifact does not claim to solve data-space enforcement or legal compliance. It gives reviewers a concrete evidence object that can be checked offline.

## 7. Evaluation

The evaluation is intentionally small and reproducible. It tests whether the repository contains a replayable positive case and a replayable negative case for the core EEOAP claim. The current matrix is:

| Scenario | Result | Evidence |
| --- | --- | --- |
| valid evidence | PASS | `examples/paper_case/evidence-valid.json` passes through `make paper-demo` |
| tampered output | FAIL | `examples/paper_case/evidence-invalid-tampered-output.json` fails with `references_digest_mismatch` |
| offline verification | PASS | `scripts/reproduce_paper_demo.sh` runs locally without network access or dependency installation |
| FDO-style mapping | discussion-ready | `examples/paper_case/fdo-dataset.json` maps the subject to an FDO-style descriptor |

The valid case demonstrates that an EEOAP object can be structurally complete, internally linked, and integrity-checkable. The tampered case demonstrates that a changed output reference can be rejected. The offline verification case demonstrates that the core artifact can be replayed without a live service, network call, or external provider. The FDO-style mapping case demonstrates that the operation evidence can be related to data-object identity and policy discussion without claiming formal standard adoption.

The paper case is not a benchmark. It does not compare runtime systems, measure throughput, or evaluate model quality. Its role is narrower: to establish a minimal reproducibility artifact that reviewers can inspect directly. The accompanying test `tests/test_paper_case.py` checks that the paper case files exist, that the valid output hash matches the operation output content hash, that the tampered output hash differs, and that the demo script reports the expected PASS and FAIL lines.

### Artifact Availability

The artifact is available in the repository as ordinary source files. A reviewer can run:

```bash
make paper-demo
```

The expected output includes `PASS valid evidence bundle` and `FAIL tampered output hash mismatch`. The demo output also reports the observed tamper failure code `references_digest_mismatch`. This is the recommended minimal replay path for the paper draft.

## 8. Limitations

The current EEOAP artifact is intentionally conservative. It proves only a bounded form of reviewability and tamper detection. It does not prove that the AI output is semantically correct. An aggregate summary can be structurally bound and still be statistically wrong, incomplete, or misleading. Semantic validation requires domain-specific checks that are outside the current profile.

It does not prove that the policy is legally sufficient. The aggregate-only policy in the paper case is a small demonstration object. It is useful for showing policy binding, but it is not a legal opinion and should not be treated as evidence that a real deployment satisfies institutional, contractual, or regulatory requirements.

It does not prove perfect runtime security. The evidence object can represent an operation after execution and can detect changes to bound references. It cannot prove that the operating system, runtime, dependency chain, signer, or repository account was never compromised. Stronger deployment evidence would require additional controls such as signed build provenance, trusted execution records, secure time sources, key-management evidence, or independent attestations.

It does not claim official FDO adoption. The repository uses FDO-style language to make the mapping understandable for FDO and data-space discussion, but the profile is not an official FDO standard.

It does not implement ZKP. Zero-Knowledge Proof mechanisms may later help reviewers verify selected properties without disclosing full data or full operation details. In this version, EEOAP uses inspectable JSON objects and ordinary hash bindings. That choice is deliberate: the first artifact should be easy to read, replay, and falsify before adding privacy-preserving proof layers.

## 9. Related Work Placeholder

This section should be completed before formal submission. The likely related-work areas are:

- AI agent tracing and observability systems, which capture runtime traces but may not package operation evidence as an independent review object.
- Provenance models and workflow audit trails, which describe derivation and process history.
- Software supply-chain attestations and signed provenance, which bind artifacts to build or release events.
- Data-space policy and usage-control work, which motivates policy-bound operation records.
- FAIR Digital Object discussions, which motivate persistent identity, metadata, references, and integrity-oriented object description.
- Privacy-preserving audit and ZKP work, which may support future selective-disclosure versions of EEOAP.

The final paper should position EEOAP as a minimal profile and reproducibility artifact rather than as a replacement for these areas. Its contribution is the small bridge between AI agent operation records and independently replayable execution evidence.

## 10. Conclusion

EEOAP packages a single AI agent or service operation as a structured evidence object. The profile binds actor, action, subject, policy, output, provenance, integrity, and validation into one artifact that can be checked offline. The current repository demonstrates the idea with a minimal paper case, a validator, boundary documents, tests, and a one-command demo.

The key result is not that the system is complete. It is that the core accountability boundary is concrete: a valid evidence object passes, and a tampered output case fails with `references_digest_mismatch`. That failure mode shows that EEOAP is more than a JSON log. It is a small integrity-bound execution evidence object.

Future work should expand the profile carefully. Useful next steps include signed manifests, richer operation adapters, broader data-space mapping, independent reviewer packages, clearer venue-specific evaluation, and optional ZKP-based selective disclosure. Those extensions should not obscure the current contribution: a minimal working profile, validator, and reproducible artifact for verifiable AI agent operations.
