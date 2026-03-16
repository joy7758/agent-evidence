#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

from agent_evidence.aep import verify_bundle

ROOT = Path(__file__).resolve().parents[1]
FIXTURES_ROOT = ROOT / "tests" / "fixtures" / "agent_evidence_profile"


def _read_manifest(bundle_dir: Path) -> dict[str, object]:
    return json.loads((bundle_dir / "manifest.json").read_text(encoding="utf-8"))


def main() -> int:
    scenarios = [
        ("valid", FIXTURES_ROOT / "valid" / "live-automaton-bundle", True),
        ("invalid", FIXTURES_ROOT / "invalid" / "live-automaton-tampered-bundle", False),
        (
            "valid-runtime-root",
            FIXTURES_ROOT / "valid" / "live-automaton-runtime-root-bundle",
            True,
        ),
        (
            "invalid-runtime-root",
            FIXTURES_ROOT / "invalid" / "live-automaton-runtime-root-tampered-bundle",
            False,
        ),
    ]
    results: list[dict[str, object]] = []
    exit_code = 0

    for scenario, bundle_dir, expected_ok in scenarios:
        verify_result = verify_bundle(bundle_dir)
        manifest = _read_manifest(bundle_dir)
        actual_ok = verify_result["ok"]
        results.append(
            {
                "scenario": scenario,
                "bundle_dir": str(bundle_dir),
                "expected_ok": expected_ok,
                "actual_ok": actual_ok,
                "runtime": {
                    "version": manifest.get("source_runtime_version"),
                    "commit": manifest.get("source_runtime_commit"),
                    "dirty": manifest.get("source_runtime_dirty"),
                },
                "stages": verify_result["stages"],
            }
        )
        if actual_ok != expected_ok:
            exit_code = 1

    print(json.dumps({"ok": exit_code == 0, "results": results}, indent=2, sort_keys=True))
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
