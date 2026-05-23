# Word Count and Structure Audit

## Word Count Result

The v1.9 draft was counted with a simple Python regular-expression token count.

- Total word count: `2939`
- Approximate body word count excluding metadata table and references: `2520`
- Within 3000-word target: yes, based on the current approximation.

This is not an official venue word count. It is sufficient for a draft-stage
SoftwareX self-review.

## Section Audit

| Section | Approximate word count | Target range | Action |
|---|---:|---:|---|
| Software metadata table placeholder | 149 | excluded from article body | Keep as placeholder; resolve TODOs later. |
| Highlights | 67 | 3-5 concise bullets | Keep; polish wording in v1.11. |
| Abstract | 181 | 180-220 | Keep within range; tighten software utility phrasing. |
| Keywords | 11 | concise | Keep. |
| Motivation and Significance | 444 | 500-650 | Slightly short but acceptable; add only if clarity needs it. |
| Software Description | 565 | 700-850 | Short for target; v1.11 should add run path and package layout detail without overclaiming. |
| Illustrative Example | 397 | 450-600 | Slightly short; add a compact run-and-validate flow if useful. |
| Impact | 296 | 300-450 | Acceptable; avoid expanding into journal novelty claims. |
| Limitations | 231 | 250-350 | Slightly short; add release-metadata limitation or CFF validation note if needed. |
| Reproducibility and Artifact Availability | 189 | 250-350 | Too short; v1.11 should add exact artifacts and maintenance test result. |
| Declarations | 206 | minimal | Acceptable; keep draft/TODO status clear. |
| References | 194 | excluded from article body | Keep TODOs until release references are fixed. |

## What Should Be Compressed

- Repeated statements that telemetry is not automatically evidence.
- Method-paper phrasing around "claim boundary" and "software engineering
  method".
- Conceptual discussion that does not name source paths, commands, artifacts, or
  validation.

## What Should Move To Supplementary Material

- Long route history from journal path to SoftwareX path.
- Detailed v0.5/v1.3/v1.5 command logs.
- Extended reviewer defense and strict review materials.
- Full metadata strategy rationale.

## What Should Remain Unchanged

- Two-valid plus four-invalid evaluation story.
- Validator result boundary.
- No schema change statement.
- No legal accountability, no production readiness, no broad OpenTelemetry
  compatibility, and no real runtime integration boundaries.
