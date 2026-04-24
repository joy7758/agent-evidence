#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PAPER_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
CODE_ROOT="${CODE_ROOT:-$(cd "$PAPER_ROOT/.." && pwd)}"
PACK="${1:-$PAPER_ROOT/paper_packs/scientific_workflow_public}"

NCS_CONTAINER_IMAGE="${NCS_CONTAINER_IMAGE:-agent-evidence-ncs-ci:local}"
NCS_CONTAINER_DOCKERFILE="${NCS_CONTAINER_DOCKERFILE:-$PAPER_ROOT/docker/Dockerfile.ncs-ci}"
NCS_CONTAINER_PULL_IMAGE="${NCS_CONTAINER_PULL_IMAGE:-0}"
NCS_CONTAINER_BUILD_LOCAL="${NCS_CONTAINER_BUILD_LOCAL:-1}"
RESULT_PATH="$PACK/container_verification_result.json"

if ! command -v docker >/dev/null 2>&1; then
  echo "ERROR: docker command not found" >&2
  exit 3
fi

if ! docker info >/dev/null 2>&1; then
  echo "ERROR: docker daemon is not available" >&2
  exit 3
fi

if [ "$NCS_CONTAINER_PULL_IMAGE" = "1" ]; then
  echo "Attempting optional container pull: $NCS_CONTAINER_IMAGE"
  if ! docker pull "$NCS_CONTAINER_IMAGE"; then
    echo "Optional pull failed; continuing with local build fallback if enabled."
  fi
fi

if [ "$NCS_CONTAINER_BUILD_LOCAL" = "1" ]; then
  echo "Building local NCS CI image: $NCS_CONTAINER_IMAGE"
  docker build -f "$NCS_CONTAINER_DOCKERFILE" -t "$NCS_CONTAINER_IMAGE" "$CODE_ROOT"
elif ! docker image inspect "$NCS_CONTAINER_IMAGE" >/dev/null 2>&1; then
  echo "ERROR: image not available and local build is disabled: $NCS_CONTAINER_IMAGE" >&2
  exit 3
fi

echo "Running container verification with image: $NCS_CONTAINER_IMAGE"
mkdir -p "$(dirname "$RESULT_PATH")"

docker run --rm \
  -e AGENT_EVIDENCE_BIN=agent-evidence \
  -e PACK="$PACK" \
  -e RESULT_PATH="$RESULT_PATH" \
  -e NCS_CONTAINER_IMAGE="$NCS_CONTAINER_IMAGE" \
  -e NCS_CONTAINER_DOCKERFILE="$NCS_CONTAINER_DOCKERFILE" \
  -v "$CODE_ROOT:/repo" \
  -w /repo \
  "$NCS_CONTAINER_IMAGE" '
    set -euo pipefail
    export AGENT_EVIDENCE_BIN=agent-evidence

    python -m pip install -e .

    python paper-ncs-execution-evidence/scripts/build_public_scientific_workflow_pack.py \
      --pack "$PACK" \
      --force

    agent-evidence validate-pack --pack "$PACK" --strict

    bash paper-ncs-execution-evidence/scripts/run_public_scientific_workflow_validation_matrix.sh \
      "$PACK"

    bash paper-ncs-execution-evidence/scripts/run_independent_checker_agreement.sh \
      "$PACK"

    python - <<PY
import json
from datetime import datetime, timezone
from pathlib import Path

pack = Path("$PACK")
result_path = Path("$RESULT_PATH")
summary = json.loads((pack / "summary.json").read_text(encoding="utf-8"))

payload = {
    "mode": "container",
    "image": "$NCS_CONTAINER_IMAGE",
    "dockerfile": "$NCS_CONTAINER_DOCKERFILE",
    "validator_source": "repository",
    "pack": str(pack),
    "commands_run": [
        "python -m pip install -e .",
        "python paper-ncs-execution-evidence/scripts/build_public_scientific_workflow_pack.py --pack <pack> --force",
        "agent-evidence validate-pack --pack <pack> --strict",
        "bash paper-ncs-execution-evidence/scripts/run_public_scientific_workflow_validation_matrix.sh <pack>",
        "bash paper-ncs-execution-evidence/scripts/run_independent_checker_agreement.sh <pack>",
    ],
    "status": "PASS",
    "receipt_digest": summary.get("receipt_digest"),
    "timestamp_utc": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
}
result_path.write_text(
    json.dumps(payload, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
    encoding="utf-8",
)
print(f"Wrote {result_path}")
PY
  '

if command -v sudo >/dev/null 2>&1; then
  sudo chown -R "$(id -u):$(id -g)" "$PACK" || true
else
  chown -R "$(id -u):$(id -g)" "$PACK" || true
fi

echo "CONTAINER_VERIFICATION: PASS"
echo "Result: $RESULT_PATH"
