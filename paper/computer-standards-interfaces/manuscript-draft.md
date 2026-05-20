# A Minimal Execution Evidence Profile for Verifiable AI Agent Operations in FDO-style Data Spaces

Status: journal research article draft for Computer Standards & Interfaces
(计算机标准与接口期刊). Not submitted. Reference style and citation placement are
draft-not-final.

## 1. Introduction

AI (Artificial Intelligence, 人工智能) agent systems increasingly perform
operations whose evidence matters after the original interaction is over. An
agent may read a data descriptor, call a tool, apply a policy, produce a
summary, export a review package, or hand a result to another human or machine
reviewer. In those settings the important question is not only what text the
agent produced. A later reviewer may need to know which actor performed the
operation, what subject was acted on, which policy was referenced, what output
object was produced, which evidence references were included, and whether the
record still matches the referenced artifacts.

Runtime logs, traces, transcripts, and observability systems can preserve
important execution details. Provenance models can describe derivation,
activities, agents, and entities. Attestation and supply-chain metadata can
bind artifacts to process claims. These foundations are useful, but they do
not automatically define a compact operation evidence object that can be
validated outside the original runtime. A log line may report a tool call
without binding policy, output reference, provenance, and integrity into one
profile. A trace may be detailed yet tightly coupled to a framework. A signed
file may protect bytes while leaving the operation-level relationship among
subject, policy, output, and evidence references unclear.

This paper introduces EEOAP (Execution Evidence and Operation Accountability
Profile, 执行证据与操作问责配置文件), a minimal operation-level evidence profile and
validator path for independently reviewable AI agent operations in
FDO (FAIR Digital Object, 公平数字对象)-style data spaces. The profile records
the actor, action, subject, policy reference, output, provenance, evidence
references, artifacts, integrity bindings, and validation metadata for one
operation. The validator checks whether those parts are present, internally
linked, and bound by recomputable integrity values.

The contribution is deliberately narrow. EEOAP is not presented as a full AI
governance platform, production forensic system, legal compliance mechanism,
official FDO standard, universal agent registry, hosted API, or privacy-
preserving ZKP (Zero-Knowledge Proof, 零知识证明) implementation. It also does
not claim semantic correctness of AI output. The intended claim is smaller and
more testable: a minimal evidence object can make selected operation-level
claims inspectable and falsifiable offline.

The current artifact fixes this claim to a reproducible paper case. The
repository contains an FDO-style dataset descriptor, an aggregate-only policy,
an agent operation descriptor, a valid evidence object, and a paired tampered
evidence object. Running `make paper-demo` reports `PASS valid evidence bundle`
for the valid case and `FAIL tampered output hash mismatch` for the negative
case. The expected tampered failure code is
`references_digest_mismatch`. Targeted EEOAP tests previously passed with
`19 passed, 1 warning`; full repository pytest success is not claimed.

This paper makes exactly four contributions:

1. A minimal operation-level execution evidence profile for one AI
   (Artificial Intelligence, 人工智能) agent operation.
2. A validator-backed checking path for structure, references,
   policy/evidence linkage, and integrity binding.
3. A reproducible `paper_case` artifact showing valid evidence PASS and
   tampered-output FAIL with `references_digest_mismatch`.
4. An FDO (FAIR Digital Object, 公平数字对象)-style data-space mapping for
   standards discussion, not official standard adoption.

The rest of the paper is organized as follows. Section 2 defines the problem
and scope. Section 3 describes the EEOAP profile design. Section 4 explains
the validator and evidence bundle. Section 5 maps the profile to FDO-style
data-space concepts. Section 6 reports the reproducible paper case and
evaluation facts. Section 7 states the claim-to-evidence boundary. Section 8
discusses related work using verified source anchors. Section 9 records
limitations and threats to validity. Section 10 discusses standards and
interface implications. Section 11 concludes. Section 12 states artifact
availability.

## 2. Problem and Scope

The motivating problem is independent review of one AI agent operation after
execution. The reviewer may be a project maintainer, standards reviewer,
artifact reviewer, data-space participant, compliance engineer, or another
agent. The reviewer may not have access to the original runtime environment,
live service credentials, private logs, raw prompts, or model internals. What
the reviewer needs is a bounded record that answers a small set of questions:
who or what acted, what action was recorded, which subject was involved, which
policy was referenced, what output was produced, which evidence references
belong to the record, and whether the integrity binding still matches the
record under review.

This paper treats that need as a profile and validation problem. A profile
narrows a broad space of possible execution data into a specified structure. A
validator checks whether a concrete object satisfies that structure, whether
references close, whether policy and evidence linkages are coherent, and
whether integrity values still match. The result is not a proof of truth,
legality, security, or semantic correctness. It is a reviewable operation
object whose basic structural and integrity claims can be accepted or rejected
offline.

The scope is intentionally smaller than a general agent governance system.
EEOAP does not define organizational approval workflows, runtime enforcement,
human consent management, legal interpretation, agent reputation, policy
authoring, or production incident response. It also does not define a new
agent orchestration framework. It can be used beside such systems, but the
paper contribution is the evidence profile and validator boundary.

The scope is also smaller than a full cryptographic trust fabric. The current
artifact uses ordinary JSON (JavaScript Object Notation, JavaScript 对象表示法)
evidence structures and hash-like integrity bindings. It does not establish
secure time, key custody, signer identity, trusted execution, transparency-log
inclusion, certificate-chain validation, or non-repudiation. Such mechanisms
may be added in future work, but they are outside the present claim.

The FDO-style data-space scope is likewise bounded. The paper uses an
FDO-style dataset descriptor to make the subject object legible in standards
and data-space discussions. It does not claim official FDO adoption,
certification, conformance, endorsement, or implementation of an official FDO
standard. The term "FDO-style" indicates a discussion mapping around object
identity, typed metadata, policy reference, provenance, and integrity, not a
formal standard status.

The reproducible evaluation scope is one paper case. The artifact demonstrates
a valid evidence bundle and a paired tampered-output failure. It does not
claim broad cross-framework coverage, full repository pytest success, public
release publication, Zenodo DOI issuance, production readiness, legal
compliance, or ZKP implementation. Those boundaries are part of the paper
claim, not omissions to be hidden.

## 3. EEOAP Profile Design

EEOAP organizes execution evidence around one accountable operation. The
profile is designed to be small enough for review, strict enough for
validation, and explicit enough to separate claims from non-claims. It records
the minimum operation-level material needed to describe and check a completed
AI agent action.

The profile includes the following conceptual elements:

| Element | Role in EEOAP |
| --- | --- |
| Actor | Identifies the agent, service, or runtime actor associated with the operation. |
| Action | Describes the operation performed by the actor. |
| Subject | Identifies the object acted on, including digest or comparable fingerprint. |
| Policy reference | Names the policy or constraint object that the operation claims to reference. |
| Output reference | Identifies the output object and binds it to expected content information. |
| Provenance | Connects actor, operation, subject, input, output, and evidence context. |
| Evidence references | Lists files or objects that support review of the operation claim. |
| Integrity binding | Allows selected evidence material to be recomputed and compared. |
| Validation metadata | Records how the object was checked and what result was expected. |

This profile should be read as an interface boundary, not a complete
representation of every runtime event. An implementation may have much richer
logs, traces, prompts, tool messages, approvals, and model telemetry. EEOAP
selects a reviewable subset and packages it as one evidence object. The design
therefore complements observability and provenance systems rather than
replacing them.

The actor element makes the operation attributable at the profile level. It
does not prove legal identity, key custody, or uncompromised runtime state. The
subject element makes the data or object under operation explicit. In the
paper case, the subject is represented by an FDO-style dataset descriptor with
identity, type, owner, content hash, policy reference, and metadata. The
policy reference records the policy object that the operation claims to use.
In the paper case, this is an aggregate-only policy that denies row-level
records, personal data, raw prompts, and unredacted runtime logs as outputs.

The output reference is central to the tamper-detection example. The valid
evidence object includes an output digest that matches the operation output
content hash. The tampered evidence object changes the output digest while
leaving the integrity binding stale. This is enough for the validator-backed
path to reject the object with `references_digest_mismatch`. The profile does
not need to prove that the output is semantically correct to demonstrate this
structural and integrity boundary.

The provenance component follows the general provenance idea that entities,
activities, and agents can be related for later review [1]. EEOAP does not
claim full PROV conformance. It uses provenance as one component of a smaller
operation-level evidence object. Similarly, profile and validation ideas are
consistent with JSON Schema and conformance-validation traditions [3], but the
paper contribution is not JSON Schema itself. The contribution is the
composition of operation evidence fields, policy/evidence linkage, reference
closure, and integrity binding for AI agent operations.

The design goal is not maximal expressiveness. It is reviewability. A reviewer
should be able to open the evidence object, identify the actor, subject,
policy, output, and references, and rerun a local validation command. If a
bound reference is altered without updating the integrity binding, the
validator should produce a clear failure. That basic property is the foundation
on which stronger trust, publication, and privacy layers may later be added.

## 4. Validator and Evidence Bundle

The validator turns EEOAP from a descriptive document shape into a checkable
artifact. A profile without a validator can encourage consistent writing, but
it does not by itself reject malformed or tampered objects. The current
validator path checks required structure, internal references,
policy/evidence linkage, provenance consistency, and integrity binding for the
paper case boundary.

The paper case is located under `examples/paper_case/`. It contains:

| File | Purpose |
| --- | --- |
| `fdo-dataset.json` | FDO-style subject descriptor for discussion. |
| `policy-aggregate-only.json` | Aggregate-only policy descriptor. |
| `agent-operation.json` | Actor, action, subject, output, timestamp, policy, and provenance notes. |
| `evidence-valid.json` | Valid EEOAP evidence object. |
| `evidence-invalid-tampered-output.json` | Tampered object with changed output digest and stale binding. |
| `expected-validator-pass.json` | Expected positive validator result. |
| `expected-validator-fail.json` | Expected negative validator result. |

The reproducible path is:

```bash
make paper-demo
```

The Makefile target calls `scripts/reproduce_paper_demo.sh`. The script uses
the repository's existing environment and does not install dependencies. It
locates the paper case, prefers the local `agent-evidence validate-profile`
command when available, and performs local checks that load the JSON files,
verify required artifacts, check dataset and policy linkage, validate the
positive evidence object, compare the valid output digest with the operation
output content hash, and confirm that the tampered output digest differs.

The expected visible output includes:

```text
PASS valid evidence bundle
FAIL tampered output hash mismatch
```

The summary includes the tampered primary error code:

```text
tampered_primary_error_code=references_digest_mismatch
```

The negative case is important because it prevents the artifact from being a
happy-path-only example. A valid bundle passing validation shows that the
object can be represented and checked. A tampered-output case failing as
expected shows that changing a bound output reference is not silently
accepted. The specific failure code, `references_digest_mismatch`, gives
reviewers a concrete boundary to inspect.

The evidence bundle is intentionally local and inspectable. The current paper
does not require a hosted service, browser UI, OpenAPI surface, MCP surface,
remote verifier, or network access. This makes the artifact easier to review
as a standards-facing interface proposal. The object shape and validator
behavior can be inspected directly from repository files.

The validator path also helps keep claims bounded. It can show that a record
is structurally complete and integrity-checkable under the paper case. It
cannot show that the AI output is true, that a deployment is legally compliant,
that a runtime was uncompromised, that an official FDO standard has adopted
the profile, or that a public release exists. The validator is a checking
interface for a defined evidence object, not an all-purpose trust authority.

## 5. FDO-style Data-space Mapping

EEOAP is relevant to FDO-style data-space discussions because those
discussions often involve persistent object identity, typed metadata, policy
references, provenance, integrity, and exchange interfaces. An AI agent
operation performed against a data object can benefit from a separate
operation evidence object that records what was done, under which policy, with
which output, and with which integrity binding.

The paper case uses `fdo-dataset.json` as the subject descriptor. It is
FDO-style rather than an official FDO implementation. The descriptor gives the
operation a subject identity, type, owner, content hash, policy reference, and
metadata. EEOAP then records an agent operation against that subject and binds
the result to evidence references and integrity values. In this mapping, the
data object layer and operation evidence layer remain distinct.

| Data-space concern | EEOAP mapping |
| --- | --- |
| Object identity | Subject identifier and descriptor reference. |
| Typed metadata | Subject metadata carried in the FDO-style descriptor. |
| Policy context | Policy reference linked from subject and operation evidence. |
| Provenance | Operation-level relation among actor, action, subject, and output. |
| Integrity | Recomputable digest or comparable binding over evidence references. |
| Review interface | Local validation command and inspectable evidence bundle. |

This mapping is standards-facing because it gives reviewers a concrete object
boundary to critique. Should operation evidence be attached to a data object,
kept as a separate object, or registered through a data-space service? Which
fields are mandatory? Which policy references require stronger semantics?
Which integrity bindings are sufficient for a given assurance level? Which
future layers should provide signatures, timestamps, transparency, or
selective disclosure? EEOAP does not answer all of these questions. It
provides a minimal artifact that makes them reviewable.

The mapping is also cautious. It does not claim official FDO standard
adoption, certification, conformance, or endorsement. It does not implement
DONA DOIP, even though DOIP and digital object architecture provide relevant
background for object-interface discussion [5], [6]. The present contribution
is an operation evidence profile adjacent to data-space object systems, not a
replacement for those systems.

## 6. Reproducible Paper Case and Evaluation

The evaluation is intentionally scoped to the current paper artifact. It asks
whether the repository contains a reproducible positive case and a reproducible
negative case for the core EEOAP claim. The evaluation is not a model
benchmark, not a user study, not a deployment study, and not a formal
conformance test against an external standard.

The verified evaluation facts for this draft are:

| Check | Result | Boundary |
| --- | --- | --- |
| `make paper-demo` | PASS | Scoped paper artifact command. |
| Valid evidence bundle | PASS | Expected line: `PASS valid evidence bundle`. |
| Tampered output | FAIL as expected | Expected line: `FAIL tampered output hash mismatch`. |
| Tampered primary error code | `references_digest_mismatch` | Detects changed output reference digest. |
| Targeted EEOAP tests | 19 passed, 1 warning | Targeted tests only. |
| Full repository pytest | Not claimed | Not part of this package's current claim. |

The targeted EEOAP tests previously reported as passing were:

```text
tests/test_paper_case.py
tests/test_operation_accountability_profile.py
19 passed, 1 warning
```

These tests support the paper case scope and operation-accountability profile
behavior. They do not establish full repository health. The draft therefore
states the targeted result and explicitly says that full repository pytest
success is not claimed.

The positive case demonstrates that the valid evidence bundle is structurally
complete, internally linked, policy-bound, and integrity-checkable under the
repository validator path. The negative case demonstrates that a modified
output reference is rejected. In the tampered case, the output digest has been
changed while the integrity binding remains stale, so the validator-backed
path detects the mismatch.

The evaluation is meaningful because it is replayable and falsifiable. A
reviewer can inspect the evidence files, run `make paper-demo`, observe the
PASS/FAIL boundary, and compare the expected error code. If the tampered case
were accepted, the central integrity claim would fail. If the valid case were
rejected, the profile would not be a usable paper artifact. The pair of checks
therefore captures the minimum useful evidence for this stage.

At the same time, the evaluation is small. It covers one aggregate-only
operation over one FDO-style subject descriptor. It does not show that EEOAP
works across all agent frameworks, all data-space policy systems, all
deployment environments, or all adversarial conditions. It should be read as a
reproducible artifact and interface proof point, not as production validation.

## 7. Claim-to-Evidence Boundary

The paper's credibility depends on keeping each claim tied to the artifact
that supports it and keeping non-claims visible. The following table is the
submission-facing boundary.

| Claim | Evidence in artifact | Boundary / non-claim |
| --- | --- | --- |
| EEOAP defines a minimal operation-level profile. | `evidence-valid.json`, paper profile description, and paper case files. | Does not define a full governance platform or universal agent registry. |
| The validator checks structure and linkage. | `make paper-demo` and local validator path. | Does not prove legal compliance or runtime security. |
| The valid evidence bundle passes. | `PASS valid evidence bundle`. | Applies to scoped `paper_case`, not every possible evidence object. |
| The tampered output fails as expected. | `FAIL tampered output hash mismatch`. | Demonstrates one tamper class, not all attacks. |
| The primary error code is stable for this case. | `tampered_primary_error_code=references_digest_mismatch`. | Not a claim about all validator failures. |
| Targeted EEOAP tests passed. | `19 passed, 1 warning` for two targeted test files. | Full repository pytest success is not claimed. |
| FDO-style mapping is discussion-ready. | `fdo-dataset.json` and mapping section. | No official FDO adoption, conformance, certification, or endorsement. |
| Artifact has a local sealed anchor. | Local tag `eeoap-v0.1-paper` and sealed commit `96f444b7ed39b39fe9f47e428af835952e843cb0`. | Tag is not claimed as publicly pushed; no public release or DOI is claimed. |

This boundary also limits how related work should be used. The manuscript does
not claim first use of logs, provenance, attestation, schemas, validators, or
tamper-evident evidence. Existing work supplies background concepts. The
difference is composition and boundary: EEOAP packages selected components
into a minimal operation-level evidence object for AI agent operations and
provides a local validator path.

## 8. Related Work

This related-work section uses only verified source anchors already recorded
for the EEOAP preparation pass. Exact final citation formatting remains
draft-not-final.

Provenance models provide an important background for EEOAP. W3C PROV-DM
describes entities, activities, agents, and provenance relationships [1].
W3C PROV-Constraints gives validity and consistency-checking background [2].
EEOAP uses this family of ideas only as background. It does not implement full
PROV conformance and does not claim to replace provenance standards.

Schema and profile validation are also relevant. JSON Schema Draft 2020-12 is
a verified anchor for JSON-style schema and validation language [3]. EEOAP
uses JSON evidence objects and validator-backed checks, but JSON Schema is not
the whole contribution. The contribution is the operation evidence profile and
the specific validator path for structure, references, policy/evidence
linkage, and integrity binding.

Artifact review and reproducibility guidance provide a useful framing for the
paper case. ACM Artifact Review and Badging is a verified anchor for
artifact-reviewability and reproducibility discussion [4]. EEOAP does not
claim an ACM badge or formal artifact acceptance. The paper uses the
reviewability concept to justify a replayable `make paper-demo` path and
inspectable evidence files.

Digital object and object-interface work is relevant to the FDO-style mapping.
DONA's Digital Object Interface Protocol specification provides background on
digital object interfaces [5]. Kahn and Wilensky's digital object services
paper provides digital object architecture lineage and includes a verified DOI
[6]. EEOAP does not implement DOIP and does not claim to be a general digital
object architecture. It maps operation evidence to data-space object concerns
for discussion.

Supply-chain provenance and attestation systems show how artifacts can be
bound to process claims. SLSA Version 1.2 and SLSA Build Provenance provide
verified anchors for supply-chain integrity and provenance framing [7], [8].
The in-toto Stable specification provides background for attestation and
verifiable supply-chain metadata [9]. EEOAP does not claim SLSA conformance,
does not define a SLSA build provenance predicate, and does not implement
in-toto layout or verification.

Observability and telemetry systems supply runtime context. OpenTelemetry
Semantic Conventions provide background terminology for logs, traces, metrics,
spans, and semantic attributes [10]. OpenTelemetry's semantic conventions for
generative AI systems provide current background for model and agent telemetry
vocabulary, but their status is Development and should be used cautiously
[11]. EEOAP does not replace telemetry. It packages selected operation
evidence into a bounded object for offline review.

Across these areas, the paper does not claim first use of logs, provenance,
attestation, schemas, validators, or tamper-evident evidence. Its difference
is composition and boundary. It combines selected elements into a minimal
operation evidence profile for one AI agent operation and demonstrates a local
validator-backed PASS/FAIL path.

## 9. Limitations and Threats to Validity

The main limitation is scale. The current artifact contains one paper case,
not a large corpus of agent operations. It is sufficient for demonstrating the
minimum profile and validator boundary, but it does not show generality across
agent frameworks, data domains, deployment models, or data-space
implementations. A reviewer may reasonably ask for more cases before treating
EEOAP as mature.

A second limitation is semantic correctness. The validator can check whether a
bound output reference matches the evidence object. It cannot prove that the
AI output is true, complete, unbiased, policy-sufficient, or useful. Domain
correctness needs separate evaluation. This is especially important for
scientific, medical, financial, legal, or safety-sensitive uses.

A third limitation is the trust model. The current artifact uses local JSON
evidence and integrity bindings. It does not prove that the runtime was
secure, that the agent identity was uncompromised, that clocks were correct,
that signing keys were protected, or that the evidence entered an external
transparency system. A stronger deployment would need additional signing,
timestamping, key-management, and operational controls.

A fourth limitation is privacy and selective disclosure. The paper mentions
ZKP (Zero-Knowledge Proof, 零知识证明) only as a non-claim and future direction.
No ZKP implementation is present. The current artifact is intentionally
inspectable rather than privacy-preserving. Future privacy extensions should
not be claimed until implemented and validated.

A fifth limitation is standards status. The FDO-style mapping is not official
FDO adoption, certification, conformance, or endorsement. The artifact can
support standards discussion, but it does not establish standard status. The
same caution applies to DOIP, SLSA, in-toto, OpenTelemetry, JSON Schema, and
PROV references: they are related-work anchors, not proof that EEOAP conforms
to those systems.

A sixth limitation is repository health. The paper reports `make paper-demo`
and targeted EEOAP tests. It does not claim full repository pytest success.
That boundary prevents a targeted paper artifact from being overstated as a
full project release.

A final threat to validity is citation completeness. The current references
are draft-not-final and based only on verified source anchors. Before formal
submission, the author must manually verify all reference metadata, venue
style, DOI values where known, access information if required, and exact
citation placement. Missing bibliography work should not be hidden behind the
artifact results.

## 10. Standards and Interface Implications

The standards-facing implication of EEOAP is that AI agent operations may need
a portable evidence object between raw runtime traces and broad governance
claims. Standards and interface discussions often separate object identity,
metadata, policy, provenance, integrity, validation, and exchange. Agent
operations can collapse these concerns into framework-specific logs or
application-specific transcripts. EEOAP proposes a small boundary that makes
the operation evidence object explicit.

For interface designers, the profile suggests that a completed operation
should expose at least actor, action, subject, policy reference, output
reference, provenance, evidence references, integrity binding, and validation
metadata. Not every system needs to use the same serialization or exact field
names, but the review questions should be answerable. Without those elements,
a later reviewer may see output without evidence, policy without linkage, or
logs without an operation boundary.

For conformance and validation discussions, EEOAP suggests a staged approach.
First, define the smallest object that can be validated. Second, provide a
local checker that accepts valid evidence and rejects a known tampered case.
Third, add stronger assurance layers only when the base object is stable. This
keeps future signing, timestamping, transparency, and selective-disclosure
work from masking an unclear evidence profile.

For FDO-style and data-space discussions, EEOAP suggests that operation
evidence can be adjacent to data-object descriptors and policy artifacts. A
data object can identify the subject. A policy can state constraints. An
operation evidence object can record that an AI agent acted against that
subject, referenced that policy, produced a bounded output, and bound the
result to evidence references. This is a useful discussion pattern even before
any official standard adoption is considered.

For software quality, the paper emphasizes negative tests and non-claims. The
tampered-output failure is as important as the valid PASS. It shows that the
validator rejects a concrete mismatch. The non-claims are also part of quality:
the artifact does not overstate production readiness, legal compliance,
semantic correctness, official FDO status, ZKP implementation, public release,
or DOI issuance.

## 11. Conclusion

EEOAP (Execution Evidence and Operation Accountability Profile, 执行证据与操作问责配置文件)
defines a minimal operation-level evidence profile for one AI
(Artificial Intelligence, 人工智能) agent operation. It packages actor, action,
subject, policy, output, provenance, evidence references, integrity bindings,
and validation metadata into an object that can be reviewed outside the
original runtime. Its validator-backed path checks structure, reference
closure, policy/evidence linkage, and integrity binding.

The reproducible paper case demonstrates the core boundary. Running
`make paper-demo` reports `PASS valid evidence bundle` for the valid object and
`FAIL tampered output hash mismatch` for the tampered object. The expected
tampered primary error code is `references_digest_mismatch`. Targeted EEOAP
tests previously passed with `19 passed, 1 warning`; full repository pytest
success is not claimed.

The paper's value is not that it invents logs, provenance, validators,
attestations, or tamper-evident records. It does not claim that. Its value is
the composition of a small evidence profile, an inspectable evidence bundle,
a local validator path, and an FDO-style data-space mapping for standards
discussion. That composition gives reviewers a concrete object to test and
criticize.

Future work should expand cautiously. Additional paper cases, runtime
adapters, signatures, timestamps, transparency integration, richer policy
semantics, and privacy-preserving selective disclosure may be useful. Each
extension should preserve the base boundary: first make the operation evidence
object inspectable and validator-backed, then add stronger trust layers where
the use case justifies them.

## 12. Artifact Availability

The current artifact has a local sealed tag, `eeoap-v0.1-paper`, as an
artifact anchor. The sealed artifact commit is
`96f444b7ed39b39fe9f47e428af835952e843cb0`. This draft does not claim that
the tag has been pushed publicly.

Public GitHub Release publication is not claimed. Zenodo DOI (Digital Object
Identifier, 数字对象标识符) issuance is not claimed. Production readiness,
official FDO (FAIR Digital Object, 公平数字对象) standard adoption, legal
compliance, ZKP (Zero-Knowledge Proof, 零知识证明) implementation, and semantic
correctness of AI output are not claimed.

The artifact remains scoped to `paper_case`, the local validator path, valid
PASS, tampered FAIL, and targeted EEOAP tests. The reproduction command is:

```bash
make paper-demo
```

If a public release or archive is created later, the artifact availability
statement must be updated only after that public state actually exists.
