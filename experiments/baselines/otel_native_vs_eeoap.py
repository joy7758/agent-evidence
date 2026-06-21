#!/usr/bin/env python3
"""Compare native OTLP retention baselines with OpenTelemetry-to-EEOAP output.

This is a local feature-coverage comparison. It is not an external benchmark,
certification, or production-readiness result.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from agent_evidence.oap import validate_profile_file  # noqa: E402


OUTPUT_MD = ROOT / "experiments" / "results" / "otel_native_vs_eeoap.md"
OUTPUT_JSON = ROOT / "experiments" / "results" / "otel_native_vs_eeoap.json"
RAW_TRACE_REL = Path("data/otel/raw_demo_trace.json")
RAW_TRACE_PATH = ROOT / RAW_TRACE_REL
EEOAP_PATH = ROOT / "data" / "eeoap" / "real_trace_evidence.json"

COMPARISON_CONSTRAINTS = [
    "All systems use the identical input trace: data/otel/raw_demo_trace.json.",
    "No preprocessing differences are allowed before comparison.",
    "Only the output representation differs across rows.",
]


def load_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return payload


def has_resource_spans(payload: dict[str, Any]) -> bool:
    return isinstance(payload.get("resourceSpans"), list) and bool(payload["resourceSpans"])


def validate_same_input_trace(profile: dict[str, Any]) -> None:
    evidence = profile.get("evidence", {})
    references = evidence.get("references", [])
    if not isinstance(references, list):
        raise ValueError("EEOAP profile evidence.references must be a list")

    expected = RAW_TRACE_PATH.resolve()
    matching_inputs = []
    for item in references:
        if not isinstance(item, dict) or item.get("role") != "input":
            continue
        locator = item.get("locator")
        if not isinstance(locator, str):
            continue
        if Path(locator).resolve() == expected:
            matching_inputs.append(item)
    if not matching_inputs:
        raise ValueError(f"EEOAP profile must reference identical input trace {expected}")


def baseline_rows() -> list[dict[str, Any]]:
    raw_trace = load_json(RAW_TRACE_PATH)
    profile = load_json(EEOAP_PATH)
    validate_same_input_trace(profile)
    validation = validate_profile_file(EEOAP_PATH, fail_fast=False)

    raw_trace_has_spans = has_resource_spans(raw_trace)

    return [
        {
            "system": "Baseline A: raw OpenTelemetry trace storage",
            "preserves_trace_identity": "yes" if raw_trace_has_spans else "no",
            "binds_policy_or_constraints": "no",
            "binds_provenance": "no",
            "includes_evidence_refs": "no",
            "validator_readable_output": "no",
            "notes": "Preserves OTLP trace payload but does not bind policy, provenance, evidence references, or local validator output.",
        },
        {
            "system": "Baseline B: OpenTelemetry trace plus JSON export only",
            "preserves_trace_identity": "yes" if raw_trace_has_spans else "no",
            "binds_policy_or_constraints": "no",
            "binds_provenance": "no",
            "includes_evidence_refs": "no",
            "validator_readable_output": "no",
            "notes": "Portable JSON improves transport but remains observability-oriented rather than operation-accountability-oriented.",
        },
        {
            "system": "System: OpenTelemetry to EEOAP conversion",
            "preserves_trace_identity": "yes",
            "binds_policy_or_constraints": "yes",
            "binds_provenance": "yes",
            "includes_evidence_refs": "yes",
            "validator_readable_output": "yes" if validation["ok"] else "no",
            "notes": "Adds operation, policy, provenance, evidence references, integrity digests, and local validator-readable output.",
        },
    ]


def render_markdown(rows: list[dict[str, Any]]) -> str:
    lines = [
        "# OpenTelemetry Native vs EEOAP Baseline Comparison",
        "",
        "Affected clauses: EEOAP-001, EEOAP-002, EEOAP-003, EEOAP-004, EEOAP-005.",
        "",
        "Feature-coverage comparison across identical input traces.",
        "The comparison is local and descriptive, not an external benchmark.",
        "",
        "Fairness constraints:",
        "",
        "- All comparisons use the identical input trace:",
        "  `data/otel/raw_demo_trace.json`.",
        "- No preprocessing differences are allowed before comparison.",
        "- Only the output representation differs across rows.",
        "",
        "| System | Preserves trace identity | Binds policy/constraints | Binds provenance | Includes evidence references | Validator-readable output | Notes |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for row in rows:
        lines.append(
            "| {system} | {preserves_trace_identity} | {binds_policy_or_constraints} | "
            "{binds_provenance} | {includes_evidence_refs} | {validator_readable_output} | {notes} |".format(
                **row
            )
        )
    lines.extend(
        [
            "",
            "Boundary: the comparison identifies local review surfaces. It does not",
            "claim legal sufficiency, external certification, deployment robustness,",
            "official standard adoption, or publication status.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    rows = baseline_rows()
    OUTPUT_MD.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_MD.write_text(render_markdown(rows), encoding="utf-8")
    OUTPUT_JSON.write_text(
        json.dumps(
            {
                "comparison_constraints": COMPARISON_CONSTRAINTS,
                "input_trace": RAW_TRACE_REL.as_posix(),
                "rows": rows,
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )
    print(f"wrote {OUTPUT_MD}")
    print(f"wrote {OUTPUT_JSON}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
