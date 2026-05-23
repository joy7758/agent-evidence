# SoftwareX Release-Candidate Support Package v1.15

## Purpose

This directory is the local release-candidate support package for the
OpenTelemetry-to-EEOAP SoftwareX route. It supersedes the historical version 0.5
frozen package as the forward support package for final submission preparation.

## Relationship to Version 0.5 Frozen Package

The version 0.5 frozen package under
`papers/opentelemetry-to-eeoap/frozen_v0_5/` remains a historical internal
freeze. It predates the version 0.7 second valid trace and should not be used
as the complete final SoftwareX support package.

This version 1.15 package includes the current two-valid-trace evidence story,
the version 1.14 SoftwareX template-style article draft, local metadata drafts,
generated EEOAP statements, adapter reports, validation results, checksum
material, and a clean-clone verification plan.

## Contents

- `ARTICLE/`: SoftwareX-compatible Markdown article draft copied from version
  1.14 plus article status.
- `METADATA/`: local OpenTelemetry-to-EEOAP metadata drafts copied from version
  1.8 plus metadata status.
- `EVIDENCE/`: valid and invalid trace fixtures plus generated statements and
  adapter reports.
- `VALIDATION/`: validation summary and reproducibility commands.
- `MANIFEST.md`: package file inventory.
- `RELEASE_CANDIDATE_STATUS.md`: release status and boundaries.
- `RELEASE_BLOCKERS.md`: blockers before formal release/submission.
- `CLEAN_CLONE_VERIFICATION_PLAN.md`: clean-clone plan for this support package.
- `CHECKSUMS.sha256`: SHA-256 checksums for package files.

## Not Included

- DOI.
- GitHub Release.
- Pushed tags.
- Official SoftwareX `.docx` or `.tex` template file.
- Runtime code changes.
- Test changes.
- Fixture changes outside this copied support package.
- Generated output changes outside this copied support package.

## Current Release Status

Local release-candidate support package only. This is not a public release, not
a DOI archive, not a GitHub Release, and not a formal SoftwareX submission.

## Next Action Placeholder

Run clean-clone verification for the version 1.15 support package after this
package is committed.
