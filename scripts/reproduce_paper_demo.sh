#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
CASE_DIR="$REPO_ROOT/examples/paper_case"
PYTHON_BIN="${PYTHON:-python3}"

VALID_EVIDENCE="$CASE_DIR/evidence-valid.json"
INVALID_EVIDENCE="$CASE_DIR/evidence-invalid-tampered-output.json"

if [ -x "$REPO_ROOT/.venv/bin/agent-evidence" ]; then
  VALIDATOR_BIN="$REPO_ROOT/.venv/bin/agent-evidence"
elif command -v agent-evidence >/dev/null 2>&1; then
  VALIDATOR_BIN="$(command -v agent-evidence)"
else
  VALIDATOR_BIN=""
fi

if [ -n "$VALIDATOR_BIN" ]; then
  "$VALIDATOR_BIN" validate-profile "$VALID_EVIDENCE" >/dev/null
  if "$VALIDATOR_BIN" validate-profile "$INVALID_EVIDENCE" >/dev/null 2>&1; then
    echo "ERROR: tampered output unexpectedly passed repository validator" >&2
    exit 1
  fi
fi

PYTHONPATH="$REPO_ROOT${PYTHONPATH:+:$PYTHONPATH}" "$PYTHON_BIN" - "$CASE_DIR" <<'PY'
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

from agent_evidence.oap import validate_profile_file

case_dir = Path(sys.argv[1])
required = [
    "fdo-dataset.json",
    "policy-aggregate-only.json",
    "agent-operation.json",
    "evidence-valid.json",
    "evidence-invalid-tampered-output.json",
    "expected-validator-pass.json",
    "expected-validator-fail.json",
]

missing = [name for name in required if not (case_dir / name).is_file()]
if missing:
    raise SystemExit(f"missing paper_case files: {', '.join(missing)}")


def load(name: str) -> dict[str, Any]:
    with (case_dir / name).open("r", encoding="utf-8") as handle:
        payload = json.load(handle)
    if not isinstance(payload, dict):
        raise SystemExit(f"{name} must contain a JSON object")
    return payload


def output_digest(profile: dict[str, Any]) -> str:
    for reference in profile["evidence"]["references"]:
        if reference["role"] == "output":
            return reference["digest"]
    raise SystemExit("no output reference found")


fdo_dataset = load("fdo-dataset.json")
policy = load("policy-aggregate-only.json")
operation = load("agent-operation.json")
valid = load("evidence-valid.json")
tampered = load("evidence-invalid-tampered-output.json")

if fdo_dataset["policy_ref"] != policy["policy_id"]:
    raise SystemExit("dataset policy_ref does not match policy_id")
if operation["policy_ref"] != policy["policy_id"]:
    raise SystemExit("operation policy_ref does not match policy_id")
if valid["subject"]["digest"] != fdo_dataset["content_hash"]:
    raise SystemExit("valid evidence subject digest does not match dataset content_hash")

valid_report = validate_profile_file(case_dir / "evidence-valid.json")
if not valid_report["ok"]:
    raise SystemExit(f"valid evidence did not pass: {valid_report['summary']}")

expected_output_hash = operation["output_object"]["content_hash"]
if output_digest(valid) != expected_output_hash:
    raise SystemExit("valid evidence output digest does not match operation output content_hash")

tampered_report = validate_profile_file(case_dir / "evidence-invalid-tampered-output.json")
if tampered_report["ok"]:
    raise SystemExit("tampered evidence unexpectedly passed validator")
if output_digest(tampered) == expected_output_hash:
    raise SystemExit("tampered evidence did not alter the output digest")

print("PASS valid evidence bundle")
print("FAIL tampered output hash mismatch")
print(json.dumps(
    {
        "ok": True,
        "paper_case": str(case_dir),
        "valid_primary_error_code": valid_report["primary_error_code"],
        "tampered_primary_error_code": tampered_report["primary_error_code"],
        "validator": "agent-evidence validate-profile",
        "keywords": [
            "EEOAP",
            "execution evidence",
            "operation accountability",
            "validator",
            "FDO-style mapping",
            "paper_case"
        ],
    },
    indent=2,
    sort_keys=True,
))
PY
