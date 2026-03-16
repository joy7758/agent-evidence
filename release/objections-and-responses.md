# Objections and Responses

## Isn’t this just logging or tracing?

No. Logging records events inside a runtime. This prototype packages execution
evidence as a portable object with integrity checks.

## Why treat execution evidence as an object?

Because an object can be exported, verified, compared, and reused more cleanly
than framework-native trace output.

## What is verifiable today?

The canonical specimen object is verifiable today through schema checks and hash
recomputation.

## Why is FDO relevant?

Because FDO provides an object-oriented way to discuss identity, metadata,
integrity, and provenance. Those are already visible in this specimen.

## What is new beyond observability tooling?

The new step is not another tracing tool. The new step is an object model for
execution evidence.

## How portable is it?

The prototype already includes export examples for OpenAI Agents, LangChain,
and CrewAI.

## What is implemented now and what is future work?

Implemented now:

- spec
- schema
- example objects
- verification
- FDO-style wrapper example
- cross-framework prototype exporters

Future work:

- stable conformance profile
- broader interoperability checks
- registry-facing packaging

## What are the current limitations?

The work is still a specimen, not a final standard. It is intentionally small
and does not yet define production governance or community-approved profiles.

## What would broader standardization require?

Stable field rules, conformance tests, portability criteria, provenance
requirements, and community review.

## How should sensitive runtime content be handled?

Sensitive content should be filtered or replaced before wider distribution. The
current specimen focuses on object shape, integrity, and portability.

## What this work does not claim

It does not claim formal adoption, production registry deployment, or complete
coverage of all runtime evidence use cases.
