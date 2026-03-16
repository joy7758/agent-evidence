#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

from agent_evidence.aep import verify_bundle

ROOT = Path(__file__).resolve().parents[1]
FIXTURES_ROOT = ROOT / "tests" / "fixtures" / "agent_evidence_profile"


def main() -> int:
    scenarios = [
        ("valid", FIXTURES_ROOT / "valid" / "basic-bundle", True),
        ("invalid", FIXTURES_ROOT / "invalid" / "tampered-bundle", False),
    ]
    summary = []
    exit_code = 0

    for name, bundle_dir, expected_ok in scenarios:
        result = verify_bundle(bundle_dir)
        actual_ok = result["ok"]
        summary.append(
            {
                "scenario": name,
                "bundle_dir": str(bundle_dir),
                "expected_ok": expected_ok,
                "actual_ok": actual_ok,
                "stages": result["stages"],
            }
        )
        if actual_ok != expected_ok:
            exit_code = 1

    print(json.dumps({"ok": exit_code == 0, "results": summary}, indent=2, sort_keys=True))
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
