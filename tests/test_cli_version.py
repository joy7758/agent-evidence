from __future__ import annotations

from importlib import import_module
from importlib.metadata import PackageNotFoundError
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
cli_main = import_module("agent_evidence.cli.main")


def test_current_package_version_falls_back_to_pyproject(monkeypatch) -> None:
    def raise_not_found(package_name: str) -> str:
        raise PackageNotFoundError(package_name)

    monkeypatch.setattr(cli_main, "package_version", raise_not_found)

    assert cli_main.current_package_version() == "0.1.0rc3"


def test_cli_version_fallback_does_not_retain_stale_literal() -> None:
    cli_source = (ROOT / "agent_evidence/cli/main.py").read_text(encoding="utf-8")

    assert '"0.2.0"' not in cli_source
