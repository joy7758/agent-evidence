# AEP-Media Mission 016 SoftwareX Preparation Report

## 1. Goal

Mission 016 prepares AEP-Media for Path A retargeting as a software/artifact paper after the IEEE TSE initial editorial scope rejection. The primary target is SoftwareX-style submission. JOSS is kept as a compatibility check, and Forensic Science International: Digital Investigation is kept as a Path B backup.

## 2. Scope

This mission does not change implementation logic. It does not add validators, schemas, adapters, tests, demos, or features. It only creates software/artifact submission materials and updates repository status.

## 3. Inputs Reviewed

Found:

- `docs/reports/aep_media_tse_rejection_analysis.md`
- `docs/paper/aep_media_retargeting_strategy.md`
- `docs/paper/aep_media_software_artifact_abstract.md`
- `docs/paper/aep_media_digital_evidence_abstract.md`
- `docs/reports/aep_media_tse_decision_archive_note.md`
- `spec/aep-media-profile-v0.1.md`
- `spec/aep-media-bundle-v0.1.md`
- `spec/aep-media-time-trace-v0.1.md`
- `spec/aep-media-adapters-v0.1.md`
- `schema/aep_media_profile_v0_1.schema.json`
- `schema/aep_media_bundle_v0_1.schema.json`
- `schema/aep_media_time_trace_v0_1.schema.json`
- `schema/aep_media_adapter_report_v0_1.schema.json`
- `docs/reports/aep_media_mission004_report.md`
- `docs/reports/aep_media_mission005_report.md`
- `docs/reports/aep_media_mission006_report.md`
- `docs/reports/aep_media_mission007_report.md`
- `docs/reports/aep_media_adapter_claim_boundary.md`
- `docs/reports/aep_media_non_claims_matrix.md`
- `docs/reports/aep_media_reproducibility_checklist.md`

Missing:

- `docs/reports/aep_media_mission007_final_report.md`

The available `docs/reports/aep_media_mission007_report.md` was used instead.

## 4. Files Created

- `docs/paper/softwarex/aep_media_softwarex_manuscript_draft.md`
- `docs/paper/softwarex/aep_media_softwarex_metadata.md`
- `docs/paper/softwarex/aep_media_softwarex_software_description.md`
- `docs/paper/softwarex/aep_media_softwarex_statement_of_need.md`
- `docs/paper/softwarex/aep_media_softwarex_reproducibility.md`
- `docs/paper/softwarex/aep_media_softwarex_limitations.md`
- `docs/paper/softwarex/aep_media_softwarex_cover_letter.md`
- `docs/paper/softwarex/aep_media_softwarex_submission_checklist.md`
- `docs/paper/softwarex/aep_media_softwarex_joss_compatibility_check.md`
- `docs/paper/softwarex/aep_media_softwarex_fsidi_backup_positioning.md`
- `docs/reports/aep_media_mission016_softwarex_preparation_report.md`

## 5. Files Updated

- `docs/STATUS.md`
- `plans/implementation-plan.md`

## 6. Repository Readiness

Observed:

- Repository: `https://github.com/joy7758/agent-evidence`
- Package: `agent_evidence`
- Console script: `agent-evidence`
- License: Apache-2.0
- Repository DOI in README: `10.5281/zenodo.19334062`

Action required:

- Confirm repository is public at submission time.
- Confirm the repository DOI corresponds to the exact AEP-Media release, or create an AEP-Media-specific archive DOI.
- Make the AEP-Media path more discoverable from the top-level README.
- Rerun tests and evaluation commands for the final SoftwareX release.

## 7. Readiness Ratings

- SoftwareX readiness: NEAR READY.
- JOSS compatibility: POSSIBLE.
- FSIDI backup suitability: POSSIBLE.

## 8. Claim Boundary

The Path A package preserves the AEP-Media claim boundary. It does not claim legal admissibility, non-repudiation, trusted timestamping, real PTP proof, full MP4 PRFT parsing, real C2PA signature verification, chain of custody, production deployment, or proof that the original media capture event was truthful, authorized, or unmodified before packaging.

## 9. Validation

This mission only changes documentation. No implementation tests were required.

Validation performed:

- `git diff --check`: passed for the Mission 016 documentation scope.
- Newly created SoftwareX files contain no local absolute paths.
- Newly created SoftwareX files contain no references to unrelated paper workspaces.
- Non-claims are present only as claim-boundary language.

## 10. Next Mission Recommendation

Mission 017 should be Repository Readiness Audit and SoftwareX Final Pack:

- update README discoverability for AEP-Media;
- confirm or create release archive and DOI;
- rerun targeted tests and evaluation commands;
- prepare final SoftwareX template files;
- generate a clean SoftwareX submission pack.
