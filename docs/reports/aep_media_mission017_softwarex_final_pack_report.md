# AEP-Media Mission 017 SoftwareX Final Pack Report

Date: 2026-05-10

## 1. What Changed

Mission 017 prepared a SoftwareX-oriented final pack for AEP-Media without changing validator logic, schemas, adapters, demos, or tests.

Changed documentation and packaging files:

- Updated `README.md` with a concise AEP-Media entry point.
- Added `.zenodo.json` draft metadata for an AEP-Media-focused archive.
- Added SoftwareX final manuscript, cover letter, template log, readiness audit, Zenodo release plan, supplementary pack, and generated submission-pack outputs under `docs/paper/softwarex/final/`.

## 2. Repository Readiness Audit Result

Repository readiness: NOT READY.

Positive checks:

- Repository URL identified: `https://github.com/joy7758/agent-evidence`.
- GitHub visibility check: PUBLIC.
- License check: Apache-2.0.
- README now exposes the AEP-Media path.
- Specs, schemas, examples, demos, reports, and tests exist.

Blocking checks:

- Current CLI does not expose AEP-Media commands expected by the tests and documentation.
- AEP-Media-specific DOI/archive is not yet confirmed.

## 3. License Status

License status: PASS.

- `LICENSE` contains Apache License 2.0.
- `pyproject.toml` declares `license = "Apache-2.0"`.
- GitHub license metadata reports Apache-2.0.

## 4. README Status

README status: PASS after Mission 017 update.

Added section:

`AEP-Media: time-aware media evidence validation`

The section includes purpose, install command, media validation command, bundle build/verify commands, strict-time command, evaluation command, adapter-only boundary note, non-claims, and links to specs, schemas, examples, demos, and reports.

## 5. Template Status

Template status: PARTIAL PASS.

- Official SoftwareX Word template downloaded from the SoftwareX / Elsevier official guide path.
- Word template hash: `9fcf40ede96a2f188ee4ef77134e0596d01e1b65fd9db63f2874d29f2ecb916d`.
- LaTeX template download failed in the local environment and is recorded as an optional template-path blocker.
- Final manuscript DOCX was generated using the official Word template as reference.
- A preview PDF and TeX file were generated for local review.

## 6. SoftwareX Manuscript Status

Manuscript status: DRAFT GENERATED.

Generated files:

- `docs/paper/softwarex/final/aep_media_softwarex_final_manuscript.md`
- `docs/paper/softwarex/final/submission-pack/main/AEP-Media_SoftwareX_Manuscript.docx`
- `docs/paper/softwarex/final/submission-pack/main/AEP-Media_SoftwareX_Manuscript.pdf`
- `docs/paper/softwarex/final/submission-pack/main/AEP-Media_SoftwareX_Manuscript.tex`

Word count:

- Markdown manuscript: 1189 words.

## 7. Cover Letter Status

Cover letter status: DRAFT GENERATED.

Generated files:

- `docs/paper/softwarex/final/aep_media_softwarex_cover_letter_final.md`
- local staging DOCX copy generated from the final cover letter.

The cover letter does not mention TSE rejection and frames the work as reusable research software.

## 8. Supplementary Pack Status

Supplementary pack status: GENERATED.

Generated file:

- `docs/paper/softwarex/final/submission-pack/AEP-Media_SoftwareX_Supplementary.zip`

Supplement contents:

- `README_SOFTWAREX_SUPPLEMENT.md`
- `REPRODUCIBILITY.md`
- `CLAIM_BOUNDARY.md`
- `SOFTWARE_INVENTORY.md`
- `EVALUATION_SUMMARY.md`
- `CHECKSUMS.sha256`
- `reports/`
- `schemas/`
- `examples/`
- `specs/`

## 9. DOI / Archive Status

DOI/archive status: BLOCKER.

Observed:

- `CITATION.cff` records repository DOI `10.5281/zenodo.19334062`.
- `.zenodo.json` was added with AEP-Media-focused metadata.

Action required:

- Confirm whether the existing repository DOI corresponds to the exact AEP-Media release.
- If not, create a tagged AEP-Media release and archive it before SoftwareX final submission.
- Do not invent a DOI.

## 10. Test and Evaluation Results

Targeted AEP-Media tests:

- Command: targeted media pytest set.
- Result: `44 passed, 2 failed, 1 warning`.
- Failures:
  - `test_cli_run_media_evaluation`: missing CLI command `run-media-evaluation`.
  - `test_cli_build_aep_media_release_pack`: missing CLI command `build-aep-media-release-pack`.

Full test suite:

- Result: `148 passed, 5 failed, 1 skipped, 15 warnings`.
- Failures are all missing CLI command registrations:
  - `run-media-evaluation`
  - `build-aep-media-high-revision-pack`
  - `build-aep-media-ieee-word-pack`
  - `build-aep-media-release-pack`
  - `build-aep-media-submission-pack`

Internal function evaluation:

- Default evaluation: `PASS aep-media-evaluation@0.1 cases=18 unexpected=0`
- Adapter-inclusive evaluation: `PASS aep-media-evaluation@0.1 cases=26 unexpected=0 adapters=included`
- Optional-tool reporting evaluation: `PASS aep-media-evaluation@0.1 cases=23 unexpected=0 optional_tools=included`
- Combined adapter and optional-tool evaluation: `PASS aep-media-evaluation@0.1 cases=31 unexpected=0 adapters=included optional_tools=included`
- Release pack internal function: `PASS aep-media-release-pack@0.1`

Interpretation:

The underlying AEP-Media functions and evaluation paths are present, but the repository is not SoftwareX-ready until the expected CLI commands are registered or the documentation is changed to use supported entry points.

## 11. Red-line Scan Result

Red-line scan status: PASS for the generated SoftwareX final scope.

Scanned final manuscript, cover letter, supplementary materials, README, CITATION, archive metadata, and final SoftwareX reports for:

- TSE submission-ready language;
- TSE desk-reject language in external-facing SoftwareX files;
- local absolute home path;
- template placeholders;
- unrelated paper-workspace names;
- positive claims of legal admissibility, non-repudiation, trusted timestamping, real PTP proof, real C2PA signature verification, production deployment, or chain of custody.

No red-line hits were found.

## 12. Remaining Blockers

Blocking before SoftwareX submission:

1. Register or otherwise resolve the missing AEP-Media CLI commands expected by tests and README.
2. Confirm or create an AEP-Media-specific archive DOI.
3. Rerun targeted tests and full evaluation after the CLI blocker is fixed.
4. Manually inspect the generated DOCX/PDF and SoftwareX template formatting.

Non-blocking but recommended:

- Consider whether the LaTeX template is needed. The Word template path is currently available.
- Confirm that the SoftwareX submission system accepts the generated DOCX and supplementary zip structure.

## 13. Final Readiness

Final readiness: NOT READY.

Reason:

The SoftwareX manuscript and supplementary pack are generated, the repository is public, and the license is correct. However, tests show missing AEP-Media CLI command registrations, and the AEP-Media-specific DOI/archive is not confirmed.

## 14. Next Recommended Mission

Mission 018 should be a narrowly scoped repository-readiness fix:

- register existing AEP-Media CLI commands without changing validator logic;
- rerun targeted and full tests;
- confirm or create the AEP-Media release archive / DOI;
- regenerate the final SoftwareX pack after tests pass.

## 15. Mission 018 Refresh

Mission 018 resolved the CLI registration blocker identified above.

Updated verification:

- Targeted AEP-Media tests: `48 passed, 1 warning`
- SoftwareX/readiness tests: `23 passed, 1 warning`
- Full pytest: `155 passed, 1 skipped, 15 warnings`
- Default evaluation CLI: `18 cases, unexpected=0`
- Adapter-inclusive evaluation CLI: `26 cases, unexpected=0`
- Optional-tool reporting evaluation CLI: `23 cases, unexpected=0`
- Combined evaluation CLI: `31 cases, unexpected=0`
- Release pack CLI: `PASS aep-media-release-pack@0.1`

Updated readiness: NEAR READY.

Remaining blocker: confirm or create an AEP-Media-specific release archive DOI before final SoftwareX submission.
