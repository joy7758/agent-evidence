# AEP-Media Mission 019 Release Archive and SoftwareX Finalization Report

Date: 2026-05-10

## 1. Mission Result Summary

Mission 019 prepared the AEP-Media v0.1.0 release candidate and refreshed the SoftwareX final submission pack metadata. No GitHub release was published and no tag was pushed because `AEP_MEDIA_PUBLISH_RELEASE` was not set to `1`.

Current readiness: NEAR READY.

Reason: tests, evaluation, release-candidate packaging, and red-line scans pass, but an AEP-Media-specific archive DOI is not yet confirmed.

## 2. Release Candidate Status

Release candidate generated:

- `docs/paper/softwarex/final/release/staging/AEP-Media-v0.1.0-release-candidate.zip`
- `docs/paper/softwarex/final/release/staging/AEP-Media-v0.1.0-release-candidate.sha256`

Release candidate checksum:

- `71fd7940fc1c99705321bcb8c3198061d549862e044f8b8b879b87675172020c`

Release tag proposal:

- `aep-media-v0.1.0`

Release title:

- `AEP-Media v0.1.0: Offline Validation of Time-Aware Media Evidence Bundles`

## 3. Tests and Evaluation Results

Final pre-release validation:

- Targeted AEP-Media tests: `48 passed, 1 warning`
- SoftwareX/readiness tests: `23 passed, 1 warning`
- Full pytest: `155 passed, 1 skipped, 15 warnings`
- Ruff: `All checks passed!`
- `git diff --check`: passed

Evaluation CLI:

- Default evaluation: `PASS aep-media-evaluation@0.1 cases=18 unexpected=0`
- Adapter-inclusive evaluation: `PASS aep-media-evaluation@0.1 cases=26 unexpected=0 adapters=included`
- Optional-tool reporting evaluation: `PASS aep-media-evaluation@0.1 cases=23 unexpected=0 optional_tools=included`
- Combined evaluation: `PASS aep-media-evaluation@0.1 cases=31 unexpected=0 adapters=included optional_tools=included`

Release pack CLI:

- `PASS aep-media-release-pack@0.1`

## 4. Red-Line Scan Result

Release-facing materials and the release candidate were scanned for local absolute paths, template placeholders, old local staging status phrases, unrelated paper workspace names, and inflated legal/forensic/security claims.

Result: PASS.

Claim-boundary terms appear only as explicit non-claims or limitations.

## 5. Release Metadata Status

Updated or verified:

- `CITATION.cff`
- `.zenodo.json`
- `codemeta.json`
- `docs/how-to-cite.md`
- SoftwareX manuscript archive note
- SoftwareX submission metadata

No DOI was invented or inserted.

## 6. GitHub Release Status

GitHub release status: NOT PUBLISHED.

Reason: publish guard not enabled.

Command preview is recorded in:

- `docs/paper/softwarex/final/release/reports/aep_media_v0.1.0_doi_action_required.md`

## 7. Zenodo DOI / Archive Status

Zenodo DOI status: ACTION REQUIRED.

No AEP-Media-specific DOI was created during this mission. The broader repository DOI remains separate from the proposed AEP-Media v0.1.0 release until confirmed.

## 8. SoftwareX Final Pack Status

SoftwareX final pack refreshed:

- main manuscript DOCX/PDF/TEX under `docs/paper/softwarex/final/submission-pack/main/`
- cover letter under `docs/paper/softwarex/final/submission-pack/cover-letter/`
- supplementary zip under `docs/paper/softwarex/final/submission-pack/`
- metadata under `docs/paper/softwarex/final/submission-pack/metadata/`

The manuscript and metadata state that the AEP-Media-specific archive DOI is pending release archive and remains action required before final submission.

## 9. Files Generated

- `docs/paper/softwarex/final/release/reports/release_baseline_audit.md`
- `docs/paper/softwarex/final/release/reports/git_release_scope_audit.md`
- `docs/paper/softwarex/final/release/reports/final_pre_release_validation.md`
- `docs/paper/softwarex/final/release/reports/release_redline_scan.md`
- `docs/paper/softwarex/final/release/reports/aep_media_v0.1.0_doi_action_required.md`
- `docs/paper/softwarex/final/release/notes/aep-media-v0.1.0-release-notes.md`
- `docs/paper/softwarex/final/release/staging/AEP-Media-v0.1.0-release-candidate.zip`
- `docs/paper/softwarex/final/release/staging/AEP-Media-v0.1.0-release-candidate.sha256`
- `docs/paper/softwarex/final/submission-pack/metadata/softwarex_submission_metadata.md`

## 10. Files Updated

- `CITATION.cff`
- `.zenodo.json`
- `codemeta.json`
- `docs/how-to-cite.md`
- `docs/project-facts.md`
- `docs/callable-surfaces.md`
- `docs/paper/softwarex/aep_media_softwarex_metadata.md`
- `docs/paper/softwarex/final/aep_media_softwarex_final_manuscript.md`
- `docs/paper/softwarex/final/reports/aep_media_archive_doi_readiness.md`
- SoftwareX submission-pack outputs

## 11. Current Readiness

Current readiness: NEAR READY.

## 12. Remaining Blockers

1. Human approval to publish the release.
2. Create GitHub release `aep-media-v0.1.0`.
3. Confirm Zenodo GitHub integration and obtain the generated DOI.
4. Update citation metadata, SoftwareX manuscript, SoftwareX metadata, release notes, and final pack with the real DOI.

## 13. Exact Next Action

If ready to publish, rerun with:

```bash
AEP_MEDIA_PUBLISH_RELEASE=1
```

Do not publish before checking the intended release scope and excluding unrelated workspaces.
