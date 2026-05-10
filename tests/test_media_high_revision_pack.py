from __future__ import annotations

import json
import re
import subprocess
import sys
import zipfile
from pathlib import Path

from click.testing import CliRunner

from agent_evidence.cli.main import main
from agent_evidence.media_final_journal_revision_pack import (
    RED_FLAG_PATTERNS,
    build_aep_media_high_revision_pack,
)

REPO_ROOT = Path(__file__).resolve().parents[1]


def _text_files(root: Path) -> list[Path]:
    return [
        path
        for path in root.rglob("*")
        if path.is_file() and path.suffix in {".csv", ".json", ".md", ".txt", ".xml"}
    ]


def test_high_revision_pack_builds(tmp_path: Path) -> None:
    report = build_aep_media_high_revision_pack(tmp_path, repo_root=REPO_ROOT)

    assert report["ok"] is True, report
    assert (tmp_path / "manuscript" / "aep_media_tse_submission_high_revision.docx").exists()
    assert (tmp_path / "manuscript" / "aep_media_tse_submission_high_revision.pdf").exists()
    assert (tmp_path / "supplementary" / "aep_media_supplementary_package.zip").exists()
    assert (tmp_path / "full-pack" / "aep_media_high_revision_submission_pack.zip").exists()
    assert (tmp_path / "metadata" / "pack-manifest.json").exists()


def test_high_revision_manuscript_no_editor_red_flags(tmp_path: Path) -> None:
    build_aep_media_high_revision_pack(tmp_path, repo_root=REPO_ROOT)
    text = (tmp_path / "manuscript" / "aep_media_tse_submission_high_revision.md").read_text(
        encoding="utf-8"
    )

    assert "Appendix Pointer" not in text
    assert "VIII. Optional External Tool Path" not in text
    assert "4.1" not in text
    for pattern in RED_FLAG_PATTERNS:
        assert pattern not in text


def test_high_revision_docx_headers_no_template_placeholder(tmp_path: Path) -> None:
    build_aep_media_high_revision_pack(tmp_path, repo_root=REPO_ROOT)
    docx_path = tmp_path / "manuscript" / "aep_media_tse_submission_high_revision.docx"

    with zipfile.ZipFile(docx_path) as archive:
        xml_text = "\n".join(
            archive.read(name).decode("utf-8", errors="ignore")
            for name in archive.namelist()
            if name.startswith(("word/header", "word/footer", "word/document"))
            and name.endswith(".xml")
        )

    assert "REPLACE THIS " + "LINE" not in xml_text
    assert "MANUSCRIPT " + "ID NUMBER" not in xml_text


def test_high_revision_cover_letter_single_author(tmp_path: Path) -> None:
    build_aep_media_high_revision_pack(tmp_path, repo_root=REPO_ROOT)
    text = (tmp_path / "cover-letter" / "aep_media_cover_letter_high_revision.md").read_text(
        encoding="utf-8"
    )

    assert "Dear Editor," in text
    assert "Sincerely,\n\nBin Zhang" in text
    assert "The authors" not in text
    assert "draft" not in text.lower()
    assert "manual upload" not in text.lower()


def test_high_revision_references_present(tmp_path: Path) -> None:
    build_aep_media_high_revision_pack(tmp_path, repo_root=REPO_ROOT)
    text = (tmp_path / "manuscript" / "aep_media_tse_submission_high_revision.md").read_text(
        encoding="utf-8"
    )
    body, _, refs = text.partition("## References")
    cited = {int(value) for value in re.findall(r"\[(\d+)\]", body)}
    defined = {int(value) for value in re.findall(r"^\[(\d+)\]", refs, flags=re.M)}

    assert len(defined) >= 16
    assert cited <= defined
    assert defined <= cited
    assert "IEEE Author" not in refs


def test_high_revision_supplementary_readme_present(tmp_path: Path) -> None:
    build_aep_media_high_revision_pack(tmp_path, repo_root=REPO_ROOT)
    readme = (tmp_path / "supplementary" / "README_SUPPLEMENTARY.md").read_text(encoding="utf-8")

    assert "what is not claimed" in readme.lower()
    assert "no external tools required" not in readme.lower()
    assert "does not require LinuxPTP" in readme


def test_high_revision_no_absolute_home_paths(tmp_path: Path) -> None:
    build_aep_media_high_revision_pack(tmp_path, repo_root=REPO_ROOT)
    forbidden = {str(Path.home()), str(Path("/", "Users", "zhangbin"))}
    for path in _text_files(tmp_path):
        text = path.read_text(encoding="utf-8")
        for value in forbidden:
            assert value not in text, f"{path} contains {value}"


def test_high_revision_no_paper_ncs(tmp_path: Path) -> None:
    build_aep_media_high_revision_pack(tmp_path, repo_root=REPO_ROOT)
    forbidden = "paper-ncs-" + "execution-evidence"

    assert not any(forbidden in part for path in tmp_path.rglob("*") for part in path.parts)
    for path in _text_files(tmp_path):
        assert forbidden not in path.read_text(encoding="utf-8")


def test_cli_build_high_revision_pack(tmp_path: Path) -> None:
    runner = CliRunner()
    result = runner.invoke(
        main,
        ["build-aep-media-high-revision-pack", "--out", str(tmp_path)],
    )

    assert result.exit_code == 0, result.output
    assert "PASS aep-media-high-revision-pack@0.1" in result.output
    manifest = json.loads((tmp_path / "metadata" / "pack-manifest.json").read_text())
    assert manifest["ok"] is True


def test_high_revision_demo_runs() -> None:
    result = subprocess.run(
        [sys.executable, "demo/build_aep_media_high_revision_pack.py"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    assert "PASS aep-media-high-revision-pack@0.1 demo" in result.stdout
