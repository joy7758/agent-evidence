# SoftwareX Article Draft Plan

This file plans a future SoftwareX article draft. It is not the draft itself.

## Candidate Title

1. `OpenTelemetry-to-EEOAP: A Minimal Adapter for Portable Agent Operation Evidence`
2. `A Reproducible Adapter from Agent Telemetry to EEOAP-Compatible Evidence Objects`
3. `OpenTelemetry-to-EEOAP Adapter: Research Software for Telemetry-to-Evidence Transformation`

## Highlights

- Converts OpenTelemetry-style agent traces into EEOAP-compatible operation
  evidence statements.
- Preserves trace/span provenance and checks parent-child span relations.
- Includes two valid trace contexts and four controlled invalid diagnostics.
- Reuses the existing EEOAP validator without schema changes.
- Provides reproducibility material, checksums, and local artifact tags.

## Abstract Intent

The abstract should present the software need, the adapter function, the
validation result, and the non-claim boundary in a compact form. It should avoid
method-paper overreach and emphasize reusable research software.

## Software Metadata Table Fields

- Software name.
- Current software version or release candidate tag.
- Repository URL.
- License.
- Programming language.
- Runtime requirements.
- Main adapter path.
- Test path.
- Fixture path.
- Generated output path.
- Persistent identifier once available.

## Motivation and Significance

- Runtime telemetry helps observability but is not automatically portable
  operation evidence.
- Agent evidence research needs reproducible bridges between telemetry and
  validator-ready evidence objects.
- The package gives a bounded, inspectable baseline for later real-runtime
  integrations.

## Software Description

- Input: local OpenTelemetry-style trace JSON.
- Process: locate agent span, preserve provenance, resolve tool spans, check
  parent-child relation, emit EEOAP statement, route into validator.
- Output: EEOAP-compatible statement and adapter report.
- Boundary: controlled fixtures only.

## Illustrative Example

- First valid trace: direct tool-child pattern.
- Second valid trace: workflow span with deeper tool descendants.
- Both generated statements validate with `ok=true`, `issue_count=0`.
- Four invalid traces show bounded diagnostics.

## Impact

- Provides a concrete path from telemetry to portable operation evidence.
- Supports reproducible review of adapter behavior.
- Clarifies what EEOAP adds beyond raw traces.
- Provides a baseline for future integrations.

## Limitations

- Synthetic fixtures only.
- No broad OpenTelemetry compatibility proof.
- No production readiness.
- No legal accountability proof.
- No cross-framework generality.

## Reproducibility

- Scoped adapter tests.
- Generated statements and reports.
- Existing EEOAP validator.
- Clean release-candidate worktree.
- Frozen package checksum verification.
- Local artifact tags.

## Declarations

- Generative AI-assisted writing disclosure.
- Conflict of interest declaration.
- Funding statement.
- Data/software availability statement.

## References Still Needed

- Official OpenTelemetry Generative AI semantic conventions.
- Official OpenTelemetry agent span semantic conventions.
- JSON Schema reference.
- W3C PROV reference.
- EEOAP artifact reference.
- AEP artifact reference.
- SoftwareX author guidance or software article template reference if required.
