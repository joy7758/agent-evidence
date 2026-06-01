# Zenodo Release Timing Decision for AEP-Media

Date: 2026-06-02

## Decision

Do not create a new Zenodo archive now.

AEP-Media already has an archived v0.1.0 release:

- Current version: `aep-media-v0.1.0`
- Existing AEP-Media DOI: `10.5281/zenodo.20107097`
- Current JOSS technical readiness: READY
- Current JOSS submission readiness: WAITING FOR PUBLIC HISTORY
- Earliest honest JOSS submission date: 2026-09-16 or later

## Rationale

Recent changes improved governance, documentation, agent-readable discovery,
and external reviewer recruitment materials. These are useful maintenance
signals, but they are not yet a coherent software maintenance release by
themselves.

Creating another archive now would risk making the release stream look too
fine-grained. The next archive should correspond to a clear maintenance release
with public development evidence, reproducibility improvements, and release
notes.

## Recommended Next Release

Recommended next release target:

`aep-media-v0.1.1`

Proposed release meaning:

documentation, reproducibility, discoverability, and regression-test
maintenance release.

## Trigger Conditions

Do not publish `aep-media-v0.1.1` until these conditions are satisfied:

1. Mobile-video walkthrough is merged.
2. Adapter-boundary documentation is merged.
3. Mobile-video fixture regression tests are merged.
4. CI status is documented.
5. At least one meaningful issue, PR, or external reproducibility review is
   recorded.
6. `CHANGELOG.md` is updated.

## Expected Archive Route

When the trigger conditions are met:

1. Prepare clean release notes.
2. Confirm the working tree is clean or only contains intended release files.
3. Create a GitHub release for `aep-media-v0.1.1`.
4. Let Zenodo archive the GitHub release through the repository integration.
5. Record the issued DOI in citation and release metadata.

## Guardrails

- Do not invent a DOI.
- Do not publish without release notes.
- Do not publish from a dirty working tree.
- Do not include old target-route submission packages.
- Do not include excluded workspaces.
- Do not use a release archive to manufacture public activity.
- Do not claim JOSS submission readiness until the public-history gate is
  satisfied.

## Current Action

Record this timing decision only. No GitHub release, tag, archive, upload, or
new DOI is created in this mission.
