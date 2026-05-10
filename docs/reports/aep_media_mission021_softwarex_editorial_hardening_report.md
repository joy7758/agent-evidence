# Mission 021: SoftwareX Manuscript Editorial Hardening

## 1. What Changed

Mission 021 performed a manuscript-only editorial hardening pass for the
AEP-Media SoftwareX package. No implementation code, validators, schemas,
adapters, tests, demos, or evaluation semantics were changed.

The main manuscript was revised to read as a SoftwareX-style software paper:

- shortened and refocused the abstract;
- added a complete Software Availability block with GitHub release, Zenodo DOI,
  and Zenodo record;
- preserved the SoftwareX code metadata table;
- strengthened the statement of need against PROV, C2PA, FFmpeg/ffprobe,
  LinuxPTP, GStreamer, JSON Schema, artifact review, in-toto, SLSA, and digital
  object references;
- added Table 1 for components, locations, functions, and commands;
- replaced prior-report language with AEP-Media v0.1.0 final validation
  results;
- explicitly cited `AEP-Media_SoftwareX_Supplementary.zip` in the manuscript;
- strengthened impact around concrete user groups and reuse paths;
- preserved full limitations and non-claims;
- hardened references from skeletal placeholders to 15 cited references;
- regenerated the DOCX and PDF manuscript outputs.

Post-review cleanup also shortened the DONA reference URL to prevent an orphan
PDF reference line and removed internal red-line scan reports from the
reviewer-facing supplementary package.

## 2. Word Count

- Before hardening: 1643 words.
- After hardening: 1926 words.
- Target: under 3000 words.

## 3. References

- Reference count: 15.
- Body citations cover all references: yes.
- Missing references for body citations: none.
- Uncited references: none.

Final reference style should still receive a final human check in the SoftwareX
portal proofing process, but the current list no longer reads as a placeholder
list.

## 4. Supplementary Citation

The manuscript explicitly cites:

`AEP-Media_SoftwareX_Supplementary.zip`

The supplementary package was refreshed to include release/DOI information,
v0.1.0 validation results, reproducibility notes, claim boundary, inventory,
selected schemas, examples, reports, and checksums.

## 5. Declarations

Present in the manuscript:

- CRediT author statement;
- declaration of competing interest;
- funding statement;
- data and software availability statement;
- AI-assisted writing disclosure.

## 6. Software Availability

The Software Availability block now includes:

- repository URL;
- GitHub release URL;
- Zenodo DOI `10.5281/zenodo.20107097`;
- Zenodo record URL;
- Apache-2.0 license;
- Python package and command-line surface;
- documentation, tests, and main commands.

## 7. v0.1.0 Validation Numbers

The manuscript records the AEP-Media v0.1.0 final validation results:

- targeted AEP-Media tests: 48 passed, 1 warning;
- SoftwareX/readiness tests: 23 passed, 1 warning;
- full test suite: 155 passed, 1 skipped, 15 warnings;
- default evaluation: 18 cases, `unexpected=0`;
- adapter-inclusive evaluation: 26 cases, `unexpected=0`;
- optional-tool reporting evaluation: 23 cases, `unexpected=0`;
- combined adapter and optional-tool evaluation: 31 cases, `unexpected=0`;
- release pack: `PASS aep-media-release-pack@0.1`.

## 8. Regenerated Outputs

Regenerated:

- `docs/paper/softwarex/final/submission-pack/main/AEP-Media_SoftwareX_Manuscript.docx`
- `docs/paper/softwarex/final/submission-pack/main/AEP-Media_SoftwareX_Manuscript.pdf`
- `docs/paper/softwarex/final/submission-pack/AEP-Media_SoftwareX_Supplementary.zip`
- local upload convenience zip: `AEP-Media-SoftwareX-Submission-Ready.zip`

The generic manuscript `.tex` file was removed from the submission-pack main
directory and is not recommended for upload.

## 9. Red-Line Scan

Hard red-line scan result: pass.

No hits for local absolute paths, prior-venue status language, template
placeholders, or unrelated paper workspace markers.

Claim-boundary terms appear only as limitations or non-claims.

## 10. Lightweight Verification

- `git diff --check`: passed.
- `pytest tests/test_media_cli_registration.py tests/test_media_evaluation.py -q`:
  8 passed, 1 warning.
- DOCX structure check: valid zip/XML, two tables, no red-line terms.
- PDF preview check: 8 pages, Letter size, unencrypted, no red-line terms.
- Citation closure check: passed.

## 11. Remaining Risks

- A final human visual check in Word or the SoftwareX portal is still necessary.
- The PDF preview is generated locally from Markdown/Pandoc and is secondary to
  the SoftwareX DOCX upload path.
- Reference formatting may be adjusted by the journal production workflow, but
  all references are now cited and substantially complete.

## 12. Final Recommendation

READY FOR SOFTWAREX PORTAL UPLOAD.

Upload the SoftwareX DOCX manuscript, PDF preview if requested, supplementary
zip, and cover-letter text/file. Do not upload a generic TeX source file.
