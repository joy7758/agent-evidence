# A Minimal Execution Evidence Profile for Validator-Checkable AI Agent Operation Records in FAIR Digital Object-Inspired Data-Space Settings

Bin Zhang

Independent Researcher, China

Corresponding author email: joy7759@gmail.com

ORCID: 0009-0002-8861-1481

## 1. Introduction

AI (Artificial Intelligence) agent systems increasingly perform operations
whose evidence matters after the original interaction is over. An agent may
read a data descriptor, call a tool, apply a policy, produce a summary, export
a review package, or hand a result to another reviewer. A later reviewer may
need to know which actor performed the operation, what subject was acted on,
which policy was referenced, what output object was produced, which evidence
references were included, and whether the record still matches the referenced
artifacts.

Runtime logs, traces, transcripts, and observability systems can preserve
execution details. Provenance models describe entities, activities, agents,
and relationships [1], [2]. Schema and conformance-validation methods can
turn broad data models into checkable subsets [3]. Supply-chain attestation
and telemetry systems provide additional background for process claims and
runtime events [7]-[11]. These foundations are useful, but they do not by
themselves define a compact operation evidence object that can be validated
outside the original runtime.

This paper introduces EEOAP (Execution Evidence and Operation Accountability
Profile), a minimal operation-level evidence profile and validator path for
independently reviewable AI agent operations in FAIR Digital Object-inspired
data-space settings. The profile records actor, action, subject, policy
reference, output, provenance, evidence references, artifacts, integrity
bindings, and validation metadata for one operation. The validator checks
whether those parts are present, internally linked, and bound by recomputable
integrity values.

The contribution is deliberately narrow. EEOAP is not presented as a full AI
governance platform, production forensic system, legal compliance mechanism,
FAIR Digital Object Framework implementation, universal agent registry, hosted API, or
privacy-preserving ZKP (Zero-Knowledge Proof) implementation. It also does not
claim semantic correctness of AI output. The intended claim is smaller and
more testable: a minimal evidence object can make selected operation-level
claims inspectable and falsifiable offline.

The current artifact fixes this claim to a reproducible paper case. Running
`make paper-demo` reports `PASS valid evidence bundle` for the valid case and
`FAIL tampered output hash mismatch` for the negative case. The expected
tampered failure code is `references_digest_mismatch`. Targeted EEOAP tests
previously passed with `19 passed, 1 warning`; full repository pytest success
is not claimed.

## 2. Problem and Scope

The motivating problem is independent review of one AI agent operation after
execution. The reviewer may be a project maintainer, standards reviewer,
artifact reviewer, data-space participant, compliance engineer, or another
agent. The reviewer may not have access to the original runtime environment,
live service credentials, private logs, raw prompts, or model internals.

This paper treats that need as a profile and validation problem. A profile
narrows a broad space of possible execution data into a specified structure. A
validator checks whether a concrete object satisfies that structure, whether
references close, whether policy and evidence linkages are coherent, and
whether integrity values still match. The result is not a proof of truth,
legality, security, or semantic correctness. It is a reviewable operation
object whose structural and integrity claims can be accepted or rejected
offline.

The scope is intentionally smaller than a general agent governance system.
EEOAP does not define organizational approval workflows, runtime enforcement,
human consent management, legal interpretation, agent reputation, policy
authoring, or production incident response. It also does not define a new
agent orchestration framework. It can be used beside such systems, but the
paper contribution is the evidence profile and validator boundary.

The FAIR Digital Object-inspired data-space scope is also bounded. The paper
uses a FAIR Digital Object-inspired dataset descriptor to make the subject
object legible in standards and data-space discussions. It does not claim
conformance to, certification by, endorsement from, or implementation of a
specific FAIR Digital Object Framework.

In this paper, "validator-checkable" refers only to offline checking of
structural completeness, reference closure, and selected linkage and integrity
constraints within the bounded EEOAP evidence object. It does not denote
formal verification of the underlying runtime, semantic correctness of the
generated output, legal compliance, or exhaustive assurance of the surrounding
system.

## 3. EEOAP Profile Design

EEOAP organizes execution evidence around one accountable operation. It is
designed to be small enough for review, strict enough for validation, and
explicit enough to separate claims from non-claims. The profile includes:

| Element | Role in EEOAP |
| --- | --- |
| Actor | Identifies the agent, service, or runtime actor. |
| Action | Describes the operation performed by the actor. |
| Subject | Identifies the object acted on, including a digest or fingerprint. |
| Policy reference | Names the policy or constraint object referenced by the operation. |
| Output reference | Identifies the output object and expected content information. |
| Provenance | Connects actor, operation, subject, input, output, and context. |
| Evidence references | Lists files or objects that support review of the operation claim. |
| Integrity binding | Allows selected evidence material to be recomputed and compared. |
| Validation metadata | Records how the object was checked and what result was expected. |

The term "minimal" is used in a pragmatic rather than formal proof-theoretic
sense. Each required element is included because it is needed either to
identify the acted-on object, reconstruct the claimed operation context,
connect the operation to a policy and evidence boundary, or recompute the
integrity boundary used in validation. In the paper case, removing actor,
subject, policy reference, output reference, evidence references, integrity
binding, or validation metadata would leave at least one review question
unanswered or would disable at least one validator check.

This profile is an interface boundary, not a complete representation of every
runtime event. An implementation may have richer logs, traces, prompts, tool
messages, approvals, and model telemetry. EEOAP selects a reviewable subset
and packages it as one evidence object. In this sense it complements
observability, provenance, schema validation, and attestation systems [1],
[3], [7]-[11].

The output reference is central to the tamper-detection example. The valid
evidence object includes an output digest that matches the operation output
content hash. The tampered evidence object changes the output digest while
leaving the integrity binding stale. This is enough for the validator-backed
path to reject the object with `references_digest_mismatch`. The profile does
not need to prove that the output is semantically correct to demonstrate this
structural and integrity boundary.

## 4. Validator and Evidence Bundle

The validator turns EEOAP from a descriptive document shape into a checkable
artifact. A profile without a validator can encourage consistent writing, but
it does not by itself reject malformed or tampered objects. The current
validator path enforces required structure, reference closure, and
integrity-linked consistency conditions over the fields used by the review
object. The manuscript directly demonstrates this boundary through a valid
case and a controlled integrity-failure case. Broader validator behavior is
supported by targeted tests but is not claimed exhaustively here.

The paper case is under `examples/paper_case/` and contains a FAIR Digital
Object-inspired subject descriptor, an aggregate-only policy descriptor, an
agent operation descriptor, a valid EEOAP evidence object, a tampered object
with a changed output digest and stale binding, and expected validator
pass/fail results.

The reproducible path is:

```bash
make paper-demo
```

The expected visible output includes:

```text
PASS valid evidence bundle
FAIL tampered output hash mismatch
```

The summary includes the tampered primary error code:

```text
tampered_primary_error_code=references_digest_mismatch
```

The negative case prevents the artifact from being a happy-path-only example.
A valid bundle passing validation shows that the object can be represented and
checked. A tampered-output case failing as expected shows that changing a
bound output reference is not silently accepted.

## 5. FAIR Digital Object-inspired Data-space Mapping

EEOAP is relevant to FAIR Digital Object-inspired data-space discussions
because those discussions often involve persistent object identity, typed
metadata, policy references, provenance, integrity, and exchange interfaces.
Digital object and object-interface work provides useful background [5], [6].
An AI agent operation performed against a data object can benefit from a
separate operation evidence object that records what was done, under which
policy, with which output, and with which integrity binding.

In this manuscript, "FAIR Digital Object-inspired" denotes an object-centric
packaging pattern motivated by FAIR Digital Object discussions, including
persistent identity, machine-readable metadata, typed description, policy
references, and resolvable links. It does not claim conformance to a specific
FAIR Digital Object Framework implementation or to a DOIP (Digital Object
Interface Protocol, 数字对象接口协议) service.

The paper case uses `fdo-dataset.json` as the subject descriptor. It is
FAIR Digital Object-inspired rather than an implementation of a specific FAIR
Digital Object Framework. The descriptor gives the operation a subject
identity, type, owner, content hash, policy reference, and metadata. EEOAP
then records an agent operation against that subject and binds the result to
evidence references and integrity values.

| Data-space concern | EEOAP mapping |
| --- | --- |
| Object identity | Subject identifier and descriptor reference. |
| Typed metadata | Subject metadata carried in the FAIR Digital Object-inspired descriptor. |
| Policy context | Policy reference linked from subject and operation evidence. |
| Provenance | Operation-level relation among actor, action, subject, and output. |
| Integrity | Recomputable digest or comparable binding over evidence references. |
| Review interface | Local validation command and inspectable evidence bundle. |

This mapping is standards-facing because it gives reviewers a concrete object
boundary to critique. It does not claim FAIR Digital Object Framework
conformance, certification, endorsement, or deployment. It also does not
implement DONA DOIP, even though DOIP and digital object architecture provide
relevant background [5], [6].

## 6. Reproducible Paper Case and Evaluation

The evaluation is intentionally scoped to the current paper artifact. It asks
whether the repository contains a reproducible positive case and a reproducible
negative case for the core EEOAP claim. The evaluation is not a model
benchmark, user study, deployment study, or formal conformance test against an
external standard.

| Check | Result | Boundary |
| --- | --- | --- |
| `make paper-demo` | PASS | Scoped paper artifact command. |
| Valid evidence bundle | PASS | Expected line: `PASS valid evidence bundle`. |
| Tampered output | FAIL as expected | Expected line: `FAIL tampered output hash mismatch`. |
| Tampered primary error code | `references_digest_mismatch` | Detects changed output reference digest. |
| Targeted EEOAP tests | 19 passed, 1 warning | Targeted tests only. |
| Full repository pytest | Not claimed | Not part of this package's current claim. |

The targeted EEOAP tests previously reported as passing were
`tests/test_paper_case.py` and
`tests/test_operation_accountability_profile.py`, with `19 passed, 1 warning`.
These tests support the paper case scope and operation-accountability profile
behavior. They do not establish full repository health.

The evaluation is meaningful because it is replayable and falsifiable. A
reviewer can inspect the evidence files, run `make paper-demo`, observe the
PASS/FAIL boundary, and compare the expected error code. If the tampered case
were accepted, the central integrity claim would fail. If the valid case were
rejected, the profile would not be a usable paper artifact.

## 7. Claim-to-Evidence Boundary

The paper's credibility depends on keeping each claim tied to the artifact
that supports it and keeping non-claims visible.

| Claim | Evidence in artifact | Boundary / non-claim |
| --- | --- | --- |
| EEOAP defines a minimal operation-level profile. | `evidence-valid.json`, profile description, and paper case files. | Not a full governance platform or universal agent registry. |
| The validator enforces required structure, reference closure, and integrity-linked consistency conditions for the paper case. | `make paper-demo` and local validator path. | Does not prove legal compliance, runtime security, or exhaustive validator assurance. |
| The valid evidence bundle passes. | `PASS valid evidence bundle`. | Applies to scoped `paper_case`. |
| The tampered output fails as expected. | `FAIL tampered output hash mismatch`. | Demonstrates one tamper class, not all attacks. |
| The primary error code is stable for this case. | `tampered_primary_error_code=references_digest_mismatch`. | Not a claim about all validator failures. |
| Targeted EEOAP tests passed. | `19 passed, 1 warning` for two targeted test files. | Full repository pytest success is not claimed. |
| FAIR Digital Object-inspired mapping is discussion-ready. | `fdo-dataset.json` and mapping section. | No FAIR Digital Object Framework conformance, certification, endorsement, or deployment. |
| Artifact has a local sealed anchor. | Local tag `eeoap-v0.1-paper`; commit `96f444b7ed39b39fe9f47e428af835952e843cb0`. | Tag is not claimed as publicly pushed; no public release or DOI is claimed. |

## 8. Related Work

W3C PROV-DM and PROV-Constraints provide provenance and consistency-checking
background [1], [2]. EEOAP uses this family of ideas only as background. It
does not implement full PROV conformance and does not claim to replace
provenance standards.

JSON Schema Draft 2020-12 is a verified anchor for JSON-style schema and
validation language [3]. EEOAP uses JSON evidence objects and
validator-backed checks, but JSON Schema is not the whole contribution. The
contribution is the operation evidence profile and the specific validator path
for required structure, reference closure, and integrity-linked consistency
conditions over the paper-case fields.

ACM Artifact Review and Badging provides artifact-reviewability and
reproducibility framing [4]. EEOAP does not claim an ACM badge or formal
artifact acceptance. The paper uses the reviewability concept to justify a
replayable `make paper-demo` path and inspectable evidence files.

DONA's Digital Object Interface Protocol specification and Kahn and
Wilensky's digital object services paper provide digital object and
object-interface background [5], [6]. EEOAP does not implement DOIP and does
not claim to be a general digital object architecture.

SLSA Version 1.2, SLSA Build Provenance, and in-toto Stable provide
supply-chain provenance and attestation background [7]-[9]. EEOAP does not
claim SLSA conformance, does not define a SLSA build provenance predicate, and
does not implement in-toto layout or verification.

OpenTelemetry Semantic Conventions and the OpenTelemetry generative AI
conventions provide observability and telemetry background [10], [11]. The
generative AI conventions are marked Development and should be cited
cautiously. EEOAP does not replace telemetry. It packages selected operation
evidence into a bounded object for offline review.

EEOAP is adjacent to several existing approaches but narrower than all of
them. Unlike PROV, it does not attempt to represent arbitrary provenance
graphs or claim PROV validity; it packages one reviewable operation record.
Unlike JSON Schema, it does not rely on schema assertions alone, because
cross-reference and digest checks are part of the validator path. Unlike SLSA
and in-toto, it does not attest a software supply chain; it records post hoc
evidence for one AI-agent operation. Unlike OpenTelemetry, it is not a live
observability convention; it is an offline review object.

## 9. Limitations and Threats to Validity

The main limitation is scale. The current artifact contains one paper case,
not a large corpus of agent operations. It is sufficient for demonstrating the
minimum profile and validator boundary, but it does not show generality across
agent frameworks, data domains, deployment models, or data-space
implementations.

A second limitation is semantic correctness. The validator can check whether a
bound output reference matches the evidence object. It cannot prove that the
AI output is true, complete, unbiased, policy-sufficient, or useful. Domain
correctness needs separate evaluation.

A third limitation is the trust model. The current artifact uses local JSON
evidence and integrity bindings. It does not prove that the runtime was
secure, that agent identity was uncompromised, that clocks were correct, that
signing keys were protected, or that evidence entered an external transparency
system.

A fourth limitation is privacy and selective disclosure. ZKP is mentioned
only as a non-claim and future direction. No ZKP implementation is present.
The current artifact is intentionally inspectable rather than
privacy-preserving.

In broader deployments, operation evidence may contain prompts, tool
definitions, outputs, identifiers, or policy references that carry sensitive
or proprietary information. The present paper does not solve selective
disclosure, retention control, or privacy-preserving release of such content
and therefore treats privacy-preserving deployment as out of scope.

A fifth limitation is standards status. The FAIR Digital Object-inspired
mapping is not FAIR Digital Object Framework conformance, certification,
endorsement, or deployment. The same caution applies to DOIP, SLSA, in-toto,
OpenTelemetry, JSON Schema, and PROV references: they are related-work
anchors, not proof that EEOAP conforms to those systems.

A final threat to validity is citation completeness. Before formal
submission, the author must manually verify all reference metadata, venue
style, DOI values where known, access information if required, and exact
citation placement.

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
names, but the review questions should be answerable.

For conformance and validation discussions, EEOAP suggests a staged approach:
define the smallest object that can be validated, provide a local checker that
accepts valid evidence and rejects a known tampered case, and add stronger
assurance layers only when the base object is stable.

## 11. Conclusion

EEOAP defines a minimal operation-level evidence profile for one AI agent
operation. It packages actor, action, subject, policy, output, provenance,
evidence references, integrity bindings, and validation metadata into an
object that can be reviewed outside the original runtime. Its validator-backed
path enforces required structure, reference closure, and integrity-linked
consistency conditions over the paper-case fields.

The reproducible paper case demonstrates the core boundary. Running
`make paper-demo` reports `PASS valid evidence bundle` for the valid object
and `FAIL tampered output hash mismatch` for the tampered object. The expected
tampered primary error code is `references_digest_mismatch`. Targeted EEOAP
tests previously passed with `19 passed, 1 warning`; full repository pytest
success is not claimed.

The paper's value is the composition of a small evidence profile, an
inspectable evidence bundle, a local validator path, and a FAIR Digital
Object-inspired data-space mapping for standards discussion. That composition
gives reviewers a concrete object to test and criticize without overstating
production, legal, standards, privacy, or release claims.

## 12. Artifact Availability

The artifact supporting the bounded claims of this paper consists of the
`paper_case` files, the local validator path, and the `make paper-demo`
reproduction command. At initial submission, the supporting software artifact
is not deposited in a public repository because the author is maintaining a
sealed review-state package and does not yet claim a public release or
archival identifier. A private review package can be supplied to editors and
reviewers through the journal workflow on request.

This submission does not claim a public GitHub Release or a Zenodo DOI. The
claims supported by the artifact are limited to acceptance of the valid paper
case, rejection of a controlled tampered case with the expected error
boundary, and the bounded targeted-test evidence described in the manuscript.
If the artifact is later publicly released, this statement will be updated to
include the persistent access point.

## Declaration of generative AI and AI-assisted technologies in the manuscript preparation process

During the preparation of this work, the author used OpenAI ChatGPT and Codex
to support language editing, structural reorganization, command generation,
and drafting of submission-packaging text. After using these tools, the
author reviewed and edited the content as needed and takes full
responsibility for the content of the article.

## 13. References

[1] W3C (World Wide Web Consortium). PROV-DM: The PROV Data Model. W3C
Recommendation, 30 April 2013. Editors: Luc Moreau and Paolo Missier.
Available at: https://www.w3.org/TR/prov-dm/. Accessed 21 May 2026.

[2] W3C (World Wide Web Consortium). Constraints of the PROV Data Model. W3C
Recommendation, 30 April 2013. Editors: James Cheney, Paolo Missier, and Luc
Moreau; author: Tom De Nies. Available at:
https://www.w3.org/TR/prov-constraints/. Accessed 21 May 2026.

[3] Austin Wright, Henry Andrews, Ben Hutton, and Greg Dennis. JSON Schema
Draft 2020-12. JSON Schema project, published 16 June 2022. Available at:
https://json-schema.org/draft/2020-12. Accessed 21 May 2026.

[4] ACM (Association for Computing Machinery). Artifact Review and Badging -
Current. Artifact Review and Badging Version 1.1, 24 August 2020. Available
at: https://www.acm.org/publications/policies/artifact-review-and-badging-current.
Accessed 21 May 2026.

[5] DONA Foundation. Digital Object Interface Protocol Specification. Version
2.0, 12 November 2018. Available at:
https://www.dona.net/sites/default/files/2018-11/DOIPv2Spec_1.pdf. Accessed
21 May 2026.

[6] Robert Kahn and Robert Wilensky. A framework for distributed digital object
services. International Journal on Digital Libraries, 6, 115-123, 2006.
https://doi.org/10.1007/s00799-005-0128-x.

[7] SLSA (Supply-chain Levels for Software Artifacts). SLSA specification.
Version 1.2, status: Approved. Available at: https://slsa.dev/spec/v1.2/.
Accessed 21 May 2026.

[8] SLSA (Supply-chain Levels for Software Artifacts). Build: Provenance.
Status: Approved. Predicate type: https://slsa.dev/provenance/v1. Available
at: https://slsa.dev/spec/v1.2/build-provenance. Accessed 21 May 2026.

[9] in-toto. Specifications: in-toto Stable (v1.0). Status from source:
thoroughly reviewed specification. Available at: https://in-toto.io/docs/specs/.
Accessed 21 May 2026.

[10] OpenTelemetry. OpenTelemetry semantic conventions 1.41.0. Available at:
https://opentelemetry.io/docs/specs/semconv/. Accessed 21 May 2026.

[11] OpenTelemetry. Semantic conventions for generative AI systems.
OpenTelemetry semantic conventions 1.41.0, status: Development. Available at:
https://opentelemetry.io/docs/specs/semconv/gen-ai/. Accessed 21 May 2026.
