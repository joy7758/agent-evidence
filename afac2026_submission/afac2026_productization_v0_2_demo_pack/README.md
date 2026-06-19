# AFAC2026 TRPS Demo and Submission Pack v0.2

Status: local demo and submission-material pack, not externally submitted.

This directory converts the validated v0.1 TRPS kernel into reviewer-facing
AFAC2026 startup-track materials: an offline static demo, portal field drafts,
solution/business/governance notes, pitch Markdown, Q&A defense material,
claim-evidence mapping, and validation reports.

## Scope

TRPS is positioned as a decision-support and governance layer for pre-trade
risk decisions. It is not an autonomous trading bot, does not provide personal
investment advice, does not create actual transactions, and does not claim
external approval.

## Inputs

This pack consumes only the committed v0.1 surface:

- `afac2026_submission/afac2026_productization_v0_1/07_demo_scenarios.json`
- `afac2026_submission/afac2026_productization_v0_1/outputs/demo_receipts.json`
- `afac2026_submission/afac2026_productization_v0_1/outputs/demo_metrics.json`
- `afac2026_submission/afac2026_productization_v0_1/outputs/validation_report.json`

## Run

```bash
bash afac2026_submission/afac2026_productization_v0_2_demo_pack/scripts/run_all.sh
```

The static demo can be opened directly from:

- `demo/index.html`

No network CDN, large frontend framework, external account, or execution venue
is required.

## Outputs

- `demo/assets/trps_demo_data.json`
- `outputs/afac_v0_2_manifest.json`
- `outputs/afac_v0_2_manifest.md`
- `outputs/submission_readiness_score.json`
- `outputs/submission_readiness_score.md`
- `outputs/validation_report.json`
- `outputs/validation_report.md`

## EEOAP Mapping

Affected local clauses: `EEOAP-001`, `EEOAP-003`, `EEOAP-004`,
`EEOAP-005`.

These clause references are repository-local traceability markers. They do not
indicate legal compliance, external certification, publication acceptance, or
deployment proof.
