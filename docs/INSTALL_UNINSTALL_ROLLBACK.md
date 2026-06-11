# Install, Uninstall, and Rollback Guide

## Status

Stage 1 internal hardening documentation. Not commercial-ready. Not
production-ready.

## Scope

This guide describes a safe evaluation install and rollback path for EEOAP
assets. It is documentation only and does not change runtime behavior.

## Safe Install Principles

- Use a test branch only.
- Start in advisory mode.
- Avoid branch protection changes.
- Avoid secrets and production data.
- Keep the install commit separate and reviewable.
- Keep the rollback commit separate and reviewable.

## Evaluation Install Checklist

Use this checklist when evaluating EEOAP in another repository:

- create a test branch;
- copy or adapt EEOAP assets only if evaluating in another repository;
- add PR template guidance;
- add workflow checks only in advisory mode;
- run local commands from `docs/CUSTOMER_QUICKSTART.md`;
- open a draft PR if review is needed.

## Uninstall / Rollback Checklist

Use this checklist to remove EEOAP-specific evaluation assets:

- remove EEOAP-specific protocol files;
- remove EEOAP-specific workflow files;
- remove EEOAP-specific PR template sections;
- remove EEOAP-specific Skill Pack directory;
- remove EEOAP-specific examples;
- remove EEOAP-specific docs;
- confirm no required check points to a removed workflow;
- run normal repository tests;
- keep rollback reviewable.

## Branch Protection Note

- Do not enable branch protection requirements during the first evaluation.
- If enforce mode is enabled later, disable required checks before removing
  the workflow.
- Never change branch protection without maintainer approval.

## What To Keep

If useful, keep:

- anonymized feedback;
- command pass/fail notes;
- clean-clone notes;
- non-sensitive environment notes.

Do not keep secrets, customer data, private evidence payloads, or production
logs.

## Rollback Success Criteria

Rollback is complete when:

- normal repository tests pass;
- no EEOAP workflow is required;
- no broken references remain in `AGENTS.md` or the PR template;
- the maintainer confirms the normal workflow is restored.

## Non-Claims

This guide does not claim certification, legal compliance, standardization,
commercial readiness, production readiness, external validation, submission,
acceptance, or publication.
