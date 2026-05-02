import asyncio
import importlib.util
import json
import os
import subprocess
import sys
from pathlib import Path
from uuid import uuid4

import pytest
from langchain_core.runnables import RunnableLambda
from langchain_core.tools import tool

from agent_evidence.aep import EvidenceBundleBuilder, load_bundle_payload, verify_bundle
from agent_evidence.integrations import (
    EvidenceCallbackHandler,
    evidence_from_langchain_event,
    record_langchain_event,
)
from agent_evidence.recorder import EvidenceRecorder
from agent_evidence.storage.local import LocalEvidenceStore

ROOT = Path(__file__).resolve().parents[1]


def _load_langchain_minimal_example():
    example_path = ROOT / "examples" / "langchain_minimal_evidence.py"
    spec = importlib.util.spec_from_file_location(
        "langchain_minimal_evidence_example",
        example_path,
    )
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


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
    event_types = [record.event.event_type for record in records]
    assert "chain.start" in event_types
    assert "chain.end" in event_types
    assert "tool.start" in event_types
    assert "tool.end" in event_types

    chain_start = next(record for record in records if record.event.event_type == "chain.start")
    assert chain_start.event.inputs["input"] == "hello"
    assert chain_start.event.metadata["session_id"] == "chain-demo"
    assert "baseline" in chain_start.event.context.tags
    assert "langchain" in chain_start.event.context.tags
    assert chain_start.event.context.source_event_type == "on_chain_start"

    tool_end = next(record for record in records if record.event.event_type == "tool.end")
    assert tool_end.event.outputs["x"] == "1"
    assert tool_end.event.context.component == "tool"


def test_stream_event_adapter_matches_v2_event_shape(tmp_path: Path) -> None:
    async def collect_events() -> list[dict]:
        chain = RunnableLambda(lambda text: text[::-1]).with_config({"run_name": "reverse"})
        return [event async for event in chain.astream_events("hello", version="v2")]

    events = asyncio.run(collect_events())
    start_event = next(event for event in events if event["event"] == "on_chain_start")
    end_event = next(event for event in events if event["event"] == "on_chain_end")

    evidence_event = evidence_from_langchain_event(start_event)
    assert evidence_event.actor == "reverse"
    assert evidence_event.event_type == "chain.start"
    assert evidence_event.inputs["input"] == "hello"
    assert evidence_event.context.component == "chain"
    assert evidence_event.context.source_event_type == "on_chain_start"

    store = LocalEvidenceStore(tmp_path / "stream.evidence.jsonl")
    recorder = EvidenceRecorder(store)
    record_langchain_event(recorder, end_event)

    [record] = store.list()
    assert record.event.event_type == "chain.end"
    assert record.event.outputs["output"] == "olleh"


def test_callback_handler_writes_digest_only_profile_bundle(tmp_path: Path) -> None:
    builder = EvidenceBundleBuilder(
        run_id="langchain-profile-run",
        source_runtime="langchain",
        trace_ref="langchain-profile-run",
        redaction={"omit_request": False, "omit_response": False},
    )
    handler = EvidenceCallbackHandler(
        bundle_builder=builder,
        base_tags=["baseline"],
        digest_only=True,
    )

    chain = RunnableLambda(lambda text: text.upper()).with_config({"run_name": "uppercase"})

    @tool
    def pair(x: int, y: str) -> dict[str, str]:
        """Return the provided inputs."""

        return {"x": str(x), "y": y}

    failing = RunnableLambda(lambda _: (_ for _ in ()).throw(RuntimeError("boom"))).with_config(
        {"run_name": "explode"}
    )

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
    model_run_id = uuid4()
    handler.on_chat_model_start(
        serialized={"name": "mock-model"},
        messages=[[{"type": "human", "content": "hello"}]],
        run_id=model_run_id,
        name="mock-model",
        metadata={"session_id": "model-demo"},
    )
    handler.on_llm_end(
        {"text": "HELLO"},
        run_id=model_run_id,
        name="mock-model",
        metadata={"session_id": "model-demo"},
    )
    with pytest.raises(RuntimeError):
        failing.invoke(
            "boom",
            config={
                "callbacks": [handler],
                "metadata": {"session_id": "error-demo"},
                "tags": ["demo"],
            },
        )

    bundle_dir = builder.write_bundle(tmp_path / "bundle")
    report = verify_bundle(bundle_dir)
    payload = load_bundle_payload(bundle_dir)

    assert report["ok"] is True
    event_types = [record["event_type"] for record in payload["records"]]
    assert "chain.start" in event_types
    assert "chain.end" in event_types
    assert "tool.start" in event_types
    assert "tool.end" in event_types
    assert "chat_model.start" in event_types
    assert "llm.end" in event_types
    assert "chain.error" in event_types

    for record in payload["records"]:
        request = record["payload"].get("request", {})
        response = record["payload"].get("response", {})
        assert "content" not in request
        assert "content" not in response

    tool_record = next(
        record for record in payload["records"] if record["event_type"] == "tool.end"
    )
    assert tool_record["payload"]["attributes"]["openinference"]["span_kind"] == "TOOL"


def test_langchain_minimal_evidence_example_smoke(tmp_path: Path) -> None:
    module = _load_langchain_minimal_example()

    summary = module.run_example(tmp_path / "langchain-minimal-evidence")

    assert summary["ok"] is True
    assert summary["record_count"] >= 6
    assert Path(summary["store_path"]).exists()
    assert Path(summary["bundle_path"]).exists()
    assert Path(summary["manifest_path"]).exists()
    assert Path(summary["public_key_path"]).exists()
    assert summary["verify_result"]["ok"] is True


def test_langchain_minimal_evidence_subprocess_and_cli_verify(tmp_path: Path) -> None:
    output_dir = tmp_path / "langchain-minimal-evidence"
    env = os.environ.copy()
    for name in [
        "ANTHROPIC_API_KEY",
        "GOOGLE_API_KEY",
        "LANGCHAIN_API_KEY",
        "MISTRAL_API_KEY",
        "OPENAI_API_KEY",
    ]:
        env.pop(name, None)

    result = subprocess.run(
        [
            sys.executable,
            "examples/langchain_minimal_evidence.py",
            "--output-dir",
            str(output_dir),
        ],
        cwd=ROOT,
        env=env,
        check=True,
        capture_output=True,
        text=True,
    )
    payload = json.loads(result.stdout)
    assert payload["ok"] is True

    expected_files = [
        "runtime-events.jsonl",
        "langchain-evidence.bundle.json",
        "langchain-evidence.manifest.json",
        "manifest-private.pem",
        "manifest-public.pem",
        "summary.json",
    ]
    for filename in expected_files:
        assert (output_dir / filename).exists(), filename

    summary = json.loads((output_dir / "summary.json").read_text(encoding="utf-8"))
    bundle_path = output_dir / "langchain-evidence.bundle.json"
    public_key_path = output_dir / "manifest-public.pem"
    agent_evidence_cli = Path(sys.executable).with_name("agent-evidence")
    assert agent_evidence_cli.exists()
    verify_result = subprocess.run(
        [
            str(agent_evidence_cli),
            "verify-export",
            "--bundle",
            str(bundle_path),
            "--public-key",
            str(public_key_path),
        ],
        cwd=ROOT,
        env=env,
        check=True,
        capture_output=True,
        text=True,
    )
    verify_payload = json.loads(verify_result.stdout)
    assert verify_payload["ok"] is True
    assert summary["verify_result"]["ok"] is True
    assert summary["verify_command"].startswith("agent-evidence verify-export")


def test_langchain_minimal_cookbook_references_runnable_path() -> None:
    text = (ROOT / "docs/cookbooks/langchain_minimal_evidence.md").read_text(encoding="utf-8")

    for required in [
        "examples/langchain_minimal_evidence.py",
        "agent-evidence verify-export",
        "summary.json",
        "runtime-events.jsonl",
        "langchain-evidence.bundle.json",
    ]:
        assert required in text
