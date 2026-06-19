# AFAC2026 Startup-Track Pitch Outline

## 1. Title and One-Sentence Positioning

TRPS：面向金融机构交易前风险治理的可审计智能决策与模拟执行平台。

TRPS turns risky pre-trade decision requests into structured risk review,
policy gates, human review states, simulated outcomes, and audit-ready receipts.

## 2. Industry Pain Point

Financial institutions face fast-moving decision requests where model output,
market stress, missing evidence, and human responsibility are hard to align in
one reviewable object.

## 3. Target Customers and Workflow Position

Target users are risk, compliance, advisory-operations, and investment-control
teams. TRPS sits before external execution paths as a review and accountability
layer.

## 4. TRPS Closed-Loop Architecture

`input -> belief_state -> risk_distribution -> constrained_policy -> action -> human_review -> simulated_execution -> receipt`

## 5. Core Technical Innovation

TRPS makes traceability a first-class object: the receipt binds input, risk,
policy, gate decision, human review status, limitations, and reproducibility
hashes.

## 6. Demo Scenarios

- Scenario A: normal market and low-risk suggestion, expected `ALLOW` or `WARN`.
- Scenario B: market shock, high volatility, and budget exceedance, expected
  `REVIEW_REQUIRED` or `ESCALATE`.
- Scenario C: misleading input, missing evidence, and unsafe bypass intent,
  expected `BLOCK` or `DEGRADE_TO_SAFE_MODE`.

## 7. Demo Results

The demo shows that unsafe actions are stopped, high-risk decisions are routed
to human review, and every scenario produces a complete receipt.

## 8. Quantitative Metrics

Show `scenario_count`, `blocked_unsafe_action_count`,
`mandatory_review_count`, `receipt_completeness_rate`,
`policy_violation_count`, `average_decision_latency_ms`, and
`audit_trace_linkage_rate`.

## 9. Competitive and Substitute Solutions

Existing review flows are often document-heavy, dashboard-only, or model-score
only. TRPS focuses on decision receipts that are inspectable by humans and
agents.

## 10. Business Model

Initial commercial form: internal risk-governance workflow module, audit-trace
exporter, and controlled proof-of-concept service for synthetic pre-trade
scenarios.

## 11. Compliance and Governance

TRPS keeps human responsibility explicit and treats the receipt as an
accountability artifact. It does not claim official approval or replace a
regulated institution's own controls.

## 12. Milestones and Partnership Ask

v0.1: local runnable demo pack.

v0.2: lightweight page demo, metrics panel, and pitch deck.

v0.3: partner-specific synthetic scenario calibration and human review
workflow testing.
