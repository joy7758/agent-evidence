from __future__ import annotations

import argparse
import json
from pathlib import Path
from uuid import uuid4

from agent_evidence.integrations import LangChainAdapter

try:
    from langchain_core.runnables import RunnableLambda
    from langchain_core.tools import tool
except ModuleNotFoundError as exc:  # pragma: no cover - runtime dependency guard
    raise ModuleNotFoundError(
        "langchain-core is required for this example. Install agent-evidence with "
        "the [langchain] or [dev] extra."
    ) from exc


DEFAULT_OUTPUT_DIR = Path(__file__).resolve().parent / "artifacts" / "langchain-minimal-evidence"


@tool
def multiply(x: int, y: int) -> int:
    """Multiply two integers."""

    return x * y


def run_example(output_dir: str | Path = DEFAULT_OUTPUT_DIR) -> dict[str, object]:
    adapter = LangChainAdapter.for_output_dir(
        output_dir,
        digest_only=True,
        omit_request=False,
        omit_response=False,
        base_tags=["cookbook", "local-first"],
        key_id="langchain-cookbook-demo",
        signer="local-demo",
        role="attestor",
    )
    handler = adapter.callback_handler()

    uppercase = RunnableLambda(lambda text: text.upper()).with_config({"run_name": "uppercase"})
    failing = RunnableLambda(
        lambda _: (_ for _ in ()).throw(RuntimeError("demo failure"))
    ).with_config({"run_name": "explode"})

    run_config = {
        "callbacks": [handler],
        "metadata": {"scenario": "langchain-minimal-evidence"},
        "tags": ["cookbook", "local-first"],
    }

    uppercase.invoke("hello world", config=run_config)
    multiply.invoke({"x": 6, "y": 7}, config=run_config)

    # Simulate a model step without requiring any external model provider.
    model_run_id = uuid4()
    handler.on_chat_model_start(
        serialized={"name": "mock-model"},
        messages=[[{"type": "human", "content": "hello world"}]],
        run_id=model_run_id,
        name="mock-model",
        metadata={"scenario": "langchain-minimal-evidence"},
    )
    handler.on_llm_end(
        {"text": "HELLO WORLD"},
        run_id=model_run_id,
        name="mock-model",
        metadata={"scenario": "langchain-minimal-evidence"},
    )

    try:
        failing.invoke("boom", config=run_config)
    except RuntimeError:
        pass

    artifacts = adapter.finalize()
    return artifacts.summary


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate a minimal local-first LangChain evidence bundle."
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help=f"Directory for generated artifacts. Default: {DEFAULT_OUTPUT_DIR}",
    )
    args = parser.parse_args()

    summary = run_example(args.output_dir)
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0 if summary["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
