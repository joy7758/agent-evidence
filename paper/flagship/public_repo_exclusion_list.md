# Public Repo Exclusion List

## Purpose

This file lists flagship-paper files that should not remain in a public repo by default because they are submission-sensitive, editor-facing, or contain private contact or upload-packaging material.

## Exclude from a Public Repo

| path | reason |
| --- | --- |
| `paper/flagship/41_full_draft_tse_en.md` | full current manuscript text; submission-sensitive by default |
| `paper/flagship/42_appendix_validation_tse_en.md` | full current appendix / supplement text; submission-sensitive by default |
| `paper/flagship/43_cover_letter_tse_aligned_en.md` | editor-facing cover letter |
| `paper/flagship/44_difference_from_tosem_submission_aligned.md` | editor-facing related-submission disclosure |
| `paper/flagship/submission_metadata_tse.txt` | submission metadata and personal contact details |
| `paper/flagship/49_tse_upload_manifest.md` | upload-only packaging control file |
| `paper/flagship/50_comments_to_editor_tse.txt` | editor-facing portal text |
| `paper/flagship/51_supporting_docs_upload_decision.md` | submission-side disclosure strategy |
| `paper/flagship/submission_package_readme_tse.md` | submission operational note rather than public research content |
| `paper/flagship/39_final_submission_checklist.md` | submission-completion control file |
| `paper/flagship/40_submission_package_index.md` | submission package routing and do-not-upload control |
| `paper/flagship/45_term_and_first_use_map.md` | manuscript submission control for wording and acronym discipline |
| `paper/flagship/46_ieee_page_truth_precheck.md` | submission-precheck packaging note |
| `paper/flagship/47_supplement_reproducibility_cleanup.md` | supplement packaging note for review preparation |
| `paper/flagship/48_tse_upload_gate_report.md` | internal upload gate decision record |
| `paper/flagship/52_english_only_verification_report.md` | submission-side verification record |
| `paper/flagship/tse_upload_package/` | consolidated upload package and trial outputs |
| `paper/flagship/private_repo_bundle/` | private sync bundle intended for a separate private repo |
| `paper/flagship/private_repo_sync_note.local.txt` | local-only operational note |
| `paper/flagship/submission_private_contact_local.txt` | local-only contact file if later created |

## Public-Safe by Default

The following asset groups are safe to keep in the public main repo unless the project owner later chooses a stricter privacy policy:

- `paper/flagship/assets/run_archive/`
- `paper/flagship/assets/run_archive/json/`
- `paper/flagship/assets/same_case_pack/`
- `paper/flagship/assets/specimens/`
- `paper/flagship/prototype/independent_checker/`
- `paper/flagship/14_checker_comparison_note.md`
- `paper/flagship/18_validation_results_table.md`

## Practical Rule

If a file is needed mainly for submission, editor communication, manuscript sync, or private contact handling, keep it out of the public repo and place it in the private repo sync path instead.
