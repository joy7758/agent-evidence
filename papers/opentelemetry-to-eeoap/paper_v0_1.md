# From Agent Telemetry to Portable Operation Evidence: A Minimal Adapter from OpenTelemetry Agent Spans to EEOAP Evidence Objects

Version: 0.1

## 1. Abstract

Runtime telemetry can describe agent execution, but it does not automatically
become portable operation evidence. This paper presents a minimal adapter that
transforms one OpenTelemetry-style GenAI agent trace into an Execution Evidence
and Operation Accountability Profile (EEOAP) v0.1 operation accountability
statement. The work is deliberately narrow: it does not define a new profile,
does not change the EEOAP schema, and does not claim legal accountability, full
runtime reconstruction, general OpenTelemetry compatibility, cross-framework
generality, or agent-output correctness.

The prototype, committed as
`c5df6ce235b7194cafe35945e4b60bd5963c8b94`, reads a local trace JSON file,
locates exactly one agent span, extracts agent identity and operation fields,
maps resolved `execute_tool` spans into evidence artifacts, preserves trace and
span provenance links, emits an EEOAP-compatible statement, and checks it with
the existing `agent-evidence validate-profile` validator. A second commit,
`ff8c794b1444527e40b587aef41597bd919b157b`, records the paper-facing evidence
closure. Evaluation uses one valid trace and four invalid traces. The valid
trace produces an EEOAP statement with validator result `ok=true` and
`issue_count=0`; invalid fixtures expose `missing_agent_span`,
`unresolved_tool_span`, `broken_parent_span_relation`, and
`missing_operation_name`. Scoped tests report
`pytest tests/test_opentelemetry_to_eeoap_adapter.py -q: 6 passed in 1.33s`;
the repository test suite reports `164 passed, 1 skipped, 15 warnings in
35.38s`.

## 2. Introduction

Agent runtimes increasingly emit structured traces. These traces are useful for
observability because they record spans, parent-child relationships, timestamps,
attributes, and error signals. However, observability telemetry and portable
operation evidence solve different problems. A trace may help diagnose a
runtime, but it is not automatically a standalone statement that an external
reviewer can validate outside that runtime.

EEOAP addresses a different layer: a compact operation accountability statement
with actor, subject, operation, policy, provenance, evidence, and validation
sections. The existing `agent-evidence` repository already contains the EEOAP
v0.1 schema and validator. The question addressed here is therefore not
whether to create another profile. The question is narrower and more concrete:
can an OpenTelemetry-style agent trace be transformed into an EEOAP-compatible
operation evidence object without changing EEOAP itself?

This paper answers that question with a minimal artifact. The adapter reads a
local trace JSON fixture, identifies one agent span, checks the operation name,
resolves `execute_tool` spans through parent-span relationships, and generates
an EEOAP v0.1 statement. The generated statement is then checked by the
existing validator. The evaluation is intentionally small: one valid fixture
demonstrates the successful path, and four invalid fixtures demonstrate
diagnostic failures at the adapter boundary.

The contribution is an adapter, a mapping model, and a local evaluation. It is
not a new governance framework and not a claim that telemetry alone proves
accountability. The result is a reproducible bridge from agent telemetry into a
validator-checkable evidence-object path.

## 3. Problem: Telemetry Is Not Portable Operation Evidence

OpenTelemetry-style traces are runtime observation material. A trace can encode
that an agent span started, that a tool span occurred under it, that timestamps
were recorded, or that an error type appeared. This makes the trace valuable
for debugging and monitoring. It does not by itself provide all properties that
an external operation evidence object needs.

Portable operation evidence needs a stable statement boundary. It needs to say
what subject is being accounted for, which actor performed the operation, what
operation was claimed, which policy or constraints define the review context,
what references and artifacts support the statement, how provenance links are
closed, and whether a validator can check the object. A raw trace does not
necessarily provide this structure in a directly reviewable shape.

The gap is especially visible for agent executions. Agent spans may carry
identity fields such as `gen_ai.agent.id`, `gen_ai.agent.name`, and
`gen_ai.agent.version`. Tool-call spans may carry `gen_ai.operation.name` equal
to `execute_tool` and tool-specific attributes. These fields can support an
evidence statement, but only after the trace is transformed into a profile that
has explicit subject references, evidence artifacts, provenance links, and
integrity digests.

The problem addressed in this paper is therefore the bounded transformation
problem: given one local OpenTelemetry-style trace with one agent span and
related tool-call spans, produce one EEOAP-compatible operation accountability
statement and show that it passes the existing EEOAP validator.

## 4. Background

### 4.1 OpenTelemetry Agent Spans

The prototype consumes local OpenTelemetry-style JSON. It supports the
`resourceSpans` / `scopeSpans` / `spans` shape used by OpenTelemetry export
formats and a simpler top-level `spans` list. The adapter extracts common span
fields including `traceId`, `spanId`, `parentSpanId`, `startTimeUnixNano`, and
`endTimeUnixNano`. It also normalizes OpenTelemetry attribute values from
objects such as `{"stringValue": "..."}`.

The agent-span boundary is identified through GenAI agent attributes. The
adapter looks for one span carrying `gen_ai.agent.id`,
`gen_ai.agent.name`, or `gen_ai.agent.version`. It requires the selected agent
span to declare `gen_ai.operation.name`. Tool-call spans are identified when
`gen_ai.operation.name` equals `execute_tool` or when the span name begins with
`execute_tool`.

Parent-span relationships matter because a tool span is not enough by itself.
For this prototype, an `execute_tool` span is considered resolved only if it is
a descendant of the selected agent span through `parentSpanId` links. This is a
local structural check; it does not assert that the tool output is correct or
that the runtime environment has been reconstructed.

### 4.2 EEOAP Evidence Objects

EEOAP v0.1 represents one operation accountability statement. The current
schema requires top-level sections for `profile`, `statement_id`, `timestamp`,
`actor`, `subject`, `operation`, `policy`, `constraints`, `provenance`,
`evidence`, and `validation`.

The existing validator checks more than JSON shape. It validates schema
conformance, reference closure, link consistency, and integrity digests. In the
generated statement, the trace input is represented as an input reference, the
mapped operation result is represented as an output reference, and span-level
evidence is represented in `evidence.artifacts[]`. Integrity fields are
recomputed through the existing EEOAP helper rather than through new validator
logic.

This is important for the paper boundary. The adapter does not create a second
EEOAP. It emits an object that the existing EEOAP validator already knows how
to check. Compatibility with the existing validator is the core artifact result.

## 5. Mapping Model

The mapping model converts trace-level and span-level information into a
schema-safe EEOAP statement.

| OpenTelemetry-style input | EEOAP v0.1 output |
|---|---|
| `traceId` / `trace_id` | `subject.id`, trace input reference, evidence locators |
| agent `spanId` / `span_id` | `operation.id`, `provenance.id`, agent-span artifact id |
| `parentSpanId` / `parent_span_id` | adapter report extraction and tool-span resolution |
| `gen_ai.agent.id` | `actor.id` |
| `gen_ai.agent.name` | `actor.name` |
| `gen_ai.agent.version` | `actor.runtime` suffix |
| agent `gen_ai.operation.name` | `operation.type` |
| resolved `execute_tool` spans | `evidence.artifacts[]` |
| span timestamps | statement timestamp and adapter report extraction |
| `error.type` | operation result status and adapter report extraction |

The generated evidence shape keeps provenance links explicit. The input trace
file is referenced by `subject.locator` and by an input entry in
`evidence.references[]`. The mapped operation result is represented as an
output reference. The selected agent span and each resolved tool span are
represented as artifacts whose locators use the form
`otel://trace/<trace-id>/span/<span-id>`.

The adapter also defines failure surfaces. If no agent span is found, it emits
`missing_agent_span`. If an `execute_tool` span is present but not reachable
from the selected agent span, it emits `unresolved_tool_span`. If a span
references a missing parent, it emits `broken_parent_span_relation`. If the
agent span lacks `gen_ai.operation.name`, it emits `missing_operation_name`.
These diagnostics are adapter diagnostics, not EEOAP schema changes.

## 6. Adapter Implementation

The implementation lives at
`tools/opentelemetry_to_eeoap_adapter.py`. It is a local Python script and does
not call a network service, external OpenTelemetry collector, hosted API, or
runtime attestation layer. The script reads one JSON file, writes one generated
EEOAP statement, writes one adapter report, and invokes the existing EEOAP
validator path.

The valid run writes:

- `generated/valid-agent-trace-eeoap-statement.json`
- `generated/valid-agent-trace-adapter-report.json`

The adapter report records the extracted trace id, agent span id, parent span
id, agent id, agent name, agent version, operation name, timestamps, error type,
and resolved tool spans. For the valid fixture, the extracted fields include:

- trace id: `aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa`
- agent span id: `1111111111111111`
- agent id: `agent:research-assistant-001`
- agent name: `research-assistant`
- agent version: `0.1.0`
- operation name: `research.answer`
- tool spans: `2222222222222222`, `3333333333333333`

The generated EEOAP statement sets `profile.name` to
`execution-evidence-operation-accountability-profile` and `profile.version` to
`0.1`. It records the trace as the subject, maps the selected agent into the
actor, maps the agent operation into `operation.type`, records tool spans as
evidence artifacts, and recomputes integrity digests before validation.

The implementation commit is:
`c5df6ce235b7194cafe35945e4b60bd5963c8b94`. The paper evidence closure commit
is: `ff8c794b1444527e40b587aef41597bd919b157b`.

## 7. Evaluation

The evaluation asks two narrow questions:

1. Can a valid OpenTelemetry-style agent trace be converted into an
   EEOAP-compatible statement that passes the existing validator?
2. Do malformed traces fail at readable adapter diagnostic surfaces before a
   misleading EEOAP statement is emitted?

### 7.1 Valid Trace

The valid fixture is
`examples/opentelemetry/valid-agent-trace.json`. It contains one agent span and
two resolved `execute_tool` spans. Running the adapter on this fixture returns
exit code 0 and writes the generated statement and report.

The generated statement was checked with:

```bash
.venv/bin/agent-evidence validate-profile \
  generated/valid-agent-trace-eeoap-statement.json
```

The observed validator result is:

- `profile`: `execution-evidence-operation-accountability-profile@0.1`
- `ok`: `true`
- `issue_count`: `0`
- passed stages: `schema`, `references`, `consistency`, `integrity`
- summary:
  `PASS execution-evidence-operation-accountability-profile@0.1 generated/valid-agent-trace-eeoap-statement.json`

This supports the paper claim that the adapter can produce a portable operation
evidence object that is checkable by the existing EEOAP validator.

### 7.2 Invalid Traces

Four invalid fixtures exercise the adapter diagnostic boundary:

| Fixture | Diagnostic label | Observed result |
|---|---|---|
| `invalid-missing-agent-span.json` | `missing_agent_span` | exit code 1, no EEOAP statement emitted |
| `invalid-unresolved-tool-span.json` | `unresolved_tool_span` | exit code 1, no EEOAP statement emitted |
| `invalid-broken-parent-span.json` | `broken_parent_span_relation` | exit code 1, no EEOAP statement emitted |
| `invalid-missing-operation-name.json` | `missing_operation_name` | exit code 1, no EEOAP statement emitted |

These negative cases matter because the adapter should not silently transform
ambiguous telemetry into an accountability statement. The failure labels mark
mapping preconditions that must hold before the EEOAP validator is asked to
check the generated object.

### 7.3 Test Results

The scoped adapter test command is:

```bash
.venv/bin/python -m pytest tests/test_opentelemetry_to_eeoap_adapter.py -q
```

Observed result:

```text
6 passed in 1.33s
```

The full repository pytest command is:

```bash
.venv/bin/python -m pytest
```

Observed result:

```text
164 passed, 1 skipped, 15 warnings in 35.38s
```

During the adapter implementation commit, the staged pre-commit checks for
`check json`, `ruff check`, and `ruff format` passed for the adapter-related
files. Full-repository `ruff check .` was not rerun during this paper-draft
step because unrelated out-of-scope lint debt already exists in pre-existing
directories such as `pd-oap/` and other generated or paper-support trees. This
should be disclosed honestly as repository lint debt outside the adapter
commit, not as an adapter failure.

## 8. Threats to Validity

The evaluation is intentionally minimal. It uses local fixtures and does not
survey all OpenTelemetry exporters, collector configurations, or vendor
implementations. The paper therefore does not claim general OpenTelemetry
implementation compatibility.

The adapter checks structural mapping preconditions. It does not reconstruct
the complete runtime environment, inspect hidden runtime state, or prove that
the agent output is correct. `error.type` is mapped as an execution signal, not
as a semantic proof about output quality.

The generated EEOAP statement passes the existing validator, but validator
success means that the statement is structurally complete, internally
consistent, reference-closed, and integrity-linked under the current schema. It
does not prove legal accountability, court-grade audit proof, regulatory
certification, or non-repudiation.

The prototype is also not a cross-framework study. It does not evaluate
LangChain, CrewAI, AutoGen, or other runtime surfaces. Such work would require
additional committed fixtures and adapter evidence. This paper keeps that
future work out of the current claim.

Finally, full-repository ruff is not a clean artifact-wide signal at this
point because unrelated pre-existing lint debt exists outside the adapter
scope. The adapter evidence therefore relies on scoped lint/pre-commit checks,
generated evidence, validator output, scoped pytest, and full pytest.

## 9. Related Work

OpenTelemetry provides a standard observability vocabulary for recording
runtime traces and spans. In this paper, OpenTelemetry-style GenAI agent spans
serve as the source telemetry. The adapter treats those spans as input material
that can support evidence construction, not as evidence by default.

EEOAP provides the target operation accountability statement shape and
validator path. This work does not redefine EEOAP. It demonstrates how
telemetry can enter the existing EEOAP evidence-object path through a bounded
mapping.

AEP and other evidence-object work in the repository address broader artifact
and evidence packaging concerns. The present contribution is narrower: it is
not a new AEP profile, not a media evidence bundle, and not a release-pack
paper. It is a telemetry-to-EEOAP adapter, mapping, and evaluation paper.

More general provenance and metadata systems also address how runtime or
workflow records can be preserved for later review. The distinguishing point
here is not a broad provenance theory, but a concrete, local artifact that
transforms an agent trace into a validator-checkable EEOAP statement without
changing the target profile.

## 10. Conclusion

Telemetry can describe agent execution, but it does not automatically become
portable operation evidence. This paper presented a minimal adapter that
transforms an OpenTelemetry-style GenAI agent trace into an EEOAP v0.1 operation
accountability statement and checks that statement with the existing EEOAP
validator.

The result is deliberately small and verifiable. One valid trace produces an
EEOAP statement that passes validation with `ok=true` and `issue_count=0`.
Four invalid traces fail at expected adapter diagnostic surfaces:
`missing_agent_span`, `unresolved_tool_span`, `broken_parent_span_relation`,
and `missing_operation_name`. Scoped adapter tests pass with `6 passed in
1.33s`, and the repository test suite passes with `164 passed, 1 skipped, 15
warnings in 35.38s`.

The paper's contribution is therefore an adapter, mapping model, and evaluation
closure. It does not claim legal accountability, full runtime reconstruction,
general OpenTelemetry compatibility, cross-framework generality, output
correctness, or a new profile. Its value is narrower: it shows that
OpenTelemetry-style agent telemetry can be transformed into portable operation
evidence under an existing EEOAP validator path.
