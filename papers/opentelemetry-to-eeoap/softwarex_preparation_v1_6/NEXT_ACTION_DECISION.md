# Next Action Decision

## Decision

resolve metadata strategy first

## Reason

The isolated release-candidate branch is clean and the adapter evidence still
passes scoped validation, but the current repository metadata points to
AEP-Media rather than OpenTelemetry-to-EEOAP. Drafting a SoftwareX article or
creating release tags before choosing the metadata strategy would risk naming
the wrong software object.

## Next Single Action

Create an OpenTelemetry-to-EEOAP metadata strategy note in the isolated
release-candidate branch.

## Do Not Do Yet

- Code refactor.
- Source layout rewrite.
- DOI.
- GitHub Release.
- Tag push.
- Formal submission.
- LangChain runtime integration.
- OpenTelemetry Collector integration.
