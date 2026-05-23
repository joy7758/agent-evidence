# Claim Readiness Check

This file checks whether v0.8 claims are supported by committed evidence.

| Claim | Evidence source | Support level | Action needed before submission |
|---|---|---|---|
| Telemetry is not automatically portable operation evidence. | `paper_v0_8_journal_draft.md`, `journal_v0_6_gap_analysis/COMPARISON_FRAMEWORK.md`, `frozen_v0_5/EXTERNAL_REVIEW_BRIEF.md`. | bounded | Keep as framing claim; support with OpenTelemetry and EEOAP references. |
| Adapter transforms OpenTelemetry-style traces to EEOAP-compatible statements. | `tools/opentelemetry_to_eeoap_adapter.py`, `generated/valid-agent-trace-eeoap-statement.json`, `generated/valid-agent-workflow-trace-eeoap-statement.json`, scoped tests. | strong | Keep wording as OpenTelemetry-style controlled fixtures, not broad implementation compatibility. |
| Adapter preserves trace/span provenance. | Generated statements, adapter reports, tests checking trace/span locators and artifact ids. | strong | Cite concrete generated files and explain locator semantics. |
| Adapter resolves tool spans. | Adapter code, valid-trace tests, workflow-trace tests, generated tool-span artifacts. | strong | Keep claim scoped to `execute_tool` spans under controlled fixture shape. |
| Adapter checks parent-child relationships. | Adapter parent closure logic, invalid broken-parent fixture, workflow trace with deeper parent chain. | strong | Keep diagnostics table in final paper. |
| Two valid traces pass. | `journal_v0_7_second_trace/EVALUATION_UPDATE.md`, `tests/test_opentelemetry_to_eeoap_adapter.py`, generated statements. | strong | Re-run before final submission and record current result. |
| Four invalid traces expose diagnostics. | Invalid fixtures, scoped tests, v0.7 evaluation update. | strong | Preserve diagnostic codes exactly. |
| Existing EEOAP validator accepts generated statements. | `journal_v0_7_second_trace/COMMAND_LOG.md`, generated adapter reports, validator tests. | strong | Re-run manual validator before submission candidate. |
| No EEOAP schema change required. | Commit chain, v0.7 command log, v0.8 draft preparation note. | strong | Keep statement factual: no schema changes in this branch for this adapter path. |
| Clean-clone verification supports reproducibility. | `frozen_v0_5/CLEAN_CLONE_VERIFICATION.md`, `frozen_v0_5/CHECKSUMS.sha256`. | bounded | v0.5 clean clone covers frozen package; consider repeating after v1.0 if submitting. |
| Broad OpenTelemetry compatibility is not claimed. | `paper_v0_8_journal_draft.md`, claim-boundary files, v0.9 citation notes showing evolving OpenTelemetry status. | strong | Keep as explicit non-claim in abstract, threats, and conclusion. |

## Overall Readiness

The core claims are supported if they remain bounded. The weakest external
submission point is not the adapter evidence; it is citation stability and
artifact-publication status. Before external submission, local artifact
references should be replaced by immutable public identifiers.
