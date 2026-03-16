#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

echo
echo "== Verify canonical object =="
python3 "${ROOT_DIR}/scripts/verify_evidence_object.py" \
  "${ROOT_DIR}/examples/evidence-object-openai-run.json"

echo
echo "== Run human-readable prototype demo =="
python3 "${ROOT_DIR}/scripts/demo_execution_evidence_object.py"

echo
echo "== Preview FDO-style object example =="
ROOT_DIR="${ROOT_DIR}" python3 - <<'PY'
import json
import os
from pathlib import Path

root = Path(os.environ["ROOT_DIR"])
path = root / "examples" / "fdo-style-execution-evidence-object.json"
data = json.loads(path.read_text(encoding="utf-8"))
summary = {
    "object_id": data["object_id"],
    "pid_placeholder": data["pid_placeholder"],
    "integrity": data["integrity"],
    "provenance": data["provenance"],
}
print(json.dumps(summary, indent=2))
PY
