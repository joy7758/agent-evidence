# Venue Route Audit

Official venue pages were freshly checked on 2026-05-23 using the official
ScienceDirect guide pages for JSS, IST, and SoftwareX.

## JSS Route

- Fit score: low.
- Reason: JSS covers software engineering and expects evidence supporting
  claims, including empirical studies, simulation, formal proofs, or other
  validation. The current validation is local and small.
- Fatal blocker: no real runtime or broader validation; artifact references
  are not stable.
- Required next action: add stronger validation and stabilize artifact
  references before considering JSS.
- Recommendation: do not target JSS now.

## IST Route

- Fit score: low.
- Reason: IST requires a clear software engineering component and focuses on
  improving software development practices. The paper has a software
  engineering angle, but the evidence is not yet strong enough to show a
  practice or method contribution at IST level.
- Fatal blocker: weak empirical/practical evidence and no venue-specific
  structured abstract.
- Required next action: strengthen evaluation or pivot route.
- Recommendation: do not target IST now.

## SoftwareX Route

- Fit score: high.
- Reason: SoftwareX is designed for research software descriptions and expects
  a short paper plus open-source software distribution and support material.
  This artifact has a runnable adapter, fixtures, generated outputs, and
  reproducibility evidence.
- Fatal blocker: no public stable artifact identifier yet.
- Required next action: create an immutable release/archive/tag and prepare a
  SoftwareX-style software paper.
- Recommendation: best primary route after blockers are fixed.

## Workshop / Artifact Track Route

- Fit score: high.
- Reason: The contribution is small, bounded, reproducible, and has controlled
  valid/invalid cases.
- Fatal blocker: target-specific rules are not selected.
- Required next action: choose a concrete track and cut a final artifact
  package.
- Recommendation: best fallback route.

## Route verdict

Primary route: SoftwareX software paper route.

Fallback route: workshop / artifact track.
