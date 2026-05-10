from __future__ import annotations

import shutil
from pathlib import Path

from agent_evidence.media_final_journal_revision_pack import build_aep_media_high_revision_pack


def main() -> int:
    out_dir = Path("demo/output/aep_media_high_revision_pack")
    if out_dir.exists():
        shutil.rmtree(out_dir)
    report = build_aep_media_high_revision_pack(out_dir)
    print(f"{report['summary']} demo")
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
