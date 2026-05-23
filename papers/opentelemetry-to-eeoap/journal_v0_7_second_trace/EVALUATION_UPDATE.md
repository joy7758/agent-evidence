# Evaluation Update

v0.7 expands the evaluation from one valid trace plus four invalid traces to
two valid traces plus four invalid traces.

| Case | Fixture | Operation pattern | Expected result | Observed result | Interpretation |
|---|---|---|---|---|---|
| `valid-agent-trace` | `examples/opentelemetry/valid-agent-trace.json` | root agent operation `research.answer` with two direct child tool spans | adapter succeeds and validator passes | validator `ok=true`, `issue_count=0`; scoped tests pass | baseline valid conversion remains intact |
| `valid-agent-workflow-trace` | `examples/opentelemetry/valid-agent-workflow-trace.json` | root agent operation `workflow.execute`, one workflow invocation span, two descendant tool spans | adapter succeeds and validator passes | generated statement passes validator with `ok=true`, `issue_count=0`; scoped tests pass | second valid operation context confirms deeper parent-chain resolution |
| `invalid-missing-agent-span` | `examples/opentelemetry/invalid-missing-agent-span.json` | no agent span | adapter fails with `missing_agent_span` | scoped test preserves expected diagnostic | no accountable agent can be selected |
| `invalid-unresolved-tool-span` | `examples/opentelemetry/invalid-unresolved-tool-span.json` | tool span not under selected agent span | adapter fails with `unresolved_tool_span` | scoped test preserves expected diagnostic | unattached tool spans are not converted into operation evidence |
| `invalid-broken-parent-span` | `examples/opentelemetry/invalid-broken-parent-span.json` | span references missing parent | adapter fails with `broken_parent_span_relation` | scoped test preserves expected diagnostic | broken trace ancestry prevents safe mapping |
| `invalid-missing-operation-name` | `examples/opentelemetry/invalid-missing-operation-name.json` | agent span lacks operation name | adapter fails with `missing_operation_name` | scoped test preserves expected diagnostic | an unnamed operation cannot become an operation accountability statement |

Scoped test result:

```text
8 passed in 2.48s
```

Manual validator results:

```text
generated/valid-agent-trace-eeoap-statement.json: ok=true, issue_count=0
generated/valid-agent-workflow-trace-eeoap-statement.json: ok=true, issue_count=0
```
