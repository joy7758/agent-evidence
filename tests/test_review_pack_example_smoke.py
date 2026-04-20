import json
import subprocess
import sys
from pathlib import Path


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def _run_json_command(args: list[str], *, cwd: Path) -> dict[str, object]:
    result = subprocess.run(
        args,
        cwd=cwd,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr
    return json.loads(result.stdout)


def test_review_pack_example_smoke(tmp_path: Path) -> None:
    repo_root = _repo_root()
    run_dir = tmp_path / "langchain-run"
    pack_dir = tmp_path / "review-pack"
    primary_only_pack_dir = tmp_path / "review-pack-primary-only"

    langchain_example = repo_root / "examples" / "langchain_minimal_evidence.py"
    review_pack_example = repo_root / "examples" / "review_pack" / "build_review_pack.py"

    example_payload = _run_json_command(
        [sys.executable, str(langchain_example), "--output-dir", str(run_dir)],
        cwd=repo_root,
    )
    assert example_payload["ok"] is True

    bundle_path = run_dir / "langchain-evidence.bundle.json"
    receipt_path = run_dir / "receipt.json"
    summary_path = run_dir / "summary.json"
    manifest_path = run_dir / "langchain-evidence.manifest.json"
    public_key_path = run_dir / "manifest-public.pem"
    runtime_events_path = run_dir / "runtime-events.jsonl"
    private_key_path = run_dir / "manifest-private.pem"

    for path in (
        bundle_path,
        receipt_path,
        summary_path,
        manifest_path,
        public_key_path,
        runtime_events_path,
        private_key_path,
    ):
        assert path.exists()

    pack_payload = _run_json_command(
        [
            sys.executable,
            str(review_pack_example),
            "--bundle-path",
            str(bundle_path),
            "--receipt-path",
            str(receipt_path),
            "--summary-path",
            str(summary_path),
            "--manifest-path",
            str(manifest_path),
            "--public-key-path",
            str(public_key_path),
            "--runtime-events-path",
            str(runtime_events_path),
            "--private-key-path",
            str(private_key_path),
            "--output-dir",
            str(pack_dir),
        ],
        cwd=repo_root,
    )

    pack_root = Path(str(pack_payload["pack_dir"]))
    index_path = Path(str(pack_payload["index_path"]))
    report_path = Path(str(pack_payload["report_path"]))
    assert pack_root.exists()
    assert index_path.exists()
    assert report_path.exists()
    assert (pack_root / "primary" / "bundle.json").exists()
    assert (pack_root / "primary" / "receipt.json").exists()
    assert (pack_root / "primary" / "summary.json").exists()
    assert (pack_root / "review" / "report.md").exists()
    assert (pack_root / "review" / "report.pdf").exists()
    assert (pack_root / "review" / "report.pdf").read_bytes().startswith(b"%PDF")
    assert (pack_root / "index.json").exists()
    assert not (pack_root / "supporting" / "manifest-private.pem").exists()

    pack_index = json.loads(index_path.read_text(encoding="utf-8"))
    assert pack_index["excluded_supporting_files"] == ["private_key"]
    assert pack_index["supporting_files"] == {
        "manifest": "supporting/manifest.json",
        "public_key": "supporting/manifest-public.pem",
        "runtime_events": "supporting/runtime-events.jsonl",
    }
    assert "private_key" not in pack_payload["supporting_files"]

    primary_only_payload = _run_json_command(
        [
            sys.executable,
            str(review_pack_example),
            "--bundle-path",
            str(bundle_path),
            "--receipt-path",
            str(receipt_path),
            "--summary-path",
            str(summary_path),
            "--output-dir",
            str(primary_only_pack_dir),
        ],
        cwd=repo_root,
    )

    primary_only_root = Path(str(primary_only_payload["pack_dir"]))
    assert primary_only_root.exists()
    assert (primary_only_root / "primary" / "bundle.json").exists()
    assert (primary_only_root / "primary" / "receipt.json").exists()
    assert (primary_only_root / "primary" / "summary.json").exists()
    assert (primary_only_root / "review" / "report.md").exists()
    assert (primary_only_root / "review" / "report.pdf").exists()
    assert (primary_only_root / "review" / "report.pdf").read_bytes().startswith(b"%PDF")
    assert (primary_only_root / "index.json").exists()
    assert not (primary_only_root / "supporting").exists()
    assert primary_only_payload["supporting_files"] == {}
