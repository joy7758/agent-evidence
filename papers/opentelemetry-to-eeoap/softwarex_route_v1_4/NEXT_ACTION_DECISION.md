# Next Action Decision

## Decision

proceed to SoftwareX preparation after fixing blockers

## Reason

The current package fits SoftwareX better than JSS or IST because its strongest
asset is runnable, reproducible research software: a local adapter, fixtures,
generated outputs, validator checks, clean-clone evidence, checksums, and local
artifact tags. It is not ready for SoftwareX submission because the release
state, source layout, citation metadata, public artifact identifiers, and
3000-word template adaptation are unresolved.

## Next Single Action

clean and isolate release branch

The next practical step should be to create or verify a clean release branch for
the OpenTelemetry-to-EEOAP package before any public tag push, DOI, GitHub
Release, or SoftwareX template conversion. This prevents unrelated AEP-Media,
`pd-oap`, `tmp`, and manuscript worktree artifacts from leaking into the
SoftwareX release path.

## Do Not Do Yet

- DOI.
- GitHub release.
- Tag push.
- Venue formatting.
- Formal submission.
- LangChain runtime integration.
- OpenTelemetry Collector integration.
