# Abstract

AI runtime traces are useful for debugging, but they do not automatically
provide operation-level accountability for FDO-based agent systems. A reviewer
may still be unable to answer a bounded set of questions: who executed an
operation, which object was acted on, which policy constrained the action, how
inputs and outputs were referenced, what evidence was emitted, and how an
independent third party can verify the statement. This repository addresses
that gap with a deliberately minimal artifact rather than a general governance
platform.

We introduce Execution Evidence and Operation Accountability Profile v0.1, a
small JSON profile for one operation accountability statement. The profile keeps five sections
in focus: operation, policy, provenance, evidence, and validation. It avoids
registry design, full cryptographic infrastructure, and multi-agent governance
abstractions. Instead, it defines a compact accountability statement with explicit
internal references and a bounded integrity surface. The profile requires a
named actor, a primary subject object, an operation record, a governing policy
with constraint references, provenance links, evidence references for inputs
and outputs, and a validation block that identifies the verifier pathway.

The implementation contribution is a profile-aware validator integrated into the
existing Python and CLI surface of this repository. The validator checks four
properties required for a minimal accountability loop: structural completeness,
required fields, reference closure, and consistency across policy, provenance,
and evidence links. It also recomputes a small integrity set consisting of
reference, artifact, and statement digests. The output remains intentionally
simple: machine-readable JSON, explicit error codes, and a short human-readable
summary inside one validation report.

The repository also includes one valid example, three invalid examples that
each intentionally break a single major rule class, and one runnable demo. The
demo uses a policy-constrained metadata enrichment scenario in which one input
object is loaded, transformed into one derived object, wrapped into an
accountability statement, and then validated end to end. The result is not a
claim of formal standard adoption. It is a reproducible minimal specimen for
discussing execution evidence and operation accountability with a concrete,
testable artifact rather than a broad architectural narrative.
