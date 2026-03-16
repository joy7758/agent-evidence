# 5-Minute Talk

Execution evidence should be a first-class digital object for AI runtimes.

The reason is that runtime activity is becoming more autonomous, but the way we
represent what happened after a run is still mostly tied to logs, traces, and
framework-specific exports. Those records help developers, but they do not
automatically become portable objects for verification, review, or future
standardization.

Execution Evidence Object is our specimen answer to that gap. We define a
bounded object with identity, execution steps, runtime context, and integrity
hashes. The object is small enough to inspect, but structured enough to be
validated and reused.

The repository demonstrates this in several layers. There is a specification
and schema for the object. There are canonical example files, including a
verified execution evidence object and an FDO-style object wrapper. There is a
verification script that recomputes hashes and checks integrity. There is also
a human-readable demo that prints the specimen in a way non-specialists can
follow.

We also show portability. OpenAI Agents, LangChain, and CrewAI each have a
prototype export path that converts runtime activity into the same evidence
object profile. That matters because a standard specimen should not look like a
single-framework private format.

FDO relevance enters at the object boundary. Once the runtime evidence is
bounded and verified, it can be read through identity, metadata, integrity, and
provenance-oriented surfaces. That is the bridge from runtime evidence to a
digital object discussion.

This work does not claim formal standards-body adoption or production registry
deployment. It claims something narrower and more concrete: we already have a
reproducible specimen for discussing execution evidence as a first-class digital
object.
