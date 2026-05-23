# DOI and GitHub Release Strategy

## Option A: GitHub Release First, Then Zenodo DOI

Advantages:

- Clear release artifact and release notes.
- GitHub Release can attach support package files.
- Zenodo integration can mint a DOI from a tagged release.

Risks:

- Requires tag and release metadata to be correct before publication.
- Mistakes become public quickly.
- Root metadata mismatch must be handled clearly before release.

Requirements:

- Final release tag.
- Final support package.
- Clean-clone and checksum verification.
- Final metadata and references.

Effect on references:

- Manuscript can cite GitHub Release URL and Zenodo DOI after creation.

Effect on SoftwareX submission:

- Strong fit if release is stable before submission.

## Option B: Zenodo Archive From GitHub Repository State

Advantages:

- Produces citable DOI.
- Can archive a specific repository state.

Risks:

- If the archived state includes broad repository content, root metadata
  mismatch must be explained or fixed.
- Archive may not isolate the focused package unless carefully packaged.

Requirements:

- Decided repository state.
- Stable metadata.
- Final support package and checksums.

Effect on references:

- DOI becomes the primary immutable artifact reference.

Effect on SoftwareX submission:

- Good fit if SoftwareX accepts the archive/repository structure.

## Option C: No DOI Before Initial Editorial Feedback

Advantages:

- Avoids premature public archive.
- Allows editorial feedback before irreversible release decisions.
- Keeps current route conservative.

Risks:

- SoftwareX submission may require public software distribution at submission.
- Metadata table and artifact availability would still contain TODOs, which may
  be unacceptable for formal submission.

Requirements:

- Explicit pre-submission decision from author/editorial policy.
- Clear manuscript TODO status if used before final submission.

Effect on references:

- Release references remain placeholders.

Effect on SoftwareX submission:

- Suitable for internal draft only, not likely sufficient for formal submission.

## Option D: Institutional or External Archive Later

Advantages:

- May support long-term preservation independent of GitHub.
- Can include curated package artifacts.

Risks:

- Additional administrative overhead.
- May not integrate cleanly with GitHub release workflow.
- Could delay submission.

Requirements:

- Archive platform selection.
- Metadata and license compatibility.
- Final package upload.

Effect on references:

- Adds archive URL/DOI if available.

Effect on SoftwareX submission:

- Potentially strong, but only after archive is complete.

## Provisional Recommendation

Use Option A if the route proceeds to formal submission: create a focused GitHub
Release from a verified tag, then create or link a DOI archive. Do not execute
this until metadata, tag scope, support package, and validation checks are
final.
