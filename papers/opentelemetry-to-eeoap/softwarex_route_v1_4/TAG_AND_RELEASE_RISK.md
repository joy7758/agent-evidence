# Tag and Release Risk

## EEOAP Local Tag Status

- Tag: `eeoap-v0.1-artifact`
- Tag object: `f4270a575517f987dcd45d8ef80a7d30d808f39f`
- Target commit: `96f444b7ed39b39fe9f47e428af835952e843cb0`
- Status: local annotated tag created in v1.3.
- Pushed: no.

## AEP Local Tag Status

- Tag: `aep-v0.1-artifact`
- Tag object: `a58aa33501252b26acde085fed3dfa0104e255a0`
- Target commit: `af2b90c14587718a8ed6982131ba9c98e3274054`
- Status: local annotated tag created in v1.3.
- Pushed: no.

## Why Local Tags Are Not Enough for Final SoftwareX Submission

Local tags improve internal citation stability, but they are not public
artifact identifiers. A SoftwareX submission needs an inspectable software
distribution and durable retrieval path. Local tags cannot be resolved by
reviewers unless they are pushed, archived, or replaced by public release/DOI
links.

## Required Before Final Submission

- Decide whether to push tags.
- Create a public release or archive if the SoftwareX route is selected.
- Update references to use the final public identifiers.
- Verify repository cleanliness before any release candidate is cut.
- Preserve checksum and clean-clone evidence in the final support package.
- Re-run scoped adapter tests after the release candidate is isolated.

## Release Risks

- Current branch has many unrelated dirty/untracked worktree items.
- Existing root `CITATION.cff` and `codemeta.json` describe AEP-Media, not this
  package.
- No OpenTelemetry-to-EEOAP public release tag exists yet.
- A release from the current dirty workspace could accidentally include
  unrelated AEP-Media, `pd-oap`, `tmp`, or manuscript artifacts.
