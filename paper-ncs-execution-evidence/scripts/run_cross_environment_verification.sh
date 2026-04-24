#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PAPER_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
CODE_ROOT="${CODE_ROOT:-$(cd "$PAPER_ROOT/.." && pwd)}"
PACK_ROOT="${1:-$PAPER_ROOT/paper_packs/scientific_workflow_public}"
WORKFLOW_FILE="$PAPER_ROOT/.github/workflows/ncs-cross-environment.yml"
RESULT_JSON="$PACK_ROOT/cross_environment_verification.json"
RESULT_MD="$PACK_ROOT/cross_environment_verification.md"
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
"$AGENT_EVIDENCE" validate-pack --pack "$PACK_ROOT" --strict >"$TMP_DIR/repository_validator.txt" 2>&1
REPO_CODE=$?

python "$PAPER_ROOT/scripts/validate_ncs_pack.py" --pack "$PACK_ROOT" --strict >"$TMP_DIR/paper_local_validator.txt" 2>&1
PAPER_LOCAL_CODE=$?

bash "$PAPER_ROOT/scripts/run_public_scientific_workflow_validation_matrix.sh" >"$TMP_DIR/public_matrix.txt" 2>&1
PUBLIC_MATRIX_CODE=$?

bash "$PAPER_ROOT/scripts/run_independent_checker_agreement.sh" "$PACK_ROOT" >"$TMP_DIR/independent_checker.txt" 2>&1
INDEPENDENT_CODE=$?
set -e

DOCKER_STATUS="not-run"
DOCKER_CODE=""
DOCKER_REASON="Docker execution is optional locally; CI runs the declared container matrix."
if [ "${NCS_SKIP_DOCKER:-0}" != "1" ] && command -v docker >/dev/null 2>&1 && docker info >/dev/null 2>&1; then
  DOCKER_STATUS="run"
  DOCKER_REASON=""
  set +e
  docker run --rm \
    -v "$CODE_ROOT:/work" \
    -w /work \
    ghcr.io/joy7758/agent-evidence:ncs-v0.1 \
    /bin/sh -lc '
      python -m pip install -e . >/tmp/ncs-pip-install.log 2>&1 &&
      python paper-ncs-execution-evidence/scripts/build_public_scientific_workflow_pack.py --pack paper-ncs-execution-evidence/paper_packs/scientific_workflow_public --force &&
      agent-evidence validate-pack --pack paper-ncs-execution-evidence/paper_packs/scientific_workflow_public --strict &&
      python paper-ncs-execution-evidence/scripts/validate_ncs_pack.py --pack paper-ncs-execution-evidence/paper_packs/scientific_workflow_public --strict &&
      bash paper-ncs-execution-evidence/scripts/run_public_scientific_workflow_validation_matrix.sh &&
      bash paper-ncs-execution-evidence/scripts/run_independent_checker_agreement.sh paper-ncs-execution-evidence/paper_packs/scientific_workflow_public
    ' >"$TMP_DIR/docker_container.txt" 2>&1
  DOCKER_CODE=$?
  set -e
else
  if [ "${NCS_REQUIRE_DOCKER:-0}" = "1" ]; then
    echo "ERROR: Docker is required but not available or not running" >&2
    exit 3
  fi
  echo "Docker container validation skipped locally; CI workflow includes ghcr.io/joy7758/agent-evidence:ncs-v0.1."
fi

python - "$RESULT_JSON" "$RESULT_MD" "$WORKFLOW_FILE" "$PACK_ROOT" "$AGENT_EVIDENCE" \
  "$REPO_CODE" "$PAPER_LOCAL_CODE" "$PUBLIC_MATRIX_CODE" "$INDEPENDENT_CODE" "$DOCKER_STATUS" "$DOCKER_CODE" "$DOCKER_REASON" "$TMP_DIR" <<'PY'
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
docker_status = sys.argv[10]
docker_code_raw = sys.argv[11]
docker_reason = sys.argv[12]
tmp_dir = Path(sys.argv[13])

def read_text(name: str) -> str:
    path = tmp_dir / name
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")[:4000]

docker_code = None if docker_code_raw == "" else int(docker_code_raw)
local_pass = all(code == 0 for code in [repo_code, paper_local_code, public_matrix_code, independent_code])
docker_pass = docker_status != "run" or docker_code == 0

summary = {}
summary_path = pack_root / "summary.json"
if summary_path.exists():
    summary = json.loads(summary_path.read_text(encoding="utf-8"))

payload = {
    "generated_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
    "pack": str(pack_root),
    "workflow_file": str(workflow_file),
    "ci_matrix": {
        "native_os": ["ubuntu-latest", "macos-latest"],
        "python_versions": ["3.11", "3.12", "3.13"],
        "container_images": ["ghcr.io/joy7758/agent-evidence:ncs-v0.1"],
    },
    "local_environment": {
        "system": platform.system(),
        "release": platform.release(),
        "machine": platform.machine(),
        "python": platform.python_version(),
    },
    "repository_validator": {
        "command": f"{agent_evidence} validate-pack --pack <pack> --strict",
        "exit_code": repo_code,
        "output": read_text("repository_validator.txt"),
    },
    "paper_local_validator": {
        "command": "python paper-ncs-execution-evidence/scripts/validate_ncs_pack.py --pack <pack> --strict",
        "exit_code": paper_local_code,
        "output": read_text("paper_local_validator.txt"),
    },
    "failure_matrix": {
        "command": "bash paper-ncs-execution-evidence/scripts/run_public_scientific_workflow_validation_matrix.sh",
        "exit_code": public_matrix_code,
        "output": read_text("public_matrix.txt"),
    },
    "independent_checker": {
        "command": "bash paper-ncs-execution-evidence/scripts/run_independent_checker_agreement.sh <pack>",
        "exit_code": independent_code,
        "output": read_text("independent_checker.txt"),
    },
    "docker_container_local": {
        "image": "ghcr.io/joy7758/agent-evidence:ncs-v0.1",
        "status": docker_status,
        "exit_code": docker_code,
        "reason": docker_reason,
        "output": read_text("docker_container.txt"),
    },
    "receipt_digest": summary.get("receipt_digest"),
    "local_native_pass": local_pass,
    "local_docker_pass": docker_pass,
    "overall_local_pass": local_pass and docker_pass,
    "remote_ci": {
        "status": "configured_not_run",
        "reason": "Workflow is staged as a paper-local CI definition; remote GitHub Actions require committing and installing/enabling it from the repository workflow path.",
    },
}

result_json.write_text(json.dumps(payload, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8")

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
    "| Container | ghcr.io/joy7758/agent-evidence:ncs-v0.1 |",
    "",
    "## Local verification",
    "",
    "| Check | Exit code | Status |",
    "|---|---:|---|",
    f"| Repository strict validator | {repo_code} | {'PASS' if repo_code == 0 else 'FAIL'} |",
    f"| Paper-local validator | {paper_local_code} | {'PASS' if paper_local_code == 0 else 'FAIL'} |",
    f"| Public failure matrix | {public_matrix_code} | {'PASS' if public_matrix_code == 0 else 'FAIL'} |",
    f"| Independent checker agreement | {independent_code} | {'PASS' if independent_code == 0 else 'FAIL'} |",
    f"| Local Docker container | {docker_code if docker_code is not None else 'not run'} | {'PASS' if docker_pass else 'FAIL'} |",
    "",
    f"Receipt digest: `{summary.get('receipt_digest')}`",
    "",
    "Remote CI status: configured, not run in this local session.",
]
if docker_reason:
    lines.extend(["", f"Local Docker note: {docker_reason}"])
result_md.write_text("\n".join(lines) + "\n", encoding="utf-8")

print(f"Wrote {result_json}")
print(f"Wrote {result_md}")
print(f"repository_validator_exit_code={repo_code}")
print(f"paper_local_validator_exit_code={paper_local_code}")
print(f"public_failure_matrix_exit_code={public_matrix_code}")
print(f"independent_checker_exit_code={independent_code}")
print(f"docker_container_status={docker_status}")
if docker_code is not None:
    print(f"docker_container_exit_code={docker_code}")
raise SystemExit(0 if payload["overall_local_pass"] else 1)
PY
