# Evaluation Expansion Plan

## Current Evaluation

The current evaluation includes:

- one valid trace: `examples/opentelemetry/valid-agent-trace.json`
- four invalid traces:
  - `invalid-missing-agent-span.json`
  - `invalid-unresolved-tool-span.json`
  - `invalid-broken-parent-span.json`
  - `invalid-missing-operation-name.json`
- scoped adapter test:
  `pytest tests/test_opentelemetry_to_eeoap_adapter.py -q`
- existing EEOAP validator pass for
  `generated/valid-agent-trace-eeoap-statement.json`
- clean-clone verification:
  `6 passed in 1.70s`
- checksum verification:
  updated frozen package checksum `13 files OK`

## Proposed Minimal Journal Evaluation

The proposed minimum journal evaluation should include:

1. Two valid traces:
   - current `valid-agent-trace`
   - one second trace selected from `SECOND_TRACE_OPTIONS.md`
2. Four or more invalid traces, with the current set preserved.
3. Validator pass for each valid generated statement.
4. Adapter diagnostics for each invalid case.
5. A comparison against the raw telemetry-only representation.
6. A table showing what EEOAP adds beyond trace data.

The second trace should not force an EEOAP schema change or a broad adapter
rewrite. The strongest minimal option is a LangChain-derived fixture manually
normalized into OpenTelemetry-style span structure. If that creates ambiguity,
the safer fallback is a second synthetic OpenTelemetry-style trace with a
different operation pattern.

## Additional Tables Needed

### Valid Trace Contexts

| Case | Source type | Operation pattern | Tool-span pattern | Generated statement | Validator result |
|---|---|---|---|---|---|
| `valid-agent-trace` | Synthetic OpenTelemetry-style fixture | `research.answer` | two resolved tool spans | existing generated statement | pass |
| second valid trace | To be selected | To be defined | To be defined | to be generated | to be verified |

### Invalid Diagnostics

| Fixture | Mapping precondition violated | Expected diagnostic | Statement emitted | Interpretation |
|---|---|---|---|---|
| `invalid-missing-agent-span` | no agent span | `missing_agent_span` | no | cannot identify accountable agent |
| `invalid-unresolved-tool-span` | tool span not descended from agent span | `unresolved_tool_span` | no | cannot attach tool evidence to operation |
| `invalid-broken-parent-span` | missing parent span reference | `broken_parent_span_relation` | no | trace ancestry is not closed |
| `invalid-missing-operation-name` | no `gen_ai.operation.name` on agent span | `missing_operation_name` | no | operation cannot be named |

### Telemetry vs Evidence Object

| Capability | Raw telemetry-only representation | EEOAP statement | Adapter role |
|---|---|---|---|
| runtime observation | captures spans and attributes | references trace as subject evidence | selects relevant spans |
| accountable operation | implicit in span fields | explicit `operation` object | requires operation name |
| provenance | parent/child span links | provenance and evidence locators | preserves trace/span links |
| validation | exporter-dependent | schema/reference/consistency/integrity checks | routes to validator |
| integrity | not necessarily object-level | statement and evidence digests | recomputes integrity |

### Mapping Field Coverage

| Field or concept | Current coverage | Gap for journal version | Required evidence |
|---|---|---|---|
| trace id | covered | second trace should vary id | second generated statement |
| agent span id | covered | second trace should vary id and context | adapter report |
| parent span closure | covered by invalid case | preserve current diagnostic | pytest result |
| tool spans | two resolved tool spans covered | add different tool-span pattern if possible | generated artifacts |
| timestamps | covered | preserve conversion in second trace | adapter report |
| `error.type` | supported by adapter | consider second trace with error signal if compatible | validator pass |

### Non-claim Boundary

| Boundary | Current wording | Journal requirement |
|---|---|---|
| legal accountability | explicitly disallowed | keep unchanged |
| full runtime reconstruction | explicitly disallowed | keep unchanged |
| broad OpenTelemetry compatibility | explicitly disallowed | keep unchanged unless broad tests exist |
| cross-framework generality | explicitly disallowed | keep unchanged even with derived fixture |
| agent-output correctness | explicitly disallowed | keep unchanged |
| new profile | explicitly disallowed | keep unchanged |

### Reproducibility Evidence

| Evidence | Current result | Journal upgrade needed |
|---|---|---|
| clean clone scoped test | `6 passed in 1.70s` | rerun after second trace |
| original repo scoped test | `6 passed in 2.31s` | update expected test count after second trace |
| checksum verification | `13 files OK` | regenerate package checksums if package changes |
| validator pass | one valid statement passes | require pass for both valid statements |
| command log | present for clean clone verification | add journal expansion command log |

## Stop Conditions

Do not continue journal expansion if:

- the second trace forces EEOAP schema changes;
- the adapter needs a broad rewrite;
- the claim boundary becomes unclear;
- the evaluation expansion turns into a cross-framework generality claim;
- dependency setup becomes heavier than the paper's bounded contribution can
  justify;
- the second trace cannot be documented as a committed fixture with generated
  output and validator result.
