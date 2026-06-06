from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
CHECKER = REPO_ROOT / "scripts" / "check_protocol_citations.py"


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


def copy_clause_index(tmp_path: Path) -> Path:
    target = tmp_path / "clause-index.json"
    target.write_text(
        (REPO_ROOT / "protocol" / "clause-index.json").read_text(encoding="utf-8"),
        encoding="utf-8",
    )
    return target


def test_default_checker_succeeds_on_repository_files() -> None:
    exit_code, output = run_checker()

    assert exit_code == 0
    assert output["ok"] is True
    assert output["clause_count"] == 5
    assert output["clause_ids"] == [
        "EEOAP-001",
        "EEOAP-002",
        "EEOAP-003",
        "EEOAP-004",
        "EEOAP-005",
    ]
    assert output["checked_related_files"] is True


def test_alternate_clause_index_path_succeeds(tmp_path: Path) -> None:
    clause_index = copy_clause_index(tmp_path)

    exit_code, output = run_checker(
        "--manifest",
        "protocol/manifest.json",
        "--clause-index",
        str(clause_index),
        "--clauses-md",
        "docs/protocol/clauses.md",
        "--pr-template",
        ".github/pull_request_template.md",
        "--root",
        str(REPO_ROOT),
    )

    assert exit_code == 0
    assert output["ok"] is True
    assert output["checked_related_files"] is True


def test_alternate_clause_index_with_bad_clause_id_fails(tmp_path: Path) -> None:
    clause_index = copy_clause_index(tmp_path)
    payload = json.loads(clause_index.read_text(encoding="utf-8"))
    payload["clauses"][0]["clause_id"] = "BAD-001"
    clause_index.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    exit_code, output = run_checker(
        "--manifest",
        "protocol/manifest.json",
        "--clause-index",
        str(clause_index),
        "--clauses-md",
        "docs/protocol/clauses.md",
        "--pr-template",
        ".github/pull_request_template.md",
        "--root",
        str(REPO_ROOT),
    )

    assert exit_code == 1
    assert output["ok"] is False
    assert "invalid_clause_id_format:BAD-001" in output["errors"]


def test_alternate_clause_index_with_missing_related_file_fails(
    tmp_path: Path,
) -> None:
    clause_index = copy_clause_index(tmp_path)
    payload = json.loads(clause_index.read_text(encoding="utf-8"))
    payload["clauses"][0]["related_files"].append("missing/file.json")
    clause_index.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    exit_code, output = run_checker(
        "--manifest",
        "protocol/manifest.json",
        "--clause-index",
        str(clause_index),
        "--clauses-md",
        "docs/protocol/clauses.md",
        "--pr-template",
        ".github/pull_request_template.md",
        "--root",
        str(REPO_ROOT),
    )

    assert exit_code == 1
    assert output["ok"] is False
    assert output["error_code"] == "missing_related_file"
    assert {
        "clause_id": "EEOAP-001",
        "path": "missing/file.json",
    } in output["missing_related_files"]


def test_current_protocol_related_files_exist() -> None:
    exit_code, output = run_checker(
        "--manifest",
        "protocol/manifest.json",
        "--clause-index",
        "protocol/clause-index.json",
        "--clauses-md",
        "docs/protocol/clauses.md",
        "--pr-template",
        ".github/pull_request_template.md",
        "--root",
        str(REPO_ROOT),
    )

    assert exit_code == 0
    assert output["ok"] is True
    assert output["checked_related_files"] is True
    assert "missing_related_files" not in output
