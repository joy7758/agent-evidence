#!/usr/bin/env python3
# ruff: noqa: E402, I001
from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from agent_evidence.oap import validate_profile_file
from check_minimal_boundary import load_payload, validate_payload

DEFAULT_CORPUS = [
    "examples/minimal-valid-evidence.json",
    "examples/valid-retention-review-evidence.json",
    "examples/invalid-missing-required.json",
    "examples/invalid-unclosed-reference.json",
    "examples/invalid-policy-link-broken.json",
    "examples/invalid-provenance-output-mismatch.json",
    "examples/invalid-validation-provenance-link-broken.json",
    "paper/flagship/assets/specimens/scenario_03_access_decision_valid.json",
    "paper/flagship/assets/specimens/scenario_03_access_decision_invalid_missing_policy_linkage.json",
    "paper/flagship/assets/specimens/scenario_04_object_derivation_handoff_valid.json",
    "paper/flagship/assets/specimens/scenario_04_object_derivation_handoff_invalid_broken_evidence_continuity.json",
    "paper/flagship/assets/specimens/scenario_05_failed_or_denied_operation_valid.json",
    "paper/flagship/assets/specimens/scenario_05_failed_or_denied_operation_invalid_missing_outcome.json",
    "paper/flagship/assets/specimens/scenario_06_missing_identity_binding_invalid.json",
    "paper/flagship/assets/specimens/scenario_07_temporal_inconsistency_invalid.json",
    "paper/flagship/assets/specimens/scenario_08_implementation_coupled_evidence_invalid.json",
    "paper/flagship/assets/specimens/scenario_09_missing_target_binding_invalid.json",
    "paper/flagship/assets/specimens/scenario_10_ambiguous_operation_semantics_invalid.json",
    "paper/flagship/assets/specimens/scenario_11_outcome_unverifiability_invalid.json",
]


def summarize_reference(path: Path) -> tuple[str, str]:
    report = validate_profile_file(path)
    status = "PASS" if report["ok"] else "FAIL"
    labels: list[str] = []
    for stage in report["stages"]:
        for issue in stage["issues"]:
            code = issue["code"]
            if code not in labels:
                labels.append(code)
    return status, ", ".join(labels) if labels else "-"


def summarize_independent(path: Path) -> tuple[str, str]:
    payload = load_payload(path)
    issues = validate_payload(payload)
    status = "PASS" if not issues else "FAIL"
    labels: list[str] = []
    for issue in issues:
        label = issue["label"]
        if label not in labels:
            labels.append(label)
    return status, ", ".join(labels) if labels else "-"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Compare reference and independent checkers.")
    parser.add_argument("paths", nargs="*", help="Optional corpus paths")
    args = parser.parse_args(argv)

    raw_paths = args.paths or DEFAULT_CORPUS
    corpus = [Path(item) for item in raw_paths]

    print("| file | reference | reference labels | independent | independent labels |")
    print("| --- | --- | --- | --- | --- |")
    for path in corpus:
        ref_status, ref_labels = summarize_reference(path)
        ind_status, ind_labels = summarize_independent(path)
        print(f"| `{path}` | {ref_status} | {ref_labels} | {ind_status} | {ind_labels} |")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
