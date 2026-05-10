from __future__ import annotations

import csv
import io
import json
import shutil
from collections.abc import Callable, Iterable
from hashlib import sha256
from pathlib import Path
from typing import Any

from agent_evidence.adapters.c2pa_manifest import ingest_c2pa_manifest
from agent_evidence.adapters.ffmpeg_prft import ingest_ffmpeg_prft
from agent_evidence.adapters.linuxptp import ingest_linuxptp_trace
from agent_evidence.media_bundle import build_media_bundle, verify_media_bundle
from agent_evidence.media_time import validate_media_time_profile

ADAPTER_EVALUATION_PROFILE = "aep-media-adapter-evaluation@0.1"
ADAPTER_BACKED_PROFILE = "aep-media-adapter-backed-bundle@0.1"
GENERATED_UTC = "2026-04-26T00:00:00Z"

LINUXPTP_PTP4L = "examples/media/adapters/linuxptp/ptp4l-sample.log"
LINUXPTP_PHC2SYS = "examples/media/adapters/linuxptp/phc2sys-sample.log"
LINUXPTP_EMPTY = "examples/media/adapters/linuxptp/invalid-empty.log"
FFMPEG_PRFT = "examples/media/adapters/ffmpeg/ffprobe-prft-sample.json"
FFMPEG_NO_PRFT = "examples/media/adapters/ffmpeg/ffprobe-no-prft-sample.json"
C2PA_VALID = "examples/media/adapters/c2pa/c2pa-manifest-valid-like.json"
C2PA_INVALID = "examples/media/adapters/c2pa/c2pa-manifest-invalid-signature-like.json"
TIME_VALID = "examples/media/time/minimal-valid-time-aware-media-evidence.json"
TIME_PRIMARY = "examples/media/time/fixtures/demo-media.bin"


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
        return path.name if path.is_absolute() else path.as_posix()


def _sanitize_paths(value: Any, *, repo_root: Path, out_dir: Path) -> Any:
    if isinstance(value, dict):
        return {
            key: _sanitize_paths(item, repo_root=repo_root, out_dir=out_dir)
            for key, item in value.items()
        }
    if isinstance(value, list):
        return [_sanitize_paths(item, repo_root=repo_root, out_dir=out_dir) for item in value]
    if isinstance(value, str):
        for root, label in ((out_dir, "<adapter-evaluation>"), (repo_root, ".")):
            root_text = str(root.resolve())
            if value == root_text:
                return label
            if value.startswith(root_text + "/"):
                suffix = value[len(root_text) + 1 :]
                return f"{label}/{suffix}" if label != "." else suffix
    return value


def _copy_file(source: Path, target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, target)


def _artifact(
    *,
    artifact_id: str,
    role: str,
    path: str,
    full_path: Path,
    mime_type: str,
    time_context_ref: str,
    prft_declared: bool = False,
    timecode_declared: bool = False,
) -> dict[str, Any]:
    return {
        "id": artifact_id,
        "role": role,
        "path": path,
        "sha256": _sha256_file(full_path),
        "mime_type": mime_type,
        "size_bytes": full_path.stat().st_size,
        "time_context_ref": time_context_ref,
        "container": "json" if mime_type == "application/json" else "demo-binary",
        "timing": {
            "prft_declared": prft_declared,
            "timecode_declared": timecode_declared,
        },
    }


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
    text = "".join(
        f"{digest}  {relative_path}\n" for relative_path, digest in sorted(entries.items())
    )
    (bundle_dir / "checksums.txt").write_text(text, encoding="utf-8")


def _normalize_bundle(bundle_dir: Path, repo_root: Path) -> None:
    bundle_path = bundle_dir / "bundle.json"
    bundle = _read_json(bundle_path)
    bundle["created_utc"] = GENERATED_UTC
    for artifact in bundle.get("artifacts", []):
        if not isinstance(artifact, dict):
            continue
        source_path = artifact.get("source_path")
        if isinstance(source_path, str):
            artifact["source_path"] = _repo_relative(Path(source_path), repo_root)
    _write_json(bundle_path, bundle)
    _rewrite_bundle_checksums(bundle_dir)


def _collect_issue_codes(report: dict[str, Any]) -> list[str]:
    codes: list[str] = []

    def add(code: object) -> None:
        if isinstance(code, str) and code not in codes:
            codes.append(code)

    def visit(value: object) -> None:
        if isinstance(value, dict):
            for issue in value.get("issues", []):
                if isinstance(issue, dict):
                    add(issue.get("code"))
            for nested in value.values():
                if isinstance(nested, dict):
                    visit(nested)
        elif isinstance(value, list):
            for item in value:
                visit(item)

    visit(report)
    return codes


def _case_record(
    *,
    case_id: str,
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
    else:
        matched = not observed_ok and (
            not expected_code_set or bool(expected_code_set.intersection(primary_codes))
        )
    return {
        "case_id": case_id,
        "category": "adapter_ingestion",
        "input": input_path,
        "expected": expected,
        "observed_ok": observed_ok,
        "matched_expectation": matched,
        "primary_codes": primary_codes,
        "issue_count": int(report.get("issue_count", len(report.get("issues", [])))),
        "report_path": report_path,
    }


def _write_report(out_dir: Path, rel_path: str, report: dict[str, Any], *, repo_root: Path) -> None:
    sanitized = _sanitize_paths(report, repo_root=repo_root, out_dir=out_dir)
    _write_json(out_dir / rel_path, sanitized)


def _csv_safe(value: object) -> str:
    text = "|".join(value) if isinstance(value, list) else str(value)
    if text.startswith(("=", "+", "-", "@")):
        return "'" + text
    return text


def _write_csv(path: Path, cases: list[dict[str, Any]]) -> None:
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
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=fieldnames)
    writer.writeheader()
    for case in cases:
        writer.writerow({field: _csv_safe(case[field]) for field in fieldnames})
    path.write_text(output.getvalue(), encoding="utf-8")


def _write_matrix_md(path: Path, cases: list[dict[str, Any]]) -> None:
    matched_count = sum(1 for case in cases if case["matched_expectation"])
    lines = [
        "# AEP-Media Adapter Evaluation Matrix v0.1",
        "",
        "This matrix covers fixture-only adapter ingestion for LinuxPTP-style logs, "
        "ffprobe PRFT-style timing metadata, C2PA-like manifests, and one "
        "adapter-backed strict-time bundle. It does not require external tools.",
        "",
        "category | cases | matched | unexpected",
        "--- | ---: | ---: | ---:",
        f"adapter_ingestion | {len(cases)} | {matched_count} | {len(cases) - matched_count}",
        "",
        "case_id | expected | observed | primary codes | matched",
        "--- | --- | --- | --- | ---",
    ]
    for case in cases:
        observed = "pass" if case["observed_ok"] else "fail"
        codes = ", ".join(case["primary_codes"])
        matched = "yes" if case["matched_expectation"] else "no"
        lines.append(f"{case['case_id']} | {case['expected']} | {observed} | {codes} | {matched}")
    lines.extend(
        [
            "",
            "Interpretation: these cases demonstrate adapter ingestion plus local "
            "validation only. They do not claim real external anchoring.",
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def create_adapter_backed_statement(
    out_dir: str | Path,
    repo_root: str | Path | None = None,
) -> dict[str, Any]:
    resolved_repo_root = (
        Path(repo_root).resolve() if repo_root is not None else Path(__file__).resolve().parents[1]
    )
    resolved_out_dir = Path(out_dir).resolve()
    artifacts_dir = resolved_out_dir / "artifacts"
    reports_dir = resolved_out_dir / "adapter-reports"
    artifacts_dir.mkdir(parents=True, exist_ok=True)
    reports_dir.mkdir(parents=True, exist_ok=True)

    linuxptp_trace = artifacts_dir / "clock-trace-from-linuxptp.json"
    ffmpeg_metadata = artifacts_dir / "ffmpeg-prft-metadata.json"
    c2pa_metadata = artifacts_dir / "c2pa-manifest-metadata.json"
    primary_media = artifacts_dir / "demo-media.bin"

    linuxptp_report = ingest_linuxptp_trace(resolved_repo_root / LINUXPTP_PTP4L, linuxptp_trace)
    ffmpeg_report = ingest_ffmpeg_prft(resolved_repo_root / FFMPEG_PRFT, ffmpeg_metadata)
    c2pa_report = ingest_c2pa_manifest(resolved_repo_root / C2PA_VALID, c2pa_metadata)
    _copy_file(resolved_repo_root / TIME_PRIMARY, primary_media)

    _write_json(reports_dir / "linuxptp-report.json", linuxptp_report)
    _write_json(reports_dir / "ffmpeg-prft-report.json", ffmpeg_report)
    _write_json(reports_dir / "c2pa-report.json", c2pa_report)

    statement = _read_json(resolved_repo_root / TIME_VALID)
    time_context_id = statement["time_context"]["id"]
    artifacts = [
        _artifact(
            artifact_id="media:adapter-demo-primary",
            role="primary_media",
            path="artifacts/demo-media.bin",
            full_path=primary_media,
            mime_type="application/octet-stream",
            time_context_ref=time_context_id,
        ),
        _artifact(
            artifact_id="media:adapter-demo-c2pa-metadata",
            role="sidecar_manifest",
            path="artifacts/c2pa-manifest-metadata.json",
            full_path=c2pa_metadata,
            mime_type="application/json",
            time_context_ref=time_context_id,
        ),
        _artifact(
            artifact_id="media:adapter-demo-clock-trace",
            role="clock_trace",
            path="artifacts/clock-trace-from-linuxptp.json",
            full_path=linuxptp_trace,
            mime_type="application/json",
            time_context_ref=time_context_id,
        ),
        _artifact(
            artifact_id="media:adapter-demo-ffmpeg-prft",
            role="other",
            path="artifacts/ffmpeg-prft-metadata.json",
            full_path=ffmpeg_metadata,
            mime_type="application/json",
            time_context_ref=time_context_id,
            prft_declared=True,
            timecode_declared=True,
        ),
    ]
    artifact_ids = [artifact["id"] for artifact in artifacts]
    statement["statement_id"] = "aep-media-adapter:statement:demo-001"
    statement["timestamp"] = "2026-04-26T08:20:05Z"
    statement["media"]["artifacts"] = artifacts
    statement["time_context"]["clock_trace_refs"] = ["media:adapter-demo-clock-trace"]
    statement["operation"]["id"] = "operation:media-adapter-capture-demo-001"
    statement["operation"]["media_refs"] = artifact_ids
    statement["operation"]["evidence_refs"] = ["evidence:media-adapter-capture-demo-001"]
    statement["provenance"]["id"] = "provenance:media-adapter-capture-demo-001"
    statement["provenance"]["operation_ref"] = statement["operation"]["id"]
    statement["provenance"]["media_refs"] = artifact_ids
    statement["provenance"]["c2pa_manifest_ref"] = "media:adapter-demo-c2pa-metadata"
    statement["provenance"]["claim_generator"] = "aep-media-c2pa-manifest-adapter fixture ingestion"
    statement["evidence"]["id"] = "evidence:media-adapter-capture-demo-001"
    statement["evidence"]["artifact_refs"] = artifact_ids
    statement["evidence"]["notes"] = (
        "Adapter-backed declared-demo media evidence object. LinuxPTP, FFmpeg PRFT, "
        "and C2PA-like outputs are fixture-ingested metadata, not external proof."
    )
    statement["validation"]["required_checks"] = [
        *statement["validation"]["required_checks"],
        "adapter_ingestion",
    ]

    statement_path = resolved_out_dir / "adapter-backed-media-evidence.json"
    _write_json(statement_path, statement)
    time_report = validate_media_time_profile(statement_path)
    _write_json(resolved_out_dir / "adapter-time-validation-report.json", time_report)

    bundle_dir = resolved_out_dir / "adapter-backed-bundle"
    build_media_bundle(statement_path, bundle_dir)
    _normalize_bundle(bundle_dir, resolved_repo_root)
    bundle_report = verify_media_bundle(bundle_dir, strict_time=True)
    _write_json(resolved_out_dir / "adapter-bundle-validation-report.json", bundle_report)

    issues: list[dict[str, str]] = []
    for name, report in (
        ("linuxptp", linuxptp_report),
        ("ffmpeg_prft", ffmpeg_report),
        ("c2pa_manifest", c2pa_report),
    ):
        if not report["ok"]:
            issues.append(
                {
                    "code": f"{name}_adapter_failed",
                    "message": f"{name} adapter report was not ok.",
                    "path": f"adapter-reports/{name}",
                }
            )
    if not time_report["ok"]:
        issues.append(
            {
                "code": "adapter_backed_time_validation_failed",
                "message": "adapter-backed statement failed strict time validation.",
                "path": "adapter-time-validation-report.json",
            }
        )
    if not bundle_report["ok"]:
        issues.append(
            {
                "code": "adapter_backed_bundle_validation_failed",
                "message": "adapter-backed bundle failed strict-time verification.",
                "path": "adapter-bundle-validation-report.json",
            }
        )

    report = {
        "ok": not issues,
        "profile": ADAPTER_BACKED_PROFILE,
        "issue_count": len(issues),
        "issues": issues,
        "adapter_reports": {
            "linuxptp": linuxptp_report,
            "ffmpeg_prft": ffmpeg_report,
            "c2pa_manifest": c2pa_report,
        },
        "time_profile_ok": time_report["ok"],
        "bundle_strict_time_ok": bundle_report["ok"],
        "statement_path": "adapter-backed-media-evidence.json",
        "bundle_path": "adapter-backed-bundle",
        "claim_boundary": {
            "adapter_ingestion": True,
            "external_verification": False,
            "local_validation_only": True,
        },
        "summary": f"{'PASS' if not issues else 'FAIL'} {ADAPTER_BACKED_PROFILE}",
    }
    _write_json(resolved_out_dir / "adapter-demo-summary.json", report)
    return report


def _run_adapter_case(
    *,
    input_path: Path,
    out_path: Path,
    ingest_func: Callable[[Path, Path], dict[str, Any]],
) -> dict[str, Any]:
    return ingest_func(input_path, out_path)


def run_media_adapter_evaluation(
    out_dir: str | Path,
    repo_root: str | Path | None = None,
) -> dict[str, Any]:
    resolved_repo_root = (
        Path(repo_root).resolve() if repo_root is not None else Path(__file__).resolve().parents[1]
    )
    resolved_out_dir = Path(out_dir).resolve()
    if resolved_out_dir.exists():
        shutil.rmtree(resolved_out_dir)
    (resolved_out_dir / "reports").mkdir(parents=True, exist_ok=True)
    (resolved_out_dir / "outputs").mkdir(parents=True, exist_ok=True)

    cases: list[dict[str, Any]] = []

    def store_case(
        *,
        case_id: str,
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
                input_path=input_path,
                expected=expected,
                report=report,
                report_path=report_path,
                expected_codes=expected_codes,
            )
        )

    adapter_cases = [
        (
            "adapter_linuxptp_ptp4l_valid",
            LINUXPTP_PTP4L,
            "outputs/clock-trace-ptp4l.json",
            ingest_linuxptp_trace,
            "pass",
            "reports/adapter-linuxptp-ptp4l-valid.json",
            [],
        ),
        (
            "adapter_linuxptp_phc2sys_valid",
            LINUXPTP_PHC2SYS,
            "outputs/clock-trace-phc2sys.json",
            ingest_linuxptp_trace,
            "pass",
            "reports/adapter-linuxptp-phc2sys-valid.json",
            [],
        ),
        (
            "adapter_linuxptp_empty_invalid",
            LINUXPTP_EMPTY,
            "outputs/clock-trace-empty.json",
            ingest_linuxptp_trace,
            "fail",
            "reports/adapter-linuxptp-empty-invalid.json",
            ["linuxptp_no_samples"],
        ),
        (
            "adapter_ffmpeg_prft_valid",
            FFMPEG_PRFT,
            "outputs/ffmpeg-prft-metadata.json",
            ingest_ffmpeg_prft,
            "pass",
            "reports/adapter-ffmpeg-prft-valid.json",
            [],
        ),
        (
            "adapter_ffmpeg_prft_missing_invalid",
            FFMPEG_NO_PRFT,
            "outputs/ffmpeg-no-prft-metadata.json",
            ingest_ffmpeg_prft,
            "fail",
            "reports/adapter-ffmpeg-prft-missing-invalid.json",
            ["ffmpeg_prft_not_found"],
        ),
        (
            "adapter_c2pa_manifest_valid_like",
            C2PA_VALID,
            "outputs/c2pa-valid-metadata.json",
            ingest_c2pa_manifest,
            "pass",
            "reports/adapter-c2pa-valid-like.json",
            [],
        ),
        (
            "adapter_c2pa_manifest_invalid_signature_like",
            C2PA_INVALID,
            "outputs/c2pa-invalid-metadata.json",
            ingest_c2pa_manifest,
            "fail",
            "reports/adapter-c2pa-invalid-signature-like.json",
            ["c2pa_signature_invalid_declared"],
        ),
    ]
    for (
        case_id,
        input_path,
        output_path,
        ingest_func,
        expected,
        report_path,
        expected_codes,
    ) in adapter_cases:
        report = _run_adapter_case(
            input_path=resolved_repo_root / input_path,
            out_path=resolved_out_dir / output_path,
            ingest_func=ingest_func,
        )
        store_case(
            case_id=case_id,
            input_path=input_path,
            expected=expected,
            report=report,
            report_path=report_path,
            expected_codes=expected_codes,
        )

    adapter_backed_report = create_adapter_backed_statement(
        resolved_out_dir / "adapter-backed",
        repo_root=resolved_repo_root,
    )
    store_case(
        case_id="adapter_backed_strict_time_bundle_valid",
        input_path="adapter-backed/adapter-backed-media-evidence.json",
        expected="pass",
        report=adapter_backed_report,
        report_path="reports/adapter-backed-strict-time-bundle-valid.json",
    )

    matched_count = sum(1 for case in cases if case["matched_expectation"])
    unexpected_count = len(cases) - matched_count
    summary = {
        "profile": ADAPTER_EVALUATION_PROFILE,
        "ok": unexpected_count == 0,
        "case_count": len(cases),
        "matched_count": matched_count,
        "unexpected_count": unexpected_count,
        "categories": {
            "adapter_ingestion": {
                "cases": len(cases),
                "expected_pass": sum(1 for case in cases if case["expected"] == "pass"),
                "expected_fail": sum(1 for case in cases if case["expected"] == "fail"),
                "matched": matched_count,
                "unexpected": unexpected_count,
            }
        },
        "summary": (
            f"{'PASS' if unexpected_count == 0 else 'FAIL'} {ADAPTER_EVALUATION_PROFILE} "
            f"cases={len(cases)} unexpected={unexpected_count}"
        ),
    }
    matrix = {
        "profile": ADAPTER_EVALUATION_PROFILE,
        "generated_utc": GENERATED_UTC,
        "case_count": len(cases),
        "unexpected_count": unexpected_count,
        "cases": cases,
    }

    _write_json(resolved_out_dir / "adapter-evaluation-summary.json", summary)
    _write_json(resolved_out_dir / "adapter-evaluation-matrix.json", matrix)
    _write_matrix_md(resolved_out_dir / "adapter-evaluation-matrix.md", cases)
    _write_csv(resolved_out_dir / "adapter-evaluation-matrix.csv", cases)
    return summary
