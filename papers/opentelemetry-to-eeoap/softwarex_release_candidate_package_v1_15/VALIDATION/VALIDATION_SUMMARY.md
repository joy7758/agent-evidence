# Validation Summary

## Scoped Pytest

Command:

```bash
/Users/zhangbin/GitHub/agent-evidence/.venv/bin/python -m pytest tests/test_opentelemetry_to_eeoap_adapter.py -q
```

Result:

```text
8 passed in 1.84s
```

## Validator Results

Command:

```bash
/Users/zhangbin/GitHub/agent-evidence/.venv/bin/agent-evidence validate-profile generated/valid-agent-trace-eeoap-statement.json
```

Result:

- `ok=true`
- `issue_count=0`
- stages passed: `schema`, `references`, `consistency`, `integrity`
- warning: Python 3.14/Pydantic V1 compatibility warning from LangChain Core

Command:

```bash
/Users/zhangbin/GitHub/agent-evidence/.venv/bin/agent-evidence validate-profile generated/valid-agent-workflow-trace-eeoap-statement.json
```

Result:

- `ok=true`
- `issue_count=0`
- stages passed: `schema`, `references`, `consistency`, `integrity`
- warning: Python 3.14/Pydantic V1 compatibility warning from LangChain Core

## Checksum Verification

Command:

```bash
cd papers/opentelemetry-to-eeoap/softwarex_release_candidate_package_v1_15
sha256sum -c CHECKSUMS.sha256
```

Result:

- Final checksum file generated with `sha256sum`.
- Final verification returned OK for all 31 listed files.

## Clean-Clone Verification

Clean-clone verification remains planned, not yet executed for this support
package. It should be run after this version 1.15 package commit and before any
formal release or submission.
