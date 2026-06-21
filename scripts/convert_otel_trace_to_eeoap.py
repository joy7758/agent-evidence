#!/usr/bin/env python3
"""Convert an OTLP JSON trace into local EEOAP evidence artifacts.

The canonical output is an operation-accountability profile that can be checked
with `agent-evidence validate-profile`. A secondary trace-grounding record is
available for paper figures and reviewer inspection.
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from agent_evidence.oap import sha256_digest, with_recomputed_integrity


ROOT = Path(__file__).resolve().parents[1]


def repo_locator(path: Path) -> str:
    resolved = path.resolve()
    try:
        return resolved.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path, help="Input OTLP JSON trace.")
    parser.add_argument(
        "--output",
        required=True,
        type=Path,
        help="Output EEOAP operation-accountability statement JSON.",
    )
    parser.add_argument(
        "--adapter-record",
        type=Path,
        help="Optional output path for the trace-grounded EEOAP adapter record.",
    )
    return parser.parse_args()


def load_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return payload


def otlp_value(value: Any) -> Any:
    if not isinstance(value, dict):
        return value
    if "stringValue" in value:
        return value["stringValue"]
    if "intValue" in value:
        return value["intValue"]
    if "doubleValue" in value:
        return value["doubleValue"]
    if "boolValue" in value:
        return value["boolValue"]
    if "arrayValue" in value:
        values = value["arrayValue"].get("values", [])
        return [otlp_value(item) for item in values]
    if "kvlistValue" in value:
        entries = value["kvlistValue"].get("values", [])
        return {
            str(item.get("key", "")): otlp_value(item.get("value", {}))
            for item in entries
            if item.get("key")
        }
    return value


def otlp_attributes(attributes: Any) -> dict[str, Any]:
    if not isinstance(attributes, list):
        return {}
    normalized: dict[str, Any] = {}
    for item in attributes:
        if not isinstance(item, dict) or "key" not in item:
            continue
        normalized[str(item["key"])] = otlp_value(item.get("value", {}))
    return normalized


def flatten_spans(trace: dict[str, Any]) -> list[dict[str, Any]]:
    spans: list[dict[str, Any]] = []
    for resource_span in trace.get("resourceSpans", []):
        resource_attrs = otlp_attributes(resource_span.get("resource", {}).get("attributes", []))
        scope_spans = resource_span.get("scopeSpans") or resource_span.get(
            "instrumentationLibrarySpans", []
        )
        for scope_span in scope_spans:
            scope = scope_span.get("scope") or scope_span.get("instrumentationLibrary") or {}
            scope_attrs = otlp_attributes(scope.get("attributes", []))
            for span in scope_span.get("spans", []):
                if not isinstance(span, dict):
                    continue
                normalized = {
                    "trace_id": str(span.get("traceId", "")),
                    "span_id": str(span.get("spanId", "")),
                    "parent_span_id": span.get("parentSpanId") or None,
                    "name": str(span.get("name", "")),
                    "start_time_unix_nano": str(span.get("startTimeUnixNano", "0")),
                    "end_time_unix_nano": str(span.get("endTimeUnixNano", "0")),
                    "kind": span.get("kind", "unknown"),
                    "attributes": otlp_attributes(span.get("attributes", [])),
                    "resource_attributes": resource_attrs,
                    "scope": {
                        "name": scope.get("name"),
                        "version": scope.get("version"),
                        "attributes": scope_attrs,
                    },
                }
                spans.append(normalized)
    if not spans:
        raise ValueError("no OTLP spans found")
    missing = [span for span in spans if not span["trace_id"] or not span["span_id"]]
    if missing:
        raise ValueError("all normalized spans must include trace_id and span_id")
    return spans


def ns_to_iso8601(raw_ns: str) -> str:
    seconds = int(raw_ns) / 1_000_000_000
    return datetime.fromtimestamp(seconds, tz=timezone.utc).isoformat().replace("+00:00", "Z")


def trace_status(spans: list[dict[str, Any]]) -> str:
    for span in spans:
        status = span["attributes"].get("otel.status_code") or span["attributes"].get("status.code")
        if str(status).lower() in {"error", "2"}:
            return "failed"
    return "succeeded"


def trace_identifier(spans: list[dict[str, Any]]) -> str:
    return spans[0]["trace_id"]


def build_profile(trace: dict[str, Any], *, input_path: Path) -> dict[str, Any]:
    spans = flatten_spans(trace)
    trace_id = trace_identifier(spans)
    trace_digest = sha256_digest(trace)
    span_digest = sha256_digest(spans)
    output_digest = sha256_digest({"trace_id": trace_id, "span_count": len(spans), "spans": spans})
    status = trace_status(spans)
    statement = {
        "profile": {
            "name": "execution-evidence-operation-accountability-profile",
            "version": "0.1",
        },
        "statement_id": f"eeoap:otel:{trace_id.lower()}",
        "timestamp": ns_to_iso8601(spans[0]["start_time_unix_nano"]),
        "actor": {
            "id": "actor:opentelemetry-demo-source",
            "type": "telemetry-source",
            "name": "OpenTelemetry OTLP JSON example",
            "runtime": "opentelemetry-proto/examples/trace.json",
        },
        "subject": {
            "id": f"trace:{trace_id}",
            "type": "opentelemetry-trace",
            "digest": trace_digest,
            "locator": repo_locator(input_path),
        },
        "operation": {
            "id": f"op:otel-to-eeoap:{trace_id.lower()}",
            "type": "telemetry.trace.convert",
            "description": "Convert one OTLP JSON trace into a local EEOAP evidence statement.",
            "subject_ref": f"trace:{trace_id}",
            "policy_ref": "policy:eeoap-v0.1-local-trace-grounding",
            "input_refs": ["ref:raw-otlp-trace"],
            "output_refs": ["ref:eeoap-statement"],
            "result": {
                "status": status,
                "summary": f"converted {len(spans)} OTLP span(s) into a local EEOAP statement",
            },
        },
        "policy": {
            "id": "policy:eeoap-v0.1-local-trace-grounding",
            "name": "local-eeoap-trace-grounding-policy",
            "constraint_refs": [
                "constraint:bind-raw-trace-digest",
                "constraint:preserve-span-identifiers",
                "constraint:local-validation-only",
            ],
        },
        "constraints": [
            {
                "id": "constraint:bind-raw-trace-digest",
                "description": "The EEOAP statement must reference the digest of the input OTLP JSON trace.",
            },
            {
                "id": "constraint:preserve-span-identifiers",
                "description": "Trace and span identifiers must be preserved in reviewer-visible evidence.",
            },
            {
                "id": "constraint:local-validation-only",
                "description": "Validation is local and does not claim external certification.",
            },
        ],
        "provenance": {
            "id": f"prov:otel-to-eeoap:{trace_id.lower()}",
            "actor_ref": "actor:opentelemetry-demo-source",
            "operation_ref": f"op:otel-to-eeoap:{trace_id.lower()}",
            "subject_ref": f"trace:{trace_id}",
            "input_refs": ["ref:raw-otlp-trace"],
            "output_refs": ["ref:eeoap-statement"],
        },
        "evidence": {
            "id": f"evidence:otel-to-eeoap:{trace_id.lower()}",
            "subject_ref": f"trace:{trace_id}",
            "operation_ref": f"op:otel-to-eeoap:{trace_id.lower()}",
            "policy_ref": "policy:eeoap-v0.1-local-trace-grounding",
            "references": [
                {
                    "ref_id": "ref:raw-otlp-trace",
                    "role": "input",
                    "object_id": f"trace:{trace_id}",
                    "digest": trace_digest,
                    "locator": repo_locator(input_path),
                },
                {
                    "ref_id": "ref:eeoap-statement",
                    "role": "output",
                    "object_id": f"eeoap:otel:{trace_id.lower()}",
                    "digest": output_digest,
                    "locator": "data/eeoap/real_trace_evidence.json",
                },
            ],
            "artifacts": [
                {
                    "artifact_id": "artifact:normalized-spans",
                    "type": "normalized-opentelemetry-spans",
                    "digest": span_digest,
                    "locator": "data/eeoap/real_trace_adapter_record.json",
                }
            ],
            "integrity": {
                "references_digest": "sha256:" + "0" * 64,
                "artifacts_digest": "sha256:" + "0" * 64,
                "statement_digest": "sha256:" + "0" * 64,
            },
        },
        "validation": {
            "id": f"validation:otel-to-eeoap:{trace_id.lower()}",
            "evidence_ref": f"evidence:otel-to-eeoap:{trace_id.lower()}",
            "provenance_ref": f"prov:otel-to-eeoap:{trace_id.lower()}",
            "policy_ref": "policy:eeoap-v0.1-local-trace-grounding",
            "validator": "agent-evidence validate-profile",
            "method": "schema+reference+consistency",
            "status": "verifiable",
        },
    }
    return with_recomputed_integrity(statement)


def build_adapter_record(
    trace: dict[str, Any],
    profile: dict[str, Any],
    *,
    input_path: Path,
    output_path: Path,
) -> dict[str, Any]:
    spans = flatten_spans(trace)
    trace_id = trace_identifier(spans)
    trace_digest = sha256_digest(trace)
    profile_digest = sha256_digest(profile)
    return {
        "version": "v0.1",
        "execution_id": profile["statement_id"],
        "timestamp": profile["timestamp"],
        "trace_source": {
            "system": "opentelemetry",
            "format": "otlp-json",
            "locator": repo_locator(input_path),
            "digest": trace_digest,
        },
        "spans": [
            {
                "trace_id": span["trace_id"],
                "span_id": span["span_id"],
                "parent_span_id": span["parent_span_id"],
                "name": span["name"],
                "start_time_unix_nano": span["start_time_unix_nano"],
                "end_time_unix_nano": span["end_time_unix_nano"],
                "kind": span["kind"],
                "attributes": span["attributes"],
            }
            for span in spans
        ],
        "evidence": [
            {
                "evidence_id": "evidence:raw-otlp-trace",
                "role": "input",
                "object_ref": f"trace:{trace_id}",
                "digest": trace_digest,
                "locator": repo_locator(input_path),
                "derived_from_span_ids": [span["span_id"] for span in spans],
            },
            {
                "evidence_id": "evidence:eeoap-statement",
                "role": "output",
                "object_ref": profile["statement_id"],
                "digest": profile_digest,
                "locator": repo_locator(output_path),
                "derived_from_span_ids": [span["span_id"] for span in spans],
            },
        ],
        "status": profile["operation"]["result"]["status"],
    }


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> int:
    args = parse_args()
    trace = load_json(args.input)
    profile = build_profile(trace, input_path=args.input)
    write_json(args.output, profile)
    print(f"wrote {args.output}")

    if args.adapter_record:
        adapter_record = build_adapter_record(
            trace,
            profile,
            input_path=args.input,
            output_path=args.output,
        )
        write_json(args.adapter_record, adapter_record)
        print(f"wrote {args.adapter_record}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
