# Clean-Clone Verification Plan

## Purpose

Verify that a clean clone of the release-candidate branch can inspect the
version 1.15 support package, run scoped tests, validate both generated EEOAP
statements, and verify package checksums.

## Target Future Commit

TODO: set to the version 1.15 commit after this package is committed.

## Suggested Clean Clone Path

`/tmp/agent-evidence-otel-eeoap-v1-15-clean-verify`

## Commands

Run from the release-candidate repository after version 1.15 commit:

```bash
rm -rf /tmp/agent-evidence-otel-eeoap-v1-15-clean-verify
git clone "$(pwd)" /tmp/agent-evidence-otel-eeoap-v1-15-clean-verify
cd /tmp/agent-evidence-otel-eeoap-v1-15-clean-verify
git checkout <v1.15-commit>
/Users/zhangbin/GitHub/agent-evidence/.venv/bin/python -m pytest tests/test_opentelemetry_to_eeoap_adapter.py -q
/Users/zhangbin/GitHub/agent-evidence/.venv/bin/agent-evidence validate-profile generated/valid-agent-trace-eeoap-statement.json
/Users/zhangbin/GitHub/agent-evidence/.venv/bin/agent-evidence validate-profile generated/valid-agent-workflow-trace-eeoap-statement.json
cd papers/opentelemetry-to-eeoap/softwarex_release_candidate_package_v1_15
sha256sum -c CHECKSUMS.sha256
git status --short
```

If `sha256sum` is unavailable:

```bash
shasum -a 256 -c CHECKSUMS.sha256
```

## Expected Outputs

- Scoped pytest: `8 passed`.
- First generated statement validator result: `ok=true`, `issue_count=0`.
- Second generated statement validator result: `ok=true`, `issue_count=0`.
- Checksum verification: all listed files OK.
- Git status: clean.

## Files to Verify

- `ARTICLE/softwarex_template_style_draft_v1_14.md`
- `METADATA/`
- `EVIDENCE/examples/opentelemetry/`
- `EVIDENCE/generated/`
- `VALIDATION/`
- `CHECKSUMS.sha256`

## When to Execute

After the version 1.15 package commit and before any formal release,
archive, GitHub Release, tag push, DOI creation, or SoftwareX submission.
