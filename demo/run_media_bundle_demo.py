#!/usr/bin/env python3
from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

DEMO_ROOT = Path(__file__).resolve().parent
REPO_ROOT = DEMO_ROOT.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from agent_evidence.media_bundle import (  # noqa: E402
    BUNDLE_PROFILE,
    build_media_bundle,
    verify_media_bundle,
)

OUTPUT_DIR = DEMO_ROOT / "output" / "media_bundle_demo"
SOURCE_STATEMENT = REPO_ROOT / "examples" / "media" / "minimal-valid-media-evidence.json"


def write_json(path: Path, payload: object) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def copy_bundle_tree(source: Path, target: Path) -> None:
    target.mkdir(parents=True, exist_ok=True)
    for name in (
        "bundle.json",
        "statement.json",
        "checksums.txt",
        "validation-report.json",
        "summary.json",
    ):
        shutil.copyfile(source / name, target / name)
    shutil.copytree(source / "artifacts", target / "artifacts")


def load_statement(bundle_dir: Path) -> dict[str, object]:
    return json.loads((bundle_dir / "statement.json").read_text(encoding="utf-8"))


def tamper_artifact(bundle_dir: Path) -> None:
    statement = load_statement(bundle_dir)
    artifacts = statement["media"]["artifacts"]  # type: ignore[index]
    primary = next(artifact for artifact in artifacts if artifact["role"] == "primary_media")
    artifact_path = bundle_dir / primary["path"]
    with artifact_path.open("ab") as artifact_file:
        artifact_file.write(b"\ntampered artifact payload\n")


def tamper_missing_time_context(bundle_dir: Path) -> None:
    statement_path = bundle_dir / "statement.json"
    statement = load_statement(bundle_dir)
    statement.pop("time_context", None)
    write_json(statement_path, statement)


def tamper_policy_ref(bundle_dir: Path) -> None:
    statement_path = bundle_dir / "statement.json"
    statement = load_statement(bundle_dir)
    statement["operation"]["policy_ref"] = "policy:missing-from-bundle-demo"  # type: ignore[index]
    write_json(statement_path, statement)


def result_case(case: str, expected: str, report: dict[str, object]) -> dict[str, object]:
    issues = report["issues"]  # type: ignore[index]
    return {
        "case": case,
        "expected": expected,
        "observed_ok": report["ok"],
        "primary_codes": [issue["code"] for issue in issues],
    }


def main() -> int:
    if OUTPUT_DIR.exists():
        shutil.rmtree(OUTPUT_DIR)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    print("Step 1: build valid media bundle")
    build_media_bundle(SOURCE_STATEMENT, OUTPUT_DIR)
    print("- wrote bundle.json")

    print("Step 2: verify valid media bundle")
    valid_report = verify_media_bundle(OUTPUT_DIR)
    print(f"- {valid_report['summary']}")

    cases = [result_case("valid_bundle", "pass", valid_report)]

    tamper_specs = [
        ("tampered_artifact", "tampered-artifact", tamper_artifact),
        (
            "tampered_statement_missing_time",
            "tampered-statement-missing-time",
            tamper_missing_time_context,
        ),
        ("tampered_statement_policy_ref", "tampered-statement-policy-ref", tamper_policy_ref),
    ]

    print("Step 3: verify tampered bundles")
    for case_name, directory_name, tamper_func in tamper_specs:
        tampered_dir = OUTPUT_DIR / directory_name
        copy_bundle_tree(OUTPUT_DIR, tampered_dir)
        tamper_func(tampered_dir)
        report = verify_media_bundle(tampered_dir)
        cases.append(result_case(case_name, "fail", report))
        print(f"- {case_name}: {report['summary']}")

    matrix = {
        "profile": "aep-media-bundle-tamper-matrix@0.1",
        "cases": cases,
    }
    write_json(OUTPUT_DIR / "tamper-matrix.json", matrix)
    print("- wrote tamper-matrix.json")

    if valid_report["ok"] and all(case["observed_ok"] is False for case in cases[1:]):
        print(f"PASS {BUNDLE_PROFILE} demo")
        return 0

    print(f"FAIL {BUNDLE_PROFILE} demo")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
