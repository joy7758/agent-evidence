# Paid External Review Acceptance Checklist

Use this checklist before accepting a paid external review issue or PR.

## Required Evidence

- [ ] The task is linked to a written task description.
- [ ] The deliverable is a public GitHub issue or PR.
- [ ] Exact commands are included where reproduction is relevant.
- [ ] Environment information is included where reproduction is relevant.
- [ ] Feedback is actionable and specific.
- [ ] Screenshots, if included, contain no private data.
- [ ] No private media, real evidence files, confidential logs, or large
      binaries are included.
- [ ] The work does not introduce unsupported legal, forensic, timestamping,
      PTP, PRFT, C2PA, chain-of-custody, or production-deployment claims.
- [ ] The work does not contain generic praise-only content.
- [ ] The work does not include unrelated rewrites or route changes.

## PR-Specific Checks

- [ ] The PR explains the purpose of the change.
- [ ] Tests or documentation were updated where appropriate.
- [ ] `git diff --check` passes.
- [ ] Relevant pytest command output is included if tests changed.
- [ ] CI passes when available.
- [ ] No validator/schema/adapter/evaluation semantic change is hidden inside
      the PR.

## Disclosure

- [ ] Paid-review or paid-contribution status is disclosed where relevant.
- [ ] Any reviewer conflict of interest is declared where relevant.
- [ ] No authorship, citation, or publication outcome is promised.
