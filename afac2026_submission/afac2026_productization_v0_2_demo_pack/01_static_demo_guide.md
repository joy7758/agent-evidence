# Static Demo Guide

## Demo Entry

Open:

`afac2026_submission/afac2026_productization_v0_2_demo_pack/demo/index.html`

The page is a pure HTML/CSS/JavaScript artifact. It has no network dependency
and can be inspected offline.

## Demo Narrative

1. Start with the title:
   TRPS：面向金融机构交易前风险治理的可审计智能决策与模拟执行平台
2. Explain the short positioning:
   Not an autonomous trading bot. A governance layer for pre-trade risk
   decisions.
3. Select each scenario card:
   - normal market and low-risk suggestion;
   - market shock, high volatility, and risk-budget exceedance;
   - misleading input, missing evidence, and unauthorized intent.
4. Inspect the decision details:
   - `belief_state`;
   - `risk_distribution`;
   - `triggered_constraints`;
   - `gate_decision`;
   - `human_review_status`;
   - `final_action`;
   - `receipt_id`;
   - `rationale`.
5. Close with the metrics panel and boundary statement.

## Judge-Facing Point

The demo is not trying to show return generation. It shows whether a risky
pre-trade decision can be converted into a reviewable governance object with a
complete receipt.
