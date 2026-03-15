from __future__ import annotations

from pathlib import Path

import pytest
from agents import set_trace_processors, trace
from agents.tracing import custom_span

from agent_evidence.integrations import (
    AgentEvidenceTracingProcessor,
    exported_span_summary,
    exported_trace_summary,
    install_openai_agents_processor,
)
from agent_evidence.recorder import EvidenceRecorder
from agent_evidence.storage.local import LocalEvidenceStore


def test_processor_records_trace_and_span_lifecycle(tmp_path: Path) -> None:
    set_trace_processors([])

    store = LocalEvidenceStore(tmp_path / "evidence.jsonl")
    recorder = EvidenceRecorder(store)
    processor = AgentEvidenceTracingProcessor(recorder, base_tags=["sdk-test"])

    with trace(
        "agent-evidence-sdk-demo",
        group_id="sdk-session",
        metadata={"session_id": "sdk-session", "environment": "test"},
    ) as current_trace:
        processor.on_trace_start(current_trace)
        with custom_span("collect_context", {"phase": "input"}) as current_span:
            processor.on_span_start(current_span)
        processor.on_span_end(current_span)
    processor.on_trace_end(current_trace)

    records = store.list()
    assert [record.event.event_type for record in records] == [
        "trace.start",
        "span.start",
        "span.end",
        "trace.end",
    ]

    trace_start, span_start, span_end, trace_end = records
    assert trace_start.event.actor == "agent-evidence-sdk-demo"
    assert trace_start.event.inputs["workflow_name"] == "agent-evidence-sdk-demo"
    assert trace_start.event.metadata["session_id"] == "sdk-session"
    assert trace_start.event.context.source == "openai_agents"
    assert trace_start.event.context.component == "trace"
    assert trace_start.event.context.source_event_type == "on_trace_start"
    assert "sdk-test" in trace_start.event.context.tags

    assert span_start.event.actor == "collect_context"
    assert span_start.event.context.component == "custom"
    assert span_start.event.context.source_event_type == "on_span_start"
    assert span_start.event.context.attributes["trace_id"] == trace_start.event.context.span_id
    assert span_start.event.metadata["span_data"]["data"]["phase"] == "input"
    assert span_start.event.metadata["trace_metadata"]["session_id"] == "sdk-session"

    assert span_end.event.outputs["span_data"]["name"] == "collect_context"
    assert span_end.event.context.span_id == span_start.event.context.span_id
    assert span_end.event.context.attributes["ended_at"] is not None

    assert trace_end.event.outputs["group_id"] == "sdk-session"
    assert trace_end.event.context.span_id == trace_start.event.context.span_id


def test_exported_summaries_are_json_safe() -> None:
    set_trace_processors([])

    with trace(
        "agent-evidence-summary-demo",
        group_id="summary-session",
        metadata={"session_id": "summary-session"},
    ) as current_trace:
        with custom_span("summarize_bundle", {"format": "json"}) as current_span:
            trace_summary = exported_trace_summary(current_trace)
            span_summary = exported_span_summary(current_span)

    assert trace_summary["workflow_name"] == "agent-evidence-summary-demo"
    assert trace_summary["group_id"] == "summary-session"
    assert trace_summary["metadata"]["session_id"] == "summary-session"

    assert span_summary["trace_id"] == trace_summary["id"]
    assert span_summary["type"] == "custom"
    assert span_summary["name"] == "summarize_bundle"
    assert span_summary["span_data"]["data"]["format"] == "json"
    assert span_summary["trace_metadata"]["session_id"] == "summary-session"
    assert span_summary["error"] is None


def test_install_openai_agents_processor_registers_with_sdk(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    store = LocalEvidenceStore(tmp_path / "evidence.jsonl")
    recorder = EvidenceRecorder(store)
    added: list[AgentEvidenceTracingProcessor] = []
    replaced: list[list[AgentEvidenceTracingProcessor]] = []

    monkeypatch.setattr("agent_evidence.integrations.openai_agents._HAS_OPENAI_AGENTS", True)
    monkeypatch.setattr(
        "agent_evidence.integrations.openai_agents._add_trace_processor",
        lambda processor: added.append(processor),
    )
    monkeypatch.setattr(
        "agent_evidence.integrations.openai_agents._set_trace_processors",
        lambda processors: replaced.append(list(processors)),
    )

    installed = install_openai_agents_processor(recorder, base_tags=["default"])
    replaced_processor = install_openai_agents_processor(
        recorder,
        replace=True,
        base_tags=["replacement"],
    )

    assert isinstance(installed, AgentEvidenceTracingProcessor)
    assert isinstance(replaced_processor, AgentEvidenceTracingProcessor)
    assert added == [installed]
    assert replaced == [[replaced_processor]]
    assert installed.base_tags == ["default"]
    assert replaced_processor.base_tags == ["replacement"]
