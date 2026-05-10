from __future__ import annotations

import shutil
from pathlib import Path

from agent_evidence.media_ieee_word_pack import build_aep_media_ieee_word_pack


def main() -> int:
    repo_root = Path(__file__).resolve().parents[1]
    out_dir = repo_root / "demo" / "output" / "aep_media_ieee_word_pack"
    if out_dir.exists():
        shutil.rmtree(out_dir)
    report = build_aep_media_ieee_word_pack(out_dir, repo_root=repo_root)
    if report["ok"]:
        print("PASS aep-media-ieee-word-pack@0.1 demo")
        return 0
    print(report["summary"])
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
