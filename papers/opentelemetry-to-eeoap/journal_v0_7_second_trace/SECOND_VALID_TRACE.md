# Second Valid Trace

## Fixture Path

`examples/opentelemetry/valid-agent-workflow-trace.json`

## Operation Pattern

The fixture represents a synthetic workflow-style agent operation. The root
agent span declares `gen_ai.operation.name=workflow.execute`. A child workflow
invocation span represents a local workflow invocation. Two tool execution
spans are attached below that workflow invocation span.

This differs from the first valid fixture, where the operation is
`research.answer` and both tool spans are direct children of the agent span.

## Span Structure

| Span | Role | Parent | Key operation attribute |
|---|---|---|---|
| `4444444444444444` | root agent span | none | `workflow.execute` |
| `5555555555555555` | workflow invocation span | `4444444444444444` | `workflow.invoke` |
| `6666666666666666` | tool execution span | `5555555555555555` | `execute_tool` |
| `7777777777777777` | tool execution span | `5555555555555555` | `execute_tool` |

Trace id:

```text
bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb
```

Agent attributes:

- `gen_ai.agent.id`: `agent:workflow-coordinator-002`
- `gen_ai.agent.name`: `workflow-coordinator`
- `gen_ai.agent.version`: `0.2.0`

## Mapped EEOAP Statement Path

`generated/valid-agent-workflow-trace-eeoap-statement.json`

## Adapter Report Path

`generated/valid-agent-workflow-trace-adapter-report.json`

## Validator Result

The generated statement passed the existing EEOAP validator:

```text
PASS execution-evidence-operation-accountability-profile@0.1 generated/valid-agent-workflow-trace-eeoap-statement.json
ok=true
issue_count=0
```

Validator stages passed:

- `schema`
- `references`
- `consistency`
- `integrity`

## Difference From The First Valid Trace

| Aspect | First valid trace | Second valid trace |
|---|---|---|
| Fixture | `valid-agent-trace.json` | `valid-agent-workflow-trace.json` |
| Operation | `research.answer` | `workflow.execute` |
| Agent | `research-assistant` | `workflow-coordinator` |
| Trace id | `aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa` | `bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb` |
| Agent span id | `1111111111111111` | `4444444444444444` |
| Tool span ancestry | direct children of agent span | children of workflow invocation span |
| Intermediate non-tool span | none | `workflow.invoke.local-review` |

## Evaluation Value

The second trace strengthens evaluation without overclaiming. It demonstrates
a second controlled valid context and a deeper parent-child span structure,
but it remains synthetic and local. It does not claim production telemetry,
broad OpenTelemetry compatibility, real framework integration, or
cross-framework generality.
