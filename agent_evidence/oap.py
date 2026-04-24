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


def _stage(
    name: str,
    issues: list[dict[str, str]],
    *,
    skipped: bool = False,
    skip_reason: str | None = None,
) -> dict[str, Any]:
    stage: dict[str, Any] = {
        "name": name,
        "ok": not issues and not skipped,
        "issues": issues,
        "skipped": skipped,
    }
    if skip_reason is not None:
        stage["skip_reason"] = skip_reason
    return stage


def _flatten_issues(stages: list[dict[str, Any]]) -> list[dict[str, str]]:
    return [issue for stage in stages for issue in stage["issues"]]


def _issue_summary(issues: list[dict[str, str]]) -> dict[str, dict[str, int]]:
    by_stage: dict[str, int] = {}
    by_code: dict[str, int] = {}
    for issue in issues:
        by_stage[issue["stage"]] = by_stage.get(issue["stage"], 0) + 1
        by_code[issue["code"]] = by_code.get(issue["code"], 0) + 1
    return {
        "by_stage": dict(sorted(by_stage.items())),
        "by_code": dict(sorted(by_code.items())),
    }


def _skipped_stage(name: str, reason: str) -> dict[str, Any]:
    return _stage(name, [], skipped=True, skip_reason=reason)


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


def build_validation_report(
    profile: dict[str, Any],
    *,
    schema_path: str | Path | None = None,
    source: str | None = None,
    fail_fast: bool = True,
) -> dict[str, Any]:
    resolved_schema_path = schema_path or SCHEMA_PATH
    stages: list[dict[str, Any]] = []
    schema_issues = _validate_schema(profile, resolved_schema_path)
    stages.append(_stage("schema", schema_issues))

    if schema_issues:
        skip_reason = "Skipped because schema validation failed."
        stages.extend(
            [
                _skipped_stage("references", skip_reason),
                _skipped_stage("consistency", skip_reason),
                _skipped_stage("integrity", skip_reason),
            ]
        )
    else:
        reference_issues = _validate_reference_closure(profile)
        stages.append(_stage("references", reference_issues))

        if fail_fast and reference_issues:
            skip_reason = "Skipped because fail_fast stopped after reference validation failed."
            stages.extend(
                [
                    _skipped_stage("consistency", skip_reason),
                    _skipped_stage("integrity", skip_reason),
                ]
            )
        else:
            consistency_issues = _validate_link_consistency(profile)
            stages.append(_stage("consistency", consistency_issues))

            if fail_fast and consistency_issues:
                stages.append(
                    _skipped_stage(
                        "integrity",
                        "Skipped because fail_fast stopped after consistency validation failed.",
                    )
                )
            else:
                stages.append(_stage("integrity", _validate_integrity(profile)))

    issues = _flatten_issues(stages)
    issue_summary = _issue_summary(issues)
    report = {
        "ok": not issues,
        "profile": f"{PROFILE_NAME}@{PROFILE_VERSION}",
        "source": source,
        "fail_fast": fail_fast,
        "issue_count": len(issues),
        "primary_error_code": issues[0]["code"] if issues else None,
        "issues": issues,
        "issue_summary": issue_summary,
        "stages": stages,
        "summary": render_summary_lines(
            {
                "ok": not issues,
                "profile": f"{PROFILE_NAME}@{PROFILE_VERSION}",
                "source": source,
                "issue_count": len(issues),
                "issues": issues,
                "issue_summary": issue_summary,
            }
        ),
    }
    return report


def validate_profile_file(
    path: str | Path,
    *,
    schema_path: str | Path | None = None,
    fail_fast: bool = True,
) -> dict[str, Any]:
    profile = load_profile(path)
    return build_validation_report(
        profile,
        schema_path=schema_path,
        source=str(path),
        fail_fast=fail_fast,
    )


def render_summary_lines(report: dict[str, Any]) -> list[str]:
    source = report.get("source") or "<memory>"
    profile = report["profile"]
    if report["ok"]:
        return [f"PASS {profile} {source}"]

    issues = report.get("issues")
    if issues is None:
        issues = _flatten_issues(report.get("stages", []))

    lines = [f"FAIL {profile} {source} ({report['issue_count']} issue(s))"]
    issue_summary = report.get("issue_summary")
    if issue_summary and issue_summary.get("by_stage"):
        stage_counts = ", ".join(
            f"{stage}={count}" for stage, count in issue_summary["by_stage"].items()
        )
        lines.append(f"Stages with issues: {stage_counts}")
    for issue in issues:
        lines.append(f"[{issue['code']}] {issue['path']}: {issue['message']}")
    return lines
