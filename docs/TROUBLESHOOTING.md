# Troubleshooting Guide

## Status

Internal hardening documentation. Not commercial-ready. Not production-ready.

## Quick Diagnosis

| Symptom | Likely cause | First command to run | Fix |
| --- | --- | --- | --- |
| `agent-evidence command not found` | CLI is not installed in the active environment. | `.venv/bin/agent-evidence validate-profile examples/minimal-valid-evidence.json` | Use the virtual-environment CLI or install the package in editable mode. |
| `No module named pytest` | Test dependencies are missing. | `.venv/bin/python -m pip install -e ".[test]"` | Install the `test` extra in the active virtual environment. |
| `missing_related_file` | `protocol/clause-index.json` references a missing path. | `python3 scripts/check_protocol_citations.py` | Update `related_files` to an existing path, or add the missing file if in scope. |
| `invalid_clause_id_format` | Clause ID does not match `EEOAP-XXX`. | `python3 scripts/check_protocol_citations.py` | Use a valid clause identifier and open a dedicated protocol-change PR for new clauses. |
| `missing_delivery_surface_path` | Delivery surface includes a missing path. | `python3 scripts/check_delivery_surface.py` | Remove stale includes or add stable files that belong in the surface. |
| `forbidden_delivery_surface_path` | Delivery surface includes an excluded path. | `python3 scripts/check_delivery_surface.py` | Remove paper, submission, manuscript, media, or package artifact paths from the surface. |
| Validator returns `schema_violation` | Evidence does not match the expected profile. | `agent-evidence validate-profile examples/minimal-valid-evidence.json` | Inspect missing or invalid fields and rerun the validator. |
| GitHub Actions CI fails but local commands pass | Local environment, paths, or dependency install differ from CI. | `python3 scripts/check_protocol_citations.py && python3 scripts/check_delivery_surface.py` | Reproduce from a clean clone and compare install commands. |
| Clean clone install fails | Virtual environment or package extras were not installed. | `.venv/bin/python -m pip install -e ".[test]"` | Recreate the virtual environment and install the `test` extra. |
| Delivery surface checker passes but broad repository scan finds paper/submission context | The broad repository contains research or governance context outside the commercial delivery surface. | `python3 scripts/check_delivery_surface.py` | Treat `packaging/commercial-delivery-surface.json` as the candidate delivery set. |

## Recommended Local Check Sequence

Run these commands from the repository root:

```bash
python3 -m json.tool protocol/manifest.json
python3 -m json.tool protocol/clause-index.json
python3 scripts/check_protocol_citations.py
python3 scripts/check_delivery_surface.py
agent-evidence validate-profile examples/minimal-valid-evidence.json
pytest tests/test_protocol_citation_checker.py tests/test_delivery_surface.py
```

Fallback validator command:

```bash
.venv/bin/agent-evidence validate-profile examples/minimal-valid-evidence.json
```

## Clean Clone Checklist

1. Clone the repository fresh.
2. Create a virtual environment.
3. Install editable package dependencies with `.[test]`.
4. Run the protocol citation checker.
5. Run the delivery-surface checker.
6. Run the validator smoke command.
7. Run focused tests.

Example:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install --upgrade pip
.venv/bin/python -m pip install -e ".[test]"
python3 scripts/check_protocol_citations.py
python3 scripts/check_delivery_surface.py
.venv/bin/agent-evidence validate-profile examples/minimal-valid-evidence.json
.venv/bin/pytest tests/test_protocol_citation_checker.py tests/test_delivery_surface.py
```

## Delivery Surface vs Whole Repository

The commercial delivery surface is the candidate delivery set defined in
`packaging/commercial-delivery-surface.json`.

The whole repository may contain research or governance context that is not part
of the commercial delivery surface. Stage 1 checks should prioritize the
delivery surface file. Do not treat unrelated paper, submission, manuscript, or
media files as delivery-surface blockers unless they enter the delivery surface.

## Safe Fix Rules

- Do not add EEOAP clauses casually.
- Do not change protocol claim scope casually.
- Do not modify validator logic for documentation-only failures.
- Open a dedicated PR for protocol changes.
- Open a dedicated PR for validator changes.

## Not Support / Not Claims

This project does not currently claim commercial readiness, production
readiness, legal compliance, external certification, standardization, or
external validation.
