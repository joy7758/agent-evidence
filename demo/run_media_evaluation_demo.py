#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

DEMO_ROOT = Path(__file__).resolve().parent
REPO_ROOT = DEMO_ROOT.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from agent_evidence.media_evaluation import EVALUATION_PROFILE, run_media_evaluation  # noqa: E402

OUTPUT_DIR = DEMO_ROOT / "output" / "media_evaluation_demo"


def main() -> int:
    summary = run_media_evaluation(OUTPUT_DIR, repo_root=REPO_ROOT)
    print(summary["summary"])
    if summary["ok"]:
        print(f"PASS {EVALUATION_PROFILE} demo")
        return 0
    print(f"FAIL {EVALUATION_PROFILE} demo")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
