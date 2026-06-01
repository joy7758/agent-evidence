# Mission 036H Zenodo Release Timing Decision Report

Date: 2026-06-02

## 1. Mission Summary

Mission 036H records that AEP-Media should not publish a new Zenodo archive
now. The existing `aep-media-v0.1.0` archive DOI remains the current citable
AEP-Media release DOI.

No implementation code was changed. No validator, schema, adapter, or
evaluation semantics were changed. No GitHub release, Zenodo archive, upload,
or new DOI was created.

## 2. Existing DOI

- Existing DOI: `10.5281/zenodo.20107097`
- Current version: `aep-media-v0.1.0`

## 3. Release Now?

No.

## 4. Reason

Current changes are primarily recruitment, governance, documentation,
discoverability, and review-process materials. They are valuable JOSS waiting
period maintenance artifacts, but they should be bundled into a coherent
maintenance release only after additional public development evidence exists.

## 5. Next Release Target

Recommended next release:

`aep-media-v0.1.1`

Recommended meaning:

documentation, reproducibility, discoverability, and regression-test
maintenance release.

## 6. Trigger Conditions

Publish `aep-media-v0.1.1` only after:

1. Mobile-video walkthrough is merged.
2. Adapter-boundary documentation is merged.
3. Mobile-video fixture regression tests are merged.
4. CI status is documented.
5. At least one meaningful issue, PR, or external reproducibility review is
   recorded.
6. `CHANGELOG.md` is updated.

## 7. Expected Archive Route

Expected route:

GitHub release -> Zenodo archive -> DOI recorded in release metadata.

## 8. Guardrails

- Do not invent a DOI.
- Do not publish without release notes.
- Do not publish from a dirty working tree.
- Do not include old target-route submission packages.
- Do not include excluded workspaces.
- Do not create a release merely to manufacture public activity.

## 9. Validation

- `git diff --check`: PASS.
- Red-line scan: PASS.

Scan result:

- no invented DOI;
- no local absolute path in repository docs;
- no excluded workspace reference;
- no rejected-route history text in Mission 036H files;
- no venue publication promise;
- no positive-review requirement.

## 10. Current JOSS Readiness

- JOSS technical readiness: READY.
- JOSS submission readiness: WAITING FOR PUBLIC HISTORY.
- Earliest honest JOSS submission date: 2026-09-16 or later.

## 11. Next Recommended Action

Continue real public maintenance. After a meaningful issue, PR, or external
reproducibility review is recorded, revisit `aep-media-v0.1.1` release
preparation.
