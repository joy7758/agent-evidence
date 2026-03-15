from pathlib import Path

from agent_evidence.recorder import EvidenceRecorder
from agent_evidence.storage.local import LocalEvidenceStore


def test_local_store_appends_chain(tmp_path: Path) -> None:
    store = LocalEvidenceStore(tmp_path / "evidence.jsonl")
    recorder = EvidenceRecorder(store)

    first = recorder.record(actor="planner", action="draft")
    second = recorder.record(actor="executor", action="run")

    records = store.list()
    assert len(records) == 2
    assert records[0].chain_digest == first.chain_digest
    assert records[1].previous_digest == first.chain_digest
    assert second.chain_digest == records[1].chain_digest
