import json
import subprocess
import sys
from pathlib import Path

from agent_evidence.media_bundle import build_media_bundle, verify_media_bundle
from agent_evidence.media_time import validate_media_time_profile

ROOT = Path(__file__).resolve().parents[1]
TIME_EXAMPLES = ROOT / "examples" / "media" / "time"
VALID_STATEMENT = TIME_EXAMPLES / "minimal-valid-time-aware-media-evidence.json"
DEMO_SCRIPT = ROOT / "demo" / "run_media_time_demo.py"
DEMO_OUTPUT = ROOT / "demo" / "output" / "media_time_demo"


def issue_codes(report: dict[str, object]) -> set[str]:
    codes = {issue["code"] for issue in report["issues"]}  # type: ignore[index]
    time_report = report.get("time_profile_report")
    if isinstance(time_report, dict):
        codes.update(issue["code"] for issue in time_report.get("issues", []))
    return codes


def build_bundle(tmp_path: Path) -> Path:
    bundle_dir = tmp_path / "aep-media-time-bundle"
    build_media_bundle(VALID_STATEMENT, bundle_dir)
    return bundle_dir


def load_statement(bundle_dir: Path) -> dict[str, object]:
    return json.loads((bundle_dir / "statement.json").read_text(encoding="utf-8"))


def write_json(path: Path, payload: object) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def clock_trace_path(bundle_dir: Path) -> Path:
    statement = load_statement(bundle_dir)
    artifacts = statement["media"]["artifacts"]  # type: ignore[index]
    trace_artifact = next(artifact for artifact in artifacts if artifact["role"] == "clock_trace")
    return bundle_dir / trace_artifact["path"]


def test_valid_time_aware_media_profile_passes() -> None:
    report = validate_media_time_profile(VALID_STATEMENT)

    assert report["ok"] is True
    assert report["issue_count"] == 0


def test_missing_clock_trace_ref_fails() -> None:
    report = validate_media_time_profile(TIME_EXAMPLES / "invalid-missing-clock-trace-ref.json")

    assert report["ok"] is False
    assert "missing_clock_trace_ref" in issue_codes(report)


def test_clock_offset_threshold_fails() -> None:
    report = validate_media_time_profile(TIME_EXAMPLES / "invalid-clock-offset-threshold.json")

    assert report["ok"] is False
    assert "clock_offset_threshold_exceeded" in issue_codes(report)


def test_clock_window_mismatch_fails() -> None:
    report = validate_media_time_profile(TIME_EXAMPLES / "invalid-clock-window-mismatch.json")

    assert report["ok"] is False
    assert "clock_trace_window_mismatch" in issue_codes(report)


def test_build_and_verify_bundle_strict_time_passes(tmp_path: Path) -> None:
    bundle_dir = build_bundle(tmp_path)

    report = verify_media_bundle(bundle_dir, strict_time=True)

    assert report["ok"] is True
    assert report["time_profile_ok"] is True


def test_verify_bundle_strict_time_detects_missing_clock_ref(tmp_path: Path) -> None:
    bundle_dir = build_bundle(tmp_path)
    statement = load_statement(bundle_dir)
    statement["time_context"].pop("clock_trace_refs", None)  # type: ignore[index]
    write_json(bundle_dir / "statement.json", statement)

    report = verify_media_bundle(bundle_dir, strict_time=True)

    assert report["ok"] is False
    assert "missing_clock_trace_ref" in issue_codes(report)


def test_verify_bundle_strict_time_detects_offset_tamper(tmp_path: Path) -> None:
    bundle_dir = build_bundle(tmp_path)
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

    report = verify_media_bundle(bundle_dir, strict_time=True)

    assert report["ok"] is False
    assert "clock_offset_threshold_exceeded" in issue_codes(report)


def test_media_time_demo_runs() -> None:
    result = subprocess.run(
        [sys.executable, str(DEMO_SCRIPT)],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stdout + result.stderr
    matrix_path = DEMO_OUTPUT / "time-tamper-matrix.json"
    assert matrix_path.exists()

    matrix = json.loads(matrix_path.read_text(encoding="utf-8"))
    pass_cases = [case for case in matrix["cases"] if case["observed_ok"] is True]
    fail_cases = [case for case in matrix["cases"] if case["observed_ok"] is False]
    assert len(pass_cases) >= 1
    assert len(fail_cases) >= 3
