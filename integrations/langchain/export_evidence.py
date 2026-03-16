from __future__ import annotations

import json
from pathlib import Path
from uuid import uuid4

from langchain_core.runnables import RunnableLambda
from langchain_core.tools import tool

from agent_evidence.aep import EvidenceBundleBuilder, verify_bundle
from agent_evidence.integrations import EvidenceCallbackHandler


@tool
def multiply(x: int, y: int) -> int:
    """Multiply two integers."""

    return x * y


def export_langchain_evidence_bundle(output_dir: str | Path) -> Path:
    builder = EvidenceBundleBuilder(
        run_id="langchain-demo-run",
        source_runtime="langchain",
        trace_ref="langchain-demo-run",
        redaction={"omit_request": False, "omit_response": False},
    )
    handler = EvidenceCallbackHandler(bundle_builder=builder, digest_only=True)

    uppercase = RunnableLambda(lambda text: text.upper()).with_config({"run_name": "uppercase"})
    failing = RunnableLambda(
        lambda _: (_ for _ in ()).throw(RuntimeError("demo failure"))
    ).with_config({"run_name": "explode"})

    uppercase.invoke(
        "hello world",
        config={
            "callbacks": [handler],
            "metadata": {"scenario": "quickstart"},
            "tags": ["quickstart"],
        },
    )
    multiply.invoke(
        {"x": 6, "y": 7},
        config={
            "callbacks": [handler],
            "metadata": {"scenario": "quickstart"},
            "tags": ["quickstart"],
        },
    )

    model_run_id = uuid4()
    handler.on_chat_model_start(
        serialized={"name": "mock-model"},
        messages=[[{"type": "human", "content": "hello world"}]],
        run_id=model_run_id,
        name="mock-model",
        metadata={"scenario": "quickstart"},
    )
    handler.on_llm_end(
        {"text": "HELLO WORLD"},
        run_id=model_run_id,
        name="mock-model",
        metadata={"scenario": "quickstart"},
    )

    try:
        failing.invoke(
            "boom",
            config={
                "callbacks": [handler],
                "metadata": {"scenario": "quickstart"},
                "tags": ["quickstart"],
            },
        )
    except RuntimeError:
        pass

    return builder.write_bundle(output_dir)


if __name__ == "__main__":
    destination = Path(__file__).with_name("langchain-evidence-bundle")
    written = export_langchain_evidence_bundle(destination)
    print(written)
    print(json.dumps(verify_bundle(written), indent=2, sort_keys=True))
