# Tag Readiness Decision

## Decision

Ready to create local tag next.

## Reason

The version 1.25 support package exists, includes package-local metadata drafts,
and has checksum, CodeMeta JSON, validator, scoped pytest, and privacy evidence.
Version 1.26 clean-clone verification confirmed that the support package is
reproducible from a clean checkout and that the clean checkout remained clean.

The proposed tag does not already exist locally. The remaining blockers are
public release actions and final public identifiers, so they block tag push,
GitHub Release, DOI, and formal submission, but they do not block creating a
local annotated RC tag if the target commit is selected and checked.

## Next Single Action

Create local annotated release-candidate tag
`opentelemetry-to-eeoap-softwarex-rc-v1.0` pointing to the selected post-v1.27
commit, without pushing it.

## Do Not Do Yet

- DOI, Digital Object Identifier
- GitHub Release
- Tag push
- Formal submission
- Root metadata overwrite
- Source layout rewrite
- LangChain runtime integration
- OpenTelemetry Collector integration
