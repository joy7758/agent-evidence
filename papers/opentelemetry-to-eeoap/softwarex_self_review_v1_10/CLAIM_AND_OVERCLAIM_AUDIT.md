# Claim and Overclaim Audit

| Statement or claim | Support evidence | Risk level | Action |
|---|---|---|---|
| Adapter transforms OpenTelemetry-style traces into EEOAP-compatible statements. | Adapter path, two valid generated statements, tests. | low | Keep. |
| Two valid trace contexts are evaluated. | `valid-agent-trace` and `valid-agent-workflow-trace`; generated statements. | low | Keep exact scope. |
| Four invalid diagnostics are evaluated. | Four invalid fixtures and scoped tests. | low | Keep diagnostic names. |
| Generated statements pass existing validator. | Validator result recorded as `ok=true`, `issue_count=0` for both valid statements. | low | Keep; cite generated paths. |
| No EEOAP schema modification was required. | Historical boundary and no schema edit in release-candidate path. | low | Keep. |
| Reproducibility package exists. | Frozen package, generated outputs, tests, clean-clone/checksum materials. | low | Keep but separate v0.5 frozen evidence from later v0.7 second trace. |
| No broad OpenTelemetry compatibility is claimed. | Explicit limitations. | low | Keep; avoid accidental broad wording. |
| No legal accountability is claimed. | Abstract, limitations, metadata drafts. | low | Keep. |
| No production readiness is claimed. | Limitations and availability notes. | low | Keep. |
| No real runtime integration is claimed. | Limitations say no LangChain runtime or Collector integration. | low | Keep. |
| Package is useful as research software. | Reproducible adapter, examples, generated artifacts, validator path. | medium | In v1.11, make utility more concrete through run path and review workflow. |
| Public artifact availability is implied. | Current draft says local only and TODO. | medium | Keep "draft only" wording until release exists. |
