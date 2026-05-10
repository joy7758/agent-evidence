import json
import subprocess
import sys
from pathlib import Path

from agent_evidence.media_bundle import build_media_bundle, verify_media_bundle

ROOT = Path(__file__).resolve().parents[1]
SOURCE_STATEMENT = ROOT / "examples" / "media" / "minimal-valid-media-evidence.json"
DEMO_SCRIPT = ROOT / "demo" / "run_media_bundle_demo.py"
DEMO_OUTPUT = ROOT / "demo" / "output" / "media_bundle_demo"


def issue_codes(report: dict[str, object]) -> set[str]:
    return {issue["code"] for issue in report["issues"]}  # type: ignore[index]


def build_bundle(tmp_path: Path) -> Path:
    bundle_dir = tmp_path / "aep-media-bundle"
    build_media_bundle(SOURCE_STATEMENT, bundle_dir)
    return bundle_dir


def load_statement(bundle_dir: Path) -> dict[str, object]:
    return json.loads((bundle_dir / "statement.json").read_text(encoding="utf-8"))


def write_statement(bundle_dir: Path, statement: dict[str, object]) -> None:
    (bundle_dir / "statement.json").write_text(
        json.dumps(statement, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def primary_artifact_path(bundle_dir: Path) -> Path:
    statement = load_statement(bundle_dir)
    artifacts = statement["media"]["artifacts"]  # type: ignore[index]
    primary = next(artifact for artifact in artifacts if artifact["role"] == "primary_media")
    return bundle_dir / primary["path"]


def test_build_media_bundle_from_valid_statement(tmp_path: Path) -> None:
    bundle_dir = build_bundle(tmp_path)

    assert (bundle_dir / "bundle.json").exists()
    assert (bundle_dir / "statement.json").exists()
    assert (bundle_dir / "checksums.txt").exists()
    assert (bundle_dir / "validation-report.json").exists()
    assert (bundle_dir / "summary.json").exists()
    assert any((bundle_dir / "artifacts").iterdir())


def test_verify_media_bundle_passes(tmp_path: Path) -> None:
    bundle_dir = build_bundle(tmp_path)

    report = verify_media_bundle(bundle_dir)

    assert report["ok"] is True
    assert report["issue_count"] == 0


def test_tampered_artifact_fails(tmp_path: Path) -> None:
    bundle_dir = build_bundle(tmp_path)
    with primary_artifact_path(bundle_dir).open("ab") as artifact_file:
        artifact_file.write(b"\ntampered bytes\n")

    report = verify_media_bundle(bundle_dir)

    assert report["ok"] is False
    assert issue_codes(report) & {"bundle_checksum_mismatch", "media_hash_mismatch"}


def test_tampered_statement_missing_time_context_fails(tmp_path: Path) -> None:
    bundle_dir = build_bundle(tmp_path)
    statement = load_statement(bundle_dir)
    statement.pop("time_context", None)
    write_statement(bundle_dir, statement)

    report = verify_media_bundle(bundle_dir)

    assert report["ok"] is False
    assert issue_codes(report) & {"missing_time_context", "media_profile_validation_failed"}


def test_tampered_statement_policy_ref_fails(tmp_path: Path) -> None:
    bundle_dir = build_bundle(tmp_path)
    statement = load_statement(bundle_dir)
    statement["operation"]["policy_ref"] = "policy:missing-policy"  # type: ignore[index]
    write_statement(bundle_dir, statement)

    report = verify_media_bundle(bundle_dir)

    assert report["ok"] is False
    assert issue_codes(report) & {"unresolved_policy_ref", "media_profile_validation_failed"}


def test_media_bundle_demo_runs() -> None:
    result = subprocess.run(
        [sys.executable, str(DEMO_SCRIPT)],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stdout + result.stderr
    assert (DEMO_OUTPUT / "bundle.json").exists()
    matrix_path = DEMO_OUTPUT / "tamper-matrix.json"
    assert matrix_path.exists()

    matrix = json.loads(matrix_path.read_text(encoding="utf-8"))
    pass_cases = [case for case in matrix["cases"] if case["observed_ok"] is True]
    fail_cases = [case for case in matrix["cases"] if case["observed_ok"] is False]
    assert len(pass_cases) >= 1
    assert len(fail_cases) >= 3


def test_bundle_rejects_path_escape(tmp_path: Path) -> None:
    bundle_dir = build_bundle(tmp_path)
    bundle_path = bundle_dir / "bundle.json"
    bundle = json.loads(bundle_path.read_text(encoding="utf-8"))
    bundle["artifacts"][0]["path"] = "../evil"  # type: ignore[index]
    bundle_path.write_text(json.dumps(bundle, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    report = verify_media_bundle(bundle_dir)

    assert report["ok"] is False
    assert "bundle_path_escape" in issue_codes(report)
