# From Agent Telemetry to Portable Operation Evidence: Journal Plan v0.7

This is a journal-oriented planning draft, not a final manuscript. Its purpose
is to update the paper narrative after v0.7 expanded the evaluation from one
valid trace to two valid trace contexts.

## 1. Current Journal Thesis

This paper studies telemetry-to-evidence transformation as a bounded software
engineering method. It shows that OpenTelemetry-style agent traces can be
transformed into EEOAP-compatible operation accountability statements under
two controlled valid trace contexts and four controlled invalid diagnostic
contexts, without modifying the EEOAP schema.

The journal version should present the work as a method for moving from
runtime observability records to portable, validator-checkable operation
evidence objects. The paper should not present the work as a new profile, a
legal accountability framework, a production runtime integration, or a broad
OpenTelemetry compatibility study.

## 2. Why v0.7 Is Stronger Than v0.5

v0.5 had one valid trace and four invalid traces. That package was strong as
an artifact-style frozen package because it showed one complete path from an
OpenTelemetry-style trace into an EEOAP-compatible statement, plus four
controlled diagnostic failures.

v0.7 adds a second valid workflow-style trace:

```text
examples/opentelemetry/valid-agent-workflow-trace.json
```

The second trace introduces a deeper parent-child span relation. Its two tool
spans are children of a workflow invocation span, not direct children of the
agent span:

```text
agent span 4444444444444444
  workflow invocation span 5555555555555555
    tool span 6666666666666666
    tool span 7777777777777777
```

Both valid generated statements pass the existing EEOAP validator:

```text
generated/valid-agent-trace-eeoap-statement.json
PASS, ok=true, issue_count=0

generated/valid-agent-workflow-trace-eeoap-statement.json
PASS, ok=true, issue_count=0
```

This strengthens the evaluation without claiming broad OpenTelemetry
compatibility. The evidence still stays local, synthetic, and controlled, but
the adapter is now tested against two successful operation contexts rather
than one.

## 3. Revised Research Questions

RQ1: Can OpenTelemetry-style agent telemetry be transformed into
EEOAP-compatible operation accountability statements without modifying the
EEOAP schema?

RQ2: Can the adapter support more than one valid trace context, including a
workflow-style parent-child span pattern?

RQ3: Can controlled invalid traces expose bounded and meaningful
telemetry-to-evidence diagnostic surfaces?

## 4. Revised Contributions

C1. A bounded telemetry-to-evidence mapping model from OpenTelemetry-style
agent spans to EEOAP-compatible operation accountability statements.

C2. A minimal adapter implementation that preserves trace/span provenance,
resolves tool spans, checks parent-child span relations, and emits
validator-ready EEOAP statements.

C3. A controlled evaluation set with two valid trace contexts and four invalid
diagnostic contexts.

C4. A reproducibility package with generated statements, adapter reports,
scoped tests, checksum verification, clean-clone verification, and external
review notes.

## 5. Revised Evaluation Story

| Case | Trace pattern | Expected outcome | Observed result | Journal relevance |
|---|---|---|---|---|
| `valid-agent-trace` | Root agent operation `research.answer` with two direct child tool spans. | Adapter emits an EEOAP-compatible statement and validator passes. | PASS; generated statement validates with `ok=true`, `issue_count=0`. | Baseline positive context proves the original telemetry-to-evidence path. |
| `valid-agent-workflow-trace` | Root agent operation `workflow.execute`, one workflow invocation span, and two descendant tool spans. | Adapter resolves a deeper parent-child chain, emits an EEOAP-compatible statement, and validator passes. | PASS; generated statement validates with `ok=true`, `issue_count=0`. | Second positive context shows the adapter is not tied to one trace shape. |
| `invalid-missing-agent-span` | Trace lacks a span with `gen_ai.agent.*` attributes. | Adapter fails with `missing_agent_span`. | Expected diagnostic preserved by scoped tests. | Shows the adapter requires an accountable agent boundary. |
| `invalid-unresolved-tool-span` | Tool span is not under the selected agent span. | Adapter fails with `unresolved_tool_span`. | Expected diagnostic preserved by scoped tests. | Shows unattached tool spans are not converted into operation evidence. |
| `invalid-broken-parent-span` | Span references a missing parent span. | Adapter fails with `broken_parent_span_relation`. | Expected diagnostic preserved by scoped tests. | Shows broken span ancestry blocks safe mapping. |
| `invalid-missing-operation-name` | Agent span lacks `gen_ai.operation.name`. | Adapter fails with `missing_operation_name`. | Expected diagnostic preserved by scoped tests. | Shows an unnamed span cannot become an operation accountability statement. |

Scoped pytest result:

```text
8 passed in 2.48s
```

The evaluation story should therefore be:

```text
2 valid traces
4 invalid traces
2 generated EEOAP statements
2 validator passes
4 controlled adapter diagnostics
```

## 6. How to Reframe the Paper

The paper should shift from:

```text
Here is a small adapter artifact.
```

to:

```text
Here is a bounded software engineering method for transforming runtime
telemetry into portable operation evidence objects, validated across two
successful trace contexts and controlled failure surfaces.
```

This reframing should not inflate the technical claim. The method remains
bounded and artifact-backed. The journal version should emphasize the
engineering shape of the method:

- select an accountable agent span;
- require an operation name;
- resolve tool spans through parent-child ancestry;
- preserve trace/span provenance through locators and evidence artifacts;
- emit an EEOAP-compatible statement;
- validate the generated statement through the existing EEOAP validator;
- reject traces that cannot support the operation evidence claim.

## 7. What Still Must Not Be Claimed

The journal version must preserve these non-claims:

- no legal accountability proof
- no full runtime reconstruction
- no general OpenTelemetry implementation compatibility
- no cross-framework generality
- no agent-output correctness
- no production readiness
- no new EEOAP profile
- no regulatory compliance
- no complete agent governance framework

These non-claims are not cosmetic caveats. They define the boundary that makes
the paper defensible as a focused software engineering contribution rather
than an overbroad governance claim.

## 8. Journal Manuscript Structure

### 1. Introduction

- State that runtime telemetry is useful but not automatically portable
  operation evidence.
- Present the telemetry-to-evidence adapter as the central method contribution.
- Introduce EEOAP as the existing target evidence object and validator path.
- Summarize the two-valid/four-invalid evaluation.
- State the non-claim boundary early.

### 2. Problem: Telemetry Is Not Portable Operation Evidence

- Explain the difference between observability traces and evidence objects.
- Show why trace fields need interpretation before they can support
  accountability statements.
- Use tool-span parentage and missing operation names as motivating failure
  examples.
- Define what "portable operation evidence" means in this paper.

### 3. Background: OpenTelemetry Agent Spans and EEOAP Evidence Objects

- Summarize the OpenTelemetry-style source fields used by the adapter.
- Summarize EEOAP statement sections: actor, subject, operation, policy,
  constraints, provenance, evidence, and validation.
- Explain that the paper does not modify EEOAP schema.
- Position AEP as related but broader runtime evidence packaging work.

### 4. Method: Telemetry-to-Evidence Mapping

- Present the mapping from trace/span fields to EEOAP statement fields.
- Distinguish field extraction from evidence-object construction.
- Explain parent-child span closure and tool-span resolution.
- Explain why malformed mappings fail before EEOAP statement emission.
- Include the telemetry-to-evidence mapping table.

### 5. Adapter Implementation

- Describe the local adapter script and its no-network, no-collector boundary.
- Explain input fixture format and output statement/report paths.
- Describe provenance locators and evidence artifact construction.
- Explain integrity recomputation and validator routing.
- Note that v0.7 did not require adapter code changes.

### 6. Evaluation

- Present the two valid trace contexts and four invalid diagnostic contexts.
- Report validator success for both generated valid statements.
- Report scoped pytest result: `8 passed in 2.48s`.
- Compare raw telemetry-only representation with generated EEOAP statements.
- Explain what each invalid diagnostic demonstrates.

### 7. Discussion

- Discuss why the second workflow trace strengthens the claim without
  overclaiming.
- Explain why this is more than field copying.
- Discuss how semantic-convention evolution should be treated as a source-side
  versioning issue.
- Explain why broad OpenTelemetry compatibility is deferred.

### 8. Threats to Validity

- State that both valid traces are controlled and synthetic.
- State that the evaluation does not include production telemetry.
- State that there is no LangChain runtime or OpenTelemetry Collector
  integration.
- Discuss limited fixture diversity and draft references.
- Reaffirm the claim-upgrade rule: no stronger claim without committed
  fixture, output, test, and validation evidence.

### 9. Related Work

- Discuss OpenTelemetry and GenAI agent span semantics as source-side context.
- Discuss EEOAP as the target evidence object and validator path.
- Discuss AEP as broader evidence-bundle work, not a duplicate contribution.
- Discuss provenance and structured validation as adjacent foundations.
- Discuss artifact review and reproducibility expectations.

### 10. Conclusion

- Restate that telemetry can be transformed into portable operation evidence
  under bounded conditions.
- Summarize the two valid traces, four invalid diagnostics, and validator
  results.
- Emphasize that the EEOAP schema was not changed.
- Preserve the non-claim boundary.
- Point to future work: journal draft, final references, and later runtime
  integration only after the journal narrative is stable.

## 9. Required Tables for Journal Draft

- Table 1: Telemetry-to-evidence mapping. It should show OpenTelemetry source
  fields, adapter extraction, EEOAP target fields, validation relevance, and
  failure behavior.
- Table 2: Valid trace contexts. It should compare `valid-agent-trace` and
  `valid-agent-workflow-trace`, including operation pattern, span ancestry,
  generated statement path, and validator result.
- Table 3: Invalid diagnostic cases. It should list the four invalid fixtures,
  violated precondition, expected diagnostic, statement emission result, and
  interpretation.
- Table 4: Telemetry-only vs EEOAP statement comparison. It should show what
  raw traces capture and what EEOAP adds, without dismissing telemetry as
  useless.
- Table 5: Claim boundary. It should separate allowed claims, disallowed
  claims, and evidence required to upgrade any claim.
- Table 6: Reproducibility evidence. It should list scoped tests, generated
  statements, adapter reports, validator results, checksum verification,
  clean-clone verification, and external review notes.

## 10. Next Writing Task

The next writing task should be to create
`paper_v0_8_journal_draft.md` using this v0.7 journal plan.

## 11. Command Log

### Commands Run

Plugin/tool inspection:

```sh
tool_search query="plan task file edit test local repository workflow"
```

Memory/context and preflight:

```sh
rg -n "agent-evidence|artifact-first|EEOAP journal|docs-only|targeted validation|full-repo" /Users/zhangbin/.codex/memories/MEMORY.md
git branch --show-current
git status --short
git log --oneline -10
git rev-parse HEAD
```

Evidence inspection:

```sh
sed -n '1,260p' papers/opentelemetry-to-eeoap/paper_v0_4.md
sed -n '1,240p' papers/opentelemetry-to-eeoap/journal_v0_6_gap_analysis/JOURNAL_GAP_ANALYSIS.md
sed -n '1,180p' papers/opentelemetry-to-eeoap/journal_v0_6_gap_analysis/JOURNAL_ROUTE_DECISION.md
sed -n '1,240p' papers/opentelemetry-to-eeoap/journal_v0_7_second_trace/EVALUATION_UPDATE.md
sed -n '1,240p' papers/opentelemetry-to-eeoap/journal_v0_7_second_trace/SECOND_VALID_TRACE.md
sed -n '1,220p' tests/test_opentelemetry_to_eeoap_adapter.py
sed -n '1,220p' generated/valid-agent-trace-eeoap-statement.json
sed -n '1,220p' generated/valid-agent-workflow-trace-eeoap-statement.json
sed -n '1,220p' examples/opentelemetry/valid-agent-workflow-trace.json
```

Planned validation:

```sh
/Users/zhangbin/GitHub/agent-evidence/.venv/bin/python -m pytest tests/test_opentelemetry_to_eeoap_adapter.py -q
```

Scoped pytest result:

```text
........                                                                 [100%]
8 passed in 2.01s
```

### Git Status Before

Branch:

```text
opentelemetry-to-eeoap-adapter
```

HEAD:

```text
43cb4888f8a2c0f90e7c7e80f3e486c6eedef563
```

Existing dirty worktree items before this planning draft:

```text
 M docs/paper/softwarex/final/aep_media_softwarex_final_manuscript.md
 M docs/paper/softwarex/final/submission-pack/UPLOAD_MANIFEST.md
 M docs/paper/softwarex/final/submission-pack/main/AEP-Media_SoftwareX_Manuscript.docx
 M docs/paper/softwarex/final/submission-pack/main/AEP-Media_SoftwareX_Manuscript.pdf
 M docs/paper/softwarex/final/submission-pack/metadata/softwarex_submission_metadata.md
?? codex-eeoap-low-risk-summary.md
?? docs/paper/aep_media_abstract.md
?? docs/paper/aep_media_cover_letter_draft.md
?? docs/paper/aep_media_cover_letter_high_revision.docx
?? docs/paper/aep_media_cover_letter_high_revision.md
?? docs/paper/aep_media_digital_evidence_abstract.md
?? docs/paper/aep_media_editor_defense_notes.md
?? docs/paper/aep_media_evaluation_section.md
?? docs/paper/aep_media_final_reference_list.md
?? docs/paper/aep_media_ieee_word_conversion_report.md
?? docs/paper/aep_media_ieee_word_final_checklist.md
?? docs/paper/aep_media_ieee_word_style_checklist.md
?? docs/paper/aep_media_ieee_word_submission_metadata.md
?? docs/paper/aep_media_manuscript_draft.md
?? docs/paper/aep_media_methods_section.md
?? docs/paper/aep_media_paper_outline.md
?? docs/paper/aep_media_related_work_matrix.md
?? docs/paper/aep_media_related_work_notes.md
?? docs/paper/aep_media_retargeting_strategy.md
?? docs/paper/aep_media_software_artifact_abstract.md
?? docs/paper/aep_media_submission_appendix.md
?? docs/paper/aep_media_submission_checklist.md
?? docs/paper/aep_media_submission_risk_register.md
?? docs/paper/aep_media_threats_to_validity.md
?? docs/paper/aep_media_tse_format_preflight.md
?? docs/paper/aep_media_tse_submission_draft.md
?? docs/paper/aep_media_tse_submission_high_revision.docx
?? docs/paper/aep_media_tse_submission_high_revision.md
?? docs/paper/aep_media_tse_submission_high_revision.pdf
?? docs/paper/final-submission-checklist.md
?? docs/paper/ieee_tse_submission_resources/
?? docs/paper/softwarex/final/submission-pack/supplementary/AEP-Media_SoftwareX_Supplementary_S1.pdf
?? docs/reports/aep_media_final_editor_attack_defense.md
?? docs/reports/aep_media_mission008_report.md
?? docs/reports/aep_media_mission009_report.md
?? docs/reports/aep_media_mission010_report.md
?? docs/reports/aep_media_mission011_high_revision_report.md
?? docs/reports/aep_media_tse_decision_archive_note.md
?? docs/reports/aep_media_tse_rejection_analysis.md
?? paper-ncs-execution-evidence/
?? pd-oap.zip
?? pd-oap/
?? tmp/
```

These out-of-scope items were not cleaned, stashed, reset, staged, or
modified.

### Git Status After

Status after creating the planning draft and running scoped pytest, before
staging:

```text
 M docs/paper/softwarex/final/aep_media_softwarex_final_manuscript.md
 M docs/paper/softwarex/final/submission-pack/UPLOAD_MANIFEST.md
 M docs/paper/softwarex/final/submission-pack/main/AEP-Media_SoftwareX_Manuscript.docx
 M docs/paper/softwarex/final/submission-pack/main/AEP-Media_SoftwareX_Manuscript.pdf
 M docs/paper/softwarex/final/submission-pack/metadata/softwarex_submission_metadata.md
?? codex-eeoap-low-risk-summary.md
?? docs/paper/aep_media_abstract.md
?? docs/paper/aep_media_cover_letter_draft.md
?? docs/paper/aep_media_cover_letter_high_revision.docx
?? docs/paper/aep_media_cover_letter_high_revision.md
?? docs/paper/aep_media_digital_evidence_abstract.md
?? docs/paper/aep_media_editor_defense_notes.md
?? docs/paper/aep_media_evaluation_section.md
?? docs/paper/aep_media_final_reference_list.md
?? docs/paper/aep_media_ieee_word_conversion_report.md
?? docs/paper/aep_media_ieee_word_final_checklist.md
?? docs/paper/aep_media_ieee_word_style_checklist.md
?? docs/paper/aep_media_ieee_word_submission_metadata.md
?? docs/paper/aep_media_manuscript_draft.md
?? docs/paper/aep_media_methods_section.md
?? docs/paper/aep_media_paper_outline.md
?? docs/paper/aep_media_related_work_matrix.md
?? docs/paper/aep_media_related_work_notes.md
?? docs/paper/aep_media_retargeting_strategy.md
?? docs/paper/aep_media_software_artifact_abstract.md
?? docs/paper/aep_media_submission_appendix.md
?? docs/paper/aep_media_submission_checklist.md
?? docs/paper/aep_media_submission_risk_register.md
?? docs/paper/aep_media_threats_to_validity.md
?? docs/paper/aep_media_tse_format_preflight.md
?? docs/paper/aep_media_tse_submission_draft.md
?? docs/paper/aep_media_tse_submission_high_revision.docx
?? docs/paper/aep_media_tse_submission_high_revision.md
?? docs/paper/aep_media_tse_submission_high_revision.pdf
?? docs/paper/final-submission-checklist.md
?? docs/paper/ieee_tse_submission_resources/
?? docs/paper/softwarex/final/submission-pack/supplementary/AEP-Media_SoftwareX_Supplementary_S1.pdf
?? docs/reports/aep_media_final_editor_attack_defense.md
?? docs/reports/aep_media_mission008_report.md
?? docs/reports/aep_media_mission009_report.md
?? docs/reports/aep_media_mission010_report.md
?? docs/reports/aep_media_mission011_high_revision_report.md
?? docs/reports/aep_media_tse_decision_archive_note.md
?? docs/reports/aep_media_tse_rejection_analysis.md
?? paper-ncs-execution-evidence/
?? papers/opentelemetry-to-eeoap/paper_v0_7_journal_plan.md
?? pd-oap.zip
?? pd-oap/
?? tmp/
```

### Change Boundary

- Runtime code changed: no.
- Tests changed: no.
- Fixtures changed: no.
- Generated JSON outputs changed: no.
- EEOAP schema changed: no.
- Adapter features added: no.
- LangChain runtime integration added: no.
- OpenTelemetry Collector integration added: no.
- Out-of-scope worktree items touched: no.

### Plugin Selection Report

Tool/workflow inspection was performed before implementation.

Selected:

- `tool_search`: used to inspect whether a more specialized local
  plan/task/file-edit/test plugin was available.
- `update_plan`: used to create and track a short execution plan.
- `apply_patch`: used for the single deterministic Markdown file edit.
- `exec_command`: used for repository inspection, evidence inspection,
  scoped pytest, and git checks.

Not selected:

- Canva, Figma, Google Drive, Hugging Face, OpenAI Platform, and Node REPL
  tools were available but not relevant to this local Markdown planning task.

Reason:

This task is a local paper-planning update. It does not require external
design tools, cloud documents, model search, API-key setup, or browser/runtime
automation.
