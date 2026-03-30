from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path
from uuid import uuid4

from agent_evidence import (
    EvidenceRecorder,
    LocalEvidenceStore,
    export_json_bundle,
    verify_json_bundle,
)
from agent_evidence.integrations import EvidenceCallbackHandler

try:
    from cryptography.hazmat.primitives import serialization
    from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
except ModuleNotFoundError as exc:  # pragma: no cover - runtime dependency guard
    raise ModuleNotFoundError(
        "cryptography is required for this example. Install agent-evidence with "
        "the [signing] or [dev] extra."
    ) from exc

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


def run_example(output_dir: str | Path = DEFAULT_OUTPUT_DIR) -> dict[str, object]:
    output_root = Path(output_dir)
    if output_root.exists():
        shutil.rmtree(output_root)
    output_root.mkdir(parents=True, exist_ok=True)

    store_path = output_root / "runtime-events.jsonl"
    bundle_path = output_root / "langchain-evidence.bundle.json"
    manifest_path = output_root / "langchain-evidence.manifest.json"

    store = LocalEvidenceStore(store_path)
    recorder = EvidenceRecorder(store)
    handler = EvidenceCallbackHandler(recorder=recorder, base_tags=["cookbook", "local-first"])

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

    records = store.list()
    private_key_path, public_key_path, private_pem, public_pem = _write_ed25519_keypair(output_root)

    bundle = export_json_bundle(
        records,
        bundle_path,
        filters={"source": "langchain", "limit": len(records)},
        private_key_pem=private_pem,
        key_id="langchain-cookbook-demo",
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
        "output_dir": str(output_root),
        "store_path": str(store_path),
        "bundle_path": str(bundle_path),
        "manifest_path": str(manifest_path),
        "private_key_path": str(private_key_path),
        "public_key_path": str(public_key_path),
        "record_count": len(records),
        "signature_count": len(bundle.signatures),
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
