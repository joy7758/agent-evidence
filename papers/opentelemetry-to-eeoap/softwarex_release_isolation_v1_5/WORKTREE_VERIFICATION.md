# Worktree Verification

## Current Dirty Repository Preflight

The source repository preflight was run in:

`/Users/zhangbin/GitHub/agent-evidence`

Observed branch:

`opentelemetry-to-eeoap-adapter`

Observed HEAD:

`eda35b047041baee2eb6b578ba1cdd603fd06939`

Existing dirty/untracked items were present before isolation, including
SoftwareX/AEP-Media manuscript files, `pd-oap`, `tmp`,
`paper-ncs-execution-evidence`, and related local paper artifacts. These files
were not cleaned, reset, stashed, edited, or staged.

## Clean Worktree Creation

Command:

```bash
rm -rf /tmp/agent-evidence-softwarex-otel-eeoap-rc && git worktree add -b softwarex-otel-eeoap-release-candidate /tmp/agent-evidence-softwarex-otel-eeoap-rc eda35b047041baee2eb6b578ba1cdd603fd06939
```

Result:

```text
Preparing worktree (new branch 'softwarex-otel-eeoap-release-candidate')
HEAD is now at eda35b0 Add SoftwareX route analysis for OpenTelemetry-to-EEOAP package
```

## Clean Worktree Status

- Worktree path: `/tmp/agent-evidence-softwarex-otel-eeoap-rc`
- Branch name: `softwarex-otel-eeoap-release-candidate`
- HEAD commit before v1.5 documentation: `eda35b047041baee2eb6b578ba1cdd603fd06939`
- `git status --short` before v1.5 documentation: clean
- Tag list includes:
  - `eeoap-v0.1-artifact`
  - `aep-v0.1-artifact`
  - `eeoap-v0.1-paper`
  - `v0.1-live-chain-security`
  - `aep-media-v0.1.0`

## Scoped Test Result

Command:

```bash
/Users/zhangbin/GitHub/agent-evidence/.venv/bin/python -m pytest tests/test_opentelemetry_to_eeoap_adapter.py -q
```

Result before v1.5 documentation:

```text
8 passed in 2.30s
```

Result after v1.5 documentation:

```text
8 passed in 2.69s
```

## Validator Results

Validator command used for the first generated statement:

```bash
PYTHONPATH=/tmp/agent-evidence-softwarex-otel-eeoap-rc /Users/zhangbin/GitHub/agent-evidence/.venv/bin/agent-evidence validate-profile generated/valid-agent-trace-eeoap-statement.json
```

Observed result:

- `ok=true`
- `issue_count=0`
- stages passed: `schema`, `references`, `consistency`, `integrity`
- summary: `PASS execution-evidence-operation-accountability-profile@0.1 generated/valid-agent-trace-eeoap-statement.json`

Validator command used for the second generated statement:

```bash
PYTHONPATH=/tmp/agent-evidence-softwarex-otel-eeoap-rc /Users/zhangbin/GitHub/agent-evidence/.venv/bin/agent-evidence validate-profile generated/valid-agent-workflow-trace-eeoap-statement.json
```

Observed result:

- `ok=true`
- `issue_count=0`
- stages passed: `schema`, `references`, `consistency`, `integrity`
- summary: `PASS execution-evidence-operation-accountability-profile@0.1 generated/valid-agent-workflow-trace-eeoap-statement.json`

Warning observed during validator invocation:

```text
UserWarning: Core Pydantic V1 functionality isn't compatible with Python 3.14 or greater.
```

The warning came from the shared virtual environment and did not prevent either
validator command from returning a passing result.

## Frozen Package Checksum Result

Command:

```bash
cd papers/opentelemetry-to-eeoap/frozen_v0_5
shasum -a 256 -c CHECKSUMS.sha256
```

Result:

- 13 files OK.
- No checksum failure.

## Conclusion

The release-candidate worktree is isolated and reproducible for the current
OpenTelemetry-to-EEOAP SoftwareX preparation gate. It starts from the v1.4
commit, has clean status before v1.5 documentation, exposes the expected local
tags, passes scoped adapter tests, validates both generated EEOAP statements,
and verifies the frozen v0.5 checksum set.
