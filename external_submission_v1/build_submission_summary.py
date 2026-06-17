#!/usr/bin/env python3
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent
GATES = [
    "PLACEHOLDER_SCAN.py",
    "CLAIM_BOUNDARY_SCAN.py",
    "PATH_REFERENCE_SCAN.py",
    "RELEASE_READINESS_SUMMARY.py",
]


def main():
    print("Origin External Submission Execution Kit v1.0")
    print(f"root={ROOT}")
    print("publishes_external_artifacts=false")
    print("decision=PENDING_HUMAN_APPROVAL")
    for d in sorted(p for p in ROOT.iterdir() if p.is_dir()):
        print(f"artifact_count {d.name}={sum(1 for x in d.rglob('*') if x.is_file())}")
    code = 0
    for gate in GATES:
        r = subprocess.run(
            [sys.executable, str(ROOT / "publish_gate" / gate)],
            cwd=REPO,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=False,
        )
        print(f"gate={gate} status={'PASS' if r.returncode == 0 else 'FAIL'}")
        print(r.stdout.strip())
        code = max(code, r.returncode)
    print("warning: this script does not publish, submit, post, email, or request endorsement.")
    return code


if __name__ == "__main__":
    raise SystemExit(main())
