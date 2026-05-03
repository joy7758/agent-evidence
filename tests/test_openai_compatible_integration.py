from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_openai_compatible_minimal_evidence_subprocess_and_cli_verify(
    tmp_path: Path,
) -> None:
    output_dir = tmp_path / "openai-compatible-minimal-evidence"
    env = os.environ.copy()
    for name in [
        "ANTHROPIC_API_KEY",
        "GOOGLE_API_KEY",
        "LANGCHAIN_API_KEY",
        "MISTRAL_API_KEY",
        "OPENAI_API_KEY",
        "OPENAI_COMPATIBLE_API_KEY",
        "OPENAI_COMPATIBLE_BASE_URL",
        "OPENAI_COMPATIBLE_MODEL",
        "ZHIPUAI_API_KEY",
        "ZHIPU_API_KEY",
    ]:
        env.pop(name, None)

    result = subprocess.run(
        [
            sys.executable,
            "examples/openai_compatible_minimal_evidence.py",
            "--output-dir",
            str(output_dir),
            "--mock",
        ],
        cwd=ROOT,
        env=env,
        check=True,
        capture_output=True,
        text=True,
    )
    payload = json.loads(result.stdout)
    assert payload["ok"] is True
    assert payload["mode"] == "mock"
    assert payload["provider_config"]["api_key_configured"] is False

    expected_files = [
        "runtime-events.jsonl",
        "openai-compatible-evidence.bundle.json",
        "openai-compatible-evidence.manifest.json",
        "manifest-private.pem",
        "manifest-public.pem",
        "summary.json",
    ]
    for filename in expected_files:
        assert (output_dir / filename).exists(), filename

    summary = json.loads((output_dir / "summary.json").read_text(encoding="utf-8"))
    bundle_path = output_dir / "openai-compatible-evidence.bundle.json"
    public_key_path = output_dir / "manifest-public.pem"
    bundle = json.loads(bundle_path.read_text(encoding="utf-8"))
    assert bundle["manifest"]["filters"]["source"] == "openai_compatible"
    assert all(
        record["event"]["context"]["source"] == "openai_compatible" for record in bundle["records"]
    )

    agent_evidence_cli = Path(sys.executable).with_name("agent-evidence")
    assert agent_evidence_cli.exists()
    verify_result = subprocess.run(
        [
            str(agent_evidence_cli),
            "verify-export",
            "--bundle",
            str(bundle_path),
            "--public-key",
            str(public_key_path),
        ],
        cwd=ROOT,
        env=env,
        check=True,
        capture_output=True,
        text=True,
    )
    verify_payload = json.loads(verify_result.stdout)
    assert verify_payload["ok"] is True
    assert summary["verify_result"]["ok"] is True
    assert summary["verify_command"].startswith("agent-evidence verify-export")


def test_openai_compatible_minimal_cookbook_references_runnable_path() -> None:
    text = (ROOT / "docs/cookbooks/openai_compatible_minimal_evidence.md").read_text(
        encoding="utf-8"
    )

    for required in [
        "examples/openai_compatible_minimal_evidence.py",
        "agent-evidence verify-export",
        "summary.json",
        "runtime-events.jsonl",
        "openai-compatible-evidence.bundle.json",
        "OPENAI_COMPATIBLE_API_KEY",
        "OPENAI_COMPATIBLE_BASE_URL",
        "OPENAI_COMPATIBLE_MODEL",
    ]:
        assert required in text


def test_openai_compatible_live_mode_requires_explicit_provider_config(
    tmp_path: Path,
) -> None:
    env = os.environ.copy()
    for name in [
        "OPENAI_API_KEY",
        "OPENAI_COMPATIBLE_API_KEY",
        "OPENAI_COMPATIBLE_BASE_URL",
        "OPENAI_COMPATIBLE_MODEL",
        "ZHIPUAI_API_KEY",
        "ZHIPU_API_KEY",
    ]:
        env.pop(name, None)

    result = subprocess.run(
        [
            sys.executable,
            "examples/openai_compatible_minimal_evidence.py",
            "--output-dir",
            str(tmp_path / "openai-compatible-minimal-evidence"),
            "--live",
        ],
        cwd=ROOT,
        env=env,
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 2
    payload = json.loads(result.stdout)
    assert payload["ok"] is False
    assert payload["error"]["code"] == "invalid_provider_config"
