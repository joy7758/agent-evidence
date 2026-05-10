from __future__ import annotations

import argparse
import json
import re
import shutil
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path, PurePosixPath
from typing import Any
from urllib.parse import urlparse

from jsonschema import Draft202012Validator

from agent_evidence.media_profile import (
    PROFILE_LABEL as MEDIA_PROFILE_LABEL,
)
from agent_evidence.media_profile import (
    load_media_profile,
    validate_media_profile_file,
)
from agent_evidence.media_time import validate_media_time_profile

BUNDLE_NAME = "aep-media-bundle"
BUNDLE_VERSION = "0.1"
BUNDLE_PROFILE = f"{BUNDLE_NAME}@{BUNDLE_VERSION}"
ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schema" / "aep_media_bundle_v0_1.schema.json"

CHECKSUMS_PATH = "checksums.txt"
STATEMENT_PATH = "statement.json"
VALIDATION_REPORT_PATH = "validation-report.json"
SUMMARY_PATH = "summary.json"
ARTIFACTS_DIR = "artifacts"

PATH_ESCAPE_CODE = "bundle_path_escape"
CHECKSUM_CODES = {
    "bundle_manifest_not_found",
    "bundle_manifest_invalid",
    "bundle_statement_not_found",
    "bundle_artifact_not_found",
    "bundle_checksum_missing",
    "bundle_checksum_mismatch",
    "bundle_path_escape",
    "bundle_profile_mismatch",
}


class MediaBundleError(ValueError):
    """Raised when a media bundle cannot be built."""


def _issue(code: str, path: str, message: str) -> dict[str, str]:
    return {
        "code": code,
        "message": message,
        "path": path,
    }


def _write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _load_json(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise MediaBundleError(f"invalid JSON file: {path}") from exc
    if not isinstance(payload, dict):
        raise MediaBundleError(f"JSON file must contain an object: {path}")
    return payload


def _sha256_file(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def _utc_now() -> str:
    value = datetime.now(timezone.utc).replace(microsecond=0)
    return value.isoformat().replace("+00:00", "Z")


def _safe_name(value: str, *, fallback: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9._-]+", "-", value).strip(".-")
    return cleaned or fallback


def _unique_artifact_name(
    *,
    artifact_id: str,
    source_path: Path,
    used_names: set[str],
) -> str:
    safe_id = _safe_name(artifact_id, fallback="artifact")
    safe_basename = _safe_name(source_path.name, fallback="payload")
    candidate = f"{safe_id}-{safe_basename}"
    if candidate not in used_names:
        used_names.add(candidate)
        return candidate

    stem = Path(safe_basename).stem or "payload"
    suffix = Path(safe_basename).suffix
    counter = 2
    while True:
        candidate = f"{safe_id}-{stem}-{counter}{suffix}"
        if candidate not in used_names:
            used_names.add(candidate)
            return candidate
        counter += 1


def _is_local_source_path(raw_path: str) -> bool:
    parsed = urlparse(raw_path)
    return parsed.scheme in ("", "file")


def _resolve_source_path(raw_path: str, base_dir: Path) -> Path:
    parsed = urlparse(raw_path)
    if parsed.scheme == "file":
        return Path(parsed.path)
    candidate = Path(raw_path)
    if candidate.is_absolute():
        return candidate
    return (base_dir / candidate).resolve()


def _path_escape_issue(raw_path: object, path: str) -> dict[str, str] | None:
    if not isinstance(raw_path, str) or not raw_path:
        return _issue(PATH_ESCAPE_CODE, path, "bundle path must be a non-empty string.")
    if "\\" in raw_path:
        return _issue(PATH_ESCAPE_CODE, path, "bundle path must use POSIX separators.")

    posix_path = PurePosixPath(raw_path)
    if posix_path.is_absolute():
        return _issue(PATH_ESCAPE_CODE, path, "bundle path must be relative.")
    if ".." in posix_path.parts:
        return _issue(PATH_ESCAPE_CODE, path, "bundle path must not contain '..'.")
    return None


def _resolve_bundle_path(raw_path: str, bundle_dir: Path) -> Path:
    parts = PurePosixPath(raw_path).parts
    return bundle_dir.joinpath(*parts).resolve()


def _validate_bundle_relative_path(
    raw_path: object,
    *,
    bundle_dir: Path,
    path: str,
) -> tuple[Path | None, dict[str, str] | None]:
    path_issue = _path_escape_issue(raw_path, path)
    if path_issue is not None:
        return None, path_issue

    resolved = _resolve_bundle_path(str(raw_path), bundle_dir)
    try:
        resolved.relative_to(bundle_dir.resolve())
    except ValueError:
        return (
            None,
            _issue(PATH_ESCAPE_CODE, path, "bundle path resolves outside the bundle directory."),
        )
    return resolved, None


def _checksum_lines(entries: dict[str, str]) -> str:
    return "".join(
        f"{digest}  {relative_path}\n" for relative_path, digest in sorted(entries.items())
    )


def _read_checksums(path: Path) -> tuple[dict[str, str], list[dict[str, str]]]:
    if not path.exists():
        return {}, [
            _issue(
                "bundle_checksum_missing",
                CHECKSUMS_PATH,
                "checksums.txt is required for bundle verification.",
            )
        ]

    checksums: dict[str, str] = {}
    issues: list[dict[str, str]] = []
    for line_number, raw_line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        line = raw_line.strip()
        if not line:
            continue
        parts = line.split(None, 1)
        if len(parts) != 2 or not re.fullmatch(r"[0-9a-f]{64}", parts[0]):
            issues.append(
                _issue(
                    "bundle_manifest_invalid",
                    f"{CHECKSUMS_PATH}:{line_number}",
                    "checksum line must use '<sha256>  <relative_path>'.",
                )
            )
            continue
        checksums[parts[1].strip()] = parts[0]
    return checksums, issues


def _schema_issues(bundle: dict[str, Any]) -> list[dict[str, str]]:
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema)
    issues: list[dict[str, str]] = []
    for error in sorted(validator.iter_errors(bundle), key=lambda item: list(item.path)):
        path = ".".join(str(part) for part in error.path) or "bundle.json"
        issues.append(_issue("bundle_manifest_invalid", path, error.message))
    return issues


def build_media_bundle(statement_path: str | Path, bundle_dir: str | Path) -> dict[str, Any]:
    statement_source_path = Path(statement_path).resolve()
    output_dir = Path(bundle_dir).resolve()
    artifacts_dir = output_dir / ARTIFACTS_DIR
    statement = load_media_profile(statement_source_path)

    output_dir.mkdir(parents=True, exist_ok=True)
    artifacts_dir.mkdir(parents=True, exist_ok=True)

    artifact_entries: list[dict[str, Any]] = []
    used_names: set[str] = set()
    for index, artifact in enumerate(statement["media"]["artifacts"]):
        raw_artifact_path = artifact["path"]
        if not _is_local_source_path(raw_artifact_path):
            raise MediaBundleError(
                f"media artifact path must be local for bundle build: {raw_artifact_path}"
            )

        source_path = _resolve_source_path(raw_artifact_path, statement_source_path.parent)
        if not source_path.exists() or not source_path.is_file():
            raise MediaBundleError(f"media artifact not found: {raw_artifact_path}")

        target_name = _unique_artifact_name(
            artifact_id=artifact["id"],
            source_path=source_path,
            used_names=used_names,
        )
        relative_target = f"{ARTIFACTS_DIR}/{target_name}"
        target_path = output_dir / ARTIFACTS_DIR / target_name
        shutil.copyfile(source_path, target_path)

        digest = _sha256_file(target_path)
        size_bytes = target_path.stat().st_size
        artifact["path"] = relative_target
        artifact["sha256"] = digest
        artifact["size_bytes"] = size_bytes

        artifact_entries.append(
            {
                "id": artifact["id"],
                "role": artifact["role"],
                "path": relative_target,
                "sha256": digest,
                "size_bytes": size_bytes,
                "mime_type": artifact["mime_type"],
                "source_path": str(source_path),
            }
        )

        if index == 0 and artifact["role"] != "primary_media":
            # The profile allows multiple roles; no build policy depends on ordering.
            pass

    bundled_statement_path = output_dir / STATEMENT_PATH
    _write_json(bundled_statement_path, statement)

    validation_report = validate_media_profile_file(bundled_statement_path)
    validation_report_path = output_dir / VALIDATION_REPORT_PATH
    _write_json(validation_report_path, validation_report)

    statement_digest = _sha256_file(bundled_statement_path)
    bundle = {
        "profile": {
            "name": BUNDLE_NAME,
            "version": BUNDLE_VERSION,
        },
        "bundle_id": f"bundle:{statement.get('statement_id', 'aep-media')}",
        "created_utc": _utc_now(),
        "statement": {
            "path": STATEMENT_PATH,
            "sha256": statement_digest,
            "size_bytes": bundled_statement_path.stat().st_size,
            "profile": MEDIA_PROFILE_LABEL,
        },
        "artifacts": artifact_entries,
        "validation": {
            "path": VALIDATION_REPORT_PATH,
            "validator": "agent-evidence validate-media-profile",
            "expected_result": "pass",
        },
        "summary": {
            "path": SUMMARY_PATH,
        },
    }
    bundle_path = output_dir / "bundle.json"
    _write_json(bundle_path, bundle)

    checksum_entries = {
        "bundle.json": _sha256_file(bundle_path),
        STATEMENT_PATH: _sha256_file(bundled_statement_path),
    }
    for artifact_entry in artifact_entries:
        checksum_entries[artifact_entry["path"]] = _sha256_file(output_dir / artifact_entry["path"])
    (output_dir / CHECKSUMS_PATH).write_text(_checksum_lines(checksum_entries), encoding="utf-8")

    summary = {
        "ok": validation_report["ok"],
        "profile": BUNDLE_PROFILE,
        "bundle_id": bundle["bundle_id"],
        "artifact_count": len(artifact_entries),
        "media_profile_ok": validation_report["ok"],
        "summary": (
            f"PASS {BUNDLE_PROFILE} build"
            if validation_report["ok"]
            else f"FAIL {BUNDLE_PROFILE} build"
        ),
    }
    _write_json(output_dir / SUMMARY_PATH, summary)

    if not validation_report["ok"]:
        raise MediaBundleError("bundled statement failed media profile validation")
    return summary


def _validate_bundle_profile(bundle: dict[str, Any]) -> list[dict[str, str]]:
    profile = bundle.get("profile")
    if not isinstance(profile, dict):
        return [_issue("bundle_profile_mismatch", "profile", "bundle profile must be an object.")]

    if profile.get("name") != BUNDLE_NAME or profile.get("version") != BUNDLE_VERSION:
        return [
            _issue(
                "bundle_profile_mismatch",
                "profile",
                f"bundle profile must be {BUNDLE_PROFILE}.",
            )
        ]
    return []


def _declared_bundle_paths(bundle: dict[str, Any]) -> list[tuple[str, object, str]]:
    paths: list[tuple[str, object, str]] = [
        ("statement.path", bundle.get("statement", {}).get("path"), "statement"),
        ("validation.path", bundle.get("validation", {}).get("path"), "validation"),
        ("summary.path", bundle.get("summary", {}).get("path"), "summary"),
    ]
    for index, artifact in enumerate(bundle.get("artifacts", [])):
        if isinstance(artifact, dict):
            paths.append((f"artifacts[{index}].path", artifact.get("path"), "artifact"))
    return paths


def _load_bundle_manifest(bundle_dir: Path) -> tuple[dict[str, Any] | None, list[dict[str, str]]]:
    bundle_path = bundle_dir / "bundle.json"
    if not bundle_path.exists():
        return None, [
            _issue("bundle_manifest_not_found", "bundle.json", "bundle.json was not found.")
        ]
    try:
        bundle = _load_json(bundle_path)
    except MediaBundleError as exc:
        return None, [_issue("bundle_manifest_invalid", "bundle.json", str(exc))]
    return bundle, []


def _verify_declared_files(
    bundle: dict[str, Any],
    *,
    bundle_dir: Path,
) -> tuple[Path | None, list[dict[str, str]]]:
    issues: list[dict[str, str]] = []
    statement_path: Path | None = None

    for path_key, raw_path, kind in _declared_bundle_paths(bundle):
        resolved_path, path_issue = _validate_bundle_relative_path(
            raw_path,
            bundle_dir=bundle_dir,
            path=path_key,
        )
        if path_issue is not None:
            issues.append(path_issue)
            continue

        if kind == "statement":
            statement_path = resolved_path
            if not resolved_path or not resolved_path.exists():
                issues.append(
                    _issue(
                        "bundle_statement_not_found",
                        str(raw_path),
                        "bundled statement file was not found.",
                    )
                )
        elif kind == "artifact" and (not resolved_path or not resolved_path.exists()):
            issues.append(
                _issue(
                    "bundle_artifact_not_found",
                    str(raw_path),
                    "bundled artifact file was not found.",
                )
            )

    return statement_path, issues


def _verify_statement_artifact_paths(
    statement_path: Path,
    *,
    bundle_dir: Path,
) -> list[dict[str, str]]:
    issues: list[dict[str, str]] = []
    try:
        statement = load_media_profile(statement_path)
    except ValueError as exc:
        return [
            _issue(
                "media_profile_validation_failed",
                "statement.json",
                f"statement could not be loaded: {exc}",
            )
        ]

    for index, artifact in enumerate(statement.get("media", {}).get("artifacts", [])):
        if not isinstance(artifact, dict):
            continue
        _, path_issue = _validate_bundle_relative_path(
            artifact.get("path"),
            bundle_dir=bundle_dir,
            path=f"statement.media.artifacts[{index}].path",
        )
        if path_issue is not None:
            issues.append(path_issue)
    return issues


def _verify_checksums(
    bundle: dict[str, Any],
    *,
    bundle_dir: Path,
) -> list[dict[str, str]]:
    checksums, issues = _read_checksums(bundle_dir / CHECKSUMS_PATH)
    if issues:
        return issues

    expected_paths = {
        "bundle.json",
        str(bundle["statement"]["path"]),
        *(str(artifact["path"]) for artifact in bundle["artifacts"]),
    }
    for relative_path in sorted(expected_paths):
        if relative_path not in checksums:
            issues.append(
                _issue(
                    "bundle_checksum_missing",
                    relative_path,
                    "checksums.txt does not include this required bundle path.",
                )
            )

    for relative_path, expected_digest in checksums.items():
        resolved_path, path_issue = _validate_bundle_relative_path(
            relative_path,
            bundle_dir=bundle_dir,
            path=f"{CHECKSUMS_PATH}:{relative_path}",
        )
        if path_issue is not None:
            issues.append(path_issue)
            continue
        if resolved_path is None or not resolved_path.exists():
            issues.append(
                _issue(
                    "bundle_artifact_not_found",
                    relative_path,
                    "checksums.txt references a missing bundle file.",
                )
            )
            continue
        actual_digest = _sha256_file(resolved_path)
        if actual_digest != expected_digest:
            issues.append(
                _issue(
                    "bundle_checksum_mismatch",
                    relative_path,
                    "bundle file sha256 does not match checksums.txt.",
                )
            )
    return issues


def _media_profile_issues(statement_path: Path) -> tuple[bool, list[dict[str, str]]]:
    media_report = validate_media_profile_file(statement_path)
    if media_report["ok"]:
        return True, []

    issues = [
        _issue(
            "media_profile_validation_failed",
            "statement.json",
            "bundled statement failed AEP-Media Profile validation.",
        )
    ]
    for media_issue in media_report["issues"]:
        issues.append(
            _issue(
                media_issue["code"],
                f"statement.json:{media_issue['path']}",
                media_issue["message"],
            )
        )
    return False, issues


def _bundle_report(
    issues: list[dict[str, str]],
    *,
    media_profile_ok: bool,
    strict_time: bool = False,
    time_profile_report: dict[str, Any] | None = None,
) -> dict[str, Any]:
    ok = not issues
    bundle_checksum_ok = not any(issue["code"] in CHECKSUM_CODES for issue in issues)
    report = {
        "ok": ok,
        "profile": BUNDLE_PROFILE,
        "media_profile_ok": media_profile_ok,
        "bundle_checksum_ok": bundle_checksum_ok,
        "issue_count": len(issues),
        "issues": issues,
        "summary": f"{'PASS' if ok else 'FAIL'} {BUNDLE_PROFILE}",
    }
    if strict_time:
        report["strict_time"] = True
        report["time_profile_ok"] = bool(time_profile_report and time_profile_report.get("ok"))
        report["time_profile_report"] = time_profile_report
    return report


def verify_media_bundle(bundle_dir: str | Path, *, strict_time: bool = False) -> dict[str, Any]:
    resolved_bundle_dir = Path(bundle_dir).resolve()
    issues: list[dict[str, str]] = []
    media_profile_ok = False
    time_profile_report: dict[str, Any] | None = None

    bundle, manifest_issues = _load_bundle_manifest(resolved_bundle_dir)
    if bundle is None:
        return _bundle_report(
            manifest_issues,
            media_profile_ok=media_profile_ok,
            strict_time=strict_time,
            time_profile_report=time_profile_report,
        )

    profile_issues = _validate_bundle_profile(bundle)
    if profile_issues:
        return _bundle_report(
            profile_issues,
            media_profile_ok=media_profile_ok,
            strict_time=strict_time,
            time_profile_report=time_profile_report,
        )

    schema_issues = _schema_issues(bundle)
    if schema_issues:
        return _bundle_report(
            schema_issues,
            media_profile_ok=media_profile_ok,
            strict_time=strict_time,
            time_profile_report=time_profile_report,
        )

    statement_path, file_issues = _verify_declared_files(bundle, bundle_dir=resolved_bundle_dir)
    issues.extend(file_issues)

    if statement_path is not None and statement_path.exists():
        issues.extend(
            _verify_statement_artifact_paths(statement_path, bundle_dir=resolved_bundle_dir)
        )

    issues.extend(_verify_checksums(bundle, bundle_dir=resolved_bundle_dir))

    if statement_path is not None and statement_path.exists():
        media_profile_ok, media_issues = _media_profile_issues(statement_path)
        issues.extend(media_issues)

    if strict_time and statement_path is not None and statement_path.exists():
        time_profile_report = validate_media_time_profile(statement_path)
        if not time_profile_report["ok"]:
            for time_issue in time_profile_report["issues"]:
                issues.append(
                    _issue(
                        time_issue["code"],
                        f"strict_time:{time_issue['path']}",
                        time_issue["message"],
                    )
                )

    return _bundle_report(
        issues,
        media_profile_ok=media_profile_ok,
        strict_time=strict_time,
        time_profile_report=time_profile_report,
    )


def build_main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build an AEP-Media Bundle v0.1 directory.")
    parser.add_argument("media_statement_json", type=Path)
    parser.add_argument("--out", dest="bundle_dir", required=True, type=Path)
    args = parser.parse_args(argv)

    try:
        build_media_bundle(args.media_statement_json, args.bundle_dir)
    except (MediaBundleError, ValueError, OSError) as exc:
        print(json.dumps({"ok": False, "error": str(exc)}, indent=2, sort_keys=True))
        return 1

    print(f"PASS {BUNDLE_PROFILE} build")
    return 0


def verify_main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Verify an AEP-Media Bundle v0.1 directory.")
    parser.add_argument("bundle_dir", type=Path)
    parser.add_argument("--strict-time", action="store_true")
    args = parser.parse_args(argv)

    report = verify_media_bundle(args.bundle_dir, strict_time=args.strict_time)
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(verify_main())
