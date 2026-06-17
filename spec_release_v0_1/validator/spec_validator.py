#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

REQ = ("intent", "context", "action", "evidence", "risk", "authority")
STAGES = ("EVENT", "CI", "RISK", "REVIEW", "MERGE")
HASHES = ("event_hash", "trace_hash", "audit_hash", "certification_hash")


def m(v: Any) -> dict[str, Any]:
    return v if isinstance(v, dict) else {}


def sha(v: Any) -> bool:
    return (
        isinstance(v, str)
        and v.startswith("sha256:")
        and len(v.split(":", 1)[1]) == 64
        and all(c in "0123456789abcdef" for c in v.split(":", 1)[1])
    )


def validate(p: dict[str, Any]) -> list[str]:
    issues = []
    e = m(p.get("event"))
    for f in REQ:
        if f not in e:
            issues.append(f"event missing {f}")
    t = p.get("trace")
    if not isinstance(t, list):
        issues.append("trace must be a list")
    else:
        if [m(i).get("stage") for i in t] != list(STAGES):
            issues.append(f"trace stages must be {list(STAGES)}")
        if [m(i).get("index") for i in t] != list(range(len(t))):
            issues.append("trace indexes must be sequential from 0")
    a = m(p.get("audit"))
    if not a.get("policy_status"):
        issues.append("audit missing policy_status")
    if not a.get("causal_edges"):
        issues.append("audit missing causal_edges")
    c = m(p.get("certification_artifact"))
    h = m(c.get("hashes"))
    if c.get("verifiable") is not True:
        issues.append("certification_artifact.verifiable must be true")
    if c.get("replayable") is not True:
        issues.append("certification_artifact.replayable must be true")
    for f in HASHES:
        if not sha(h.get(f)):
            issues.append(f"certification_artifact.hashes.{f} must be sha256")
    return issues


def main(argv):
    if len(argv) != 2:
        print("usage: spec_validator.py <payload.json>")
        return 2
    try:
        payload = json.loads(Path(argv[1]).read_text(encoding="utf-8"))
    except Exception as exc:
        print(f"FAIL {argv[1]}: {exc}")
        return 1
    issues = validate(payload)
    if issues:
        print("FAIL")
        print("\n".join(issues))
        return 1
    print("PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
