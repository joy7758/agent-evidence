from __future__ import annotations

import json
from pathlib import Path
from uuid import uuid4

from langchain_core.runnables import RunnableLambda
from langchain_core.tools import tool

from agent_evidence.integrations.langchain import (
    EvidenceCallbackHandler,
    LangChainAdapter,
)


@tool
def multiply(x: int, y: int) -> int:
    """Multiply two integers."""

    return x * y


def test_langchain_adapter_finalize_writes_normalized_artifacts(tmp_path: Path) -> None:
    adapter = LangChainAdapter.for_output_dir(
        tmp_path / "langchain-run",
        digest_only=True,
        omit_request=False,
        omit_response=False,
        base_tags=["baseline"],
    )
    handler = adapter.callback_handler()

    uppercase = RunnableLambda(lambda text: text.upper()).with_config({"run_name": "uppercase"})
    run_config = {
        "callbacks": [handler],
        "metadata": {"scenario": "langchain-adapter-test"},
        "tags": ["baseline"],
    }

    uppercase.invoke("hello world", config=run_config)
    multiply.invoke({"x": 6, "y": 7}, config=run_config)

    model_run_id = uuid4()
    handler.on_chat_model_start(
        serialized={"name": "mock-model"},
        messages=[[{"type": "human", "content": "hello world"}]],
        run_id=model_run_id,
        name="mock-model",
        metadata={"scenario": "langchain-adapter-test"},
    )
    handler.on_llm_end(
        {"text": "HELLO WORLD"},
        run_id=model_run_id,
        name="mock-model",
        metadata={"scenario": "langchain-adapter-test"},
    )

    artifacts = adapter.finalize()

    assert artifacts.bundle_path.exists()
    assert artifacts.receipt_path.exists()
    assert artifacts.summary_path.exists()
    assert artifacts.receipt["ok"] is True
    assert artifacts.summary["ok"] is True
    assert artifacts.summary["receipt_path"] == str(artifacts.receipt_path)
    assert artifacts.summary["bundle_path"] == str(artifacts.bundle_path)
    assert artifacts.summary["verify_result"] == artifacts.receipt
    assert artifacts.supporting_files["manifest"].exists()
    assert artifacts.supporting_files["public_key"].exists()
    assert artifacts.supporting_files["private_key"].exists()
    assert artifacts.supporting_files["runtime_events"].exists()

    written_receipt = json.loads(artifacts.receipt_path.read_text(encoding="utf-8"))
    written_summary = json.loads(artifacts.summary_path.read_text(encoding="utf-8"))
    assert written_receipt == artifacts.receipt
    assert written_summary == artifacts.summary


def test_langchain_adapter_reuses_handler_and_finalize_result(tmp_path: Path) -> None:
    adapter = LangChainAdapter.for_output_dir(tmp_path / "langchain-run")

    first_handler = adapter.callback_handler()
    second_handler = adapter.callback_handler()

    assert isinstance(first_handler, EvidenceCallbackHandler)
    assert first_handler is second_handler

    chain = RunnableLambda(lambda text: text.upper()).with_config({"run_name": "uppercase"})
    chain.invoke("hello", config={"callbacks": [first_handler]})

    first_artifacts = adapter.finalize()
    second_artifacts = adapter.finalize()

    assert first_artifacts is second_artifacts
    assert first_artifacts.receipt["ok"] is True
