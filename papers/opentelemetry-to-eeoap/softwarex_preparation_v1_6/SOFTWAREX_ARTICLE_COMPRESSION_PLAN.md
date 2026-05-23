# SoftwareX Article Compression Plan

## Current Word Count

`paper_v1_0_submission_candidate.md` is approximately 3692 words.

## SoftwareX Target

SoftwareX software article maximum: 3000 words, excluding title, authors,
affiliations, references, and metadata tables.

## Sections to Preserve

- Problem: telemetry does not automatically become portable operation evidence.
- Software contribution: a minimal adapter from OpenTelemetry-style agent spans
  to EEOAP-compatible statements.
- Reproducible evidence: two valid traces, four invalid traces, generated
  statements, adapter reports, scoped tests, validator results, clean-clone
  checks, checksums, and local artifact tags.
- Non-claims: no legal accountability, runtime reconstruction, broad
  compatibility, production readiness, or new EEOAP profile.

## Sections to Compress

- Background on OpenTelemetry and EEOAP.
- Detailed mapping rationale.
- Related work.
- Threats to validity.
- Reviewer-defense language from v1.0.

## Sections to Move to Supplementary Material

- Full reviewer-positioning argument.
- Full claim-boundary table.
- Detailed v0.5/v1.3/v1.5 command logs.
- Extended route analysis and strict review artifacts.
- Full references draft history.

## Suggested SoftwareX Article Structure

1. Software metadata table.
2. Highlights.
3. Abstract.
4. Keywords.
5. Motivation and significance.
6. Software description.
7. Illustrative example.
8. Impact.
9. Limitations.
10. Reproducibility and artifact availability.
11. Declarations.
12. References.

## Target Word Budget

| Section | Target words |
|---|---:|
| Abstract | 180-220 |
| Motivation and significance | 500-650 |
| Software description | 700-850 |
| Illustrative example | 450-600 |
| Impact | 300-450 |
| Limitations | 250-350 |
| Reproducibility and availability | 250-350 |
| Declarations | minimal |

## Compression Principle

Treat this as a software paper, not a journal method article. Keep the adapter,
inputs, outputs, validation path, and reproducibility package in the foreground;
move method-theory defense into supplementary material.
