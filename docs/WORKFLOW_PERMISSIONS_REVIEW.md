# Workflow Permissions Review

## Status

Stage 1 internal hardening review. Not commercial-ready. Not production-ready.

## Purpose

Review GitHub Actions workflow permissions, trigger surfaces, and
required-check behavior for the EEOAP repository.

## Scope

This document records a review of current workflows. It does not change
workflow behavior and does not change branch protection.

## Review Basis

GitHub Actions supports the `permissions` key to adjust `GITHUB_TOKEN` access
at the workflow or job level. The review uses least-required-access as the
working principle: validation-only workflows should prefer read-only repository
access, and write permissions should be documented and isolated.

If a workflow declares specific `permissions`, unspecified permissions are
treated as `none`. This makes explicit minimal permissions preferable for
validation-only workflows.

## Workflow Inventory

Branch protection required checks observed during this review:

- `eeoap-protocol-gate`
- `validate-agent-native-metadata`
- `Lint and Test (Python 3.11)`
- `Lint and Test (Python 3.12)`
- `Lint and Test (Python 3.13)`

`Check documentation links` is a CI-relevant check in the review scope, but it
was not listed by the branch protection `required_status_checks` API response
at review time.

| Workflow file | Workflow name | Trigger events | Required check | Top-level permissions | Job-level permissions | Third-party actions | Secrets used | Write permissions | Classification | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `.github/workflows/ci.yml` | CI | `push` to `main`, `pull_request` | Yes, via Python matrix jobs | Not declared | Not declared | No non-GitHub third-party action observed | No | No explicit write permission | `WORKFLOW_PERMISSION_WARNING` | Validation behavior appears read-only, but explicit `contents: read` is not declared. Official actions are tag-pinned rather than full-SHA-pinned. |
| `.github/workflows/docs-link-check.yml` | Docs Link Check | `push` to `main`, `pull_request`, `workflow_dispatch` | No, not listed by branch protection API | `contents: read` | Not declared | `lycheeverse/lychee-action@v2` | No | No | `WORKFLOW_PERMISSION_WARNING` | Permission posture is read-only. Warning is due to tag-pinned third-party action. |
| `.github/workflows/eeoap-protocol-gate.yml` | EEOAP Protocol Gate | `pull_request`, `push` to `main` | Yes | `contents: read` | Not declared | No non-GitHub third-party action observed | No | No | `WORKFLOW_PERMISSION_OK` | Required validation gate with explicit read-only permissions. Official actions are tag-pinned. |
| `.github/workflows/pip-audit.yml` | Dependency Audit | `push` to `main`, `pull_request` | No | `contents: read` | Not declared | No non-GitHub third-party action observed | No | No | `WORKFLOW_PERMISSION_OK` | Read-only audit workflow. Official actions are tag-pinned. |
| `.github/workflows/prototype-check.yml` | Prototype Check | `push` to `main` and `feat/openai-agents-exporter`, `pull_request` | No | Not declared | Not declared | No non-GitHub third-party action observed | No | No explicit write permission | `WORKFLOW_PERMISSION_WARNING` | Validation behavior appears read-only, but explicit `contents: read` is not declared. Official actions are tag-pinned. |
| `.github/workflows/sbom.yml` | SBOM | `push` to `main`, `pull_request`, `workflow_dispatch` | No | `contents: read` | Not declared | `anchore/sbom-action@v0` | No | No explicit repository write permission | `WORKFLOW_PERMISSION_WARNING` | Read-only repository permission, but artifact upload and tag-pinned third-party action should remain reviewed. |
| `.github/workflows/validate-agent-native-metadata.yml` | Validate agent-native metadata | `push`, `pull_request` | Yes | Not declared | Not declared | No non-GitHub third-party action observed | No | No explicit write permission | `WORKFLOW_PERMISSION_WARNING` | Required metadata validation appears read-only, but explicit `contents: read` is not declared. Official actions are tag-pinned. |
| `.github/workflows/weekly-agentic-email-notification.yml` | Weekly Agentic Compatibility Email Notification | `workflow_dispatch`, `schedule`, selected `push` paths | No | `contents: read`, `issues: write` | Not declared | No non-GitHub third-party action observed | No explicit `secrets.*`; uses `github.token` as `GH_TOKEN` | Yes, `issues: write` | `WORKFLOW_PERMISSION_WARNING` | Write permission appears scoped to issue creation and is not triggered by `pull_request`. Keep separate from PR validation gates. |

## Permission Findings

- Explicit read-only permissions are already present in:
  - `.github/workflows/docs-link-check.yml`;
  - `.github/workflows/eeoap-protocol-gate.yml`;
  - `.github/workflows/pip-audit.yml`;
  - `.github/workflows/sbom.yml`.
- Missing explicit permissions were observed in:
  - `.github/workflows/ci.yml`;
  - `.github/workflows/prototype-check.yml`;
  - `.github/workflows/validate-agent-native-metadata.yml`.
- One workflow intentionally uses write permission:
  - `.github/workflows/weekly-agentic-email-notification.yml` uses
    `issues: write` to create reminder issues.
- No `permissions: write-all` setting was observed.
- No `pull_request_target` trigger was observed.
- No explicit `secrets.*` reference was observed in PR-triggered workflows.
- No workflow was observed exposing repository write permissions to untrusted
  pull request code.

## Required Checks

Branch protection currently reports these required checks:

- `eeoap-protocol-gate`
- `validate-agent-native-metadata`
- `Lint and Test (Python 3.11)`
- `Lint and Test (Python 3.12)`
- `Lint and Test (Python 3.13)`

The documentation link check remains part of CI review evidence, but it was not
listed by the branch protection required-status-check API result at review time.

## Risk Notes

### Over-permission Risk

Validation-only workflows without explicit permissions should be reviewed for a
future permission-hardening PR. The expected baseline for those workflows is:

```yaml
permissions:
  contents: read
```

### `pull_request_target` Risk

No `pull_request_target` trigger was observed. This is important because
`pull_request_target` can grant broader token access than ordinary
`pull_request` workflows and requires a separate review before it is used.

### Third-party Action Pinning Risk

Some workflows use non-GitHub third-party actions pinned by tags:

- `lycheeverse/lychee-action@v2`
- `anchore/sbom-action@v0`

Tag pinning is common, but full commit-SHA pinning would be stronger for a
future hardening pass.

### Secrets Exposure Risk

No explicit `secrets.*` usage was observed in the reviewed workflows. The
weekly notification workflow uses `github.token` through `GH_TOKEN`, but it is
not triggered by `pull_request` and is scoped to issue creation.

### Artifact Upload Risk

The SBOM workflow uploads an artifact through `anchore/sbom-action@v0`. This is
not a repository mutation, but artifact-producing workflows should remain
separate from required PR validation gates unless explicitly reviewed.

### Untrusted PR Text or Comment Input Risk

No workflow was observed processing PR body text, issue text, or comment text
as executable input.

## Recommendations

Overall review classification:

`WORKFLOW_PERMISSION_REVIEW_PASS_WITH_WARNINGS`

Recommended future PRs:

- Add explicit `permissions: contents: read` to validation-only workflows that
  currently omit permissions.
- Review whether third-party actions should be pinned by full commit SHA.
- Keep issue-creating or artifact-producing workflows outside the required PR
  validation gate unless separately approved.

No blocking permission issue was identified in this review.

## Non-Claims

This review does not claim:

- commercial readiness;
- production readiness;
- legal compliance;
- external certification;
- standardization;
- external validation;
- security certification.
