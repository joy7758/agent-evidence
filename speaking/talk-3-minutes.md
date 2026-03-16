# 3-Minute Talk

Execution evidence should be a first-class digital object for AI runtimes.

Today, most agent systems generate logs, traces, or callback streams. Those are
useful for debugging, but they are not usually portable objects that can be
verified and reused outside the original runtime.

This repository proposes Execution Evidence Object as a bounded object model for
that missing layer. The object includes identity, ordered execution steps,
runtime context, and integrity hashes.

The specimen is not only a document. It includes a JSON schema, canonical
examples, a verification script, a human-readable demo, and export prototypes
for OpenAI Agents, LangChain, and CrewAI.

The verification path is simple. An agent run produces runtime events. Those
events are converted into an Execution Evidence Object. The object is then
checked for schema validity and hash consistency. After that, the same object
can be wrapped in an FDO-style shell with identity, metadata, integrity, and
provenance-oriented surfaces.

What matters here is not that we claim a finished standard. What matters is
that we already have a reproducible standards specimen: a named object, a
working verification path, a cross-framework export path, and an FDO-facing
mapping path.
