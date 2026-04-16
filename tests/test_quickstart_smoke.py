import json
import shutil
import subprocess
import sys
from pathlib import Path


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def _agent_evidence_cli() -> Path:
    candidates = [
        Path(sys.executable).with_name("agent-evidence"),
        Path(sys.executable).with_name("agent-evidence.exe"),
        Path(sys.executable).resolve().with_name("agent-evidence"),
        Path(sys.executable).resolve().with_name("agent-evidence.exe"),
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate

    resolved = shutil.which("agent-evidence")
    if resolved is None:
        raise AssertionError(
            "agent-evidence CLI was not found in the active test environment. "
            "This smoke test assumes the quickstart install step is already satisfied."
        )
    return Path(resolved)


def test_quickstart_langchain_minimal_path_smoke(tmp_path: Path) -> None:
    repo_root = _repo_root()
    output_dir = tmp_path / "quickstart-output"
    example_path = repo_root / "examples" / "langchain_minimal_evidence.py"
    cli_path = _agent_evidence_cli()

    example_result = subprocess.run(
        [sys.executable, str(example_path), "--output-dir", str(output_dir)],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=False,
    )
    assert example_result.returncode == 0, example_result.stderr

    example_payload = json.loads(example_result.stdout)
    assert example_payload["ok"] is True

    bundle_path = output_dir / "langchain-evidence.bundle.json"
    public_key_path = output_dir / "manifest-public.pem"
    receipt_path = output_dir / "receipt.json"
    summary_path = output_dir / "summary.json"

    assert bundle_path.exists()
    assert public_key_path.exists()

    with receipt_path.open("w", encoding="utf-8") as receipt_file:
        verify_result = subprocess.run(
            [
                str(cli_path),
                "verify-export",
                "--bundle",
                str(bundle_path),
                "--public-key",
                str(public_key_path),
            ],
            cwd=repo_root,
            stdout=receipt_file,
            stderr=subprocess.PIPE,
            text=True,
            check=False,
        )
    assert verify_result.returncode == 0, verify_result.stderr

    receipt_payload = json.loads(receipt_path.read_text(encoding="utf-8"))
    assert receipt_payload["ok"] is True

    assert summary_path.exists()
    summary_payload = json.loads(summary_path.read_text(encoding="utf-8"))
    assert summary_payload["ok"] is True
