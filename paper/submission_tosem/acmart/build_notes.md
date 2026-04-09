# Build Notes

## Compile Blockers

- The scaffold has already been sanity-compiled locally with `pdflatex + bibtex + pdflatex + pdflatex`.
- No hard scaffold-level LaTeX blocker is currently known if the local toolchain includes `acmart.cls`, `pdflatex`, and `bibtex`.
- The three core figures are now integrated as real PNG assets under `acmart/figures/`.
- Table~1 through Table~4 are now integrated as real LaTeX assets under `acmart/tables/`.
- Figure-description warnings have been cleared by adding explicit `\Description{...}` text to the integrated figures.
- The anonymous review front matter is now explicit. The remaining `printacmref=false` class warning is intentional for the current anonymous review PDF.
- The CCS block is now populated with a conservative final candidate for the anonymous review package.
- The remaining compile-time warnings are limited to minor prose-driven overfull boxes and non-final bibliography metadata for some non-article references.

## Polish Blockers

- Do a final citation-style sanity check after the first BibTeX compile, especially for editors-only or non-article references.
- Tune labels, cross-references, float placement, and figure scaling after figures and tables are all real.
- Recheck Fig.~7 for final submission readability; it is structurally correct, but still the most likely figure to benefit from manual layout refinement.
- Decide whether Fig.~7 should stay as a wide one-column figure or receive one more readability-focused layout pass before final submission.
- Recheck Table~2 first if table polish time is limited; it remains the most width-sensitive table in the current scaffold even after blinding.
- Recheck Table~1 for final readability if page pressure increases; it is the densest table in the current scaffold.
- Recheck Table~3 after final copyediting because error-code tokens are naturally width-sensitive.
- Recheck Table~4 if page pressure changes; it compiles cleanly enough for the scaffold, but long explanatory text still makes it mildly width-sensitive.

## Submission Metadata Blockers

- Replace anonymous author metadata with final author, affiliation, and contact metadata.
- Recheck the final ACM CCS concept choices once more before upload.
- Confirm the final artifact-availability-note placement expected by the target workflow.
- Confirm rights, DOI, and ACM front-matter metadata once the submission system is in use.

## First Recommended Next Step

After the current blind-package refresh, the next most useful step is a final human PDF check and upload using the assembled anonymous review bundle.
