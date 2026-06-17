#!/usr/bin/env python3
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
KIT = ROOT / "external_submission_v1"
REC = KIT / "publish_gate" / "RELEASE_DECISION_RECORD.md"
SCRIPTS = ["PLACEHOLDER_SCAN.py", "CLAIM_BOUNDARY_SCAN.py", "PATH_REFERENCE_SCAN.py"]


def main():
    print("release_readiness_summary")
    print("publishes_external_artifacts=false")
    code = 0
    for name in SCRIPTS:
        r = subprocess.run(
            [sys.executable, str(KIT / "publish_gate" / name)],
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=False,
        )
        print(f"gate={name} status={'PASS' if r.returncode == 0 else 'FAIL'}")
        print(r.stdout.strip())
        code = max(code, r.returncode)
    text = REC.read_text(encoding="utf-8")
    markers = [
        "decision: PENDING_HUMAN_APPROVAL",
        "- [ ] Human approval to perform external actions",
        "No external action has been performed",
    ]
    miss = [m for m in markers if m not in text]
    print(f"gate=RELEASE_DECISION_RECORD status={'PASS' if not miss else 'FAIL'}")
    for m in miss:
        print(f"missing marker: {m}")
    if miss:
        code = max(code, 1)
    else:
        print("decision_record=PENDING_HUMAN_APPROVAL")
        print("human_approval_checked=false")
    print(
        "release_readiness=READY_FOR_HUMAN_REVIEW"
        if code == 0
        else "release_readiness=BLOCKED_BY_LOCAL_GATE"
    )
    print("external_action_performed=false")
    return code


if __name__ == "__main__":
    raise SystemExit(main())
