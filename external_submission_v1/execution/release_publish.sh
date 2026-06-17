#!/usr/bin/env bash
set -euo pipefail

AEP_REPO="${AEP_REPO:-joy7758/agent-evidence}"
AEP_RELEASE_TAG="${AEP_RELEASE_TAG:-origin-aep-v0.1-candidate}"
AEP_RELEASE_TITLE="${AEP_RELEASE_TITLE:-Origin AEP v0.1 Candidate}"
AEP_PUBLIC_REPO_URL="${AEP_PUBLIC_REPO_URL:-https://github.com/joy7758/agent-evidence}"
ISSUE_TITLE="External technical review request: Origin AEP v0.1 candidate"
RESULT="external_submission_v1/execution/PUBLIC_RELEASE_RESULT.md"

run_local_validation() {
  python3 external_submission_v1/publish_gate/PLACEHOLDER_SCAN.py
  python3 external_submission_v1/publish_gate/CLAIM_BOUNDARY_SCAN.py
  python3 external_submission_v1/publish_gate/PATH_REFERENCE_SCAN.py
  python3 external_submission_v1/publish_gate/RELEASE_READINESS_SUMMARY.py
  python3 external_submission_v1/build_submission_summary.py
  python3 spec_release_v0_1/validator/spec_validator.py spec_release_v0_1/examples/github_pr_example.json
  make demo
  git diff --check
  if [ -x .venv/bin/python ]; then
    .venv/bin/python -m unittest discover -s tests
    .venv/bin/python -m pytest -q
    .venv/bin/python spec_release_v0_1/validator/spec_validator.py spec_release_v0_1/examples/github_pr_example.json
    .venv/bin/agent-evidence validate-profile examples/minimal-valid-evidence.json
  fi
}

run_local_validation

if [ "${I_APPROVE_EXTERNAL_PUBLISH:-}" != "YES" ]; then
  echo "I_APPROVE_EXTERNAL_PUBLISH is not YES; no external action performed."
  exit 0
fi

command -v gh >/dev/null
gh auth status
git status --short
if [ -n "$(git status --porcelain -- Makefile spec_release_v0_1 external_submission_v1 tests/test_external_submission_v1.py .gitignore)" ]; then
  git add Makefile spec_release_v0_1 external_submission_v1 tests/test_external_submission_v1.py .gitignore
  git commit -m "Prepare Origin AEP external submission package v1" || true
fi
git branch -M main
git push -u origin main
git tag -a "$AEP_RELEASE_TAG" -m "$AEP_RELEASE_TITLE" || true
git push origin "$AEP_RELEASE_TAG"
gh release view "$AEP_RELEASE_TAG" -R "$AEP_REPO" >/dev/null 2>&1 || gh release create "$AEP_RELEASE_TAG" -R "$AEP_REPO" --title "$AEP_RELEASE_TITLE" --notes-file external_submission_v1/github_release/RELEASE_NOTES_v0_1.md
RELEASE_URL="$(gh release view "$AEP_RELEASE_TAG" -R "$AEP_REPO" --json url --jq .url 2>/dev/null || true)"
ISSUE_URL="$(gh issue list -R "$AEP_REPO" --search "$ISSUE_TITLE in:title" --json url --jq '.[0].url // empty' 2>/dev/null || true)"
if [ -z "$ISSUE_URL" ]; then
  ISSUE_URL="$(gh issue create -R "$AEP_REPO" --title "$ISSUE_TITLE" --body-file external_submission_v1/github_release/GITHUB_DISCUSSION_POST.md 2>/dev/null || true)"
fi
if [ "${I_APPROVE_GITHUB_DISCUSSION:-}" = "YES" ]; then
  echo "GitHub Discussion approval present, but discussion creation is not automated by this script."
fi
mkdir -p external_submission_v1/execution
{
  echo "# Public Release Result"
  echo
  echo "- timestamp_utc: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
  echo "- repository: $AEP_PUBLIC_REPO_URL"
  echo "- tag: $AEP_RELEASE_TAG"
  echo "- commit: $(git rev-parse HEAD)"
  echo "- release_url: ${RELEASE_URL:-pending}"
  echo "- review_issue_url: ${ISSUE_URL:-pending}"
  echo "- validation_summary: local gates passed before external action"
  echo "- arxiv_submission: not submitted"
  echo "- emails_sent_by_this_script: no"
} > "$RESULT"
cat "$RESULT"
