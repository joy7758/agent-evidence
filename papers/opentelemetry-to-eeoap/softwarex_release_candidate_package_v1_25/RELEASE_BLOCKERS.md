# Release Blockers

| Blocker | Current status | Severity | Required before formal submission? | Action required |
|---|---|---|---:|---|
| DOI not created | No DOI exists for OpenTelemetry-to-EEOAP | blocker | yes, if DOI route selected | Create only after package and public release metadata are stable |
| GitHub Release not created | No GitHub Release exists | blocker | yes, if GitHub Release route selected | Create only after package checks and tag approval |
| Tags not pushed | Local tags exist; OpenTelemetry-to-EEOAP release tag not created or pushed | blocker | yes | Push only after metadata, checksum, validator, pytest, and clean-clone checks pass |
| Final release URL missing | TODO | blocker | yes | Fill after public release exists |
| Final release version missing | TODO | blocker | yes | Assign after release scope is approved |
| Final GitHub Issues URL missing | GitHub Issues selected; final URL TODO | important | yes | Fill after public repository/release URL is finalized |
| Root metadata mismatch intentionally unresolved | Root `CITATION.cff` and `codemeta.json` describe AEP-Media | important | yes | Continue package-local metadata unless focused release branch metadata update is approved |
| Final public metadata pending | v1.24 drafts are local support metadata | blocker | yes | Finalize after release URL, tag, GitHub Release, and DOI decisions |
| Final references need public URLs / DOI / archives | Placeholders remain | blocker | yes | Update after public identifiers exist |
| Official final SoftwareX submission file not finalized | Draft template files exist; final submission file not complete | blocker | yes | Finalize after metadata and references are stable |
| Final clean-clone verification for v1.25 package not executed | Planned next | blocker | yes | Run clean-clone verification after commit |
| Final checksum verification after later metadata changes | Current checksum covers v1.25 only | important | yes | Regenerate after any later metadata edits |
| Source layout does not use `repo/src` | Disclosed current layout remains | important | yes | Keep disclosed unless source layout rewrite is explicitly approved |
| CFF YAML validation skipped unless PyYAML becomes available | PyYAML unavailable in prior checks | important | yes | Validate when PyYAML or equivalent parser is available, or document accepted skip |
