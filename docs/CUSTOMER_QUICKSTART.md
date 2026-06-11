# Customer Quickstart

## Status

Stage 1 internal hardening documentation. Not commercial-ready. Not
production-ready.

## Purpose

This quickstart provides a short, practical path for a low-risk evaluator to
understand what EEOAP does, run local checks, and avoid overclaims.

EEOAP means Execution Evidence and Operation Accountability Profile.

## Before You Start

- Use a test branch only.
- Do not use customer data, secrets, production logs, or sensitive evidence.
- Start in advisory mode.
- Do not enable enforce mode during the first evaluation.
- Do not enable branch protection requirements during the first evaluation.
- You can stop and roll back.

## What EEOAP Does

EEOAP helps a maintainer or evaluator:

- check protocol citation metadata;
- validate a minimal evidence example;
- check delivery-surface paths;
- use PR evidence guidance;
- review operation-accountability records.

## What EEOAP Does Not Do

EEOAP does not provide:

- legal compliance;
- certification;
- standardization;
- production readiness;
- commercial readiness;
- external validation;
- a guarantee that an agent is correct.

## 10-Minute Local Check

Run these commands from the repository root:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install --upgrade pip
.venv/bin/python -m pip install -e ".[test]"
.venv/bin/python -m json.tool protocol/manifest.json
.venv/bin/python -m json.tool protocol/clause-index.json
.venv/bin/python scripts/check_protocol_citations.py
.venv/bin/python scripts/check_delivery_surface.py
.venv/bin/agent-evidence validate-profile examples/minimal-valid-evidence.json
.venv/bin/python -m pytest tests/test_protocol_citation_checker.py tests/test_delivery_surface.py
```

## Expected Result

A successful local check means:

- JSON checks pass;
- the protocol citation checker returns `ok: true`;
- the delivery-surface checker returns `ok: true`;
- the validator returns `ok: true`;
- focused tests pass.

## If Something Fails

Use these documents first:

- `docs/ERROR_CODES.md`
- `docs/TROUBLESHOOTING.md`
- `docs/SUPPORT_BOUNDARY.md`

When reporting a problem, include the command, exit code, redacted output,
environment, branch, and whether a clean clone was used.

## Next Step

If local checks pass:

- remain in advisory mode;
- review PR template guidance;
- do not claim production readiness;
- do not claim commercial readiness;
- do not enable enforce mode without maintainer approval.

## Non-Claims

This quickstart does not claim:

- commercial readiness;
- production readiness;
- legal compliance;
- external certification;
- standardization;
- publication;
- external validation;
- submitted, accepted, or externally reviewed status;
- external pilot status.
