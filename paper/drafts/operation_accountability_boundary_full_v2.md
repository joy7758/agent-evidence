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

## 1. Introduction

Machine-actionable object systems increasingly leave behind runtime traces,
event logs, command outputs, and validation receipts. These materials are useful
for debugging and operational diagnosis, but they are not always sufficient for
later review. A reviewer may need to answer a smaller and more specific
question: what was the operation, who or what executed it, which object was
acted on, which policy and constraints were referenced, which evidence items
were emitted, and which checks make the statement independently reviewable?

This paper studies operation accountability as a first-class verification
boundary. The boundary is intentionally small. Instead of treating a complete
workflow, platform, registry, or runtime ecosystem as the paper object, the
paper asks whether one operation accountability statement can be expressed and
checked as a bounded object. The goal is not to maximize breadth. The goal is to
make the closure of one operation-level evidence statement explicit enough that
another party can inspect the statement, run the validator, and compare the
observed failures against the stated claim boundary.

The proposed profile is Execution Evidence and Operation Accountability Profile
v0.1. It binds an actor, subject, operation, policy, constraints, provenance,
evidence, and validation metadata into one JSON statement. It is paired with a
JSON Schema, a profile-aware validator, a controlled example set, a
metadata-enrichment demo, a rerun script, and a review package. These pieces are
not presented as a broad governance platform. They are presented as a small
research artifact whose value depends on alignment: the profile states what the
object is, the validator checks the expected closure properties, the examples
ground expected success and failure modes, the demo gives one concrete
operation, and the review package freezes the inspection surface.

The contribution is therefore modest but concrete. The paper frames operation
accountability as a review boundary, defines a minimal profile for that
boundary, exposes a validator path for the profile, and packages the evidence
needed to inspect the claim. The result is a paper-minimal object for checking
whether an operation accountability statement is structurally present,
internally referenced, cross-field consistent, and integrity-checkable under the
profile's current assumptions.

## 2. Problem and Scope

The scope question is deliberately narrow:

Can one operation accountability statement be expressed and checked as a bounded
verification object?

This question excludes several larger questions. It does not ask whether an
entire workflow graph is trustworthy. It does not ask whether multiple agents
were coordinated correctly. It does not ask whether a registry, network service,
or institution can provide durable trust. It does not ask whether a legal or
organizational process will accept the evidence. It asks whether one statement
can bind the minimum fields needed for review and whether the repository can
reproduce the expected validation behavior for that statement and its controlled
negative examples.

The object of study is one operation accountability statement. The statement is
not simply a log line. It includes structured references to the actor, subject,
operation, policy, constraints, provenance, evidence, and validation method. The
profile is useful only if these fields are connected. For example, an operation
may cite a subject, but the provenance and evidence sections must agree with
that subject. A policy may cite constraints, but those constraints must resolve
locally. Input and output references must close against evidence references, and
the integrity fields must be recomputable over the relevant statement surfaces.

This paper's evidence set is also bounded. It uses one valid example, three
controlled invalid examples, and one metadata-enrichment demo. The invalid
examples are not a complete test suite for all possible mistakes. They are
representative checks for three important failure surfaces: missing required
structure, an unclosed output reference, and a broken policy-evidence linkage.
The evaluation therefore supports bounded reproducibility rather than broad
coverage. The paper-minimal review package carries this same scope forward by
including only the documents, profile/schema material, examples, demo, rerun
script, tables, generated metadata, manifest, and claim boundary needed to
inspect the current contribution.

## 3. Profile Design

Execution Evidence and Operation Accountability Profile v0.1 is designed as a
small JSON profile for one operation accountability statement. The profile is
not a complete provenance model and not a complete object infrastructure. It is
a bounded statement format whose fields are chosen to make one operation
reviewable.

The top-level sections are:

| section | purpose in the statement |
| --- | --- |
| `profile` | Declares the profile name and version used by the statement. |
| `statement_id` | Gives the statement a stable identifier for citation and review. |
| `timestamp` | Records when the statement was emitted. |
| `actor` | Identifies the executor and runtime label. |
| `subject` | Identifies the object acted on, including locator and digest. |
| `operation` | Describes the action, result, policy link, subject link, and I/O refs. |
| `policy` | Names the governing policy and its constraint references. |
| `constraints` | Lists the concrete rules referenced by the policy. |
| `provenance` | Links actor, subject, operation, input refs, and output refs. |
| `evidence` | Lists referenced materials, artifacts, and integrity digests. |
| `validation` | Records validator metadata and links to evidence, provenance, and policy. |

The `profile` section fixes the profile identity and version. In v0.1, this
allows the validator to distinguish the intended statement shape from unrelated
JSON objects. The `statement_id` and `timestamp` fields make the statement
citable and temporally explicit. These fields do not establish external trust
by themselves; they provide a local review handle and a recorded emission time.

The `actor` section identifies the executor, including an identifier, type,
name, and runtime label. The runtime label is descriptive. It does not imply a
broad runtime integration claim. The `subject` section identifies the object
acted on by the operation, including a locator and digest. The locator can be a
URI, path, or persistent identifier placeholder, while the digest gives the
statement a concrete integrity surface for the subject reference.

The `operation` section is the central action record. It identifies the action,
the subject reference, the policy reference, the input references, the output
references, and the result. The operation is reviewable only if these references
connect to other sections. The `policy` section names the governing policy, and
the `constraints` section lists the concrete rules cited by that policy. This
lets a reviewer check whether the operation refers to explicit constraints
rather than an implicit or missing rule set.

The `provenance` section records the linkage among actor, subject, operation,
and input/output refs. It is narrower than a full provenance graph. Its purpose
is to check that the operation statement is internally coherent. The `evidence`
section lists references and artifacts, assigns roles such as input or output,
and includes integrity fields. The `validation` section records which validator
and method are used and links validation back to evidence, provenance, and
policy. Together, these sections form the bounded object checked by the
profile-aware validator.

## 4. Profile-Aware Validator

The profile-aware validator checks four layers: schema conformance, reference
closure, cross-field consistency, and integrity digest recomputation. These
layers are ordered from structural checks toward more semantic local checks.
The validator is exposed through the command-line validation path:

```bash
agent-evidence validate-profile <profile-json>
```

Schema conformance checks whether the JSON instance satisfies the declared
schema. This includes required top-level sections, required nested fields,
constant profile name and version, array shapes, string lengths, enumerated
result status values, and SHA-256 digest patterns. A missing required field or
invalid shape is reported as a schema-level violation. In the paper-minimal
path, the controlled example `examples/invalid-missing-required.json` grounds
this failure surface with the primary error code `schema_violation`.

Reference closure checks whether local identifiers resolve within the statement
where required. Operation input and output references must resolve to evidence
references. Policy constraint references must resolve to listed constraints.
Validation references must resolve to evidence, provenance, and policy. This
layer is important because an operation statement can look complete while still
pointing to missing local identifiers. In the paper-minimal path,
`examples/invalid-unclosed-reference.json` grounds the representative failure
`unresolved_output_ref`.

Cross-field consistency checks whether linked fields agree across operation,
policy, provenance, evidence, and validation. For example, the operation's
policy reference should align with the policy section, the evidence policy
reference should refer to the same policy, and validation should refer to the
same evidence, provenance, and policy objects. This layer is narrower than
truth verification. It does not decide whether the external world matched the
claim. It checks whether the local statement is internally coherent. The
controlled example `examples/invalid-policy-link-broken.json` grounds the
representative failure `unresolved_evidence_policy_ref`.

Integrity digest recomputation checks canonical digests for the evidence
references, artifacts, and statement core. This layer gives the statement a
minimal tamper-detection surface for the fields under the profile's current
scope. It does not establish external identity, signing, timestamping, or
durable trust. It simply checks whether the digests recorded in the statement
match recomputed canonical digests over the expected local surfaces.

These four layers are intentionally small. They provide a repeatable path for
checking one statement rather than a general assurance framework. Their value is
that they turn a paper claim into a concrete command path with expected outputs
for one valid example and three controlled invalid examples.

## 5. Paper-Minimal Artifact Package

The paper-minimal artifact package turns the profile and validator path into an
inspection package. It is created through the repository's review-pack command:

```bash
agent-evidence review-pack create --paper-minimal --out dist/review-pack-paper-minimal.zip
```

The package includes boundary docs, profile/schema material, examples, the
metadata-enrichment demo, paper tables, the reproduce script, generated
metadata, `MANIFEST.json`, `CLAIM_BOUNDARY.md`, and `PACKAGE_INFO.json`.
`MANIFEST.json` records package file paths, file sizes, and SHA-256 digests for
the package payload. It excludes itself from the digest list to avoid a
self-referential checksum. `CLAIM_BOUNDARY.md` repeats the non-claims in the
package so the review surface carries the same boundary as the paper.
`PACKAGE_INFO.json` records package metadata such as the package name, profile
name, profile version, git commit, included examples, and non-claims.

The paper-minimal review package is an inspection package, not a standalone
software distribution. The included reproduction instructions state that
commands are intended to be run from the repository root after installing
agent-evidence. This distinction matters. The package freezes the paper-minimal
review surface, but it does not claim to include every dependency, environment,
or service needed for a complete independent software release. Its purpose is
to help reviewers inspect whether the profile, validator, examples, demo, rerun
script, tables, and boundary documents match the paper's claims.

The review package also supports auditability of the package itself. A reviewer
can inspect `MANIFEST.json`, recompute SHA-256 digests over the listed files,
and check that the package includes the required files. The review-package test
path validates these properties for the paper-minimal package. This keeps the
packaging layer aligned with the paper's main argument: small boundaries are
more useful when their contents and checks are explicit.

## 6. Evaluation

The evaluation is limited to the paper-minimal path. It validates one valid
example, three controlled invalid examples, and one metadata-enrichment demo.
The evaluation is not a benchmark of many systems, not a comparison across
frameworks, and not evidence of deployed operation.

The valid example is `examples/minimal-valid-evidence.json`. It is expected to
return `ok: true` and `issue_count: 0` when run through the profile-aware
validator. This result shows that the minimal statement shape can satisfy the
schema, close the required references, maintain cross-field consistency, and
match the integrity digest checks under the profile's current assumptions.

The three invalid examples are expected to exit nonzero with stable primary
codes. `examples/invalid-missing-required.json` is expected to produce
`schema_violation`. `examples/invalid-unclosed-reference.json` is expected to
produce `unresolved_output_ref`. `examples/invalid-policy-link-broken.json` is
expected to produce `unresolved_evidence_policy_ref`. These cases are chosen to
ground three representative failure modes rather than to exhaust the space of
possible invalid statements.

The metadata-enrichment demo is expected to end with a `PASS` summary line. The
demo provides a concrete operation in which a metadata-enrichment actor emits a
derived object under a policy and evidence context. The demo is not used to
claim broad runtime coverage. It is used to show how the profile can be applied
to one small operation.

The clean rerun script combines these checks into a single paper-facing command
path:

```bash
bash scripts/reproduce_paper_minimal.sh
```

Passing this script supports bounded reproducibility only. It means that the
repository can rerun the current profile, validator, examples, demo, and
summary generation path. It does not imply that the profile has been validated
across many runtimes, deployed in production, or accepted as a complete object
interoperability layer.

## 7. Related Work

Logs and traces are the closest operational baseline. They provide event-level
or span-level visibility into execution. They are useful for debugging,
monitoring, and incident reconstruction. However, a log or trace stream does
not necessarily define a compact review object for one operation. The profile
in this paper complements logs and traces by asking which fields need to be
bound into a single operation accountability statement and which local checks
can be rerun over that statement.

W3C PROV provides a general model for representing provenance relationships
among entities, activities, and agents. It is broader and more general than the
paper-minimal object here. This paper does not replace provenance models.
Instead, it uses a narrow provenance section inside one statement to check that
actor, subject, operation, input refs, and output refs agree with the rest of
the profile. The focus is not general provenance expressiveness, but a small
operation-level review boundary.

in-toto and SLSA address supply-chain integrity for software artifacts. They
make important distinctions about steps, materials, products, provenance, and
levels of assurance in build and release pipelines. The profile here is
different in scope. It is not a supply-chain level framework and does not
define a build-pipeline assurance level. It borrows the general insight that
artifact integrity and step accountability benefit from explicit metadata and
verifiable links, then applies that insight to one operation accountability
statement.

FDO and DOIP work concerns digital objects, persistent identifiers, and
interfaces for object interaction. This paper uses FDO-oriented language only
as a local framing for object references and reviewable evidence links. It does
not claim complete FDO interoperability or DOIP implementation. The profile is
better read as a small operation-level statement format that may be discussed
alongside object-system work, not as a full object infrastructure.

## 8. Threats to Validity

The main threat to validity is scale. The paper-minimal path is based on one
implementation, one valid example, three invalid examples, and one
metadata-enrichment demo. This is sufficient for checking the current artifact
boundary, but it is not sufficient for broad empirical claims about many
systems.

A second threat is example coverage. The controlled invalid examples target
schema conformance, reference closure, and policy-evidence linkage. They do not
cover every possible invalid statement, every digest mismatch scenario, or
every possible misuse of operation accountability metadata. Additional examples
would be needed before claiming broader validator coverage.

A third threat is runtime coverage. The paper-minimal path does not validate
the profile across many frameworks or execution environments. The runtime label
inside the statement is descriptive within the current example. It is not a
claim that the profile has been integrated across a broad runtime ecosystem.

A fourth threat is deployment context. The artifact is a repository-backed
research object with a command-line validator, examples, demo, rerun script,
and review package. It is not a production deployment. It does not establish
operational monitoring, service-level guarantees, external trust anchors,
access-control policy, key management, or institutional acceptance.

A fifth threat is legal and interoperability scope. The profile does not claim
legal non-repudiation. It also does not claim complete FDO interoperability.
The digest checks are useful for local integrity review, but they do not by
themselves establish signatures, trusted timestamps, external identity, or
multi-party assurance. The paper's claims should therefore be read as bounded
and artifact-level.

In short, there is no broad cross-framework validation, no production
deployment, no legal non-repudiation, no complete FDO interoperability, and no
broad runtime integration coverage. The paper also makes no compliance approval
claim.

Finally, the review package itself is an inspection package. It freezes a
review surface for the paper-minimal path, but it is not a complete independent
distribution of all software dependencies or a substitute for installing and
running the repository. Reviewers should evaluate whether the package contents
match the paper's boundary and whether the rerun path behaves as claimed.

## 9. Conclusion

Operation accountability can be reduced to a small independently checkable
boundary when profile, validator, examples, demo, rerun script, and review
package are aligned. This paper presents that boundary for Execution Evidence
and Operation Accountability Profile v0.1. The contribution is intentionally
narrow: one statement format, one validator path, one valid example, three
controlled invalid examples, one demo, and one paper-minimal review package.

The main result is closure rather than breadth. The profile defines the object,
the validator checks the object's structure and local links, the examples
ground expected pass and fail behavior, the demo supplies one concrete
operation, the rerun script makes the checks repeatable, and the review package
freezes the inspection surface. This combination gives reviewers a compact
artifact for assessing the paper's specific claim without implying broader
system guarantees.

## Appendix A: Reproduction Commands

Run the full paper-minimal rerun from the repository root:

```bash
bash scripts/reproduce_paper_minimal.sh
```

The individual validator commands are:

```bash
agent-evidence validate-profile examples/minimal-valid-evidence.json
agent-evidence validate-profile examples/invalid-missing-required.json
agent-evidence validate-profile examples/invalid-unclosed-reference.json
agent-evidence validate-profile examples/invalid-policy-link-broken.json
python demo/run_operation_accountability_demo.py
```

Expected outcomes:

| command | expected exit | expected result |
| --- | ---: | --- |
| `agent-evidence validate-profile examples/minimal-valid-evidence.json` | 0 | `ok: true` / `issue_count: 0` |
| `agent-evidence validate-profile examples/invalid-missing-required.json` | nonzero | `schema_violation` |
| `agent-evidence validate-profile examples/invalid-unclosed-reference.json` | nonzero | `unresolved_output_ref` |
| `agent-evidence validate-profile examples/invalid-policy-link-broken.json` | nonzero | `unresolved_evidence_policy_ref` |
| `python demo/run_operation_accountability_demo.py` | 0 | `PASS` summary line |

## Appendix B: Claim Boundary

The paper does not claim:

- registry design
- multi-agent orchestration
- full FDO interoperability
- full cryptographic trust fabric
- legal non-repudiation
- production deployment
- broad platform governance
- broad runtime integration coverage
- compliance approval

These non-claims are part of the paper-minimal boundary. They should be read as
constraints on interpretation. Passing the rerun validates the bounded artifact
path only.

## Appendix C: Artifact Package Contents

The paper-minimal review package includes the following content classes:

| content class | representative files |
| --- | --- |
| boundary docs | `docs/PAPER_BOUNDARY_FREEZE.md`, `docs/PAPER_MAINLINE.md`, `docs/REPRODUCE_PAPER_MINIMAL.md` |
| profile/schema material | `spec/execution-evidence-operation-accountability-profile-v0.1.md`, `schema/execution-evidence-operation-accountability-profile-v0.1.schema.json` |
| examples | `examples/minimal-valid-evidence.json`, three controlled invalid examples |
| demo | `demo/run_operation_accountability_demo.py` |
| paper tables | `paper/tables/minimal_profile_tables.md` |
| reproduction script | `scripts/reproduce_paper_minimal.sh` |
| generated package metadata | `MANIFEST.json`, `CLAIM_BOUNDARY.md`, `PACKAGE_INFO.json` |

The package is intended for inspection. Reproduction commands are intended to
be run from the repository root after installing agent-evidence.
