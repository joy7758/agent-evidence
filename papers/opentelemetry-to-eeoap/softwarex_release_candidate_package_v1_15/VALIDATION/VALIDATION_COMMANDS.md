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

## Validate First Generated Statement

```bash
/Users/zhangbin/GitHub/agent-evidence/.venv/bin/agent-evidence validate-profile generated/valid-agent-trace-eeoap-statement.json
```

## Validate Second Generated Statement

```bash
/Users/zhangbin/GitHub/agent-evidence/.venv/bin/agent-evidence validate-profile generated/valid-agent-workflow-trace-eeoap-statement.json
```

## Verify Checksums

```bash
cd papers/opentelemetry-to-eeoap/softwarex_release_candidate_package_v1_15
sha256sum -c CHECKSUMS.sha256
```

Fallback if `sha256sum` is unavailable:

```bash
cd papers/opentelemetry-to-eeoap/softwarex_release_candidate_package_v1_15
shasum -a 256 -c CHECKSUMS.sha256
```
