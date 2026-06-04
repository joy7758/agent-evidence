#!/usr/bin/env bash
set -euo pipefail

if [ ! -f "pyproject.toml" ] || [ ! -d "agent_evidence" ]; then
  echo "ERROR: run this script from the repository root." >&2
  exit 2
fi

ARTIFACT_DIR="artifacts/paper-minimal-rerun"
mkdir -p "$ARTIFACT_DIR"

if [ -n "${PYTHON:-}" ]; then
  PYTHON_BIN="$PYTHON"
elif [ -x ".venv/bin/python" ]; then
  PYTHON_BIN=".venv/bin/python"
else
  PYTHON_BIN="python3"
fi

if [ -x ".venv/bin/agent-evidence" ]; then
  AGENT_EVIDENCE_BIN=".venv/bin/agent-evidence"
elif command -v agent-evidence >/dev/null 2>&1; then
  AGENT_EVIDENCE_BIN="$(command -v agent-evidence)"
else
  echo "ERROR: agent-evidence CLI not found. Install the package first." >&2
  exit 2
fi

"$PYTHON_BIN" - <<'PY'
import agent_evidence
PY

GIT_COMMIT="$(git rev-parse --short HEAD 2>/dev/null || printf 'unknown')"
RUN_TIMESTAMP="$("$PYTHON_BIN" - <<'PY'
from datetime import datetime, timezone

print(datetime.now(timezone.utc).isoformat())
PY
)"
PYTHON_VERSION="$("$PYTHON_BIN" - <<'PY'
import platform

print(platform.python_version())
PY
)"

run_command() {
  local case_id="$1"
  local expected_exit="$2"
  local expected_primary_code="$3"
  shift 3

  local stdout_path="$ARTIFACT_DIR/${case_id}.stdout"
  local stderr_path="$ARTIFACT_DIR/${case_id}.stderr"
  local status_path="$ARTIFACT_DIR/${case_id}.status.json"

  set +e
  "$@" >"$stdout_path" 2>"$stderr_path"
  local observed_exit=$?
  set -e

  "$PYTHON_BIN" - "$case_id" "$expected_exit" "$expected_primary_code" \
    "$observed_exit" "$stdout_path" "$stderr_path" "$status_path" "$@" <<'PY'
import json
import sys
from pathlib import Path

case_id = sys.argv[1]
expected_exit_raw = sys.argv[2]
expected_primary_code = sys.argv[3] or None
observed_exit = int(sys.argv[4])
stdout_path = Path(sys.argv[5])
stderr_path = Path(sys.argv[6])
status_path = Path(sys.argv[7])
command = sys.argv[8:]
stdout_text = stdout_path.read_text(encoding="utf-8")
stderr_text = stderr_path.read_text(encoding="utf-8")

expected_exit = None if expected_exit_raw == "nonzero" else int(expected_exit_raw)
expected_ok = observed_exit != 0 if expected_exit_raw == "nonzero" else observed_exit == expected_exit

observed_primary_code = None
ok_field = None
try:
    payload = json.loads(stdout_text)
except json.JSONDecodeError:
    payload = None
else:
    if isinstance(payload, dict):
        observed_primary_code = payload.get("primary_error_code")
        ok_field = payload.get("ok")

if expected_primary_code:
    result_ok = expected_ok and observed_primary_code == expected_primary_code
elif case_id == "demo_metadata_enrichment":
    result_ok = expected_ok and "PASS execution-evidence-operation-accountability-profile@0.1" in stdout_text
else:
    result_ok = expected_ok and ok_field is True

status = {
    "case_id": case_id,
    "command": " ".join(command),
    "expected_exit": expected_exit_raw,
    "observed_exit": observed_exit,
    "expected_primary_code": expected_primary_code,
    "observed_primary_code": observed_primary_code,
    "observed_ok": ok_field,
    "stdout": str(stdout_path),
    "stderr": str(stderr_path),
    "stderr_nonempty": bool(stderr_text.strip()),
    "observed_result": "pass" if result_ok else "fail",
}
status_path.write_text(json.dumps(status, indent=2, sort_keys=True) + "\n", encoding="utf-8")
if not result_ok:
    raise SystemExit(
        f"{case_id} failed expectation: exit={observed_exit}, primary={observed_primary_code}"
    )
PY
}

run_command valid_minimal 0 "" \
  "$AGENT_EVIDENCE_BIN" validate-profile examples/minimal-valid-evidence.json

run_command invalid_missing_required nonzero schema_violation \
  "$AGENT_EVIDENCE_BIN" validate-profile examples/invalid-missing-required.json

run_command invalid_unclosed_reference nonzero unresolved_output_ref \
  "$AGENT_EVIDENCE_BIN" validate-profile examples/invalid-unclosed-reference.json

run_command invalid_policy_link_broken nonzero unresolved_evidence_policy_ref \
  "$AGENT_EVIDENCE_BIN" validate-profile examples/invalid-policy-link-broken.json

run_command demo_metadata_enrichment 0 "" \
  "$PYTHON_BIN" demo/run_operation_accountability_demo.py

"$PYTHON_BIN" - "$ARTIFACT_DIR" "$RUN_TIMESTAMP" "$PYTHON_VERSION" "$GIT_COMMIT" <<'PY'
import json
import sys
from pathlib import Path

artifact_dir = Path(sys.argv[1])
run_timestamp = sys.argv[2]
python_version = sys.argv[3]
git_commit = sys.argv[4]

case_order = [
    "valid_minimal",
    "invalid_missing_required",
    "invalid_unclosed_reference",
    "invalid_policy_link_broken",
    "demo_metadata_enrichment",
]
cases = []
for case_id in case_order:
    status_path = artifact_dir / f"{case_id}.status.json"
    cases.append(json.loads(status_path.read_text(encoding="utf-8")))

summary = {
    "ok": all(case["observed_result"] == "pass" for case in cases),
    "timestamp": run_timestamp,
    "python_version": python_version,
    "git_commit": git_commit,
    "cases": cases,
}
(artifact_dir / "summary.json").write_text(
    json.dumps(summary, indent=2, sort_keys=True) + "\n",
    encoding="utf-8",
)
print(json.dumps(summary, indent=2, sort_keys=True))
PY
