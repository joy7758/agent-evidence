from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

from jsonschema import Draft202012Validator

PROFILE_NAME = "aep-media-evidence-profile"
PROFILE_VERSION = "0.1"
PROFILE_LABEL = f"{PROFILE_NAME}@{PROFILE_VERSION}"
ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schema" / "aep_media_profile_v0_1.schema.json"

REQUIRED_TOP_LEVEL_FIELDS = (
    "profile",
    "statement_id",
    "timestamp",
    "actor",
    "subject",
    "operation",
    "policy",
    "constraints",
    "time_context",
    "media",
    "provenance",
    "evidence",
    "validation",
)


def load_media_profile(path: str | Path) -> dict[str, Any]:
    try:
        payload = json.loads(Path(path).read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"invalid JSON media profile: {path}") from exc
    if not isinstance(payload, dict):
        raise ValueError("media profile payload must be a JSON object")
    return payload


def _issue(code: str, path: str, message: str) -> dict[str, str]:
    return {
        "code": code,
        "message": message,
        "path": path,
    }


def _report(
    issues: list[dict[str, str]],
    *,
    source: str | None,
) -> dict[str, Any]:
    ok = not issues
    return {
        "ok": ok,
        "profile": PROFILE_LABEL,
        "source": source,
        "issue_count": len(issues),
        "issues": issues,
        "summary": f"{'PASS' if ok else 'FAIL'} {PROFILE_LABEL}",
    }


def _validate_required_fields(profile: dict[str, Any]) -> list[dict[str, str]]:
    issues: list[dict[str, str]] = []
    for field in REQUIRED_TOP_LEVEL_FIELDS:
        if field not in profile:
            code = "missing_time_context" if field == "time_context" else "missing_required_field"
            issues.append(_issue(code, field, f"required top-level field is missing: {field}"))
    return issues


def _validate_profile_identity(profile: dict[str, Any]) -> list[dict[str, str]]:
    issues: list[dict[str, str]] = []
    identity = profile.get("profile")
    if not isinstance(identity, dict):
        return [_issue("invalid_profile_identity", "profile", "profile must be an object.")]

    if identity.get("name") != PROFILE_NAME:
        issues.append(
            _issue(
                "invalid_profile_identity",
                "profile.name",
                f"profile.name must be {PROFILE_NAME}.",
            )
        )
    if identity.get("version") != PROFILE_VERSION:
        issues.append(
            _issue(
                "invalid_profile_identity",
                "profile.version",
                f"profile.version must be {PROFILE_VERSION}.",
            )
        )
    return issues


def _validate_schema(
    profile: dict[str, Any],
    schema_path: str | Path = SCHEMA_PATH,
) -> list[dict[str, str]]:
    schema = json.loads(Path(schema_path).read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema)
    issues: list[dict[str, str]] = []
    for error in sorted(validator.iter_errors(profile), key=lambda item: list(item.path)):
        path = ".".join(str(part) for part in error.path) or "root"
        issues.append(_issue("schema_violation", path, error.message))
    return issues


def _duplicate_id_issues(
    values: list[str],
    *,
    code: str,
    path: str,
) -> list[dict[str, str]]:
    issues: list[dict[str, str]] = []
    seen: set[str] = set()
    for value in values:
        if value in seen:
            issues.append(_issue(code, path, f"duplicate identifier found: {value}"))
        seen.add(value)
    return issues


def _validate_reference_closure(profile: dict[str, Any]) -> list[dict[str, str]]:
    issues: list[dict[str, str]] = []
    actor_id = profile["actor"]["id"]
    subject_id = profile["subject"]["id"]
    operation_id = profile["operation"]["id"]
    policy_id = profile["policy"]["id"]
    evidence_id = profile["evidence"]["id"]

    constraint_ids = [constraint["id"] for constraint in profile["constraints"]]
    artifact_ids = [artifact["id"] for artifact in profile["media"]["artifacts"]]
    evidence_artifact_refs = set(profile["evidence"]["artifact_refs"])

    constraint_id_set = set(constraint_ids)
    artifact_id_set = set(artifact_ids)
    evidence_ref_set = {evidence_id} | evidence_artifact_refs

    issues.extend(
        _duplicate_id_issues(
            constraint_ids,
            code="duplicate_constraint_id",
            path="constraints",
        )
    )
    issues.extend(
        _duplicate_id_issues(
            artifact_ids,
            code="duplicate_media_artifact_id",
            path="media.artifacts",
        )
    )

    if profile["operation"]["subject_ref"] != subject_id:
        issues.append(
            _issue(
                "unresolved_subject_ref",
                "operation.subject_ref",
                "operation.subject_ref must resolve to subject.id.",
            )
        )
    if profile["operation"]["policy_ref"] != policy_id:
        issues.append(
            _issue(
                "unresolved_policy_ref",
                "operation.policy_ref",
                "operation.policy_ref must resolve to policy.id.",
            )
        )

    for index, value in enumerate(profile["policy"]["constraint_refs"]):
        if value not in constraint_id_set:
            issues.append(
                _issue(
                    "unresolved_constraint_ref",
                    f"policy.constraint_refs[{index}]",
                    "policy constraint ref does not resolve to constraints[].id.",
                )
            )

    for index, value in enumerate(profile["operation"]["media_refs"]):
        if value not in artifact_id_set:
            issues.append(
                _issue(
                    "unresolved_media_ref",
                    f"operation.media_refs[{index}]",
                    "operation media ref does not resolve to media.artifacts[].id.",
                )
            )

    for index, value in enumerate(profile["operation"]["evidence_refs"]):
        if value not in evidence_ref_set:
            issues.append(
                _issue(
                    "unresolved_evidence_ref",
                    f"operation.evidence_refs[{index}]",
                    "operation evidence ref must resolve to evidence.id or evidence.artifact_refs.",
                )
            )

    if profile["provenance"]["actor_ref"] != actor_id:
        issues.append(
            _issue(
                "unresolved_actor_ref",
                "provenance.actor_ref",
                "provenance.actor_ref must resolve to actor.id.",
            )
        )
    if profile["provenance"]["subject_ref"] != subject_id:
        issues.append(
            _issue(
                "unresolved_provenance_subject_ref",
                "provenance.subject_ref",
                "provenance.subject_ref must resolve to subject.id.",
            )
        )
    if profile["provenance"]["operation_ref"] != operation_id:
        issues.append(
            _issue(
                "unresolved_operation_ref",
                "provenance.operation_ref",
                "provenance.operation_ref must resolve to operation.id.",
            )
        )

    for index, value in enumerate(profile["provenance"]["media_refs"]):
        if value not in artifact_id_set:
            issues.append(
                _issue(
                    "unresolved_media_ref",
                    f"provenance.media_refs[{index}]",
                    "provenance media ref does not resolve to media.artifacts[].id.",
                )
            )

    c2pa_manifest_ref = profile["provenance"].get("c2pa_manifest_ref")
    if c2pa_manifest_ref is not None and c2pa_manifest_ref not in artifact_id_set:
        issues.append(
            _issue(
                "unresolved_c2pa_manifest_ref",
                "provenance.c2pa_manifest_ref",
                "provenance.c2pa_manifest_ref must resolve to media.artifacts[].id.",
            )
        )

    for index, value in enumerate(profile["evidence"]["policy_refs"]):
        if value != policy_id:
            issues.append(
                _issue(
                    "unresolved_evidence_policy_ref",
                    f"evidence.policy_refs[{index}]",
                    "evidence policy ref must resolve to policy.id.",
                )
            )

    for index, value in enumerate(profile["evidence"]["artifact_refs"]):
        if value not in artifact_id_set:
            issues.append(
                _issue(
                    "unresolved_media_ref",
                    f"evidence.artifact_refs[{index}]",
                    "evidence artifact ref does not resolve to media.artifacts[].id.",
                )
            )

    return issues


def _validate_association_consistency(profile: dict[str, Any]) -> list[dict[str, str]]:
    issues: list[dict[str, str]] = []
    operation_media_refs = set(profile["operation"]["media_refs"])
    provenance_media_refs = set(profile["provenance"]["media_refs"])
    evidence_artifact_refs = set(profile["evidence"]["artifact_refs"])

    if operation_media_refs != provenance_media_refs:
        issues.append(
            _issue(
                "media_ref_mismatch",
                "provenance.media_refs",
                "provenance.media_refs must match operation.media_refs.",
            )
        )
    if not operation_media_refs.issubset(evidence_artifact_refs):
        issues.append(
            _issue(
                "evidence_artifact_refs_mismatch",
                "evidence.artifact_refs",
                "evidence.artifact_refs must include every operation media ref.",
            )
        )
    if profile["operation"]["policy_ref"] not in set(profile["evidence"]["policy_refs"]):
        issues.append(
            _issue(
                "policy_ref_mismatch",
                "evidence.policy_refs",
                "evidence.policy_refs must include operation.policy_ref.",
            )
        )
    return issues


def _parse_datetime(value: str) -> datetime:
    normalized = value.replace("Z", "+00:00")
    return datetime.fromisoformat(normalized)


def _validate_time_context(profile: dict[str, Any]) -> list[dict[str, str]]:
    issues: list[dict[str, str]] = []
    time_context = profile["time_context"]
    time_context_id = time_context["id"]

    try:
        start = _parse_datetime(time_context["start_utc"])
        end = _parse_datetime(time_context["end_utc"])
    except ValueError:
        issues.append(
            _issue(
                "invalid_time_range",
                "time_context",
                "time_context.start_utc and end_utc must be valid ISO datetimes.",
            )
        )
        return issues

    if end < start:
        issues.append(
            _issue(
                "invalid_time_range",
                "time_context.end_utc",
                "time_context.end_utc must not be earlier than start_utc.",
            )
        )

    for index, artifact in enumerate(profile["media"]["artifacts"]):
        if artifact["role"] != "primary_media":
            continue
        if artifact.get("time_context_ref") != time_context_id:
            issues.append(
                _issue(
                    "missing_media_time_context_ref",
                    f"media.artifacts[{index}].time_context_ref",
                    "primary_media artifact must reference time_context.id.",
                )
            )
    return issues


def _is_local_path(raw_path: str) -> bool:
    parsed = urlparse(raw_path)
    return parsed.scheme in ("", "file")


def _resolve_artifact_path(raw_path: str, base_dir: Path) -> Path:
    parsed = urlparse(raw_path)
    if parsed.scheme == "file":
        return Path(parsed.path)
    candidate = Path(raw_path)
    if candidate.is_absolute():
        return candidate
    return (base_dir / candidate).resolve()


def _validate_media_files(profile: dict[str, Any], *, base_dir: Path) -> list[dict[str, str]]:
    issues: list[dict[str, str]] = []
    for index, artifact in enumerate(profile["media"]["artifacts"]):
        raw_path = artifact["path"]
        if not _is_local_path(raw_path):
            continue

        artifact_path = _resolve_artifact_path(raw_path, base_dir)
        artifact_issue_path = f"media.artifacts[{index}]"
        if not artifact_path.exists():
            issues.append(
                _issue(
                    "media_artifact_not_found",
                    artifact_issue_path,
                    f"media artifact file not found: {raw_path}",
                )
            )
            continue
        if not artifact_path.is_file():
            issues.append(
                _issue(
                    "media_artifact_not_found",
                    artifact_issue_path,
                    f"media artifact path is not a file: {raw_path}",
                )
            )
            continue

        payload = artifact_path.read_bytes()
        actual_digest = hashlib.sha256(payload).hexdigest()
        if actual_digest != artifact["sha256"]:
            issues.append(
                _issue(
                    "media_hash_mismatch",
                    artifact_issue_path,
                    "media artifact sha256 does not match the recomputed digest.",
                )
            )

        actual_size = len(payload)
        if actual_size != artifact["size_bytes"]:
            issues.append(
                _issue(
                    "media_size_mismatch",
                    artifact_issue_path,
                    "media artifact size_bytes does not match the local file size.",
                )
            )

    return issues


def build_media_validation_report(
    profile: dict[str, Any],
    *,
    source_path: str | Path | None = None,
    schema_path: str | Path | None = None,
) -> dict[str, Any]:
    source = str(source_path) if source_path is not None else None
    base_dir = Path(source_path).resolve().parent if source_path is not None else Path.cwd()

    issues = _validate_required_fields(profile)
    if issues:
        return _report(issues, source=source)

    issues = _validate_profile_identity(profile)
    if issues:
        return _report(issues, source=source)

    issues = _validate_schema(profile, schema_path or SCHEMA_PATH)
    if issues:
        return _report(issues, source=source)

    issues = _validate_reference_closure(profile)
    if issues:
        return _report(issues, source=source)

    issues = _validate_association_consistency(profile)
    if issues:
        return _report(issues, source=source)

    issues = _validate_time_context(profile)
    if issues:
        return _report(issues, source=source)

    issues = _validate_media_files(profile, base_dir=base_dir)
    return _report(issues, source=source)


def validate_media_profile_file(
    path: str | Path,
    *,
    schema_path: str | Path | None = None,
) -> dict[str, Any]:
    profile = load_media_profile(path)
    return build_media_validation_report(profile, source_path=path, schema_path=schema_path)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate an AEP-Media Profile v0.1 JSON file.")
    parser.add_argument("profile_path", type=Path)
    parser.add_argument("--schema", dest="schema_path", type=Path)
    args = parser.parse_args(argv)

    try:
        report = validate_media_profile_file(args.profile_path, schema_path=args.schema_path)
    except ValueError as exc:
        parser.error(str(exc))

    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
