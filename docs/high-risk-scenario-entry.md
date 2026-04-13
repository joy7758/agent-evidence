# High-Risk Scenario Entry

This note adds one discoverable, reviewer-facing high-risk scenario to the
current AEP v0.1 path without changing the core package boundary.

## Scenario

The scenario is one flagged payment review:

- one payment case subject
- two input references
- one review decision output
- one policy-constrained operation accountability statement

## Files

- `examples/valid-high-risk-payment-review-evidence.json`
- `examples/invalid-high-risk-unclosed-reference.json`
- `examples/invalid-high-risk-policy-link-broken.json`

## Boundary

This is not a payment engine, settlement system, fraud model, or compliance
control plane. It is a minimal operation-accountability surface for a
high-risk, reviewer-facing setting.

## Validate

```bash
agent-evidence validate-profile examples/valid-high-risk-payment-review-evidence.json
agent-evidence validate-profile examples/invalid-high-risk-unclosed-reference.json
agent-evidence validate-profile examples/invalid-high-risk-policy-link-broken.json
```
