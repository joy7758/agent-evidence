#!/usr/bin/env python3
"""Noisy OTLP trace recovery experiment with ignored non-semantic fields."""

from __future__ import annotations

import copy
from pathlib import Path

from _common import RESULTS_DIR, ROOT, experiment_result, load_json, validate_profile, write_json
from convert_otel_trace_to_eeoap import build_profile, flatten_spans


def add_noise(trace: dict) -> dict:
    noisy = copy.deepcopy(trace)
    noisy["unknownTopLevelField"] = {
        "note": "ignored by converter; used to test resilience to non-semantic noise"
    }
    for resource_span in noisy.get("resourceSpans", []):
        resource = resource_span.setdefault("resource", {})
        resource.setdefault("attributes", []).append(
            {"key": "noise.resource", "value": {"stringValue": "ignored"}}
        )
        for scope_span in resource_span.get("scopeSpans", []):
            scope_span["unknownScopeField"] = "ignored"
            for span in scope_span.get("spans", []):
                span.setdefault("attributes", []).append(
                    {"key": "noise.span", "value": {"stringValue": "ignored"}}
                )
                span["unknownSpanField"] = {"ignored": True}
    return noisy


def main() -> int:
    source_trace_path = ROOT / "data" / "otel" / "raw_demo_trace.json"
    noisy_trace_path = RESULTS_DIR / "exp3_noisy_trace.json"
    output_profile = RESULTS_DIR / "exp3_noisy_recovery_evidence.json"
    result_path = RESULTS_DIR / "exp3_noisy_recovery.json"

    trace = load_json(source_trace_path)
    noisy_trace = add_noise(trace)
    profile = build_profile(noisy_trace, input_path=noisy_trace_path)
    report = validate_profile(profile, str(output_profile))

    write_json(noisy_trace_path, noisy_trace)
    write_json(output_profile, profile)
    write_json(
        result_path,
        experiment_result(
            experiment_id="exp3_noisy_recovery",
            description="Noisy public OTLP example converted while preserving span identifiers.",
            source_type="public_opentelemetry_proto_example_with_non_semantic_noise",
            trace=noisy_trace,
            output_profile=output_profile,
            validation_report=report,
            extra={
                "noise_model": "extra top-level, scope, resource, and span fields",
                "recovered_span_ids": [span["span_id"] for span in flatten_spans(noisy_trace)],
            },
        ),
    )
    print(f"wrote {result_path}")
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
