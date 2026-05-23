# DOI And GitHub Release Sequence

## Preferred Sequence

1. Finalize package-local metadata drafts.
2. Create final release-candidate support package.
3. Run checksum, validator, scoped pytest, and clean-clone verification.
4. Create and push the focused release-candidate tag if approved.
5. Create GitHub Release from the verified tag if approved.
6. Create or link Zenodo DOI after the GitHub Release if approved.
7. Update manuscript references, artifact availability, CFF, CodeMeta, and
   SoftwareX metadata table with final public identifiers.

## Why GitHub Release First

GitHub Release can bind the verified tag, release notes, and support package in
one public software distribution surface. Zenodo or another archive can then
mint or link a DOI against a stable public release artifact.

## What Must Be True Before GitHub Release

- Final release scope approved.
- Final release tag name approved.
- Package-local CFF and CodeMeta metadata drafted and checked.
- Final support package created.
- Checksums verified.
- Scoped pytest passes.
- Validator checks pass.
- CodeMeta JSON parses.
- CFF YAML validation passes or documented skip is accepted.
- Clean-clone verification passes.
- Git status clean.

## What Must Be True Before DOI

- GitHub Release or archive source is public and stable.
- Metadata values match the release.
- Support package is attached or reachable.
- License and author metadata are correct.
- References can be updated with the final DOI.

## References To Update After DOI

- EEOAP/OpenTelemetry-to-EEOAP artifact reference.
- SoftwareX metadata table permanent link.
- Artifact availability statement.
- CFF `doi` or equivalent field if used.
- CodeMeta `identifier` / `downloadUrl` / `releaseNotes` fields as applicable.

## Metadata To Update After DOI

- Package-local CFF.
- Package-local CodeMeta JSON.
- Software metadata note.
- Artifact availability statement.
- Manuscript references.
- SoftwareX final template file.

## Rollback Risks

- DOI records are persistent and hard to correct after publication.
- A wrong tag or release URL can create a misleading citation trail.
- Updating root metadata too early can conflict with AEP-Media.

No GitHub Release or DOI is created in this task.
