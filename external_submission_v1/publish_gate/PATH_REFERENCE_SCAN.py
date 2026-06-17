#!/usr/bin/env python3
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
KIT = ROOT / "external_submission_v1"
INDEX = KIT / "final_index" / "ARTIFACT_INDEX.md"
ALLOW = {
    ".agent-evidence/runs/demo.json",
    "external_submission_v1/execution/PUBLIC_RELEASE_RESULT.md",
    "external_submission_v1/execution/private_outreach_recipients.json",
}
PATH_RE = re.compile(
    r"(?<![A-Za-z0-9_.-])((?:external_submission_v1|spec_release_v0_1|docs|agent_evidence|examples|demo|scripts|\.agent-evidence)/[A-Za-z0-9_./-]+)"
)


def clean(r):
    return r.rstrip(".,;:)\"'")


def files():
    return sorted(
        p
        for p in KIT.rglob("*")
        if p.is_file() and "__pycache__" not in p.parts and p.suffix != ".pyc"
    )


def main():
    findings = []
    for p in files():
        if p.suffix.lower() not in {".md", ".json", ".py", ".sh"}:
            continue
        for n, line in enumerate(p.read_text(encoding="utf-8").splitlines(), 1):
            for m in PATH_RE.finditer(line):
                ref = clean(m.group(1))
                if ref not in ALLOW and not (ROOT / ref).exists():
                    findings.append(f"{p.relative_to(ROOT)}:{n}: missing path reference {ref}")
    text = INDEX.read_text(encoding="utf-8") if INDEX.exists() else ""
    indexed = {
        clean(m.group(1))
        for m in PATH_RE.finditer(text)
        if m.group(1).startswith("external_submission_v1/")
    }
    actual = {str(p.relative_to(ROOT)) for p in files()}
    for ref in sorted(actual - indexed):
        findings.append(f"{INDEX.relative_to(ROOT)}: missing index entry {ref}")
    for ref in sorted(indexed - actual):
        findings.append(f"{INDEX.relative_to(ROOT)}: stale index entry {ref}")
    if findings:
        print("path_reference_scan=FAIL")
        print("\n".join(findings))
        return 1
    print("path_reference_scan=PASS")
    print(f"scanned_files={len(files())}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
