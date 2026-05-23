# From Agent Telemetry to Portable Operation Evidence: A Minimal Adapter from OpenTelemetry Agent Spans to EEOAP Evidence Objects

Version: 0.3 submission-prep draft

## Abstract

OpenTelemetry-style agent traces describe runtime behavior, but telemetry is
not automatically portable operation evidence. This paper presents a minimal
OpenTelemetry-to-EEOAP adapter that transforms a local agent trace into an
Execution Evidence and Operation Accountability Profile (EEOAP) operation
accountability statement. The implementation uses committed local fixtures,
generates an EEOAP-compatible statement, and routes that statement into the
existing profile-aware EEOAP validator. Evaluation is intentionally bounded:
one valid trace demonstrates successful transformation and validator
acceptance, while four invalid traces demonstrate diagnostic failure surfaces
for missing agent spans, unresolved tool spans, broken parent relations, and
missing operation names. Scoped adapter tests pass, and the paper-facing
evidence closure records reproducible commands and test results. The claim is
narrow: the prototype does not prove legal accountability, reconstruct the full
runtime environment, establish general OpenTelemetry implementation
compatibility, demonstrate cross-framework generality, or prove agent-output
correctness.

## Introduction

Agent runtimes increasingly emit structured telemetry. Span traces can record
operation names, agent identifiers, parent-child relationships, timestamps,
tool calls, and error signals. These records are useful for observability, but
they do not by themselves define an externally reviewable evidence object.
Reviewable operation evidence needs a stable statement boundary, provenance
links, evidence references, integrity checks, and a validator-aware structure.

EEOAP already provides a compact target shape for operation accountability
statements. The current `agent-evidence` repository includes the EEOAP v0.1
schema and existing `validate-profile` path. This paper therefore does not
define another profile. It asks a narrower question: can OpenTelemetry-style
agent telemetry be transformed into an EEOAP-compatible portable operation
evidence statement without changing the target EEOAP schema?

The implemented adapter answers this question with a deliberately small
artifact. It reads a local trace JSON file, locates one accountable agent span,
requires an operation name, resolves `execute_tool` spans through parent-span
links, preserves trace and span provenance through evidence locators, emits an
EEOAP-compatible statement, and validates that statement with the existing
EEOAP validator. The adapter prototype is committed as
`c5df6ce235b7194cafe35945e4b60bd5963c8b94`; the paper evidence closure is
committed as `ff8c794b1444527e40b587aef41597bd919b157b`.

This paper makes four contributions:

- C1. A bounded telemetry-to-evidence mapping model.
- C2. A minimal adapter from OpenTelemetry-style agent spans to
  EEOAP-compatible statements.
- C3. A controlled valid/invalid fixture set and diagnostic surface.
- C4. A paper-facing evidence closure with reproducible commands and scoped
  test results.

The contribution is not OpenTelemetry itself [OpenTelemetry-GenAI], not the
EEOAP profile itself [EEOAP-Artifact], and not a broad runtime evidence bundle
framework [AEP-Artifact]. It is the adapter, mapping, and evaluation layer that
connects agent telemetry to portable operation evidence.

## Problem: Telemetry Is Not Portable Operation Evidence

Telemetry records observations about a runtime. An OpenTelemetry-style trace
may say that a span started, that another span was its child, that an agent
identifier was present, or that an `error.type` attribute was emitted. Such
records are useful for debugging and monitoring, but they do not automatically
answer the evidence question: what operation is being accounted for, what
object is the subject, what evidence references support the statement, and can
an independent validator check it?

Portable operation evidence needs explicit structure. The statement must bind
an actor to a subject and operation, preserve provenance, carry evidence
references and artifacts, and expose enough consistency for validation. A raw
trace can supply material for such a statement, but it must first be
interpreted and transformed. The adapter's role is to perform this bounded
transformation rather than treating telemetry as evidence by default.

This distinction matters for agent systems because tool use can be nested,
ambiguous, or unattached. A tool span that is not reachable from the selected
agent span should not become evidence for that agent operation. Likewise, an
agent span without an operation name is not yet a well-formed operation
accountability claim. The prototype therefore treats missing or inconsistent
mapping inputs as adapter failures, not as EEOAP schema changes.

## Background

OpenTelemetry defines structured telemetry concepts for traces, spans, span
attributes, and semantic conventions [OpenTelemetry-GenAI]. The agent-oriented
semantic surface includes fields such as agent identity attributes, operation
names, timestamps, parent span identifiers, and error attributes
[OpenTelemetry-Agent-Spans]. This paper uses local OpenTelemetry-style JSON
fixtures rather than a live collector or external service.

EEOAP defines an operation accountability statement shape with sections for
actor, subject, operation, policy, constraints, provenance, evidence, and
validation [EEOAP-Artifact]. The existing validator checks schema conformance,
reference closure, consistency, and integrity. The underlying JSON validation
model is related to JSON Schema 2020-12 [JSON-Schema-2020-12], while the
provenance motivation is adjacent to established provenance work such as W3C
PROV [W3C-PROV].

AEP and related repository artifacts address broader evidence-object and
runtime evidence bundle concerns [AEP-Artifact]. This paper is narrower. It
does not introduce a bundle format, a release process, or a new evidence
profile. It shows how one telemetry source can enter an existing EEOAP
statement and validator path.

## Mapping Model

The mapping model converts selected trace and span fields into a schema-safe
EEOAP statement. It is intentionally bounded and local: it is not a general
OpenTelemetry compliance model, and it does not attempt to support every
runtime exporter.

| OpenTelemetry source | Adapter extraction | EEOAP target | Validation relevance | Failure if absent or inconsistent |
|---|---|---|---|---|
| `trace_id` / `traceId` | Read from spans and used to select same-trace spans. | `subject.id`, input reference, evidence locators. | Binds the generated statement to one trace input. | Malformed span cannot be mapped. |
| `span_id` / `spanId` | Read from agent and tool spans. | `operation.id`, `provenance.id`, artifact ids. | Gives stable span-level provenance anchors. | Malformed span cannot be mapped. |
| `parent_span_id` / `parentSpanId` | Used for parent closure and tool-span ancestry. | Adapter report and provenance interpretation. | Prevents unattached tool spans from becoming evidence. | `broken_parent_span_relation` or `unresolved_tool_span`. |
| `gen_ai.agent.id` | Extracted from the selected agent span. | `actor.id`. | Identifies the accountable agent actor. | Absence of all `gen_ai.agent.*` fields yields `missing_agent_span`. |
| `gen_ai.agent.name` | Extracted from the selected agent span. | `actor.name`. | Provides readable actor identity. | Missing name alone can use adapter fallback. |
| `gen_ai.agent.version` | Extracted from the selected agent span. | `actor.runtime` suffix. | Preserves version context without schema change. | Missing version alone is allowed. |
| `gen_ai.operation.name` | Required on the selected agent span. | `operation.type`. | Defines the accountable operation. | `missing_operation_name`. |
| execute tool span | Identified by `gen_ai.operation.name=execute_tool` or span-name prefix. | `evidence.artifacts[]`. | Records supporting tool-call spans. | `unresolved_tool_span` if not descended from the agent span. |
| timestamp | Extracted from span start/end timestamps. | statement timestamp and adapter report fields. | Preserves timing context. | Missing timestamp reduces context but does not fail the minimal mapping. |
| `error.type` | Extracted when present. | operation result status and adapter report. | Carries runtime failure signal. | Missing value is not treated as output correctness proof. |

This mapping is more than field copying. The adapter identifies the accountable
operation span, checks parent-child span consistency, resolves tool spans,
preserves provenance links, emits an EEOAP-compatible statement, recomputes
integrity fields, and routes the result into the existing validator.

## Adapter Implementation

The implementation lives at
`tools/opentelemetry_to_eeoap_adapter.py`. It is a local script and does not
call a network service, OpenTelemetry Collector, hosted API, or external
attestation layer. The script reads one trace JSON file, writes one generated
EEOAP statement, writes one adapter report, and invokes the existing
`agent-evidence validate-profile` path.

The valid fixture is `examples/opentelemetry/valid-agent-trace.json`. Its
generated outputs are:

- `generated/valid-agent-trace-eeoap-statement.json`
- `generated/valid-agent-trace-adapter-report.json`

The valid trace includes trace id `aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa`, agent span
id `1111111111111111`, agent id `agent:research-assistant-001`, agent name
`research-assistant`, agent version `0.1.0`, operation name
`research.answer`, and two resolved tool spans:
`2222222222222222` and `3333333333333333`.

The generated EEOAP statement records the trace as the subject, the agent as
the actor, the operation name as `operation.type`, the trace as an input
reference, the mapped operation result as an output reference, and the selected
agent/tool spans as evidence artifacts with `otel://trace/.../span/...`
locators. Integrity fields are recomputed through the existing EEOAP helper.

## Evaluation

The evaluation is intentionally limited to the adapter claim. It asks whether a
valid trace can produce a validator-accepted EEOAP statement and whether
invalid traces fail at meaningful adapter diagnostics.

| Artifact | Role | Evidence path | Result |
|---|---|---|---|
| valid OpenTelemetry fixture | Positive input case | `examples/opentelemetry/valid-agent-trace.json` | Adapter run succeeds. |
| generated EEOAP statement | Portable operation evidence output | `generated/valid-agent-trace-eeoap-statement.json` | EEOAP-compatible statement emitted. |
| existing EEOAP validator | Profile-aware checker | `agent-evidence validate-profile generated/valid-agent-trace-eeoap-statement.json` | `ok=true`, `issue_count=0`; stages `schema`, `references`, `consistency`, `integrity` pass. |
| invalid fixtures | Negative mapping cases | `examples/opentelemetry/invalid-*.json` | Expected diagnostics: `missing_agent_span`, `unresolved_tool_span`, `broken_parent_span_relation`, `missing_operation_name`. |
| scoped pytest result | Adapter regression check | `pytest tests/test_opentelemetry_to_eeoap_adapter.py -q` | `6 passed` in the latest v0.3 scoped run. |
| full pytest result | Repository test context | `pytest` | Evidence closure records `164 passed, 1 skipped, 15 warnings in 35.38s`. |
| repository hygiene note | Lint boundary disclosure | full-repository Ruff | Not rerun for v0.3 due to unrelated pre-existing out-of-scope lint debt. |

The invalid fixtures are central to the evaluation. They show that the adapter
does not blindly convert telemetry into evidence. It rejects traces without an
agent span, tool spans that are not attached to the selected agent span, spans
with broken parent references, and agent spans lacking an operation name.

### Artifact and Repository Hygiene

Adapter-specific tests passed, and the existing EEOAP validator accepted the
generated statement. Full repository Ruff was not rerun for v0.3 because
unrelated pre-existing lint debt remains in out-of-scope directories such as
`pd-oap/` and SoftwareX-related paper-support trees. This is disclosed as
repository hygiene debt, not as an adapter failure.

## Threats to Validity

The evaluation uses local fixtures and does not survey all OpenTelemetry
exporters, collector configurations, vendor implementations, or
semantic-convention variants. The paper therefore does not claim general
OpenTelemetry implementation compatibility.

The adapter checks structural mapping preconditions. It does not reconstruct
the complete runtime environment, inspect hidden runtime state, or prove that
the agent output is correct. `error.type` is mapped as an execution signal, not
as a semantic proof about output quality.

The generated EEOAP statement passes the existing validator, but validator
success means that the statement is structurally complete, internally
consistent, reference-closed, and integrity-linked under the current schema. It
does not prove legal accountability, court-grade audit proof, regulatory
certification, or non-repudiation.

The prototype is not a cross-framework study. It does not evaluate LangChain,
CrewAI, AutoGen, or other runtime surfaces. Such work would require additional
committed fixtures and adapter evidence and is intentionally outside v0.3.

## Related Work

OpenTelemetry provides the observability vocabulary used as the source side of
this paper [OpenTelemetry-GenAI]. The agent-span material motivates the fields
used by the adapter, including agent identity, operation name, span parentage,
timestamps, and error attributes [OpenTelemetry-Agent-Spans].

EEOAP provides the target operation accountability statement and validation
path [EEOAP-Artifact]. This paper does not redefine EEOAP. It demonstrates how
telemetry can enter the existing EEOAP evidence-object path through a bounded
mapping and adapter.

AEP and related artifact work provide broader context for evidence objects and
runtime evidence bundles [AEP-Artifact]. This paper is narrower: it is not a
new AEP profile and not a bundle/release paper. Artifact review expectations
and reproducibility framing are adjacent to artifact badging practices
[ACM-Artifact-Badging], but final venue-specific packaging is not attempted in
this draft.

JSON Schema and provenance standards provide additional context for validating
structured objects and preserving provenance relationships [JSON-Schema-2020-12]
[W3C-PROV]. The current contribution remains practical and artifact-centered:
a local adapter that converts agent telemetry into a validator-checkable EEOAP
statement.

## Conclusion

OpenTelemetry-style agent telemetry can describe execution, but it does not
automatically become portable operation evidence. This paper presented a
minimal adapter that transforms one local OpenTelemetry-style agent trace into
an EEOAP-compatible operation accountability statement and validates that
statement with the existing EEOAP validator.

The result is small but concrete. One valid fixture produces a statement that
passes validation with `ok=true` and `issue_count=0`. Four invalid fixtures
exercise the adapter boundary through `missing_agent_span`,
`unresolved_tool_span`, `broken_parent_span_relation`, and
`missing_operation_name`. The paper preserves its non-claims: no legal
accountability proof, no full runtime reconstruction, no general
OpenTelemetry compatibility claim, no cross-framework generality claim, no
agent-output correctness claim, and no new profile claim.

The value of the work is therefore not conceptual expansion. It is a short,
reproducible adapter and evidence closure showing how agent telemetry can enter
an existing portable operation evidence profile.
