# Mission 022: SoftwareX Final Upload Authority Freeze

## 1. Mission Summary

Mission 022 froze the authoritative AEP-Media SoftwareX upload package. The
work was limited to manuscript metadata, upload packaging, supplementary-file
hygiene, citation metadata parity, and final upload instructions. No
implementation code, validators, schemas, adapters, tests, or evaluation
semantics were changed.

Final status: READY FOR SOFTWAREX PORTAL UPLOAD.

## 2. Authoritative Source Selected

Authoritative manuscript source:

`docs/paper/softwarex/final/aep_media_softwarex_final_manuscript.md`

The source is the hardened SoftwareX manuscript with 15 references, explicit
Software Availability, release DOI, Supplementary file S1 citation, v0.1.0
validation numbers, declarations, and claim boundaries.

## 3. Duplicate / Stale Manuscript Files

Repository search found one authoritative generated main-manuscript pair:

- `docs/paper/softwarex/final/submission-pack/main/AEP-Media_SoftwareX_Manuscript.docx`
- `docs/paper/softwarex/final/submission-pack/main/AEP-Media_SoftwareX_Manuscript.pdf`

No `.tex` upload source remains in the submission-pack main directory. Old
TSE/IEEE and unrelated untracked paper files remain outside the SoftwareX
upload package and are not for upload.

## 4. Title Page / Front Matter

The manuscript front matter now records:

- Bin Zhang
- Independent Researcher, China
- ORCID: 0009-0002-8861-1481
- Email: joy7759@gmail.com
- Corresponding author: Bin Zhang (joy7759@gmail.com)

No institutional affiliation or postal address was invented.

## 5. Supplementary File S1

The manuscript now cites:

`Supplementary file S1 (AEP-Media_SoftwareX_Supplementary.zip)`

The supplementary package README also identifies the package as Supplementary
file S1 for the SoftwareX submission.

## 6. Software Availability

The Software Availability section includes:

- repository URL;
- GitHub release URL;
- Zenodo DOI and record URL;
- Apache-2.0 license;
- installation command: `python -m pip install -e .`;
- main validation and release commands;
- adapter ingestion commands: `ingest-linuxptp-trace`, `ingest-ffmpeg-prft`,
  and `ingest-c2pa-manifest`.

## 7. Metadata Parity

Metadata parity audit: PASS.

The following files were checked and aligned where appropriate:

- `CITATION.cff`
- `.zenodo.json`
- `codemeta.json`
- `README.md`
- `docs/how-to-cite.md`
- `docs/paper/softwarex/final/release/notes/aep-media-v0.1.0-release-notes.md`
- `docs/paper/softwarex/final/aep_media_softwarex_final_manuscript.md`
- `docs/paper/softwarex/final/submission-pack/metadata/softwarex_submission_metadata.md`

The canonical version, DOI, repository URL, GitHub release URL, Zenodo record
URL, license, author identity, ORCID, and email are consistent across the
SoftwareX-facing files.

## 8. DOCX / PDF Regeneration

Regenerated:

- `docs/paper/softwarex/final/submission-pack/main/AEP-Media_SoftwareX_Manuscript.docx`
- `docs/paper/softwarex/final/submission-pack/main/AEP-Media_SoftwareX_Manuscript.pdf`

Checks:

- DOCX zip/XML structure: valid.
- PDF: 8 pages, Letter size, unencrypted.
- Required strings are present across Markdown, DOCX XML, and PDF text.
- DOCX remains the primary upload file; PDF is a preview file.

## 9. Supplementary ZIP

Regenerated:

`docs/paper/softwarex/final/submission-pack/AEP-Media_SoftwareX_Supplementary.zip`

Checks:

- ZIP integrity: passed.
- Supplementary archive contains 22 files.
- Internal red-line and release-process reports were removed.
- Remaining contents are reviewer-facing: README, reproducibility notes, claim
  boundary, software inventory, evaluation summary, selected specs, selected
  schemas, examples, checksums, validation report, reproducibility checklist,
  non-claims matrix, and DOI confirmation.

## 10. Red-Line Scan

Red-line scan result: PASS.

No hits were found for prior-venue status language, template placeholders,
mounted-data paths, local home paths in repository-facing upload files, or
unrelated workspace markers.

Claim-boundary terms appear only as explicit limitations or non-claims.

## 11. Final Local Upload Folder

Created local final upload folder:

`<local-home>/Downloads/AEP-Media-SoftwareX-Upload-Final/`

Created local convenience archive:

`<local-home>/Downloads/AEP-Media-SoftwareX-Upload-Final.zip`

The local upload archive contains only the final DOCX, PDF preview,
Supplementary file S1, cover letter, upload manifest, metadata parity audit,
red-line report, and final readiness report.

## 12. Final Files to Upload

Upload:

1. `main/AEP-Media_SoftwareX_Manuscript.docx`
2. `main/AEP-Media_SoftwareX_Manuscript.pdf`, only if requested or allowed
3. `supplementary/AEP-Media_SoftwareX_Supplementary.zip`
4. `cover-letter/AEP-Media_SoftwareX_Cover_Letter.md`, or paste the text into
   the portal

## 13. Do-Not-Upload List

Do not upload:

- TeX source files;
- local all-in-one convenience zips as manuscript or supplementary material;
- release-candidate archives;
- old TSE/IEEE files;
- local archive-only packs;
- unrelated paper/NCS evidence workspaces.

## 14. Current Readiness

READY FOR SOFTWAREX PORTAL UPLOAD.

Remaining risk: a human visual check in the SoftwareX portal or Word is still
needed before pressing submit, because the PDF preview is generated locally and
the DOCX is the authoritative upload file.
