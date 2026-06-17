#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MARKERS = (
    "TO" + "DO",
    "FIX" + "ME",
    "<" + "link" + ">",
    "<" + "repo" + ">",
    "T" + "BD",
    "INS" + "ERT",
    "replace" + "-me",
)


def spans(path, text):
    if path.name != "submission_metadata.json":
        return []
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        return []
    urls = data.get("artifact_urls")
    out = []
    if isinstance(urls, dict):
        for v in urls.values():
            if isinstance(v, str):
                s = text.find(v)
                if s >= 0:
                    out.append((s, s + len(v)))
    return out


def main():
    files = sorted(
        p
        for p in ROOT.rglob("*")
        if p.is_file() and p.suffix.lower() in {".md", ".json", ".py", ".sh"}
    )
    findings = []
    for p in files:
        text = p.read_text(encoding="utf-8")
        allow = spans(p, text)
        for marker in MARKERS:
            i = text.find(marker)
            while i >= 0:
                if not any(a <= i < b for a, b in allow):
                    line_number = text.count(chr(10), 0, i) + 1
                    findings.append(
                        f"{p.relative_to(ROOT)}:{line_number}: unresolved marker {marker!r}"
                    )
                i = text.find(marker, i + len(marker))
    if findings:
        print("placeholder_scan=FAIL")
        print("\n".join(findings))
        return 1
    print("placeholder_scan=PASS")
    print(f"scanned_files={len(files)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
