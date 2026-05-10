import json
import subprocess
import sys
from pathlib import Path

from click.testing import CliRunner

from agent_evidence.cli.main import main
from agent_evidence.media_evaluation import run_media_evaluation

ROOT = Path(__file__).resolve().parents[1]
DEMO_SCRIPT = ROOT / "demo" / "run_media_evaluation_demo.py"
DEMO_OUTPUT = ROOT / "demo" / "output" / "media_evaluation_demo"

REQUIRED_CASES = {
    "profile_valid",
    "profile_missing_time_context",
    "profile_broken_media_hash",
    "profile_unresolved_policy_ref",
    "bundle_valid_build",
    "bundle_valid_verify",
    "bundle_tampered_artifact",
    "bundle_tampered_missing_time_context",
    "bundle_tampered_policy_ref",
    "bundle_path_escape",
    "time_valid",
    "time_missing_clock_trace_ref",
    "time_offset_threshold",
    "time_window_mismatch",
    "time_bundle_strict_valid",
    "time_tampered_clock_offset",
    "time_tampered_clock_window",
    "time_tampered_missing_clock_ref",
}


def run_pack(tmp_path: Path) -> Path:
    out_dir = tmp_path / "evaluation-pack"
    summary = run_media_evaluation(out_dir, repo_root=ROOT)
    assert summary["ok"] is True
    return out_dir


def load_matrix(out_dir: Path) -> dict[str, object]:
    return json.loads((out_dir / "evaluation-matrix.json").read_text(encoding="utf-8"))


def case_by_id(matrix: dict[str, object], case_id: str) -> dict[str, object]:
    return next(case for case in matrix["cases"] if case["case_id"] == case_id)  # type: ignore[index]


def test_run_media_evaluation_pack(tmp_path: Path) -> None:
    out_dir = run_pack(tmp_path)
    summary = json.loads((out_dir / "evaluation-summary.json").read_text(encoding="utf-8"))

    assert summary["ok"] is True
    assert summary["case_count"] >= 18
    assert summary["unexpected_count"] == 0
    assert (out_dir / "evaluation-summary.json").exists()
    assert (out_dir / "evaluation-matrix.json").exists()
    assert (out_dir / "evaluation-matrix.md").exists()
    assert (out_dir / "artifact-inventory.json").exists()
    assert (out_dir / "reproducibility-commands.md").exists()
    assert (out_dir / "non-claims-matrix.md").exists()


def test_evaluation_matrix_contains_required_cases(tmp_path: Path) -> None:
    out_dir = run_pack(tmp_path)
    matrix = load_matrix(out_dir)
    cases = {case["case_id"]: case for case in matrix["cases"]}  # type: ignore[index]

    assert REQUIRED_CASES.issubset(cases)
    assert len(cases) >= 18
    assert all(case["matched_expectation"] is True for case in cases.values())


def test_time_tamper_cases_have_time_specific_codes(tmp_path: Path) -> None:
    out_dir = run_pack(tmp_path)
    matrix = load_matrix(out_dir)

    offset = case_by_id(matrix, "time_tampered_clock_offset")
    window = case_by_id(matrix, "time_tampered_clock_window")
    missing = case_by_id(matrix, "time_tampered_missing_clock_ref")
    assert "clock_offset_threshold_exceeded" in offset["primary_codes"]
    assert "clock_trace_window_mismatch" in window["primary_codes"]
    assert "missing_clock_trace_ref" in missing["primary_codes"]


def test_artifact_inventory_hashes_exist(tmp_path: Path) -> None:
    out_dir = run_pack(tmp_path)
    inventory = json.loads((out_dir / "artifact-inventory.json").read_text(encoding="utf-8"))

    for items in inventory.values():
        for item in items:
            if item["exists"] is True:
                assert item["sha256"]
                assert isinstance(item["size_bytes"], int)


def test_media_evaluation_demo_runs() -> None:
    result = subprocess.run(
        [sys.executable, str(DEMO_SCRIPT)],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stdout + result.stderr
    assert (DEMO_OUTPUT / "evaluation-summary.json").exists()
    assert "PASS aep-media-evaluation@0.1 demo" in result.stdout


def test_cli_run_media_evaluation(tmp_path: Path) -> None:
    runner = CliRunner()
    result = runner.invoke(
        main,
        ["run-media-evaluation", "--out", str(tmp_path / "cli-evaluation")],
    )

    assert result.exit_code == 0, result.output
    assert "PASS aep-media-evaluation@0.1" in result.output
