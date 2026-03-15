from pathlib import Path

from agent_evidence.crypto.chain import verify_chain
from agent_evidence.recorder import EvidenceRecorder
from agent_evidence.storage.local import LocalEvidenceStore


def test_local_store_appends_chain(tmp_path: Path) -> None:
    store = LocalEvidenceStore(tmp_path / "evidence.jsonl")
    recorder = EvidenceRecorder(store)

    first = recorder.record(actor="planner", event_type="plan.draft")
    second = recorder.record(actor="executor", event_type="execution.run")

    records = store.list()
    assert len(records) == 2
    assert records[0].hashes.chain_hash == first.hashes.chain_hash
    assert records[1].hashes.previous_event_hash == first.hashes.event_hash
    assert second.hashes.chain_hash == records[1].hashes.chain_hash


def test_verify_chain_detects_tampering(tmp_path: Path) -> None:
    store = LocalEvidenceStore(tmp_path / "evidence.jsonl")
    recorder = EvidenceRecorder(store)

    recorder.record(actor="planner", event_type="plan.draft")
    recorder.record(actor="executor", event_type="execution.run")

    records = store.list()
    assert verify_chain(records) == []

    records[1].event.actor = "tampered"
    issues = verify_chain(records)
    assert "record 1: event_hash mismatch" in issues


def test_local_store_query_supports_span_hash_and_pagination(tmp_path: Path) -> None:
    store = LocalEvidenceStore(tmp_path / "evidence.jsonl")
    recorder = EvidenceRecorder(store)

    root = recorder.record(
        actor="planner",
        event_type="chain.start",
        context={"source": "langchain", "component": "chain", "span_id": "root"},
    )
    tool_call = recorder.record(
        actor="planner",
        event_type="tool.call",
        context={
            "source": "langchain",
            "component": "tool",
            "span_id": "tool-1",
            "parent_span_id": "root",
        },
    )
    tool_end = recorder.record(
        actor="planner",
        event_type="tool.end",
        context={
            "source": "langchain",
            "component": "tool",
            "span_id": "tool-1",
            "parent_span_id": "root",
        },
    )

    span_records = store.query(span_id="tool-1")
    assert [record.event.event_type for record in span_records] == ["tool.call", "tool.end"]

    child_records = store.query(parent_span_id="root")
    assert [record.event.event_type for record in child_records] == ["tool.call", "tool.end"]

    [linked] = store.query(previous_event_hash=root.hashes.event_hash)
    assert linked.event.event_id == tool_call.event.event_id

    lower, upper = sorted([tool_call.hashes.event_hash, tool_end.hashes.event_hash])
    expected_range = [
        record for record in store.list() if lower <= record.hashes.event_hash <= upper
    ]
    ranged = store.query(event_hash_from=lower, event_hash_to=upper)
    assert [record.event.event_id for record in ranged] == [
        record.event.event_id for record in expected_range
    ]

    paged = store.query(offset=1, limit=1)
    assert [record.event.event_type for record in paged] == ["tool.call"]
