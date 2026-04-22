#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from agent_evidence.oap import sha256_digest, with_recomputed_integrity  # noqa: E402


class ConversionError(ValueError):
    """Raised when the synthetic AGT-like fixture cannot be mapped."""


def _required_mapping(payload: dict[str, Any], key: str) -> dict[str, Any]:
    value = payload.get(key)
    if not isinstance(value, dict):
        raise ConversionError(f"expected object at {key}")
    return value


def _required_string(payload: dict[str, Any], path: str) -> str:
    current: Any = payload
    for part in path.split("."):
        if not isinstance(current, dict) or part not in current:
            raise ConversionError(f"missing required field: {path}")
        current = current[part]
    if not isinstance(current, str) or not current:
        raise ConversionError(f"expected non-empty string at {path}")
    return current


def _constraints(policy_decision: dict[str, Any]) -> list[dict[str, str]]:
    raw_constraints = policy_decision.get("constraints")
    if not isinstance(raw_constraints, list) or not raw_constraints:
        raise ConversionError("expected non-empty array at policy_decision.constraints")

    constraints: list[dict[str, str]] = []
    for index, raw_constraint in enumerate(raw_constraints):
        if not isinstance(raw_constraint, dict):
            raise ConversionError(f"expected object at policy_decision.constraints[{index}]")
        constraint_id = _required_string(raw_constraint, "id")
        description = _required_string(raw_constraint, "description")
        constraints.append({"id": constraint_id, "description": description})
    return constraints


def _operation_status(policy_result: str) -> str:
    return "succeeded" if policy_result == "allow" else "failed"


def convert_agt_evidence_to_eeoap(agt_evidence: dict[str, Any]) -> dict[str, Any]:
    """Convert the synthetic AGT-like fixture into an EEOAP v0.1 statement."""

    agent = _required_mapping(agt_evidence, "agent")
    action = _required_mapping(agt_evidence, "action")
    subject = _required_mapping(agt_evidence, "subject")
    policy_decision = _required_mapping(agt_evidence, "policy_decision")
    input_ref = _required_mapping(agt_evidence, "input")
    output_ref = _required_mapping(agt_evidence, "output")
    audit_artifact = _required_mapping(agt_evidence, "audit_artifact")
    constraints = _constraints(policy_decision)

    action_id = _required_string(action, "id")
    action_name = _required_string(action, "name")
    action_type = _required_string(action, "type")
    operation_id = f"op:{action_id}"
    provenance_id = f"prov:{action_id}"
    evidence_id = f"evidence:{action_id}"
    policy_result = _required_string(policy_decision, "result")

    statement = {
        "profile": {
            "name": "execution-evidence-operation-accountability-profile",
            "version": "0.1",
        },
        "statement_id": f"eeoap:{action_id}",
        "timestamp": _required_string(agt_evidence, "timestamp"),
        "actor": {
            "id": _required_string(agent, "id"),
            "type": "agent",
            "name": _required_string(agent, "name"),
            "runtime": _required_string(agent, "runtime"),
        },
        "subject": {
            "id": _required_string(subject, "id"),
            "type": _required_string(subject, "type"),
            "digest": _required_string(subject, "digest"),
            "locator": _required_string(subject, "locator"),
        },
        "operation": {
            "id": operation_id,
            "type": action_name,
            "description": f"Mapped from AGT action {action_id} ({action_type}).",
            "subject_ref": _required_string(subject, "id"),
            "policy_ref": _required_string(policy_decision, "id"),
            "input_refs": ["ref:agt-input"],
            "output_refs": ["ref:agt-output"],
            "result": {
                "status": _operation_status(policy_result),
                "summary": f"AGT policy decision {policy_result} for {action_name}.",
            },
        },
        "policy": {
            "id": _required_string(policy_decision, "id"),
            "name": _required_string(policy_decision, "name"),
            "constraint_refs": [constraint["id"] for constraint in constraints],
        },
        "constraints": constraints,
        "provenance": {
            "id": provenance_id,
            "actor_ref": _required_string(agent, "id"),
            "operation_ref": operation_id,
            "subject_ref": _required_string(subject, "id"),
            "input_refs": ["ref:agt-input"],
            "output_refs": ["ref:agt-output"],
        },
        "evidence": {
            "id": evidence_id,
            "subject_ref": _required_string(subject, "id"),
            "operation_ref": operation_id,
            "policy_ref": _required_string(policy_decision, "id"),
            "references": [
                {
                    "ref_id": "ref:agt-input",
                    "role": "input",
                    "object_id": _required_string(input_ref, "id"),
                    "digest": _required_string(input_ref, "digest"),
                    "locator": _required_string(input_ref, "locator"),
                },
                {
                    "ref_id": "ref:agt-output",
                    "role": "output",
                    "object_id": _required_string(output_ref, "id"),
                    "digest": _required_string(output_ref, "digest"),
                    "locator": _required_string(output_ref, "locator"),
                },
            ],
            "artifacts": [
                {
                    "artifact_id": "artifact:agt-runtime-evidence-001",
                    "type": _required_string(agt_evidence, "source"),
                    "digest": sha256_digest(agt_evidence),
                    "locator": _required_string(agt_evidence, "source_locator"),
                },
                {
                    "artifact_id": _required_string(audit_artifact, "id"),
                    "type": _required_string(audit_artifact, "type"),
                    "digest": _required_string(audit_artifact, "digest"),
                    "locator": _required_string(audit_artifact, "locator"),
                },
            ],
            "integrity": {},
        },
        "validation": {
            "id": f"validation:{action_id}",
            "evidence_ref": evidence_id,
            "provenance_ref": provenance_id,
            "policy_ref": _required_string(policy_decision, "id"),
            "validator": "agent-evidence validate-profile",
            "method": "schema+reference+consistency",
            "status": "verifiable",
        },
    }
    return with_recomputed_integrity(statement)


def load_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ConversionError(f"expected JSON object: {path}")
    return payload


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Convert synthetic AGT-like evidence into an EEOAP v0.1 statement."
    )
    parser.add_argument("--input", required=True, type=Path, help="Synthetic AGT-like JSON input.")
    parser.add_argument("--output", required=True, type=Path, help="EEOAP v0.1 JSON output.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        agt_evidence = load_json(args.input)
        statement = convert_agt_evidence_to_eeoap(agt_evidence)
        write_json(args.output, statement)
    except (ConversionError, json.JSONDecodeError, OSError) as exc:
        print(f"AGT-to-EEOAP conversion failed: {exc}", file=sys.stderr)
        return 1
    print(args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
