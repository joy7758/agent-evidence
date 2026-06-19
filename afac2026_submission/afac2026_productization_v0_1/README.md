# AFAC2026 TRPS Productization v0.1

Status: local productization pack, not externally submitted.

This directory turns the existing TRPS AFAC candidate into a minimum runnable
startup-track demo pack. It is a separate surface from the existing paper,
deck, ZIP, and reviewable submission candidates.

## Positioning

TRPS is an auditable intelligent decision and simulated execution platform for
pre-trade risk governance in financial institutions.

It is a decision-support and governance layer. It is not an autonomous trading
bot, does not prove real-market profitability, does not replace human
responsibility, and defaults to human-in-the-loop review.

## Demo Loop

The v0.1 loop is:

`scenario -> belief_state -> risk_distribution -> policy_gate -> action -> human_review -> simulated_execution -> receipt -> metrics`

The local demo is deterministic and uses only synthetic scenario objects. It
does not connect to external execution venues, create actual transactions, or
provide investment advice.

## Files

- `00_inventory.md`: current AFAC/TRPS artifact inventory before this pack.
- `01_positioning.md`: Chinese and English product positioning.
- `02_demo_storyboard.md`: five-minute demo path.
- `03_decision_schema.json`: decision object schema.
- `04_action_ontology.json`: action ontology for gate decisions.
- `05_policy_constraints.json`: policy constraints used by the demo gate.
- `06_receipt_schema.json`: receipt schema.
- `07_demo_scenarios.json`: three synthetic demo scenarios.
- `08_metrics_plan.md`: metric definitions and formulas.
- `09_governance_note.md`: governance and claim-boundary note.
- `10_pitch_outline.md`: twelve-page AFAC startup-track pitch outline.
- `scripts/run_afac_trps_demo.py`: deterministic local demo runner.
- `scripts/validate_afac_pack.py`: local pack validator.
- `outputs/`: generated demo and validation outputs.

## Run

Use `python3` when the local `python` alias is not configured:

```bash
python3 afac2026_submission/afac2026_productization_v0_1/scripts/run_afac_trps_demo.py
python3 afac2026_submission/afac2026_productization_v0_1/scripts/validate_afac_pack.py
```

## EEOAP Mapping

This pack is local review material. Its receipt and validation artifacts align
with repository-local EEOAP clauses only:

- `EEOAP-001`: completed demo decision produces a reviewable receipt.
- `EEOAP-003`: each receipt binds policy, scenario evidence, and provenance.
- `EEOAP-004`: the validator produces machine-readable validation reports.
- `EEOAP-005`: task summaries must cite affected clauses.

These local clause citations do not imply legal compliance, external
certification, official standard adoption, or venue acceptance.
