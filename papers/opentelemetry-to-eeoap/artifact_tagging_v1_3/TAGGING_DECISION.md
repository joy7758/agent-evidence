# Tagging Decision

## EEOAP Target Analysis

The most appropriate EEOAP target is commit
`96f444b7ed39b39fe9f47e428af835952e843cb0`.

Reasoning:

- The repository already had the local annotated tag `eeoap-v0.1-paper` pointing
  to this commit.
- The tag message describes a scoped EEOAP reproducible artifact, including the
  paper-case demo, targeted EEOAP tests, and tampered-output detection.
- This commit is on the EEOAP paper/release line and predates the
  OpenTelemetry-to-EEOAP adapter branch.
- It is a better target than current `HEAD` because current `HEAD` includes
  later OpenTelemetry paper/review materials, while this tag target represents
  the EEOAP artifact used as the validation foundation.

Final decision: create local annotated tag `eeoap-v0.1-artifact` at
`96f444b7ed39b39fe9f47e428af835952e843cb0`.

## AEP Target Analysis

The most appropriate AEP target is commit
`af2b90c14587718a8ed6982131ba9c98e3274054`.

Reasoning:

- The v0.9 citation verification treated `[AEP-Artifact]` as partially verified
  because it lacked an exact artifact identifier.
- The repository already had the lightweight tag `v0.1-live-chain-security`
  pointing to this commit.
- The commit contains the AEP live-chain specimen line, including:
  - `agent_evidence/aep/` core Agent Evidence Profile primitives.
  - `agent_evidence/aep/schema_v0.1.json`.
  - `tests/fixtures/agent_evidence_profile/` valid and invalid evidence bundles.
  - `release/v0.1-live-chain/` release notes, boundary statement, and
    reproducibility guidance.
- The existing `aep-media-v0.1.0` tag was inspected but not used as the AEP
  artifact target because it represents the later AEP-Media SoftwareX package,
  not the broader AEP live-chain artifact cited for runtime evidence bundle and
  integrity-verifiable packaging context.

Final decision: create local annotated tag `aep-v0.1-artifact` at
`af2b90c14587718a8ed6982131ba9c98e3274054`.

## Final Tag Decision

Both proposed local annotated tags were created:

- `eeoap-v0.1-artifact`
- `aep-v0.1-artifact`

No existing tag was overwritten or force-updated.

## Ambiguity

EEOAP target ambiguity: none. The existing `eeoap-v0.1-paper` tag already
identified the scoped EEOAP reproducible artifact commit.

AEP target ambiguity: reduced but not eliminated for final publication. The
local target is now clear for this repository, but external submission will
still require a final citation decision: cite this local immutable tag, publish
or push the tag, archive the artifact, or create a DOI as required by the target
venue.

## Blocker Status

This step satisfies the local immutable tag blocker for both EEOAP and AEP. It
does not satisfy public artifact availability, DOI creation, GitHub Release
publication, venue formatting, or formal submission requirements.
