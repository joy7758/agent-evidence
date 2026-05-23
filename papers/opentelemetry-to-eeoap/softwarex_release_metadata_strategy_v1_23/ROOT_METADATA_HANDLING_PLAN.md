# Root Metadata Handling Plan

## Current Root `CITATION.cff` Scope

The root `CITATION.cff` describes AEP-Media, including its AEP-Media title,
release version, DOI, release URL, and keywords.

## Current Root `codemeta.json` Scope

The root `codemeta.json` describes AEP-Media as a software source code package,
including AEP-Media release identifiers, Zenodo DOI, GitHub Release URL, and
requirements.

## Why Blind Overwrite Is Risky

The repository contains multiple artifact and paper lines. Blindly overwriting
root metadata with OpenTelemetry-to-EEOAP metadata could corrupt the AEP-Media
citation surface, confuse release consumers, and create inconsistent public
metadata if the full repository remains multi-purpose.

## Strategy Options

### Option A: Leave Root Metadata Unchanged And Use Package-Local Metadata

Advantages:

- Safest for the current multi-line repository.
- Avoids damaging AEP-Media release metadata.
- Matches the current local metadata strategy.

Risks:

- Some repository-level archive tooling may not discover package-local metadata.
- Manuscript must explain metadata scope clearly.

### Option B: Update Root Metadata Only On Focused Release Branch

Advantages:

- Gives a focused release branch conventional root metadata.
- Could support GitHub/Zenodo release automation.

Risks:

- Must not be merged back in a way that overwrites AEP-Media metadata
  unintentionally.
- Requires branch/release discipline.

### Option C: Convert Root Metadata To Repository-Level Umbrella Metadata

Advantages:

- Represents the whole `agent-evidence` repository.
- Could reduce per-package conflict in the long run.

Risks:

- Larger metadata design task.
- May delay SoftwareX submission.
- Could weaken package-specific citation clarity.

### Option D: Add OpenTelemetry-to-EEOAP Metadata Under Package Path Only

Advantages:

- Clear package-local scope.
- Works well with a support package archive.
- Avoids root metadata churn.

Risks:

- Needs strong documentation so reviewers can find it.
- DOI/archive workflow must include the package-local files explicitly.

## Recommendation

Use a hybrid of Option A and Option D now: leave root metadata unchanged and
prepare OpenTelemetry-to-EEOAP metadata under the package/paper path. Consider
Option B only if a focused release branch is explicitly approved for public
release.

## When Root Metadata May Be Changed Later

Root metadata may be changed only after:

1. Release scope is formally approved.
2. It is clear whether the public release is full-repository, focused branch, or
   package archive.
3. AEP-Media metadata preservation risk is resolved.
4. CFF and CodeMeta drafts are validated.
5. The change is isolated to an approved release metadata task.

## Verification Before Any Root Metadata Change

- Compare root metadata before and after.
- Validate CFF syntax.
- Validate CodeMeta JSON.
- Confirm manuscript metadata table and references match the chosen release
  scope.
- Run scoped pytest and clean-clone verification after metadata changes.
