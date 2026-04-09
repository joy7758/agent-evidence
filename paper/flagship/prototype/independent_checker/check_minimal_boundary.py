#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

EXPECTED_PROFILE_NAME = "execution-evidence-operation-accountability-profile"
EXPECTED_PROFILE_VERSION = "0.1"

GENERIC_OPERATION_TYPES = {
    "action",
    "execute",
    "operation",
    "process",
    "run",
    "task",
}

GENERIC_RESULT_SUMMARIES = {
    "done",
    "ok",
    "success",
    "completed",
    "finished",
}

LOCAL_MARKERS = (
    "/tmp/",
    "/private/tmp/",
    "file:///tmp/",
    "file://localhost/",
    "localhost",
    "127.0.0.1",
    ".venv/",
    ".pytest_cache/",
    "\\\\",
)


def issue(label: str, path: str, message: str) -> dict[str, str]:
    return {"label": label, "path": path, "message": message}


def load_payload(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"invalid JSON: {path}") from exc
    if not isinstance(payload, dict):
        raise ValueError(f"top-level payload must be a JSON object: {path}")
    return payload


def get_dict(payload: dict[str, Any], key: str) -> dict[str, Any]:
    value = payload.get(key)
    return value if isinstance(value, dict) else {}


def get_list(payload: dict[str, Any], key: str) -> list[Any]:
    value = payload.get(key)
    return value if isinstance(value, list) else []


def get_text(payload: dict[str, Any], key: str) -> str:
    value = payload.get(key)
    return value.strip() if isinstance(value, str) else ""


def build_reference_map(payload: dict[str, Any]) -> dict[str, dict[str, Any]]:
    reference_map: dict[str, dict[str, Any]] = {}
    evidence = get_dict(payload, "evidence")
    for item in get_list(evidence, "references"):
        if not isinstance(item, dict):
            continue
        ref_id = get_text(item, "ref_id")
        if ref_id:
            reference_map[ref_id] = item
    return reference_map


def is_local_marker(value: str) -> bool:
    if not value:
        return False
    if value.startswith("/") or value.startswith("C:\\") or value.startswith("D:\\"):
        return True
    return any(marker in value for marker in LOCAL_MARKERS)


def parse_timestamp(raw: str) -> datetime | None:
    if not raw:
        return None
    normalized = raw.replace("Z", "+00:00")
    try:
        parsed = datetime.fromisoformat(normalized)
    except ValueError:
        return None
    if parsed.tzinfo is None:
        return parsed.replace(tzinfo=timezone.utc)
    return parsed


def check_profile_identity(payload: dict[str, Any]) -> list[dict[str, str]]:
    issues: list[dict[str, str]] = []
    profile = get_dict(payload, "profile")
    name = get_text(profile, "name")
    version = get_text(profile, "version")
    if name != EXPECTED_PROFILE_NAME:
        issues.append(
            issue(
                "wrong_profile_name",
                "profile.name",
                f"expected {EXPECTED_PROFILE_NAME!r}, found {name!r}",
            )
        )
    if version != EXPECTED_PROFILE_VERSION:
        issues.append(
            issue(
                "wrong_profile_version",
                "profile.version",
                f"expected {EXPECTED_PROFILE_VERSION!r}, found {version!r}",
            )
        )
    return issues


def check_identity_binding(payload: dict[str, Any]) -> list[dict[str, str]]:
    issues: list[dict[str, str]] = []
    actor = get_dict(payload, "actor")
    provenance = get_dict(payload, "provenance")
    actor_id = get_text(actor, "id")
    if not actor_id:
        issues.append(issue("missing_identity_binding", "actor.id", "actor.id is required"))
    for field in ("type", "name", "runtime"):
        if not get_text(actor, field):
            issues.append(
                issue(
                    "missing_identity_binding",
                    f"actor.{field}",
                    f"actor.{field} is required",
                )
            )
    actor_ref = get_text(provenance, "actor_ref")
    if not actor_ref:
        issues.append(
            issue(
                "missing_identity_binding",
                "provenance.actor_ref",
                "provenance.actor_ref is required",
            )
        )
    elif actor_id and actor_ref != actor_id:
        issues.append(
            issue(
                "broken_identity_binding",
                "provenance.actor_ref",
                "provenance.actor_ref must match actor.id",
            )
        )
    return issues


def check_target_binding(payload: dict[str, Any]) -> list[dict[str, str]]:
    issues: list[dict[str, str]] = []
    subject = get_dict(payload, "subject")
    operation = get_dict(payload, "operation")
    provenance = get_dict(payload, "provenance")
    evidence = get_dict(payload, "evidence")
    subject_id = get_text(subject, "id")
    if not subject_id:
        issues.append(issue("missing_target_binding", "subject.id", "subject.id is required"))
    for field in ("type", "digest", "locator"):
        if not get_text(subject, field):
            issues.append(
                issue(
                    "missing_target_binding",
                    f"subject.{field}",
                    f"subject.{field} is required",
                )
            )
    for path_name, container, field in (
        ("operation.subject_ref", operation, "subject_ref"),
        ("provenance.subject_ref", provenance, "subject_ref"),
        ("evidence.subject_ref", evidence, "subject_ref"),
    ):
        value = get_text(container, field)
        if not value:
            issues.append(issue("missing_target_binding", path_name, f"{path_name} is required"))
        elif subject_id and value != subject_id:
            issues.append(
                issue("broken_target_binding", path_name, f"{path_name} must match subject.id")
            )
    return issues


def check_operation_semantics(payload: dict[str, Any]) -> list[dict[str, str]]:
    issues: list[dict[str, str]] = []
    operation = get_dict(payload, "operation")
    result = get_dict(operation, "result")
    op_id = get_text(operation, "id")
    op_type = get_text(operation, "type")
    if not op_id:
        issues.append(
            issue("missing_operation_semantics", "operation.id", "operation.id is required")
        )
    if not op_type:
        issues.append(
            issue("missing_operation_semantics", "operation.type", "operation.type is required")
        )
    elif op_type.lower() in GENERIC_OPERATION_TYPES:
        issues.append(
            issue(
                "ambiguous_operation_semantics",
                "operation.type",
                "operation.type is too generic for boundary-level review",
            )
        )
    status = get_text(result, "status")
    if not status:
        issues.append(
            issue("missing_operation_semantics", "operation.result.status", "status is required")
        )
    if not get_list(operation, "input_refs"):
        issues.append(
            issue(
                "missing_operation_semantics",
                "operation.input_refs",
                "at least one input ref is required",
            )
        )
    if not get_list(operation, "output_refs"):
        issues.append(
            issue(
                "missing_operation_semantics",
                "operation.output_refs",
                "at least one output ref is required",
            )
        )
    return issues


def check_policy_linkage(payload: dict[str, Any]) -> list[dict[str, str]]:
    issues: list[dict[str, str]] = []
    policy = get_dict(payload, "policy")
    operation = get_dict(payload, "operation")
    evidence = get_dict(payload, "evidence")
    validation = get_dict(payload, "validation")
    constraints = get_list(payload, "constraints")
    policy_id = get_text(policy, "id")
    if not policy_id:
        issues.append(issue("missing_policy_linkage", "policy.id", "policy.id is required"))
    if not get_text(policy, "name"):
        issues.append(issue("missing_policy_linkage", "policy.name", "policy.name is required"))
    constraint_refs = get_list(policy, "constraint_refs")
    if not constraint_refs:
        issues.append(
            issue(
                "missing_policy_linkage",
                "policy.constraint_refs",
                "policy.constraint_refs is required",
            )
        )
    constraint_ids = {get_text(item, "id") for item in constraints if isinstance(item, dict)}
    for index, ref in enumerate(constraint_refs):
        if isinstance(ref, str) and ref and ref in constraint_ids:
            continue
        issues.append(
            issue(
                "broken_policy_linkage",
                f"policy.constraint_refs[{index}]",
                "constraint ref does not resolve locally",
            )
        )
    for path_name, container, field in (
        ("operation.policy_ref", operation, "policy_ref"),
        ("evidence.policy_ref", evidence, "policy_ref"),
        ("validation.policy_ref", validation, "policy_ref"),
    ):
        value = get_text(container, field)
        if not value:
            issues.append(issue("missing_policy_linkage", path_name, f"{path_name} is required"))
        elif policy_id and value != policy_id:
            issues.append(
                issue("broken_policy_linkage", path_name, f"{path_name} must match policy.id")
            )
    return issues


def check_evidence_continuity(payload: dict[str, Any]) -> list[dict[str, str]]:
    issues: list[dict[str, str]] = []
    operation = get_dict(payload, "operation")
    evidence = get_dict(payload, "evidence")
    provenance = get_dict(payload, "provenance")
    validation = get_dict(payload, "validation")
    reference_map = build_reference_map(payload)
    if not get_text(evidence, "id"):
        issues.append(issue("broken_evidence_continuity", "evidence.id", "evidence.id is required"))
    if get_text(evidence, "operation_ref") != get_text(operation, "id"):
        issues.append(
            issue(
                "broken_evidence_continuity",
                "evidence.operation_ref",
                "evidence.operation_ref must match operation.id",
            )
        )
    for list_name, expected_role in (("input_refs", "input"), ("output_refs", "output")):
        refs = get_list(operation, list_name)
        for index, ref_id in enumerate(refs):
            if not isinstance(ref_id, str) or not ref_id:
                issues.append(
                    issue(
                        "broken_evidence_continuity",
                        f"operation.{list_name}[{index}]",
                        "reference id must be a non-empty string",
                    )
                )
                continue
            reference = reference_map.get(ref_id)
            if reference is None:
                issues.append(
                    issue(
                        "broken_evidence_continuity",
                        f"operation.{list_name}[{index}]",
                        "reference does not resolve in evidence.references",
                    )
                )
                continue
            if get_text(reference, "role") != expected_role:
                issues.append(
                    issue(
                        "broken_evidence_continuity",
                        f"evidence.references[{ref_id}]",
                        f"reference role must be {expected_role!r}",
                    )
                )
            for field in ("object_id", "digest", "locator"):
                if not get_text(reference, field):
                    issues.append(
                        issue(
                            "broken_evidence_continuity",
                            f"evidence.references[{ref_id}].{field}",
                            f"reference {field} is required",
                        )
                    )
    if get_list(provenance, "input_refs") != get_list(operation, "input_refs"):
        issues.append(
            issue(
                "broken_evidence_continuity",
                "provenance.input_refs",
                "provenance.input_refs must match operation.input_refs",
            )
        )
    if get_list(provenance, "output_refs") != get_list(operation, "output_refs"):
        issues.append(
            issue(
                "broken_evidence_continuity",
                "provenance.output_refs",
                "provenance.output_refs must match operation.output_refs",
            )
        )
    if get_text(validation, "evidence_ref") != get_text(evidence, "id"):
        issues.append(
            issue(
                "broken_evidence_continuity",
                "validation.evidence_ref",
                "validation.evidence_ref must match evidence.id",
            )
        )
    if get_text(validation, "provenance_ref") != get_text(provenance, "id"):
        issues.append(
            issue(
                "broken_evidence_continuity",
                "validation.provenance_ref",
                "validation.provenance_ref must match provenance.id",
            )
        )
    return issues


def check_validation_declaration(payload: dict[str, Any]) -> list[dict[str, str]]:
    issues: list[dict[str, str]] = []
    validation = get_dict(payload, "validation")
    required_fields = ("id", "validator", "method", "status")
    for field in required_fields:
        if not get_text(validation, field):
            issues.append(
                issue(
                    "missing_validation_declaration",
                    f"validation.{field}",
                    f"validation.{field} is required",
                )
            )
    return issues


def check_outcome_presence(payload: dict[str, Any]) -> list[dict[str, str]]:
    issues: list[dict[str, str]] = []
    operation = get_dict(payload, "operation")
    reference_map = build_reference_map(payload)
    result = get_dict(operation, "result")
    status = get_text(result, "status")
    input_refs = get_list(operation, "input_refs")
    output_refs = get_list(operation, "output_refs")
    if status not in {"succeeded", "failed"}:
        issues.append(
            issue(
                "missing_outcome_presence",
                "operation.result.status",
                "status must be 'succeeded' or 'failed'",
            )
        )
    if not get_text(result, "summary"):
        issues.append(
            issue(
                "missing_outcome_presence",
                "operation.result.summary",
                "summary is required for outcome review",
            )
        )
    elif get_text(result, "summary").lower() in GENERIC_RESULT_SUMMARIES:
        issues.append(
            issue(
                "ambiguous_outcome_presence",
                "operation.result.summary",
                "result.summary is too generic for outcome-level review",
            )
        )
    if status == "succeeded" and not output_refs:
        issues.append(
            issue(
                "outcome_unverifiable",
                "operation.output_refs",
                "succeeded operations must expose at least one output ref",
            )
        )
    if status == "succeeded" and output_refs:
        input_signatures: set[tuple[str, str, str]] = set()
        output_signatures: set[tuple[str, str, str]] = set()
        resolved_all_outputs = True
        for ref_id in input_refs:
            reference = reference_map.get(ref_id)
            if reference is None:
                continue
            signature = (
                get_text(reference, "object_id"),
                get_text(reference, "digest"),
                get_text(reference, "locator"),
            )
            if all(signature):
                input_signatures.add(signature)
        for ref_id in output_refs:
            reference = reference_map.get(ref_id)
            if reference is None:
                resolved_all_outputs = False
                continue
            signature = (
                get_text(reference, "object_id"),
                get_text(reference, "digest"),
                get_text(reference, "locator"),
            )
            if all(signature):
                output_signatures.add(signature)
        if (
            resolved_all_outputs
            and output_signatures
            and output_signatures.issubset(input_signatures)
        ):
            issues.append(
                issue(
                    "outcome_unverifiable",
                    "operation.output_refs",
                    "succeeded operation does not identify any distinguishable output object",
                )
            )
    return issues


def check_temporal_sanity(payload: dict[str, Any]) -> list[dict[str, str]]:
    issues: list[dict[str, str]] = []
    raw_timestamp = get_text(payload, "timestamp")
    parsed = parse_timestamp(raw_timestamp)
    if not raw_timestamp:
        issues.append(issue("temporal_inconsistency", "timestamp", "timestamp is required"))
        return issues
    if parsed is None:
        issues.append(
            issue(
                "temporal_inconsistency",
                "timestamp",
                "timestamp must be a parseable ISO 8601 datetime",
            )
        )
        return issues
    now = datetime.now(timezone.utc)
    if parsed > now + timedelta(days=1):
        issues.append(
            issue(
                "temporal_inconsistency",
                "timestamp",
                "timestamp is implausibly far in the future",
            )
        )
    if parsed < datetime(2000, 1, 1, tzinfo=timezone.utc):
        issues.append(
            issue(
                "temporal_inconsistency",
                "timestamp",
                "timestamp is implausibly old for the current profile line",
            )
        )
    return issues


def check_implementation_coupling(payload: dict[str, Any]) -> list[dict[str, str]]:
    issues: list[dict[str, str]] = []
    subject = get_dict(payload, "subject")
    evidence = get_dict(payload, "evidence")
    validation = get_dict(payload, "validation")

    candidate_paths: list[tuple[str, str]] = []
    candidate_paths.append(("subject.locator", get_text(subject, "locator")))
    candidate_paths.append(("validation.validator", get_text(validation, "validator")))

    for index, item in enumerate(get_list(evidence, "references")):
        if isinstance(item, dict):
            candidate_paths.append(
                (f"evidence.references[{index}].locator", get_text(item, "locator"))
            )
    for index, item in enumerate(get_list(evidence, "artifacts")):
        if isinstance(item, dict):
            candidate_paths.append(
                (f"evidence.artifacts[{index}].locator", get_text(item, "locator"))
            )

    for path_name, value in candidate_paths:
        if value and is_local_marker(value):
            issues.append(
                issue(
                    "implementation_coupling_marker",
                    path_name,
                    "value appears coupled to a local or implementation-specific environment",
                )
            )
    return issues


def validate_payload(payload: dict[str, Any]) -> list[dict[str, str]]:
    checks = (
        check_profile_identity,
        check_identity_binding,
        check_target_binding,
        check_operation_semantics,
        check_policy_linkage,
        check_evidence_continuity,
        check_validation_declaration,
        check_outcome_presence,
        check_temporal_sanity,
        check_implementation_coupling,
    )
    issues: list[dict[str, str]] = []
    for check in checks:
        issues.extend(check(payload))
    return issues


def render(path: Path, issues: list[dict[str, str]]) -> list[str]:
    status = "PASS" if not issues else "FAIL"
    lines = [f"{status} {path} ({len(issues)} issue(s))"]
    for item in issues:
        lines.append(f"- [{item['label']}] {item['path']}: {item['message']}")
    return lines


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Check minimal operation-accountability boundary conditions."
    )
    parser.add_argument("paths", nargs="+", help="JSON files to check")
    args = parser.parse_args(argv)

    exit_code = 0
    for raw_path in args.paths:
        path = Path(raw_path)
        try:
            payload = load_payload(path)
            issues = validate_payload(payload)
        except ValueError as exc:
            issues = [issue("invalid_input", "root", str(exc))]
        print("\n".join(render(path, issues)))
        if issues:
            exit_code = 1
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
