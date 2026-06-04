import hashlib
import json
import zipfile
from pathlib import Path

from click.testing import CliRunner

from agent_evidence.cli.main import main
from agent_evidence.review_pack import (
    PAPER_MINIMAL_REQUIRED_FILES,
    create_paper_minimal_review_pack,
    verify_review_pack_manifest,
)

ROOT = Path(__file__).resolve().parents[1]


def _sha256(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def test_create_paper_minimal_review_pack_manifest_and_boundary(tmp_path: Path) -> None:
    output_path = tmp_path / "review-pack-paper-minimal.zip"

    report = create_paper_minimal_review_pack(ROOT, output_path)

    assert report["ok"] is True
    assert output_path.is_file()

    with zipfile.ZipFile(output_path) as archive:
        names = set(archive.namelist())
        required_files = set(PAPER_MINIMAL_REQUIRED_FILES)
        required_files.update(
            {
                "CLAIM_BOUNDARY.md",
                "REPRODUCE.md",
                "PACKAGE_INFO.json",
                "MANIFEST.json",
            }
        )
        assert required_files <= names

        manifest = json.loads(archive.read("MANIFEST.json"))
        entries = {entry["path"]: entry for entry in manifest["files"]}
        assert set(PAPER_MINIMAL_REQUIRED_FILES) <= set(entries)
        assert "CLAIM_BOUNDARY.md" in entries
        assert "REPRODUCE.md" in entries
        assert "PACKAGE_INFO.json" in entries

        for relative_path, entry in entries.items():
            payload = archive.read(relative_path)
            assert entry["size_bytes"] == len(payload)
            assert entry["sha256"] == _sha256(payload)

        claim_boundary = archive.read("CLAIM_BOUNDARY.md").decode("utf-8")
        for non_claim in (
            "registry design",
            "multi-agent orchestration",
            "full FDO interoperability",
            "full cryptographic trust fabric",
            "legal non-repudiation",
            "production deployment",
            "broad platform governance",
            "broad runtime integration coverage",
        ):
            assert non_claim in claim_boundary

        reproduce = archive.read("REPRODUCE.md").decode("utf-8")
        assert "This review package is a paper-minimal inspection package" in reproduce
        assert "bash scripts/reproduce_paper_minimal.sh" in reproduce

        package_info = json.loads(archive.read("PACKAGE_INFO.json"))
        assert package_info["package_name"] == "review-pack-paper-minimal"
        assert package_info["profile_name"] == "execution-evidence-operation-accountability-profile"
        assert package_info["profile_version"] == "0.1"
        assert package_info["paper_minimal"] is True
        assert package_info["included_examples"] == [
            "examples/minimal-valid-evidence.json",
            "examples/invalid-missing-required.json",
            "examples/invalid-unclosed-reference.json",
            "examples/invalid-policy-link-broken.json",
        ]

        script_mode = archive.getinfo("scripts/reproduce_paper_minimal.sh").external_attr >> 16
        assert script_mode & 0o111

    verification = verify_review_pack_manifest(output_path, tmp_path / "check")
    assert verification["ok"] is True, verification["issues"]


def test_cli_creates_paper_minimal_review_pack(tmp_path: Path, monkeypatch) -> None:
    output_path = tmp_path / "review-pack-paper-minimal.zip"
    monkeypatch.chdir(ROOT)
    runner = CliRunner()

    result = runner.invoke(
        main,
        ["review-pack", "create", "--paper-minimal", "--out", str(output_path)],
    )

    assert result.exit_code == 0, result.output
    report = json.loads(result.output)
    assert report["ok"] is True
    assert report["output"] == str(output_path.resolve())
    assert output_path.is_file()


def test_cli_review_pack_create_requires_paper_minimal(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(ROOT)
    runner = CliRunner()

    result = runner.invoke(
        main,
        ["review-pack", "create", "--out", str(tmp_path / "review-pack.zip")],
    )

    assert result.exit_code != 0
    assert "Only --paper-minimal review packages are currently supported" in result.output
