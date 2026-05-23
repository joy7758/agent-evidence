# OpenTelemetry to EEOAP Mapping

This note defines a bounded local adapter path from OpenTelemetry-style GenAI
trace JSON into the existing Execution Evidence and Operation Accountability
Profile v0.1.

The adapter does not create a new profile. It emits one EEOAP v0.1 operation
accountability statement and validates that statement with the existing
`agent-evidence validate-profile` path.

## Pipeline

```text
OpenTelemetry-style trace JSON
-> tools/opentelemetry_to_eeoap_adapter.py
-> generated/<case-name>-eeoap-statement.json
-> generated/<case-name>-adapter-report.json
-> agent-evidence validate-profile
```

## Field Mapping

| OpenTelemetry input | EEOAP v0.1 output |
|---|---|
| `traceId` / `trace_id` | `subject.id`, `subject.locator`, evidence locators |
| agent `spanId` / `span_id` | `operation.id`, `provenance.id`, evidence artifact id |
| `parentSpanId` / `parent_span_id` | adapter report provenance extraction |
| `gen_ai.agent.id` | `actor.id` |
| `gen_ai.agent.name` | `actor.name` |
| `gen_ai.agent.version` | `actor.runtime` suffix |
| `gen_ai.operation.name` on the agent span | `operation.type` |
| `execute_tool` spans | `evidence.artifacts[]` entries |
| span start/end timestamps | statement timestamp and adapter report extraction |
| `error.type` | operation result status and adapter report extraction |

## Evidence Shape

The generated statement keeps trace and span provenance links in schema-safe
locations:

- `subject.locator` points to the local trace JSON file.
- `evidence.references[]` binds the trace input and mapped operation result.
- `evidence.artifacts[]` records the agent span and each resolved
  `execute_tool` span with `otel://trace/<trace-id>/span/<span-id>` locators.
- `evidence.integrity` is recomputed by the existing EEOAP helper.

## Adapter Diagnostics

The adapter fails before statement emission for:

- `missing_agent_span`
- `unresolved_tool_span`
- `broken_parent_span_relation`
- `missing_operation_name`

Diagnostics are written to
`generated/<case-name>-adapter-report.json` so failures remain local and
reproducible.
