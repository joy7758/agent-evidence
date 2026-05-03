from __future__ import annotations

import importlib.util
import json
import socket
import sys
from pathlib import Path
from types import ModuleType

import pytest
from click.testing import CliRunner

from agent_evidence.cli.main import main
from agent_evidence.review_pack import (
    ALLOWED_FINDING_SEVERITIES,
    ReviewPackError,
    ReviewPackVerificationError,
    create_review_pack,
)

ROOT = Path(__file__).resolve().parents[1]

SECRET_SENTINELS = [
    "pypi-test-secret-do-not-leak-review-pack",
    "sk-review-pack-openai-compatible-do-not-leak",
    "Bearer review-pack-authorization-do-not-leak",
]

BOUNDARY_PHRASES = [
    "not legal non-repudiation",
    "not compliance certification",
    "not AI Act approval",
    "not full AI governance assessment",
]


def _load_example(module_name: str, relative_path: str) -> ModuleType:
    example_path = ROOT / relative_path
    spec = importlib.util.spec_from_file_location(module_name, example_path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def _load_langchain_example() -> ModuleType:
    return _load_example(
        "review_pack_langchain_minimal_evidence",
        "examples/langchain_minimal_evidence.py",
    )


def _load_openai_compatible_example() -> ModuleType:
    return _load_example(
        "review_pack_openai_compatible_minimal_evidence",
        "examples/openai_compatible_minimal_evidence.py",
    )


def _assert_review_pack_layout(pack_dir: Path, *, includes_summary: bool = True) -> None:
    expected_files = [
        "manifest.json",
        "receipt.json",
        "findings.json",
        "summary.md",
        "artifacts/evidence.bundle.json",
        "artifacts/manifest-public.pem",
    ]
    if includes_summary:
        expected_files.append("artifacts/summary.json")
    for relative_path in expected_files:
        assert (pack_dir / relative_path).exists(), relative_path

    receipt = json.loads((pack_dir / "receipt.json").read_text(encoding="utf-8"))
    findings = json.loads((pack_dir / "findings.json").read_text(encoding="utf-8"))
    manifest = json.loads((pack_dir / "manifest.json").read_text(encoding="utf-8"))
    summary = (pack_dir / "summary.md").read_text(encoding="utf-8")

    assert receipt["ok"] is True
    assert receipt["verification"]["ok"] is True
    assert findings["ok"] is True
    assert {finding["severity"] for finding in findings["findings"]} <= ALLOWED_FINDING_SEVERITIES
    assert manifest["review_pack_version"] == "0.1"
    for phrase in BOUNDARY_PHRASES:
        assert phrase in summary
        assert phrase in " ".join(manifest["boundaries"])


def _scan_text_files(root: Path) -> str:
    chunks: list[str] = []
    for path in sorted(item for item in root.rglob("*") if item.is_file()):
        chunks.append(path.read_text(encoding="utf-8", errors="replace"))
    return "\n".join(chunks)


def test_review_pack_create_from_langchain_minimal_example(tmp_path: Path) -> None:
    module = _load_langchain_example()
    source_dir = tmp_path / "langchain-minimal-evidence"
    source_summary = module.run_example(source_dir)

    pack_dir = tmp_path / "langchain-review-pack"
    result = create_review_pack(
        bundle_path=source_summary["bundle_path"],
        public_key_path=source_summary["public_key_path"],
        summary_path=source_dir / "summary.json",
        output_dir=pack_dir,
    )

    assert result["ok"] is True
    _assert_review_pack_layout(pack_dir)


def test_review_pack_create_from_openai_compatible_mock_example(tmp_path: Path) -> None:
    module = _load_openai_compatible_example()
    source_dir = tmp_path / "openai-compatible-minimal-evidence"
    source_summary = module.run_example(source_dir, mode="mock")

    pack_dir = tmp_path / "openai-compatible-review-pack"
    result = create_review_pack(
        bundle_path=source_summary["bundle_path"],
        public_key_path=source_summary["public_key_path"],
        summary_path=source_dir / "summary.json",
        output_dir=pack_dir,
    )

    assert result["ok"] is True
    _assert_review_pack_layout(pack_dir)


def test_review_pack_fails_closed_for_bad_public_key(tmp_path: Path) -> None:
    module = _load_langchain_example()
    source_dir = tmp_path / "langchain-minimal-evidence"
    source_summary = module.run_example(source_dir)
    bad_key = tmp_path / "bad-public.pem"
    bad_key.write_text("not a public key\n", encoding="utf-8")
    pack_dir = tmp_path / "bad-review-pack"

    with pytest.raises(ReviewPackVerificationError):
        create_review_pack(
            bundle_path=source_summary["bundle_path"],
            public_key_path=bad_key,
            summary_path=source_dir / "summary.json",
            output_dir=pack_dir,
        )

    assert not pack_dir.exists()
    assert not (pack_dir / "summary.md").exists()


def test_review_pack_does_not_copy_private_key(tmp_path: Path) -> None:
    module = _load_langchain_example()
    source_dir = tmp_path / "langchain-minimal-evidence"
    source_summary = module.run_example(source_dir)
    assert (source_dir / "manifest-private.pem").exists()

    pack_dir = tmp_path / "langchain-review-pack"
    create_review_pack(
        bundle_path=source_summary["bundle_path"],
        public_key_path=source_summary["public_key_path"],
        summary_path=source_dir / "summary.json",
        output_dir=pack_dir,
    )

    copied_names = {path.name for path in (pack_dir / "artifacts").iterdir()}
    assert "manifest-private.pem" not in copied_names
    assert all("private" not in name for name in copied_names)


def test_review_pack_does_not_serialize_secret_sentinels(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    module = _load_openai_compatible_example()
    monkeypatch.setenv("OPENAI_COMPATIBLE_API_KEY", SECRET_SENTINELS[1])
    monkeypatch.setenv("AUTHORIZATION", SECRET_SENTINELS[2])
    source_dir = tmp_path / "openai-compatible-minimal-evidence"
    source_summary = module.run_example(
        source_dir,
        mode="mock",
        api_key=SECRET_SENTINELS[1],
        base_url="mock://openai-compatible/v1",
        model="mock-compatible-model",
    )

    pack_dir = tmp_path / "openai-compatible-review-pack"
    create_review_pack(
        bundle_path=source_summary["bundle_path"],
        public_key_path=source_summary["public_key_path"],
        summary_path=source_dir / "summary.json",
        output_dir=pack_dir,
    )

    content = _scan_text_files(pack_dir)
    for sentinel in SECRET_SENTINELS:
        assert sentinel not in content
    assert "Authorization" not in content


def test_review_pack_fails_closed_when_optional_summary_contains_secret_like_content(
    tmp_path: Path,
) -> None:
    module = _load_langchain_example()
    source_dir = tmp_path / "langchain-minimal-evidence"
    source_summary = module.run_example(source_dir)
    unsafe_summary = tmp_path / "unsafe-summary.json"
    unsafe_summary.write_text(
        json.dumps({"token": SECRET_SENTINELS[0], "header": SECRET_SENTINELS[2]}),
        encoding="utf-8",
    )
    pack_dir = tmp_path / "unsafe-review-pack"

    with pytest.raises(ReviewPackError):
        create_review_pack(
            bundle_path=source_summary["bundle_path"],
            public_key_path=source_summary["public_key_path"],
            summary_path=unsafe_summary,
            output_dir=pack_dir,
        )

    assert not pack_dir.exists()


def test_review_pack_creation_makes_no_network_calls(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    module = _load_langchain_example()
    source_dir = tmp_path / "langchain-minimal-evidence"
    source_summary = module.run_example(source_dir)

    def fail_socket(*_args: object, **_kwargs: object) -> socket.socket:
        raise AssertionError("Review Pack creation must not open network sockets")

    monkeypatch.setattr(socket, "socket", fail_socket)

    pack_dir = tmp_path / "langchain-review-pack"
    create_review_pack(
        bundle_path=source_summary["bundle_path"],
        public_key_path=source_summary["public_key_path"],
        summary_path=source_dir / "summary.json",
        output_dir=pack_dir,
    )

    _assert_review_pack_layout(pack_dir)


def test_review_pack_cli_create_smoke(tmp_path: Path) -> None:
    module = _load_langchain_example()
    source_dir = tmp_path / "langchain-minimal-evidence"
    source_summary = module.run_example(source_dir)
    pack_dir = tmp_path / "langchain-review-pack"

    result = CliRunner().invoke(
        main,
        [
            "review-pack",
            "create",
            "--bundle",
            str(source_summary["bundle_path"]),
            "--public-key",
            str(source_summary["public_key_path"]),
            "--summary",
            str(source_dir / "summary.json"),
            "--output-dir",
            str(pack_dir),
        ],
    )

    assert result.exit_code == 0, result.output
    payload = json.loads(result.output)
    assert payload["ok"] is True
    _assert_review_pack_layout(pack_dir)


def test_review_pack_cli_fails_closed_for_invalid_signature(tmp_path: Path) -> None:
    module = _load_langchain_example()
    source_dir = tmp_path / "langchain-minimal-evidence"
    source_summary = module.run_example(source_dir)
    bad_key = tmp_path / "bad-public.pem"
    bad_key.write_text("not a public key\n", encoding="utf-8")
    pack_dir = tmp_path / "bad-review-pack"

    result = CliRunner().invoke(
        main,
        [
            "review-pack",
            "create",
            "--bundle",
            str(source_summary["bundle_path"]),
            "--public-key",
            str(bad_key),
            "--summary",
            str(source_dir / "summary.json"),
            "--output-dir",
            str(pack_dir),
        ],
    )

    assert result.exit_code != 0
    assert "Bundle verification failed" in result.output
    assert not pack_dir.exists()
