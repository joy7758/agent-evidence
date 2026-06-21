#!/usr/bin/env python3
"""Check deterministic content equivalence for the OTLP-to-EEOAP conversion."""

from __future__ import annotations

import copy
from pathlib import Path
from typing import Any

from _common import ROOT, experiment_result, load_json, repo_locator, validate_profile, write_json
from agent_evidence.oap import sha256_digest
from convert_otel_trace_to_eeoap import build_profile


ITERATIONS = 3
TRACE_PATH = ROOT / "data" / "otel" / "raw_demo_trace.json"
OUTPUT_PROFILE = ROOT / "data" / "eeoap" / "real_trace_evidence.json"
RESULT_PATH = ROOT / "experiments" / "results" / "exp4_determinism_oracle.json"


def _without_locator_fields(value: Any) -> Any:
    if isinstance(value, dict):
        return {
            key: _without_locator_fields(item)
            for key, item in value.items()
            if key not in {"locator"}
        }
    if isinstance(value, list):
        return [_without_locator_fields(item) for item in value]
    return value


def canonical_evidence_content(profile: dict[str, Any]) -> dict[str, Any]:
    """Return semantic evidence content, excluding environment-specific locators."""
    return _without_locator_fields(copy.deepcopy(profile))


def main() -> int:
    trace = load_json(TRACE_PATH)
    runs = []

    for index in range(ITERATIONS):
        profile = build_profile(trace, input_path=TRACE_PATH)
        report = validate_profile(profile, f"determinism-oracle-run-{index}")
        runs.append(
            {
                "iteration": index,
                "canonical_evidence_digest": sha256_digest(canonical_evidence_content(profile)),
                "validator_ok": report["ok"],
                "issue_count": report["issue_count"],
                "validator_status_digest": sha256_digest(
                    {
                        "ok": report["ok"],
                        "issue_count": report["issue_count"],
                        "primary_error_code": report["primary_error_code"],
                    }
                ),
            }
        )

    evidence_digests = {run["canonical_evidence_digest"] for run in runs}
    validator_digests = {run["validator_status_digest"] for run in runs}
    deterministic = len(evidence_digests) == 1 and len(validator_digests) == 1

    report = validate_profile(build_profile(trace, input_path=TRACE_PATH), str(OUTPUT_PROFILE))
    result = experiment_result(
        experiment_id="exp4_determinism_oracle",
        description=(
            "Repeated conversion of the same OTLP JSON fixture with canonicalized "
            "evidence-content comparison."
        ),
        source_type="determinism_oracle",
        trace=trace,
        output_profile=OUTPUT_PROFILE,
        validation_report=report,
        extra={
            "input_trace": repo_locator(TRACE_PATH),
            "iterations": ITERATIONS,
            "deterministic_content_equivalence": deterministic,
            "oracle_compares": [
                "canonicalized evidence content",
                "validator outcome status",
            ],
            "oracle_excludes": [
                "environment-specific locator fields",
            ],
            "runs": runs,
        },
    )
    write_json(RESULT_PATH, result)
    print(f"wrote {RESULT_PATH}")
    return 0 if deterministic and report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
