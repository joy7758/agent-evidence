#!/usr/bin/env python3

from __future__ import annotations

import json
import sys
from pathlib import Path

from jsonschema import Draft202012Validator

CHECKER_ID = "repo-local-second-checker@0.1"
ROOT = Path(__file__).resolve().parents[3]
SCHEMA_PATH = (
    ROOT / "schema" / "execution-evidence-operation-accountability-profile-v0.1.schema.json"
)


def issue(stage: str, code: str, path: str, message: str) -> dict[str, str]:
    return {
        "stage": stage,
        "code": code,
        "path": path,
        "message": message,
    }


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def schema_issues(profile: dict) -> list[dict[str, str]]:
    schema = load_json(SCHEMA_PATH)
    validator = Draft202012Validator(schema)
    issues: list[dict[str, str]] = []
    for error in sorted(validator.iter_errors(profile), key=lambda item: list(item.path)):
        path = ".".join(str(part) for part in error.path) or "root"
        issues.append(issue("schema", "schema_violation", path, error.message))
    return issues


def minimal_closure_issues(profile: dict) -> list[dict[str, str]]:
    issues: list[dict[str, str]] = []

    policy_id = profile.get("policy", {}).get("id")
    evidence_policy_ref = profile.get("evidence", {}).get("policy_ref")
    if evidence_policy_ref != policy_id:
        issues.append(
            issue(
                "closure",
                "broken_evidence_policy_ref",
                "evidence.policy_ref",
                "evidence.policy_ref must resolve to policy.id.",
            )
        )

    reference_ids = {
        reference.get("ref_id")
        for reference in profile.get("evidence", {}).get("references", [])
        if isinstance(reference, dict) and reference.get("ref_id")
    }
    for index, ref_id in enumerate(profile.get("operation", {}).get("output_refs", [])):
        if ref_id not in reference_ids:
            issues.append(
                issue(
                    "closure",
                    "unresolved_output_ref",
                    f"operation.output_refs[{index}]",
                    "operation output ref does not resolve to evidence.references[].ref_id.",
                )
            )

    return issues


def build_report(profile_path: Path) -> dict:
    profile = load_json(profile_path)
    issues = schema_issues(profile)
    if not issues:
        issues.extend(minimal_closure_issues(profile))
    return {
        "checker": CHECKER_ID,
        "ok": not issues,
        "issue_count": len(issues),
        "issues": issues,
        "source": str(profile_path),
    }


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print(
            json.dumps(
                {
                    "checker": CHECKER_ID,
                    "ok": False,
                    "issue_count": 1,
                    "issues": [
                        issue(
                            "usage",
                            "missing_profile_path",
                            "argv",
                            "usage: check_profile_minimal.py <profile.json>",
                        )
                    ],
                },
                indent=2,
                sort_keys=True,
            )
        )
        return 2

    profile_path = Path(argv[1])
    report = build_report(profile_path)
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
