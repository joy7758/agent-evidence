# Paid External Review Protocol for AEP-Media

Date: 2026-06-01

## Purpose

This protocol defines how AEP-Media may use small paid external review tasks
during the JOSS waiting period. The purpose is to obtain real reproduction
notes, real criticism, and useful open-source contributions. It is not for
artificial popularity, synthetic activity, generic praise, or manufactured
history.

AEP-Media's current JOSS state remains:

- JOSS technical readiness: READY.
- JOSS submission readiness: WAITING FOR PUBLIC HISTORY.
- Earliest honest JOSS submission date: 2026-09-16 or later.

## Allowed Work

Paid work should be limited to focused, auditable tasks:

- reproducing README and mobile-video walkthrough commands from a fresh clone;
- identifying unclear setup, documentation, or error reporting;
- reviewing adapter-boundary documentation for unsupported-claim risk;
- submitting small documentation PRs;
- submitting small regression-test PRs for existing fixture behavior.

All substantive work should happen through public GitHub issues or pull
requests. Reviewers should include exact commands, environment details, and
specific observations rather than high-level praise.

## Disallowed Work

Do not pay for:

- stars, followers, or popularity signals;
- praise-only comments;
- meaningless issues;
- fake pull requests;
- positive conclusions;
- publication or acceptance promises;
- citation promises;
- private-media uploads;
- broad legal, forensic, timestamping, PRFT, PTP, C2PA, chain-of-custody, or
  production-deployment claims.

## Data and Fixture Rules

Contributors must use only small synthetic fixtures already in the repository
or tiny new synthetic fixtures proposed in a PR. They must not upload private
media, real incident footage, medical data, private device logs, confidential
evidence files, or large binaries.

If a new fixture is proposed, it must remain small, synthetic, documented, and
compatible with the existing AEP-Media claim boundary.

## Authorship and Credit

Payment does not create authorship. Code and documentation contributions are
credited through the public Git commit and PR history. Substantial review
feedback may be acknowledged where appropriate. Authorship requires a
substantial intellectual or software contribution, explicit agreement, and
responsibility for the work.

## Recommended First Round

Use a small pilot:

- two external reviewers;
- one task per reviewer;
- seven-day window;
- one public issue or PR per task;
- no broad retainer or open-ended consulting arrangement.

Recommended first task: Task A, reproducibility review from a fresh clone.

## References for Policy Alignment

- JOSS submission requirements: https://joss.readthedocs.io/en/latest/submitting.html
- JOSS review checklist: https://joss.readthedocs.io/en/latest/review_checklist.html
- GitHub Issues documentation: https://docs.github.com/en/issues/tracking-your-work-with-issues/learning-about-issues/about-issues
