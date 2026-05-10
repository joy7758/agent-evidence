from __future__ import annotations

import argparse
import json
import math
from datetime import datetime
from hashlib import sha256
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

from jsonschema import Draft202012Validator

from agent_evidence.media_profile import build_media_validation_report, load_media_profile

TIME_PROFILE = "aep-media-time-evidence@0.1"
TRACE_NAME = "aep-media-time-trace"
TRACE_VERSION = "0.1"
ROOT = Path(__file__).resolve().parents[1]
TRACE_SCHEMA_PATH = ROOT / "schema" / "aep_media_time_trace_v0_1.schema.json"


def _issue(code: str, path: str, message: str) -> dict[str, str]:
    return {
        "code": code,
        "message": message,
        "path": path,
    }


def _report(
    issues: list[dict[str, str]],
    *,
    media_profile_ok: bool,
    clock_trace_ok: bool,
) -> dict[str, Any]:
    ok = not issues
    return {
        "ok": ok,
        "profile": TIME_PROFILE,
        "media_profile_ok": media_profile_ok,
        "clock_trace_ok": clock_trace_ok,
        "issue_count": len(issues),
        "issues": issues,
        "summary": f"{'PASS' if ok else 'FAIL'} {TIME_PROFILE}",
    }


def _parse_utc(value: object) -> datetime:
    if not isinstance(value, str):
        raise ValueError("timestamp must be a string")
    normalized = value.replace("Z", "+00:00")
    return datetime.fromisoformat(normalized)


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


def _sha256_file(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def _load_trace(path: Path) -> tuple[dict[str, Any] | None, dict[str, str] | None]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return None, _issue("clock_trace_parse_error", str(path), f"invalid JSON: {exc}")
    if not isinstance(payload, dict):
        return None, _issue("clock_trace_parse_error", str(path), "clock trace must be an object.")
    return payload, None


def _trace_schema_issues(trace: dict[str, Any], *, path_prefix: str) -> list[dict[str, str]]:
    schema = json.loads(TRACE_SCHEMA_PATH.read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema)
    issues: list[dict[str, str]] = []
    for error in sorted(validator.iter_errors(trace), key=lambda item: list(item.path)):
        path = ".".join(str(part) for part in error.path) or "root"
        issues.append(
            _issue(
                "clock_trace_schema_violation",
                f"{path_prefix}.{path}",
                error.message,
            )
        )
    return issues


def _trace_profile_issues(trace: dict[str, Any], *, path_prefix: str) -> list[dict[str, str]]:
    profile = trace.get("profile")
    if not isinstance(profile, dict):
        return [
            _issue(
                "clock_trace_profile_mismatch",
                f"{path_prefix}.profile",
                "clock trace profile must be an object.",
            )
        ]
    if profile.get("name") != TRACE_NAME or profile.get("version") != TRACE_VERSION:
        return [
            _issue(
                "clock_trace_profile_mismatch",
                f"{path_prefix}.profile",
                "clock trace profile must be aep-media-time-trace@0.1.",
            )
        ]
    return []


def _validate_trace_window(
    trace: dict[str, Any],
    *,
    time_context: dict[str, Any],
    path_prefix: str,
) -> list[dict[str, str]]:
    try:
        collection_start = _parse_utc(trace["collection"]["start_utc"])
        collection_end = _parse_utc(trace["collection"]["end_utc"])
        context_start = _parse_utc(time_context["start_utc"])
        context_end = _parse_utc(time_context["end_utc"])
    except (KeyError, TypeError, ValueError) as exc:
        return [
            _issue(
                "clock_trace_window_mismatch",
                f"{path_prefix}.collection",
                f"clock trace and time_context windows must be parseable: {exc}",
            )
        ]

    if collection_start > context_start or collection_end < context_end:
        return [
            _issue(
                "clock_trace_window_mismatch",
                f"{path_prefix}.collection",
                "clock trace collection window must cover time_context start_utc/end_utc.",
            )
        ]
    return []


def _sample_metrics(
    trace: dict[str, Any],
    *,
    path_prefix: str,
) -> tuple[dict[str, float | int | bool] | None, list[dict[str, str]]]:
    samples = trace.get("samples")
    if not isinstance(samples, list) or not samples:
        return None, [
            _issue(
                "invalid_clock_trace_samples",
                f"{path_prefix}.samples",
                "clock trace samples must be a non-empty array.",
            )
        ]

    issues: list[dict[str, str]] = []
    offsets: list[float] = []
    previous_sample_time: datetime | None = None
    for index, sample in enumerate(samples):
        sample_path = f"{path_prefix}.samples[{index}]"
        if not isinstance(sample, dict):
            issues.append(
                _issue("invalid_clock_trace_samples", sample_path, "sample must be an object.")
            )
            continue

        try:
            sample_time = _parse_utc(sample.get("sample_utc"))
        except ValueError:
            issues.append(
                _issue(
                    "invalid_clock_trace_samples",
                    f"{sample_path}.sample_utc",
                    "sample_utc must be a parseable UTC ISO timestamp.",
                )
            )
            continue
        if previous_sample_time is not None and sample_time < previous_sample_time:
            issues.append(
                _issue(
                    "invalid_clock_trace_samples",
                    f"{sample_path}.sample_utc",
                    "sample_utc values must be non-decreasing.",
                )
            )
        previous_sample_time = sample_time

        offset = sample.get("offset_ns")
        if not isinstance(offset, int | float) or isinstance(offset, bool):
            issues.append(
                _issue(
                    "invalid_clock_trace_samples",
                    f"{sample_path}.offset_ns",
                    "offset_ns must be numeric.",
                )
            )
            continue
        offsets.append(float(offset))

        if sample.get("state") not in {"locked", "holdover", "unknown"}:
            issues.append(
                _issue(
                    "invalid_clock_trace_samples",
                    f"{sample_path}.state",
                    "state must be locked, holdover, or unknown.",
                )
            )

    if issues or not offsets:
        return None, issues

    max_abs_offset = max(abs(offset) for offset in offsets)
    max_jitter = 0.0
    if len(offsets) > 1:
        max_jitter = max(
            abs(offsets[index] - offsets[index - 1]) for index in range(1, len(offsets))
        )

    thresholds = trace.get("thresholds", {})
    max_abs_threshold = float(thresholds.get("max_abs_offset_ns", math.inf))
    max_jitter_threshold = float(thresholds.get("max_jitter_ns", math.inf))
    within_threshold = max_abs_offset <= max_abs_threshold and max_jitter <= max_jitter_threshold
    return (
        {
            "sample_count": len(offsets),
            "max_abs_offset_ns": max_abs_offset,
            "max_jitter_ns": max_jitter,
            "within_threshold": within_threshold,
        },
        [],
    )


def _close_number(left: object, right: float) -> bool:
    if not isinstance(left, int | float) or isinstance(left, bool):
        return False
    return math.isclose(float(left), right, rel_tol=0.0, abs_tol=1e-9)


def _validate_trace_summary_and_thresholds(
    trace: dict[str, Any],
    *,
    metrics: dict[str, float | int | bool],
    path_prefix: str,
) -> list[dict[str, str]]:
    issues: list[dict[str, str]] = []
    summary = trace.get("summary")
    thresholds = trace.get("thresholds")
    if not isinstance(summary, dict) or not isinstance(thresholds, dict):
        return [
            _issue(
                "clock_trace_summary_mismatch",
                f"{path_prefix}.summary",
                "clock trace summary and thresholds must be objects.",
            )
        ]

    if summary.get("sample_count") != metrics["sample_count"]:
        issues.append(
            _issue(
                "clock_trace_summary_mismatch",
                f"{path_prefix}.summary.sample_count",
                "summary sample_count does not match samples length.",
            )
        )
    if not _close_number(summary.get("max_abs_offset_ns"), float(metrics["max_abs_offset_ns"])):
        issues.append(
            _issue(
                "clock_trace_summary_mismatch",
                f"{path_prefix}.summary.max_abs_offset_ns",
                "summary max_abs_offset_ns does not match recomputed value.",
            )
        )
    if not _close_number(summary.get("max_jitter_ns"), float(metrics["max_jitter_ns"])):
        issues.append(
            _issue(
                "clock_trace_summary_mismatch",
                f"{path_prefix}.summary.max_jitter_ns",
                "summary max_jitter_ns does not match recomputed value.",
            )
        )
    if summary.get("within_threshold") is not metrics["within_threshold"]:
        issues.append(
            _issue(
                "clock_trace_summary_mismatch",
                f"{path_prefix}.summary.within_threshold",
                "summary within_threshold does not match recomputed threshold result.",
            )
        )

    max_abs_threshold = float(thresholds["max_abs_offset_ns"])
    max_jitter_threshold = float(thresholds["max_jitter_ns"])
    if float(metrics["max_abs_offset_ns"]) > max_abs_threshold:
        issues.append(
            _issue(
                "clock_offset_threshold_exceeded",
                f"{path_prefix}.thresholds.max_abs_offset_ns",
                "clock trace max_abs_offset_ns exceeds threshold.",
            )
        )
    if float(metrics["max_jitter_ns"]) > max_jitter_threshold:
        issues.append(
            _issue(
                "clock_jitter_threshold_exceeded",
                f"{path_prefix}.thresholds.max_jitter_ns",
                "clock trace max_jitter_ns exceeds threshold.",
            )
        )
    return issues


def _validate_primary_media_time_binding(profile: dict[str, Any]) -> list[dict[str, str]]:
    time_context = profile.get("time_context")
    if not isinstance(time_context, dict):
        return []
    time_context_id = time_context.get("id")
    issues: list[dict[str, str]] = []
    for index, artifact in enumerate(profile.get("media", {}).get("artifacts", [])):
        if not isinstance(artifact, dict) or artifact.get("role") != "primary_media":
            continue
        artifact_path = f"media.artifacts[{index}].time_context_ref"
        if "time_context_ref" not in artifact:
            issues.append(
                _issue(
                    "missing_media_time_context_ref",
                    artifact_path,
                    "primary_media artifact must declare time_context_ref.",
                )
            )
        elif artifact.get("time_context_ref") != time_context_id:
            issues.append(
                _issue(
                    "media_time_context_mismatch",
                    artifact_path,
                    "primary_media time_context_ref must equal time_context.id.",
                )
            )
    return issues


def _validate_clock_trace_refs(profile: dict[str, Any], *, base_dir: Path) -> list[dict[str, str]]:
    time_context = profile.get("time_context")
    if not isinstance(time_context, dict):
        return []

    refs = time_context.get("clock_trace_refs")
    if not isinstance(refs, list) or not refs:
        return [
            _issue(
                "missing_clock_trace_ref",
                "time_context.clock_trace_refs",
                "strict time validation requires at least one clock trace ref.",
            )
        ]

    artifacts = {
        artifact.get("id"): artifact
        for artifact in profile.get("media", {}).get("artifacts", [])
        if isinstance(artifact, dict)
    }
    issues: list[dict[str, str]] = []
    for ref_index, ref in enumerate(refs):
        ref_path = f"time_context.clock_trace_refs[{ref_index}]"
        artifact = artifacts.get(ref)
        if artifact is None:
            issues.append(
                _issue(
                    "unresolved_clock_trace_ref",
                    ref_path,
                    "clock trace ref does not resolve to media.artifacts[].id.",
                )
            )
            continue
        if artifact.get("role") != "clock_trace":
            issues.append(
                _issue(
                    "invalid_clock_trace_artifact_role",
                    ref_path,
                    "clock trace ref must resolve to an artifact with role clock_trace.",
                )
            )
            continue

        raw_path = artifact.get("path")
        if not isinstance(raw_path, str) or not _is_local_path(raw_path):
            issues.append(
                _issue(
                    "clock_trace_artifact_not_found",
                    ref_path,
                    "clock trace artifact path must be a local path.",
                )
            )
            continue
        trace_path = _resolve_artifact_path(raw_path, base_dir)
        if not trace_path.exists() or not trace_path.is_file():
            issues.append(
                _issue(
                    "clock_trace_artifact_not_found",
                    ref_path,
                    f"clock trace artifact file not found: {raw_path}",
                )
            )
            continue

        actual_digest = _sha256_file(trace_path)
        if actual_digest != artifact.get("sha256"):
            issues.append(
                _issue(
                    "clock_trace_hash_mismatch",
                    ref_path,
                    "clock trace artifact sha256 does not match the recomputed digest.",
                )
            )

        trace, parse_issue = _load_trace(trace_path)
        if parse_issue is not None or trace is None:
            issues.append(
                parse_issue or _issue("clock_trace_parse_error", ref_path, "parse failed.")
            )
            continue

        trace_prefix = ref_path
        issues.extend(_trace_profile_issues(trace, path_prefix=trace_prefix))
        issues.extend(_trace_schema_issues(trace, path_prefix=trace_prefix))
        issues.extend(
            _validate_trace_window(trace, time_context=time_context, path_prefix=trace_prefix)
        )
        metrics, sample_issues = _sample_metrics(trace, path_prefix=trace_prefix)
        issues.extend(sample_issues)
        if metrics is not None:
            issues.extend(
                _validate_trace_summary_and_thresholds(
                    trace,
                    metrics=metrics,
                    path_prefix=trace_prefix,
                )
            )
    return issues


def validate_media_time_profile_payload(payload: dict[str, Any], base_dir: Path) -> dict[str, Any]:
    base_report = build_media_validation_report(payload, source_path=base_dir / "statement.json")
    media_profile_ok = bool(base_report["ok"])
    base_issues = [dict(issue) for issue in base_report["issues"]]

    time_issues: list[dict[str, str]] = []
    time_issues.extend(_validate_clock_trace_refs(payload, base_dir=base_dir))
    time_issues.extend(_validate_primary_media_time_binding(payload))

    issues = base_issues + time_issues
    return _report(
        issues,
        media_profile_ok=media_profile_ok,
        clock_trace_ok=not time_issues,
    )


def validate_media_time_profile(statement_path: str | Path) -> dict[str, Any]:
    resolved_path = Path(statement_path)
    payload = load_media_profile(resolved_path)
    return validate_media_time_profile_payload(payload, resolved_path.resolve().parent)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate strict AEP-Media time evidence.")
    parser.add_argument("statement_json", type=Path)
    args = parser.parse_args(argv)

    try:
        report = validate_media_time_profile(args.statement_json)
    except ValueError as exc:
        parser.error(str(exc))

    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
