# Claim Boundary

## Positive Claim

Runtime telemetry can describe agent execution, but it does not automatically
become portable operation evidence. This prototype demonstrates a bounded
adapter path that transforms OpenTelemetry-style agent traces into
EEOAP-compatible operation accountability statements that can be checked by the
existing EEOAP validator.

## Evidence Basis

- Adapter prototype commit:
  `c5df6ce235b7194cafe35945e4b60bd5963c8b94`
- Paper evidence closure commit:
  `ff8c794b1444527e40b587aef41597bd919b157b`
- Adapter path: `tools/opentelemetry_to_eeoap_adapter.py`
- Valid fixture: `examples/opentelemetry/valid-agent-trace.json`
- Generated statement:
  `generated/valid-agent-trace-eeoap-statement.json`
- Generated adapter report:
  `generated/valid-agent-trace-adapter-report.json`
- Existing validator path:
  `agent-evidence validate-profile`

## Non-Claims

- No legal accountability proof.
- No court-grade audit proof.
- No regulatory certification.
- No full runtime reconstruction.
- No general OpenTelemetry implementation compatibility claim.
- No cross-framework generality claim.
- No LangChain, CrewAI, AutoGen, or multi-runtime comparison claim.
- No agent-output correctness claim.
- No new profile claim.
- No EEOAP schema change claim.

## Scope of Validator Success

The existing EEOAP validator checks that the generated statement is
schema-conformant, reference-closed, internally consistent, and
integrity-linked under the current EEOAP v0.1 schema.

Validator success does not prove legal sufficiency, semantic correctness of
the agent output, complete runtime reconstruction, or external runtime
attestation.
