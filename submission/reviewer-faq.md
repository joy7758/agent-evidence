# Reviewer FAQ

## Isn’t this just logging or tracing?

No. Logs and traces are runtime-native records. Execution Evidence Object is a
bounded export object with identity, integrity hashes, and a verification path.

## Why should execution evidence be treated as an object?

Because object form makes the evidence portable, verifiable, and reusable
across runtimes and review contexts.

## What is actually verifiable here?

The current specimen verifies schema validity and recomputed integrity hashes
for the canonical object instance.

## Why is FDO relevant rather than optional?

FDO is relevant because this work frames execution evidence in object-oriented
terms: identity, metadata, integrity, and provenance-oriented structure.

## What is the novelty beyond existing observability tooling?

The novelty is not better observability dashboards. The novelty is treating AI
runtime evidence itself as a portable object specimen with explicit verification
and standards-facing mapping.

## How portable is the object across frameworks?

The repository already shows prototype export paths for OpenAI Agents,
LangChain, and CrewAI toward one shared object profile.

## What is implemented today versus future work?

Implemented today:

- object model
- schema
- canonical examples
- verification
- FDO-style wrapper example
- cross-framework export prototypes

Future work:

- stable community conformance profile
- persistent identifier binding
- broader interoperability testing

## What are the current limitations?

The specimen is still a proposal prototype. It does not yet define a
community-approved profile, registry deployment, or production-grade sensitive
content policies.

## What would be needed for broader standardization?

Broader standardization needs stable required fields, clearer provenance rules,
interoperability tests, and community review across frameworks.

## How should sensitive runtime content be handled?

Sensitive content should be minimized, redacted, or replaced with policy-aware
references before packaging evidence for broader distribution.

## What this work does not claim

This work does not claim formal standards-body endorsement, registry deployment,
universal interoperability, or replacement of full observability systems.
