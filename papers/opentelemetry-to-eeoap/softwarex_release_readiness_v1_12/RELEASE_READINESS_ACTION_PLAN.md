# Release-Readiness Action Plan

## P0 Before Template Conversion

Only these actions are required before official SoftwareX template conversion:

- Create a template-conversion readiness draft that updates release,
  metadata, artifact availability, and source-layout wording.
- State the provisional release strategy: focused release-candidate branch for
  OpenTelemetry-to-EEOAP, with optional supplementary archive later.
- State that root `CITATION.cff` and `codemeta.json` currently describe
  AEP-Media and are not final OpenTelemetry-to-EEOAP metadata.
- State that local metadata drafts are draft-only and public release metadata
  remains TODO.
- Clarify that `frozen_v0_5/` is historical support material, not the final
  SoftwareX release package.
- Explain that source code currently lives under `tools/` and broader package
  code under `agent_evidence/`, not `repo/src`.
- Keep DOI, GitHub Release, tag push, and public archive as explicit TODOs.

## P1 Before Formal Submission

These actions are needed before formal submission but not before template
conversion:

- Decide and execute public release strategy.
- Create or publish a final OpenTelemetry-to-EEOAP release tag.
- Decide whether to push EEOAP/AEP local artifact tags.
- Create GitHub Release or public archive if selected.
- Create DOI if the archive route is selected.
- Finalize OpenTelemetry-to-EEOAP CFF and CodeMeta metadata.
- Validate CFF YAML syntax with a parser.
- Replace EEOAP/AEP placeholder references with final public identifiers.
- Refresh final support package so it includes the second valid trace evidence.
- Run final clean-clone verification.
- Regenerate final checksums.
- Rerun validator checks for both valid generated statements.
- Rerun scoped pytest.
- Finalize declarations and data/artifact availability statements.

## P2 After Editorial Feedback or Before Final Archive

- Consider whether a `LICENSE.txt` copy is necessary.
- Consider whether a focused source layout or `src/` package is necessary.
- Add optional graphical abstract if helpful.
- Add optional workflow diagram if helpful.
- Polish metadata table fields after public release identifiers exist.
- Adjust repository README only if release scope is confirmed.

## One-Week Plan

Day 1:
Create version 1.13 template-conversion readiness draft with updated artifact,
metadata, frozen-package, and source-layout wording.

Day 2:
Review the version 1.13 wording against v1.11 article sections and v1.8
metadata drafts.

Day 3:
Decide whether the official template conversion can start without public
release execution.

Day 4:
If ready, begin template conversion using the v1.13 readiness wording. If not,
revise the readiness draft once more.

Day 5:
Run scoped tests and prepare a release-execution checklist for P1 blockers,
without pushing tags or creating DOI/GitHub Release yet.
