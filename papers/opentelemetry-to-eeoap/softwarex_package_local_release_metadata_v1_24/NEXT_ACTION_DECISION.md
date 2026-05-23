# Next Action Decision

## Decision

Validate metadata drafts and prepare updated support package next.

## Reason

Version 1.24 creates package-local CFF, CodeMeta, human-readable metadata,
artifact availability, data availability, support contact, and reference drafts
without changing root metadata or creating public release artifacts. These
drafts now need to be incorporated into a new release-candidate support package
so the package can be checksummed, validated, and clean-clone checked as a
coherent submission support artifact.

## Next Single Action

Create version 1.25 updated release-candidate support package that incorporates
the version 1.24 package-local metadata drafts, then regenerate checksums and
run validation.

## Do Not Do Yet

- DOI, Digital Object Identifier
- GitHub Release
- Tag push
- Formal submission
- Root metadata overwrite
- Source layout rewrite
- LangChain runtime integration
- OpenTelemetry Collector integration
