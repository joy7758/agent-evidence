# Next Action Decision

## Decision

Proceed to release-candidate tag preparation plan.

## Reason

Clean-clone verification passed for the version 1.25 support package, including
package existence, checksum verification, CodeMeta JSON validation, validator
checks, scoped pytest, privacy check, and clean final git status. The remaining
release blockers are public-release actions and final metadata/reference fields,
not support-package reproducibility.

## Next Single Action

Create version 1.27 release-candidate tag preparation plan for
`opentelemetry-to-eeoap-softwarex-rc-v1.0`, without creating or pushing the tag
yet.

## Do Not Do Yet

- DOI, Digital Object Identifier
- GitHub Release
- Tag push
- Formal submission
- Root metadata overwrite
- Source layout rewrite
- LangChain runtime integration
- OpenTelemetry Collector integration
