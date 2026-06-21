#!/usr/bin/env python3
"""Official OpenTelemetry OTLP JSON example conversion experiment."""

from __future__ import annotations

from pathlib import Path

from _common import ROOT, experiment_result, load_json, repo_locator, validate_profile, write_json
from convert_otel_trace_to_eeoap import build_adapter_record, build_profile


def main() -> int:
    trace_path = ROOT / "data" / "otel" / "raw_demo_trace.json"
    output_profile = ROOT / "data" / "eeoap" / "real_trace_evidence.json"
    adapter_record = ROOT / "data" / "eeoap" / "real_trace_adapter_record.json"
    result_path = ROOT / "experiments" / "results" / "exp2_real_trace.json"
    if not trace_path.exists():
        raise FileNotFoundError(
            f"missing {trace_path}; run scripts/fetch_otel_demo_trace.py first"
        )

    trace = load_json(trace_path)
    profile = build_profile(trace, input_path=trace_path)
    report = validate_profile(profile, str(output_profile))
    write_json(output_profile, profile)
    write_json(
        adapter_record,
        build_adapter_record(trace, profile, input_path=trace_path, output_path=output_profile),
    )
    write_json(
        result_path,
        experiment_result(
            experiment_id="exp2_real_trace",
            description="Official OpenTelemetry OTLP JSON example converted to EEOAP.",
            source_type="public_opentelemetry_proto_example",
            trace=trace,
            output_profile=output_profile,
            validation_report=report,
            extra={
                "input_trace": repo_locator(trace_path),
                "adapter_record": repo_locator(adapter_record),
                "source_note": (
                    "Fetched from open-telemetry/opentelemetry-proto examples/trace.json."
                ),
            },
        ),
    )
    print(f"wrote {result_path}")
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
