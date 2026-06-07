# Error Codes and Troubleshooting Reference

## Status

Internal hardening documentation. Not commercial-ready. Not production-ready.

## Purpose

This document explains common failure modes for the EEOAP evidence gate, the
protocol citation checker, the delivery-surface checker, the validator smoke
path, and the clean-clone install workflow.

## Scope

This document explains existing behavior. It does not add new EEOAP clauses and
does not change validator logic.

## Protocol Citation Checker

Default command:

```bash
python3 scripts/check_protocol_citations.py
```

Explicit-root command:

```bash
python3 scripts/check_protocol_citations.py \
  --manifest protocol/manifest.json \
  --clause-index protocol/clause-index.json \
  --clauses-md docs/protocol/clauses.md \
  --pr-template .github/pull_request_template.md \
  --root .
```

### `invalid_clause_id_format`

Meaning: a clause ID does not use the `EEOAP-XXX` format.

Common cause: a typo such as `BAD-001`.

Fix: use a valid `EEOAP-001` style clause identifier, or avoid adding a new
clause without a dedicated protocol-change PR.

### `missing_related_file`

Meaning: a `protocol/clause-index.json` `related_files` entry points to a path
that does not exist under `--root`.

Common cause: a stale documentation path or a moved example file.

Fix: update `related_files` to an existing path, or add the missing file if it
is in scope for the change.

### Clause mismatch

Meaning: human-readable clauses in `docs/protocol/clauses.md` and the
machine-readable index in `protocol/clause-index.json` disagree.

Fix: update both files consistently in the same protocol-change PR.

## Delivery Surface Checker

Default command:

```bash
python3 scripts/check_delivery_surface.py
```

Explicit command:

```bash
python3 scripts/check_delivery_surface.py \
  --surface packaging/commercial-delivery-surface.json \
  --root .
```

### `missing_delivery_surface_path`

Meaning: an included delivery-surface path does not exist.

Fix: remove the stale include or add the expected stable file if it belongs in
the delivery surface.

### `forbidden_delivery_surface_path`

Meaning: the delivery surface includes a path that is excluded from the
commercial delivery surface.

Common cause: a paper, submission, manuscript, media, or package artifact path
was accidentally included.

Fix: remove the forbidden path from
`packaging/commercial-delivery-surface.json`.

## Validator Smoke Path

Default command:

```bash
agent-evidence validate-profile examples/minimal-valid-evidence.json
```

Fallback command:

```bash
.venv/bin/agent-evidence validate-profile examples/minimal-valid-evidence.json
```

### `schema_violation`

Meaning: the evidence file does not conform to the expected schema or profile.

Fix: inspect missing or invalid fields in the evidence file, then rerun the
validator smoke command.

### `command not found`

Meaning: the package CLI is not installed in the current environment.

Fix: use `.venv/bin/agent-evidence` or install the package in editable mode.

## Clean Clone Install

Recommended setup:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install --upgrade pip
.venv/bin/python -m pip install -e ".[test]"
```

### `does not provide the extra 'test'`

Meaning: installed package metadata lacks the `test` optional dependency.

Current status: fixed by PR #89.

### `No module named pytest`

Meaning: test dependencies are not installed in the active environment.

Fix: install with `.[test]` or install `pytest` in the local virtual
environment.

## Claim Boundary Errors

Do not claim:

- commercial readiness;
- production readiness;
- legal compliance;
- external certification;
- standard-body adoption;
- publication acceptance;
- external validation.

## What To Report When Asking For Help

Include:

- command run;
- exit code;
- JSON output;
- repository path;
- branch name;
- whether the command ran in a clean clone;
- whether the command used `agent-evidence` or `.venv/bin/agent-evidence`;
- whether paths were adapted.
