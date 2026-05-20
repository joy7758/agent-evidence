# Execution Evidence and Operation Accountability Profile for Verifiable AI Agent Operations

## 1. Abstract

Logs, traces, and chat transcripts help developers understand what an AI (Artificial Intelligence, 人工智能) agent did, but they do not automatically become independently checkable operation evidence. This paper introduces EEOAP (Execution Evidence and Operation Accountability Profile, 执行证据与操作问责配置文件), a minimal profile for representing one AI agent operation as a bounded evidence object. EEOAP packages actor, action, subject, policy, output, provenance, evidence references, and integrity binding into a structured object that can be reviewed outside the original runtime. The accompanying artifact includes a profile, evidence bundle, validator path, and reproducible `paper_case` example. Running `make paper-demo` validates the positive case and exercises a paired negative case: the valid evidence bundle reports `PASS valid evidence bundle`, while the tampered-output case reports `FAIL tampered output hash mismatch` and exposes `tampered_primary_error_code=references_digest_mismatch`. The contribution is deliberately narrow. EEOAP does not establish semantic correctness of AI outputs, production readiness, legal compliance, official FDO (FAIR Digital Object, 公平数字对象) standard adoption, a full cryptographic trust fabric, or ZKP (Zero-Knowledge Proof, 零知识证明) support. Instead, it shows how a small operation-level evidence profile and validator can make selected execution claims inspectable and falsifiable offline.

## 2. Introduction

AI (Artificial Intelligence, 人工智能) agent systems increasingly perform operations that matter beyond a single interactive session. They read and transform data, call tools, summarize records, prepare handoff artifacts, and produce outputs that may later be reused by a person, an organization, or another agent. After such an operation, the immediate question is often not only what the model answered. A later reviewer may need to know which actor performed the operation, which subject was acted on, which policy or constraint was referenced, what output object was produced, and whether the evidence record still matches the referenced output.

Many existing systems preserve parts of this story. Application logs capture events. Observability traces reconstruct call paths. Agent frameworks expose tool calls, intermediate messages, or execution spans. Provenance models describe derivation. Attestation systems bind artifacts to execution, identity, or build events. These are important foundations, but they are not always packaged as a compact operation evidence object that an external reviewer can validate without access to the original runtime.

EEOAP (Execution Evidence and Operation Accountability Profile, 执行证据与操作问责配置文件) addresses this smaller review problem. It defines a minimal evidence profile for one AI agent operation and a validator-backed path for checking the structure and bindings of that operation. The profile records the actor, action, subject, policy, output, provenance, evidence references, artifacts, and integrity digests needed for independent review. The validator checks whether those parts are present, internally linked, and bound by recomputable integrity values.

The current paper artifact is intentionally scoped. It demonstrates one aggregate-only operation over an FDO (FAIR Digital Object, 公平数字对象)-style dataset descriptor. The valid evidence object passes validation. A paired tampered object changes the output reference digest while leaving the integrity binding stale. The validator rejects the tampered object with `references_digest_mismatch`, and the demo reports the expected negative result.

This scope matters. The paper does not claim that EEOAP is a governance platform, production forensic system, legal compliance system, official FDO standard, or privacy-preserving ZKP implementation. It also does not claim that the AI output is semantically correct. The claim is narrower and more testable: a minimal evidence object can make selected operation-level claims checkable after execution.

## 3. Problem Statement

The motivating problem is independent review of an AI agent operation after the operation has completed. In many settings, the reviewer is not the original operator. The reviewer may not have runtime credentials, live service access, raw logs, model internals, or the complete tool environment. What the reviewer needs is a bounded evidence object that answers a small set of accountability questions:

- Who or what acted?
- What action was recorded?
- Which subject or data object was involved?
- Which policy or constraint was referenced?
- Which output object was produced?
- Which evidence references and artifacts are part of the record?
- Does the integrity binding still match the evidence object under review?

Logs and traces can help answer some of these questions, but they do not usually impose an operation-level evidence boundary. A log line may say that a tool call occurred without binding the actor, subject, policy, output reference, provenance statement, and validation status into one independently checkable object. A trace can be detailed but environment-specific. A signed file can show that some bytes were signed, yet still leave unclear whether the policy reference, output reference, and validation record are mutually consistent.

EEOAP (Execution Evidence and Operation Accountability Profile, 执行证据与操作问责配置文件) frames the problem as a profile and validation problem. The profile makes the operation components explicit. The validator checks that references close, policy and evidence linkages are coherent, and integrity digests still match canonicalized evidence material. The intended result is not a complete demonstration of truth or compliance. It is a reviewable operation object whose basic structural and integrity claims can be accepted or rejected offline.

The paper artifact fixes this problem statement to a single reproducible case. An AI agent operation emits an aggregate summary from an FDO (FAIR Digital Object, 公平数字对象)-style dataset descriptor under an aggregate-only policy. The valid evidence bundle should pass. If the output reference is changed, the validator should reject the object. This is the minimum behavior the artifact must show.

## 4. Contributions

- Minimal execution evidence profile for one AI (Artificial Intelligence, 人工智能) agent operation.
- Validator-backed evidence checking for structure, references, policy/evidence linkage, and integrity binding.
- Reproducible paper_case artifact showing valid evidence PASS and tampered-output FAIL with references_digest_mismatch.
- FDO (FAIR Digital Object, 公平数字对象) / data-space style mapping for discussion, not official standard adoption.

## 5. EEOAP Profile Design

EEOAP (Execution Evidence and Operation Accountability Profile, 执行证据与操作问责配置文件) is organized around one accountable operation. The profile is deliberately small. It does not try to model every possible agent state, every framework event, or every legal relationship around data processing. It records the minimum set of fields needed to describe and validate one operation-level evidence claim.

The profile contains an actor, a subject, an operation statement, a policy reference, constraints, provenance, evidence references, artifacts, integrity values, and validation metadata. The actor identifies the agent, service, or runtime identity associated with the operation. The subject identifies the object acted on, including a digest or comparable fingerprint. The operation records the action, input references, output references, policy reference, timestamp, and result summary. The policy and constraints express the policy object and named constraints that the operation claims to follow. Provenance links the actor, operation, subject, input, and output. Evidence references and artifacts bind external or embedded materials into the evidence object. Integrity values allow recomputation over canonical structures. Validation metadata records how the object was checked.

This design treats operation evidence as more than descriptive logging. In the `paper_case` example, the output reference digest is not just a note in a JSON (JavaScript Object Notation, JavaScript 对象表示法) file. It is part of an evidence structure whose reference digest can be recomputed. When the output digest is changed without updating the integrity binding, the validator reports `references_digest_mismatch`.

The design also keeps policy visible without inflating the policy claim. The example policy is aggregate-only. It can state that row-level records, personal data, raw prompts, and unredacted runtime logs are denied outputs. EEOAP can record that the operation referenced this policy and that the evidence object links to that policy. It does not establish that the policy is legally sufficient, correctly enforced by every runtime layer, or accepted by any regulator.

The profile is therefore a composition boundary. Existing systems may already provide logs, traces, provenance records, policy metadata, signatures, or attestations. EEOAP composes a small subset of such information into one operation-level evidence object and makes the validation path explicit.

## 6. Validator and Evidence Bundle

The validator is the operational center of the artifact. It turns the profile from a document shape into a checkable object. The validation path checks required structure, internal references, policy/evidence linkage, provenance consistency, and integrity binding. This paper does not require a network service, hosted API, OpenAPI surface, MCP surface, or external verifier. The current callable path is local and command-based.

The paper case lives in `examples/paper_case/`. It includes an FDO (FAIR Digital Object, 公平数字对象)-style dataset descriptor, an aggregate-only policy descriptor, an operation descriptor, a valid EEOAP evidence object, a tampered EEOAP evidence object, and expected validator result files. The positive evidence object is intended to be structurally complete and internally bound. The negative object is intentionally altered so that the output reference digest no longer matches the operation output content hash and the stored integrity binding is stale.

The reproducible path is:

```bash
make paper-demo
```

The target runs `scripts/reproduce_paper_demo.sh`. The script locates the paper case, prefers the local `agent-evidence validate-profile` command when available, and performs a local check that loads the JSON (JavaScript Object Notation, JavaScript 对象表示法) files, verifies required artifacts, checks dataset and policy linkage, validates the positive evidence object, compares the valid output digest with the operation output content hash, and confirms that the tampered output digest differs.

The expected visible lines are:

```text
PASS valid evidence bundle
FAIL tampered output hash mismatch
```

The script also prints a machine-readable summary that includes the `tampered_primary_error_code` JSON (JavaScript Object Notation, JavaScript 对象表示法) field with value `references_digest_mismatch`. That failure code is the central negative result: the validator detects that a reference digest no longer matches the integrity binding for the evidence object.

This evidence bundle is intentionally inspectable. A reviewer can open the files, compare the valid and tampered evidence objects, and rerun the same command locally. The goal is not to hide complexity behind a service. The goal is to make the minimum review path visible enough that a reviewer can understand why one case passes and the paired tampered case fails.

## 7. FDO/Data-space Mapping

EEOAP (Execution Evidence and Operation Accountability Profile, 执行证据与操作问责配置文件) is relevant to FDO (FAIR Digital Object, 公平数字对象) and data-space discussions because those communities often care about persistent identity, typed metadata, policy references, provenance, and integrity. The `paper_case` includes `fdo-dataset.json`, which represents the subject as an FDO-style dataset descriptor with identity, type, owner, content hash, policy reference, and metadata.

The mapping is deliberately standards-facing but not standards-claiming. The paper uses FDO-style language to make the relationship legible to FDO and data-space reviewers. It does not claim official FDO adoption, certification, conformance, endorsement, or release status. The example is a discussion object, not an official standard implementation.

The mapping can be read in two layers. At the data-object layer, an FDO-style descriptor identifies and describes the dataset-like subject. At the operation-evidence layer, EEOAP records what an AI (Artificial Intelligence, 人工智能) agent did with respect to that subject, which policy was referenced, what output was produced, and which integrity bindings make the record checkable. Data-space policy or usage-control systems may define permissions and obligations. EEOAP can record that a particular operation referenced a policy and produced a bounded output under that policy.

This complementarity is the main standards-facing point. FDO and data-space systems provide object identity, policy context, and exchange concepts. EEOAP provides an operation-level evidence object and validator path that can sit beside those concepts. It does not replace enforcement, contract interpretation, consent management, access control, or legal compliance review.

## 8. Evaluation

The evaluation is scoped to the current paper artifact. It checks whether the repository contains a reproducible positive case and a reproducible negative case for the core EEOAP (Execution Evidence and Operation Accountability Profile, 执行证据与操作问责配置文件) claim. The command `make paper-demo` passes in the intended artifact state. Its expected output includes `PASS valid evidence bundle` for the valid evidence object and `FAIL tampered output hash mismatch` for the tampered-output case. The tampered case exposes `tampered_primary_error_code=references_digest_mismatch`.

The explicit evaluation facts for this paper text are:

- `make paper-demo`: PASS.
- Valid evidence bundle: PASS.
- Tampered output: FAIL as expected.
- `tampered_primary_error_code=references_digest_mismatch`.
- Targeted EEOAP tests: 19 passed, 1 warning.
- Full repository pytest success is not claimed.

The positive case demonstrates that the valid evidence bundle is structurally complete, internally linked, policy-bound, and integrity-checkable under the repository validator path. The negative case demonstrates that a modified output reference is not silently accepted. When the output digest is altered while the integrity binding remains stale, the validator rejects the object.

The paper artifact also records that the targeted EEOAP tests previously passed with `19 passed, 1 warning`:

- `tests/test_paper_case.py`
- `tests/test_operation_accountability_profile.py`

Those tests cover the paper case files, output hash binding, demo PASS/FAIL lines, valid profile behavior, invalid profile behavior, issue summary reporting, fail-fast behavior, aggregation of structurally safe later-stage errors, schema-failure stage skipping, and the `validate-profile` command path used by the local CLI (Command Line Interface, 命令行界面). The targeted test result is reported only for that EEOAP (Execution Evidence and Operation Accountability Profile, 执行证据与操作问责配置文件) scope. This paper does not claim full repository pytest success. It also does not claim release validation for the entire repository. The evaluation is limited to the EEOAP paper case, the validator path relevant to that case, and the previously passed targeted tests.

This is not a model-performance benchmark. It does not measure accuracy, latency, robustness, policy enforcement strength, or cross-framework portability. It is an artifact validation check: one valid operation evidence object should pass, and one intentionally tampered output reference should fail with the expected error code.

## 9. Related Work

### Logs, traces, and observability

Observability systems record logs, metrics, traces, spans, tool calls, and runtime events. Agent frameworks often expose intermediate messages and tool execution traces that are useful for debugging and performance analysis. EEOAP (Execution Evidence and Operation Accountability Profile, 执行证据与操作问责配置文件) does not replace these systems. It uses a different boundary: instead of retaining every runtime event, it packages one completed operation as an evidence object that can be checked outside the runtime. Existing observability material may supply inputs to such an object, but logs and traces alone do not usually define the actor, subject, policy, output, provenance, and integrity binding as one validator target.

### Provenance and validity constraints

Provenance work describes where data came from, how it was derived, and which process or agent contributed to a result. Validity constraints and workflow audit trails can make derivation and dependency relationships explicit. EEOAP builds on this general idea by treating provenance as one component of an operation-level accountability object. Its focus is not complete historical reconstruction. The profile asks whether the recorded operation, policy, evidence references, and output binding form a coherent object for independent review.

### Profile, schema, and conformance validation

Profile and schema systems are widely used to narrow broad data models into implementable subsets. Conformance validators then check whether a concrete object satisfies the required shape and references. EEOAP follows this tradition. Its novelty is not that schemas or validators exist, but the composition of a minimal operation evidence profile for AI (Artificial Intelligence, 人工智能) agent operations with a validator path that checks structure, reference closure, policy/evidence linkage, and integrity binding.

### Verifiable provenance and attestation artifacts

Supply-chain provenance, signed metadata, transparency logs, attestations, and integrity manifests show how artifacts can be bound to identities, environments, or process claims. EEOAP does not claim first use of cryptographic evidence or tamper-evident records. The current artifact uses ordinary hashes over inspectable JSON (JavaScript Object Notation, JavaScript 对象表示法) evidence structures. Stronger signing, timestamping, transparency, and trusted-execution layers are compatible future additions, but the present contribution is the smaller profile and validator boundary for an AI operation.

### FDO (FAIR Digital Object, 公平数字对象) and data-space object systems

FDO (FAIR Digital Object, 公平数字对象) and data-space systems emphasize persistent identity, typed metadata, policy references, provenance, and controlled data exchange. EEOAP is complementary to those concerns. It can describe an operation performed against an FDO-style subject and bind the resulting output to policy and integrity information. The paper deliberately frames this as a mapping for discussion, not official FDO standard adoption or data-space compliance.

### Agent governance and execution evidence

Agent governance work addresses monitoring, control, approval, auditability, policy compliance, and organizational accountability for agentic systems. EEOAP contributes a narrow artifact inside that broader space: a minimal operation-level evidence object plus a validator path. It does not solve semantic correctness, legal compliance, multi-agent governance, reputation, or runtime enforcement. Its difference is composition and boundary: existing work has logs, provenance, telemetry, policy, attestation, and digital-object systems; EEOAP defines a small evidence object that packages selected operation claims for independent offline review.

## 10. Limitations

The current artifact has strict non-claims. First, it does not establish semantic correctness of AI (Artificial Intelligence, 人工智能) output. A summary or tool result can be structurally bound and still be wrong, incomplete, biased, or misleading. Domain-specific validation remains outside the current profile.

Second, it does not claim production readiness. The artifact is a scoped paper case and validator path, not a hardened multi-tenant service, deployment package, or operational compliance product. It does not claim broad cross-framework validation across agent runtimes.

Third, it does not claim official FDO (FAIR Digital Object, 公平数字对象) standard status. The mapping is meant for standards-facing discussion and data-space review, not certification, conformance, or endorsement.

Fourth, it does not claim full repository pytest success. The evaluation is limited to `make paper-demo`, the valid and tampered paper cases, and the targeted EEOAP tests previously reported as passing.

Fifth, it does not provide a full cryptographic trust fabric. The current artifact uses inspectable JSON (JavaScript Object Notation, JavaScript 对象表示法) evidence objects and hash bindings. It does not establish uncompromised runtime state, signer identity, secure time, key custody, trusted execution, or transparency-log inclusion.

Sixth, it does not implement ZKP (Zero-Knowledge Proof, 零知识证明). Selective disclosure and privacy-preserving audit are future work. They should be layered only after the base evidence object and validator path are stable.

Seventh, it does not make a legal compliance claim. A policy reference inside an evidence object is not a legal opinion, regulatory certification, or proof that a real deployment satisfies institutional or statutory obligations.

## 11. Standards-facing Implications

The standards-facing implication of EEOAP (Execution Evidence and Operation Accountability Profile, 执行证据与操作问责配置文件) is modest but useful: AI agent operations may need a portable evidence object between raw logs and broad governance claims. Standards and community discussions often distinguish object identity, metadata, policy, provenance, integrity, and validation, but agent operations can blur these concerns inside framework-specific traces or application logs.

EEOAP proposes one boundary for discussion. An operation evidence object should identify the actor, subject, action, policy, output, provenance, evidence references, and integrity bindings. A validator should be able to accept a well-formed object and reject a tampered object without contacting the original runtime. This boundary gives standards reviewers a concrete object shape to critique: which fields are too narrow, which references need stronger semantics, which integrity bindings should be externalized, and which claims require additional trust infrastructure.

For FDO (FAIR Digital Object, 公平数字对象) and data-space communities, the main question is whether an operation evidence object should be adjacent to data-object descriptors and policy artifacts. EEOAP suggests that it should. A data object can have identity and metadata. A policy can express constraints. An operation evidence object can record that an AI (Artificial Intelligence, 人工智能) agent acted against the data object under a referenced policy and produced a bounded output. This is a discussion proposal, not a standards adoption claim.

## 12. Conclusion

EEOAP (Execution Evidence and Operation Accountability Profile, 执行证据与操作问责配置文件) packages one AI (Artificial Intelligence, 人工智能) agent operation as a structured evidence object. It binds actor, action, subject, policy, output, provenance, evidence references, and integrity values into an object that a reviewer can inspect offline. The validator path checks structure, reference closure, policy/evidence linkage, and integrity binding.

The scoped paper artifact demonstrates the key boundary. Running `make paper-demo` reports a valid evidence bundle as passing and a tampered-output case as failing with `references_digest_mismatch`. This result is not a broad demonstration of correctness, compliance, security, or standards adoption. It is a small reproducible demonstration that operation evidence can be represented as a minimal profile and rejected when a bound output reference is altered.

Future work should remain incremental: clearer reviewer packages, stronger signing and timestamping options, additional runtime adapters, broader data-space discussion, and possible ZKP (Zero-Knowledge Proof, 零知识证明)-based selective disclosure. These extensions should preserve the base boundary: first make the operation evidence object inspectable, then add stronger trust layers where the use case requires them.

## 13. Artifact Availability

The current artifact is a scoped reproducible artifact candidate for EEOAP (Execution Evidence and Operation Accountability Profile, 执行证据与操作问责配置文件). The sealed local tag `eeoap-v0.1-paper` exists locally as the artifact anchor, but this text does not claim that the tag has been pushed publicly. The artifact remains local-only unless it is published later through an explicit repository release, archive, or DOI (Digital Object Identifier, 数字对象标识符) process. This draft does not claim that a public GitHub Release, Zenodo archive, DOI, or external endorsement already exists for the EEOAP paper artifact. If the artifact is later published, the public release note should preserve the scoped-release boundary: paper artifact, local validator path, bounded `paper_case` example, no production readiness, no official FDO (FAIR Digital Object, 公平数字对象) standard status, and no Zenodo DOI claim unless a DOI has actually been issued.

For the next text-only preparation stage, `paper/references.md` and `paper/citation-audit.md` record candidate citation work only. They are not a finalized venue bibliography. Formal submission still requires verified bibliography metadata, citation integration, and venue-specific formatting.

The replay command is:

```bash
make paper-demo
```

The expected demo output includes:

```text
PASS valid evidence bundle
FAIL tampered output hash mismatch
```

The expected tampered failure code is `references_digest_mismatch`. The targeted EEOAP tests previously reported `19 passed, 1 warning` for `tests/test_paper_case.py` and `tests/test_operation_accountability_profile.py`. Full repository pytest success, public GitHub Release publication, Zenodo DOI (Digital Object Identifier, 数字对象标识符), production readiness, official FDO (FAIR Digital Object, 公平数字对象) standard adoption, legal compliance, and ZKP (Zero-Knowledge Proof, 零知识证明) implementation are not claimed.
