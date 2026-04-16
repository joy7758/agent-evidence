from __future__ import annotations

import json
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Mapping, TypeVar
from uuid import uuid4

from agent_evidence.aep.hash_chain import sha256_digest
from agent_evidence.export import export_json_bundle, verify_json_bundle
from agent_evidence.models import EvidenceContext
from agent_evidence.recorder import EvidenceRecorder
from agent_evidence.serialization import ensure_json_object, to_jsonable
from agent_evidence.storage import LocalEvidenceStore

T = TypeVar("T")


@dataclass(frozen=True)
class OpenAICompatibleArtifacts:
    """Normalized OpenAI-compatible integration outputs plus supporting files."""

    bundle_path: Path
    receipt: dict[str, Any]
    receipt_path: Path
    summary: dict[str, Any]
    summary_path: Path
    supporting_files: dict[str, Path]


def _load_ed25519_runtime():
    try:
        from cryptography.hazmat.primitives import serialization
        from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
    except ModuleNotFoundError as exc:  # pragma: no cover - depends on extras
        raise ModuleNotFoundError(
            "OpenAICompatibleAdapter signing requires cryptography. Install agent-evidence "
            "with the [signing] or [dev] extra."
        ) from exc

    return serialization, Ed25519PrivateKey


def _write_adapter_keypair(
    output_dir: Path,
    *,
    private_key_pem: bytes | None = None,
) -> tuple[Path, Path, bytes, bytes]:
    serialization, Ed25519PrivateKey = _load_ed25519_runtime()
    if private_key_pem is None:
        private_key = Ed25519PrivateKey.generate()
    else:
        loaded = serialization.load_pem_private_key(private_key_pem, password=None)
        if not isinstance(loaded, Ed25519PrivateKey):
            raise TypeError(
                "OpenAICompatibleAdapter requires an Ed25519 private key in PEM format."
            )
        private_key = loaded

    resolved_private_pem = private_key.private_bytes(
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
    private_key_path.write_bytes(resolved_private_pem)
    public_key_path.write_bytes(public_pem)
    return private_key_path, public_key_path, resolved_private_pem, public_pem


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _merge_tags(*parts: list[str] | tuple[str, ...] | None) -> list[str]:
    merged: list[str] = []
    for part in parts:
        for tag in part or []:
            tag_text = str(tag)
            if tag_text and tag_text not in merged:
                merged.append(tag_text)
    return merged


def _payload_slot(value: Any, *, digest_only: bool, omit: bool) -> dict[str, Any]:
    if omit:
        return {"mode": "omitted"}

    normalized = to_jsonable(value)
    if normalized is None or normalized == {} or normalized == []:
        return {"mode": "absent"}

    slot = {
        "mode": "digest_only" if digest_only else "inline",
        "digest": sha256_digest(normalized),
    }
    if not digest_only:
        slot["content"] = normalized
    return slot


class OpenAICompatibleAdapter:
    """Provider-agnostic wrapper for the current local-first export path."""

    def __init__(
        self,
        *,
        output_dir: Path,
        store: LocalEvidenceStore,
        recorder: EvidenceRecorder,
        provider_label: str,
        model: str,
        api_key: str,
        base_url: str | None,
        digest_only: bool,
        omit_request: bool,
        omit_response: bool,
        request_settings: dict[str, Any],
        base_tags: list[str],
        private_key_pem: bytes | None = None,
        key_id: str = "openai-compatible-demo",
        key_version: str | None = None,
        signer: str = "local-demo",
        role: str = "attestor",
    ) -> None:
        self.output_dir = output_dir
        self.store = store
        self.recorder = recorder
        self.provider_label = provider_label
        self.model = model
        self.base_url = base_url
        self.digest_only = digest_only
        self.omit_request = omit_request
        self.omit_response = omit_response
        self.request_settings = request_settings
        self.base_tags = base_tags
        self._api_key = api_key
        self._private_key_pem = private_key_pem
        self._key_id = key_id
        self._key_version = key_version
        self._signer = signer
        self._role = role
        self._call_count = 0
        self._artifacts: OpenAICompatibleArtifacts | None = None

    @classmethod
    def for_output_dir(
        cls,
        output_dir: str | Path,
        *,
        provider_label: str,
        model: str,
        api_key: str,
        base_url: str | None = None,
        digest_only: bool = True,
        omit_request: bool = False,
        omit_response: bool = False,
        temperature: float | None = None,
        top_p: float | None = None,
        max_output_tokens: int | None = None,
        tool_choice: str | None = None,
        parallel_tool_calls: bool | None = None,
        timeout: float | None = None,
        base_tags: list[str] | None = None,
        private_key_pem: bytes | None = None,
        key_id: str = "openai-compatible-demo",
        key_version: str | None = None,
        signer: str = "local-demo",
        role: str = "attestor",
    ) -> "OpenAICompatibleAdapter":
        if not provider_label:
            raise ValueError("provider_label is required.")
        if not model:
            raise ValueError("model is required.")
        if not api_key:
            raise ValueError("api_key is required.")

        resolved_output_dir = Path(output_dir)
        if resolved_output_dir.exists():
            if resolved_output_dir.is_dir():
                shutil.rmtree(resolved_output_dir)
            else:
                resolved_output_dir.unlink()
        resolved_output_dir.mkdir(parents=True, exist_ok=True)

        request_settings = {
            key: value
            for key, value in {
                "temperature": temperature,
                "top_p": top_p,
                "max_output_tokens": max_output_tokens,
                "tool_choice": tool_choice,
                "parallel_tool_calls": parallel_tool_calls,
                "timeout": timeout,
            }.items()
            if value is not None
        }

        store = LocalEvidenceStore(resolved_output_dir / "runtime-events.jsonl")
        recorder = EvidenceRecorder(store)
        return cls(
            output_dir=resolved_output_dir,
            store=store,
            recorder=recorder,
            provider_label=provider_label,
            model=model,
            api_key=api_key,
            base_url=base_url,
            digest_only=digest_only,
            omit_request=omit_request,
            omit_response=omit_response,
            request_settings=request_settings,
            base_tags=base_tags or [],
            private_key_pem=private_key_pem,
            key_id=key_id,
            key_version=key_version,
            signer=signer,
            role=role,
        )

    def _event_tags(self, tags: list[str] | None) -> list[str]:
        return _merge_tags(
            ["openai-compatible", self.provider_label, "provider-call"],
            self.base_tags,
            tags,
        )

    def _call_metadata(
        self,
        *,
        operation: str,
        metadata: Mapping[str, Any] | None,
    ) -> dict[str, Any]:
        merged: dict[str, Any] = {
            "operation": operation,
            "provider_label": self.provider_label,
            "model": self.model,
            "request_settings": ensure_json_object(self.request_settings),
        }
        if self.base_url is not None:
            merged["base_url"] = self.base_url
        if metadata is not None:
            merged.update(ensure_json_object(metadata))
        return merged

    def _build_context(
        self,
        *,
        source_event_type: str,
        operation: str,
        call_id: str,
        tags: list[str],
        status: str,
    ) -> EvidenceContext:
        attributes = {
            "provider_label": self.provider_label,
            "model": self.model,
            "call_id": call_id,
            "status": status,
            "request_settings": ensure_json_object(self.request_settings),
        }
        if self.base_url is not None:
            attributes["base_url"] = self.base_url
        return EvidenceContext(
            source="openai_compatible",
            component="provider_call",
            source_event_type=source_event_type,
            span_id=call_id,
            name=operation,
            tags=tags,
            attributes=attributes,
        )

    def record_call(
        self,
        *,
        operation: str,
        request: Any,
        invoke: Callable[[], T],
        metadata: Mapping[str, Any] | None = None,
        tags: list[str] | None = None,
    ) -> T:
        call_id = str(uuid4())
        event_tags = self._event_tags(tags)
        event_metadata = self._call_metadata(operation=operation, metadata=metadata)

        self.recorder.record(
            actor=self.provider_label,
            event_type="provider.call.start",
            inputs=_payload_slot(
                request,
                digest_only=self.digest_only,
                omit=self.omit_request,
            ),
            context=self._build_context(
                source_event_type="on_provider_call_start",
                operation=operation,
                call_id=call_id,
                tags=event_tags,
                status="started",
            ),
            metadata=event_metadata,
        )

        try:
            response = invoke()
        except BaseException as exc:
            self._call_count += 1
            self.recorder.record(
                actor=self.provider_label,
                event_type="provider.call.error",
                outputs={"error": to_jsonable(exc)},
                context=self._build_context(
                    source_event_type="on_provider_call_error",
                    operation=operation,
                    call_id=call_id,
                    tags=event_tags,
                    status="failed",
                ),
                metadata=event_metadata,
            )
            raise

        self._call_count += 1
        self.recorder.record(
            actor=self.provider_label,
            event_type="provider.call.end",
            outputs=_payload_slot(
                response,
                digest_only=self.digest_only,
                omit=self.omit_response,
            ),
            context=self._build_context(
                source_event_type="on_provider_call_end",
                operation=operation,
                call_id=call_id,
                tags=event_tags,
                status="succeeded",
            ),
            metadata=event_metadata,
        )
        return response

    def finalize(self) -> OpenAICompatibleArtifacts:
        if self._artifacts is not None:
            return self._artifacts

        records = self.store.list()
        bundle_path = self.output_dir / "openai-compatible.bundle.json"
        manifest_path = self.output_dir / "openai-compatible.manifest.json"
        receipt_path = self.output_dir / "receipt.json"
        summary_path = self.output_dir / "summary.json"

        private_key_path, public_key_path, private_pem, public_pem = _write_adapter_keypair(
            self.output_dir,
            private_key_pem=self._private_key_pem,
        )
        bundle = export_json_bundle(
            records,
            bundle_path,
            filters={
                "source": "openai_compatible",
                "provider_label": self.provider_label,
                "model": self.model,
                "limit": len(records),
            },
            private_key_pem=private_pem,
            key_id=self._key_id,
            key_version=self._key_version,
            signer=self._signer,
            role=self._role,
            manifest_output_path=manifest_path,
        )
        receipt = verify_json_bundle(bundle_path, public_key_pem=public_pem)
        _write_json(receipt_path, receipt)

        verify_command = (
            f"agent-evidence verify-export --bundle {bundle_path} --public-key {public_key_path}"
        )
        summary = {
            "ok": receipt["ok"],
            "provider_label": self.provider_label,
            "model": self.model,
            "base_url": self.base_url,
            "output_dir": str(self.output_dir),
            "store_path": str(self.store.path),
            "bundle_path": str(bundle_path),
            "receipt_path": str(receipt_path),
            "manifest_path": str(manifest_path),
            "private_key_path": str(private_key_path),
            "public_key_path": str(public_key_path),
            "call_count": self._call_count,
            "record_count": len(records),
            "signature_count": len(bundle.signatures),
            "verify_command": verify_command,
            "verify_result": receipt,
        }
        _write_json(summary_path, summary)

        self._artifacts = OpenAICompatibleArtifacts(
            bundle_path=bundle_path,
            receipt=receipt,
            receipt_path=receipt_path,
            summary=summary,
            summary_path=summary_path,
            supporting_files={
                "manifest": manifest_path,
                "private_key": private_key_path,
                "public_key": public_key_path,
                "runtime_events": self.store.path,
            },
        )
        return self._artifacts
