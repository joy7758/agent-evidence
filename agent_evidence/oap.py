from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

PROFILE_NAME = "execution-evidence-operation-accountability-profile"
PROFILE_VERSION = "0.1"
ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schema" / f"{PROFILE_NAME}-v{PROFILE_VERSION}.schema.json"


def load_profile(path: str | Path) -> dict[str, Any]:
    try:
        payload = json.loads(Path(path).read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"invalid JSON profile: {path}") from exc
    if not isinstance(payload, dict):
        raise ValueError("profile payload must be a JSON object")
    return payload


def canonical_json_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
    ).encode("utf-8")


def sha256_digest(value: Any) -> str:
    return "sha256:" + hashlib.sha256(canonical_json_bytes(value)).hexdigest()


def statement_core(profile: dict[str, Any]) -> dict[str, Any]:
    return {
        "actor": profile["actor"],
        "subject": profile["subject"],
        "operation": profile["operation"],
        "policy": profile["policy"],
        "constraints": profile["constraints"],
        "provenance": profile["provenance"],
    }


def recompute_integrity(profile: dict[str, Any]) -> dict[str, str]:
    evidence = profile["evidence"]
    return {
        "references_digest": sha256_digest(evidence["references"]),
        "artifacts_digest": sha256_digest(evidence["artifacts"]),
        "statement_digest": sha256_digest(statement_core(profile)),
    }


def with_recomputed_integrity(profile: dict[str, Any]) -> dict[str, Any]:
    updated = copy.deepcopy(profile)
    updated["evidence"]["integrity"] = recompute_integrity(updated)
    return updated


def _issue(stage: str, code: str, path: str, message: str) -> dict[str, str]:
    return {
        "stage": stage,
        "code": code,
        "path": path,
        "message": message,
    }


def _validate_schema(
    profile: dict[str, Any], schema_path: str | Path = SCHEMA_PATH
) -> list[dict[str, str]]:
    schema = json.loads(Path(schema_path).read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema)
    issues: list[dict[str, str]] = []
    for error in sorted(validator.iter_errors(profile), key=lambda item: list(item.path)):
        path = ".".join(str(part) for part in error.path) or "root"
        issues.append(_issue("schema", "schema_violation", path, error.message))
    return issues


def _duplicate_ids(values: list[str], stage: str, code: str, path: str) -> list[dict[str, str]]:
    seen: set[str] = set()
    issues: list[dict[str, str]] = []
    for value in values:
        if value in seen:
            issues.append(_issue(stage, code, path, f"duplicate identifier found: {value}"))
        seen.add(value)
    return issues


def _validate_reference_closure(profile: dict[str, Any]) -> list[dict[str, str]]:
    issues: list[dict[str, str]] = []
    actor_id = profile["actor"]["id"]
    subject_id = profile["subject"]["id"]
    operation_id = profile["operation"]["id"]
    policy_id = profile["policy"]["id"]
    provenance_id = profile["provenance"]["id"]
    evidence_id = profile["evidence"]["id"]

    constraint_ids = [constraint["id"] for constraint in profile["constraints"]]
    reference_ids = [reference["ref_id"] for reference in profile["evidence"]["references"]]

    issues.extend(
        _duplicate_ids(
            constraint_ids,
            "references",
            "duplicate_constraint_id",
            "constraints",
        )
    )
    issues.extend(
        _duplicate_ids(
            reference_ids,
            "references",
            "duplicate_reference_id",
            "evidence.references",
        )
    )

    constraint_id_set = set(constraint_ids)
    reference_id_set = set(reference_ids)

    if profile["operation"]["subject_ref"] != subject_id:
        issues.append(
            _issue(
                "references",
                "unresolved_subject_ref",
                "operation.subject_ref",
                "operation.subject_ref must resolve to subject.id.",
            )
        )
    if profile["operation"]["policy_ref"] != policy_id:
        issues.append(
            _issue(
                "references",
                "unresolved_policy_ref",
                "operation.policy_ref",
                "operation.policy_ref must resolve to policy.id.",
            )
        )
    for index, value in enumerate(profile["policy"]["constraint_refs"]):
        if value not in constraint_id_set:
            issues.append(
                _issue(
                    "references",
                    "unresolved_constraint_ref",
                    f"policy.constraint_refs[{index}]",
                    "policy constraint ref does not resolve to constraints[].id.",
                )
            )

    for index, value in enumerate(profile["operation"]["input_refs"]):
        if value not in reference_id_set:
            issues.append(
                _issue(
                    "references",
                    "unresolved_input_ref",
                    f"operation.input_refs[{index}]",
                    "operation input ref does not resolve to evidence.references[].ref_id.",
                )
            )
    for index, value in enumerate(profile["operation"]["output_refs"]):
        if value not in reference_id_set:
            issues.append(
                _issue(
                    "references",
                    "unresolved_output_ref",
                    f"operation.output_refs[{index}]",
                    "operation output ref does not resolve to evidence.references[].ref_id.",
                )
            )

    if profile["provenance"]["actor_ref"] != actor_id:
        issues.append(
            _issue(
                "references",
                "unresolved_actor_ref",
                "provenance.actor_ref",
                "provenance.actor_ref must resolve to actor.id.",
            )
        )
    if profile["provenance"]["operation_ref"] != operation_id:
        issues.append(
            _issue(
                "references",
                "unresolved_operation_ref",
                "provenance.operation_ref",
                "provenance.operation_ref must resolve to operation.id.",
            )
        )
    if profile["provenance"]["subject_ref"] != subject_id:
        issues.append(
            _issue(
                "references",
                "unresolved_provenance_subject_ref",
                "provenance.subject_ref",
                "provenance.subject_ref must resolve to subject.id.",
            )
        )
    if profile["evidence"]["subject_ref"] != subject_id:
        issues.append(
            _issue(
                "references",
                "unresolved_evidence_subject_ref",
                "evidence.subject_ref",
                "evidence.subject_ref must resolve to subject.id.",
            )
        )
    if profile["evidence"]["operation_ref"] != operation_id:
        issues.append(
            _issue(
                "references",
                "unresolved_evidence_operation_ref",
                "evidence.operation_ref",
                "evidence.operation_ref must resolve to operation.id.",
            )
        )
    if profile["evidence"]["policy_ref"] != policy_id:
        issues.append(
            _issue(
                "references",
                "unresolved_evidence_policy_ref",
                "evidence.policy_ref",
                "evidence.policy_ref must resolve to policy.id.",
            )
        )

    if profile["validation"]["evidence_ref"] != evidence_id:
        issues.append(
            _issue(
                "references",
                "unresolved_validation_evidence_ref",
                "validation.evidence_ref",
                "validation.evidence_ref must resolve to evidence.id.",
            )
        )
    if profile["validation"]["provenance_ref"] != provenance_id:
        issues.append(
            _issue(
                "references",
                "unresolved_validation_provenance_ref",
                "validation.provenance_ref",
                "validation.provenance_ref must resolve to provenance.id.",
            )
        )
    if profile["validation"]["policy_ref"] != policy_id:
        issues.append(
            _issue(
                "references",
                "unresolved_validation_policy_ref",
                "validation.policy_ref",
                "validation.policy_ref must resolve to policy.id.",
            )
        )
    return issues


def _validate_link_consistency(profile: dict[str, Any]) -> list[dict[str, str]]:
    issues: list[dict[str, str]] = []
    reference_roles = {
        reference["ref_id"]: reference["role"] for reference in profile["evidence"]["references"]
    }
    reference_object_ids = {
        reference["ref_id"]: reference["object_id"]
        for reference in profile["evidence"]["references"]
    }
    subject_id = profile["subject"]["id"]

    for index, value in enumerate(profile["operation"]["input_refs"]):
        if reference_roles.get(value) not in (None, "input"):
            issues.append(
                _issue(
                    "consistency",
                    "input_ref_role_mismatch",
                    f"operation.input_refs[{index}]",
                    "operation input refs must point to evidence references with role input.",
                )
            )
    for index, value in enumerate(profile["operation"]["output_refs"]):
        if reference_roles.get(value) not in (None, "output"):
            issues.append(
                _issue(
                    "consistency",
                    "output_ref_role_mismatch",
                    f"operation.output_refs[{index}]",
                    "operation output refs must point to evidence references with role output.",
                )
            )

    if profile["provenance"]["input_refs"] != profile["operation"]["input_refs"]:
        issues.append(
            _issue(
                "consistency",
                "provenance_input_refs_mismatch",
                "provenance.input_refs",
                "provenance.input_refs must match operation.input_refs.",
            )
        )
    if profile["provenance"]["output_refs"] != profile["operation"]["output_refs"]:
        issues.append(
            _issue(
                "consistency",
                "provenance_output_refs_mismatch",
                "provenance.output_refs",
                "provenance.output_refs must match operation.output_refs.",
            )
        )

    policy_refs = {
        "operation.policy_ref": profile["operation"]["policy_ref"],
        "evidence.policy_ref": profile["evidence"]["policy_ref"],
        "validation.policy_ref": profile["validation"]["policy_ref"],
    }
    if len(set(policy_refs.values())) != 1:
        issues.append(
            _issue(
                "consistency",
                "policy_ref_mismatch",
                ",".join(policy_refs.keys()),
                "operation, evidence, and validation must carry the same policy ref.",
            )
        )

    if profile["evidence"]["operation_ref"] != profile["provenance"]["operation_ref"]:
        issues.append(
            _issue(
                "consistency",
                "operation_ref_mismatch",
                "evidence.operation_ref",
                "evidence.operation_ref must match provenance.operation_ref.",
            )
        )
    if profile["evidence"]["subject_ref"] != profile["provenance"]["subject_ref"]:
        issues.append(
            _issue(
                "consistency",
                "subject_ref_mismatch",
                "evidence.subject_ref",
                "evidence.subject_ref must match provenance.subject_ref.",
            )
        )

    input_refs = profile["operation"]["input_refs"]
    if not any(reference_object_ids.get(ref_id) == subject_id for ref_id in input_refs):
        issues.append(
            _issue(
                "consistency",
                "subject_input_reference_missing",
                "operation.input_refs",
                "at least one input ref must point to the subject object.",
            )
        )
    return issues


def _validate_integrity(profile: dict[str, Any]) -> list[dict[str, str]]:
    issues: list[dict[str, str]] = []
    expected = recompute_integrity(profile)
    actual = profile["evidence"]["integrity"]

    for field in ("references_digest", "artifacts_digest", "statement_digest"):
        if actual.get(field) != expected[field]:
            issues.append(
                _issue(
                    "integrity",
                    f"{field}_mismatch",
                    f"evidence.integrity.{field}",
                    f"{field} does not match the canonical recomputed digest.",
                )
            )
    return issues


def _trust_binding_targets(profile: dict[str, Any]) -> dict[str, str]:
    targets = {
        profile["statement_id"]: recompute_integrity(profile)["statement_digest"],
    }
    for artifact in profile["evidence"]["artifacts"]:
        targets[artifact["artifact_id"]] = artifact["digest"]
    return targets


def _validate_trust_bindings(profile: dict[str, Any]) -> list[dict[str, str]]:
    bindings = profile["validation"].get("trust_bindings") or []
    if not bindings:
        return []

    issues = _duplicate_ids(
        [binding["binding_id"] for binding in bindings],
        "trust",
        "duplicate_trust_binding_id",
        "validation.trust_bindings",
    )
    targets = _trust_binding_targets(profile)

    for index, binding in enumerate(bindings):
        target_ref = binding["target_ref"]
        if target_ref not in targets:
            issues.append(
                _issue(
                    "trust",
                    "unresolved_trust_binding_target_ref",
                    f"validation.trust_bindings[{index}].target_ref",
                    "trust binding target_ref must resolve to statement_id or "
                    "evidence.artifacts[].artifact_id.",
                )
            )
            continue
        if binding["target_digest"] != targets[target_ref]:
            issues.append(
                _issue(
                    "trust",
                    "trust_binding_target_digest_mismatch",
                    f"validation.trust_bindings[{index}].target_digest",
                    "trust binding target_digest does not match the resolved local target.",
                )
            )
    return issues


def build_validation_report(
    profile: dict[str, Any],
    *,
    schema_path: str | Path | None = None,
    source: str | None = None,
) -> dict[str, Any]:
    resolved_schema_path = schema_path or SCHEMA_PATH
    schema_issues = _validate_schema(profile, resolved_schema_path)
    reference_issues: list[dict[str, str]] = []
    consistency_issues: list[dict[str, str]] = []
    integrity_issues: list[dict[str, str]] = []
    trust_issues: list[dict[str, str]] = []

    if not schema_issues:
        reference_issues = _validate_reference_closure(profile)
    if not schema_issues and not reference_issues:
        consistency_issues = _validate_link_consistency(profile)
    if not schema_issues and not reference_issues and not consistency_issues:
        integrity_issues = _validate_integrity(profile)
    if (
        not schema_issues
        and not reference_issues
        and not consistency_issues
        and not integrity_issues
    ):
        trust_issues = _validate_trust_bindings(profile)

    stages = [
        {"name": "schema", "ok": not schema_issues, "issues": schema_issues},
        {"name": "references", "ok": not reference_issues, "issues": reference_issues},
        {"name": "consistency", "ok": not consistency_issues, "issues": consistency_issues},
        {"name": "integrity", "ok": not integrity_issues, "issues": integrity_issues},
        {"name": "trust", "ok": not trust_issues, "issues": trust_issues},
    ]
    issues = [issue for stage in stages for issue in stage["issues"]]
    report = {
        "ok": not issues,
        "profile": f"{PROFILE_NAME}@{PROFILE_VERSION}",
        "source": source,
        "issue_count": len(issues),
        "stages": stages,
        "summary": render_summary_lines(
            {
                "ok": not issues,
                "profile": f"{PROFILE_NAME}@{PROFILE_VERSION}",
                "source": source,
                "issue_count": len(issues),
                "issues": issues,
            }
        ),
    }
    return report


def validate_profile_file(
    path: str | Path,
    *,
    schema_path: str | Path | None = None,
) -> dict[str, Any]:
    profile = load_profile(path)
    return build_validation_report(profile, schema_path=schema_path, source=str(path))


def render_summary_lines(report: dict[str, Any]) -> list[str]:
    source = report.get("source") or "<memory>"
    profile = report["profile"]
    if report["ok"]:
        return [f"PASS {profile} {source}"]

    lines = [f"FAIL {profile} {source} ({report['issue_count']} issue(s))"]
    for issue in report["issues"]:
        lines.append(f"[{issue['code']}] {issue['path']}: {issue['message']}")
    return lines
