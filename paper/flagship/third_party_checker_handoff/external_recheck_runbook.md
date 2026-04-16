# External Recheck Runbook

## Purpose

This file is a runbook for a future external re-check of the B1 line.

Its purpose is limited: give an external checker implementation or external reviewer a
minimal execution guide for re-checking the current handoff surface without changing
canonical B1 or supplementary boundaries.

Canonical B1 remains `1 valid / 3 invalid / 1 demo`.

## Required inputs

Use `checker_input_manifest.json` as the authoritative input list.

- `canonical_b1` defines the minimum canonical inputs that should be checked
- `supplementary` defines optional supplementary inputs that may be checked without
  changing canonical B1 counts

## Minimum checks expected

Use `checker_contract.md` as the minimum contract.

At minimum, a future external re-check should be able to cover:

- schema validity
- unresolved output refs
- broken evidence-policy refs

## Expected output file shape

The expected output shape is defined by `external_recheck_result_template.json`.

At minimum, the output should record:

- who ran the re-check
- when it was run
- which checker name and version were used
- which inputs were checked
- what per-input results were returned
- any notes needed to interpret the run
- a top-level run status

## Status note

This runbook is for a future external re-check only.

There is no external result included yet.

Status shorthand: no external result is included yet.
