from __future__ import annotations

import shutil
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))


def main() -> int:
    from agent_evidence.media_submission_pack import build_aep_media_submission_pack

    out_dir = REPO_ROOT / "demo" / "output" / "aep_media_submission_pack"
    if out_dir.exists():
        shutil.rmtree(out_dir)
    report = build_aep_media_submission_pack(out_dir, repo_root=REPO_ROOT)
    if report["ok"]:
        print("PASS aep-media-submission-pack@0.1 demo")
        return 0
    print(report["summary"])
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
