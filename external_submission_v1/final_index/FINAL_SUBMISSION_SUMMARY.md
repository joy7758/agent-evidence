# Final Submission Summary

Origin AEP v0.1 has a local external submission preparation kit under `external_submission_v1/`. The package is ready for local gate checks and human publication review, not external action.

## External execution status

- Release script path: `external_submission_v1/execution/release_publish.sh`
- Verified channels path: `external_submission_v1/execution/VERIFIED_CHANNELS.md`
- Verified public contacts path:
  `external_submission_v1/execution/VERIFIED_PUBLIC_CONTACTS.md`
- Contact source summary path:
  `external_submission_v1/execution/CONTACT_SOURCE_SUMMARY.md`
- Outreach script path: `external_submission_v1/execution/send_verified_outreach.py`
- Private recipients file requirement: `external_submission_v1/execution/private_outreach_recipients.json` must be created manually and must contain only user-verified team emails.
- Manual approval gates: `I_APPROVE_EXTERNAL_PUBLISH=YES` for publication and `I_APPROVE_EMAIL_SEND=YES` for email sending.

## Verified public contact findings

- No general technical email was found for Cursor Origin, Graphite, or MCP.
- Cursor `security@cursor.com` is limited to security/audit architecture
  feedback and requires explicit local send gates.
- Cursor `security-reports@cursor.com` is vulnerability-only.
- Cursor `hi@cursor.com` is support/privacy context, not protocol outreach.
- Graphite security emails are limited to security, audit, privacy, or policy
  context and are not generic outreach channels.
- Official public channels remain primary: Cursor Forum/Origin waitlist,
  Graphite Community Slack/public channels, and MCP GitHub Discussions/SEP
  route.

The release decision remains `PENDING_HUMAN_APPROVAL`. No external action has been performed.
