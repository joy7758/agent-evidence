# Evaluation Summary

## Repository Evidence

- Branch: `opentelemetry-to-eeoap-adapter`
- Adapter prototype commit:
  `c5df6ce235b7194cafe35945e4b60bd5963c8b94`
- Paper evidence closure commit:
  `ff8c794b1444527e40b587aef41597bd919b157b`
- Paper v0.1 path:
  `papers/opentelemetry-to-eeoap/paper_v0_1.md`

## Valid Trace

Input fixture:

```text
examples/opentelemetry/valid-agent-trace.json
```

Generated outputs:

```text
generated/valid-agent-trace-eeoap-statement.json
generated/valid-agent-trace-adapter-report.json
```

Observed extracted fields:

| Field | Value |
|---|---|
| `trace_id` | `aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa` |
| agent `span_id` | `1111111111111111` |
| `gen_ai.agent.id` | `agent:research-assistant-001` |
| `gen_ai.agent.name` | `research-assistant` |
| `gen_ai.agent.version` | `0.1.0` |
| `gen_ai.operation.name` | `research.answer` |
| resolved tool spans | `2222222222222222`, `3333333333333333` |

Existing validator result:

| Validator field | Result |
|---|---|
| `profile` | `execution-evidence-operation-accountability-profile@0.1` |
| `ok` | `true` |
| `issue_count` | `0` |
| passed stages | `schema`, `references`, `consistency`, `integrity` |

## Invalid Trace Diagnostics

| Fixture | Expected label | Result |
|---|---|---|
| `invalid-missing-agent-span.json` | `missing_agent_span` | exit code 1, no statement emitted |
| `invalid-unresolved-tool-span.json` | `unresolved_tool_span` | exit code 1, no statement emitted |
| `invalid-broken-parent-span.json` | `broken_parent_span_relation` | exit code 1, no statement emitted |
| `invalid-missing-operation-name.json` | `missing_operation_name` | exit code 1, no statement emitted |

## Test Results

Scoped adapter tests:

```text
pytest tests/test_opentelemetry_to_eeoap_adapter.py -q: 6 passed in 1.33s
```

Full pytest:

```text
pytest: 164 passed, 1 skipped, 15 warnings in 35.38s
```

## Ruff Boundary

Full-repository ruff was not rerun for the paper v0.1 draft. The repository
already contains unrelated out-of-scope lint debt in pre-existing directories,
including `pd-oap/` and generated or paper-support trees.

The adapter commit itself passed staged pre-commit `ruff check` and
`ruff format`; the paper v0.1 commit changes only Markdown files and does not
alter runtime behavior.
