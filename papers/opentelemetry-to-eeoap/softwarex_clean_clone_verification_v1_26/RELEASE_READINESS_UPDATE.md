# Release Readiness Update

## What Version 1.26 Verifies

Version 1.26 verifies that the version 1.25 release-candidate support package
can be recovered from a clean checkout of commit
`a03f6455d87bcf67987c7ba1e4297a224de70976`.

The verification confirms:

- the support package exists;
- requested key files are present;
- SHA-256 checksum verification passes for 34 listed files;
- CodeMeta JSON syntax validation passes;
- repository generated statements pass the EEOAP validator;
- support package copied statements pass the EEOAP validator;
- scoped pytest passes;
- the clean checkout remains clean after verification;
- no private phone number or home address is present in the support package.

## Blocker Reduced

Support package reproducibility is reduced as a blocker. The version 1.25
package is reproducible from a clean checkout.

## Remaining Unresolved Items

- DOI not created.
- GitHub Release not created.
- Tags not pushed.
- Root metadata not overwritten.
- Final release URL missing.
- Final release version missing.
- Final GitHub Issues URL missing.
- Final public references missing.
- CFF YAML validation skipped unless PyYAML or an equivalent YAML parser becomes
  available.
- Official final SoftwareX submission file not yet finalized.

## Readiness Assessment

The version 1.25 support package is ready for the next release planning step:
release-candidate tag preparation planning. It is not ready for tag creation,
tag push, GitHub Release, DOI creation, or formal submission.
