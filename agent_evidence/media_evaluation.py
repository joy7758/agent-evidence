from __future__ import annotations

import argparse
import csv
import io
import json
import platform
import shutil
import subprocess
import sys
from collections.abc import Iterable
from hashlib import sha256
from pathlib import Path
from typing import Any

from agent_evidence.media_bundle import build_media_bundle, verify_media_bundle
from agent_evidence.media_profile import validate_media_profile_file
from agent_evidence.media_time import validate_media_time_profile

EVALUATION_PROFILE = "aep-media-evaluation@0.1"
GENERATED_UTC = "2026-04-26T00:00:00Z"

PROFILE_VALID = "examples/media/minimal-valid-media-evidence.json"
PROFILE_MISSING_TIME = "examples/media/invalid-missing-time-context.json"
PROFILE_BROKEN_HASH = "examples/media/invalid-broken-media-hash.json"
PROFILE_POLICY_REF = "examples/media/invalid-unresolved-policy-ref.json"

TIME_VALID = "examples/media/time/minimal-valid-time-aware-media-evidence.json"
TIME_MISSING_CLOCK_REF = "examples/media/time/invalid-missing-clock-trace-ref.json"
TIME_OFFSET_THRESHOLD = "examples/media/time/invalid-clock-offset-threshold.json"
TIME_WINDOW_MISMATCH = "examples/media/time/invalid-clock-window-mismatch.json"


def _write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _read_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"expected JSON object: {path}")
    return payload


def _sha256_file(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def _repo_relative(path: Path, repo_root: Path) -> str:
    try:
        return path.resolve().relative_to(repo_root.resolve()).as_posix()
    except ValueError:
        return path.name


def _sanitize_paths(value: Any, *, repo_root: Path, out_dir: Path) -> Any:
    if isinstance(value, dict):
        return {
            key: _sanitize_paths(item, repo_root=repo_root, out_dir=out_dir)
            for key, item in value.items()
        }
    if isinstance(value, list):
        return [_sanitize_paths(item, repo_root=repo_root, out_dir=out_dir) for item in value]
    if isinstance(value, str):
        for root, label in ((out_dir, "<evaluation>"), (repo_root, ".")):
            root_text = str(root.resolve())
            if value == root_text:
                return label
            if value.startswith(root_text + "/"):
                suffix = value[len(root_text) + 1 :]
                return f"{label}/{suffix}" if label != "." else suffix
    return value


def _copy_bundle_tree(source: Path, target: Path) -> None:
    if target.exists():
        shutil.rmtree(target)
    shutil.copytree(source, target)


def _rewrite_bundle_checksums(bundle_dir: Path) -> None:
    bundle = _read_json(bundle_dir / "bundle.json")
    entries = {
        "bundle.json": _sha256_file(bundle_dir / "bundle.json"),
        "statement.json": _sha256_file(bundle_dir / "statement.json"),
    }
    for artifact in bundle.get("artifacts", []):
        if isinstance(artifact, dict) and isinstance(artifact.get("path"), str):
            artifact_path = bundle_dir / artifact["path"]
            if artifact_path.exists() and artifact_path.is_file():
                entries[artifact["path"]] = _sha256_file(artifact_path)

    checksum_text = "".join(
        f"{digest}  {relative_path}\n" for relative_path, digest in sorted(entries.items())
    )
    (bundle_dir / "checksums.txt").write_text(checksum_text, encoding="utf-8")


def _normalize_evaluation_bundle(bundle_dir: Path, repo_root: Path) -> None:
    bundle_path = bundle_dir / "bundle.json"
    bundle = _read_json(bundle_path)
    bundle["created_utc"] = GENERATED_UTC
    for artifact in bundle.get("artifacts", []):
        if not isinstance(artifact, dict):
            continue
        source_path = artifact.get("source_path")
        if isinstance(source_path, str) and Path(source_path).is_absolute():
            artifact["source_path"] = _repo_relative(Path(source_path), repo_root)
    _write_json(bundle_path, bundle)
    _rewrite_bundle_checksums(bundle_dir)


def _load_statement(bundle_dir: Path) -> dict[str, Any]:
    return _read_json(bundle_dir / "statement.json")


def _write_statement(bundle_dir: Path, statement: dict[str, Any]) -> None:
    _write_json(bundle_dir / "statement.json", statement)


def _primary_artifact_path(bundle_dir: Path) -> Path:
    statement = _load_statement(bundle_dir)
    artifacts = statement["media"]["artifacts"]
    primary = next(artifact for artifact in artifacts if artifact["role"] == "primary_media")
    return bundle_dir / primary["path"]


def _clock_trace_path(bundle_dir: Path) -> Path:
    statement = _load_statement(bundle_dir)
    artifacts = statement["media"]["artifacts"]
    clock_trace = next(artifact for artifact in artifacts if artifact["role"] == "clock_trace")
    return bundle_dir / clock_trace["path"]


def _tamper_artifact(bundle_dir: Path) -> None:
    with _primary_artifact_path(bundle_dir).open("ab") as artifact_file:
        artifact_file.write(b"\nevaluation tamper: primary media\n")


def _tamper_missing_time_context(bundle_dir: Path) -> None:
    statement = _load_statement(bundle_dir)
    statement.pop("time_context", None)
    _write_statement(bundle_dir, statement)


def _tamper_policy_ref(bundle_dir: Path) -> None:
    statement = _load_statement(bundle_dir)
    statement["operation"]["policy_ref"] = "policy:evaluation-missing-policy"
    _write_statement(bundle_dir, statement)


def _tamper_path_escape(bundle_dir: Path) -> None:
    bundle_path = bundle_dir / "bundle.json"
    bundle = _read_json(bundle_path)
    bundle["artifacts"][0]["path"] = "../evil"
    _write_json(bundle_path, bundle)


def _tamper_clock_offset(bundle_dir: Path) -> None:
    trace_path = _clock_trace_path(bundle_dir)
    trace = _read_json(trace_path)
    offsets = [2000000, 2100000, 1900000]
    for sample, offset in zip(trace["samples"], offsets, strict=True):
        sample["offset_ns"] = offset
    trace["summary"] = {
        "sample_count": 3,
        "max_abs_offset_ns": 2100000,
        "max_jitter_ns": 200000,
        "within_threshold": False,
    }
    _write_json(trace_path, trace)


def _tamper_clock_window(bundle_dir: Path) -> None:
    trace_path = _clock_trace_path(bundle_dir)
    trace = _read_json(trace_path)
    trace["collection"]["start_utc"] = "2026-04-26T08:20:01Z"
    trace["collection"]["end_utc"] = "2026-04-26T08:20:02Z"
    _write_json(trace_path, trace)


def _tamper_missing_clock_ref(bundle_dir: Path) -> None:
    statement = _load_statement(bundle_dir)
    statement["time_context"].pop("clock_trace_refs", None)
    _write_statement(bundle_dir, statement)


def _collect_issue_codes(report: dict[str, Any]) -> list[str]:
    codes: list[str] = []

    def add(code: object) -> None:
        if isinstance(code, str) and code not in codes:
            codes.append(code)

    for issue in report.get("issues", []):
        if isinstance(issue, dict):
            add(issue.get("code"))
    time_report = report.get("time_profile_report")
    if isinstance(time_report, dict):
        for issue in time_report.get("issues", []):
            if isinstance(issue, dict):
                add(issue.get("code"))
    return codes


def _case_record(
    *,
    case_id: str,
    category: str,
    input_path: str,
    expected: str,
    report: dict[str, Any],
    report_path: str,
    expected_codes: Iterable[str] = (),
) -> dict[str, Any]:
    observed_ok = bool(report.get("ok"))
    primary_codes = _collect_issue_codes(report)
    expected_code_set = set(expected_codes)
    if expected == "pass":
        matched = observed_ok
    elif expected == "fail":
        matched = not observed_ok and (
            not expected_code_set or bool(expected_code_set.intersection(primary_codes))
        )
    else:
        matched = bool(report.get("matched_expectation", observed_ok))
    return {
        "case_id": case_id,
        "category": category,
        "input": input_path,
        "expected": expected,
        "observed_ok": observed_ok,
        "matched_expectation": matched,
        "primary_codes": primary_codes,
        "issue_count": int(report.get("issue_count", len(report.get("issues", [])))),
        "report_path": report_path,
    }


def _write_report(
    out_dir: Path,
    rel_path: str,
    report: dict[str, Any],
    *,
    repo_root: Path,
) -> None:
    sanitized = _sanitize_paths(report, repo_root=repo_root, out_dir=out_dir)
    _write_json(out_dir / rel_path, sanitized)


def _category_summary(cases: list[dict[str, Any]]) -> dict[str, dict[str, int]]:
    categories: dict[str, dict[str, int]] = {}
    for case in cases:
        category = case["category"]
        bucket = categories.setdefault(
            category,
            {
                "cases": 0,
                "expected_pass": 0,
                "expected_fail": 0,
                "expected_optional": 0,
                "matched": 0,
                "unexpected": 0,
            },
        )
        bucket["cases"] += 1
        if case["expected"] == "pass":
            bucket["expected_pass"] += 1
        elif case["expected"] == "fail":
            bucket["expected_fail"] += 1
        else:
            bucket["expected_optional"] += 1
        if case["matched_expectation"]:
            bucket["matched"] += 1
        else:
            bucket["unexpected"] += 1
    return categories


def _csv_safe(value: object) -> str:
    text = "|".join(value) if isinstance(value, list) else str(value)
    if text.startswith(("=", "+", "-", "@")):
        return "'" + text
    return text


def _write_csv(path: Path, cases: list[dict[str, Any]]) -> None:
    output = io.StringIO()
    fieldnames = [
        "case_id",
        "category",
        "input",
        "expected",
        "observed_ok",
        "matched_expectation",
        "primary_codes",
        "issue_count",
        "report_path",
    ]
    writer = csv.DictWriter(output, fieldnames=fieldnames)
    writer.writeheader()
    for case in cases:
        writer.writerow({field: _csv_safe(case[field]) for field in fieldnames})
    path.write_text(output.getvalue(), encoding="utf-8")


def _write_matrix_md(
    path: Path,
    cases: list[dict[str, Any]],
    categories: dict[str, dict[str, int]],
) -> None:
    lines = [
        "# AEP-Media Evaluation Matrix v0.1",
        "",
        (
            "This evaluation covers declared-demo media evidence validation, offline bundle "
            "verification, strict declared time-trace validation, and controlled tamper cases. "
            "It does not test real PTP, FFmpeg PRFT extraction, or C2PA signature verification."
        ),
        "",
        "## Summary",
        "",
        (
            "category | cases | expected pass | expected fail | expected optional | "
            "matched | unexpected"
        ),
        "--- | ---: | ---: | ---: | ---: | ---: | ---:",
    ]
    for category, values in sorted(categories.items()):
        lines.append(
            f"{category} | {values['cases']} | {values['expected_pass']} | "
            f"{values['expected_fail']} | {values.get('expected_optional', 0)} | "
            f"{values['matched']} | {values['unexpected']}"
        )
    lines.extend(
        [
            "",
            "## Cases",
            "",
            "case_id | category | expected | observed | primary codes | matched",
            "--- | --- | --- | --- | --- | ---",
        ]
    )
    for case in cases:
        observed = (
            str(case.get("status"))
            if case.get("status")
            else ("pass" if case["observed_ok"] else "fail")
        )
        codes = ", ".join(case["primary_codes"])
        matched = "yes" if case["matched_expectation"] else "no"
        lines.append(
            f"{case['case_id']} | {case['category']} | {case['expected']} | "
            f"{observed} | {codes} | {matched}"
        )
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- Valid profile passes.",
            "- Controlled invalid profiles fail with expected codes.",
            "- Valid bundle verifies offline.",
            "- Tampered bundle fails.",
            "- Valid strict-time evidence passes.",
            "- Time-trace tampering fails with time-specific codes.",
            "",
            "## Non-claims",
            "",
            "See `non-claims-matrix.md`.",
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _inventory_item(path: str, repo_root: Path) -> dict[str, Any]:
    full_path = repo_root / path
    exists = full_path.exists()
    return {
        "path": path,
        "exists": exists,
        "sha256": _sha256_file(full_path) if exists and full_path.is_file() else None,
        "size_bytes": full_path.stat().st_size if exists and full_path.is_file() else None,
    }


def _artifact_inventory(repo_root: Path) -> dict[str, list[dict[str, Any]]]:
    examples = sorted(
        path.relative_to(repo_root).as_posix()
        for path in (repo_root / "examples" / "media").glob("**/*.json")
    )
    inventory = {
        "specs": [
            "spec/aep-media-profile-v0.1.md",
            "spec/aep-media-bundle-v0.1.md",
            "spec/aep-media-time-trace-v0.1.md",
            "spec/aep-media-adapters-v0.1.md",
        ],
        "schemas": [
            "schema/aep_media_profile_v0_1.schema.json",
            "schema/aep_media_bundle_v0_1.schema.json",
            "schema/aep_media_time_trace_v0_1.schema.json",
            "schema/aep_media_adapter_report_v0_1.schema.json",
        ],
        "examples": examples,
        "demos": [
            "demo/run_media_evidence_demo.py",
            "demo/run_media_bundle_demo.py",
            "demo/run_media_time_demo.py",
            "demo/run_media_evaluation_demo.py",
            "demo/run_media_adapter_demo.py",
        ],
        "tests": [
            "tests/test_media_profile.py",
            "tests/test_media_bundle.py",
            "tests/test_media_time.py",
            "tests/test_media_evaluation.py",
            "tests/test_media_adapters.py",
        ],
    }
    return {
        category: [_inventory_item(path, repo_root) for path in paths]
        for category, paths in inventory.items()
    }


def _write_reproducibility_commands(path: Path) -> None:
    lines = [
        "# AEP-Media Reproducibility Commands",
        "",
        "```bash",
        (
            "./.venv/bin/python -m pytest tests/test_media_profile.py "
            "tests/test_media_bundle.py tests/test_media_time.py "
            "tests/test_media_evaluation.py -q"
        ),
        "",
        (
            "./.venv/bin/agent-evidence validate-media-profile "
            "examples/media/minimal-valid-media-evidence.json"
        ),
        (
            "./.venv/bin/agent-evidence build-media-bundle "
            "examples/media/minimal-valid-media-evidence.json "
            "--out /tmp/aep-media-bundle-check"
        ),
        "./.venv/bin/agent-evidence verify-media-bundle /tmp/aep-media-bundle-check",
        "",
        (
            "./.venv/bin/agent-evidence validate-media-time-profile "
            "examples/media/time/minimal-valid-time-aware-media-evidence.json"
        ),
        (
            "./.venv/bin/agent-evidence build-media-bundle "
            "examples/media/time/minimal-valid-time-aware-media-evidence.json "
            "--out /tmp/aep-media-time-bundle-check"
        ),
        (
            "./.venv/bin/agent-evidence verify-media-bundle "
            "/tmp/aep-media-time-bundle-check --strict-time"
        ),
        "",
        "./.venv/bin/agent-evidence run-media-evaluation --out demo/output/media_evaluation_demo",
        (
            "./.venv/bin/agent-evidence run-media-evaluation "
            "--out demo/output/media_evaluation_with_adapters --include-adapters"
        ),
        (
            "./.venv/bin/agent-evidence run-media-evaluation "
            "--out demo/output/media_evaluation_with_tools --include-optional-tools"
        ),
        "",
        "./.venv/bin/python demo/run_media_evaluation_demo.py",
        "./.venv/bin/python demo/run_media_adapter_demo.py",
        "```",
    ]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _write_non_claims(path: Path) -> None:
    rows = [
        (
            "legal admissibility",
            "local declared-demo validation cannot establish legal admissibility",
            "legal process, chain of custody, jurisdiction-specific review",
        ),
        (
            "non-repudiation",
            "no external signing or identity trust fabric in v0.1",
            "signing, certificate chain, external anchoring",
        ),
        (
            "trusted timestamping",
            "current time trace is declared or synthetic",
            "trusted timestamp authority, transparency log, external time anchor",
        ),
        (
            "real PTP synchronization",
            "v0.1 does not run ptp4l/phc2sys or inspect hardware clock discipline",
            "linuxptp trace ingestion",
        ),
        (
            "real MP4 PRFT extraction",
            "v0.1 does not parse MP4 boxes or call FFmpeg",
            "FFmpeg PRFT extraction adapter",
        ),
        (
            "real C2PA signature verification",
            "v0.1 uses placeholder manifest references only",
            "c2pa manifest signing and verification adapter",
        ),
        (
            "production deployment",
            "examples and demos are local declared-demo fixtures",
            "field pilot and deployment evidence",
        ),
        (
            "complete regulatory compliance",
            "profile validates evidence structure, not legal sufficiency",
            "domain-specific compliance mapping and external review",
        ),
    ]
    lines = [
        "# AEP-Media Non-claims Matrix",
        "",
        "claim_not_made | reason | future integration",
        "--- | --- | ---",
    ]
    lines.extend(f"{claim} | {reason} | {future}" for claim, reason, future in rows)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _environment(repo_root: Path) -> dict[str, Any]:
    def run_git(args: list[str]) -> str:
        try:
            result = subprocess.run(
                ["git", *args],
                cwd=repo_root,
                check=False,
                capture_output=True,
                text=True,
            )
        except OSError:
            return "unavailable"
        return result.stdout.strip() if result.returncode == 0 else "unavailable"

    status_lines = run_git(["status", "--short"]).splitlines()
    return {
        "python_version": sys.version.split()[0],
        "platform": platform.platform(),
        "git_commit": run_git(["rev-parse", "HEAD"]),
        "git_dirty": bool(status_lines),
        "git_status_entry_count": len(status_lines),
    }


def _make_build_report(summary: dict[str, Any]) -> dict[str, Any]:
    return {
        "ok": bool(summary.get("ok")),
        "profile": summary.get("profile", "aep-media-bundle@0.1"),
        "issue_count": 0 if summary.get("ok") else 1,
        "issues": [] if summary.get("ok") else [{"code": "bundle_build_failed"}],
        "summary": summary.get("summary"),
    }


def run_media_evaluation(
    out_dir: str | Path,
    repo_root: str | Path | None = None,
    include_adapters: bool = False,
    include_optional_tools: bool = False,
) -> dict[str, Any]:
    if repo_root is not None:
        resolved_repo_root = Path(repo_root).resolve()
    else:
        resolved_repo_root = Path(__file__).resolve().parents[1]
    resolved_out_dir = Path(out_dir).resolve()
    if resolved_out_dir.exists():
        shutil.rmtree(resolved_out_dir)
    (resolved_out_dir / "reports").mkdir(parents=True, exist_ok=True)
    (resolved_out_dir / "bundles").mkdir(parents=True, exist_ok=True)

    cases: list[dict[str, Any]] = []

    def store_case(
        *,
        case_id: str,
        category: str,
        input_path: str,
        expected: str,
        report: dict[str, Any],
        report_path: str,
        expected_codes: Iterable[str] = (),
    ) -> None:
        _write_report(resolved_out_dir, report_path, report, repo_root=resolved_repo_root)
        cases.append(
            _case_record(
                case_id=case_id,
                category=category,
                input_path=input_path,
                expected=expected,
                report=report,
                report_path=report_path,
                expected_codes=expected_codes,
            )
        )

    profile_cases = [
        ("profile_valid", PROFILE_VALID, "pass", "reports/profile-valid.json", []),
        (
            "profile_missing_time_context",
            PROFILE_MISSING_TIME,
            "fail",
            "reports/profile-invalid-missing-time-context.json",
            ["missing_time_context"],
        ),
        (
            "profile_broken_media_hash",
            PROFILE_BROKEN_HASH,
            "fail",
            "reports/profile-invalid-broken-media-hash.json",
            ["media_hash_mismatch"],
        ),
        (
            "profile_unresolved_policy_ref",
            PROFILE_POLICY_REF,
            "fail",
            "reports/profile-invalid-unresolved-policy-ref.json",
            ["unresolved_policy_ref"],
        ),
    ]
    for case_id, input_path, expected, report_path, expected_codes in profile_cases:
        report = validate_media_profile_file(resolved_repo_root / input_path)
        store_case(
            case_id=case_id,
            category="media_profile",
            input_path=input_path,
            expected=expected,
            report=report,
            report_path=report_path,
            expected_codes=expected_codes,
        )

    valid_bundle = resolved_out_dir / "bundles" / "valid-media-bundle"
    build_summary = build_media_bundle(resolved_repo_root / PROFILE_VALID, valid_bundle)
    _normalize_evaluation_bundle(valid_bundle, resolved_repo_root)
    build_report = _make_build_report(build_summary)
    store_case(
        case_id="bundle_valid_build",
        category="media_bundle",
        input_path=PROFILE_VALID,
        expected="pass",
        report=build_report,
        report_path="reports/bundle-valid-build.json",
    )

    store_case(
        case_id="bundle_valid_verify",
        category="media_bundle",
        input_path="bundles/valid-media-bundle",
        expected="pass",
        report=verify_media_bundle(valid_bundle),
        report_path="reports/bundle-valid-verify.json",
    )

    bundle_tampers = [
        (
            "bundle_tampered_artifact",
            "tampered-bundle-artifact",
            _tamper_artifact,
            "reports/bundle-tampered-artifact.json",
            ["bundle_checksum_mismatch", "media_hash_mismatch"],
        ),
        (
            "bundle_tampered_missing_time_context",
            "tampered-bundle-missing-time-context",
            _tamper_missing_time_context,
            "reports/bundle-tampered-missing-time-context.json",
            ["missing_time_context", "media_profile_validation_failed"],
        ),
        (
            "bundle_tampered_policy_ref",
            "tampered-bundle-policy-ref",
            _tamper_policy_ref,
            "reports/bundle-tampered-policy-ref.json",
            ["unresolved_policy_ref", "media_profile_validation_failed"],
        ),
        (
            "bundle_path_escape",
            "tampered-bundle-path-escape",
            _tamper_path_escape,
            "reports/bundle-path-escape.json",
            ["bundle_path_escape"],
        ),
    ]
    for case_id, bundle_name, tamper_func, report_path, expected_codes in bundle_tampers:
        tampered_dir = resolved_out_dir / "bundles" / bundle_name
        _copy_bundle_tree(valid_bundle, tampered_dir)
        tamper_func(tampered_dir)
        store_case(
            case_id=case_id,
            category="media_bundle",
            input_path=f"bundles/{bundle_name}",
            expected="fail",
            report=verify_media_bundle(tampered_dir),
            report_path=report_path,
            expected_codes=expected_codes,
        )

    time_cases = [
        ("time_valid", TIME_VALID, "pass", "reports/time-valid.json", []),
        (
            "time_missing_clock_trace_ref",
            TIME_MISSING_CLOCK_REF,
            "fail",
            "reports/time-invalid-missing-clock-trace-ref.json",
            ["missing_clock_trace_ref"],
        ),
        (
            "time_offset_threshold",
            TIME_OFFSET_THRESHOLD,
            "fail",
            "reports/time-invalid-offset-threshold.json",
            ["clock_offset_threshold_exceeded"],
        ),
        (
            "time_window_mismatch",
            TIME_WINDOW_MISMATCH,
            "fail",
            "reports/time-invalid-window-mismatch.json",
            ["clock_trace_window_mismatch"],
        ),
    ]
    for case_id, input_path, expected, report_path, expected_codes in time_cases:
        report = validate_media_time_profile(resolved_repo_root / input_path)
        store_case(
            case_id=case_id,
            category="media_time",
            input_path=input_path,
            expected=expected,
            report=report,
            report_path=report_path,
            expected_codes=expected_codes,
        )

    valid_time_bundle = resolved_out_dir / "bundles" / "valid-time-aware-bundle"
    build_media_bundle(resolved_repo_root / TIME_VALID, valid_time_bundle)
    _normalize_evaluation_bundle(valid_time_bundle, resolved_repo_root)
    store_case(
        case_id="time_bundle_strict_valid",
        category="media_time",
        input_path=TIME_VALID,
        expected="pass",
        report=verify_media_bundle(valid_time_bundle, strict_time=True),
        report_path="reports/time-bundle-strict-valid.json",
    )

    time_tampers = [
        (
            "time_tampered_clock_offset",
            "tampered-time-clock-offset",
            _tamper_clock_offset,
            "reports/time-tampered-clock-offset.json",
            ["clock_offset_threshold_exceeded"],
        ),
        (
            "time_tampered_clock_window",
            "tampered-time-clock-window",
            _tamper_clock_window,
            "reports/time-tampered-clock-window.json",
            ["clock_trace_window_mismatch"],
        ),
        (
            "time_tampered_missing_clock_ref",
            "tampered-time-missing-clock-ref",
            _tamper_missing_clock_ref,
            "reports/time-tampered-missing-clock-ref.json",
            ["missing_clock_trace_ref"],
        ),
    ]
    for case_id, bundle_name, tamper_func, report_path, expected_codes in time_tampers:
        tampered_dir = resolved_out_dir / "bundles" / bundle_name
        _copy_bundle_tree(valid_time_bundle, tampered_dir)
        tamper_func(tampered_dir)
        store_case(
            case_id=case_id,
            category="media_time",
            input_path=f"bundles/{bundle_name}",
            expected="fail",
            report=verify_media_bundle(tampered_dir, strict_time=True),
            report_path=report_path,
            expected_codes=expected_codes,
        )

    if include_adapters:
        from agent_evidence.media_adapter_evaluation import run_media_adapter_evaluation

        adapter_dir = resolved_out_dir / "adapter-evaluation"
        adapter_summary = run_media_adapter_evaluation(
            adapter_dir,
            repo_root=resolved_repo_root,
        )
        adapter_matrix = _read_json(adapter_dir / "adapter-evaluation-matrix.json")
        for adapter_case in adapter_matrix.get("cases", []):
            if not isinstance(adapter_case, dict):
                continue
            merged_case = dict(adapter_case)
            merged_case["report_path"] = f"adapter-evaluation/{merged_case.get('report_path', '')}"
            cases.append(merged_case)
        _write_json(
            resolved_out_dir / "reports" / "adapter-evaluation-summary.json",
            _sanitize_paths(
                adapter_summary, repo_root=resolved_repo_root, out_dir=resolved_out_dir
            ),
        )

    if include_optional_tools:
        from agent_evidence.media_optional_tools import run_optional_tool_evaluation

        optional_tools_dir = resolved_out_dir / "optional-tool-evaluation"
        optional_summary = run_optional_tool_evaluation(optional_tools_dir)
        optional_matrix = _read_json(optional_tools_dir / "optional-tool-matrix.json")
        for optional_case in optional_matrix.get("cases", []):
            if not isinstance(optional_case, dict):
                continue
            merged_case = dict(optional_case)
            merged_case["report_path"] = (
                f"optional-tool-evaluation/{merged_case.get('report_path', '')}"
            )
            cases.append(merged_case)
        _write_json(
            resolved_out_dir / "reports" / "optional-tool-summary.json",
            _sanitize_paths(
                optional_summary,
                repo_root=resolved_repo_root,
                out_dir=resolved_out_dir,
            ),
        )

    categories = _category_summary(cases)
    expected_pass_count = sum(1 for case in cases if case["expected"] == "pass")
    expected_fail_count = sum(1 for case in cases if case["expected"] == "fail")
    expected_optional_count = sum(1 for case in cases if case["expected"] == "optional")
    matched_count = sum(1 for case in cases if case["matched_expectation"])
    unexpected_count = len(cases) - matched_count
    summary = {
        "profile": EVALUATION_PROFILE,
        "ok": unexpected_count == 0,
        "case_count": len(cases),
        "matched_count": matched_count,
        "unexpected_count": unexpected_count,
        "categories": categories,
        "summary": (
            f"{'PASS' if unexpected_count == 0 else 'FAIL'} {EVALUATION_PROFILE} "
            f"cases={len(cases)} unexpected={unexpected_count}"
            f"{' adapters=included' if include_adapters else ''}"
            f"{' optional_tools=included' if include_optional_tools else ''}"
        ),
    }
    matrix = {
        "profile": EVALUATION_PROFILE,
        "generated_utc": GENERATED_UTC,
        "case_count": len(cases),
        "pass_count": expected_pass_count,
        "expected_fail_count": expected_fail_count,
        "expected_optional_count": expected_optional_count,
        "unexpected_count": unexpected_count,
        "cases": cases,
    }

    write_media_evaluation_pack(
        {
            "summary": summary,
            "matrix": matrix,
            "categories": categories,
            "cases": cases,
            "artifact_inventory": _artifact_inventory(resolved_repo_root),
            "environment": _environment(resolved_repo_root),
        },
        resolved_out_dir,
    )
    return summary


def write_media_evaluation_pack(report: dict[str, Any], out_dir: Path) -> None:
    summary = report["summary"]
    matrix = report["matrix"]
    cases = report["cases"]
    categories = report["categories"]

    _write_json(out_dir / "evaluation-summary.json", summary)
    _write_json(out_dir / "evaluation-matrix.json", matrix)
    _write_matrix_md(out_dir / "evaluation-matrix.md", cases, categories)
    _write_csv(out_dir / "evaluation-matrix.csv", cases)
    _write_json(out_dir / "artifact-inventory.json", report["artifact_inventory"])
    _write_reproducibility_commands(out_dir / "reproducibility-commands.md")
    _write_non_claims(out_dir / "non-claims-matrix.md")
    _write_json(out_dir / "environment.json", report["environment"])


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run the AEP-Media evaluation evidence pack.")
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--include-adapters", action="store_true")
    parser.add_argument("--include-optional-tools", action="store_true")
    args = parser.parse_args(argv)

    summary = run_media_evaluation(
        args.out,
        include_adapters=args.include_adapters,
        include_optional_tools=args.include_optional_tools,
    )
    print(summary["summary"])
    return 0 if summary["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
