#!/usr/bin/env python3
"""Synthetic two-span OpenTelemetry-to-EEOAP conversion experiment."""

from __future__ import annotations

from pathlib import Path

from _common import RESULTS_DIR, experiment_result, validate_profile, write_json
from convert_otel_trace_to_eeoap import build_profile


ROOT = Path(__file__).resolve().parents[1]


def synthetic_trace() -> dict:
    trace_id = "11111111111111111111111111111111"
    return {
        "resourceSpans": [
            {
                "resource": {
                    "attributes": [
                        {"key": "service.name", "value": {"stringValue": "synthetic.agent"}}
                    ]
                },
                "scopeSpans": [
                    {
                        "scope": {"name": "agent.synthetic", "version": "1.0.0"},
                        "spans": [
                            {
                                "traceId": trace_id,
                                "spanId": "2222222222222222",
                                "name": "agent.request",
                                "startTimeUnixNano": "1700000000000000000",
                                "endTimeUnixNano": "1700000000500000000",
                                "kind": 2,
                                "attributes": [
                                    {"key": "agent.operation", "value": {"stringValue": "answer"}}
                                ],
                            },
                            {
                                "traceId": trace_id,
                                "spanId": "3333333333333333",
                                "parentSpanId": "2222222222222222",
                                "name": "tool.lookup",
                                "startTimeUnixNano": "1700000000100000000",
                                "endTimeUnixNano": "1700000000300000000",
                                "kind": 1,
                                "attributes": [
                                    {"key": "tool.name", "value": {"stringValue": "fixture_lookup"}}
                                ],
                            },
                        ],
                    }
                ],
            }
        ]
    }


def main() -> int:
    trace_path = RESULTS_DIR / "exp1_synthetic_trace.json"
    output_profile = RESULTS_DIR / "exp1_synthetic_evidence.json"
    result_path = RESULTS_DIR / "exp1_synthetic.json"

    trace = synthetic_trace()
    profile = build_profile(trace, input_path=trace_path)
    report = validate_profile(profile, str(output_profile))

    write_json(trace_path, trace)
    write_json(output_profile, profile)
    write_json(
        result_path,
        experiment_result(
            experiment_id="exp1_synthetic",
            description="Synthetic two-span trace conversion baseline.",
            source_type="synthetic_fixture",
            trace=trace,
            output_profile=output_profile,
            validation_report=report,
            extra={"expected_span_chain": "agent.request -> tool.lookup"},
        ),
    )
    print(f"wrote {result_path}")
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
