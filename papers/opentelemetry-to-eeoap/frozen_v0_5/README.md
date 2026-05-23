# OpenTelemetry-to-EEOAP Paper Package v0.5

Title: From Agent Telemetry to Portable Operation Evidence: A Minimal Adapter
from OpenTelemetry Agent Spans to EEOAP Evidence Objects

## Package Status

This directory is an internal frozen draft package for the
OpenTelemetry-to-EEOAP adapter paper. It is intended as a stable local package
for internal archive, future release preparation, DOI archive preparation, or
external pre-review.

It is not yet a DOI archive and not yet a venue-formatted submission.

## Branch

- Branch: `opentelemetry-to-eeoap-adapter`

## Commit Chain

- Adapter prototype:
  `c5df6ce235b7194cafe35945e4b60bd5963c8b94`
- Paper evidence closure:
  `ff8c794b1444527e40b587aef41597bd919b157b`
- Paper v0.1:
  `c4a7d5667cca9717ed6516589472b116ae997889`
- Paper v0.2:
  `07d31cd4fc2758d1c901ba1c5b69339803ae434c`
- Paper v0.3:
  `af28ea5a0c9cc161c0f5488ee8661a9fe5ac89a4`
- Paper v0.4:
  `62b1b4f7ae42d07920c91f44363356ef4f049237`

## Artifact Claim

Runtime telemetry can describe agent execution, but it does not automatically
become portable operation evidence. This package documents a bounded adapter
path that transforms OpenTelemetry-style agent traces into EEOAP-compatible
operation accountability statements that can be checked by the existing EEOAP
validator.

## Non-Claims

- No legal accountability proof.
- No full runtime reconstruction.
- No general OpenTelemetry implementation compatibility claim.
- No cross-framework generality claim.
- No agent-output correctness claim.
- No new profile claim.

## Reproduction Command

```bash
pytest tests/test_opentelemetry_to_eeoap_adapter.py -q
```

Latest scoped test result:

```text
6 passed in 1.97s
```

## Freeze Boundary

Runtime code, tests, and the EEOAP schema were not changed after the adapter
prototype commit. The later commits add paper evidence closure, paper drafts,
reviewer positioning, citation draft material, and this internal frozen paper
package.

Full-repository Ruff was not rerun for this package because unrelated
out-of-scope lint debt remains in pre-existing directories such as `pd-oap/`
and SoftwareX-related paper-support trees. This is repository hygiene debt, not
an adapter failure.
