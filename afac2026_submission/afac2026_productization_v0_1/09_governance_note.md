# Governance Note

This pack is a local AFAC2026 startup-track productization surface for TRPS.
It is designed to be agent-readable and reviewer-readable.

## Control Model

- Every scenario becomes a structured decision object.
- Every decision references a policy version.
- Every triggered policy constraint is recorded.
- Every selected gate action must be allowed by the triggered constraints.
- Human review status is explicit.
- Simulated execution is offline and synthetic.
- Every final action produces a receipt.

## Human-in-the-Loop Roles

- `risk_analyst`: reviews low-risk warnings and receipt completeness.
- `risk_manager`: reviews high-volatility and safe-mode cases.
- `risk_committee_delegate`: receives escalated material-risk cases.
- `control_owner`: owns hard-block review and remediation.

## Boundary

The local v0.1 pack does not use real customer records, does not connect to
external execution venues, does not create actual transactions, does not
provide investment advice, and does not claim external approval.

The receipt is an accountability mechanism. It records what the local demo
decided, which policy constraints were triggered, what human review state was
recorded, and how the result can be reproduced. It is not a proof of legal
compliance, production robustness, or official acceptance.

## EEOAP Clause Mapping

- `EEOAP-001`: each completed scenario decision produces a receipt-like
  operation accountability statement.
- `EEOAP-003`: each receipt links scenario input, policy constraints, evidence
  status, and generated provenance hashes.
- `EEOAP-004`: the validator emits machine-readable and Markdown validation
  reports.
- `EEOAP-005`: implementation summaries must cite affected clauses.
