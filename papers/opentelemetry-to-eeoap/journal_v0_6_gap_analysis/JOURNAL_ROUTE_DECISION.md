# Journal Route Decision

## Decision

Pursue journal route after minimal expansion.

## Reason

The current OpenTelemetry-to-EEOAP package is strong as an
external-review-ready frozen artifact. It has a working adapter, one valid
trace, four controlled invalid traces, existing EEOAP validator acceptance,
clean-clone verification, checksum verification, and clear non-claim
boundaries.

It is not yet strong enough for a journal main paper because the positive
evaluation contains only one valid trace and no second operation context,
framework-derived fixture, or SDK-generated source. The journal route becomes
more credible after one additional valid trace context is added and validated
without schema changes.

## Minimal Next Engineering Task If Pursuing Journal Route

Add one second valid OpenTelemetry-style trace context and validate it without
modifying EEOAP schema.

## Minimal Next Writing Task

Draft `paper_v0_7_journal_plan.md` using the expanded evaluation plan.

## Deferred Tasks

- Zenodo DOI
- GitHub release
- venue-specific formatting
- real runtime integration
- broad OpenTelemetry compatibility claims
- cross-framework evaluation
