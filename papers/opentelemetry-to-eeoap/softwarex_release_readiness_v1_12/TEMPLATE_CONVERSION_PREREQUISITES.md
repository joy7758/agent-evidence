# Template Conversion Prerequisites

## Must Be Resolved Before Template Conversion

- Decide the provisional release strategy to describe in the template draft.
- Decide how to handle root `CITATION.cff` and `codemeta.json` mismatch in the
  manuscript narrative.
- Define the artifact availability wording as draft text, including clear TODOs
  for public release, DOI, pushed tags, and GitHub Release.
- Define how the article will represent the lack of `repo/src` layout.
- Decide whether version 0.5 frozen material is historical support material or
  the current release candidate.
- Finalize the SoftwareX metadata table TODO strategy: which fields remain TODO
  during template conversion and which fields need stable draft wording now.

These are prerequisite decisions, not repository edits.

## Can Be Resolved During Template Conversion

- Moving Markdown sections into the official SoftwareX template.
- Polishing highlights, abstract, and metadata table language.
- Keeping declarations in the correct template locations.
- Keeping references as verified placeholders while public release identifiers
  are still missing.
- Adding a concise note that the adapter source currently lives under `tools/`
  within the broader `agent-evidence` repository.

## Must Wait Until Release/Public Archive

- Pushing `eeoap-v0.1-artifact` and `aep-v0.1-artifact`.
- Creating a package-specific OpenTelemetry-to-EEOAP release tag.
- Creating a GitHub Release.
- Creating DOI or archive metadata.
- Filling final repository, release, archive, and DOI URLs.
- Replacing EEOAP/AEP placeholder references with final public identifiers.
- Running final clean-clone verification and final checksum verification.

## Should Not Be Changed Now

- Root `CITATION.cff`.
- Root `codemeta.json`.
- Root README, LICENSE, and `pyproject.toml`.
- Runtime adapter code.
- Tests, fixtures, and generated JSON outputs.
- EEOAP schema.
- Repository source layout.
- LangChain runtime integration or OpenTelemetry Collector integration.

## Conclusion

The project is not blocked from a template-readiness draft, but it is blocked
from official template conversion unless the draft first clarifies release
strategy, metadata handling, artifact availability wording, source-layout
wording, and frozen-package status.
