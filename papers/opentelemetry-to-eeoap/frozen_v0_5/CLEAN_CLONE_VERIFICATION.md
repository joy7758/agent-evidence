# Clean Clone Verification

Verification date: 2026-05-23

Verified commit: `393aded70f9e3230ac93fb277476d8a8fc2cfb6e`

Branch: `opentelemetry-to-eeoap-adapter`

Clean clone path: `/tmp/agent-evidence-otel-eeoap-clean-verify`

Frozen package path: `papers/opentelemetry-to-eeoap/frozen_v0_5/`

## Current Repository Preflight

The verification started in the original repository at `/Users/zhangbin/GitHub/agent-evidence`.

Commands used:

```sh
git branch --show-current
git status --short
git log --oneline -8
git rev-parse HEAD
```

Observed branch:

```text
opentelemetry-to-eeoap-adapter
```

Observed HEAD:

```text
393aded70f9e3230ac93fb277476d8a8fc2cfb6e
```

Recent commit chain:

```text
393aded Freeze OpenTelemetry-to-EEOAP paper package v0.5
62b1b4f Prepare OpenTelemetry-to-EEOAP paper v0.4 citation draft
af28ea5 Prepare OpenTelemetry-to-EEOAP paper v0.3 submission draft
07d31cd Revise OpenTelemetry-to-EEOAP paper to v0.2
c4a7d56 Draft OpenTelemetry-to-EEOAP paper v0.1
ff8c794 Add paper-facing evidence closure for OpenTelemetry adapter
c5df6ce Add OpenTelemetry-to-EEOAP adapter prototype
b28c050 Add EEOAP paper release checklist
```

Existing dirty worktree items were present before this verification step:

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

These out-of-scope dirty worktree items were not cleaned, stashed, reset, staged, or modified by this verification step.

## Clean Clone Commands

Commands used:

```sh
rm -rf /tmp/agent-evidence-otel-eeoap-clean-verify
git clone "$(pwd)" /tmp/agent-evidence-otel-eeoap-clean-verify
cd /tmp/agent-evidence-otel-eeoap-clean-verify
git checkout 393aded70f9e3230ac93fb277476d8a8fc2cfb6e
test -d papers/opentelemetry-to-eeoap/frozen_v0_5
git rev-parse HEAD
git status --short
pytest tests/test_opentelemetry_to_eeoap_adapter.py -q
/Users/zhangbin/GitHub/agent-evidence/.venv/bin/python -m pytest tests/test_opentelemetry_to_eeoap_adapter.py -q
cd papers/opentelemetry-to-eeoap/frozen_v0_5
shasum -a 256 -c CHECKSUMS.sha256
cd /tmp/agent-evidence-otel-eeoap-clean-verify
git status --short
```

The direct `pytest` command was not available on the shell path in the clean clone environment:

```text
zsh:1: command not found: pytest
```

The scoped test was therefore executed against the clean checkout by using the original repository's existing virtual environment Python interpreter while keeping the working directory inside the clean clone.

## Clean Clone Results

Checked-out commit:

```text
393aded70f9e3230ac93fb277476d8a8fc2cfb6e
```

Frozen package exists:

```text
papers/opentelemetry-to-eeoap/frozen_v0_5/
```

Scoped adapter test command:

```sh
/Users/zhangbin/GitHub/agent-evidence/.venv/bin/python -m pytest tests/test_opentelemetry_to_eeoap_adapter.py -q
```

Scoped adapter test result:

```text
......                                                                   [100%]
6 passed in 1.70s
```

Checksum command:

```sh
shasum -a 256 -c CHECKSUMS.sha256
```

Checksum result:

```text
./FREEZE_STATUS.md: OK
./MANIFEST.md: OK
./NEXT_ACTIONS.md: OK
./README.md: OK
./artifact_freeze_note.md: OK
./claim_boundary.md: OK
./evaluation_summary.md: OK
./paper_v0_4.md: OK
./references_draft.md: OK
./reviewer_positioning.md: OK
./submission_checklist.md: OK
```

Clean clone git status result after verification:

```text

```

No untracked files were produced by the clean clone verification.

## Conclusion

The OpenTelemetry-to-EEOAP v0.5 frozen package is reproducible from a clean checkout of commit `393aded70f9e3230ac93fb277476d8a8fc2cfb6e`.

Runtime code was not changed by this verification step. Tests were not changed by this verification step. The EEOAP schema was not changed by this verification step. Unrelated SoftwareX, pd-oap, tmp worktree changes remain out of scope.
