from __future__ import annotations

from typing import Any, Mapping

from agent_evidence.models import EvidenceContext, EvidenceEvent
from agent_evidence.recorder import EvidenceRecorder
from agent_evidence.serialization import ensure_json_object, to_jsonable

try:
    from agents import add_trace_processor as _add_trace_processor
    from agents import set_trace_processors as _set_trace_processors
    from agents.tracing import TracingProcessor as OpenAIAgentsTracingProcessorBase
except ImportError:  # pragma: no cover - exercised when extra is absent

    class OpenAIAgentsTracingProcessorBase:  # type: ignore[no-redef]
        """Fallback base so the package remains importable without openai-agents."""

    _HAS_OPENAI_AGENTS = False
else:
    _HAS_OPENAI_AGENTS = True

_SEMANTIC_EVENT_TYPES = {
    "on_trace_start": "trace.start",
    "on_trace_end": "trace.end",
    "on_span_start": "span.start",
    "on_span_end": "span.end",
}


def _merge_tags(*parts: list[str] | tuple[str, ...] | None) -> list[str]:
    merged: list[str] = []
    for part in parts:
        for tag in part or []:
            tag_text = str(tag)
            if tag_text and tag_text not in merged:
                merged.append(tag_text)
    return merged


def _semantic_event_type(source_event_type: str) -> str:
    return _SEMANTIC_EVENT_TYPES.get(source_event_type, source_event_type.replace("_", "."))


def _trace_payload(trace: Any) -> dict[str, Any]:
    if hasattr(trace, "export"):
        exported = trace.export()
        if isinstance(exported, Mapping):
            return ensure_json_object(exported)
    return {}


def _span_payload(span: Any) -> dict[str, Any]:
    if hasattr(span, "export"):
        exported = span.export()
        if isinstance(exported, Mapping):
            return ensure_json_object(exported)
    return {}


def _trace_id(trace: Any, payload: Mapping[str, Any]) -> str | None:
    return str(payload.get("id") or getattr(trace, "trace_id", "") or "") or None


def _span_id(span: Any, payload: Mapping[str, Any]) -> str | None:
    return str(payload.get("id") or getattr(span, "span_id", "") or "") or None


def _span_parent_id(span: Any, payload: Mapping[str, Any]) -> str | None:
    return str(payload.get("parent_id") or getattr(span, "parent_id", "") or "") or None


def _span_data(payload: Mapping[str, Any]) -> dict[str, Any]:
    span_data = payload.get("span_data")
    if isinstance(span_data, Mapping):
        return ensure_json_object(span_data)
    return {}


def build_openai_agents_context(
    *,
    source_event_type: str,
    component: str,
    name: str | None,
    span_id: str | None = None,
    parent_span_id: str | None = None,
    tags: list[str] | tuple[str, ...] | None = None,
    attributes: Mapping[str, Any] | None = None,
) -> EvidenceContext:
    return EvidenceContext(
        source="openai_agents",
        component=component,
        source_event_type=source_event_type,
        span_id=span_id,
        parent_span_id=parent_span_id,
        name=name,
        tags=_merge_tags(["openai_agents", component], list(tags or [])),
        attributes=ensure_json_object(attributes),
    )


def evidence_from_openai_agents_trace(
    trace: Any,
    *,
    source_event_type: str,
) -> EvidenceEvent:
    payload = _trace_payload(trace)
    workflow_name = str(payload.get("workflow_name") or getattr(trace, "name", "trace"))
    trace_metadata = payload.get("metadata")
    return EvidenceEvent(
        event_type=_semantic_event_type(source_event_type),
        actor=workflow_name,
        inputs=payload if source_event_type == "on_trace_start" else {},
        outputs=payload if source_event_type == "on_trace_end" else {},
        context=build_openai_agents_context(
            source_event_type=source_event_type,
            component="trace",
            name=workflow_name,
            span_id=_trace_id(trace, payload),
            tags=["workflow"],
            attributes={
                "group_id": payload.get("group_id"),
                "trace_id": _trace_id(trace, payload),
                "sdk_object": payload.get("object"),
            },
        ),
        metadata=ensure_json_object(trace_metadata if isinstance(trace_metadata, Mapping) else {}),
    )


def evidence_from_openai_agents_span(
    span: Any,
    *,
    source_event_type: str,
) -> EvidenceEvent:
    payload = _span_payload(span)
    span_data = _span_data(payload)
    span_type = str(span_data.get("type") or "span")
    span_name = str(span_data.get("name") or span_type)
    error = payload.get("error")
    trace_metadata = getattr(span, "trace_metadata", None)
    return EvidenceEvent(
        event_type=_semantic_event_type(source_event_type),
        actor=span_name,
        inputs=payload if source_event_type == "on_span_start" else {},
        outputs=payload if source_event_type == "on_span_end" else {},
        context=build_openai_agents_context(
            source_event_type=source_event_type,
            component=span_type,
            name=span_name,
            span_id=_span_id(span, payload),
            parent_span_id=_span_parent_id(span, payload),
            tags=["span"],
            attributes={
                "trace_id": payload.get("trace_id"),
                "sdk_object": payload.get("object"),
                "started_at": payload.get("started_at"),
                "ended_at": payload.get("ended_at"),
                "error_present": error is not None,
            },
        ),
        metadata=ensure_json_object(
            {
                "span_data": span_data,
                "trace_metadata": trace_metadata if isinstance(trace_metadata, Mapping) else {},
                "error": error,
            }
        ),
    )


class AgentEvidenceTracingProcessor(OpenAIAgentsTracingProcessorBase):
    """OpenAI Agents tracing processor that records traces and spans as evidence."""

    def __init__(
        self,
        recorder: EvidenceRecorder,
        *,
        base_tags: list[str] | None = None,
    ) -> None:
        if not _HAS_OPENAI_AGENTS:
            raise ModuleNotFoundError(
                "openai-agents is required for AgentEvidenceTracingProcessor. "
                "Install agent-evidence with the [openai-agents] extra."
            )
        self.recorder = recorder
        self.base_tags = base_tags or []

    def _record_event(self, event: EvidenceEvent) -> None:
        context_data = event.context.model_dump(mode="json")
        context_data["tags"] = _merge_tags(event.context.tags, self.base_tags)
        self.recorder.record(
            actor=event.actor,
            event_type=event.event_type,
            inputs=event.inputs,
            outputs=event.outputs,
            context=context_data,
            metadata=event.metadata,
        )

    def on_trace_start(self, trace: Any) -> None:
        self._record_event(
            evidence_from_openai_agents_trace(trace, source_event_type="on_trace_start")
        )

    def on_trace_end(self, trace: Any) -> None:
        self._record_event(
            evidence_from_openai_agents_trace(trace, source_event_type="on_trace_end")
        )

    def on_span_start(self, span: Any) -> None:
        self._record_event(
            evidence_from_openai_agents_span(span, source_event_type="on_span_start")
        )

    def on_span_end(self, span: Any) -> None:
        self._record_event(evidence_from_openai_agents_span(span, source_event_type="on_span_end"))

    def shutdown(self) -> None:
        return None

    def force_flush(self) -> None:
        return None


def install_openai_agents_processor(
    recorder: EvidenceRecorder,
    *,
    replace: bool = False,
    base_tags: list[str] | None = None,
) -> AgentEvidenceTracingProcessor:
    """
    Register an Agent Evidence tracing processor with the OpenAI Agents SDK.

    When `replace` is False, the processor is added alongside the SDK's existing
    processors. When True, it becomes the only active tracing processor.
    """

    if not _HAS_OPENAI_AGENTS:
        raise ModuleNotFoundError(
            "openai-agents is required to install the Agent Evidence trace processor. "
            "Install agent-evidence with the [openai-agents] extra."
        )

    processor = AgentEvidenceTracingProcessor(recorder, base_tags=base_tags)
    if replace:
        _set_trace_processors([processor])
    else:
        _add_trace_processor(processor)
    return processor


def _coerce_mapping(value: Any) -> dict[str, Any]:
    if isinstance(value, Mapping):
        return ensure_json_object(value)
    return {}


def exported_trace_summary(trace: Any) -> dict[str, Any]:
    """Return a stable JSON-safe summary of an OpenAI Agents trace object."""

    payload = _trace_payload(trace)
    return {
        "id": _trace_id(trace, payload),
        "workflow_name": payload.get("workflow_name") or getattr(trace, "name", None),
        "group_id": payload.get("group_id"),
        "metadata": _coerce_mapping(payload.get("metadata")),
    }


def exported_span_summary(span: Any) -> dict[str, Any]:
    """Return a stable JSON-safe summary of an OpenAI Agents span object."""

    payload = _span_payload(span)
    span_data = _span_data(payload)
    return {
        "id": _span_id(span, payload),
        "trace_id": payload.get("trace_id"),
        "parent_id": _span_parent_id(span, payload),
        "type": span_data.get("type"),
        "name": span_data.get("name"),
        "span_data": span_data,
        "error": to_jsonable(payload.get("error")),
        "trace_metadata": _coerce_mapping(getattr(span, "trace_metadata", None)),
    }
