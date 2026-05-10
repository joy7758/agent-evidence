from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from click.testing import CliRunner

from agent_evidence.cli.main import main
from agent_evidence.media_release_pack import build_aep_media_release_pack

REPO_ROOT = Path(__file__).resolve().parents[1]


def _text_files(root: Path) -> list[Path]:
    suffixes = {".csv", ".json", ".md", ".txt"}
    return [path for path in root.rglob("*") if path.is_file() and path.suffix in suffixes]


def test_build_aep_media_release_pack(tmp_path: Path) -> None:
    report = build_aep_media_release_pack(tmp_path, repo_root=REPO_ROOT)

    assert report["ok"] is True
    assert (tmp_path / "release-summary.json").exists()
    assert (tmp_path / "claim-boundary.md").exists()
    assert (tmp_path / "reproducibility-checklist.md").exists()
    assert (tmp_path / "artifact-inventory.json").exists()
    assert (tmp_path / "checksums.sha256").exists()
    assert (tmp_path / "paper" / "aep_media_manuscript_draft.md").exists()


def test_release_pack_has_no_absolute_home_paths(tmp_path: Path) -> None:
    build_aep_media_release_pack(tmp_path, repo_root=REPO_ROOT)

    forbidden = {str(Path.home()), str(Path("/", "Users", "zhangbin"))}
    for path in _text_files(tmp_path):
        text = path.read_text(encoding="utf-8")
        for value in forbidden:
            assert value not in text, f"{path} contains {value}"


def test_release_pack_does_not_copy_unrelated_paper_workspace(tmp_path: Path) -> None:
    build_aep_media_release_pack(tmp_path, repo_root=REPO_ROOT)

    forbidden = "paper-ncs-" + "execution-evidence"
    assert not any(forbidden in part for path in tmp_path.rglob("*") for part in path.parts)
    for path in _text_files(tmp_path):
        assert forbidden not in path.read_text(encoding="utf-8")


def test_release_pack_claim_boundary_contains_non_claims(tmp_path: Path) -> None:
    build_aep_media_release_pack(tmp_path, repo_root=REPO_ROOT)

    text = (tmp_path / "claim-boundary.md").read_text(encoding="utf-8")
    assert "legal admissibility" in text
    assert "non-repudiation" in text
    assert "trusted timestamping" in text
    assert "real PTP" in text
    assert "C2PA signature verification" in text


def test_cli_build_aep_media_release_pack(tmp_path: Path) -> None:
    runner = CliRunner()
    result = runner.invoke(main, ["build-aep-media-release-pack", "--out", str(tmp_path)])

    assert result.exit_code == 0, result.output
    assert "PASS aep-media-release-pack@0.1" in result.output
    assert (tmp_path / "release-summary.json").exists()


def test_release_pack_demo_runs() -> None:
    result = subprocess.run(
        [sys.executable, "demo/build_aep_media_release_pack.py"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    assert "PASS aep-media-release-pack@0.1 demo" in result.stdout
    summary_path = REPO_ROOT / "demo" / "output" / "aep_media_release_pack" / "release-summary.json"
    assert summary_path.exists()
    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    assert summary["ok"] is True
