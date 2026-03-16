#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from typing import Any

try:
    from jsonschema import Draft202012Validator
except ImportError:  # pragma: no cover - optional dependency
    Draft202012Validator = None

ROOT = Path(__file__).resolve().parents[1]

SCHEMA_PATH = ROOT / "schema" / "execution-evidence-object.schema.json"
HASH_PATTERN = re.compile(r"^sha256:[0-9a-f]{64}$")


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def compute_hash(value: Any) -> str:
    payload = json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def validate_with_fallback(instance: dict[str, Any], schema: dict[str, Any]) -> list[str]:
    issues: list[str] = []

    if not isinstance(instance, dict):
        return ["instance must be a JSON object"]

    for field in schema.get("required", []):
        if field not in instance:
            issues.append(f"missing required field: {field}")

    if instance.get("object_type") != "execution-evidence-object":
        issues.append("object_type must equal execution-evidence-object")

    if not isinstance(instance.get("agent_framework"), str):
        issues.append("agent_framework must be a string")
    if not isinstance(instance.get("run_id"), str):
        issues.append("run_id must be a string")
    if not isinstance(instance.get("timestamp"), str):
        issues.append("timestamp must be a string")
    if not isinstance(instance.get("context"), dict):
        issues.append("context must be an object")

    steps = instance.get("steps")
    if not isinstance(steps, list):
        issues.append("steps must be an array")
    else:
        for index, step in enumerate(steps):
            if not isinstance(step, dict):
                issues.append(f"steps[{index}] must be an object")
                continue
            for field in ("step_id", "step_type", "action", "status"):
                if not isinstance(step.get(field), str):
                    issues.append(f"steps[{index}].{field} must be a string")

    hashes = instance.get("hashes")
    if not isinstance(hashes, dict):
        issues.append("hashes must be an object")
    else:
        for field in ("action_hash", "trace_hash", "proof_hash"):
            value = hashes.get(field)
            if not isinstance(value, str) or not HASH_PATTERN.match(value):
                issues.append(f"hashes.{field} must match sha256:<64 lowercase hex chars>")

    return issues


def validate_schema(instance: dict[str, Any], schema_path: Path) -> list[str]:
    schema = load_json(schema_path)

    if Draft202012Validator is None:
        return validate_with_fallback(instance, schema)

    validator = Draft202012Validator(schema)
    issues = []
    for error in sorted(validator.iter_errors(instance), key=lambda item: list(item.path)):
        path = ".".join(str(part) for part in error.path)
        issues.append(f"{path or 'root'}: {error.message}")
    return issues


def recompute_hashes(instance: dict[str, Any]) -> dict[str, str]:
    action_hash = "sha256:" + compute_hash(instance["steps"])
    trace_hash = "sha256:" + compute_hash(
        {
            "agent_framework": instance["agent_framework"],
            "run_id": instance["run_id"],
            "steps": instance["steps"],
            "context": instance["context"],
            "timestamp": instance["timestamp"],
        }
    )
    proof_hash = "sha256:" + compute_hash(
        {
            "action_hash": action_hash,
            "trace_hash": trace_hash,
        }
    )
    return {
        "action_hash": action_hash,
        "trace_hash": trace_hash,
        "proof_hash": proof_hash,
    }


def verify_integrity(instance: dict[str, Any]) -> list[str]:
    expected = recompute_hashes(instance)
    issues: list[str] = []
    for field, expected_value in expected.items():
        actual_value = instance.get("hashes", {}).get(field)
        if actual_value != expected_value:
            issues.append(f"hashes.{field} mismatch: expected {expected_value}, got {actual_value}")
    return issues


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate and verify an Execution Evidence Object."
    )
    parser.add_argument(
        "evidence_object",
        type=Path,
        help="Path to the evidence object JSON file.",
    )
    parser.add_argument(
        "--schema",
        type=Path,
        default=SCHEMA_PATH,
        help="Path to the Execution Evidence Object schema.",
    )
    args = parser.parse_args()

    instance = load_json(args.evidence_object)
    schema_issues = validate_schema(instance, args.schema)
    integrity_issues = verify_integrity(instance) if not schema_issues else []
    issues = schema_issues + integrity_issues

    if issues:
        print("VERIFY_FAIL")
        for issue in issues:
            print(f"- {issue}")
        return 1

    print("VERIFY_OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
