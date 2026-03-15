import asyncio
from pathlib import Path

from langchain_core.runnables import RunnableLambda
from langchain_core.tools import tool

from agent_evidence.integrations import (
    EvidenceCallbackHandler,
    evidence_from_langchain_event,
    record_langchain_event,
)
from agent_evidence.recorder import EvidenceRecorder
from agent_evidence.storage.local import LocalEvidenceStore


def test_callback_handler_records_chain_and_tool_runs(tmp_path: Path) -> None:
    store = LocalEvidenceStore(tmp_path / "evidence.jsonl")
    recorder = EvidenceRecorder(store)
    handler = EvidenceCallbackHandler(recorder, base_tags=["baseline"])

    chain = RunnableLambda(lambda text: text.upper()).with_config({"run_name": "uppercase"})

    @tool
    def pair(x: int, y: str) -> dict[str, str]:
        """Return the provided inputs."""

        return {"x": str(x), "y": y}

    chain.invoke(
        "hello",
        config={
            "callbacks": [handler],
            "metadata": {"session_id": "chain-demo"},
            "tags": ["demo"],
        },
    )
    pair.invoke(
        {"x": 1, "y": "2"},
        config={
            "callbacks": [handler],
            "metadata": {"session_id": "tool-demo"},
            "tags": ["demo"],
        },
    )

    records = store.list()
    actions = [record.payload.action for record in records]
    assert "on_chain_start" in actions
    assert "on_chain_end" in actions
    assert "on_tool_start" in actions
    assert "on_tool_end" in actions

    chain_start = next(record for record in records if record.payload.action == "on_chain_start")
    assert chain_start.payload.inputs["input"] == "hello"
    assert chain_start.payload.metadata["session_id"] == "chain-demo"
    assert "baseline" in chain_start.payload.tags
    assert "langchain" in chain_start.payload.tags

    tool_end = next(record for record in records if record.payload.action == "on_tool_end")
    assert tool_end.payload.outputs["x"] == "1"
    assert tool_end.payload.metadata["_langchain"]["component"] == "tool"


def test_stream_event_adapter_matches_v2_event_shape(tmp_path: Path) -> None:
    async def collect_events() -> list[dict]:
        chain = RunnableLambda(lambda text: text[::-1]).with_config({"run_name": "reverse"})
        return [event async for event in chain.astream_events("hello", version="v2")]

    events = asyncio.run(collect_events())
    start_event = next(event for event in events if event["event"] == "on_chain_start")
    end_event = next(event for event in events if event["event"] == "on_chain_end")

    payload = evidence_from_langchain_event(start_event)
    assert payload.actor == "reverse"
    assert payload.action == "on_chain_start"
    assert payload.inputs["input"] == "hello"
    assert payload.metadata["_langchain"]["component"] == "chain"

    store = LocalEvidenceStore(tmp_path / "stream.evidence.jsonl")
    recorder = EvidenceRecorder(store)
    record_langchain_event(recorder, end_event)

    [record] = store.list()
    assert record.payload.action == "on_chain_end"
    assert record.payload.outputs["output"] == "olleh"
