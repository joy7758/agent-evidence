# AFAC2026 TRPS Demo Summary

Status: local synthetic demo output.

No real customer data, investment advice, external execution connectivity, or actual transactions are used.

## Decisions

| Scenario | Gate | Human Review | Receipt |
| --- | --- | --- | --- |
| AFAC_TRPS_A_LOW_RISK_NORMAL_MARKET | `WARN` | `desk_acknowledged_for_demo` | `receipt-8a92ff7a745c29f6` |
| AFAC_TRPS_B_MARKET_SHOCK_HIGH_VOLATILITY | `ESCALATE` | `required_and_escalated_for_demo` | `receipt-391f9dafdf1af5fe` |
| AFAC_TRPS_C_MISLEADING_MISSING_EVIDENCE | `BLOCK` | `required_for_block_review` | `receipt-bf026920a9b83c7b` |

## Metrics

- `scenario_count`: `3`
- `blocked_unsafe_action_count`: `1`
- `mandatory_review_count`: `2`
- `receipt_completeness_rate`: `1.0`
- `policy_violation_count`: `0`
- `average_decision_latency_ms`: `29`
- `audit_trace_linkage_rate`: `1.0`
- `actual_transaction_generated_count`: `0`
- `external_execution_connected`: `False`

## EEOAP Notes

Generated receipts support local review for `EEOAP-001`, `EEOAP-003`, and `EEOAP-004`.
