from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
CHECKER = REPO_ROOT / "scripts" / "check_delivery_surface.py"
SURFACE = REPO_ROOT / "packaging" / "commercial-delivery-surface.json"


def run_checker(*args: str) -> tuple[int, dict[str, object]]:
    completed = subprocess.run(
        [sys.executable, str(CHECKER), *args],
        cwd=REPO_ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    assert completed.stdout, completed.stderr
    return completed.returncode, json.loads(completed.stdout)


def copy_surface(tmp_path: Path) -> Path:
    target = tmp_path / "commercial-delivery-surface.json"
    target.write_text(SURFACE.read_text(encoding="utf-8"), encoding="utf-8")
    return target


def test_current_delivery_surface_passes() -> None:
    exit_code, output = run_checker()

    assert exit_code == 0
    assert output["ok"] is True
    assert output["status"] == "surface_ok"
    assert output["included_count"] > 0


def test_missing_include_path_fails_with_expected_code(tmp_path: Path) -> None:
    surface = copy_surface(tmp_path)
    payload = json.loads(surface.read_text(encoding="utf-8"))
    payload["included_paths"].append("missing/file.txt")
    surface.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")

    exit_code, output = run_checker("--surface", str(surface), "--root", str(REPO_ROOT))

    assert exit_code == 1
    assert output["ok"] is False
    assert output["error_code"] == "missing_delivery_surface_path"
    assert output["missing"] == ["missing/file.txt"]


def test_forbidden_include_path_fails_with_expected_code(tmp_path: Path) -> None:
    surface = copy_surface(tmp_path)
    payload = json.loads(surface.read_text(encoding="utf-8"))
    payload["included_paths"].append("paper/foo.md")
    surface.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")

    exit_code, output = run_checker("--surface", str(surface), "--root", str(REPO_ROOT))

    assert exit_code == 1
    assert output["ok"] is False
    assert output["error_code"] == "forbidden_delivery_surface_path"
    assert output["forbidden"] == ["paper/foo.md"]


def test_checker_output_is_parseable_json() -> None:
    exit_code, output = run_checker()

    assert exit_code == 0
    assert isinstance(output, dict)
    assert "checked_surface" in output


def test_checker_requires_no_network_imports() -> None:
    source = CHECKER.read_text(encoding="utf-8")

    assert "requests" not in source
    assert "urllib" not in source
    assert "http.client" not in source
    assert "socket" not in source
