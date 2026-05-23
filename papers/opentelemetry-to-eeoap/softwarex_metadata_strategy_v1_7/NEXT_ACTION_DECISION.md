# Next Action Decision

## Decision

create OpenTelemetry-to-EEOAP-specific metadata draft files next

## Reason

Root metadata currently describes AEP-Media, not OpenTelemetry-to-EEOAP. Editing
root `CITATION.cff` or `codemeta.json` now would risk confusing the AEP-Media
release line and the OpenTelemetry-to-EEOAP SoftwareX route. The safest next
step is to create local, OpenTelemetry-to-EEOAP-specific metadata drafts under
`papers/opentelemetry-to-eeoap/` while preserving root metadata unchanged.

## Next Single Action

Create OpenTelemetry-to-EEOAP-specific metadata draft files under
`papers/opentelemetry-to-eeoap/`, without touching root metadata.

## Do Not Do Yet

- Root metadata overwrite.
- Code refactor.
- Source layout rewrite.
- DOI.
- GitHub Release.
- Tag push.
- Formal submission.
- LangChain runtime integration.
- OpenTelemetry Collector integration.
