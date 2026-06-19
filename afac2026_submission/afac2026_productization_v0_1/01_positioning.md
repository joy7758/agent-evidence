# TRPS Product Positioning

中文标题：

TRPS：面向金融机构交易前风险治理的可审计智能决策与模拟执行平台

English title:

TRPS: An Auditable Intelligent Decision and Simulated Execution Platform for Pre-Trade Risk Governance in Financial Institutions

## AFAC2026 Track

TRPS is positioned for the AFAC2026 startup track. It is not positioned for the
challenge track in this local productization pack.

## One-Sentence Positioning

TRPS helps financial institutions convert high-risk pre-trade decisions into
structured belief states, risk distributions, constrained policy checks,
human-reviewed actions, simulated execution outcomes, and audit-ready receipts.

## Core Boundary

- TRPS is a decision-support and governance layer.
- TRPS is not an autonomous trading bot.
- TRPS does not prove real-market profitability.
- TRPS does not replace human responsibility.
- TRPS defaults to human-in-the-loop review.
- TRPS receipts are accountability mechanisms, not performance engines.

## What v0.1 Demonstrates

The local v0.1 pack demonstrates a controlled loop:

`scenario input -> belief/risk structure -> policy gate -> action -> human review -> simulated execution -> receipt -> metrics panel`

The demo is useful when a reviewer needs to inspect how a risky financial
decision would be blocked, downgraded, or escalated before any external
execution path is considered.

## Claim Boundary

This pack is local, synthetic, and reproducible. It does not use real customer
data, does not connect to external execution venues, does not provide
investment advice, and does not claim regulatory approval or production
deployment readiness.

Affected EEOAP clauses for this local pack: `EEOAP-001`, `EEOAP-003`,
`EEOAP-004`, `EEOAP-005`.
