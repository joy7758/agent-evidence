# Metrics Plan

The v0.1 demo uses deterministic synthetic metrics. Metrics are intended for
local review and judge-facing explanation, not for claims about real-market
performance.

## Required Metrics

- `scenario_count`: number of synthetic scenarios processed.
- `blocked_unsafe_action_count`: count of scenarios where an unsafe action was
  stopped through `BLOCK` or converted through `DEGRADE_TO_SAFE_MODE`.
- `mandatory_review_count`: count of decisions where human review is required
  or escalation is selected.
- `receipt_completeness_rate`: share of generated receipts containing every
  required receipt field.
- `policy_violation_count`: count of triggered constraints not handled by the
  selected gate action.
- `average_decision_latency_ms`: deterministic simulated latency average for
  demo repeatability.
- `audit_trace_linkage_rate`: share of scenario decisions with stable scenario,
  decision, policy, and receipt hashes.

## Target v0.1 Acceptance Values

- `scenario_count = 3`
- `blocked_unsafe_action_count >= 1`
- `mandatory_review_count >= 2`
- `receipt_completeness_rate = 1.0`
- `policy_violation_count = 0`
- `audit_trace_linkage_rate = 1.0`

## Why These Metrics Matter

The productization goal is to show a minimum governance loop:

`scenario -> decision -> gate -> human review -> simulated execution -> receipt`

The strongest v0.1 signal is not return. The strongest signal is that dangerous
requests are stopped or escalated, each decision has a complete receipt, and
policy violations remain zero in the controlled demo.
