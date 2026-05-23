# Next Action Decision

## Decision

Prepare package-local release metadata drafts next.

## Reason

Declarations and author metadata are now confirmed, but final release URL, DOI,
release version, release tag, support issue URL, package-local CFF/CodeMeta
metadata, and final references remain unresolved. Root metadata still describes
AEP-Media and should not be overwritten before release scope is executed.
Package-local metadata drafts are the safest next step because they can prepare
the release surface without pushing tags, creating DOI, creating GitHub Release,
or changing root metadata.

## Next Single Action

Create version 1.24 package-local release metadata drafts using confirmed author
metadata and provisional release/tag naming, without modifying root metadata or
creating public release artifacts.

## Do Not Do Yet

- DOI, Digital Object Identifier
- GitHub Release
- Tag push
- Formal submission
- Root metadata overwrite
- Source layout rewrite
- LangChain runtime integration
- OpenTelemetry Collector integration
