from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

from agent_evidence.integrations.openai_compatible import OpenAICompatibleAdapter

DEFAULT_OUTPUT_DIR = (
    Path(__file__).resolve().parents[1] / "artifacts" / "openai-compatible-alt-base-url"
)
DEFAULT_MODEL = "gpt-4.1-mini"
DEFAULT_PROMPT = "Reply with exactly: hello from an OpenAI-compatible base URL."


def _require_env(name: str) -> str:
    value = os.environ.get(name)
    if value:
        return value
    raise RuntimeError(
        f"{name} is required for this example. Export it in your shell before running."
    )


def _build_client(*, api_key: str, base_url: str):
    try:
        from openai import OpenAI
    except ModuleNotFoundError as exc:  # pragma: no cover - depends on local environment
        raise ModuleNotFoundError(
            "The `openai` package is required for this example. Install it locally with "
            "`pip install openai`."
        ) from exc
    return OpenAI(api_key=api_key, base_url=base_url)


def run_example(output_dir: str | Path = DEFAULT_OUTPUT_DIR) -> dict[str, object]:
    api_key = _require_env("OPENAI_API_KEY")
    base_url = _require_env("OPENAI_COMPAT_BASE_URL")
    provider_label = _require_env("OPENAI_COMPAT_PROVIDER_LABEL")
    model = os.environ.get("OPENAI_MODEL", DEFAULT_MODEL)
    prompt = os.environ.get("OPENAI_PROMPT", DEFAULT_PROMPT)

    client = _build_client(api_key=api_key, base_url=base_url)
    adapter = OpenAICompatibleAdapter.for_output_dir(
        output_dir,
        provider_label=provider_label,
        model=model,
        api_key=api_key,
        base_url=base_url,
        digest_only=True,
        omit_request=False,
        omit_response=False,
        base_tags=["example", "openai-compatible"],
    )

    response = adapter.record_call(
        operation="chat.completions.create",
        request={
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "base_url": base_url,
            "provider_label": provider_label,
        },
        invoke=lambda: client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
        ),
        metadata={"example": "alternate_base_url"},
        tags=["alternate-base-url"],
    )

    artifacts = adapter.finalize()
    summary = dict(artifacts.summary)
    summary["response_id"] = getattr(response, "id", None)
    summary["provider_operation"] = "chat.completions.create"
    return summary


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run a minimal OpenAI-compatible export against an alternate base URL."
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
