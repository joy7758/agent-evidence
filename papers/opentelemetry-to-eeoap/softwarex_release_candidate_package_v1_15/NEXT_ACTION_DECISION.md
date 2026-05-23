# Next Action Decision

## Decision

run clean-clone verification for version 1.15 support package next

## Reason

The version 1.15 support package now collects the current article, metadata
drafts, two-valid-trace evidence, generated statements, adapter reports,
validation commands, and checksums. Before template-file conversion or release
work, the package should be verified from a clean clone to confirm that it is
self-contained and reproducible.

## Next Single Action

Run clean-clone verification for the version 1.15 support package after
committing it.

## Do Not Do Yet

- DOI.
- GitHub Release.
- Tag push.
- Formal submission.
- Root metadata overwrite.
- Source layout rewrite.
- LangChain runtime integration.
- OpenTelemetry Collector integration.
