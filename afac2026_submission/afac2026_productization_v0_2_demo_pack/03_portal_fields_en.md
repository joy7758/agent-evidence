# AFAC Portal Field Drafts (English)

## Project Name

TRPS: An Auditable Intelligent Decision and Simulated Execution Platform for Pre-Trade Risk Governance in Financial Institutions

## One-Sentence Summary

TRPS turns high-risk pre-trade decisions into reviewable risk structures,
policy gates, human review states, and audit receipts before any external
execution path is considered.

## Project Abstract

TRPS is a governance-layer platform for pre-trade risk decisions in financial
institutions. It converts scenario inputs into belief states, risk
distributions, constrained policy checks, gate decisions, human review states,
and receipts. The v0.2 pack uses synthetic controlled scenarios only. It does
not connect to external execution systems, does not create actual transactions,
and does not provide personal investment advice. The goal is to give advisory,
asset-management, risk, and compliance teams a reviewable demo surface for
decision accountability before risky actions move downstream.

## Technical Innovation

TRPS does not try to replace an execution system. Its technical contribution is
to make the pre-action governance object explicit. It structures intent,
evidence completeness, market pressure, liquidity pressure, and operational
risk into a risk distribution. A policy gate then selects actions such as
`ALLOW`, `WARN`, `REVIEW_REQUIRED`, `ESCALATE`, `BLOCK`, or
`DEGRADE_TO_SAFE_MODE`. Each decision produces a receipt that binds scenario
input, policy version, triggered constraints, human review state, final action,
limitations, and reproducibility hashes.

## Application Scenarios

TRPS fits risk review workflows in asset management, wealth management,
advisory operations, and compliance teams. Typical use cases include
pre-action review during market stress, governance of AI-generated advisory
recommendations, blocking decisions with missing evidence, safe-mode handling
of conflicting signals, human review routing, and later audit material
preparation. The v0.2 demo covers normal-market, market-shock, and misleading
input scenarios.

## Business Value

TRPS helps institutions turn risky AI-assisted decisions into inspectable
governance assets. It can reduce unauthorized-action risk, shorten review
preparation time, improve receipt completeness, and make stress-scenario
handling more consistent. A practical commercialization path can start with
synthetic controlled evaluation and historical control-signal replay, then move
to shadow mode, human-in-the-loop pilots, and controlled rollout.

## Governance Boundary

TRPS defaults to human-in-the-loop governance with a kill switch, whitelisted
actions, policy gates, model/policy versioning, and audit receipts. The v0.2
pack is a local synthetic demo. It does not use real customer data, connect to
external execution systems, create actual transactions, provide personal
investment advice, or claim external approval.

## Keywords

pre-trade risk governance; auditable intelligent decision; audit receipt;
human-in-the-loop; policy gate; synthetic controlled evaluation; financial AI
governance; TRPS
