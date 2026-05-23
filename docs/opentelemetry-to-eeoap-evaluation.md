# OpenTelemetry to EEOAP Adapter Evaluation Evidence

This page records the paper-facing evidence closure for the first
OpenTelemetry-to-EEOAP adapter prototype.

## Repository State

- Branch: `opentelemetry-to-eeoap-adapter`
- Adapter commit:
  `c5df6ce235b7194cafe35945e4b60bd5963c8b94`
- Commit message: `Add OpenTelemetry-to-EEOAP adapter prototype`
- Adapter path: `tools/opentelemetry_to_eeoap_adapter.py`
- EEOAP schema changed: no
- Runtime behavior changed after the adapter commit: no

## Fixture List

| Fixture | Purpose |
|---|---|
| `examples/opentelemetry/valid-agent-trace.json` | Valid trace with one agent span and two resolved `execute_tool` spans. |
| `examples/opentelemetry/invalid-missing-agent-span.json` | Fails when no span carries `gen_ai.agent.*` attributes. |
| `examples/opentelemetry/invalid-unresolved-tool-span.json` | Fails when an `execute_tool` span is not under the agent span. |
| `examples/opentelemetry/invalid-broken-parent-span.json` | Fails when a span references a missing parent span. |
| `examples/opentelemetry/invalid-missing-operation-name.json` | Fails when the agent span lacks `gen_ai.operation.name`. |

## Generated Output List

- `generated/valid-agent-trace-eeoap-statement.json`
- `generated/valid-agent-trace-adapter-report.json`

The generated statement is an EEOAP v0.1 operation accountability statement.
The generated report records extracted trace/span fields, adapter diagnostics,
and the existing EEOAP validator result.

## Exact Commands Used

```bash
git rev-parse --abbrev-ref HEAD
git rev-parse HEAD

.venv/bin/python tools/opentelemetry_to_eeoap_adapter.py \
  examples/opentelemetry/valid-agent-trace.json

.venv/bin/agent-evidence validate-profile \
  generated/valid-agent-trace-eeoap-statement.json

.venv/bin/python tools/opentelemetry_to_eeoap_adapter.py \
  examples/opentelemetry/invalid-missing-agent-span.json \
  --output-dir /tmp/otel-eeoap-eval

.venv/bin/python tools/opentelemetry_to_eeoap_adapter.py \
  examples/opentelemetry/invalid-unresolved-tool-span.json \
  --output-dir /tmp/otel-eeoap-eval

.venv/bin/python tools/opentelemetry_to_eeoap_adapter.py \
  examples/opentelemetry/invalid-broken-parent-span.json \
  --output-dir /tmp/otel-eeoap-eval

.venv/bin/python tools/opentelemetry_to_eeoap_adapter.py \
  examples/opentelemetry/invalid-missing-operation-name.json \
  --output-dir /tmp/otel-eeoap-eval

.venv/bin/python -m pytest tests/test_opentelemetry_to_eeoap_adapter.py -q
.venv/bin/python -m pytest
```

Scoped formatting/check commands used during the adapter commit validation:

```bash
.venv/bin/ruff check tools/opentelemetry_to_eeoap_adapter.py \
  tests/test_opentelemetry_to_eeoap_adapter.py

.venv/bin/ruff format --check tools/opentelemetry_to_eeoap_adapter.py \
  tests/test_opentelemetry_to_eeoap_adapter.py
```

## Observed Results

| Check | Result |
|---|---|
| Branch check | `opentelemetry-to-eeoap-adapter` |
| Adapter commit check | `c5df6ce235b7194cafe35945e4b60bd5963c8b94` |
| Valid trace adapter run | exit code 0, generated statement and report written |
| Existing EEOAP validator on generated statement | `ok=true`, `issue_count=0` |
| Scoped adapter tests | `6 passed` |
| Full pytest | `164 passed, 1 skipped, 15 warnings` |
| Staged pre-commit for adapter commit | `check json`, `ruff check`, and `ruff format` passed |

## Valid Trace Result

The valid trace maps:

- `traceId`: `aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa`
- agent `spanId`: `1111111111111111`
- `gen_ai.agent.id`: `agent:research-assistant-001`
- `gen_ai.agent.name`: `research-assistant`
- `gen_ai.agent.version`: `0.1.0`
- `gen_ai.operation.name`: `research.answer`
- resolved tool spans: `2222222222222222`, `3333333333333333`

The adapter output report records:

- `ok`: `true`
- `diagnostics`: `[]`
- `eeoap_validation.ok`: `true`
- `eeoap_validation.issue_count`: `0`
- validator summary:
  `PASS execution-evidence-operation-accountability-profile@0.1 generated/valid-agent-trace-eeoap-statement.json`

## Invalid Trace Result Table

| Fixture | Expected diagnostic | Observed result |
|---|---|---|
| `invalid-missing-agent-span.json` | `missing_agent_span` | exit code 1, no EEOAP statement emitted |
| `invalid-unresolved-tool-span.json` | `unresolved_tool_span` | exit code 1, no EEOAP statement emitted |
| `invalid-broken-parent-span.json` | `broken_parent_span_relation` | exit code 1, no EEOAP statement emitted |
| `invalid-missing-operation-name.json` | `missing_operation_name` | exit code 1, no EEOAP statement emitted |

Observed diagnostic messages:

```text
missing_agent_span: no span with gen_ai.agent.* attributes was found
unresolved_tool_span: execute_tool span 2222222222222222 is not a descendant of agent span 1111111111111111
broken_parent_span_relation: span 2222222222222222 references missing parent span 9999999999999999
missing_operation_name: agent span is missing gen_ai.operation.name
```

## Validator Result for Generated EEOAP Statement

The generated statement passed the existing validator path:

```text
agent-evidence validate-profile generated/valid-agent-trace-eeoap-statement.json
```

Observed validator result:

- `profile`: `execution-evidence-operation-accountability-profile@0.1`
- `ok`: `true`
- `issue_count`: `0`
- stages passed: `schema`, `references`, `consistency`, `integrity`

## Ruff Boundary

Full-repository `ruff check .` is currently blocked by pre-existing
out-of-scope directories, especially `pd-oap/` generated or paper-support
trees. During adapter validation, full-repository ruff reported existing lint,
long-line, and import-order debt outside this adapter commit.

This is not an adapter failure:

- the adapter Python file passed scoped `ruff check`;
- the adapter Python file passed scoped `ruff format --check`;
- the staged adapter commit passed pre-commit `ruff check` and `ruff format`;
- the full pytest suite passed.

The full-repository ruff debt should be disclosed as unrelated pre-existing
repository lint debt, not as a failure of the OpenTelemetry-to-EEOAP adapter.
