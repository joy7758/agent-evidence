from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from uuid import uuid4

from agent_evidence import (
    EvidenceRecorder,
    LocalEvidenceStore,
    export_json_bundle,
    verify_json_bundle,
)

try:
    from cryptography.hazmat.primitives import serialization
    from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
except ModuleNotFoundError as exc:  # pragma: no cover - runtime dependency guard
    raise ModuleNotFoundError(
        "cryptography is required for this example. Install agent-evidence with "
        "the [signing] or [dev] extra."
    ) from exc


DEFAULT_OUTPUT_DIR = (
    Path(__file__).resolve().parent / "artifacts" / "openai-compatible-minimal-evidence"
)
DEFAULT_MOCK_BASE_URL = "mock://openai-compatible/v1"
DEFAULT_MOCK_MODEL = "mock-compatible-model"


@dataclass(frozen=True)
class OpenAICompatibleConfig:
    mode: str
    base_url: str
    model: str
    api_key_configured: bool


def _write_ed25519_keypair(output_dir: Path) -> tuple[Path, Path, bytes, bytes]:
    private_key = Ed25519PrivateKey.generate()
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )
    public_pem = private_key.public_key().public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )
    private_key_path = output_dir / "manifest-private.pem"
    public_key_path = output_dir / "manifest-public.pem"
    private_key_path.write_bytes(private_pem)
    public_key_path.write_bytes(public_pem)
    return private_key_path, public_key_path, private_pem, public_pem


def _digest(value: Any) -> str:
    payload = json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
    ).encode("utf-8")
    return "sha256:" + hashlib.sha256(payload).hexdigest()


def _provider_config(
    *,
    mode: str,
    api_key: str | None,
    base_url: str | None,
    model: str | None,
) -> OpenAICompatibleConfig:
    if mode == "live":
        missing = [
            name
            for name, value in {
                "OPENAI_COMPATIBLE_API_KEY or --api-key": api_key,
                "OPENAI_COMPATIBLE_BASE_URL or --base-url": base_url,
                "OPENAI_COMPATIBLE_MODEL or --model": model,
            }.items()
            if not value
        ]
        if missing:
            raise ValueError(
                "Live mode requires explicit OpenAI-compatible provider config: "
                + ", ".join(missing)
            )
        return OpenAICompatibleConfig(
            mode=mode,
            base_url=str(base_url),
            model=str(model),
            api_key_configured=True,
        )

    return OpenAICompatibleConfig(
        mode="mock",
        base_url=base_url or DEFAULT_MOCK_BASE_URL,
        model=model or DEFAULT_MOCK_MODEL,
        api_key_configured=bool(api_key),
    )


def _mock_chat_completion(config: OpenAICompatibleConfig, messages: list[dict[str, str]]) -> dict:
    request_digest = _digest(messages)
    return {
        "id": f"chatcmpl-mock-{uuid4()}",
        "model": config.model,
        "provider_mode": "mock",
        "choices": [
            {
                "index": 0,
                "finish_reason": "stop",
                "message": {
                    "role": "assistant",
                    "content_digest": request_digest,
                    "summary": "Mock OpenAI-compatible response generated locally.",
                },
            }
        ],
        "usage": {
            "prompt_tokens": 12,
            "completion_tokens": 8,
            "total_tokens": 20,
        },
    }


def _live_chat_completion(
    *,
    api_key: str,
    base_url: str,
    model: str,
    messages: list[dict[str, str]],
) -> dict:
    try:
        from openai import OpenAI
    except ModuleNotFoundError as exc:  # pragma: no cover - live opt-in only
        raise ModuleNotFoundError(
            "openai is required for live OpenAI-compatible calls. Install "
            "agent-evidence with the [openai-compatible] extra."
        ) from exc

    client = OpenAI(api_key=api_key, base_url=base_url)
    completion = client.chat.completions.create(model=model, messages=messages)
    if hasattr(completion, "model_dump"):
        return completion.model_dump(mode="json")
    return json.loads(completion.model_dump_json())


def _record_openai_compatible_run(
    *,
    recorder: EvidenceRecorder,
    config: OpenAICompatibleConfig,
    completion: dict[str, Any],
    messages: list[dict[str, str]],
) -> None:
    run_id = f"openai-compatible-{uuid4()}"
    request_digest = _digest(messages)
    response_digest = _digest(completion)
    common_metadata = {
        "scenario": "openai-compatible-minimal-evidence",
        "mode": config.mode,
        "provider_config": {
            "base_url": config.base_url,
            "model": config.model,
            "api_key_configured": config.api_key_configured,
        },
        "digest_only": True,
    }

    recorder.record(
        actor="openai-compatible-client",
        event_type="run.start",
        inputs={
            "run_id": run_id,
            "provider_interface": "openai-compatible",
            "mode": config.mode,
        },
        context={
            "source": "openai_compatible",
            "component": "client",
            "source_event_type": "run.start",
            "name": "openai-compatible-minimal-evidence",
            "tags": ["cookbook", "local-first", "openai-compatible"],
        },
        metadata=common_metadata,
    )
    recorder.record(
        actor="openai-compatible-client",
        event_type="chat.completion.request",
        inputs={
            "request_digest": request_digest,
            "message_count": len(messages),
            "model": config.model,
            "base_url": config.base_url,
        },
        context={
            "source": "openai_compatible",
            "component": "chat_completion",
            "source_event_type": "request",
            "name": "chat.completions.create",
            "tags": ["cookbook", "local-first", "openai-compatible"],
        },
        metadata=common_metadata,
    )
    recorder.record(
        actor="openai-compatible-client",
        event_type="chat.completion.response",
        outputs={
            "response_digest": response_digest,
            "completion_id": completion.get("id"),
            "model": completion.get("model", config.model),
            "choice_count": len(completion.get("choices", [])),
            "usage": completion.get("usage", {}),
        },
        context={
            "source": "openai_compatible",
            "component": "chat_completion",
            "source_event_type": "response",
            "name": "chat.completions.create",
            "tags": ["cookbook", "local-first", "openai-compatible"],
        },
        metadata=common_metadata,
    )
    recorder.record(
        actor="openai-compatible-client",
        event_type="run.end",
        outputs={
            "run_id": run_id,
            "ok": True,
            "request_digest": request_digest,
            "response_digest": response_digest,
        },
        context={
            "source": "openai_compatible",
            "component": "client",
            "source_event_type": "run.end",
            "name": "openai-compatible-minimal-evidence",
            "tags": ["cookbook", "local-first", "openai-compatible"],
        },
        metadata=common_metadata,
    )


def run_example(
    output_dir: str | Path = DEFAULT_OUTPUT_DIR,
    *,
    mode: str = "mock",
    api_key: str | None = None,
    base_url: str | None = None,
    model: str | None = None,
) -> dict[str, object]:
    config = _provider_config(mode=mode, api_key=api_key, base_url=base_url, model=model)
    output_root = Path(output_dir)
    if output_root.exists():
        shutil.rmtree(output_root)
    output_root.mkdir(parents=True, exist_ok=True)

    store_path = output_root / "runtime-events.jsonl"
    bundle_path = output_root / "openai-compatible-evidence.bundle.json"
    manifest_path = output_root / "openai-compatible-evidence.manifest.json"

    messages = [
        {"role": "system", "content": "Return a concise local demo response."},
        {"role": "user", "content": "Create runtime evidence without using a real provider."},
    ]
    if config.mode == "live":
        completion = _live_chat_completion(
            api_key=api_key or "",
            base_url=config.base_url,
            model=config.model,
            messages=messages,
        )
    else:
        completion = _mock_chat_completion(config, messages)

    store = LocalEvidenceStore(store_path)
    recorder = EvidenceRecorder(store)
    _record_openai_compatible_run(
        recorder=recorder,
        config=config,
        completion=completion,
        messages=messages,
    )

    records = store.list()
    private_key_path, public_key_path, private_pem, public_pem = _write_ed25519_keypair(output_root)
    bundle = export_json_bundle(
        records,
        bundle_path,
        filters={"source": "openai_compatible", "limit": len(records)},
        private_key_pem=private_pem,
        key_id="openai-compatible-cookbook-demo",
        signer="local-demo",
        role="attestor",
        manifest_output_path=manifest_path,
    )
    verify_result = verify_json_bundle(bundle_path, public_key_pem=public_pem)

    verify_command = (
        f"agent-evidence verify-export --bundle {bundle_path} --public-key {public_key_path}"
    )
    summary = {
        "ok": verify_result["ok"],
        "mode": config.mode,
        "output_dir": str(output_root),
        "store_path": str(store_path),
        "bundle_path": str(bundle_path),
        "manifest_path": str(manifest_path),
        "private_key_path": str(private_key_path),
        "public_key_path": str(public_key_path),
        "record_count": len(records),
        "signature_count": len(bundle.signatures),
        "provider_config": {
            "base_url": config.base_url,
            "model": config.model,
            "api_key_configured": config.api_key_configured,
        },
        "verify_command": verify_command,
        "verify_result": verify_result,
        "anchor_note": (
            "Detached anchoring is not implemented in this repository. Use the exported "
            "bundle digest and signed manifest as the handoff point if you want to anchor "
            "it in an external timestamp or registry system."
        ),
    }
    (output_root / "summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return summary


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate a minimal OpenAI-compatible evidence bundle."
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help=f"Directory for generated artifacts. Default: {DEFAULT_OUTPUT_DIR}",
    )
    mode_group = parser.add_mutually_exclusive_group()
    mode_group.add_argument(
        "--mock",
        action="store_true",
        help="Use deterministic local mock behavior. This is the default.",
    )
    mode_group.add_argument(
        "--live",
        action="store_true",
        help="Call a configured OpenAI-compatible provider. Never used by tests.",
    )
    parser.add_argument("--api-key", default=os.getenv("OPENAI_COMPATIBLE_API_KEY"))
    parser.add_argument("--base-url", default=os.getenv("OPENAI_COMPATIBLE_BASE_URL"))
    parser.add_argument("--model", default=os.getenv("OPENAI_COMPATIBLE_MODEL"))
    args = parser.parse_args()

    mode = "live" if args.live else "mock"
    try:
        summary = run_example(
            args.output_dir,
            mode=mode,
            api_key=args.api_key,
            base_url=args.base_url,
            model=args.model,
        )
    except ValueError as exc:
        print(
            json.dumps(
                {
                    "ok": False,
                    "error": {
                        "code": "invalid_provider_config",
                        "message": str(exc),
                    },
                },
                indent=2,
                sort_keys=True,
            )
        )
        return 2
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0 if summary["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
