# Clean-Clone Verification

## Verification Target

- Target commit: `a03f6455d87bcf67987c7ba1e4297a224de70976`
- Target branch line: `softwarex-otel-eeoap-release-candidate`
- Support package:
  `papers/opentelemetry-to-eeoap/softwarex_release_candidate_package_v1_25/`

## Verification Method

A clean clone was created outside the original dirty worktree and outside the
existing release-candidate worktree:

```bash
rm -rf /tmp/agent-evidence-softwarex-otel-eeoap-v1-26-clean-verify
git clone /tmp/agent-evidence-softwarex-otel-eeoap-rc /tmp/agent-evidence-softwarex-otel-eeoap-v1-26-clean-verify
cd /tmp/agent-evidence-softwarex-otel-eeoap-v1-26-clean-verify
git checkout a03f6455d87bcf67987c7ba1e4297a224de70976
```

The checkout entered detached HEAD state at the target commit.

## Checkout Status Before Verification

- Clean verification path:
  `/tmp/agent-evidence-softwarex-otel-eeoap-v1-26-clean-verify`
- Checked-out commit:
  `a03f6455d87bcf67987c7ba1e4297a224de70976`
- Branch state: detached HEAD
- `git status --short` before verification: empty output
- Tag list available in the clean clone, including `eeoap-v0.1-artifact`,
  `aep-v0.1-artifact`, and existing repository tags.

## Support Package Existence Check

The support package directory exists. The requested key files are present:

- `README.md`
- `MANIFEST.md`
- `CHECKSUMS.sha256`
- `ARTICLE/softwarex_final_declaration_draft_v1_22.md`
- `ARTICLE/softwarex_template_file_draft_v1_17.md`
- `METADATA/CITATION_OTEL_EEOAP_RELEASE_DRAFT.cff`
- `METADATA/codemeta-otel-eeoap-release-draft.json`
- `EVIDENCE/examples/opentelemetry/valid-agent-trace.json`
- `EVIDENCE/examples/opentelemetry/valid-agent-workflow-trace.json`
- `EVIDENCE/generated/valid-agent-trace-eeoap-statement.json`
- `EVIDENCE/generated/valid-agent-workflow-trace-eeoap-statement.json`
- `VALIDATION/VALIDATION_SUMMARY.md`
- `VALIDATION/VALIDATION_COMMANDS.md`

Observed support package file count: 35 files.

## Checksum Result

Command:

```bash
cd papers/opentelemetry-to-eeoap/softwarex_release_candidate_package_v1_25
sha256sum -c CHECKSUMS.sha256
```

Result: all 34 listed files passed SHA-256 verification.

## CodeMeta JSON Validation

Command:

```bash
python -m json.tool papers/opentelemetry-to-eeoap/softwarex_release_candidate_package_v1_25/METADATA/codemeta-otel-eeoap-release-draft.json > /tmp/codemeta-otel-eeoap-v1-26.validated.json
```

Result: passed. The validated output was written outside the repository under
`/tmp`.

## CFF YAML Validation

Command:

```bash
python - <<'PY'
from pathlib import Path
try:
    import yaml
except Exception as exc:
    print(f"CFF YAML validation skipped: {exc}")
    raise SystemExit(0)

path = Path("papers/opentelemetry-to-eeoap/softwarex_release_candidate_package_v1_25/METADATA/CITATION_OTEL_EEOAP_RELEASE_DRAFT.cff")
with path.open("r", encoding="utf-8") as f:
    yaml.safe_load(f)
print("CFF YAML validation passed")
PY
```

Result: skipped. Exact reason: `No module named 'yaml'`.

No PyYAML dependency was installed.

## Scoped Pytest Result

Command:

```bash
/Users/zhangbin/GitHub/agent-evidence/.venv/bin/python -m pytest tests/test_opentelemetry_to_eeoap_adapter.py -q
```

Result: `8 passed in 1.94s`.

## Validator Results

Command style:

```bash
/Users/zhangbin/GitHub/agent-evidence/.venv/bin/agent-evidence validate-profile <statement-path>
```

Repository generated statements:

- `generated/valid-agent-trace-eeoap-statement.json`: `ok=true`,
  `issue_count=0`
- `generated/valid-agent-workflow-trace-eeoap-statement.json`: `ok=true`,
  `issue_count=0`

Support package copied statements:

- `papers/opentelemetry-to-eeoap/softwarex_release_candidate_package_v1_25/EVIDENCE/generated/valid-agent-trace-eeoap-statement.json`:
  `ok=true`, `issue_count=0`
- `papers/opentelemetry-to-eeoap/softwarex_release_candidate_package_v1_25/EVIDENCE/generated/valid-agent-workflow-trace-eeoap-statement.json`:
  `ok=true`, `issue_count=0`

Each validator run passed schema, references, consistency, and integrity stages.
The validator emitted the existing Python 3.14 / Pydantic V1 compatibility
warning from LangChain Core; it did not affect validation success.

## Privacy Check

Command:

```bash
grep -RInE "[0-9]{11}" papers/opentelemetry-to-eeoap/softwarex_release_candidate_package_v1_25 || true
```

Result: the generic check found 106 lines in copied synthetic trace fixtures,
generated evidence files, and checksum lines. Inspection found synthetic trace
IDs, timestamps, and SHA-256 hashes only. No private phone number, home address,
or unrelated private identifier was found.

## Git Status After Verification

Command:

```bash
git status --short
```

Result: empty output. Verification did not create tracked or untracked files in
the clean clone. Temporary validation outputs were written under `/tmp`.

## Conclusion

The version 1.25 support package is reproducible from a clean checkout of commit
`a03f6455d87bcf67987c7ba1e4297a224de70976`.

The only remaining validation gap is CFF YAML validation, which was skipped
because PyYAML is unavailable. This remains a metadata validation TODO before
formal release/submission, not a failure of clean-clone reproducibility.
