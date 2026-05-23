# OpenTelemetry to EEOAP Paper Claim

## Exact Claim

Runtime telemetry can describe agent execution, but it does not automatically become portable operation evidence. This prototype demonstrates a bounded adapter path that transforms OpenTelemetry-style agent traces into EEOAP-compatible operation accountability statements that can be checked by the existing EEOAP validator.

## Contribution Boundary

The contribution is a minimal adapter, mapping, and local evaluation path:

- input: one OpenTelemetry-style GenAI trace JSON file;
- transformation: select one agent span and resolved `execute_tool` spans;
- output: one EEOAP v0.1 operation accountability statement;
- check: the existing `agent-evidence validate-profile` validator;
- evidence: one valid fixture, four invalid fixtures, generated statement,
  adapter report, and pytest coverage.

## Non-Claims

- No legal accountability proof.
- No full runtime reconstruction.
- No general OpenTelemetry implementation compatibility claim.
- No agent-output correctness claim.
- No cross-framework generality claim.
- No new profile claim.

## Positioning

This is not an EEOAP replacement and not a second EEOAP profile. It is an
adapter paper: it shows how an external telemetry source can enter the existing
EEOAP evidence-object path without changing the EEOAP schema.
