# Submission Metadata Checklist

## Anonymous-Review Ready

- Keep the PDF in anonymous review mode with placeholder author, affiliation, and email fields in `main.tex`.
- The CCS block is now populated with a conservative final candidate; recheck the chosen concepts once more before the actual submission upload.
- Recheck the artifact availability wording against the target workflow so the note placement and wording match the submission system expectations.
- Confirm the final review-package file naming convention and the exact contents of the submission zip.
- Do one last bibliography sanity check for the current non-article references so the final review PDF does not carry avoidable style artifacts.
- Keep `printacmref=false` in the review version so the dummy ACM reference block stays out of the anonymous PDF.

## Later Camera-Ready / Post-Acceptance Only

- Replace the anonymous author block with real author, affiliation, and contact metadata.
- Decide whether acknowledgments, funding, or conflict-of-interest text should appear, and place them only in the non-anonymous version.
- Replace placeholder ACM publication metadata with the publisher-provided rights, DOI, volume, issue, article number, month, and year values.
- Revisit the artifact availability note only if the publisher or artifact review workflow requires a different final placement or wording.
- Regenerate the final non-anonymous build and rerun the compile sanity check after all publisher metadata is available.
