# Advisory Mode vs Enforce Mode

## Status

Stage 1 internal hardening documentation. Not commercial-ready. Not
production-ready.

## Purpose

Define how EEOAP checks should be used in advisory mode and enforce mode.

## Advisory Mode

Advisory mode means:

- checks may run and report findings;
- results help maintainers understand evidence gaps;
- failures may be reviewed manually;
- adoption does not block all development by default;
- suitable for early trials and internal dogfood.

Advisory mode can run the same commands used by enforce mode, but the outcome is
guidance rather than a merge blocker.

## Enforce Mode

Enforce mode means:

- checks are required before merge;
- branch protection may require specific checks;
- failure blocks merge until fixed or explicitly waived;
- suitable only after internal hardening and maintainer approval.

Enforce mode should be treated as a repository-governance decision, not as a
claim of external validation, compliance, certification, or production
readiness.

## Current Repository State

- `agent-evidence` main uses required checks for its own repository governance.
- External pilot is on hold.
- External candidate repositories should start in advisory mode only.
- Enforce mode is not recommended for a first external pilot.

## When To Use Advisory Mode

Use advisory mode when:

- testing installation friction;
- onboarding a new repository;
- collecting feedback;
- validating checker behavior;
- running a first pilot on a test branch;
- working with a docs-only repository;
- evaluating CI maturity before branch protection changes.

Expected advisory-mode commands:

```bash
python3 -m json.tool protocol/manifest.json
python3 -m json.tool protocol/clause-index.json
python3 scripts/check_protocol_citations.py
python3 scripts/check_delivery_surface.py
agent-evidence validate-profile examples/minimal-valid-evidence.json
```

If a repository does not install the CLI globally, use the repository-local
virtual-environment path instead:

```bash
.venv/bin/agent-evidence validate-profile examples/minimal-valid-evidence.json
```

Advisory-mode PR summaries should record:

- which EEOAP clauses were touched or cited;
- which checks were run;
- whether failures were expected, unexpected, or waived for review;
- known false positives;
- rollback or uninstall notes if the gate was installed temporarily.

## When To Use Enforce Mode

Use enforce mode only when:

- repository maintainer explicitly agrees;
- rollback path is tested;
- false positive rate is acceptable;
- branch protection implications are understood;
- support boundary is clear;
- install and uninstall steps are documented;
- maintainers understand that EEOAP checks do not create external certification
  or compliance status.

Typical enforce-mode checks may include:

- protocol citation checker;
- validator smoke path;
- PR evidence template completion;
- documentation link check when it is stable enough for required status;
- repository-specific tests that are already stable.

## Never Do

- do not enable enforce mode in a candidate repository without maintainer
  approval;
- do not require branch protection in a first external pilot;
- do not use enforce mode to imply certification or compliance;
- do not block unrelated development unexpectedly;
- do not treat a passing gate as publication, acceptance, standardization, or
  external validation evidence.

## Decision Table

| Situation | Recommended mode | Reason | Required approval |
| --- | --- | --- | --- |
| First install in a candidate repository | Advisory | Measures friction without blocking maintainers | Candidate maintainer approval for trial scope |
| Internal dogfood on a test branch | Advisory | Allows failure analysis and rollback testing | Repository owner approval |
| Mature repository with stable checks and clear support boundary | Enforce | Required checks can protect evidence quality | Maintainer approval plus branch-protection review |
| Docs-only repository with unknown CI maturity | Advisory | Avoids blocking unrelated documentation work | Maintainer approval for advisory reporting |
| Temporary compatibility experiment | Advisory | Results are evidence for planning, not a merge gate | Experiment owner approval |
| Repository with sensitive production evidence | Neither by default | Requires a separate data-handling and security review | Explicit security and maintainer approval |

## Current Recommendation

Keep external candidates in advisory mode during any future controlled pilot.
Do not enable enforce mode for the first external pilot.

## Non-Claims

No commercial-ready, production-ready, certification, standardization, legal
compliance, or external-validation claim.
