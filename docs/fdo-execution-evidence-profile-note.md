# Execution Evidence as a Narrow FDO Profile / Extension / Conformance Example

This note narrows the discussion to a small classification question for Fair
Digital Object (FDO) architecture work. It does not ask the FDO architecture to
adopt artificial intelligence agents as a new core object family. It asks
whether recorded execution evidence after an automated operation belongs in
the FDO discussion as a profile, an optional extension, a conformance example,
or outside the current specification scope.

`agent-evidence` is an experimental open-source repository. It is not an
official FDO specification, and it does not claim standard-body adoption. The
repository provides a working evidence profile, JSON examples, schema material,
validator behavior, and review-pack ideas that can make the classification
question concrete.

## 1. Problem boundary

The boundary is one completed automated or AI-assisted operation.

After an automated system performs an operation, reviewers often need to know
what happened without relying on the original runtime, chat session, dashboard,
or private logs. A useful evidence object should preserve enough information
for another party to inspect the operation later, verify basic integrity
references, and decide whether the result can be accepted, rejected, or sent
for deeper review.

The problem is therefore not "how should AI agents be standardized." The
problem is narrower:

- How can one operation leave a portable evidence record?
- How can that record identify the subject or digital object involved?
- How can inputs, outputs, provenance, validation results, and integrity
  references be carried together?
- How can a validator or reviewer inspect the evidence record outside the
  original runtime?

This boundary fits use cases where an automated workflow updates a record,
generates an artifact, transforms a file, produces a decision support output,
or packages a result for downstream review. The evidence object does not prove
that the operation was correct in a legal, scientific, or regulatory sense. It
only gives a stable review surface for the operation.

## 2. Non-goals

This note deliberately avoids broad standardization claims.

It is not:

- a proposal to add AI agents as a new core FDO object family;
- a general agent standard;
- a replacement for existing provenance, policy, workflow, or audit
  vocabularies;
- a claim that the current repository is an official FDO specification;
- a legal non-repudiation scheme;
- a compliance certification scheme;
- a production identity, attestation, timestamping, or forensic evidence
  system;
- a requirement that every FDO implementation support automated-agent evidence.

The intended discussion is architectural placement. If the FDO architecture
already has a better category for this material, the repository can align with
that category rather than introduce a new one.

## 3. Minimal evidence object

A minimal execution evidence object could carry these fields or their
equivalents:

- `evidence_id`: a stable identifier for the evidence record;
- `subject_ref`: the digital object, record, file, dataset, process, or other
  subject affected by the operation;
- `operation`: the action that was performed, with a bounded operation name or
  type;
- `executor_ref`: the system, agent, service, workflow, or human-supervised
  runtime that performed the operation;
- `input_refs`: references to the inputs used by the operation;
- `output_refs`: references to the outputs produced by the operation;
- `time_interval` or `timestamp`: when the operation happened or when the
  evidence record was produced;
- `provenance_refs`: links to provenance statements, workflow records, or
  runtime references;
- `integrity_checksums`: hashes, manifests, or other integrity references for
  the evidence object and related artifacts;
- `validation_result`: pass, fail, warning, or not-evaluated status from a
  declared validation method;
- `review_receipt_ref` or `review_pack_ref`: a pointer to a receipt, review
  package, or reviewer-facing summary.

The key shape is not the exact field names. The key shape is that operation,
subject, inputs, outputs, provenance, integrity, and validation are bound into
one portable review object.

## 4. Possible placement in FDO architecture

The material could be placed in several ways. The right answer depends on the
scope and extension model of the FDO architecture.

### A. Profile

Execution evidence could be discussed as a narrow FDO profile for operation
evidence records. In this placement, the evidence object would be a specialized
profile with required identity, metadata, provenance, integrity, and validation
fields.

This placement is useful if FDO profiles are expected to describe domain or
workflow-specific object shapes while preserving a common architectural model.
It keeps the proposal bounded: the evidence record is a profile, not a new
core object family.

### B. Optional extension

Execution evidence could be treated as an optional extension for systems that
need to preserve automated-operation evidence. In this placement, the FDO core
would remain unchanged, and execution evidence would be an add-on vocabulary or
payload shape.

This placement is useful if the architecture prefers to keep evidence,
workflow, policy, and validation material outside the core but still wants a
recognized extension point.

### C. Conformance example / validation fixture

Execution evidence could also be a conformance example or validation fixture.
In this placement, the evidence object is not part of the architecture
specification. It is a runnable example that tests whether an implementation
can package metadata, references, integrity checks, and validation results in a
reviewable object shape.

This placement is useful if the current architecture is not ready to classify
execution evidence as a profile or extension, but maintainers see value in a
small test case.

## 5. Conformance targets

If execution evidence is treated as a profile, extension, or fixture, the
smallest useful conformance targets could be:

### Evidence Producer

An Evidence Producer creates an evidence object after a completed operation. It
records the operation, subject, inputs, outputs, provenance references,
integrity checks, and declared validation method.

### Evidence Object

An Evidence Object is the portable record. It has stable identity, declared
schema or profile version, references to operation inputs and outputs, and
integrity material that can be inspected later.

### Evidence Validator

An Evidence Validator checks the evidence object against a schema, profile
rules, checksum manifest, and required references. It returns a machine-readable
pass/fail result with reasons.

### Evidence Consumer / Reviewer

An Evidence Consumer or Reviewer reads the evidence object and validation
receipt outside the original runtime. The consumer does not need to trust the
runtime UI. It can inspect the evidence package, validation result, and
references directly.

## 6. Minimal validation fixture

A minimal validation fixture could contain:

- one `evidence.json` file;
- one schema or profile rule file;
- one checksum manifest for referenced artifacts;
- one small set of referenced input and output artifacts;
- one expected validation receipt.

The validator would run over the fixture and output:

- `status`: pass or fail;
- `validator`: validator name and version;
- `profile`: profile or schema identifier;
- `checked_at`: validation timestamp;
- `errors`: a list of failed requirements, if any;
- `warnings`: non-blocking review notes, if any;
- `artifact_results`: checksum and reference results for included artifacts.

The purpose of the fixture is not to prove semantic correctness of the
operation. It only proves that the evidence record is structurally present,
internally reviewable, and connected to declared integrity references.

## 7. Open question for maintainers

The classification question is:

Should execution evidence after an automated operation be discussed as:

- a narrow FDO profile for evidence records;
- an optional extension;
- a conformance example / validation fixture; or
- out of scope for the current architecture specification?

Any of these answers would be useful. The goal is to place the topic in the
right category before expanding the material.
