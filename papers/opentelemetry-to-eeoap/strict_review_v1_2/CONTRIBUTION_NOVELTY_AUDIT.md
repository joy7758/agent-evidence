# Contribution Novelty Audit

## Compared with EEOAP work

- What is new: a telemetry-to-EEOAP adapter path and evaluation fixtures.
- What is not new: the target evidence object and validator.
- Overlap risk: high if reviewers think this is only another EEOAP paper.
- How to sharpen distinction: state that EEOAP defines the target, while this
  paper studies ingress from telemetry into that target.

## Compared with AEP work

- What is new: span-to-operation-evidence transformation.
- What is not new: broader evidence-bundle and integrity-packaging ideas.
- Overlap risk: medium, especially while AEP references remain unstable.
- How to sharpen distinction: treat AEP only as adjacent artifact packaging
  context, not as a core dependency.

## Compared with raw OpenTelemetry traces

- What is new: mapping from trace spans into a validator-aware operation
  evidence object.
- What is not new: traces, span ids, parent ids, timestamps, attributes, and
  error fields.
- Overlap risk: medium. Reviewers may ask why a trace plus dashboard is not
  enough.
- How to sharpen distinction: emphasize validation target, evidence object
  portability, and failure diagnostics.

## Compared with provenance models

- What is new: concrete mapping into EEOAP statements and validator checks.
- What is not new: the idea of preserving relations among agents, activities,
  and entities.
- Overlap risk: medium. The manuscript does not yet deeply engage provenance
  literature.
- How to sharpen distinction: cite specific PROV concepts and explain that the
  adapter is not a general provenance framework.

## Compared with artifact evaluation norms

- What is new: a specific telemetry-to-evidence artifact package.
- What is not new: clean-clone, checksum, and reproducibility expectations.
- Overlap risk: low for artifact route, higher for main journal route because
  reproducibility alone is not a research contribution.
- How to sharpen distinction: keep artifact evidence as support, not the sole
  novelty claim.

## Compared with adapter/tool papers

- What is new: profile-aware evidence generation and validator routing.
- What is not new: building a converter between JSON-like structures.
- Overlap risk: high. This is the most dangerous perception.
- How to sharpen distinction: add a baseline, formalize failure taxonomy, or
  add a real runtime fixture.

## Novelty verdict

better as software/artifact paper
