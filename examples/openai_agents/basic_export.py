from pathlib import Path

from agents import trace
from agents.tracing import custom_span

from agent_evidence import export_json_bundle, verify_json_bundle
from agent_evidence.integrations import install_openai_agents_processor
from agent_evidence.recorder import EvidenceRecorder
from agent_evidence.storage.local import LocalEvidenceStore


def main() -> None:
    output_dir = Path("examples") / "openai_agents"
    output_dir.mkdir(parents=True, exist_ok=True)

    store = LocalEvidenceStore(output_dir / "demo.evidence.jsonl")
    recorder = EvidenceRecorder(store)
    install_openai_agents_processor(recorder, replace=True, base_tags=["example", "openai_agents"])

    with trace(
        "agent-evidence-openai-agents-demo",
        group_id="demo-session",
        metadata={"session_id": "demo-session", "example": True},
    ):
        with custom_span("collect_requirements", {"phase": "input"}):
            pass
        with custom_span("package_evidence", {"format": "json"}):
            pass

    bundle_path = output_dir / "demo.bundle.json"
    export_json_bundle(
        store.list(),
        bundle_path,
        filters={"source": "openai_agents"},
    )

    print(f"Evidence store: {store.path}")
    print(f"Bundle: {bundle_path}")
    print(verify_json_bundle(bundle_path))


if __name__ == "__main__":
    main()
