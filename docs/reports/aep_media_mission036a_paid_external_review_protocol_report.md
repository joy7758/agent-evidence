# Mission 036A Paid External Review Protocol Report

Date: 2026-06-01

## 1. Mission Summary

Mission 036A created a safe protocol for optional paid external review during
the AEP-Media JOSS waiting period. The protocol is designed to attract real
reproduction feedback, documentation criticism, and small public contributions
without manufacturing fake development history.

No implementation code was changed. No JOSS submission was performed.

## 2. Current Readiness

- JOSS technical readiness: READY.
- JOSS submission readiness: WAITING FOR PUBLIC HISTORY.
- Earliest honest JOSS submission date: 2026-09-16 or later.

## 3. Files Created

- `docs/paper/joss/maintenance/paid-review/README.md`
- `docs/paper/joss/maintenance/paid-review/task_A_reproducibility_review.md`
- `docs/paper/joss/maintenance/paid-review/task_B_adapter_boundary_doc_review.md`
- `docs/paper/joss/maintenance/paid-review/task_C_mobile_fixture_regression_pr.md`
- `docs/paper/joss/maintenance/paid-review/contributor_credit_policy.md`
- `docs/paper/joss/maintenance/paid-review/payment_and_disclosure_policy.md`
- `docs/paper/joss/maintenance/paid-review/reviewer_onboarding_message.md`
- `docs/paper/joss/maintenance/paid-review/acceptance_checklist.md`

## 4. Recommended Paid Tasks

Recommended first paid task: Task A, reproducibility review.

Reason: a fresh-clone reproduction issue is the most valuable early signal for
JOSS readiness because it tests installation, CLI discoverability,
documentation clarity, and the mobile-video walkthrough without requiring
feature changes.

Suggested pilot:

- two external reviewers;
- one task per reviewer;
- seven-day window;
- one public issue or PR per task;
- fixed small budget or capped hours.

## 5. Risks

Main risks:

- paid work could appear like artificial activity if tasks are vague;
- reviewers could submit generic praise instead of actionable feedback;
- contributors could accidentally broaden the claim boundary;
- private or large media artifacts could be uploaded;
- authorship expectations could become unclear.

Mitigation:

- use written task statements;
- require public issues or PRs;
- require exact commands and environment details;
- use small synthetic fixtures only;
- disclose paid external review where relevant;
- use the contributor credit policy before promising acknowledgements or
  authorship.

## 6. Ethics and Disclosure Handling

Payment compensates time spent on review or contribution work. It must not buy
positive conclusions, stars, fake issues, fake PRs, citation, authorship, or a
publication outcome.

Paid status should be disclosed in issues or PRs where relevant. Reviewers
should declare conflicts of interest if they exist.

## 7. Whether to Proceed

Proceed with a small pilot only.

Do not start a broad paid-campaign or marketing-style activity. The first round
should be limited to real reproduction and narrow documentation/test review.

## 8. Validation

- `git diff --check`: PASS.
- Red-line scan: PASS.

Red-line result:

- no invented DOI;
- no paid acceptance or publication promise;
- no private-data instruction;
- no excluded workspace reference;
- restricted legal, forensic, timestamping, PTP, PRFT, C2PA,
  chain-of-custody, and production-deployment terms appear only in explicit
  do-not-claim or boundary contexts.

## 9. Next Mission Recommendation

Recommended next mission:

Mission 036A-1: open one real public GitHub issue for Task A only after a real
external reviewer is identified and agrees to perform the work.

Alternative:

Mission 037: create a clean JOSS maintenance branch and commit/push only the
coherent M34-M36A JOSS readiness files.
