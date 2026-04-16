from __future__ import annotations

import json
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping
from uuid import UUID

from agent_evidence.aep import EvidenceBundleBuilder
from agent_evidence.aep.hash_chain import sha256_digest
from agent_evidence.export import export_json_bundle, verify_json_bundle
from agent_evidence.models import EvidenceContext, EvidenceEvent, utc_now
from agent_evidence.recorder import EvidenceRecorder
from agent_evidence.serialization import ensure_json_object, to_jsonable
from agent_evidence.storage import LocalEvidenceStore

try:
    from langchain_core.callbacks import BaseCallbackHandler as LangChainBaseCallbackHandler
except ImportError:  # pragma: no cover - exercised indirectly when extra is absent

    class LangChainBaseCallbackHandler:  # type: ignore[no-redef]
        """Fallback base so the package remains importable without langchain-core."""

    _HAS_LANGCHAIN_CORE = False
else:
    _HAS_LANGCHAIN_CORE = True

_SEMANTIC_EVENT_TYPES = {
    "on_agent_action": "agent.action",
    "on_agent_finish": "agent.finish",
    "on_chain_end": "chain.end",
    "on_chain_error": "chain.error",
    "on_chain_start": "chain.start",
    "on_chain_stream": "chain.stream",
    "on_chat_model_start": "chat_model.start",
    "on_custom_event": "custom.emit",
    "on_llm_end": "llm.end",
    "on_llm_error": "llm.error",
    "on_llm_new_token": "llm.token",
    "on_llm_start": "llm.start",
    "on_retry": "retry.attempt",
    "on_retriever_end": "retriever.end",
    "on_retriever_error": "retriever.error",
    "on_retriever_start": "retriever.start",
    "on_text": "text.output",
    "on_tool_end": "tool.end",
    "on_tool_error": "tool.error",
    "on_tool_start": "tool.start",
}


@dataclass(frozen=True)
class LangChainArtifacts:
    """Normalized LangChain integration outputs plus supporting files."""

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
            "LangChainAdapter signing requires cryptography. Install agent-evidence with "
            "the [signing] or [dev] extra."
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
            raise TypeError("LangChainAdapter requires an Ed25519 private key in PEM format.")
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


def _component_from_source_event(source_event_type: str) -> str:
    if source_event_type == "on_custom_event":
        return "custom_event"
    parts = source_event_type.split("_")
    if len(parts) >= 3:
        return parts[1]
    return "langchain"


def semantic_event_type(source_event_type: str) -> str:
    if source_event_type in _SEMANTIC_EVENT_TYPES:
        return _SEMANTIC_EVENT_TYPES[source_event_type]
    if source_event_type.startswith("on_"):
        return source_event_type[3:].replace("_", ".")
    return source_event_type.replace("_", ".")


def _openinference_span_kind(component: str) -> str:
    mapping = {
        "agent": "AGENT",
        "chain": "CHAIN",
        "chat_model": "LLM",
        "custom_event": "UNKNOWN",
        "llm": "LLM",
        "retriever": "RETRIEVER",
        "retry": "UNKNOWN",
        "text": "UNKNOWN",
        "tool": "TOOL",
    }
    return mapping.get(component, "UNKNOWN")


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


def _stream_inputs(data: Mapping[str, Any]) -> Any:
    for key in ("input", "inputs", "messages", "query"):
        if key in data:
            return {key: data[key]}
    return {}


def _stream_outputs(data: Mapping[str, Any]) -> Any:
    for key in ("output", "outputs", "chunk", "documents"):
        if key in data:
            return {key: data[key]}
    return {}


def _named_value(value: Any, key: str) -> Any:
    if isinstance(value, Mapping):
        return value
    return {key: value}


def build_langchain_context(
    *,
    source_event_type: str,
    component: str | None = None,
    tags: list[str] | tuple[str, ...] | None = None,
    run_id: UUID | str | None = None,
    parent_run_id: UUID | str | None = None,
    parent_ids: list[str] | None = None,
    name: str | None = None,
    serialized: Mapping[str, Any] | None = None,
    attributes: Mapping[str, Any] | None = None,
) -> EvidenceContext:
    resolved_component = component or _component_from_source_event(source_event_type)
    return EvidenceContext(
        source="langchain",
        component=resolved_component,
        source_event_type=source_event_type,
        span_id=str(run_id) if run_id else None,
        parent_span_id=str(parent_run_id) if parent_run_id else None,
        ancestor_span_ids=[str(parent_id) for parent_id in parent_ids or []],
        name=name,
        tags=_merge_tags(["langchain", resolved_component], list(tags or [])),
        attributes=ensure_json_object(
            {
                "serialized": serialized,
                "extra": dict(attributes or {}),
            }
        ),
    )


def evidence_from_langchain_event(event: Mapping[str, Any]) -> EvidenceEvent:
    """
    Normalize a LangChain stream event into a framework-neutral EvidenceEvent.

    LangChain documents `Runnable.astream_events(..., version="v2")` as producing
    dictionaries with `event`, `name`, `run_id`, `parent_ids`, `tags`,
    `metadata`, and `data` fields.
    """

    source_event_type = str(event.get("event") or "langchain.event")
    component = _component_from_source_event(source_event_type)
    event_data = event.get("data") or {}
    if not isinstance(event_data, Mapping):
        event_data = {"value": event_data}

    return EvidenceEvent(
        event_type=semantic_event_type(source_event_type),
        actor=str(event.get("name") or component),
        inputs=ensure_json_object(_stream_inputs(event_data)),
        outputs=ensure_json_object(_stream_outputs(event_data)),
        context=build_langchain_context(
            source_event_type=source_event_type,
            component=component,
            tags=to_jsonable(event.get("tags") or []),
            run_id=event.get("run_id"),
            parent_ids=[str(parent_id) for parent_id in event.get("parent_ids") or []],
            name=str(event.get("name") or component),
            attributes={"data_keys": sorted(event_data.keys())},
        ),
        metadata=ensure_json_object(
            event.get("metadata") if isinstance(event.get("metadata"), Mapping) else {}
        ),
    )


def record_langchain_event(
    recorder: EvidenceRecorder,
    event: Mapping[str, Any],
) -> Any:
    evidence_event = evidence_from_langchain_event(event)
    return recorder.record(
        actor=evidence_event.actor,
        event_type=evidence_event.event_type,
        inputs=evidence_event.inputs,
        outputs=evidence_event.outputs,
        context=evidence_event.context,
        metadata=evidence_event.metadata,
    )


class EvidenceCallbackHandler(LangChainBaseCallbackHandler):
    """LangChain callback handler that emits stable semantic evidence events."""

    raise_error = False
    run_inline = True

    def __init__(
        self,
        recorder: EvidenceRecorder | None = None,
        *,
        actor: str = "langchain",
        base_tags: list[str] | None = None,
        capture_stream_tokens: bool = False,
        bundle_builder: EvidenceBundleBuilder | None = None,
        digest_only: bool = True,
        omit_request: bool = False,
        omit_response: bool = False,
    ) -> None:
        if not _HAS_LANGCHAIN_CORE:
            raise ModuleNotFoundError(
                "langchain-core is required for EvidenceCallbackHandler. "
                "Install agent-evidence with the [langchain] extra."
            )
        if recorder is None and bundle_builder is None:
            raise ValueError("Provide at least one of recorder or bundle_builder.")
        self.recorder = recorder
        self.actor = actor
        self.base_tags = base_tags or []
        self.capture_stream_tokens = capture_stream_tokens
        self.bundle_builder = bundle_builder
        self.digest_only = digest_only
        self.omit_request = omit_request
        self.omit_response = omit_response

    def _record(
        self,
        *,
        source_event_type: str,
        component: str,
        actor: str | None = None,
        inputs: Any = None,
        outputs: Any = None,
        metadata: Mapping[str, Any] | None = None,
        tags: list[str] | None = None,
        run_id: UUID | None = None,
        parent_run_id: UUID | None = None,
        parent_ids: list[str] | None = None,
        name: str | None = None,
        serialized: Mapping[str, Any] | None = None,
        extra: Mapping[str, Any] | None = None,
    ) -> None:
        resolved_actor = actor or name or self.actor
        resolved_tags = _merge_tags(self.base_tags, tags)
        resolved_metadata = ensure_json_object(metadata)
        resolved_context = build_langchain_context(
            source_event_type=source_event_type,
            component=component,
            tags=resolved_tags,
            run_id=run_id,
            parent_run_id=parent_run_id,
            parent_ids=parent_ids,
            name=name,
            serialized=serialized,
            attributes=extra,
        )

        if self.recorder is not None:
            self.recorder.record(
                actor=resolved_actor,
                event_type=semantic_event_type(source_event_type),
                inputs=inputs,
                outputs=outputs,
                context=resolved_context,
                metadata=resolved_metadata,
            )

        if self.bundle_builder is not None and source_event_type != "on_llm_new_token":
            self.bundle_builder.add_record(
                event_type=semantic_event_type(source_event_type),
                timestamp=utc_now().isoformat(),
                payload={
                    "actor": resolved_actor,
                    "source": "langchain",
                    "component": component,
                    "source_event_type": source_event_type,
                    "name": name,
                    "tags": resolved_tags,
                    "metadata": resolved_metadata,
                    "attributes": {
                        "openinference": {
                            "span_kind": _openinference_span_kind(component),
                        },
                        "gen_ai": {
                            "system": "langchain",
                            "operation_name": semantic_event_type(source_event_type),
                        },
                        "span": {
                            "run_id": str(run_id) if run_id else None,
                            "parent_run_id": str(parent_run_id) if parent_run_id else None,
                            "parent_ids": [str(parent_id) for parent_id in parent_ids or []],
                        },
                        "serialized": to_jsonable(serialized),
                        "extra": ensure_json_object(extra),
                    },
                    "request": _payload_slot(
                        inputs,
                        digest_only=self.digest_only,
                        omit=self.omit_request,
                    ),
                    "response": _payload_slot(
                        outputs,
                        digest_only=self.digest_only,
                        omit=self.omit_response,
                    ),
                },
            )

    def on_chain_start(
        self,
        serialized: dict[str, Any] | None,
        inputs: dict[str, Any] | Any,
        *,
        run_id: UUID,
        parent_run_id: UUID | None = None,
        tags: list[str] | None = None,
        metadata: dict[str, Any] | None = None,
        run_type: str | None = None,
        name: str | None = None,
        **kwargs: Any,
    ) -> None:
        self._record(
            source_event_type="on_chain_start",
            component=run_type or "chain",
            actor=name,
            inputs=_named_value(inputs, "input"),
            metadata=metadata,
            tags=tags,
            run_id=run_id,
            parent_run_id=parent_run_id,
            name=name,
            serialized=serialized,
            extra=kwargs,
        )

    def on_chain_end(
        self,
        outputs: dict[str, Any] | Any,
        *,
        run_id: UUID,
        parent_run_id: UUID | None = None,
        tags: list[str] | None = None,
        **kwargs: Any,
    ) -> None:
        self._record(
            source_event_type="on_chain_end",
            component="chain",
            outputs=_named_value(outputs, "output"),
            tags=tags,
            run_id=run_id,
            parent_run_id=parent_run_id,
            name=kwargs.get("name"),
            metadata=kwargs.get("metadata"),
            extra=kwargs,
        )

    def on_chain_error(
        self,
        error: BaseException,
        *,
        run_id: UUID,
        parent_run_id: UUID | None = None,
        tags: list[str] | None = None,
        **kwargs: Any,
    ) -> None:
        self._record(
            source_event_type="on_chain_error",
            component="chain",
            outputs={"error": to_jsonable(error)},
            tags=tags,
            run_id=run_id,
            parent_run_id=parent_run_id,
            name=kwargs.get("name"),
            metadata=kwargs.get("metadata"),
            extra=kwargs,
        )

    def on_tool_start(
        self,
        serialized: dict[str, Any],
        input_str: str,
        *,
        run_id: UUID,
        parent_run_id: UUID | None = None,
        tags: list[str] | None = None,
        metadata: dict[str, Any] | None = None,
        name: str | None = None,
        inputs: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> None:
        self._record(
            source_event_type="on_tool_start",
            component="tool",
            actor=name,
            inputs=inputs if inputs is not None else {"input": input_str},
            metadata=metadata,
            tags=tags,
            run_id=run_id,
            parent_run_id=parent_run_id,
            name=name,
            serialized=serialized,
            extra=kwargs,
        )

    def on_tool_end(
        self,
        output: Any,
        *,
        run_id: UUID,
        parent_run_id: UUID | None = None,
        tags: list[str] | None = None,
        **kwargs: Any,
    ) -> None:
        self._record(
            source_event_type="on_tool_end",
            component="tool",
            outputs=_named_value(output, "output"),
            tags=tags,
            run_id=run_id,
            parent_run_id=parent_run_id,
            name=kwargs.get("name"),
            metadata=kwargs.get("metadata"),
            extra=kwargs,
        )

    def on_tool_error(
        self,
        error: BaseException,
        *,
        run_id: UUID,
        parent_run_id: UUID | None = None,
        tags: list[str] | None = None,
        **kwargs: Any,
    ) -> None:
        self._record(
            source_event_type="on_tool_error",
            component="tool",
            outputs={"error": to_jsonable(error)},
            tags=tags,
            run_id=run_id,
            parent_run_id=parent_run_id,
            name=kwargs.get("name"),
            metadata=kwargs.get("metadata"),
            extra=kwargs,
        )

    def on_retriever_start(
        self,
        serialized: dict[str, Any],
        query: str,
        *,
        run_id: UUID,
        parent_run_id: UUID | None = None,
        tags: list[str] | None = None,
        metadata: dict[str, Any] | None = None,
        name: str | None = None,
        **kwargs: Any,
    ) -> None:
        self._record(
            source_event_type="on_retriever_start",
            component="retriever",
            actor=name,
            inputs={"query": query},
            metadata=metadata,
            tags=tags,
            run_id=run_id,
            parent_run_id=parent_run_id,
            name=name,
            serialized=serialized,
            extra=kwargs,
        )

    def on_retriever_end(
        self,
        documents: Any,
        *,
        run_id: UUID,
        parent_run_id: UUID | None = None,
        tags: list[str] | None = None,
        **kwargs: Any,
    ) -> None:
        self._record(
            source_event_type="on_retriever_end",
            component="retriever",
            outputs={"documents": documents},
            tags=tags,
            run_id=run_id,
            parent_run_id=parent_run_id,
            name=kwargs.get("name"),
            metadata=kwargs.get("metadata"),
            extra=kwargs,
        )

    def on_retriever_error(
        self,
        error: BaseException,
        *,
        run_id: UUID,
        parent_run_id: UUID | None = None,
        tags: list[str] | None = None,
        **kwargs: Any,
    ) -> None:
        self._record(
            source_event_type="on_retriever_error",
            component="retriever",
            outputs={"error": to_jsonable(error)},
            tags=tags,
            run_id=run_id,
            parent_run_id=parent_run_id,
            name=kwargs.get("name"),
            metadata=kwargs.get("metadata"),
            extra=kwargs,
        )

    def on_llm_start(
        self,
        serialized: dict[str, Any],
        prompts: list[str],
        *,
        run_id: UUID,
        parent_run_id: UUID | None = None,
        tags: list[str] | None = None,
        metadata: dict[str, Any] | None = None,
        name: str | None = None,
        **kwargs: Any,
    ) -> None:
        self._record(
            source_event_type="on_llm_start",
            component="llm",
            actor=name,
            inputs={"prompts": prompts},
            metadata=metadata,
            tags=tags,
            run_id=run_id,
            parent_run_id=parent_run_id,
            name=name,
            serialized=serialized,
            extra=kwargs,
        )

    def on_chat_model_start(
        self,
        serialized: dict[str, Any],
        messages: list[list[Any]],
        *,
        run_id: UUID,
        parent_run_id: UUID | None = None,
        tags: list[str] | None = None,
        metadata: dict[str, Any] | None = None,
        name: str | None = None,
        **kwargs: Any,
    ) -> None:
        self._record(
            source_event_type="on_chat_model_start",
            component="chat_model",
            actor=name,
            inputs={"messages": messages},
            metadata=metadata,
            tags=tags,
            run_id=run_id,
            parent_run_id=parent_run_id,
            name=name,
            serialized=serialized,
            extra=kwargs,
        )

    def on_llm_new_token(
        self,
        token: str,
        *,
        run_id: UUID,
        parent_run_id: UUID | None = None,
        tags: list[str] | None = None,
        **kwargs: Any,
    ) -> None:
        if not self.capture_stream_tokens:
            return
        self._record(
            source_event_type="on_llm_new_token",
            component="llm",
            outputs={"token": token, "chunk": kwargs.get("chunk")},
            tags=tags,
            run_id=run_id,
            parent_run_id=parent_run_id,
            name=kwargs.get("name"),
            metadata=kwargs.get("metadata"),
            extra=kwargs,
        )

    def on_llm_end(
        self,
        response: Any,
        *,
        run_id: UUID,
        parent_run_id: UUID | None = None,
        tags: list[str] | None = None,
        **kwargs: Any,
    ) -> None:
        self._record(
            source_event_type="on_llm_end",
            component="llm",
            outputs={"response": response},
            tags=tags,
            run_id=run_id,
            parent_run_id=parent_run_id,
            name=kwargs.get("name"),
            metadata=kwargs.get("metadata"),
            extra=kwargs,
        )

    def on_llm_error(
        self,
        error: BaseException,
        *,
        run_id: UUID,
        parent_run_id: UUID | None = None,
        tags: list[str] | None = None,
        **kwargs: Any,
    ) -> None:
        self._record(
            source_event_type="on_llm_error",
            component="llm",
            outputs={"error": to_jsonable(error)},
            tags=tags,
            run_id=run_id,
            parent_run_id=parent_run_id,
            name=kwargs.get("name"),
            metadata=kwargs.get("metadata"),
            extra=kwargs,
        )

    def on_agent_action(
        self,
        action: Any,
        *,
        run_id: UUID,
        parent_run_id: UUID | None = None,
        tags: list[str] | None = None,
        **kwargs: Any,
    ) -> None:
        self._record(
            source_event_type="on_agent_action",
            component="agent",
            inputs={
                "tool": getattr(action, "tool", None),
                "tool_input": getattr(action, "tool_input", None),
                "log": getattr(action, "log", None),
            },
            tags=tags,
            run_id=run_id,
            parent_run_id=parent_run_id,
            name=kwargs.get("name"),
            metadata=kwargs.get("metadata"),
            extra=kwargs,
        )

    def on_agent_finish(
        self,
        finish: Any,
        *,
        run_id: UUID,
        parent_run_id: UUID | None = None,
        tags: list[str] | None = None,
        **kwargs: Any,
    ) -> None:
        self._record(
            source_event_type="on_agent_finish",
            component="agent",
            outputs={
                "return_values": getattr(finish, "return_values", None),
                "log": getattr(finish, "log", None),
            },
            tags=tags,
            run_id=run_id,
            parent_run_id=parent_run_id,
            name=kwargs.get("name"),
            metadata=kwargs.get("metadata"),
            extra=kwargs,
        )

    def on_text(
        self,
        text: str,
        *,
        run_id: UUID,
        parent_run_id: UUID | None = None,
        tags: list[str] | None = None,
        **kwargs: Any,
    ) -> None:
        self._record(
            source_event_type="on_text",
            component="text",
            outputs={"text": text},
            tags=tags,
            run_id=run_id,
            parent_run_id=parent_run_id,
            name=kwargs.get("name"),
            metadata=kwargs.get("metadata"),
            extra=kwargs,
        )

    def on_retry(
        self,
        retry_state: Any,
        *,
        run_id: UUID,
        parent_run_id: UUID | None = None,
        tags: list[str] | None = None,
        **kwargs: Any,
    ) -> None:
        self._record(
            source_event_type="on_retry",
            component="retry",
            outputs={"retry_state": retry_state},
            tags=tags,
            run_id=run_id,
            parent_run_id=parent_run_id,
            name=kwargs.get("name"),
            metadata=kwargs.get("metadata"),
            extra=kwargs,
        )

    def on_custom_event(
        self,
        name: str,
        data: Any,
        *,
        run_id: UUID,
        tags: list[str] | None = None,
        metadata: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> None:
        self._record(
            source_event_type="on_custom_event",
            component="custom_event",
            actor=name,
            outputs={"data": data},
            metadata=metadata,
            tags=tags,
            run_id=run_id,
            name=name,
            extra=kwargs,
        )


class LangChainAdapter:
    """Recommended LangChain wrapper for the current quickstart artifact path."""

    def __init__(
        self,
        *,
        output_dir: Path,
        store: LocalEvidenceStore,
        recorder: EvidenceRecorder,
        handler: EvidenceCallbackHandler,
        private_key_pem: bytes | None = None,
        key_id: str = "langchain-cookbook-demo",
        key_version: str | None = None,
        signer: str = "local-demo",
        role: str = "attestor",
    ) -> None:
        self.output_dir = output_dir
        self.store = store
        self.recorder = recorder
        self._handler = handler
        self._private_key_pem = private_key_pem
        self._key_id = key_id
        self._key_version = key_version
        self._signer = signer
        self._role = role
        self._artifacts: LangChainArtifacts | None = None

    @classmethod
    def for_output_dir(
        cls,
        output_dir: str | Path,
        *,
        digest_only: bool = True,
        omit_request: bool = False,
        omit_response: bool = False,
        capture_stream_tokens: bool = False,
        base_tags: list[str] | None = None,
        private_key_pem: bytes | None = None,
        key_id: str = "langchain-cookbook-demo",
        key_version: str | None = None,
        signer: str = "local-demo",
        role: str = "attestor",
    ) -> "LangChainAdapter":
        resolved_output_dir = Path(output_dir)
        if resolved_output_dir.exists():
            if resolved_output_dir.is_dir():
                shutil.rmtree(resolved_output_dir)
            else:
                resolved_output_dir.unlink()
        resolved_output_dir.mkdir(parents=True, exist_ok=True)

        store = LocalEvidenceStore(resolved_output_dir / "runtime-events.jsonl")
        recorder = EvidenceRecorder(store)
        handler = EvidenceCallbackHandler(
            recorder=recorder,
            base_tags=base_tags,
            capture_stream_tokens=capture_stream_tokens,
            digest_only=digest_only,
            omit_request=omit_request,
            omit_response=omit_response,
        )
        return cls(
            output_dir=resolved_output_dir,
            store=store,
            recorder=recorder,
            handler=handler,
            private_key_pem=private_key_pem,
            key_id=key_id,
            key_version=key_version,
            signer=signer,
            role=role,
        )

    def callback_handler(self) -> EvidenceCallbackHandler:
        return self._handler

    def finalize(self) -> LangChainArtifacts:
        if self._artifacts is not None:
            return self._artifacts

        records = self.store.list()
        bundle_path = self.output_dir / "langchain-evidence.bundle.json"
        manifest_path = self.output_dir / "langchain-evidence.manifest.json"
        receipt_path = self.output_dir / "receipt.json"
        summary_path = self.output_dir / "summary.json"

        private_key_path, public_key_path, private_pem, public_pem = _write_adapter_keypair(
            self.output_dir,
            private_key_pem=self._private_key_pem,
        )
        bundle = export_json_bundle(
            records,
            bundle_path,
            filters={"source": "langchain", "limit": len(records)},
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
            "output_dir": str(self.output_dir),
            "store_path": str(self.store.path),
            "bundle_path": str(bundle_path),
            "receipt_path": str(receipt_path),
            "manifest_path": str(manifest_path),
            "private_key_path": str(private_key_path),
            "public_key_path": str(public_key_path),
            "record_count": len(records),
            "signature_count": len(bundle.signatures),
            "verify_command": verify_command,
            "verify_result": receipt,
            "anchor_note": (
                "Detached anchoring is not implemented in this repository. Use the exported "
                "bundle digest and signed manifest as the handoff point if you want to anchor "
                "it in an external timestamp or registry system."
            ),
        }
        _write_json(summary_path, summary)

        self._artifacts = LangChainArtifacts(
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
