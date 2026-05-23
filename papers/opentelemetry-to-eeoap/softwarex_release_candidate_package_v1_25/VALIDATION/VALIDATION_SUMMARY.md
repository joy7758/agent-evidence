# Validation Summary

This file records version 1.25 validation results.

## CodeMeta JSON Validation

Command:

```bash
python -m json.tool papers/opentelemetry-to-eeoap/softwarex_release_candidate_package_v1_25/METADATA/codemeta-otel-eeoap-release-draft.json > /tmp/codemeta-otel-eeoap-release-draft-v1-25.validated.json
```

Result: passed. The JSON parsed successfully.

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

No PyYAML dependency was installed in this task.

## Validator Results

Repository generated statements:

- `generated/valid-agent-trace-eeoap-statement.json`: `ok=true`,
  `issue_count=0`; stages passed: `schema`, `references`, `consistency`,
  `integrity`.
- `generated/valid-agent-workflow-trace-eeoap-statement.json`: `ok=true`,
  `issue_count=0`; stages passed: `schema`, `references`, `consistency`,
  `integrity`.

Support package copied statements:

- `EVIDENCE/generated/valid-agent-trace-eeoap-statement.json`: `ok=true`,
  `issue_count=0`; stages passed: `schema`, `references`, `consistency`,
  `integrity`.
- `EVIDENCE/generated/valid-agent-workflow-trace-eeoap-statement.json`:
  `ok=true`, `issue_count=0`; stages passed: `schema`, `references`,
  `consistency`, `integrity`.

Each validator run emitted the existing Python 3.14 / Pydantic V1 compatibility
warning from LangChain Core. The warning did not affect validation success.

## Scoped Pytest

Command:

```bash
/Users/zhangbin/GitHub/agent-evidence/.venv/bin/python -m pytest tests/test_opentelemetry_to_eeoap_adapter.py -q
```

Result: `8 passed in 1.93s`.

## Checksum Verification

Command:

```bash
cd papers/opentelemetry-to-eeoap/softwarex_release_candidate_package_v1_25
sha256sum -c CHECKSUMS.sha256
```

Result: final checksum verification returned OK for all 34 listed files.

## Clean-Clone Verification

Clean-clone verification remains planned, not yet executed for this support
package. It should be run after the version 1.25 package commit and before
release, tag, DOI, or formal submission decisions.
