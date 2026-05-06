# Email Notification Protocol

## Purpose

This protocol sends Chinese email notifications through GitHub Issues and the
maintainer's GitHub notification settings.

It is a reminder and decision prompt for the weekly agentic compatibility
process. It uses no direct SMTP email, is not a report generator, has no
automatic PR behavior, and has no automatic release behavior.

In short: no automatic PR, no automatic release, and no automatic promotion.

## What Is Pushed

The workflow can create:

- a weekly reminder issue
- a weekly report issue when a report file is pushed
- the report path, if a report exists
- a Chinese human decision checklist
- No-Go reminders for automation, promotion, and claims boundaries

## What Is Not Pushed

The notification workflow must not push:

- secrets
- private data
- direct SMTP email
- automatic pull requests
- automatic PR
- automatic repository changes
- automatic releases
- automatic release
- promotional messages
- automatic promotion
- fake adoption or adopter claims

## How Email Delivery Works

The workflow creates a GitHub Issue assigned to `joy7758` and mentions
`@joy7758` in the issue body. GitHub sends email only if the maintainer has
GitHub email notifications enabled for issue participation or assignment.

Email delivery is controlled by GitHub account and repository notification
settings. The repository does not store email passwords, SMTP tokens, or
third-party email service credentials.

## Human Decision Gate

The issue is only a decision prompt. It does not approve work by itself.

Any accepted action requires a separate reviewed pull request. The issue may
record a decision such as `watch`, `docs-only candidate`, `metadata-only
candidate`, `test-only candidate`, or `reject / no-go`, but it must not make
repository changes.

## No-Go

The notification workflow must not:

- perform automatic promotion
- create fake adoption signals
- ask anyone to star, follow, fork, or promote the project
- make AI Act / legal / compliance claims
- change OpenAPI, MCP, schema, or core behavior
- publish a release
- open a pull request automatically

## Manual Fallback

If the workflow is unavailable, create a reminder issue manually:

```bash
gh issue create \
  --title "【Agentic 周报提醒】YYYY-MM-DD 智能体兼容性情报" \
  --body-file <body.md> \
  --assignee joy7758
```
