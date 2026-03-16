# 90-Second Talk

The problem is that AI runtimes produce logs and traces, but those outputs are
usually bound to one framework and one debugging workflow.

Our proposal is Execution Evidence Object, a portable and verifiable object for
AI runtime evidence.

Instead of leaving execution records as raw trace data, we turn them into a
bounded object with identity, steps, context, and integrity hashes.

Verification matters because the object is not only exported, it is checked. We
validate the schema, recompute the hashes, and show that the specimen object is
internally consistent.

FDO relevance matters because this gives execution evidence an object-facing
identity, metadata, integrity, and provenance surface. That makes the runtime
evidence legible in digital object terms rather than only as engineering logs.
