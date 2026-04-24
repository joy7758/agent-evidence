#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
from pathlib import Path
from typing import Any


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, obj: Any) -> None:
    path.write_text(
        json.dumps(obj, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
        encoding="utf-8",
    )


def default_config_path() -> Path:
    return Path(__file__).resolve().parents[1] / "repo_validator_config.json"


def token_map(pack: Path) -> dict[str, str]:
    compat_dir = pack / "repo_compat"
    return {
        "{pack}": str(pack),
        "{manifest}": str(pack / "manifest.json"),
        "{bundle}": str(pack / "bundle.json"),
        "{receipt}": str(pack / "receipt.json"),
        "{summary}": str(pack / "summary.json"),
        "{compat_dir}": str(compat_dir),
        "{compat_statement}": str(compat_dir / "operation_accountability_statement.json"),
        "{compat_bundle_view}": str(compat_dir / "ncs_bundle_view.json"),
        "{artifact_index}": str(compat_dir / "artifact_index.json"),
    }


def resolve_argv(argv: list[str], replacements: dict[str, str]) -> list[str]:
    resolved: list[str] = []
    for value in argv:
        for token, replacement in replacements.items():
            value = value.replace(token, replacement)
        resolved.append(value)
    return resolved


def resolve_command(argv: list[str]) -> list[str]:
    if not argv:
        return argv
    if argv[0] != "agent-evidence":
        return argv
    if shutil.which("agent-evidence"):
        return argv
    repo_bin = Path(__file__).resolve().parents[2] / ".venv" / "bin" / "agent-evidence"
    if repo_bin.exists():
        return [str(repo_bin), *argv[1:]]
    return argv


def run_command(record: dict[str, Any], replacements: dict[str, str]) -> dict[str, Any]:
    argv = resolve_command(
        resolve_argv([str(item) for item in record.get("argv", [])], replacements)
    )
    result: dict[str, Any] = {
        "name": record.get("name"),
        "role": record.get("role"),
        "argv": argv,
        "expected_exit_code": record.get("expected_exit_code"),
        "configured_status": record.get("status"),
        "notes": record.get("notes"),
    }
    try:
        completed = subprocess.run(
            argv,
            check=False,
            text=True,
            capture_output=True,
        )
        result.update(
            {
                "exit_code": completed.returncode,
                "stdout": completed.stdout[:4000],
                "stderr": completed.stderr[:4000],
                "status": "passed"
                if completed.returncode == record.get("expected_exit_code", 0)
                else "failed",
            }
        )
    except FileNotFoundError as exc:
        result.update(
            {
                "exit_code": 127,
                "stdout": "",
                "stderr": str(exc)[:4000],
                "status": "failed",
            }
        )
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description="Run configured repository validators.")
    parser.add_argument("--pack", required=True, type=Path)
    parser.add_argument("--config", type=Path)
    parser.add_argument("--require-repo", action="store_true")
    args = parser.parse_args()

    config_path = args.config or default_config_path()
    config = load_json(config_path)
    mode = config.get("mode", "none")
    reason = config.get("reason", "")
    results_path = args.pack / "repo_validator_results.json"

    if mode == "none":
        payload = {
            "mode": mode,
            "reason": reason,
            "overall_status": "none",
            "results": [],
        }
        write_json(results_path, payload)
        print(f"REPO_VALIDATOR: NONE: {reason}")
        return 3 if args.require_repo else 0

    replacements = token_map(args.pack)
    results = [run_command(record, replacements) for record in config.get("commands", [])]
    for result in results:
        print(
            "REPO_VALIDATOR COMMAND "
            f"{result.get('name')}: exit {result.get('exit_code')} "
            f"{result.get('status')}"
        )

    failed = [result for result in results if result.get("status") != "passed"]
    if mode == "strict" and failed:
        overall = "fail"
        exit_code = 3
        print("REPO_VALIDATOR: FAIL")
    elif mode == "strict":
        overall = "pass"
        exit_code = 0
        print("REPO_VALIDATOR: PASS")
    elif mode == "advisory":
        overall = "advisory_failed" if failed else "advisory_passed"
        exit_code = 0
        print("REPO_VALIDATOR: ADVISORY")
    else:
        overall = "none"
        exit_code = 3 if args.require_repo else 0
        print(f"REPO_VALIDATOR: NONE: unsupported mode {mode}")

    payload = {
        "mode": mode,
        "reason": reason,
        "overall_status": overall,
        "results": results,
    }
    write_json(results_path, payload)
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
