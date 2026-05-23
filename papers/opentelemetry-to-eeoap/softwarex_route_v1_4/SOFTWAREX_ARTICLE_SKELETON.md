# SoftwareX Article Skeleton

This is a planning skeleton only. It is not a SoftwareX template conversion and
not a final article.

## Software Metadata Table Placeholder

- Software name: OpenTelemetry-to-EEOAP adapter package.
- Repository: `https://github.com/joy7758/agent-evidence`.
- Version: to be decided after release/tag strategy.
- License: Apache-2.0.
- Persistent identifier: not yet assigned for this package.

## Highlights

- Converts OpenTelemetry-style agent traces into EEOAP-compatible operation
  evidence statements.
- Reuses the existing EEOAP validator without changing the EEOAP schema.
- Includes two valid trace contexts and four controlled invalid diagnostics.
- Provides generated statements, adapter reports, checksums, clean-clone notes,
  and local immutable artifact tags.

## Abstract

- State the software need: telemetry does not automatically become portable
  operation evidence.
- State the software contribution: a minimal local adapter and reproducibility
  package.
- State validation: two valid traces pass the existing validator and four invalid
  traces expose diagnostics.
- State boundary: no legal accountability, production readiness, broad
  OpenTelemetry compatibility, or new EEOAP profile claim.

## Keywords

- OpenTelemetry
- operation evidence
- agent telemetry
- EEOAP
- reproducibility
- research software

## Code Metadata / Software Metadata Placeholder

- Programming language: Python.
- Package metadata source: `pyproject.toml`.
- Main adapter path: `tools/opentelemetry_to_eeoap_adapter.py`.
- Test path: `tests/test_opentelemetry_to_eeoap_adapter.py`.
- Fixture path: `examples/opentelemetry/`.
- Generated output path: `generated/`.

## Motivation and Significance

- Explain why agent telemetry is useful but insufficient for portable evidence.
- Explain why an adapter into an existing validator path is useful research
  software.
- Emphasize artifact utility over method-theory novelty.
- Identify likely users: researchers studying agent observability, provenance,
  evidence packaging, or reproducible AI-agent audit trails.

## Software Description

- Describe input trace assumptions.
- Describe agent-span selection, tool-span resolution, parent-child relation
  checks, provenance preservation, statement emission, and validator routing.
- Describe output files and adapter reports.
- Keep claims bounded to local OpenTelemetry-style fixtures.

## Illustrative Example

- Use `valid-agent-trace` as the baseline conversion example.
- Use `valid-agent-workflow-trace` to show a deeper parent-child span structure.
- Summarize generated statement validation results.
- Mention invalid diagnostics without expanding into a full method paper.

## Impact

- Positions EEOAP as reachable from telemetry ecosystems.
- Gives reviewers and later integrators a minimal baseline for telemetry-to-
  evidence transformation.
- Helps compare raw traces with portable evidence objects.
- Supports follow-on real-runtime integration without claiming it yet.

## Limitations

- Synthetic fixtures only.
- No broad OpenTelemetry implementation compatibility.
- No production readiness.
- No legal accountability proof.
- No runtime reconstruction.
- No cross-framework generality.

## Reproducibility and Artifact Availability

- Refer to `frozen_v0_5/` and v0.7 second-trace evidence.
- Include scoped test command.
- Include clean-clone and checksum evidence.
- Explain local tags and why public release/DOI is still pending.

## Declaration of Generative AI and AI-Assisted Technologies

- State that AI-assisted tools were used for drafting/planning if applicable.
- State that the author reviewed and edited the content.
- Follow the final venue wording exactly at submission time.

## Conflict of Interest

- Add final declaration before submission.
- Do not infer or invent conflicts in this analysis.

## Funding

- Add final funding declaration before submission.
- If no funding applies, use the venue-appropriate no-funding statement.

## References

- Use official OpenTelemetry and EEOAP/AEP artifact references.
- Replace local-only tag references with public release/tag/archive/DOI links
  if created.
- Keep unresolved metadata marked until final verification.
