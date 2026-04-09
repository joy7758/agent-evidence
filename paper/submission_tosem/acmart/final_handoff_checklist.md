# Final Handoff Checklist

## Must-Have Before Anonymous Upload

- [x] Manuscript source files are present in `acmart/` and included by `main.tex`.
- [x] Core figures are present under `acmart/figures/`.
- [x] Core tables are present under `acmart/tables/`.
- [x] Bibliography file `references.bib` is present.
- [x] Anonymous author metadata is enabled in `main.tex`.
- [x] CCS concepts are present in the current review scaffold.
- [x] User-defined keywords are present and aligned with the paper scope.
- [x] Artifact availability note is present.
- [x] Local compile succeeds with `pdflatex + bibtex + pdflatex + pdflatex`.
- [x] Final anonymous submission zip contents have been checked once against `submission_zip_plan.md`.

## Good-to-Have Polish

- [ ] Recheck the conservative CCS choices once more before upload.
- [ ] Do one final bibliography style sanity pass for the few non-article references that still trigger warnings.
- [ ] Reopen the PDF and visually confirm `Table 2` and `Fig. 7` one last time.
- [ ] Confirm the final artifact availability wording matches the target submission workflow.

## Post-Acceptance Only

- [ ] Replace anonymous author, affiliation, and email metadata with final identity metadata.
- [ ] Add acknowledgments or funding text only in the non-anonymous version, if needed.
- [ ] Replace placeholder ACM publication metadata with publisher-provided values.
- [ ] Regenerate the non-anonymous build after publication metadata is available.
