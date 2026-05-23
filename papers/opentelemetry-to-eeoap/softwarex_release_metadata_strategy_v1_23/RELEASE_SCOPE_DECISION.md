# Release Scope Decision

## Option A: Entire Repository Release

Description: release the full `agent-evidence` repository state as the
SoftwareX software release.

Advantages:

- Conventional GitHub/Zenodo repository release flow.
- Captures adapter, validator, examples, generated artifacts, and documentation
  in one repository state.
- Easier for reviewers to reproduce from a single checkout.

Risks:

- Root metadata currently describes AEP-Media.
- Repository includes multiple artifact and paper lines.
- A full repository release may make OpenTelemetry-to-EEOAP scope less clear.

Effect on root metadata: likely requires either root metadata update on a
focused branch or strong package-local metadata explanation.

Effect on references: public repository release URL and DOI could be cited, but
the manuscript must clarify the OpenTelemetry-to-EEOAP subpackage scope.

Effect on SoftwareX submission: possible, but only after metadata ambiguity is
resolved.

Recommendation: no as the primary current plan.

## Option B: Focused Release-Candidate Branch State

Description: release the `softwarex-otel-eeoap-release-candidate` branch state
as the SoftwareX software release.

Advantages:

- Aligns with the current isolated worktree and evidence trail.
- Preserves the full repository context needed for tests and validator support.
- Keeps the SoftwareX route auditable through versioned preparation directories.

Risks:

- Root metadata mismatch still needs a clear handling strategy.
- Branch state must stay stable until tag/release.
- Final references must point to public release identifiers, not local paths.

Effect on root metadata: root metadata can remain unchanged for now if
package-local metadata is used and the release notes explain scope; a later
focused branch metadata update remains possible.

Effect on references: cite a focused release tag/GitHub Release once public.

Effect on SoftwareX submission: strongest current option if paired with a final
support package and package-local metadata.

Recommendation: yes as primary provisional release scope.

## Option C: Support Package Archive Only

Description: release only the OpenTelemetry-to-EEOAP support package as a
standalone archive.

Advantages:

- Cleanest focused artifact.
- Avoids root metadata collision.
- Can include exact article draft, metadata, evidence, checksums, and
  validation files.

Risks:

- May not satisfy expectations for open-source software distribution if the
  executable repository context is excluded.
- Tests and validator may be harder to run without the repository.
- Must explain relationship to the repository and branch.

Effect on root metadata: minimal.

Effect on references: support archive can be cited as a supplement, especially
if DOI-backed.

Effect on SoftwareX submission: useful as supplementary archive, not primary
software distribution by itself.

Recommendation: yes as supplementary archive.

## Option D: No Release Before Editorial Feedback

Description: continue with local drafts and defer release until after SoftwareX
editorial feedback.

Advantages:

- Avoids irreversible public metadata mistakes.
- Allows final journal requirements to shape release packaging.

Risks:

- Formal SoftwareX submission likely needs public software availability.
- Manuscript metadata table and references would retain TODO values.
- Reviewers may not be able to access artifacts.

Effect on root metadata: none now.

Effect on references: public artifact references remain unavailable.

Effect on SoftwareX submission: acceptable only for internal drafting, not for
formal submission readiness.

Recommendation: no for final submission; acceptable only as a temporary hold.

## Provisional Release Scope Recommendation

Use Option B as the primary release scope and Option C as a supplementary
archive path. Do not execute any release action in version 1.23.
