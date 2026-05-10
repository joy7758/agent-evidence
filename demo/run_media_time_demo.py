#!/usr/bin/env python3
from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

DEMO_ROOT = Path(__file__).resolve().parent
REPO_ROOT = DEMO_ROOT.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from agent_evidence.media_bundle import build_media_bundle, verify_media_bundle  # noqa: E402
from agent_evidence.media_time import TIME_PROFILE, validate_media_time_profile  # noqa: E402

OUTPUT_DIR = DEMO_ROOT / "output" / "media_time_demo"
SOURCE_STATEMENT = (
    REPO_ROOT / "examples" / "media" / "time" / ("minimal-valid-time-aware-media-evidence.json")
)


def write_json(path: Path, payload: object) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def copy_bundle_tree(source: Path, target: Path) -> None:
    target.mkdir(parents=True, exist_ok=True)
    for name in (
        "bundle.json",
        "statement.json",
        "checksums.txt",
        "validation-report.json",
        "summary.json",
    ):
        shutil.copyfile(source / name, target / name)
    shutil.copytree(source / "artifacts", target / "artifacts")


def load_statement(bundle_dir: Path) -> dict[str, object]:
    return json.loads((bundle_dir / "statement.json").read_text(encoding="utf-8"))


def write_statement(bundle_dir: Path, statement: dict[str, object]) -> None:
    write_json(bundle_dir / "statement.json", statement)


def clock_trace_path(bundle_dir: Path) -> Path:
    statement = load_statement(bundle_dir)
    artifacts = statement["media"]["artifacts"]  # type: ignore[index]
    trace_artifact = next(artifact for artifact in artifacts if artifact["role"] == "clock_trace")
    return bundle_dir / trace_artifact["path"]


def tamper_clock_offset(bundle_dir: Path) -> None:
    trace_path = clock_trace_path(bundle_dir)
    trace = json.loads(trace_path.read_text(encoding="utf-8"))
    offsets = [2000000, 2100000, 1900000]
    for sample, offset in zip(trace["samples"], offsets, strict=True):
        sample["offset_ns"] = offset
    trace["summary"] = {
        "sample_count": 3,
        "max_abs_offset_ns": 2100000,
        "max_jitter_ns": 200000,
        "within_threshold": False,
    }
    write_json(trace_path, trace)


def tamper_clock_window(bundle_dir: Path) -> None:
    trace_path = clock_trace_path(bundle_dir)
    trace = json.loads(trace_path.read_text(encoding="utf-8"))
    trace["collection"]["start_utc"] = "2026-04-26T08:20:01Z"
    trace["collection"]["end_utc"] = "2026-04-26T08:20:02Z"
    write_json(trace_path, trace)


def tamper_missing_clock_ref(bundle_dir: Path) -> None:
    statement = load_statement(bundle_dir)
    statement["time_context"].pop("clock_trace_refs", None)  # type: ignore[index]
    write_statement(bundle_dir, statement)


def result_case(case: str, expected: str, report: dict[str, object]) -> dict[str, object]:
    issues = report["issues"]  # type: ignore[index]
    codes: list[str] = []
    for issue in issues:
        code = issue["code"]
        if code not in codes:
            codes.append(code)
    return {
        "case": case,
        "expected": expected,
        "observed_ok": report["ok"],
        "primary_codes": codes,
    }


def main() -> int:
    if OUTPUT_DIR.exists():
        shutil.rmtree(OUTPUT_DIR)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    print("Step 1: validate strict time media statement")
    time_report = validate_media_time_profile(SOURCE_STATEMENT)
    write_json(OUTPUT_DIR / "time-validation-report.json", time_report)
    print(f"- {time_report['summary']}")

    print("Step 2: build and strict-verify media bundle")
    build_media_bundle(SOURCE_STATEMENT, OUTPUT_DIR)
    strict_bundle_report = verify_media_bundle(OUTPUT_DIR, strict_time=True)
    write_json(OUTPUT_DIR / "strict-bundle-validation-report.json", strict_bundle_report)
    print(f"- {strict_bundle_report['summary']}")

    cases = [result_case("valid_time_aware_bundle", "pass", strict_bundle_report)]
    tamper_specs = [
        ("tampered_clock_offset", "tampered-clock-offset", tamper_clock_offset),
        ("tampered_clock_window", "tampered-clock-window", tamper_clock_window),
        ("tampered_missing_clock_ref", "tampered-missing-clock-ref", tamper_missing_clock_ref),
    ]

    print("Step 3: strict-verify time tampered bundles")
    for case_name, directory_name, tamper_func in tamper_specs:
        tampered_dir = OUTPUT_DIR / directory_name
        copy_bundle_tree(OUTPUT_DIR, tampered_dir)
        tamper_func(tampered_dir)
        report = verify_media_bundle(tampered_dir, strict_time=True)
        cases.append(result_case(case_name, "fail", report))
        print(f"- {case_name}: {report['summary']}")

    matrix = {
        "profile": "aep-media-time-tamper-matrix@0.1",
        "cases": cases,
    }
    write_json(OUTPUT_DIR / "time-tamper-matrix.json", matrix)
    print("- wrote time-tamper-matrix.json")

    if (
        time_report["ok"]
        and strict_bundle_report["ok"]
        and all(case["observed_ok"] is False for case in cases[1:])
    ):
        print(f"PASS {TIME_PROFILE} demo")
        return 0

    print(f"FAIL {TIME_PROFILE} demo")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
