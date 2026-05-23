# Evidence Status

## Included Evidence

This package includes:

- two valid OpenTelemetry-style trace contexts;
- four invalid diagnostic trace contexts;
- two generated EEOAP-compatible statements;
- two adapter reports.

## Valid Trace Contexts

- `EVIDENCE/examples/opentelemetry/valid-agent-trace.json`
- `EVIDENCE/examples/opentelemetry/valid-agent-workflow-trace.json`

## Invalid Diagnostic Contexts

- `EVIDENCE/examples/opentelemetry/invalid-missing-agent-span.json`
- `EVIDENCE/examples/opentelemetry/invalid-unresolved-tool-span.json`
- `EVIDENCE/examples/opentelemetry/invalid-broken-parent-span.json`
- `EVIDENCE/examples/opentelemetry/invalid-missing-operation-name.json`

## Generated Outputs

- `EVIDENCE/generated/valid-agent-trace-eeoap-statement.json`
- `EVIDENCE/generated/valid-agent-trace-adapter-report.json`
- `EVIDENCE/generated/valid-agent-workflow-trace-eeoap-statement.json`
- `EVIDENCE/generated/valid-agent-workflow-trace-adapter-report.json`

## Validation Meaning

Both valid generated statements passed the existing EEOAP validator with
`ok=true` and `issue_count=0` during this version 1.15 package creation.

The historical version 0.5 frozen package predates the second valid trace. This
version 1.15 support package is the forward local support package for SoftwareX
preparation.
