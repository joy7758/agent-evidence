# Clean-Clone Verification Plan

## Purpose

Verify that the version 1.25 support package is reproducible from a clean
checkout before any release, tag, DOI, GitHub Release, or formal submission
decision.

## Target Future Commit

TODO after version 1.25 commit.

## Suggested Clean Clone Path

`/tmp/agent-evidence-softwarex-otel-eeoap-v1-26-clean-verify`

## Commands To Run

```bash
rm -rf /tmp/agent-evidence-softwarex-otel-eeoap-v1-26-clean-verify
git clone /tmp/agent-evidence-softwarex-otel-eeoap-rc /tmp/agent-evidence-softwarex-otel-eeoap-v1-26-clean-verify
cd /tmp/agent-evidence-softwarex-otel-eeoap-v1-26-clean-verify
git checkout TODO-v1.25-commit
git status --short
```

Then verify:

```bash
cd papers/opentelemetry-to-eeoap/softwarex_release_candidate_package_v1_25
sha256sum -c CHECKSUMS.sha256
```

Run CodeMeta JSON validation, CFF YAML validation if PyYAML is available,
validator checks for repository and copied statements, scoped pytest, and final
`git status --short`.

## Expected Outputs

- Support package directory exists.
- Checksum verification passes for all listed files.
- CodeMeta JSON validation passes.
- CFF YAML validation passes or skip reason is documented.
- Repository generated statements validate with `ok=true`, `issue_count=0`.
- Copied package generated statements validate with `ok=true`, `issue_count=0`.
- Scoped pytest passes.
- Clean checkout status remains clean after verification.

## Files To Verify

- `README.md`
- `MANIFEST.md`
- `CHECKSUMS.sha256`
- `ARTICLE/softwarex_final_declaration_draft_v1_22.md`
- `ARTICLE/softwarex_template_file_draft_v1_17.md`
- `METADATA/CITATION_OTEL_EEOAP_RELEASE_DRAFT.cff`
- `METADATA/codemeta-otel-eeoap-release-draft.json`
- `EVIDENCE/examples/opentelemetry/valid-agent-workflow-trace.json`
- `EVIDENCE/generated/valid-agent-workflow-trace-eeoap-statement.json`
- `VALIDATION/VALIDATION_SUMMARY.md`

## When To Execute

After the version 1.25 commit and before release, tag, DOI, GitHub Release, or
formal submission decisions.
