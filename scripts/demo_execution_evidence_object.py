#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from verify_evidence_object import (
    SCHEMA_PATH,
    load_json,
    recompute_hashes,
    validate_schema,
    verify_integrity,
)

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OBJECT_PATH = ROOT / "examples" / "evidence-object-openai-run.json"
DEFAULT_FDO_PATH = ROOT / "examples" / "fdo-style-execution-evidence-object.json"


def print_section(title: str) -> None:
    print()
    print(title)
    print("-" * len(title))


def print_loaded_object(instance: dict) -> None:
    print_section("Loaded object")
    print(f"Type: {instance['object_type']}")
    print(f"Framework: {instance['agent_framework']}")
    print(f"Run ID: {instance['run_id']}")
    print(f"Steps: {len(instance['steps'])}")
    print(f"Timestamp: {instance['timestamp']}")


def print_schema_validation(schema_issues: list[str]) -> None:
    print_section("Schema validation")
    if schema_issues:
        print("Status: FAIL")
        for issue in schema_issues:
            print(f"- {issue}")
        return
    print("Status: OK")
    print("The object matches the Execution Evidence Object schema.")


def print_integrity(instance: dict, integrity_issues: list[str]) -> None:
    expected_hashes = recompute_hashes(instance)
    print_section("Integrity check")
    print(f"Action hash: {expected_hashes['action_hash']}")
    print(f"Trace hash:  {expected_hashes['trace_hash']}")
    print(f"Proof hash:  {expected_hashes['proof_hash']}")
    if integrity_issues:
        print("Status: FAIL")
        for issue in integrity_issues:
            print(f"- {issue}")
        return
    print("Status: OK")
    print("The stored hashes match the recomputed evidence hashes.")


def print_provenance(instance: dict) -> None:
    context = instance.get("context", {})
    print_section("Provenance summary")
    print(f"Agent ID: {context.get('agent_id', 'unknown')}")
    print(f"Runtime source: {context.get('source', instance['agent_framework'])}")
    print(f"Scenario: {context.get('scenario', 'n/a')}")


def print_fdo_mapping_summary(fdo_object_path: Path) -> None:
    print_section("FDO mapping summary")
    if not fdo_object_path.exists():
        print("Status: SKIPPED")
        print(f"No FDO-style example found at {fdo_object_path}.")
        return

    fdo_object = load_json(fdo_object_path)
    integrity = fdo_object.get("integrity", {})
    provenance = fdo_object.get("provenance", {})
    print(f"Object ID: {fdo_object.get('object_id', 'n/a')}")
    print(f"PID placeholder: {fdo_object.get('pid_placeholder', 'n/a')}")
    print(f"Integrity proof: {integrity.get('proof_hash', 'n/a')}")
    print(f"Provenance source: {provenance.get('runtime_source', 'n/a')}")
    print("Status: READY")
    print("The verified evidence object can be wrapped in an FDO-style object shell.")


def print_final_result(schema_issues: list[str], integrity_issues: list[str]) -> None:
    print_section("Final result")
    if schema_issues or integrity_issues:
        print("Prototype status: FAIL")
        print("The object needs fixes before it can be presented as a verified sample.")
        return
    print("Prototype status: VERIFY_OK")
    print("The sample is ready to show as a portable and verifiable prototype object.")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run a human-readable Execution Evidence Object prototype demo."
    )
    parser.add_argument(
        "evidence_object",
        nargs="?",
        type=Path,
        default=DEFAULT_OBJECT_PATH,
        help="Path to the Execution Evidence Object JSON file.",
    )
    parser.add_argument(
        "--schema",
        type=Path,
        default=SCHEMA_PATH,
        help="Path to the Execution Evidence Object schema.",
    )
    parser.add_argument(
        "--fdo-object",
        type=Path,
        default=DEFAULT_FDO_PATH,
        help="Optional FDO-style object example path.",
    )
    args = parser.parse_args()

    instance = load_json(args.evidence_object)
    schema_issues = validate_schema(instance, args.schema)
    integrity_issues = verify_integrity(instance) if not schema_issues else []

    print("Execution Evidence Object Prototype Demo")
    print("=======================================")
    print_loaded_object(instance)
    print_schema_validation(schema_issues)
    print_integrity(instance, integrity_issues)
    print_provenance(instance)
    print_fdo_mapping_summary(args.fdo_object)
    print_final_result(schema_issues, integrity_issues)
    return 1 if schema_issues or integrity_issues else 0


if __name__ == "__main__":
    raise SystemExit(main())
