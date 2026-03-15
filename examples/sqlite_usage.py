from pathlib import Path

from agent_evidence import EvidenceRecorder
from agent_evidence.storage.sql import SqlEvidenceStore


def main() -> None:
    db_url = f"sqlite+pysqlite:///{Path('examples') / 'demo.evidence.db'}"
    store = SqlEvidenceStore(db_url)
    recorder = EvidenceRecorder(store)

    recorder.record(
        actor="planner",
        event_type="tool.call",
        context={"source": "example", "component": "tool"},
        inputs={"tool": "search", "query": "sql evidence backend"},
        metadata={"session_id": "sqlite-demo"},
    )

    recorder.record(
        actor="planner",
        event_type="tool.end",
        context={"source": "example", "component": "tool"},
        outputs={"status": "ok"},
        metadata={"session_id": "sqlite-demo"},
    )

    for envelope in store.query(source="example", component="tool"):
        print(envelope.model_dump_json(indent=2))


if __name__ == "__main__":
    main()
