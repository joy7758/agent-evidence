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

REQUIRED_FILES = {
    "manifest.json",
    "bundle.json",
    "receipt.json",
    "summary.json",
    "expected_digest.txt",
}


class CheckResult(Exception):
    def __init__(self, code: int, reason: str) -> None:
        super().__init__(reason)
        self.code = code
        self.reason = reason


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def digest_json(value: Any) -> str:
    return "sha256:" + hashlib.sha256(canonical_bytes(value)).hexdigest()


def digest_file(path: Path) -> str:
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def read_json(path: Path, failure_code: int = 3) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise CheckResult(failure_code, f"cannot read JSON file: {path}") from exc


def expect_object(value: Any, label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise CheckResult(3, f"{label} must be an object")
    return value


def expect_list(value: Any, label: str) -> list[Any]:
    if not isinstance(value, list):
        raise CheckResult(3, f"{label} must be a list")
    return value


def parse_timestamp(value: Any, label: str) -> datetime:
    if not isinstance(value, str):
        raise CheckResult(6, f"{label} is not an ISO timestamp")
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise CheckResult(6, f"{label} is not parseable: {value}") from exc
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed


def inside(child: Path, parent: Path) -> bool:
    try:
        child.relative_to(parent)
    except ValueError:
        return False
    return True


def resolve_artifact(pack: Path, raw_path: Any, missing_code: int = 11) -> Path:
    if not isinstance(raw_path, str) or not raw_path:
        raise CheckResult(3, "artifact path is missing")
    path = Path(raw_path)
    if path.is_absolute():
        raise CheckResult(8, f"absolute local path is not portable: {raw_path}")
    root = pack.resolve()
    resolved = (pack / path).resolve()
    if not inside(resolved, root):
        raise CheckResult(8, f"path traversal escapes pack: {raw_path}")
    if not resolved.exists():
        raise CheckResult(missing_code, f"artifact reference does not resolve: {raw_path}")
    return resolved


def check_profile_and_operation(bundle: dict[str, Any]) -> None:
    profile = expect_object(bundle.get("profile"), "bundle.profile")
    if profile.get("version") != "ncs-v1.0-draft":
        raise CheckResult(4, f"unsupported profile version: {profile.get('version')}")

    operation = expect_object(bundle.get("operation"), "bundle.operation")
    if operation.get("type") != "fastq_qc":
        raise CheckResult(9, f"unsupported or ambiguous operation type: {operation.get('type')}")
    semantics = operation.get("semantics")
    if not isinstance(semantics, str) or len(semantics.strip()) < 20:
        raise CheckResult(9, "operation semantics are underspecified")
    if semantics.strip().lower() in {"process data", "run workflow", "analyze data"}:
        raise CheckResult(9, "operation semantics are ambiguous")


def check_policy(pack: Path, bundle: dict[str, Any]) -> None:
    policy = expect_object(bundle.get("policy"), "bundle.policy")
    declared_digest = policy.get("sha256")
    if not isinstance(policy.get("path"), str) or not declared_digest:
        raise CheckResult(5, "policy path or digest is missing")
    policy_path = resolve_artifact(pack, policy["path"], missing_code=5)
    payload = read_json(policy_path, failure_code=5)
    if digest_json(payload) != declared_digest:
        raise CheckResult(5, "policy digest mismatch")


def check_provenance(pack: Path, bundle: dict[str, Any]) -> None:
    provenance = expect_object(bundle.get("provenance"), "bundle.provenance")
    declared_digest = provenance.get("sha256")
    if not declared_digest:
        raise CheckResult(3, "provenance digest is missing")
    provenance_path = resolve_artifact(pack, provenance.get("path"))
    payload = read_json(provenance_path)
    if digest_json(payload) != declared_digest:
        raise CheckResult(2, "provenance digest mismatch")
    start = parse_timestamp(payload.get("execution_start"), "execution_start")
    end = parse_timestamp(payload.get("execution_end"), "execution_end")
    validation = parse_timestamp(payload.get("validation_time"), "validation_time")
    if not (start <= end <= validation):
        raise CheckResult(6, "execution_start <= execution_end <= validation_time was violated")


def check_referenced_files(
    pack: Path,
    raw_entries: list[Any],
    label: str,
    *,
    primary_output: str | None = None,
) -> dict[str, dict[str, Any]]:
    checked: dict[str, dict[str, Any]] = {}
    for raw_entry in raw_entries:
        entry = expect_object(raw_entry, f"{label} entry")
        entry_id = entry.get("id")
        if not isinstance(entry_id, str) or not entry_id:
            raise CheckResult(3, f"{label} entry id is missing")
        path = resolve_artifact(pack, entry.get("path"))
        declared_digest = entry.get("sha256")
        if not declared_digest:
            if label == "output" and entry_id == primary_output:
                raise CheckResult(7, "primary output digest is missing")
            raise CheckResult(3, f"{label} digest is missing for {entry_id}")
        if digest_file(path) != declared_digest:
            raise CheckResult(2, f"{label} digest mismatch for {entry_id}")
        checked[entry_id] = entry
    return checked


def check_outcome(bundle: dict[str, Any], outputs: dict[str, dict[str, Any]]) -> None:
    outcome = expect_object(bundle.get("outcome"), "bundle.outcome")
    primary = outcome.get("primary_output")
    if not isinstance(primary, str) or primary not in outputs:
        raise CheckResult(7, "primary output is not declared")
    if not outputs[primary].get("sha256"):
        raise CheckResult(7, "primary output has no verifiable digest")
    claims = expect_list(outcome.get("claims"), "bundle.outcome.claims")
    if not claims:
        raise CheckResult(7, "outcome has no claims")
    for claim in claims:
        claim_obj = expect_object(claim, "outcome claim")
        if claim_obj.get("output") != primary:
            raise CheckResult(7, "outcome claim is not linked to the primary output")
        if not claim_obj.get("name") or not claim_obj.get("json_path"):
            raise CheckResult(7, "outcome claim lacks name or JSON path")


def check_pack(pack: Path) -> None:
    if not pack.is_dir():
        raise CheckResult(3, f"pack directory not found: {pack}")
    missing = sorted(name for name in REQUIRED_FILES if not (pack / name).is_file())
    if missing:
        raise CheckResult(3, f"required files missing: {', '.join(missing)}")

    bundle = expect_object(read_json(pack / "bundle.json"), "bundle")
    receipt = expect_object(read_json(pack / "receipt.json"), "receipt")
    summary = expect_object(read_json(pack / "summary.json"), "summary")

    check_profile_and_operation(bundle)
    check_policy(pack, bundle)
    check_provenance(pack, bundle)

    outcome = expect_object(bundle.get("outcome"), "bundle.outcome")
    primary = (
        outcome.get("primary_output") if isinstance(outcome.get("primary_output"), str) else None
    )
    check_referenced_files(pack, expect_list(bundle.get("inputs"), "bundle.inputs"), "input")
    outputs = check_referenced_files(
        pack,
        expect_list(bundle.get("outputs"), "bundle.outputs"),
        "output",
        primary_output=primary,
    )
    check_referenced_files(pack, expect_list(bundle.get("evidence"), "bundle.evidence"), "evidence")
    check_outcome(bundle, outputs)

    if receipt.get("bundle_digest") != digest_json(bundle):
        raise CheckResult(2, "receipt bundle digest does not match bundle")
    receipt_digest = digest_json(receipt)
    if summary.get("receipt_digest") != receipt_digest:
        raise CheckResult(2, "summary receipt digest does not match receipt")
    expected_digest = (pack / "expected_digest.txt").read_text(encoding="utf-8").strip()
    if expected_digest != receipt_digest:
        raise CheckResult(2, "expected digest does not match receipt")


def evaluate(pack: Path) -> dict[str, Any]:
    try:
        check_pack(pack)
    except CheckResult as exc:
        return {
            "failure_class": EXIT_CLASSES[exc.code],
            "ok": False,
            "pack": str(pack),
            "reason": exc.reason,
            "exit_code": exc.code,
        }
    return {
        "failure_class": "PASS",
        "ok": True,
        "pack": str(pack),
        "reason": "pack satisfies independent checker protocol",
        "exit_code": 0,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Independent NCS pack checker.")
    parser.add_argument("--pack", required=True, type=Path)
    parser.add_argument("--strict", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    result = evaluate(args.pack)
    if args.json:
        print(json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2))
    elif result["ok"]:
        print(f"PASS: {args.pack}")
    else:
        print(f"FAIL: {result['failure_class']}: {result['reason']}")
    return int(result["exit_code"])


if __name__ == "__main__":
    raise SystemExit(main())
