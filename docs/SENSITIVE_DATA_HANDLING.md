# Sensitive Data Handling

## Status

Stage 1 internal hardening documentation. Not commercial-ready. Not
production-ready.

## Purpose

This note defines what data must not be used when evaluating EEOAP.

## Do Not Use

Do not use:

- secrets;
- tokens;
- private keys;
- credentials;
- customer data;
- production logs;
- private source code not intended for review;
- sensitive evidence payloads;
- unpublished manuscript, submission, or reviewer materials;
- private route-control notes.

## Use Synthetic Examples

Use:

- synthetic evidence examples;
- test branch data;
- minimal demonstration payloads;
- redacted command output.

## Evidence Output Guidance

- Prefer hashes or references over raw sensitive values.
- Avoid uploading candidate artifacts to unrelated repositories.
- Do not include customer data in issue reports.
- Do not publish candidate names without permission.
- Do not paste secrets, tokens, private keys, or credentials into PRs,
  issues, logs, or chat.

## Reporting Problems

When reporting a problem, include:

- command;
- exit code;
- redacted output;
- environment;
- branch;
- whether a clean clone was used.

## Non-Claims

This note does not establish legal compliance, certification, production
security assurance, commercial readiness, production readiness, external
validation, submission, acceptance, or publication.
