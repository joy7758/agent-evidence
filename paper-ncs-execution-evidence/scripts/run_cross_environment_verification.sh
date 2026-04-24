#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PAPER_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
CODE_ROOT="${CODE_ROOT:-$(cd "$PAPER_ROOT/.." && pwd)}"
PACK_ROOT="${1:-$PAPER_ROOT/paper_packs/scientific_workflow_public}"
WORKFLOW_FILE="$PAPER_ROOT/.github/workflows/ncs-cross-environment.yml"
RESULT_JSON="$PACK_ROOT/cross_environment_verification.json"
RESULT_MD="$PACK_ROOT/cross_environment_verification.md"
CONTAINER_RESULT="$PACK_ROOT/container_verification_result.json"
TMP_DIR="$(mktemp -d)"
trap 'rm -rf "$TMP_DIR"' EXIT

cd "$CODE_ROOT"

python "$PAPER_ROOT/scripts/build_public_scientific_workflow_pack.py" \
  --pack "$PACK_ROOT" \
  --force

if [ -n "${AGENT_EVIDENCE_BIN:-}" ]; then
  AGENT_EVIDENCE="$AGENT_EVIDENCE_BIN"
elif [ -x "$CODE_ROOT/.venv/bin/agent-evidence" ]; then
  AGENT_EVIDENCE="$CODE_ROOT/.venv/bin/agent-evidence"
elif command -v agent-evidence >/dev/null 2>&1; then
  AGENT_EVIDENCE="agent-evidence"
else
  echo "ERROR: no agent-evidence command found" >&2
  exit 3
fi

set +e
"$AGENT_EVIDENCE" validate-pack --pack "$PACK_ROOT" --strict \
  >"$TMP_DIR/repository_validator.txt" 2>&1
REPO_CODE=$?

python "$PAPER_ROOT/scripts/validate_ncs_pack.py" --pack "$PACK_ROOT" --strict \
  >"$TMP_DIR/paper_local_validator.txt" 2>&1
PAPER_LOCAL_CODE=$?

bash "$PAPER_ROOT/scripts/run_public_scientific_workflow_validation_matrix.sh" "$PACK_ROOT" \
  >"$TMP_DIR/public_matrix.txt" 2>&1
PUBLIC_MATRIX_CODE=$?

bash "$PAPER_ROOT/scripts/run_independent_checker_agreement.sh" "$PACK_ROOT" \
  >"$TMP_DIR/independent_checker.txt" 2>&1
INDEPENDENT_CODE=$?
set -e

python - "$RESULT_JSON" "$RESULT_MD" "$WORKFLOW_FILE" "$PACK_ROOT" "$AGENT_EVIDENCE" \
  "$REPO_CODE" "$PAPER_LOCAL_CODE" "$PUBLIC_MATRIX_CODE" "$INDEPENDENT_CODE" \
  "$CONTAINER_RESULT" "$TMP_DIR" <<'PY'
from __future__ import annotations

import json
import platform
import sys
from datetime import datetime, timezone
from pathlib import Path

result_json = Path(sys.argv[1])
result_md = Path(sys.argv[2])
workflow_file = Path(sys.argv[3])
pack_root = Path(sys.argv[4])
agent_evidence = sys.argv[5]
repo_code = int(sys.argv[6])
paper_local_code = int(sys.argv[7])
public_matrix_code = int(sys.argv[8])
independent_code = int(sys.argv[9])
container_result_path = Path(sys.argv[10])
tmp_dir = Path(sys.argv[11])


def read_text(name: str) -> str:
    path = tmp_dir / name
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")[:4000]


summary = {}
summary_path = pack_root / "summary.json"
if summary_path.exists():
    summary = json.loads(summary_path.read_text(encoding="utf-8"))

agreement = {}
agreement_path = pack_root / "independent_checker_agreement.json"
if agreement_path.exists():
    agreement = json.loads(agreement_path.read_text(encoding="utf-8"))

container_payload = None
if container_result_path.exists():
    container_payload = json.loads(container_result_path.read_text(encoding="utf-8"))

native_pass = all(code == 0 for code in [repo_code, paper_local_code, public_matrix_code])
independent_pass = independent_code == 0 and agreement.get("overall_agreement") is True
container_present = container_payload is not None
container_status = container_payload.get("status") if container_payload else None

payload = {
    "timestamp_utc": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
    "pack": str(pack_root),
    "workflow_file": str(workflow_file),
    "ci_matrix": {
        "native_os": ["ubuntu-latest", "macos-latest"],
        "python_versions": ["3.11", "3.12", "3.13"],
        "container": "locally built CI image from Dockerfile.ncs-ci",
        "optional_pull_image": "ghcr.io/joy7758/agent-evidence:ncs-v0.1",
    },
    "local_environment": {
        "system": platform.system(),
        "release": platform.release(),
        "machine": platform.machine(),
        "python": platform.python_version(),
    },
    "native_validator_exit_code": repo_code,
    "paper_local_validator_exit_code": paper_local_code,
    "public_matrix_exit_code": public_matrix_code,
    "public_matrix_status": "PASS" if public_matrix_code == 0 else "FAIL",
    "independent_checker_exit_code": independent_code,
    "independent_checker_agreement": agreement.get("overall_agreement"),
    "container_result_present": container_present,
    "container_status": container_status,
    "receipt_digest": summary.get("receipt_digest"),
    "repository_validator": {
        "command": f"{agent_evidence} validate-pack --pack <pack> --strict",
        "exit_code": repo_code,
        "output": read_text("repository_validator.txt"),
    },
    "paper_local_validator": {
        "command": "python scripts/validate_ncs_pack.py --pack <pack> --strict",
        "exit_code": paper_local_code,
        "output": read_text("paper_local_validator.txt"),
    },
    "failure_matrix": {
        "command": "bash scripts/run_public_scientific_workflow_validation_matrix.sh <pack>",
        "exit_code": public_matrix_code,
        "output": read_text("public_matrix.txt"),
    },
    "independent_checker": {
        "command": "bash scripts/run_independent_checker_agreement.sh <pack>",
        "exit_code": independent_code,
        "output": read_text("independent_checker.txt"),
    },
    "container_verification": container_payload,
    "overall_local_pass": native_pass and independent_pass,
}

result_json.write_text(
    json.dumps(payload, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
    encoding="utf-8",
)

lines = [
    "# Cross-environment verification record",
    "",
    f"Pack: `{pack_root}`",
    f"Workflow file: `{workflow_file}`",
    "",
    "## CI matrix",
    "",
    "| Dimension | Values |",
    "|---|---|",
    "| Native OS | ubuntu-latest, macos-latest |",
    "| Python | 3.11, 3.12, 3.13 |",
    "| Container | locally built CI image from Dockerfile.ncs-ci |",
    "| Optional pull image | ghcr.io/joy7758/agent-evidence:ncs-v0.1 |",
    "",
    "## Local verification",
    "",
    "| Check | Exit code | Status |",
    "|---|---:|---|",
    f"| Repository strict validator | {repo_code} | {'PASS' if repo_code == 0 else 'FAIL'} |",
    f"| Paper-local validator | {paper_local_code} | {'PASS' if paper_local_code == 0 else 'FAIL'} |",
    f"| Public failure matrix | {public_matrix_code} | {'PASS' if public_matrix_code == 0 else 'FAIL'} |",
    f"| Independent checker agreement | {independent_code} | {'PASS' if independent_pass else 'FAIL'} |",
    f"| Container result present | {'yes' if container_present else 'no'} | {container_status or 'not run'} |",
    "",
    f"Receipt digest: `{summary.get('receipt_digest')}`",
]
result_md.write_text("\n".join(lines) + "\n", encoding="utf-8")

print(f"Wrote {result_json}")
print(f"Wrote {result_md}")
print(f"native_validator_exit_code={repo_code}")
print(f"paper_local_validator_exit_code={paper_local_code}")
print(f"public_matrix_status={'PASS' if public_matrix_code == 0 else 'FAIL'}")
print(f"independent_checker_agreement={agreement.get('overall_agreement')}")
print(f"container_result_present={container_present}")
if container_status is not None:
    print(f"container_status={container_status}")
raise SystemExit(0 if payload["overall_local_pass"] else 1)
PY
