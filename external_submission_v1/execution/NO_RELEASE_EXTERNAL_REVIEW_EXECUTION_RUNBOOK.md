# No-Release External Review Execution Runbook

This runbook is blocked until the human maintainer updates `external_submission_v1/publish_gate/NO_RELEASE_EXTERNAL_REVIEW_APPROVAL.md` with the exact approval phrase and completes the checklist in `external_submission_v1/publish_gate/RELEASE_DECISION_RECORD.md`.

## Scope

Allowed only after approval:

- Create one GitHub public technical review issue.
- Send one Cursor security/audit architecture feedback email to `security@cursor.com`.

Still forbidden:

- tag
- GitHub release
- `external_submission_v1/execution/release_publish.sh`
- arXiv submission
- GitHub Discussion
- Graphite email
- MCP email
- guessed or personal email

## Later execution command

This command is intentionally blocked until the approval record is completed by a human maintainer.

```bash
cd /Users/zhangbin/GitHub/agent-evidence && \
I_APPROVE_NO_RELEASE_PUBLIC_REVIEW=YES \
I_APPROVE_EMAIL_SEND=YES \
AEP_ALLOW_CURSOR_SECURITY_RESEARCH_EMAIL=YES \
AEP_REPO="joy7758/agent-evidence" \
AEP_PUBLIC_REPO_URL="https://github.com/joy7758/agent-evidence" \
AEP_MAIN_COMMIT="e82723b3b607a81b3f1accc682807ca2f5f63320" \
python3 external_submission_v1/publish_gate/PLACEHOLDER_SCAN.py && \
python3 external_submission_v1/publish_gate/CLAIM_BOUNDARY_SCAN.py && \
python3 external_submission_v1/publish_gate/PATH_REFERENCE_SCAN.py && \
python3 external_submission_v1/build_submission_summary.py && \
python3 spec_release_v0_1/validator/spec_validator.py spec_release_v0_1/examples/github_pr_example.json && \
make demo && \
python3 scripts/check_protocol_citations.py
```

After those checks pass, the later run may create the single public review issue and then create a private recipient file containing only `security@cursor.com` with template `cursor_security_audit_feedback_email.md`. The later run must stop without alternate channels if `sendmail` fails.

## Required stop conditions

Stop before any external action if:

- the approval phrase is absent;
- any approval checkbox remains unchecked;
- any local gate fails;
- a tag or release would be created;
- more than one email recipient is present;
- the recipient is not exactly `security@cursor.com`;
- the template is not exactly `cursor_security_audit_feedback_email.md`;
- any Graphite, MCP, guessed, personal, or vulnerability-report address is present.
