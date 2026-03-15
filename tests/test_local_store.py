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
