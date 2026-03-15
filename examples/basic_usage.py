from pathlib import Path

from agent_evidence import EvidenceRecorder, LocalEvidenceStore


def main() -> None:
    store = LocalEvidenceStore(Path("examples") / "demo.evidence.jsonl")
    recorder = EvidenceRecorder(store)

    envelope = recorder.record(
        actor="planner",
        action="tool_call",
        inputs={"tool": "search", "query": "agent observability"},
        outputs={"status": "ok", "documents": 3},
        metadata={"session_id": "demo-session"},
        tags=["example", "demo"],
    )

    print(envelope.model_dump_json(indent=2))


if __name__ == "__main__":
    main()
