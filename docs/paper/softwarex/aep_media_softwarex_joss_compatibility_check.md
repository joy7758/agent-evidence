# AEP-Media JOSS Compatibility Check

## JOSS-style Expectations

JOSS expects a research software package with browsable source, an OSI-approved open-source license, documentation, tests, examples, and a concise `paper.md` that describes the software rather than a full research-results article.

## Current Fit

Criterion | Current status
--- | ---
Open repository | Repository identified; public accessibility should be confirmed before submission.
OSI-approved license | Apache-2.0 present.
Browsable source | Python package and modules are present.
Issue / PR workflow | GitHub repository supports this in principle; repository settings should be confirmed.
Research application | AEP-Media supports operation accountability and media evidence package validation.
Documentation | Specs, schemas, examples, demos, reports, and README exist.
Tests | Prior reports record pytest runs; rerun before submission.
Examples | Valid, invalid, strict-time, bundle, adapter, and tamper examples exist.
Paper format | A JOSS `paper.md` would need to be concise and less narrative than the SoftwareX draft.
Not focused on new research results | AEP-Media must be framed as software functionality and research use, not as a full empirical or theoretical paper.

## Strengths for JOSS

- Apache-2.0 license.
- Python package with CLI.
- Examples and tests.
- Reproducible validation commands.
- Clear research use case.

## Weaknesses for JOSS

- The AEP-Media story currently includes a broader software artifact and validation narrative than a typical concise JOSS paper.
- The current manuscript materials are more extensive than JOSS expects.
- The repository README should make the AEP-Media path easier for a reviewer to find quickly.

## Conclusion

JOSS is possible if the submission is reframed as a concise software package paper. SoftwareX is the stronger first target because AEP-Media includes a broader software artifact, release package, validation narrative, evaluation matrix, and research-software impact story.
