# From Agent Telemetry to Portable Operation Evidence: A Minimal Adapter from OpenTelemetry Agent Spans to EEOAP Evidence Objects

Version: 0.8 journal manuscript draft

## 1. Abstract

Runtime telemetry improves observability, but it does not automatically produce
portable operation evidence. Traces can record spans, attributes, timestamps,
parent-child relations, tool calls, and error signals, yet those records do not
by themselves define an externally checkable evidence object. This paper
presents a minimal adapter from OpenTelemetry-style agent spans to
Execution Evidence and Operation Accountability Profile (EEOAP) compatible
operation accountability statements. The adapter preserves trace and span
provenance, resolves tool spans through parent-child ancestry, checks
parent-child span relationships, and emits validator-ready EEOAP statements
without modifying the EEOAP schema. The evaluation uses two controlled valid
trace contexts and four controlled invalid traces. The first valid trace
contains a `research.answer` operation with direct child tool spans; the
second contains a `workflow.execute` operation with an intermediate workflow
invocation span and descendant tool spans. Both generated EEOAP statements
pass the existing EEOAP validator with `ok=true` and `issue_count=0` across
schema, references, consistency, and integrity stages. The invalid fixtures
exercise `missing_agent_span`, `unresolved_tool_span`,
`broken_parent_span_relation`, and `missing_operation_name` diagnostics. The
contribution is deliberately bounded: it does not claim legal accountability,
full runtime reconstruction, production readiness, agent-output correctness,
cross-framework generality, a new EEOAP profile, or broad OpenTelemetry
implementation compatibility.

## 2. Introduction

Modern agent systems increasingly emit structured runtime telemetry. A trace
can show that an agent span was created, that a tool span was nested below it,
that timestamps were recorded, or that an error attribute was present. These
observability records are useful for debugging and operations, and they are a
natural source for later review. However, telemetry is not the same thing as
portable operation evidence. A trace does not automatically state which
operation is being accounted for, which subject is bound to that operation,
which evidence references support the claim, or whether another party can
validate the resulting object.

The gap addressed in this paper is the transformation from telemetry to
evidence. We study whether OpenTelemetry-style agent traces can be mapped into
EEOAP-compatible operation accountability statements without changing the
target EEOAP schema. The practical motivation is interoperability: if agent
runtimes already produce traces, an evidence layer should be able to ingest
selected telemetry while preserving provenance, rejecting unsafe mappings, and
using an existing validator path.

This paper therefore treats telemetry as source material, not as evidence by
default. The adapter chooses one accountable agent span, requires an operation
name, resolves tool spans through parent-child ancestry, preserves trace and
span locators, constructs an EEOAP-compatible statement, recomputes integrity
fields, and routes the result into the existing EEOAP validator. The adapter
also fails before statement emission when the telemetry cannot support the
operation evidence claim.

The evaluation is intentionally controlled. It uses two valid
OpenTelemetry-style trace fixtures and four invalid trace fixtures. The first
valid trace represents a `research.answer` operation with two tool spans that
are direct children of the agent span. The second valid trace represents a
`workflow.execute` operation with an intermediate workflow invocation span and
two descendant tool spans. Both generated statements pass the existing EEOAP
validator. The four invalid traces demonstrate bounded diagnostics for missing
agent identity, unresolved tool span ancestry, broken parent relations, and
missing operation names.

This paper makes four contributions:

C1. A bounded telemetry-to-evidence mapping model.

C2. A minimal adapter implementation from OpenTelemetry-style agent spans to
EEOAP-compatible statements.

C3. A controlled evaluation with two valid trace contexts and four invalid
diagnostic contexts.

C4. A reproducibility package with generated statements, adapter reports,
scoped tests, checksum verification, clean-clone verification, and external
review notes.

The contribution is not a new profile, not a replacement for OpenTelemetry,
and not a general agent governance framework. It is a bounded software
engineering method for transforming runtime telemetry into portable operation
evidence objects under explicit constraints.

## 3. Problem: Telemetry Is Not Portable Operation Evidence

Telemetry records observations about running software. A span may record an
operation name, a trace identifier, a parent span identifier, a timestamp, or
attributes describing an agent or tool call. These records are valuable, but
their purpose is observability. They describe runtime activity in a form that
tools can collect, search, aggregate, and visualize.

Portable operation evidence has a different purpose. It must expose an
operation boundary, identify an actor and subject, preserve provenance, bind
evidence references, and allow another party to validate the object. A raw
trace can contain many of the necessary ingredients, but the trace is not
itself an operation accountability statement. It lacks the target profile
shape, policy and constraint references, evidence artifact structure, and
profile-aware validation result expected by EEOAP.

This distinction matters for agent telemetry because agent traces can include
nested and ambiguous spans. A tool call can be a descendant of the selected
agent span, or it can be unrelated. A span can claim to be an agent span, or it
can omit agent identity attributes. A trace can contain a parent span
reference that cannot be resolved. An agent span can exist without a
`gen_ai.operation.name`, leaving the accountable operation undefined. If those
conditions are not checked, the adapter could turn ambiguous telemetry into a
misleading evidence object.

The problem is therefore not merely serializing JSON from one shape into
another. The adapter must decide which span is accountable, which tool spans
belong to that operation, whether span ancestry is closed, whether the
operation is named, and how trace/span provenance should be preserved in the
target statement. If these preconditions fail, the correct behavior is to
emit a diagnostic report rather than an EEOAP statement.

## 4. Background

### 4.1 OpenTelemetry Agent Spans

OpenTelemetry provides a structured vocabulary for telemetry, including
traces, spans, parent-child relations, attributes, and status or error signals
[OpenTelemetry-GenAI]. The agent-oriented semantic surface is relevant because
it includes attributes that can identify an agent, name an operation, and
describe related tool execution spans [OpenTelemetry-Agent-Spans].

This paper uses local OpenTelemetry-style JSON fixtures rather than a live
OpenTelemetry Collector, hosted telemetry backend, or runtime SDK pipeline.
The source side of the adapter uses fields such as `traceId`, `spanId`,
`parentSpanId`, `startTimeUnixNano`, `endTimeUnixNano`,
`gen_ai.agent.id`, `gen_ai.agent.name`, `gen_ai.agent.version`,
`gen_ai.operation.name`, `gen_ai.tool.name`, `gen_ai.tool.call.id`, and
`error.type`.

The paper does not claim full OpenTelemetry implementation compatibility.
It does not test all exporters, collectors, vendors, SDKs, semantic-convention
versions, or payload encodings. The phrase "OpenTelemetry-style" is used
deliberately: the committed fixtures use a local trace shape and selected
GenAI-related fields as the source material for the adapter.

### 4.2 EEOAP Evidence Objects

EEOAP supplies the target evidence object and existing validator path
[EEOAP-Artifact]. The profile represents operation accountability through a
structured statement containing actor, subject, operation, policy,
constraints, provenance, evidence, integrity, and validation sections. The
existing validator checks schema conformance, reference closure, consistency,
and integrity.

The adapter in this paper does not create a new EEOAP profile and does not
modify the EEOAP schema. This is central to the contribution. The target is
held stable, and the adapter demonstrates that selected telemetry can enter
the existing profile and validator path.

This work is adjacent to provenance and structured validation practices.
Provenance standards such as W3C PROV motivate explicit relationships among
actors, activities, and entities [W3C-PROV]. JSON Schema provides context for
structured validation of JSON objects [JSON-Schema-2020-12]. AEP-related work
in the repository addresses broader evidence bundles and integrity-verifiable
packaging [AEP-Artifact]. This paper is narrower: it focuses on one
span-to-operation-evidence transformation path.

## 5. Method: Telemetry-to-Evidence Mapping

The method is a bounded transformation from OpenTelemetry-style agent telemetry
to EEOAP-compatible operation accountability statements. The input is one
local trace JSON file. The output, for a valid input, is one EEOAP-compatible
statement and one adapter report. For invalid input, the output is an adapter
report with a diagnostic and no EEOAP statement.

The mapping starts by flattening spans from either a top-level `spans` array
or an OpenTelemetry-style `resourceSpans` and `scopeSpans` structure. Each
span record retains its source path, raw span object, trace id, span id,
parent span id, name, attributes, timestamps, and optional `error.type`.
Attributes are normalized from OpenTelemetry-style typed values such as
`stringValue`, `intValue`, `doubleValue`, `boolValue`, array values, and
key-value-list values.

The adapter then interprets span roles. A span is treated as an agent span if
it carries at least one of `gen_ai.agent.id`, `gen_ai.agent.name`, or
`gen_ai.agent.version`. The current adapter requires exactly one agent span.
Tool spans are identified by `gen_ai.operation.name=execute_tool` or by an
`execute_tool` span-name prefix. This role interpretation is intentionally
small; it is enough to demonstrate the mapping while avoiding a claim of
general OpenTelemetry compatibility.

Parent-child validation is a method-level step, not a cosmetic check. The
adapter selects spans from the same trace as the agent span and verifies that
all parent references in that trace are closed. It then checks whether each
tool span is a descendant of the agent span. This allows both direct tool
spans and deeper workflow-style ancestry to be accepted, while rejecting tool
spans that cannot be tied to the accountable operation.

Provenance is preserved through trace and span locators. The generated EEOAP
statement records the original trace as the subject, uses an input reference
to the trace fixture, and includes evidence artifacts for the agent span and
each resolved tool span. Artifact locators use the form
`otel://trace/<trace-id>/span/<span-id>`. The statement also includes digests
for the trace, spans, references, artifacts, and statement integrity fields.

The EEOAP statement emission step constructs actor, subject, operation,
policy, constraints, provenance, evidence, and validation sections. The
operation type is taken from `gen_ai.operation.name`. The actor id, name, and
runtime are derived from agent attributes. Tool spans become evidence
artifacts. The validation section records that the intended validator is the
existing `agent-evidence validate-profile` path.

Finally, the adapter routes the generated statement into the existing EEOAP
validator. Validator success means that the generated statement satisfies the
current schema, references, consistency, and integrity checks. It does not
mean that legal accountability, output correctness, regulatory compliance, or
production readiness has been proven.

The mapping is summarized below.

| OpenTelemetry-style source | Adapter interpretation | EEOAP target | Failure behavior |
|---|---|---|---|
| `traceId` / `trace_id` | Trace boundary for selected agent span and related spans. | `subject.id`, input reference, evidence locators. | Missing trace id yields malformed-span failure. |
| `spanId` / `span_id` | Stable span identity. | operation id, provenance id, artifact ids. | Missing span id yields malformed-span failure. |
| `parentSpanId` / `parent_span_id` | Parent closure and tool-span ancestry. | adapter report, provenance interpretation, evidence admissibility. | Broken relation or unresolved ancestry fails before statement emission. |
| `gen_ai.agent.id` | Accountable agent identity. | `actor.id`. | Absence of all agent attributes yields `missing_agent_span`. |
| `gen_ai.agent.name` | Human-readable agent identity. | `actor.name`. | Missing name alone can use adapter fallback. |
| `gen_ai.agent.version` | Agent/runtime version context. | `actor.runtime` suffix. | Missing version alone is allowed. |
| `gen_ai.operation.name` | Accountable operation type. | `operation.type`. | Missing on agent span yields `missing_operation_name`. |
| `execute_tool` span | Supporting tool execution evidence. | `evidence.artifacts[]`. | Tool span not descended from agent yields `unresolved_tool_span`. |
| timestamps | Execution timing context. | statement timestamp and adapter report. | Missing timestamp reduces context but does not fail minimal mapping. |
| `error.type` | Runtime error signal when present. | operation result status and adapter report. | Missing value is not output-correctness proof. |

## 6. Adapter Implementation

The adapter implementation lives at
`tools/opentelemetry_to_eeoap_adapter.py`. It is a local script. It does not
call a network service, does not depend on a hosted OpenTelemetry backend, and
does not require an OpenTelemetry Collector. It reads a local trace JSON file,
writes generated artifacts under `generated/`, and validates the generated
statement through existing repository code.

For each input file, the adapter derives a case name from the input path and
writes two outputs:

```text
generated/<case-name>-eeoap-statement.json
generated/<case-name>-adapter-report.json
```

The statement is emitted only when the input trace satisfies the mapping
preconditions. The adapter report is emitted for both success and failure. On
success, the report records extracted trace id, span id, parent span id, agent
attributes, operation name, timestamps, error type, resolved tool spans, and
the EEOAP validator report. On failure, the report records a diagnostic code
and message.

The implementation performs several steps that make it more than field
copying. It selects an accountable agent span, checks that the parent closure
of same-trace spans is valid, resolves tool spans through ancestry, preserves
span locators as evidence artifacts, computes digests, emits an
EEOAP-compatible statement, and invokes the existing profile-aware validator.

The v0.7 evaluation expansion did not require adapter code changes. The same
adapter accepted the original `research.answer` trace and the new
`workflow.execute` trace with an intermediate workflow invocation span. That
matters because the second trace tests a deeper parent-child relation without
broadening the adapter into framework-specific or production-runtime support.

## 7. Evaluation

The evaluation asks three questions. First, can the adapter produce
validator-accepted EEOAP statements from OpenTelemetry-style agent telemetry?
Second, can it do so for more than one valid trace context, including a
workflow-style parent-child span pattern? Third, do invalid traces fail at
bounded and meaningful diagnostic surfaces?

The evaluation uses two valid traces and four invalid traces. The scoped
adapter tests report:

```text
8 passed in 2.48s
```

Both valid generated statements pass the existing EEOAP validator with
`ok=true` and `issue_count=0`. The validator stages passed for both are:

```text
schema
references
consistency
integrity
```

The latest planning-step scoped pytest also passed with `8 passed in 2.01s`.
That later run is recorded as reproducibility evidence, while the v0.7
evaluation result remains the main evaluation result.

### Table 1: Valid Trace Contexts

| Case | Operation pattern | Span structure | Generated statement | Validator result | Evaluation meaning |
|---|---|---|---|---|---|
| `valid-agent-trace` | Root agent operation `research.answer` with two tool calls. | Agent span `1111111111111111`; direct child tool spans `2222222222222222` and `3333333333333333`. | `generated/valid-agent-trace-eeoap-statement.json` | PASS; `ok=true`, `issue_count=0`; schema, references, consistency, integrity pass. | Baseline positive case for telemetry-to-evidence transformation. |
| `valid-agent-workflow-trace` | Root agent operation `workflow.execute` with one workflow invocation and two tool calls. | Agent span `4444444444444444`; workflow invocation span `5555555555555555`; descendant tool spans `6666666666666666` and `7777777777777777`. | `generated/valid-agent-workflow-trace-eeoap-statement.json` | PASS; `ok=true`, `issue_count=0`; schema, references, consistency, integrity pass. | Shows the adapter can resolve tool spans through a deeper parent-child chain. |

### Table 2: Invalid Diagnostic Cases

| Case | Broken condition | Expected diagnostic | Evaluation meaning |
|---|---|---|---|
| `invalid-missing-agent-span` | The trace contains no span carrying `gen_ai.agent.*` attributes. | `missing_agent_span` | The adapter refuses to emit evidence when it cannot identify an accountable agent. |
| `invalid-unresolved-tool-span` | An `execute_tool` span is not descended from the selected agent span. | `unresolved_tool_span` | The adapter does not attach unrelated tool activity to the operation evidence claim. |
| `invalid-broken-parent-span` | A span references a missing parent span. | `broken_parent_span_relation` | The adapter requires closed parent ancestry before evidence construction. |
| `invalid-missing-operation-name` | The selected agent span lacks `gen_ai.operation.name`. | `missing_operation_name` | The adapter requires an explicit operation boundary. |

### Table 3: Telemetry-only vs EEOAP Statement

| Representation | What it captures | What it misses | Validation path | Role in this paper |
|---|---|---|---|---|
| raw logs | Local messages, warnings, errors, and human-readable runtime events. | Stable operation boundary, typed evidence references, integrity structure, and profile-aware validation. | Usually no standard operation-evidence validation path. | Useful operational context but not the target evidence object. |
| raw OpenTelemetry-style trace | Structured spans, trace ids, span ids, parent links, attributes, timestamps, and error signals. | Explicit EEOAP actor/subject/operation statement, policy references, evidence artifacts, integrity, and EEOAP validator result. | Telemetry tools can process traces, but not as EEOAP operation accountability statements. | Source representation consumed by the adapter. |
| provenance-only record | Relationships among actors, activities, entities, and derivations. | Telemetry-specific span extraction and EEOAP-specific operation accountability sections. | Depends on the provenance format and validator. | Conceptual neighbor for explaining why provenance links matter. |
| EEOAP statement | Actor, subject, operation, policy, constraints, provenance, evidence references, artifacts, integrity, and validation metadata. | Full raw runtime breadth unless preserved by reference, digest, or artifact locator. | Existing EEOAP validator checks schema, references, consistency, and integrity. | Target portable operation evidence object. |
| adapter path | Selection, mapping, parent closure, tool-span resolution, provenance preservation, statement emission, and validator routing. | Production telemetry support, broad OpenTelemetry compatibility, legal accountability, and output correctness. | Output is checked by existing EEOAP validator. | Main contribution of the paper. |

This comparison should not be read as a dismissal of logs, traces, or
provenance records. They are partial capability holders. The paper's claim is
that a portable operation evidence object requires a transformation and
validation step beyond raw telemetry.

### Table 4: Reproducibility Evidence

| Evidence item | Result | Interpretation |
|---|---|---|
| scoped adapter tests | v0.7 evidence expansion: `8 passed in 2.48s`; later planning-step run: `8 passed in 2.01s`. | The adapter behavior and expected diagnostics are covered by focused tests. |
| generated statements | Two valid generated EEOAP statements are committed under `generated/`. | The positive evaluation has concrete output artifacts, not only prose. |
| existing EEOAP validator | Both generated statements pass with `ok=true`, `issue_count=0`. | The adapter outputs enter the existing profile-aware validation path. |
| clean-clone verification | v0.5 package clean clone test passed with `6 passed in 1.70s`. | The frozen package was reproducible from a clean checkout before v0.7 expansion. |
| checksum verification | v0.5 external-review package checksum verification reported `13 files OK`. | The frozen package had file-level integrity evidence. |
| repository hygiene note | Full-repository Ruff remains affected by unrelated out-of-scope lint debt. | The paper should rely on scoped adapter tests and validator evidence, while disclosing repository hygiene debt honestly. |

The evaluation remains bounded. The valid traces are synthetic and controlled.
They are sufficient to demonstrate two operation contexts, but not sufficient
to claim broad compatibility with all OpenTelemetry implementations or
production agent runtimes.

## 8. Discussion

The second workflow-style trace matters because it changes the positive
evaluation from one trace shape to two. The original valid trace tests an
agent operation whose tool spans are direct children of the agent span. The
new workflow trace tests a deeper parent-child chain: the tool spans are
children of a workflow invocation span, which is itself a child of the agent
span. This matters because tool-span ancestry is a central part of the
mapping. If tool spans can only be direct children, the adapter is closer to a
single-fixture demonstration. If descendant tool spans can be resolved through
an intermediate operation span, the method better captures the idea of
bounded ancestry-based evidence selection.

The adapter is more than field copying. A field-copying script would move
values from `traceId`, `spanId`, or `gen_ai.agent.name` into a new JSON object.
This adapter performs role selection, parent closure checking, descendant
resolution, evidence artifact creation, provenance locator preservation,
digest computation, statement construction, and validator routing. The invalid
diagnostics are part of the method: they show that the adapter rejects traces
that cannot safely support an operation evidence claim.

Schema reuse is also important. The adapter does not solve mapping problems by
changing EEOAP. It instead demonstrates how external telemetry can enter the
existing EEOAP evidence-object path. This keeps the target stable and makes
the evaluation more meaningful: validator success is not obtained by moving
the schema boundary.

The evaluation remains intentionally bounded. The paper does not claim
production readiness, collector integration, live runtime instrumentation, or
cross-framework support. This narrowness is a strength if stated clearly. It
keeps the contribution reviewable as a software engineering method and
artifact rather than an overbroad governance framework.

The work is software engineering research rather than just a script because it
studies an interoperability method between observability and evidence layers.
The artifact embodies a set of design decisions about span roles, ancestry,
provenance, evidence references, validation, and failure diagnostics. The
evaluation asks whether those decisions can produce validator-checkable
evidence objects under controlled success and failure cases.

## 9. Threats to Validity

The first threat is the synthetic-fixture limitation. Both valid traces are
local and controlled. They are useful for isolating the mapping, but they are
not production telemetry. The paper should not imply that real deployments
will produce identical trace shapes.

The second threat is limited positive diversity. The evaluation now includes
two valid trace contexts, which is stronger than the earlier one-valid-trace
package, but it is still small. It demonstrates a baseline agent operation and
a workflow-style parent-child pattern. It does not demonstrate all plausible
agent workflows or runtime topologies.

The third threat is OpenTelemetry semantic convention evolution. The adapter
uses fields such as `gen_ai.agent.id`, `gen_ai.agent.name`,
`gen_ai.agent.version`, `gen_ai.operation.name`, and `error.type`.
If OpenTelemetry semantic conventions evolve, the adapter's source-side
compatibility may need versioned updates. This does not imply an EEOAP schema
change, but it does limit source-side stability.

The fourth threat is the absence of real framework runtime integration. The
paper does not include LangChain runtime integration, CrewAI integration,
AutoGen integration, or OpenTelemetry Collector integration. That work is
deferred and should not be claimed in this draft.

The fifth threat is cross-framework generality. Even with two valid traces,
the paper does not prove that the adapter generalizes across agent frameworks.
Any future claim of framework generality would require committed fixtures,
tests, generated outputs, and validator results for those frameworks.

The sixth threat is repository hygiene. Full-repository Ruff is not currently
a clean artifact-wide signal because unrelated pre-existing lint debt exists
in out-of-scope directories such as `pd-oap/` and SoftwareX-related
paper-support trees. This should be disclosed as repository hygiene debt, not
as an adapter failure. The adapter-specific evidence relies on scoped tests,
generated statements, and validator results.

The seventh threat is the validator environment warning. The manual validator
runs in v0.7 emitted a Python environment warning from `langchain_core` about
Pydantic V1 compatibility with Python 3.14. The validator result itself was
successful for both generated statements, but the warning should be recorded
as an environment note until dependency compatibility is cleaned up.

## 10. Related Work

OpenTelemetry provides the source-side observability context for this paper
[OpenTelemetry-GenAI]. The agent-span semantic surface motivates the use of
agent identity attributes, operation names, parent span identifiers,
timestamps, and error attributes [OpenTelemetry-Agent-Spans]. This paper does
not compete with OpenTelemetry; it uses OpenTelemetry-style telemetry as
source material for evidence construction.

EEOAP provides the target operation accountability statement and validator
path [EEOAP-Artifact]. The paper does not redefine EEOAP or introduce a new
profile. Its contribution is the adapter method that moves selected telemetry
into the existing EEOAP evidence-object path.

JSON Schema is relevant because EEOAP statements are structured JSON objects
that require schema-aware validation [JSON-Schema-2020-12]. W3C PROV is
relevant because the paper's evidence model depends on preserving
relationships among actors, operations, subjects, inputs, outputs, and
artifacts [W3C-PROV]. The paper does not claim to be a general provenance
standard; it uses provenance-preserving evidence construction in a concrete
adapter.

AEP-related repository artifacts provide broader context for runtime evidence
bundles and integrity-verifiable evidence packaging [AEP-Artifact]. This
paper is narrower. It focuses on one operation-accountability statement path
from OpenTelemetry-style traces to EEOAP. Artifact review and reproducibility
expectations are adjacent to artifact-badging practices [ACM-Artifact-Badging],
but venue-specific artifact packaging remains future work.

## 11. Conclusion

OpenTelemetry-style agent telemetry can describe runtime behavior, but it does
not automatically become portable operation evidence. This paper presents a
minimal adapter method that transforms controlled agent trace fixtures into
EEOAP-compatible operation accountability statements without modifying the
EEOAP schema.

The v0.8 evidence story contains two valid traces, four invalid traces, two
generated EEOAP statements, two validator passes, and four controlled
diagnostic surfaces. The first valid trace demonstrates a `research.answer`
operation with direct child tool spans. The second demonstrates a
`workflow.execute` operation with descendant tool spans below an intermediate
workflow invocation span. Both generated statements pass the existing EEOAP
validator with `ok=true` and `issue_count=0` across schema, references,
consistency, and integrity stages.

The result is a bounded software engineering contribution. It does not prove
legal accountability, reconstruct a full runtime environment, demonstrate
production readiness, establish broad OpenTelemetry compatibility, prove
agent-output correctness, provide cross-framework generality, or define a new
EEOAP profile. It shows that telemetry-to-evidence transformation can be made
explicit, reproducible, validator-aware, and failure-bounded.

## 12. References

- [OpenTelemetry-GenAI] OpenTelemetry. Semantic conventions for generative AI
  systems. Official OpenTelemetry documentation. TODO: verify before external
  submission. Confirm exact title, URL, semantic-convention status, version or
  revision marker if available, and access date.

- [OpenTelemetry-Agent-Spans] OpenTelemetry. Semantic conventions for GenAI
  agent and framework spans. Official OpenTelemetry documentation. TODO:
  verify before external submission. Confirm exact title, URL,
  semantic-convention status, listed fields, version or revision marker if
  available, and access date.

- [JSON-Schema-2020-12] JSON Schema. Draft 2020-12 specification. TODO:
  verify before external submission. Confirm official title, editors/authors
  if the venue requires them, URL, publication metadata, and access date.

- [W3C-PROV] W3C. PROV provenance recommendation family. TODO: verify before
  external submission. Confirm which PROV document is cited, official title,
  date, URL, editors/authors if required, and access date.

- [EEOAP-Artifact] `agent-evidence` repository. Execution Evidence and
  Operation Accountability Profile artifact, including schema, validator,
  examples, and OpenTelemetry adapter branch commits. TODO: verify before
  external submission. Cite an immutable commit, tag, release, DOI, or archive
  once selected.

- [AEP-Artifact] `agent-evidence` repository. AEP-related evidence artifact
  material used only for positioning. TODO: verify before external submission.
  Identify the exact artifact, commit, tag, release, DOI, or archive before
  citing.

- [ACM-Artifact-Badging] ACM. Artifact review and badging guidance. TODO:
  verify before external submission. Confirm official page title, current
  policy wording, URL, and access date.

## Draft Preparation Note

### Commands Run

Plugin/tool inspection:

```sh
tool_search query="plan task file edit test local repository workflow"
```

Memory/context and preflight:

```sh
rg -n "agent-evidence|artifact-first|EEOAP journal|docs-only|targeted validation|full-repo" /Users/zhangbin/.codex/memories/MEMORY.md
git branch --show-current
git status --short
git log --oneline -10
```

Evidence inspection:

```sh
sed -n '1,520p' papers/opentelemetry-to-eeoap/paper_v0_7_journal_plan.md
sed -n '1,260p' papers/opentelemetry-to-eeoap/paper_v0_4.md
sed -n '1,240p' papers/opentelemetry-to-eeoap/references_draft.md
sed -n '1,260p' papers/opentelemetry-to-eeoap/reviewer_positioning.md
sed -n '1,240p' papers/opentelemetry-to-eeoap/journal_v0_7_second_trace/COMMAND_LOG.md
sed -n '1,240p' papers/opentelemetry-to-eeoap/journal_v0_7_second_trace/EVALUATION_UPDATE.md
sed -n '1,240p' papers/opentelemetry-to-eeoap/journal_v0_7_second_trace/SECOND_VALID_TRACE.md
sed -n '1,220p' tests/test_opentelemetry_to_eeoap_adapter.py
sed -n '1,220p' generated/valid-agent-trace-eeoap-statement.json
sed -n '1,220p' generated/valid-agent-workflow-trace-eeoap-statement.json
sed -n '1,220p' generated/valid-agent-trace-adapter-report.json
sed -n '1,220p' generated/valid-agent-workflow-trace-adapter-report.json
sed -n '1,220p' examples/opentelemetry/valid-agent-workflow-trace.json
```

Validation command:

```sh
/Users/zhangbin/GitHub/agent-evidence/.venv/bin/python -m pytest tests/test_opentelemetry_to_eeoap_adapter.py -q
```

### Scoped Pytest Result

```text
........                                                                 [100%]
8 passed in 2.60s
```

### Change Boundary

- Runtime code changed: no.
- Tests changed: no.
- Fixtures changed: no.
- Generated JSON outputs changed: no.
- EEOAP schema changed: no.
- Adapter features added: no.
- LangChain runtime integration added: no.
- OpenTelemetry Collector integration added: no.
- Out-of-scope worktree items touched: no.

### Git Status Before

Branch:

```text
opentelemetry-to-eeoap-adapter
```

Existing dirty worktree items were present before this draft and remained out
of scope:

```text
 M docs/paper/softwarex/final/aep_media_softwarex_final_manuscript.md
 M docs/paper/softwarex/final/submission-pack/UPLOAD_MANIFEST.md
 M docs/paper/softwarex/final/submission-pack/main/AEP-Media_SoftwareX_Manuscript.docx
 M docs/paper/softwarex/final/submission-pack/main/AEP-Media_SoftwareX_Manuscript.pdf
 M docs/paper/softwarex/final/submission-pack/metadata/softwarex_submission_metadata.md
?? codex-eeoap-low-risk-summary.md
?? docs/paper/aep_media_abstract.md
?? docs/paper/aep_media_cover_letter_draft.md
?? docs/paper/aep_media_cover_letter_high_revision.docx
?? docs/paper/aep_media_cover_letter_high_revision.md
?? docs/paper/aep_media_digital_evidence_abstract.md
?? docs/paper/aep_media_editor_defense_notes.md
?? docs/paper/aep_media_evaluation_section.md
?? docs/paper/aep_media_final_reference_list.md
?? docs/paper/aep_media_ieee_word_conversion_report.md
?? docs/paper/aep_media_ieee_word_final_checklist.md
?? docs/paper/aep_media_ieee_word_style_checklist.md
?? docs/paper/aep_media_ieee_word_submission_metadata.md
?? docs/paper/aep_media_manuscript_draft.md
?? docs/paper/aep_media_methods_section.md
?? docs/paper/aep_media_paper_outline.md
?? docs/paper/aep_media_related_work_matrix.md
?? docs/paper/aep_media_related_work_notes.md
?? docs/paper/aep_media_retargeting_strategy.md
?? docs/paper/aep_media_software_artifact_abstract.md
?? docs/paper/aep_media_submission_appendix.md
?? docs/paper/aep_media_submission_checklist.md
?? docs/paper/aep_media_submission_risk_register.md
?? docs/paper/aep_media_threats_to_validity.md
?? docs/paper/aep_media_tse_format_preflight.md
?? docs/paper/aep_media_tse_submission_draft.md
?? docs/paper/aep_media_tse_submission_high_revision.docx
?? docs/paper/aep_media_tse_submission_high_revision.md
?? docs/paper/aep_media_tse_submission_high_revision.pdf
?? docs/paper/final-submission-checklist.md
?? docs/paper/ieee_tse_submission_resources/
?? docs/paper/softwarex/final/submission-pack/supplementary/AEP-Media_SoftwareX_Supplementary_S1.pdf
?? docs/reports/aep_media_final_editor_attack_defense.md
?? docs/reports/aep_media_mission008_report.md
?? docs/reports/aep_media_mission009_report.md
?? docs/reports/aep_media_mission010_report.md
?? docs/reports/aep_media_mission011_high_revision_report.md
?? docs/reports/aep_media_tse_decision_archive_note.md
?? docs/reports/aep_media_tse_rejection_analysis.md
?? paper-ncs-execution-evidence/
?? pd-oap.zip
?? pd-oap/
?? tmp/
```

### Git Status After

Status after creating the v0.8 journal draft and running scoped pytest, before
staging:

```text
 M docs/paper/softwarex/final/aep_media_softwarex_final_manuscript.md
 M docs/paper/softwarex/final/submission-pack/UPLOAD_MANIFEST.md
 M docs/paper/softwarex/final/submission-pack/main/AEP-Media_SoftwareX_Manuscript.docx
 M docs/paper/softwarex/final/submission-pack/main/AEP-Media_SoftwareX_Manuscript.pdf
 M docs/paper/softwarex/final/submission-pack/metadata/softwarex_submission_metadata.md
?? codex-eeoap-low-risk-summary.md
?? docs/paper/aep_media_abstract.md
?? docs/paper/aep_media_cover_letter_draft.md
?? docs/paper/aep_media_cover_letter_high_revision.docx
?? docs/paper/aep_media_cover_letter_high_revision.md
?? docs/paper/aep_media_digital_evidence_abstract.md
?? docs/paper/aep_media_editor_defense_notes.md
?? docs/paper/aep_media_evaluation_section.md
?? docs/paper/aep_media_final_reference_list.md
?? docs/paper/aep_media_ieee_word_conversion_report.md
?? docs/paper/aep_media_ieee_word_final_checklist.md
?? docs/paper/aep_media_ieee_word_style_checklist.md
?? docs/paper/aep_media_ieee_word_submission_metadata.md
?? docs/paper/aep_media_manuscript_draft.md
?? docs/paper/aep_media_methods_section.md
?? docs/paper/aep_media_paper_outline.md
?? docs/paper/aep_media_related_work_matrix.md
?? docs/paper/aep_media_related_work_notes.md
?? docs/paper/aep_media_retargeting_strategy.md
?? docs/paper/aep_media_software_artifact_abstract.md
?? docs/paper/aep_media_submission_appendix.md
?? docs/paper/aep_media_submission_checklist.md
?? docs/paper/aep_media_submission_risk_register.md
?? docs/paper/aep_media_threats_to_validity.md
?? docs/paper/aep_media_tse_format_preflight.md
?? docs/paper/aep_media_tse_submission_draft.md
?? docs/paper/aep_media_tse_submission_high_revision.docx
?? docs/paper/aep_media_tse_submission_high_revision.md
?? docs/paper/aep_media_tse_submission_high_revision.pdf
?? docs/paper/final-submission-checklist.md
?? docs/paper/ieee_tse_submission_resources/
?? docs/paper/softwarex/final/submission-pack/supplementary/AEP-Media_SoftwareX_Supplementary_S1.pdf
?? docs/reports/aep_media_final_editor_attack_defense.md
?? docs/reports/aep_media_mission008_report.md
?? docs/reports/aep_media_mission009_report.md
?? docs/reports/aep_media_mission010_report.md
?? docs/reports/aep_media_mission011_high_revision_report.md
?? docs/reports/aep_media_tse_decision_archive_note.md
?? docs/reports/aep_media_tse_rejection_analysis.md
?? paper-ncs-execution-evidence/
?? papers/opentelemetry-to-eeoap/paper_v0_8_journal_draft.md
?? pd-oap.zip
?? pd-oap/
?? tmp/
```

### Plugin Selection Report

Tool/workflow inspection was performed before implementation.

Selected:

- `tool_search`: used to inspect whether a more specialized local
  plan/task/file-edit/test plugin was available.
- `update_plan`: used to create and track a short execution plan.
- `apply_patch`: used for deterministic Markdown file editing.
- `exec_command`: used for repository inspection, evidence inspection,
  scoped pytest, and git checks.

Not selected:

- Canva, Figma, Google Drive, Hugging Face, OpenAI Platform, and Node REPL
  tools were available but not relevant to this local Markdown manuscript
  draft.

Reason:

This task creates a local journal draft from committed repository evidence. It
does not require external design tools, cloud documents, model search,
API-key setup, browser automation, runtime integration, or generated media.
