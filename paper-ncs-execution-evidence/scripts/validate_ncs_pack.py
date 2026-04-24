#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

EXIT_CLASSES = {
    0: "PASS",
    2: "CONTENT_OR_DIGEST_MISMATCH",
    3: "INCOMPLETE_EVIDENCE",
    4: "VERSION_OR_PROFILE_MISMATCH",
    5: "POLICY_LINKAGE_FAILURE",
    6: "TEMPORAL_INCONSISTENCY",
    7: "OUTCOME_UNVERIFIABLE",
    8: "IMPLEMENTATION_COUPLING",
    9: "AMBIGUOUS_OPERATION",
    10: "SIGNATURE_OR_KEY_FAILURE",
    11: "REFERENCE_RESOLUTION_FAILURE",
}

REQUIRED_FILES = [
    "manifest.json",
    "bundle.json",
    "receipt.json",
    "summary.json",
    "expected_digest.txt",
]


class ValidationFailure(Exception):
    def __init__(self, code: int, reason: str) -> None:
        super().__init__(reason)
        self.code = code
        self.reason = reason


def canonical_json(obj: Any) -> bytes:
    return json.dumps(
        obj,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def sha256_json(obj: Any) -> str:
    return "sha256:" + hashlib.sha256(canonical_json(obj)).hexdigest()


def sha256_file(path: Path) -> str:
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def load_json(path: Path, code: int = 3) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValidationFailure(code, f"cannot read JSON: {path}") from exc


def parse_time(raw: str, label: str) -> datetime:
    try:
        value = datetime.fromisoformat(raw.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValidationFailure(6, f"invalid timestamp for {label}: {raw}") from exc
    if value.tzinfo is None:
        value = value.replace(tzinfo=timezone.utc)
    return value


def resolve_pack_path(pack: Path, raw_path: Any, missing_code: int = 11) -> Path:
    if not isinstance(raw_path, str) or not raw_path:
        raise ValidationFailure(3, "missing relative artifact path")
    candidate = Path(raw_path)
    if candidate.is_absolute():
        raise ValidationFailure(8, f"absolute path is not portable: {raw_path}")
    resolved = pack / candidate
    if not resolved.exists():
        raise ValidationFailure(missing_code, f"referenced artifact not found: {raw_path}")
    return resolved


def require_mapping(value: Any, label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValidationFailure(3, f"{label} must be an object")
    return value


def require_list(value: Any, label: str) -> list[Any]:
    if not isinstance(value, list):
        raise ValidationFailure(3, f"{label} must be a list")
    return value


def validate_policy(pack: Path, bundle: dict[str, Any]) -> None:
    policy_ref = require_mapping(bundle.get("policy"), "policy")
    policy_path_raw = policy_ref.get("path")
    declared_digest = policy_ref.get("sha256")
    if not isinstance(policy_path_raw, str) or not declared_digest:
        raise ValidationFailure(5, "policy reference or digest is missing")
    policy_path = resolve_pack_path(pack, policy_path_raw, missing_code=5)
    policy = load_json(policy_path, code=5)
    actual_digest = sha256_json(policy)
    if actual_digest != declared_digest:
        raise ValidationFailure(5, "policy digest does not match bundle declaration")


def validate_provenance(pack: Path, bundle: dict[str, Any]) -> dict[str, Any]:
    provenance_ref = require_mapping(bundle.get("provenance"), "provenance")
    provenance_path = resolve_pack_path(pack, provenance_ref.get("path"), missing_code=11)
    declared_digest = provenance_ref.get("sha256")
    if not declared_digest:
        raise ValidationFailure(3, "provenance digest is missing")
    provenance = load_json(provenance_path)
    actual_digest = sha256_json(provenance)
    if actual_digest != declared_digest:
        raise ValidationFailure(2, "provenance digest does not match bundle declaration")

    execution_start = parse_time(str(provenance.get("execution_start", "")), "execution_start")
    execution_end = parse_time(str(provenance.get("execution_end", "")), "execution_end")
    validation_time = parse_time(str(provenance.get("validation_time", "")), "validation_time")
    if not (execution_start <= execution_end <= validation_time):
        raise ValidationFailure(
            6,
            "timestamp ordering must satisfy execution_start <= execution_end <= validation_time",
        )
    return provenance


def validate_file_references(
    pack: Path,
    entries: list[Any],
    label: str,
    *,
    primary_output_id: str | None = None,
) -> dict[str, dict[str, Any]]:
    declared: dict[str, dict[str, Any]] = {}
    for raw_entry in entries:
        entry = require_mapping(raw_entry, label)
        entry_id = entry.get("id")
        if not isinstance(entry_id, str) or not entry_id:
            raise ValidationFailure(3, f"{label} entry is missing id")
        path = resolve_pack_path(pack, entry.get("path"), missing_code=11)
        declared_digest = entry.get("sha256")
        if not declared_digest:
            if label == "output" and entry_id == primary_output_id:
                raise ValidationFailure(7, "primary output digest is missing")
            raise ValidationFailure(3, f"{label} digest is missing: {entry_id}")
        actual_digest = sha256_file(path)
        if actual_digest != declared_digest:
            raise ValidationFailure(2, f"{label} digest mismatch: {entry_id}")
        declared[entry_id] = entry
    return declared


def validate_operation(bundle: dict[str, Any]) -> None:
    profile = require_mapping(bundle.get("profile"), "profile")
    if profile.get("version") != "ncs-v1.0-draft":
        raise ValidationFailure(4, f"unsupported profile version: {profile.get('version')}")

    operation = require_mapping(bundle.get("operation"), "operation")
    if operation.get("type") != "fastq_qc":
        raise ValidationFailure(
            9, f"operation type is not specific FASTQ QC: {operation.get('type')}"
        )
    semantics = operation.get("semantics")
    if not isinstance(semantics, str) or len(semantics.strip()) < 20:
        raise ValidationFailure(9, "operation semantics are missing or underspecified")
    if semantics.strip().lower() in {"process data", "run workflow", "analyze data"}:
        raise ValidationFailure(9, "operation semantics are ambiguous")


def validate_outcome(bundle: dict[str, Any], outputs: dict[str, dict[str, Any]]) -> None:
    outcome = require_mapping(bundle.get("outcome"), "outcome")
    primary_output = outcome.get("primary_output")
    if not isinstance(primary_output, str) or primary_output not in outputs:
        raise ValidationFailure(7, "outcome primary_output does not resolve to a declared output")
    if not outputs[primary_output].get("sha256"):
        raise ValidationFailure(7, "primary output lacks verifiable digest")

    claims = require_list(outcome.get("claims"), "outcome claims")
    if not claims:
        raise ValidationFailure(7, "outcome has no verifiable claims")
    for raw_claim in claims:
        claim = require_mapping(raw_claim, "outcome claim")
        if claim.get("output") != primary_output:
            raise ValidationFailure(7, "outcome claim is not linked to the primary output")
        if not claim.get("name") or not claim.get("json_path"):
            raise ValidationFailure(7, "outcome claim lacks name or JSON path")


def validate_pack(pack: Path) -> None:
    if not pack.is_dir():
        raise ValidationFailure(3, f"pack directory not found: {pack}")
    for name in REQUIRED_FILES:
        if not (pack / name).is_file():
            raise ValidationFailure(3, f"required file missing: {name}")

    bundle = require_mapping(load_json(pack / "bundle.json"), "bundle")
    receipt = require_mapping(load_json(pack / "receipt.json"), "receipt")
    summary = require_mapping(load_json(pack / "summary.json"), "summary")

    validate_operation(bundle)
    validate_policy(pack, bundle)
    validate_provenance(pack, bundle)

    outcome = require_mapping(bundle.get("outcome"), "outcome")
    primary_output = outcome.get("primary_output")
    inputs = require_list(bundle.get("inputs"), "inputs")
    outputs_raw = require_list(bundle.get("outputs"), "outputs")
    evidence = require_list(bundle.get("evidence"), "evidence")

    validate_file_references(pack, inputs, "input")
    outputs = validate_file_references(
        pack,
        outputs_raw,
        "output",
        primary_output_id=primary_output if isinstance(primary_output, str) else None,
    )
    validate_file_references(pack, evidence, "evidence")
    validate_outcome(bundle, outputs)

    bundle_digest = sha256_json(bundle)
    if receipt.get("bundle_digest") != bundle_digest:
        raise ValidationFailure(2, "receipt bundle digest does not match bundle.json")

    receipt_digest = sha256_json(receipt)
    if summary.get("receipt_digest") != receipt_digest:
        raise ValidationFailure(2, "summary receipt digest does not match receipt.json")

    expected_digest = (pack / "expected_digest.txt").read_text(encoding="utf-8").strip()
    if expected_digest != receipt_digest:
        raise ValidationFailure(2, "expected_digest.txt does not match receipt.json")


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate an NCS scientific workflow pack.")
    parser.add_argument("--pack", required=True, type=Path)
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args()

    try:
        validate_pack(args.pack)
    except ValidationFailure as exc:
        print(f"FAIL: {EXIT_CLASSES[exc.code]}: {exc.reason}")
        return exc.code

    print(f"PASS: {args.pack}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
