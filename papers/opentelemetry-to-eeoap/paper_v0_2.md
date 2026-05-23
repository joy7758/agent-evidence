# From Agent Telemetry to Portable Operation Evidence: A Minimal Adapter from OpenTelemetry Agent Spans to EEOAP Evidence Objects

Version: 0.2

## 1. Abstract

Runtime telemetry can describe agent execution, but it does not automatically
become portable operation evidence. This paper presents a minimal adapter that
transforms one OpenTelemetry-style GenAI agent trace into an Execution Evidence
and Operation Accountability Profile (EEOAP) v0.1 operation accountability
statement. The central contribution is not OpenTelemetry itself and not EEOAP
itself. The contribution is the bounded adapter path that connects
OpenTelemetry-style agent telemetry to EEOAP-compatible portable operation
evidence and routes the generated statement into the existing EEOAP validator.

The prototype, committed as
`c5df6ce235b7194cafe35945e4b60bd5963c8b94`, reads a local trace JSON file,
locates exactly one accountable agent span, extracts agent identity and
operation fields, checks parent-child span consistency, maps resolved
`execute_tool` spans into evidence artifacts, preserves trace and span
provenance links, emits an EEOAP-compatible statement, and checks it with the
existing `agent-evidence validate-profile` validator. The paper evidence
closure, committed as `ff8c794b1444527e40b587aef41597bd919b157b`, records the
commands, fixtures, generated outputs, validation result, and test results used
as evidence.

Evaluation is intentionally small and limitations-first. One valid trace
demonstrates the successful path; four invalid traces demonstrate adapter
failure surfaces. The valid trace produces an EEOAP statement with validator
result `ok=true` and `issue_count=0`. Invalid fixtures expose
`missing_agent_span`, `unresolved_tool_span`, `broken_parent_span_relation`,
and `missing_operation_name`. Scoped tests report
`pytest tests/test_opentelemetry_to_eeoap_adapter.py -q: 6 passed in 2.11s`.
The broader repository pytest result recorded for the evidence closure is
`164 passed, 1 skipped, 15 warnings in 35.38s`. The paper does not claim legal
accountability, full runtime reconstruction, general OpenTelemetry
implementation compatibility, cross-framework generality, agent-output
correctness, or a new profile.

## 2. Introduction

Agent runtimes increasingly emit structured traces. These traces are useful for
observability because they record spans, parent-child relationships,
timestamps, attributes, and error signals. However, observability telemetry and
portable operation evidence solve different problems. A trace may help
diagnose a runtime, but it is not automatically a standalone statement that an
external reviewer can validate outside that runtime.

EEOAP addresses a different layer: a compact operation accountability
statement with actor, subject, operation, policy, provenance, evidence, and
validation sections. The existing `agent-evidence` repository already contains
the EEOAP v0.1 schema and validator. The question addressed here is therefore
not whether to create another profile. The question is narrower and more
concrete: can an OpenTelemetry-style agent trace be transformed into an
EEOAP-compatible operation evidence object without changing EEOAP itself?

This paper answers that question with a minimal artifact. The adapter reads a
local trace JSON fixture, identifies one accountable agent span, checks that
the operation name exists, resolves `execute_tool` spans through parent-span
relationships, and generates an EEOAP v0.1 statement. The generated statement
is then checked by the existing validator. The evaluation is intentionally
small: one valid fixture demonstrates the successful path, and four invalid
fixtures demonstrate diagnostic failures at the adapter boundary.

This is not merely a claim that telemetry fields can be copied into another
JSON document. The adapter performs a bounded interpretation step: it selects
the accountable operation span, checks whether tool spans are structurally
attached to that operation, preserves trace and span provenance as evidence
locators, emits a schema-compatible EEOAP statement, and routes the result into
an existing profile-aware validator. The difference between telemetry and
operation evidence is exactly this transformation into a reviewable,
validator-checkable statement.

The contribution is an adapter, a mapping model, and a local evaluation. It is
not a new governance framework and not a claim that telemetry alone proves
accountability. The result is a reproducible bridge from agent telemetry into a
validator-checkable evidence-object path.

### 2.1 Novelty and Relationship to Prior Work

The novelty is deliberately scoped. Earlier EEOAP work defines the evidence
object and validator. This paper studies how telemetry enters that evidence
object. Earlier AEP work studies runtime evidence bundles and broader artifact
packaging concerns. This paper studies span-to-operation-evidence
transformation.

Therefore, this paper is not a duplicate EEOAP paper, not a duplicate AEP
paper, and not a new profile paper. Its contribution is the adapter/mapping
layer and the associated evaluation: a bounded path from OpenTelemetry-style
agent spans to EEOAP-compatible portable operation evidence under the existing
validator.

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
to check. Compatibility with the existing validator is the core artifact
result.

## 5. Mapping Model

The mapping model converts trace-level and span-level information into a
schema-safe EEOAP statement. It is not a complete OpenTelemetry compliance
model. It is a small set of extraction, closure, and validation-relevant rules
for turning one agent trace into one operation accountability statement.

| OpenTelemetry source | Adapter extraction | EEOAP target | Validation relevance | Failure if absent or inconsistent |
|---|---|---|---|---|
| `trace_id` / `traceId` | Read from each span and used to select same-trace spans. | `subject.id`, input reference, evidence locators. | Binds the generated statement to one trace input. | Malformed spans without a trace id cannot be mapped. |
| `span_id` / `spanId` | Read from agent and tool spans. | `operation.id`, `provenance.id`, artifact ids. | Gives stable span-level provenance anchors. | Malformed spans without span id cannot be mapped. |
| `parent_span_id` / `parentSpanId` | Used to check parent closure and tool-span ancestry. | Adapter report extraction and provenance interpretation. | Prevents unattached tool spans from being treated as operation evidence. | `broken_parent_span_relation` or `unresolved_tool_span`. |
| `gen_ai.agent.id` | Extracted from the selected agent span. | `actor.id`. | Identifies the accountable agent actor in the statement. | Absence of all `gen_ai.agent.*` fields yields `missing_agent_span`. |
| `gen_ai.agent.name` | Extracted from the selected agent span. | `actor.name`. | Provides human-readable agent identity. | Absence of all `gen_ai.agent.*` fields yields `missing_agent_span`; missing name alone uses adapter fallback. |
| `gen_ai.agent.version` | Extracted from the selected agent span. | `actor.runtime` suffix. | Preserves version context without changing EEOAP schema. | Absence of all `gen_ai.agent.*` fields yields `missing_agent_span`; missing version alone is allowed. |
| `gen_ai.operation.name` | Required on the selected agent span. | `operation.type`. | Defines the accountable operation being converted. | `missing_operation_name`. |
| execute tool span | Identified by `gen_ai.operation.name=execute_tool` or span name prefix. | `evidence.artifacts[]`. | Records supporting tool-call spans as evidence artifacts. | `unresolved_tool_span` if not descended from the agent span. |
| timestamp | Extracted from start/end span timestamps. | statement timestamp and adapter report fields. | Preserves operation timing context for review. | Missing timestamp can reduce context but does not by itself fail the minimal mapping. |
| `error.type` | Extracted when present. | operation result status and adapter report. | Carries runtime failure signal into operation summary. | Missing value is treated as no declared error signal, not as output correctness proof. |

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
id, agent id, agent name, agent version, operation name, timestamps, error
type, and resolved tool spans. For the valid fixture, the extracted fields
include:

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

### 6.1 Why This Is Not Just Field Copying

The adapter does more than copy values from one JSON object to another. It
identifies the accountable operation span, checks parent-child span
consistency, resolves tool spans against the selected agent span, preserves
trace and span provenance links, emits an EEOAP-compatible operation
accountability statement, recomputes integrity fields, and routes the result
into the existing profile-aware validator. Field extraction is only the first
step; the contribution is the bounded transformation from telemetry into
portable, validator-checkable operation evidence.

## 7. Evaluation

The evaluation is limitations-first. It does not attempt to prove general
OpenTelemetry compatibility or cross-framework portability. It asks two
narrower questions:

1. Can a valid OpenTelemetry-style agent trace be converted into an
   EEOAP-compatible statement that passes the existing validator?
2. Do malformed traces fail at readable adapter diagnostic surfaces before a
   misleading EEOAP statement is emitted?

### 7.1 Case Matrix

| Case | Input fixture | Expected outcome | Observed diagnostic or validation result | Interpretation |
|---|---|---|---|---|
| `valid-agent-trace` | `examples/opentelemetry/valid-agent-trace.json` | Generate an EEOAP statement and adapter report. | Existing `validate-profile` passes with `ok=true` and `issue_count=0`. | The bounded trace-to-evidence path works for the minimal valid fixture. |
| `invalid-missing-agent-span` | `examples/opentelemetry/invalid-missing-agent-span.json` | Fail before statement emission. | `missing_agent_span`. | The adapter refuses telemetry without an identifiable accountable agent span. |
| `invalid-unresolved-tool-span` | `examples/opentelemetry/invalid-unresolved-tool-span.json` | Fail before statement emission. | `unresolved_tool_span`. | Tool spans must be structurally attached to the selected agent operation. |
| `invalid-broken-parent-span` | `examples/opentelemetry/invalid-broken-parent-span.json` | Fail before statement emission. | `broken_parent_span_relation`. | Broken parent references block provenance-safe transformation. |
| `invalid-missing-operation-name` | `examples/opentelemetry/invalid-missing-operation-name.json` | Fail before statement emission. | `missing_operation_name`. | The accountable operation must be named before it can become EEOAP `operation.type`. |

### 7.2 Valid Trace

The valid fixture contains one agent span and two resolved `execute_tool`
spans. Running the adapter on this fixture returns exit code 0 and writes the
generated statement and report.

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

This supports the paper claim that the adapter can produce a portable
operation evidence object that is checkable by the existing EEOAP validator.

### 7.3 Invalid Traces

The four invalid traces exercise mapping preconditions rather than EEOAP schema
changes. This distinction is important: the adapter should reject telemetry
that cannot be mapped safely, before generating a statement that the EEOAP
validator would then inspect.

Observed diagnostic labels are:

- `missing_agent_span`
- `unresolved_tool_span`
- `broken_parent_span_relation`
- `missing_operation_name`

These negative cases make the evaluation small but targeted. The artifact does
not merely demonstrate the happy path; it also defines where the adapter
refuses to convert telemetry into operation evidence.

### 7.4 Test Results

The scoped adapter test command is:

```bash
.venv/bin/python -m pytest tests/test_opentelemetry_to_eeoap_adapter.py -q
```

Observed result for v0.2:

```text
6 passed in 2.11s
```

The full repository pytest result recorded for the evidence closure is:

```text
164 passed, 1 skipped, 15 warnings in 35.38s
```

During the adapter implementation commit, the staged pre-commit checks for
`check json`, `ruff check`, and `ruff format` passed for the adapter-related
files. Full-repository ruff was not rerun for v0.1 or v0.2. Known
out-of-scope lint debt exists in pre-existing directories such as `pd-oap/`
and SoftwareX-related paper-support trees. This limitation does not affect the
adapter-specific pytest result or the generated statement's EEOAP validator
result, but it should be disclosed honestly as repository hygiene debt outside
the adapter contribution.

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
generated evidence, validator output, scoped pytest, and the recorded full
pytest result.

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
transforms an OpenTelemetry-style GenAI agent trace into an EEOAP v0.1
operation accountability statement and checks that statement with the existing
EEOAP validator.

The result is deliberately small and verifiable. One valid trace produces an
EEOAP statement that passes validation with `ok=true` and `issue_count=0`.
Four invalid traces fail at expected adapter diagnostic surfaces:
`missing_agent_span`, `unresolved_tool_span`, `broken_parent_span_relation`,
and `missing_operation_name`. Scoped adapter tests pass with `6 passed in
2.11s`, and the evidence closure records the repository test suite result as
`164 passed, 1 skipped, 15 warnings in 35.38s`.

The paper's contribution is therefore an adapter, mapping model, and
evaluation closure. It does not claim legal accountability, full runtime
reconstruction, general OpenTelemetry compatibility, cross-framework
generality, output correctness, or a new profile. Its value is narrower: it
shows that OpenTelemetry-style agent telemetry can be transformed into
portable operation evidence under an existing EEOAP validator path.
