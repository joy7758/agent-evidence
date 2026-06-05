from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]

SECRET_SENTINELS = [
    "sk-test-secret-do-not-leak-P11",
    "sk-test-openai-env-do-not-leak-P11",
    "Bearer p11-authorization-do-not-leak",
]


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


def test_openai_compatible_mock_mode_does_not_construct_live_client(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    module = _load_openai_compatible_example()

    def fail_live_call(**_kwargs: object) -> dict:
        raise AssertionError("mock mode must not construct or call a live provider client")

    monkeypatch.setattr(module, "_live_chat_completion", fail_live_call)

    summary = module.run_example(
        tmp_path / "openai-compatible-minimal-evidence",
        mode="mock",
        api_key="sk-test-secret-do-not-leak-P11",
        base_url="https://example.invalid/v1",
        model="mock-compatible-model",
    )

    assert summary["ok"] is True
    assert summary["mode"] == "mock"
    assert summary["provider_config"]["api_key_configured"] is True


def test_openai_compatible_mock_mode_does_not_serialize_provider_secrets(
    tmp_path: Path,
) -> None:
    output_dir = tmp_path / "openai-compatible-minimal-evidence"
    env = os.environ.copy()
    env.update(
        {
            "OPENAI_COMPATIBLE_API_KEY": SECRET_SENTINELS[0],
            "OPENAI_API_KEY": SECRET_SENTINELS[1],
            "AUTHORIZATION": SECRET_SENTINELS[2],
        }
    )

    subprocess.run(
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

    artifact_paths = [
        output_dir / "runtime-events.jsonl",
        output_dir / "openai-compatible-evidence.bundle.json",
        output_dir / "openai-compatible-evidence.manifest.json",
        output_dir / "manifest-private.pem",
        output_dir / "manifest-public.pem",
        output_dir / "summary.json",
    ]
    for path in artifact_paths:
        assert path.exists(), path
        content = path.read_text(encoding="utf-8", errors="replace")
        for sentinel in SECRET_SENTINELS:
            assert sentinel not in content, f"{sentinel!r} leaked into {path.name}"
        assert "Authorization" not in content


@pytest.mark.parametrize(
    ("api_key", "base_url", "model", "missing_label"),
    [
        (None, "https://example.invalid/v1", "demo-model", "API_KEY"),
        ("sk-test-secret-do-not-leak-P11", None, "demo-model", "BASE_URL"),
        ("sk-test-secret-do-not-leak-P11", "https://example.invalid/v1", None, "MODEL"),
    ],
)
def test_openai_compatible_live_mode_reports_each_missing_config_without_secret_leak(
    tmp_path: Path,
    api_key: str | None,
    base_url: str | None,
    model: str | None,
    missing_label: str,
) -> None:
    args = [
        sys.executable,
        "examples/openai_compatible_minimal_evidence.py",
        "--output-dir",
        str(tmp_path / "openai-compatible-minimal-evidence"),
        "--live",
    ]
    if api_key is not None:
        args.extend(["--api-key", api_key])
    if base_url is not None:
        args.extend(["--base-url", base_url])
    if model is not None:
        args.extend(["--model", model])

    result = subprocess.run(
        args,
        cwd=ROOT,
        env=_without_provider_env(),
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 2
    payload = json.loads(result.stdout)
    assert payload["ok"] is False
    assert payload["error"]["code"] == "invalid_provider_config"
    assert missing_label in payload["error"]["message"]
    for sentinel in SECRET_SENTINELS:
        assert sentinel not in result.stdout


def _load_openai_compatible_example():
    import importlib.util

    example_path = ROOT / "examples" / "openai_compatible_minimal_evidence.py"
    spec = importlib.util.spec_from_file_location(
        "openai_compatible_minimal_evidence_example",
        example_path,
    )
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def _without_provider_env() -> dict[str, str]:
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
    return env
