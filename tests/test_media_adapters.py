import json
import subprocess
import sys
from pathlib import Path

from agent_evidence.adapters.c2pa_manifest import ingest_c2pa_manifest
from agent_evidence.adapters.ffmpeg_prft import ingest_ffmpeg_prft
from agent_evidence.adapters.linuxptp import ingest_linuxptp_trace
from agent_evidence.media_adapter_evaluation import (
    create_adapter_backed_statement,
    run_media_adapter_evaluation,
)
from agent_evidence.media_evaluation import run_media_evaluation
from agent_evidence.media_optional_tools import run_optional_tool_evaluation

ROOT = Path(__file__).resolve().parents[1]
DEMO_SCRIPT = ROOT / "demo" / "run_media_adapter_demo.py"
DEMO_OUTPUT = ROOT / "demo" / "output" / "media_adapter_demo"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def issue_codes(report: dict) -> set[str]:
    return {issue["code"] for issue in report.get("issues", [])}


def test_linuxptp_ptp4l_fixture_ingests_to_valid_time_trace(tmp_path: Path) -> None:
    out_path = tmp_path / "clock-trace.json"
    report = ingest_linuxptp_trace(
        ROOT / "examples/media/adapters/linuxptp/ptp4l-sample.log",
        out_path,
    )
    trace = load_json(out_path)

    assert report["ok"] is True
    assert trace["profile"]["name"] == "aep-media-time-trace"
    assert trace["summary"]["within_threshold"] is True


def test_linuxptp_phc2sys_fixture_ingests(tmp_path: Path) -> None:
    out_path = tmp_path / "clock-trace.json"
    report = ingest_linuxptp_trace(
        ROOT / "examples/media/adapters/linuxptp/phc2sys-sample.log",
        out_path,
    )
    trace = load_json(out_path)

    assert report["ok"] is True
    assert trace["profile"]["name"] == "aep-media-time-trace"
    assert trace["summary"]["within_threshold"] is True


def test_linuxptp_empty_fixture_fails(tmp_path: Path) -> None:
    report = ingest_linuxptp_trace(
        ROOT / "examples/media/adapters/linuxptp/invalid-empty.log",
        tmp_path / "clock-trace.json",
    )

    assert report["ok"] is False
    assert "linuxptp_no_samples" in issue_codes(report)


def test_ffmpeg_prft_fixture_ingests(tmp_path: Path) -> None:
    out_path = tmp_path / "ffmpeg-prft-metadata.json"
    report = ingest_ffmpeg_prft(
        ROOT / "examples/media/adapters/ffmpeg/ffprobe-prft-sample.json",
        out_path,
    )
    metadata = load_json(out_path)

    assert report["ok"] is True
    assert metadata["timing"]["prft_detected"] is True


def test_ffmpeg_no_prft_fixture_fails(tmp_path: Path) -> None:
    out_path = tmp_path / "ffmpeg-no-prft-metadata.json"
    report = ingest_ffmpeg_prft(
        ROOT / "examples/media/adapters/ffmpeg/ffprobe-no-prft-sample.json",
        out_path,
    )

    assert report["ok"] is False
    assert "ffmpeg_prft_not_found" in issue_codes(report)
    assert load_json(out_path)["timing"]["prft_detected"] is False


def test_c2pa_valid_like_manifest_ingests(tmp_path: Path) -> None:
    out_path = tmp_path / "c2pa-metadata.json"
    report = ingest_c2pa_manifest(
        ROOT / "examples/media/adapters/c2pa/c2pa-manifest-valid-like.json",
        out_path,
    )
    metadata = load_json(out_path)

    assert report["ok"] is True
    assert metadata["manifest"]["signature_status"] == "declared_valid"
    assert metadata["manifest"]["external_verification_performed"] is False
    assert metadata["claim_boundary"]["real_signature_verified"] is False


def test_c2pa_invalid_signature_like_manifest_fails(tmp_path: Path) -> None:
    out_path = tmp_path / "c2pa-metadata.json"
    report = ingest_c2pa_manifest(
        ROOT / "examples/media/adapters/c2pa/c2pa-manifest-invalid-signature-like.json",
        out_path,
    )

    assert report["ok"] is False
    assert "c2pa_signature_invalid_declared" in issue_codes(report)


def test_adapter_backed_statement_strict_bundle_passes(tmp_path: Path) -> None:
    report = create_adapter_backed_statement(tmp_path / "adapter-backed", repo_root=ROOT)

    assert report["ok"] is True
    assert report["time_profile_ok"] is True
    assert report["bundle_strict_time_ok"] is True
    assert (tmp_path / "adapter-backed" / "adapter-backed-media-evidence.json").exists()


def test_media_adapter_demo_runs() -> None:
    result = subprocess.run(
        [sys.executable, str(DEMO_SCRIPT)],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stdout + result.stderr
    assert "PASS aep-media-adapters@0.1 demo" in result.stdout
    assert (DEMO_OUTPUT / "adapter-demo-summary.json").exists()


def test_adapter_evaluation_pack_runs(tmp_path: Path) -> None:
    summary = run_media_adapter_evaluation(tmp_path / "adapter-evaluation", repo_root=ROOT)

    assert summary["ok"] is True
    assert summary["case_count"] >= 8
    assert summary["unexpected_count"] == 0


def test_run_media_evaluation_include_adapters(tmp_path: Path) -> None:
    out_dir = tmp_path / "evaluation-with-adapters"
    summary = run_media_evaluation(out_dir, repo_root=ROOT, include_adapters=True)
    matrix = load_json(out_dir / "evaluation-matrix.json")
    case_ids = {case["case_id"] for case in matrix["cases"]}

    assert summary["ok"] is True
    assert summary["case_count"] >= 26
    assert "adapter_ingestion" in summary["categories"]
    assert "profile_valid" in case_ids
    assert "adapter_backed_strict_time_bundle_valid" in case_ids


def test_run_media_evaluation_default_still_18_or_original(tmp_path: Path) -> None:
    out_dir = tmp_path / "evaluation-default"
    summary = run_media_evaluation(out_dir, repo_root=ROOT)
    matrix = load_json(out_dir / "evaluation-matrix.json")
    case_ids = {case["case_id"] for case in matrix["cases"]}

    assert summary["ok"] is True
    assert summary["case_count"] == 18
    assert "adapter_ingestion" not in summary["categories"]
    assert all(not case_id.startswith("adapter_") for case_id in case_ids)


def test_optional_tool_evaluation_records_tool_status(tmp_path: Path) -> None:
    out_dir = tmp_path / "optional-tools"
    summary = run_optional_tool_evaluation(out_dir)

    assert summary["ok"] is True
    assert summary["case_count"] == 5
    assert "failed_count" in summary
    assert (out_dir / "optional-tool-summary.json").exists()


def test_run_media_evaluation_include_optional_tools(tmp_path: Path) -> None:
    out_dir = tmp_path / "evaluation-with-tools"
    summary = run_media_evaluation(out_dir, repo_root=ROOT, include_optional_tools=True)
    matrix = load_json(out_dir / "evaluation-matrix.json")
    case_ids = {case["case_id"] for case in matrix["cases"]}

    assert summary["ok"] is True
    assert summary["case_count"] == 23
    assert "optional_tool_integration" in summary["categories"]
    assert "optional_linuxptp_ptp4l_version" in case_ids
    assert (out_dir / "optional-tool-evaluation" / "optional-tool-summary.json").exists()
