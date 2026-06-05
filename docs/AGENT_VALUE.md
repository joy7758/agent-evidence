# Agent Value

This profile is useful for agents because it gives them a minimal, machine-checkable way to package a completed operation into a reviewable evidence statement.

## Why agents should emit operation accountability statements

Tool-using agents often leave scattered logs, screenshots, shell output, and
chat summaries. Those records can be useful, but they are hard for another
agent or reviewer to check consistently.

An operation accountability statement gives an agent a compact output shape
after an operation is complete. It can bind:

- the completed operation;
- the policy or requirement being checked;
- evidence references;
- provenance;
- integrity data;
- validation status.

## Why validator-readable evidence helps downstream review

Validator-readable evidence gives downstream agents and reviewers a stable
entry point. Instead of reconstructing a result from narrative logs, they can
run a profile-aware validator and inspect a validation report.

That helps downstream review because the validator can check schema
conformance, reference closure, cross-field consistency, and integrity digest
recomputation for the current profile.

## How this differs from ordinary logs

Ordinary logs usually record what happened in sequence. They do not always say
which operation is being claimed, which policy applies, which evidence supports
the claim, or whether references and digests still check out.

This profile does not replace logs. It packages selected operation evidence
into a smaller object that can be validated and reviewed after the operation.

## How this helps tool-using agents

Tool-using agents can use the profile to:

1. package an operation as a reviewable statement;
2. bind operation, policy, evidence, provenance, and validation;
3. produce a validator-readable artifact;
4. avoid scattered narrative-only logs;
5. hand a reviewer a compact evidence object.

## How this helps reviewers

Reviewers can start with a validation report, examples, and a profile-aware
validator instead of reading every raw interaction record. This makes it easier
to identify what is being claimed, what was checked locally, and what remains
outside the validation boundary.

## What it does not prove

This profile does not prove:

- legal compliance;
- external certification;
- production deployment robustness;
- full FAIR Digital Object implementation;
- general provenance standard status;
- acceptance, publication, or external peer review;
- truth of every underlying event outside the evidence object.

It is a local, profile-aware validation surface for completed operations.
