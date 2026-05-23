# Clean-Clone Verification

## Verification Target

- Target commit: `05a58457709b79582a218615ddf63952fe17f0b7`
- Target branch line: `softwarex-otel-eeoap-release-candidate`
- Support package:
  `papers/opentelemetry-to-eeoap/softwarex_release_candidate_package_v1_15/`

## Verification Method

A new clean verification clone was created outside both the original dirty
worktree and the existing release-candidate worktree:

```bash
rm -rf /tmp/agent-evidence-softwarex-otel-eeoap-v1-16-clean-verify
git clone /tmp/agent-evidence-softwarex-otel-eeoap-rc /tmp/agent-evidence-softwarex-otel-eeoap-v1-16-clean-verify
cd /tmp/agent-evidence-softwarex-otel-eeoap-v1-16-clean-verify
git checkout 05a58457709b79582a218615ddf63952fe17f0b7
```

The checkout entered detached HEAD state at the target commit. Initial
`git status --short` was empty.

## Checkout Status Before Verification

- Checkout path:
  `/tmp/agent-evidence-softwarex-otel-eeoap-v1-16-clean-verify`
- Checked-out commit:
  `05a58457709b79582a218615ddf63952fe17f0b7`
- Branch state: detached HEAD
- Status before verification: clean
- Tag list was available in the clean clone, including:
  `eeoap-v0.1-artifact`, `aep-v0.1-artifact`, `v0.6.0`, and earlier local tags.

## Support Package Existence Check

The support package directory exists and the requested key files are present:

- `README.md`
- `MANIFEST.md`
- `CHECKSUMS.sha256`
- `ARTICLE/softwarex_template_style_draft_v1_14.md`
- `METADATA/CITATION_OTEL_EEOAP.cff`
- `METADATA/codemeta-otel-eeoap.json`
- `EVIDENCE/examples/opentelemetry/valid-agent-workflow-trace.json`
- `EVIDENCE/generated/valid-agent-workflow-trace-eeoap-statement.json`
- `VALIDATION/VALIDATION_SUMMARY.md`

Observed support package file count: 32 files.

## Checksum Result

Command:

```bash
cd papers/opentelemetry-to-eeoap/softwarex_release_candidate_package_v1_15
sha256sum -c CHECKSUMS.sha256
```

Result: all 31 listed files passed SHA-256 verification.

## CodeMeta JSON Validation

Command:

```bash
python -m json.tool papers/opentelemetry-to-eeoap/softwarex_release_candidate_package_v1_15/METADATA/codemeta-otel-eeoap.json > /tmp/codemeta-otel-eeoap-v1-16.validated.json
```

Result: passed. The validation output was written outside the repository under
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
path = Path("papers/opentelemetry-to-eeoap/softwarex_release_candidate_package_v1_15/METADATA/CITATION_OTEL_EEOAP.cff")
with path.open("r", encoding="utf-8") as f:
    yaml.safe_load(f)
print("CFF YAML validation passed")
PY
```

Result: skipped. Exact reason: `No module named 'yaml'`.

No PyYAML dependency was installed in this task.

## Scoped Pytest Result

Command:

```bash
/Users/zhangbin/GitHub/agent-evidence/.venv/bin/python -m pytest tests/test_opentelemetry_to_eeoap_adapter.py -q
```

Result: `8 passed in 2.34s`.

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

- `papers/opentelemetry-to-eeoap/softwarex_release_candidate_package_v1_15/EVIDENCE/generated/valid-agent-trace-eeoap-statement.json`:
  `ok=true`, `issue_count=0`
- `papers/opentelemetry-to-eeoap/softwarex_release_candidate_package_v1_15/EVIDENCE/generated/valid-agent-workflow-trace-eeoap-statement.json`:
  `ok=true`, `issue_count=0`

Each validator run passed schema, references, consistency, and integrity stages.
The validator emitted the existing Python 3.14 / Pydantic V1 compatibility
warning from LangChain Core; it did not affect validation success.

## Git Status After Verification

Final clean clone command:

```bash
git status --short
```

Result: empty output. Verification did not create tracked or untracked
repository files in the clean clone.

## Conclusion

The version 1.15 support package is reproducible from a clean checkout of
commit `05a58457709b79582a218615ddf63952fe17f0b7`.

The only remaining validation gap is CFF YAML syntax validation, which was
skipped because PyYAML is not installed. This remains a pre-submission metadata
check, not a blocker for the clean-clone package verification recorded here.
