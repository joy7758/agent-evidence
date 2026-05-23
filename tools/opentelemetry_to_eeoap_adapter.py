#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from agent_evidence.oap import (  # noqa: E402
    sha256_digest,
    validate_profile_file,
    with_recomputed_integrity,
)

AGENT_ATTRIBUTE_KEYS = (
    "gen_ai.agent.id",
    "gen_ai.agent.name",
    "gen_ai.agent.version",
)
DEFAULT_OUTPUT_DIR = Path("generated")


class AdapterError(ValueError):
    """Raised when an OpenTelemetry trace cannot be mapped into EEOAP."""

    def __init__(
        self,
        code: str,
        message: str,
        *,
        path: str | None = None,
        span_id: str | None = None,
    ) -> None:
        super().__init__(message)
        self.code = code
        self.path = path
        self.span_id = span_id

    def diagnostic(self) -> dict[str, str]:
        diagnostic = {
            "code": self.code,
            "message": str(self),
        }
        if self.path is not None:
            diagnostic["path"] = self.path
        if self.span_id is not None:
            diagnostic["span_id"] = self.span_id
        return diagnostic


@dataclass(frozen=True)
class SpanRecord:
    path: str
    raw: dict[str, Any]
    trace_id: str
    span_id: str
    parent_span_id: str
    name: str
    attributes: dict[str, Any]
    start_time: str | None
    end_time: str | None
    error_type: str | None


def _otel_value(value: Any) -> Any:
    if not isinstance(value, dict):
        return value

    for key in ("stringValue", "intValue", "doubleValue", "boolValue", "bytesValue"):
        if key in value:
            return value[key]

    if "arrayValue" in value:
        raw_values = value["arrayValue"].get("values", [])
        if isinstance(raw_values, list):
            return [_otel_value(item) for item in raw_values]

    if "kvlistValue" in value:
        raw_values = value["kvlistValue"].get("values", [])
        if isinstance(raw_values, list):
            return {
                str(item.get("key")): _otel_value(item.get("value"))
                for item in raw_values
                if isinstance(item, dict) and item.get("key")
            }

    return value


def _attributes(raw_span: dict[str, Any]) -> dict[str, Any]:
    raw_attributes = raw_span.get("attributes", {})
    if isinstance(raw_attributes, dict):
        return {str(key): _otel_value(value) for key, value in raw_attributes.items()}

    if isinstance(raw_attributes, list):
        attributes: dict[str, Any] = {}
        for item in raw_attributes:
            if not isinstance(item, dict) or not item.get("key"):
                continue
            attributes[str(item["key"])] = _otel_value(item.get("value"))
        return attributes

    return {}


def _string_attr(span: SpanRecord, key: str) -> str | None:
    value = span.attributes.get(key)
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def _span_id(raw_span: dict[str, Any]) -> str:
    value = raw_span.get("spanId", raw_span.get("span_id", ""))
    return str(value).strip()


def _trace_id(raw_span: dict[str, Any]) -> str:
    value = raw_span.get("traceId", raw_span.get("trace_id", ""))
    return str(value).strip()


def _parent_span_id(raw_span: dict[str, Any]) -> str:
    value = raw_span.get("parentSpanId", raw_span.get("parent_span_id", ""))
    return str(value).strip()


def _raw_spans(payload: dict[str, Any]) -> list[tuple[str, dict[str, Any]]]:
    spans = payload.get("spans")
    if isinstance(spans, list):
        return [
            (f"spans[{index}]", span) for index, span in enumerate(spans) if isinstance(span, dict)
        ]

    records: list[tuple[str, dict[str, Any]]] = []
    resource_spans = payload.get("resourceSpans", [])
    if not isinstance(resource_spans, list):
        return records

    for resource_index, resource_span in enumerate(resource_spans):
        if not isinstance(resource_span, dict):
            continue
        scope_spans = resource_span.get(
            "scopeSpans",
            resource_span.get("instrumentationLibrarySpans", []),
        )
        if not isinstance(scope_spans, list):
            continue
        for scope_index, scope_span in enumerate(scope_spans):
            if not isinstance(scope_span, dict):
                continue
            spans = scope_span.get("spans", [])
            if not isinstance(spans, list):
                continue
            for span_index, span in enumerate(spans):
                if isinstance(span, dict):
                    records.append(
                        (
                            "resourceSpans"
                            f"[{resource_index}].scopeSpans[{scope_index}].spans[{span_index}]",
                            span,
                        )
                    )
    return records


def _span_records(payload: dict[str, Any]) -> list[SpanRecord]:
    records: list[SpanRecord] = []
    for path, raw_span in _raw_spans(payload):
        span_id = _span_id(raw_span)
        trace_id = _trace_id(raw_span)
        if not span_id:
            raise AdapterError("malformed_span", "span is missing span_id/spanId", path=path)
        if not trace_id:
            raise AdapterError("malformed_span", "span is missing trace_id/traceId", path=path)

        attributes = _attributes(raw_span)
        error_type = attributes.get("error.type")
        records.append(
            SpanRecord(
                path=path,
                raw=raw_span,
                trace_id=trace_id,
                span_id=span_id,
                parent_span_id=_parent_span_id(raw_span),
                name=str(raw_span.get("name", "")).strip(),
                attributes=attributes,
                start_time=_span_time(raw_span, "start"),
                end_time=_span_time(raw_span, "end"),
                error_type=str(error_type).strip() if error_type else None,
            )
        )
    return records


def _span_time(raw_span: dict[str, Any], prefix: str) -> str | None:
    if prefix == "start":
        value = raw_span.get("startTimeUnixNano", raw_span.get("start_time_unix_nano"))
        if value is None:
            value = raw_span.get("startTime", raw_span.get("start_time"))
    else:
        value = raw_span.get("endTimeUnixNano", raw_span.get("end_time_unix_nano"))
        if value is None:
            value = raw_span.get("endTime", raw_span.get("end_time"))
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def _timestamp_to_iso(value: str | None) -> str | None:
    if not value:
        return None
    if value.isdigit():
        seconds = int(value) / 1_000_000_000
        return (
            datetime.fromtimestamp(seconds, tz=timezone.utc)
            .isoformat(timespec="microseconds")
            .replace("+00:00", "Z")
        )
    return value


def _safe_id_part(value: str) -> str:
    lowered = value.strip().lower()
    safe = re.sub(r"[^a-z0-9._:-]+", "-", lowered)
    return safe.strip("-") or "trace"


def _is_agent_span(span: SpanRecord) -> bool:
    return any(_string_attr(span, key) for key in AGENT_ATTRIBUTE_KEYS)


def _is_tool_span(span: SpanRecord) -> bool:
    operation_name = _string_attr(span, "gen_ai.operation.name")
    if operation_name == "execute_tool":
        return True
    return span.name.startswith("execute_tool")


def _locate_agent_span(spans: list[SpanRecord]) -> SpanRecord:
    agent_spans = [span for span in spans if _is_agent_span(span)]
    if not agent_spans:
        raise AdapterError(
            "missing_agent_span",
            "no span with gen_ai.agent.* attributes was found",
        )
    if len(agent_spans) > 1:
        span_ids = ", ".join(span.span_id for span in agent_spans)
        raise AdapterError(
            "multiple_agent_spans",
            f"expected one agent span, found {len(agent_spans)}: {span_ids}",
        )
    return agent_spans[0]


def _same_trace_spans(spans: list[SpanRecord], trace_id: str) -> list[SpanRecord]:
    return [span for span in spans if span.trace_id == trace_id]


def _validate_parent_closure(spans: list[SpanRecord]) -> dict[str, SpanRecord]:
    by_id = {span.span_id: span for span in spans}
    for span in spans:
        if span.parent_span_id and span.parent_span_id not in by_id:
            raise AdapterError(
                "broken_parent_span_relation",
                (f"span {span.span_id} references missing parent span {span.parent_span_id}"),
                path=span.path,
                span_id=span.span_id,
            )
    return by_id


def _is_descendant_of_agent(
    span: SpanRecord,
    agent_span: SpanRecord,
    spans_by_id: dict[str, SpanRecord],
) -> bool:
    current_parent = span.parent_span_id
    visited: set[str] = set()
    while current_parent:
        if current_parent == agent_span.span_id:
            return True
        if current_parent in visited:
            raise AdapterError(
                "broken_parent_span_relation",
                f"cycle detected while resolving parent chain for span {span.span_id}",
                path=span.path,
                span_id=span.span_id,
            )
        visited.add(current_parent)
        parent = spans_by_id.get(current_parent)
        if parent is None:
            return False
        current_parent = parent.parent_span_id
    return False


def _resolved_tool_spans(
    spans: list[SpanRecord],
    agent_span: SpanRecord,
    spans_by_id: dict[str, SpanRecord],
) -> list[SpanRecord]:
    tool_spans = [span for span in spans if _is_tool_span(span)]
    resolved: list[SpanRecord] = []
    for span in tool_spans:
        if not _is_descendant_of_agent(span, agent_span, spans_by_id):
            raise AdapterError(
                "unresolved_tool_span",
                (
                    f"execute_tool span {span.span_id} is not a descendant "
                    f"of agent span {agent_span.span_id}"
                ),
                path=span.path,
                span_id=span.span_id,
            )
        resolved.append(span)
    return resolved


def _span_locator(span: SpanRecord) -> str:
    return f"otel://trace/{span.trace_id}/span/{span.span_id}"


def _tool_payload(span: SpanRecord) -> dict[str, Any]:
    return {
        "trace_id": span.trace_id,
        "span_id": span.span_id,
        "parent_span_id": span.parent_span_id,
        "name": span.name,
        "operation_name": _string_attr(span, "gen_ai.operation.name"),
        "tool_name": _string_attr(span, "gen_ai.tool.name"),
        "tool_call_id": _string_attr(span, "gen_ai.tool.call.id"),
        "start_time": _timestamp_to_iso(span.start_time),
        "end_time": _timestamp_to_iso(span.end_time),
        "error_type": span.error_type,
    }


def _extracted_payload(
    agent_span: SpanRecord,
    tool_spans: list[SpanRecord],
    operation_name: str,
) -> dict[str, Any]:
    return {
        "trace_id": agent_span.trace_id,
        "span_id": agent_span.span_id,
        "parent_span_id": agent_span.parent_span_id,
        "agent": {
            "id": _string_attr(agent_span, "gen_ai.agent.id"),
            "name": _string_attr(agent_span, "gen_ai.agent.name"),
            "version": _string_attr(agent_span, "gen_ai.agent.version"),
        },
        "operation_name": operation_name,
        "timestamps": {
            "start_time": _timestamp_to_iso(agent_span.start_time),
            "end_time": _timestamp_to_iso(agent_span.end_time),
        },
        "error_type": agent_span.error_type,
        "tool_spans": [_tool_payload(span) for span in tool_spans],
    }


def convert_trace_to_eeoap_statement(
    payload: dict[str, Any],
    *,
    source_locator: str,
    case_name: str,
) -> tuple[dict[str, Any], dict[str, Any]]:
    spans = _span_records(payload)
    agent_span = _locate_agent_span(spans)
    trace_spans = _same_trace_spans(spans, agent_span.trace_id)
    spans_by_id = _validate_parent_closure(trace_spans)

    operation_name = _string_attr(agent_span, "gen_ai.operation.name")
    if not operation_name:
        raise AdapterError(
            "missing_operation_name",
            "agent span is missing gen_ai.operation.name",
            path=agent_span.path,
            span_id=agent_span.span_id,
        )

    tool_spans = _resolved_tool_spans(trace_spans, agent_span, spans_by_id)
    extracted = _extracted_payload(agent_span, tool_spans, operation_name)
    status = (
        "failed"
        if agent_span.error_type or any(span.error_type for span in tool_spans)
        else "succeeded"
    )
    case_id = _safe_id_part(case_name)
    subject_id = f"otel-trace:{agent_span.trace_id}"
    operation_id = f"op:otel:{agent_span.span_id}"
    policy_id = "policy:otel-to-eeoap-adapter-v1"
    evidence_id = f"evidence:otel:{agent_span.span_id}"
    provenance_id = f"prov:otel:{agent_span.span_id}"
    validation_id = f"validation:otel:{agent_span.span_id}"
    input_ref = "ref:otel-trace"
    output_ref = "ref:otel-agent-operation-result"
    agent_id = _string_attr(agent_span, "gen_ai.agent.id") or (
        f"actor:otel-agent:{agent_span.span_id}"
    )
    agent_name = _string_attr(agent_span, "gen_ai.agent.name") or "opentelemetry-agent"
    agent_version = _string_attr(agent_span, "gen_ai.agent.version")
    runtime = "opentelemetry-gen-ai"
    if agent_version:
        runtime = f"{runtime}/{agent_version}"

    trace_digest = sha256_digest(payload)
    result_object = {
        "operation_name": operation_name,
        "status": status,
        "trace_id": agent_span.trace_id,
        "agent_span_id": agent_span.span_id,
        "tool_span_ids": [span.span_id for span in tool_spans],
        "error_types": [
            error
            for error in [agent_span.error_type, *(span.error_type for span in tool_spans)]
            if error
        ],
    }

    artifacts = [
        {
            "artifact_id": f"artifact:otel-agent-span:{agent_span.span_id}",
            "type": "opentelemetry-agent-span",
            "digest": sha256_digest(agent_span.raw),
            "locator": _span_locator(agent_span),
        }
    ]
    for span in tool_spans:
        tool_name = _string_attr(span, "gen_ai.tool.name") or "unknown-tool"
        artifacts.append(
            {
                "artifact_id": f"artifact:otel-tool-span:{span.span_id}",
                "type": f"opentelemetry-tool-span:{_safe_id_part(tool_name)}",
                "digest": sha256_digest(span.raw),
                "locator": _span_locator(span),
            }
        )

    statement = {
        "profile": {
            "name": "execution-evidence-operation-accountability-profile",
            "version": "0.1",
        },
        "statement_id": f"eeoap:otel:{case_id}:{agent_span.span_id}",
        "timestamp": _timestamp_to_iso(agent_span.start_time) or "1970-01-01T00:00:00Z",
        "actor": {
            "id": agent_id,
            "type": "agent",
            "name": agent_name,
            "runtime": runtime,
        },
        "subject": {
            "id": subject_id,
            "type": "opentelemetry-trace",
            "digest": trace_digest,
            "locator": source_locator,
        },
        "operation": {
            "id": operation_id,
            "type": operation_name,
            "description": (
                "Mapped from one OpenTelemetry GenAI agent span into an EEOAP "
                "operation accountability statement."
            ),
            "subject_ref": subject_id,
            "policy_ref": policy_id,
            "input_refs": [input_ref],
            "output_refs": [output_ref],
            "result": {
                "status": status,
                "summary": (
                    f"OpenTelemetry agent span {agent_span.span_id} mapped with "
                    f"{len(tool_spans)} execute_tool span(s)."
                ),
            },
        },
        "policy": {
            "id": policy_id,
            "name": "bounded-opentelemetry-to-eeoap-adapter-policy",
            "constraint_refs": [
                "constraint:single-agent-span",
                "constraint:operation-name-required",
                "constraint:tool-spans-parented-to-agent",
            ],
        },
        "constraints": [
            {
                "id": "constraint:single-agent-span",
                "description": "The input trace must contain exactly one GenAI agent span.",
            },
            {
                "id": "constraint:operation-name-required",
                "description": "The agent span must declare gen_ai.operation.name.",
            },
            {
                "id": "constraint:tool-spans-parented-to-agent",
                "description": (
                    "execute_tool spans must be reachable from the selected agent span "
                    "through parent_span_id links."
                ),
            },
        ],
        "provenance": {
            "id": provenance_id,
            "actor_ref": agent_id,
            "operation_ref": operation_id,
            "subject_ref": subject_id,
            "input_refs": [input_ref],
            "output_refs": [output_ref],
        },
        "evidence": {
            "id": evidence_id,
            "subject_ref": subject_id,
            "operation_ref": operation_id,
            "policy_ref": policy_id,
            "references": [
                {
                    "ref_id": input_ref,
                    "role": "input",
                    "object_id": subject_id,
                    "digest": trace_digest,
                    "locator": source_locator,
                },
                {
                    "ref_id": output_ref,
                    "role": "output",
                    "object_id": f"otel-operation-result:{agent_span.span_id}",
                    "digest": sha256_digest(result_object),
                    "locator": f"{_span_locator(agent_span)}#operation-result",
                },
            ],
            "artifacts": artifacts,
            "integrity": {},
        },
        "validation": {
            "id": validation_id,
            "evidence_ref": evidence_id,
            "provenance_ref": provenance_id,
            "policy_ref": policy_id,
            "validator": "agent-evidence validate-profile",
            "method": "schema+reference+consistency",
            "status": "verifiable",
        },
    }
    return with_recomputed_integrity(statement), extracted


def load_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise AdapterError("invalid_trace_json", f"expected JSON object: {path}")
    return payload


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def run_adapter(input_path: Path, output_dir: Path) -> tuple[int, Path, Path]:
    case_name = input_path.stem
    statement_path = output_dir / f"{case_name}-eeoap-statement.json"
    report_path = output_dir / f"{case_name}-adapter-report.json"
    source_locator = input_path.as_posix()

    try:
        payload = load_json(input_path)
        statement, extracted = convert_trace_to_eeoap_statement(
            payload,
            source_locator=source_locator,
            case_name=case_name,
        )
        write_json(statement_path, statement)
        validation_report = validate_profile_file(statement_path)
        diagnostics = []
        if not validation_report["ok"]:
            diagnostics.append(
                {
                    "code": "eeoap_validator_failed",
                    "message": "generated statement failed agent-evidence validate-profile",
                    "primary_error_code": str(validation_report["primary_error_code"]),
                }
            )
        adapter_report = {
            "ok": validation_report["ok"],
            "source": source_locator,
            "case_name": case_name,
            "statement_path": statement_path.as_posix(),
            "diagnostics": diagnostics,
            "extracted": extracted,
            "eeoap_validation": validation_report,
        }
        write_json(report_path, adapter_report)
        if diagnostics:
            return 1, statement_path, report_path
        return 0, statement_path, report_path
    except (AdapterError, json.JSONDecodeError, OSError) as exc:
        if isinstance(exc, AdapterError):
            diagnostic = exc.diagnostic()
        else:
            diagnostic = {
                "code": "invalid_trace_json",
                "message": str(exc),
            }
        adapter_report = {
            "ok": False,
            "source": source_locator,
            "case_name": case_name,
            "statement_path": None,
            "diagnostics": [diagnostic],
        }
        write_json(report_path, adapter_report)
        print(
            f"OpenTelemetry-to-EEOAP adapter failed: {diagnostic['code']}: {diagnostic['message']}",
            file=sys.stderr,
        )
        return 1, statement_path, report_path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Convert one local OpenTelemetry-style GenAI trace into an EEOAP statement."
    )
    parser.add_argument("input", type=Path, help="OpenTelemetry-style trace JSON file.")
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help="Directory for generated <case>-eeoap-statement.json and <case>-adapter-report.json.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    exit_code, statement_path, report_path = run_adapter(args.input, args.output_dir)
    if exit_code == 0:
        print(statement_path)
        print(report_path)
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
