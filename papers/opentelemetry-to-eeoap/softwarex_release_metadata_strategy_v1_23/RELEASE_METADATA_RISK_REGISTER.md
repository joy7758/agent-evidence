# Release Metadata Risk Register

| Risk | Severity | Likelihood | Mitigation | Next action |
|---|---|---|---|---|
| Pushing tag too early | high | medium | Require metadata drafts, support package, checksum, validator, pytest, and clean-clone checks before any tag push | Prepare package-local metadata drafts first |
| Creating DOI before metadata is stable | high | medium | Create DOI only after public release artifacts and metadata are final | Defer DOI |
| Root metadata overwriting AEP-Media | high | medium | Keep root metadata unchanged until a focused release branch strategy is approved | Use package-local metadata |
| Support issue URL not final | medium | high | Keep support route as GitHub Issues but leave URL TODO until release route is fixed | Decide public repository/release URL first |
| Release candidate branch diverging from paper references | high | medium | Pin final tag and update references only after validation | Reconcile references after release identifiers exist |
| Article references pointing to non-public local paths | high | high | Replace local paths with public URLs/DOI before formal submission | Plan final references update |
| Private personal data accidentally entering metadata | high | low | Use only author-confirmed public fields and run privacy scans over new metadata directories | Continue privacy checks in v1.24 |
| Source layout issue being misunderstood | medium | medium | Keep narrative that adapter is under `tools/` and broader package under `agent_evidence/`; do not imply `repo/src` layout | Preserve layout disclosure |
| CFF YAML validation still not performed | medium | medium | Validate with PyYAML or equivalent before release; document any skip reason | Add validation requirement to v1.24/v1.25 plan |
