from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from click.testing import CliRunner

from agent_evidence.cli.main import main
from agent_evidence.media_submission_pack import build_aep_media_submission_pack

REPO_ROOT = Path(__file__).resolve().parents[1]


def _text_files(root: Path) -> list[Path]:
    suffixes = {".csv", ".json", ".md", ".txt"}
    return [path for path in root.rglob("*") if path.is_file() and path.suffix in suffixes]


def test_build_aep_media_submission_pack(tmp_path: Path) -> None:
    report = build_aep_media_submission_pack(tmp_path, repo_root=REPO_ROOT)

    assert report["ok"] is True
    assert report["journal_target"]["submission_status"] == "prepared_locally_" + "not_submitted"
    assert (tmp_path / "manuscript" / "aep_media_tse_submission_draft.md").exists()
    assert (tmp_path / "supplement" / "aep_media_submission_appendix.md").exists()
    assert (tmp_path / "format" / "aep_media_tse_format_preflight.md").exists()
    assert (tmp_path / "release-pack" / "release-summary.json").exists()
    assert (tmp_path / "pack-manifest.json").exists()
    assert (tmp_path / "checksums.sha256").exists()


def test_submission_pack_has_no_absolute_home_paths(tmp_path: Path) -> None:
    build_aep_media_submission_pack(tmp_path, repo_root=REPO_ROOT)

    forbidden = {str(Path.home()), str(Path("/", "Users", "zhangbin"))}
    for path in _text_files(tmp_path):
        text = path.read_text(encoding="utf-8")
        for value in forbidden:
            assert value not in text, f"{path} contains {value}"


def test_submission_pack_non_claim_checks(tmp_path: Path) -> None:
    report = build_aep_media_submission_pack(tmp_path, repo_root=REPO_ROOT)

    assert all(report["non_claim_checks"].values())
    manuscript = (tmp_path / "manuscript" / "aep_media_tse_submission_draft.md").read_text(
        encoding="utf-8"
    )
    assert "does not claim real PTP proof" in manuscript
    assert "does not claim full MP4 PRFT parsing" in manuscript
    assert "does not claim real C2PA signature verification" in manuscript
    assert "does not claim non-repudiation" in manuscript


def test_cli_build_aep_media_submission_pack(tmp_path: Path) -> None:
    runner = CliRunner()
    result = runner.invoke(main, ["build-aep-media-submission-pack", "--out", str(tmp_path)])

    assert result.exit_code == 0, result.output
    assert "PASS aep-media-submission-pack@0.1" in result.output
    assert (tmp_path / "pack-manifest.json").exists()


def test_submission_pack_demo_runs() -> None:
    result = subprocess.run(
        [sys.executable, "demo/build_aep_media_submission_pack.py"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    assert "PASS aep-media-submission-pack@0.1 demo" in result.stdout
    manifest_path = (
        REPO_ROOT / "demo" / "output" / "aep_media_submission_pack" / "pack-manifest.json"
    )
    assert manifest_path.exists()
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert manifest["ok"] is True
