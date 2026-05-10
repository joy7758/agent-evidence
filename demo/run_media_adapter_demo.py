from __future__ import annotations

import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from agent_evidence.media_adapter_evaluation import create_adapter_backed_statement  # noqa: E402

OUTPUT_DIR = ROOT / "demo" / "output" / "media_adapter_demo"


def main() -> int:
    if OUTPUT_DIR.exists():
        shutil.rmtree(OUTPUT_DIR)
    report = create_adapter_backed_statement(OUTPUT_DIR, repo_root=ROOT)
    if report["ok"]:
        print("PASS aep-media-adapters@0.1 demo")
        return 0
    print("FAIL aep-media-adapters@0.1 demo")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
