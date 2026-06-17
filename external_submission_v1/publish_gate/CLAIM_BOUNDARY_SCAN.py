#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SEARCH = (ROOT / "external_submission_v1", ROOT / "spec_release_v0_1")
PHRASES = (
    "certified" + " by",
    "endorsed" + " by",
    "approved" + " by",
    "accepted" + " by arxiv",
    "published" + " by arxiv",
    "peer" + "-reviewed",
    "production" + "-ready",
    "production" + " ready",
    "legally" + " compliant",
    "official origin integration",
    "official cursor integration",
    "official graphite integration",
    "official mcp integration",
    "secure" + " by default",
)
NEG = ("not ", "no ", "does not ", "do not ", "cannot ", "without ", "non-claim", "must not ")


def main():
    files = []
    for r in SEARCH:
        if r.exists():
            files += [
                p
                for p in r.rglob("*")
                if p.is_file()
                and p.suffix.lower() in {".md", ".json", ".py", ".sh"}
                and p.name != "CLAIM_BOUNDARY_SCAN.py"
            ]
    findings = []
    for p in sorted(files):
        for n, line in enumerate(p.read_text(encoding="utf-8").splitlines(), 1):
            low = line.lower()
            for ph in PHRASES:
                i = low.find(ph)
                win = low[max(0, i - 80) : i + 80] if i >= 0 else ""
                if i >= 0 and not any(x in win for x in NEG):
                    findings.append(f"{p.relative_to(ROOT)}:{n}: unsupported claim phrase {ph!r}")
    if findings:
        print("claim_boundary_scan=FAIL")
        print("\n".join(findings))
        return 1
    print("claim_boundary_scan=PASS")
    print(f"scanned_files={len(files)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
