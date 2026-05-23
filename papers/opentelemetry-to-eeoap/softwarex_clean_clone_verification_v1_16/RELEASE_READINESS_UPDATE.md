# Release Readiness Update

## What Version 1.16 Verifies

Version 1.16 verifies that the version 1.15 release-candidate support package
can be checked out and validated from a clean clone at commit
`05a58457709b79582a218615ddf63952fe17f0b7`.

This reduces the support package reproducibility blocker by showing that:

- the support package exists in a clean checkout;
- all 31 listed package files pass SHA-256 verification;
- the CodeMeta JSON draft parses;
- the scoped adapter pytest passes;
- both repository generated EEOAP statements pass the validator;
- both support package copied EEOAP statements pass the validator;
- verification leaves the clean clone git status clean.

## What Remains Unresolved

- DOI was not created.
- GitHub Release was not created.
- Tags were not pushed.
- Root `CITATION.cff` was not overwritten.
- Root `codemeta.json` was not overwritten.
- Official SoftwareX `.docx` or `.tex` template was not applied.
- Final release URLs are not available.
- Final declarations still need target-venue wording.
- CFF YAML validation remains deferred until a YAML parser is available.

## Blocker Reduced By This Step

Support package reproducibility is reduced from an unresolved blocker to a
verified local clean-checkout result.

This does not convert the package into a public release, DOI archive, GitHub
Release, or formal SoftwareX submission.
