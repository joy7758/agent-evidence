import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CASE_DIR = ROOT / "examples" / "paper_case"


def load_json(name: str) -> dict:
    return json.loads((CASE_DIR / name).read_text(encoding="utf-8"))


def test_paper_case_files_exist() -> None:
    expected = {
        "fdo-dataset.json",
        "policy-aggregate-only.json",
        "agent-operation.json",
        "evidence-valid.json",
        "evidence-invalid-tampered-output.json",
        "expected-validator-pass.json",
        "expected-validator-fail.json",
    }

    assert expected <= {path.name for path in CASE_DIR.iterdir()}


def test_paper_case_output_hash_binding() -> None:
    operation = load_json("agent-operation.json")
    valid = load_json("evidence-valid.json")
    tampered = load_json("evidence-invalid-tampered-output.json")

    expected_hash = operation["output_object"]["content_hash"]
    valid_output_hash = next(
        ref["digest"] for ref in valid["evidence"]["references"] if ref["role"] == "output"
    )
    tampered_output_hash = next(
        ref["digest"] for ref in tampered["evidence"]["references"] if ref["role"] == "output"
    )

    assert valid_output_hash == expected_hash
    assert tampered_output_hash != expected_hash


def test_paper_demo_script_reports_expected_pass_and_fail() -> None:
    result = subprocess.run(
        [str(ROOT / "scripts" / "reproduce_paper_demo.sh")],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, result.stdout + result.stderr
    assert "PASS valid evidence bundle\n" in result.stdout
    assert "FAIL tampered output hash mismatch\n" in result.stdout
