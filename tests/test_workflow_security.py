from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from scripts.check_github_actions_pinned import unpinned_actions

ROOT = Path(__file__).resolve().parents[1]


def test_github_workflow_actions_are_pinned_to_full_sha() -> None:
    assert unpinned_actions(ROOT) == []


def test_github_actions_pin_checker_cli_passes() -> None:
    result = subprocess.run(
        [sys.executable, "scripts/check_github_actions_pinned.py"],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, result.stdout + result.stderr
