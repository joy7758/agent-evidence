# Template Conversion Gap Review

## Remaining Gaps

- Official `.docx` or `.tex` SoftwareX template file was not yet used.
- DOI has not been created.
- GitHub Release has not been created.
- Tags have not been pushed.
- Root `CITATION.cff` still describes AEP-Media.
- Root `codemeta.json` still describes AEP-Media.
- Final release-candidate support package is missing.
- Final clean-clone verification is missing for the eventual release package.
- Final checksum verification is missing for the eventual release package.
- Final declarations require venue wording.
- Final references require public release, DOI, or immutable archive references.
- Source layout issue remains disclosed: adapter source is under `tools/`, not
  `repo/src`.

## Template Guidance Verification

The SoftwareX Guide for Authors was freshly checked on 2026-05-23. The page
states that SoftwareX submissions consist of a short descriptive paper and
open-source software distribution, that submissions are accepted only with
journal-specific templates, and that the article has a 3000-word limit excluding
title, authors, affiliations, references, and metadata tables.

Official Word and LaTeX template links were visible on the guide page. This
task did not download or populate those files. The current output is a
Markdown-based template-compatible draft.

## Conclusion

The manuscript content can move into an official template file later, but the
next route action should prepare the release-candidate support package first so
the template has stable artifact and release references.
