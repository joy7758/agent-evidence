# Template Conversion Readiness Decision

## Decision

create release-candidate support package first

## Reason

The version 1.14 Markdown draft is now organized in a SoftwareX-compatible
structure, but official `.docx` or `.tex` template file work should wait until
the support package is stable. The current draft still contains release TODOs:
public release URL, DOI/archive decision, GitHub Release decision, pushed tag
decision, final metadata, final checksums, final clean-clone verification, and
final support package.

Creating the support package first will prevent the official template file from
being filled with unstable artifact references.

## Next Single Action

Create a release-candidate support package that supersedes the historical
version 0.5 frozen package and includes version 0.7 second trace evidence,
version 1.14 article draft, metadata drafts, checksum, and clean-clone
verification plan.

## Do Not Do Yet

- DOI.
- GitHub Release.
- Tag push.
- Formal submission.
- Root metadata overwrite.
- Source layout rewrite.
- LangChain runtime integration.
- OpenTelemetry Collector integration.
