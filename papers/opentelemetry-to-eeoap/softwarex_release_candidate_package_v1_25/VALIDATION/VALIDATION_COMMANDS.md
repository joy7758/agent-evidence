# Validation Commands

Run these commands from the repository root.

## Scoped Pytest

```bash
/Users/zhangbin/GitHub/agent-evidence/.venv/bin/python -m pytest tests/test_opentelemetry_to_eeoap_adapter.py -q
```

Fallback if the absolute virtual environment is unavailable:

```bash
python -m pytest tests/test_opentelemetry_to_eeoap_adapter.py -q
```

## Validate Repository Generated Statements

```bash
/Users/zhangbin/GitHub/agent-evidence/.venv/bin/agent-evidence validate-profile generated/valid-agent-trace-eeoap-statement.json
```

```bash
/Users/zhangbin/GitHub/agent-evidence/.venv/bin/agent-evidence validate-profile generated/valid-agent-workflow-trace-eeoap-statement.json
```

## Validate Copied Support Package Statements

```bash
/Users/zhangbin/GitHub/agent-evidence/.venv/bin/agent-evidence validate-profile papers/opentelemetry-to-eeoap/softwarex_release_candidate_package_v1_25/EVIDENCE/generated/valid-agent-trace-eeoap-statement.json
```

```bash
/Users/zhangbin/GitHub/agent-evidence/.venv/bin/agent-evidence validate-profile papers/opentelemetry-to-eeoap/softwarex_release_candidate_package_v1_25/EVIDENCE/generated/valid-agent-workflow-trace-eeoap-statement.json
```

## CodeMeta JSON Validation

```bash
python -m json.tool papers/opentelemetry-to-eeoap/softwarex_release_candidate_package_v1_25/METADATA/codemeta-otel-eeoap-release-draft.json > /tmp/codemeta-otel-eeoap-release-draft-v1-25.validated.json
```

## CFF YAML Validation If PyYAML Becomes Available

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

Do not install PyYAML for this route step.

## Verify Checksums

```bash
cd papers/opentelemetry-to-eeoap/softwarex_release_candidate_package_v1_25
sha256sum -c CHECKSUMS.sha256
```

Fallback if `sha256sum` is unavailable:

```bash
cd papers/opentelemetry-to-eeoap/softwarex_release_candidate_package_v1_25
shasum -a 256 -c CHECKSUMS.sha256
```
