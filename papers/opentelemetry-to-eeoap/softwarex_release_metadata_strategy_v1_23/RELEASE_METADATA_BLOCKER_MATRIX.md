# Release Metadata Blocker Matrix

| Blocker | Current status | Category | Required before tag creation? | Required before DOI? | Required before formal submission? | Action required | Owner |
|---|---|---|---:|---:|---:|---|---|
| Release URL | TODO | release | no | yes | yes | Create only after release scope and tag are approved | Codex / manual decision |
| DOI | Not created | release | no | yes | yes, if DOI route selected | Create or link after public release artifact is stable | external platform / manual decision |
| Final release version | TODO | metadata | yes | yes | yes | Decide version before final metadata and tag | manual decision |
| Final release tag | TODO; proposed `opentelemetry-to-eeoap-softwarex-rc-v1.0` | release | yes | yes | yes | Approve tag name after metadata drafts and validation | manual decision |
| Support issue URL | TODO; support route is GitHub Issues | metadata | no | yes | yes | Insert final issue tracker URL after release route is fixed | Codex / manual decision |
| Root metadata mismatch | Root metadata describes AEP-Media | metadata | no, if package-local metadata route is used | possibly | yes | Keep unchanged for now; decide later whether focused branch root metadata is needed | manual decision |
| Package-local metadata drafts | Existing v1.8 drafts are not final | metadata | yes | yes | yes | Create v1.24 package-local release metadata drafts | Codex |
| Final references | Public release identifiers missing | references | no | yes | yes | Update after release URL/DOI exist | Codex |
| Final SoftwareX metadata table | Release/version/permanent-link fields TODO | template | no | yes | yes | Update after public identifiers exist | Codex |
| GitHub Release | Not created | release | no | yes | yes, if selected route | Create after final checks and tag approval | external platform / manual decision |
| Zenodo DOI | Not created | release | no | yes | yes, if DOI route selected | Mint/link after GitHub Release or archive is stable | external platform / manual decision |
| Clean-clone verification after metadata changes | Not run for final metadata state | validation | yes | yes | yes | Run after final metadata/support package changes | Codex |
| Checksum verification after metadata changes | Not run for final metadata state | validation | yes | yes | yes | Regenerate and verify package checksums | Codex |
