from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from click.testing import CliRunner

from agent_evidence.cli.main import main
from agent_evidence.media_ieee_word_pack import build_aep_media_ieee_word_pack

REPO_ROOT = Path(__file__).resolve().parents[1]


def _template_exists() -> bool:
    return any(
        (REPO_ROOT / path).exists()
        for path in [
            "templates/Computer_Society_Word_template.zip",
            "Computer_Society_Word_template.zip",
            "docs/templates/Computer_Society_Word_template.zip",
            "docs/paper/ieee_tse_submission_resources/Computer_Society_Word_template.zip",
        ]
    )


def _text_files(root: Path) -> list[Path]:
    suffixes = {".csv", ".json", ".md", ".txt", ".xml"}
    return [path for path in root.rglob("*") if path.is_file() and path.suffix in suffixes]


def test_ieee_word_pack_builder_reports_template_status(tmp_path: Path) -> None:
    report = build_aep_media_ieee_word_pack(tmp_path, repo_root=REPO_ROOT)

    assert (tmp_path / "pack-manifest.json").exists()
    if _template_exists():
        assert report["outputs"]["word_ready_markdown"] is True
        assert report["outputs"]["supplementary_zip_generated"] is True
        assert (tmp_path / "supplementary" / "aep_media_supplementary_package.zip").exists()
    else:
        assert report["ok"] is False
        assert report["status"] == "blocked_template_missing"


def test_word_ready_markdown_contains_required_sections_if_template_available(
    tmp_path: Path,
) -> None:
    if not _template_exists():
        return
    build_aep_media_ieee_word_pack(tmp_path, repo_root=REPO_ROOT)
    text = (
        tmp_path / "manuscript" / "aep_media_tse_submission_draft_ieee_word_ready.md"
    ).read_text(encoding="utf-8")

    assert "I. Introduction" in text
    assert "VII. Evaluation" in text
    assert "IX. Threats to Validity" in text
    assert "XI. Conclusion" in text
    assert "Acknowledgment and AI-Assisted Writing Disclosure" in text


def test_pack_contains_non_claims_if_template_available(tmp_path: Path) -> None:
    if not _template_exists():
        return
    build_aep_media_ieee_word_pack(tmp_path, repo_root=REPO_ROOT)
    text = (
        tmp_path / "manuscript" / "aep_media_tse_submission_draft_ieee_word_ready.md"
    ).read_text(encoding="utf-8")

    assert "no legal admissibility" in text
    assert "no non-repudiation" in text
    assert "no real PTP proof" in text
    assert "no real C2PA signature verification" in text


def test_pack_contains_evaluation_numbers_if_template_available(tmp_path: Path) -> None:
    if not _template_exists():
        return
    build_aep_media_ieee_word_pack(tmp_path, repo_root=REPO_ROOT)
    text = (
        tmp_path / "manuscript" / "aep_media_tse_submission_draft_ieee_word_ready.md"
    ).read_text(encoding="utf-8")

    assert "18 cases" in text
    assert "26 cases" in text
    assert "23 cases" in text
    assert "31 cases" in text
    assert "external_verification_performed: false" in text


def test_pack_has_no_absolute_home_paths(tmp_path: Path) -> None:
    report = build_aep_media_ieee_word_pack(tmp_path, repo_root=REPO_ROOT)
    if not report["template"]["zip_found"]:
        return

    forbidden = {str(Path.home()), str(Path("/", "Users", "zhangbin"))}
    for path in _text_files(tmp_path):
        text = path.read_text(encoding="utf-8")
        for value in forbidden:
            assert value not in text, f"{path} contains {value}"


def test_pack_does_not_copy_paper_ncs(tmp_path: Path) -> None:
    report = build_aep_media_ieee_word_pack(tmp_path, repo_root=REPO_ROOT)
    if not report["template"]["zip_found"]:
        return

    forbidden = "paper-ncs-" + "execution-evidence"
    assert not any(forbidden in part for path in tmp_path.rglob("*") for part in path.parts)
    for path in _text_files(tmp_path):
        assert forbidden not in path.read_text(encoding="utf-8")


def test_cli_build_ieee_word_pack(tmp_path: Path) -> None:
    runner = CliRunner()
    result = runner.invoke(main, ["build-aep-media-ieee-word-pack", "--out", str(tmp_path)])

    if _template_exists():
        assert result.exit_code == 0, result.output
        assert "PASS aep-media-ieee-word-pack@0.1" in result.output
        manifest = json.loads((tmp_path / "pack-manifest.json").read_text(encoding="utf-8"))
        assert manifest["ok"] is True
    else:
        assert result.exit_code != 0
        assert "template_missing" in result.output


def test_ieee_word_pack_demo_runs_if_template_available() -> None:
    result = subprocess.run(
        [sys.executable, "demo/build_aep_media_ieee_word_pack.py"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )

    if _template_exists():
        assert result.returncode == 0, result.stderr
        assert "PASS aep-media-ieee-word-pack@0.1 demo" in result.stdout
    else:
        assert result.returncode != 0
        assert "template_missing" in result.stdout
