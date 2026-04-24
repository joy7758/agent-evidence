from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from agent_evidence.crypto.chain import verify_chain
from agent_evidence.recorder import EvidenceRecorder
from agent_evidence.storage.local import LocalEvidenceStore


def _assert_single_linear_chain(records: list, expected_count: int) -> None:
    assert len(records) == expected_count
    assert verify_chain(records) == []

    genesis_records = [record for record in records if record.hashes.previous_event_hash is None]
    assert len(genesis_records) == 1

    previous_hashes = [
        record.hashes.previous_event_hash
        for record in records
        if record.hashes.previous_event_hash is not None
    ]
    assert len(previous_hashes) == len(set(previous_hashes))

    records_by_event_hash = {record.hashes.event_hash: record for record in records}
    assert len(records_by_event_hash) == expected_count

    visited: set[str] = set()
    cursor = records[-1]
    while True:
        event_hash = cursor.hashes.event_hash
        assert event_hash not in visited
        visited.add(event_hash)

        previous_event_hash = cursor.hashes.previous_event_hash
        if previous_event_hash is None:
            break
        assert previous_event_hash in records_by_event_hash
        cursor = records_by_event_hash[previous_event_hash]

    assert len(visited) == expected_count


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
    assert store.latest_hashes() == (second.hashes.event_hash, second.hashes.chain_hash)


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


def test_local_store_record_is_atomic_for_multithreaded_appends(tmp_path: Path) -> None:
    store = LocalEvidenceStore(tmp_path / "concurrent.evidence.jsonl")
    recorder = EvidenceRecorder(store)
    record_count = 32

    def record_event(index: int) -> str:
        envelope = recorder.record(
            actor=f"worker-{index}",
            event_type="concurrent.local",
            inputs={"index": index},
        )
        return envelope.hashes.event_hash

    with ThreadPoolExecutor(max_workers=8) as executor:
        event_hashes = list(executor.map(record_event, range(record_count)))

    assert len(event_hashes) == record_count
    assert len(set(event_hashes)) == record_count
    _assert_single_linear_chain(store.list(), record_count)
