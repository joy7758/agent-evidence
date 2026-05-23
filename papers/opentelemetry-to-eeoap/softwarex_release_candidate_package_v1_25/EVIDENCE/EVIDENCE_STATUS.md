# Evidence Status

## Included Trace Contexts

This package includes two valid synthetic OpenTelemetry-style trace contexts:

- `EVIDENCE/examples/opentelemetry/valid-agent-trace.json`
- `EVIDENCE/examples/opentelemetry/valid-agent-workflow-trace.json`

It also includes four invalid diagnostic contexts:

- `EVIDENCE/examples/opentelemetry/invalid-missing-agent-span.json`
- `EVIDENCE/examples/opentelemetry/invalid-unresolved-tool-span.json`
- `EVIDENCE/examples/opentelemetry/invalid-broken-parent-span.json`
- `EVIDENCE/examples/opentelemetry/invalid-missing-operation-name.json`

## Included Generated Artifacts

- `EVIDENCE/generated/valid-agent-trace-eeoap-statement.json`
- `EVIDENCE/generated/valid-agent-trace-adapter-report.json`
- `EVIDENCE/generated/valid-agent-workflow-trace-eeoap-statement.json`
- `EVIDENCE/generated/valid-agent-workflow-trace-adapter-report.json`

The two generated EEOAP-compatible statements are expected to validate with
`ok=true` and `issue_count=0`.

## Package Role

This support package includes the version 0.7 second valid trace evidence. It
supersedes version 1.15 as the current support package for SoftwareX
preparation after version 1.24 metadata drafts were added.

The version 0.5 frozen package remains historical only.
