from __future__ import annotations

from typing import Any, Mapping
from uuid import UUID

from agent_evidence.models import EvidencePayload
from agent_evidence.recorder import EvidenceRecorder
from agent_evidence.serialization import ensure_json_object, to_jsonable

try:
    from langchain_core.callbacks import BaseCallbackHandler as LangChainBaseCallbackHandler
except ImportError:  # pragma: no cover - exercised indirectly when extra is absent

    class LangChainBaseCallbackHandler:  # type: ignore[no-redef]
        """Fallback base so the package remains importable without langchain-core."""

    _HAS_LANGCHAIN_CORE = False
else:
    _HAS_LANGCHAIN_CORE = True


def _merge_tags(*parts: list[str] | tuple[str, ...] | None) -> list[str]:
    merged: list[str] = []
    for part in parts:
        for tag in part or []:
            tag_text = str(tag)
            if tag_text and tag_text not in merged:
                merged.append(tag_text)
    return merged


def _langchain_metadata(
    *,
    event: str,
    component: str,
    run_id: UUID | str | None = None,
    parent_run_id: UUID | str | None = None,
    parent_ids: list[str] | None = None,
    name: str | None = None,
    serialized: Mapping[str, Any] | None = None,
    metadata: Mapping[str, Any] | None = None,
    extra: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    context = ensure_json_object(metadata)
    context["_langchain"] = ensure_json_object(
        {
            "event": event,
            "component": component,
            "run_id": run_id,
            "parent_run_id": parent_run_id,
            "parent_ids": parent_ids or [],
            "name": name,
            "serialized": serialized,
            "extra": extra or {},
        }
    )
    return context


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


def _component_from_event(event_name: str) -> str:
    if event_name == "on_custom_event":
        return "custom_event"
    parts = event_name.split("_")
    if len(parts) >= 3:
        return parts[1]
    return "langchain"


def _named_value(value: Any, key: str) -> Any:
    if isinstance(value, Mapping):
        return value
    return {key: value}


def evidence_from_langchain_event(event: Mapping[str, Any]) -> EvidencePayload:
    """
    Normalize a LangChain stream event into an EvidencePayload.

    LangChain documents `Runnable.astream_events(..., version="v2")` as producing
    dictionaries with `event`, `name`, `run_id`, `parent_ids`, `tags`,
    `metadata`, and `data` fields.
    """

    event_name = str(event.get("event") or "langchain_event")
    component = _component_from_event(event_name)
    event_data = event.get("data") or {}
    if not isinstance(event_data, Mapping):
        event_data = {"value": event_data}

    metadata = _langchain_metadata(
        event=event_name,
        component=component,
        run_id=event.get("run_id"),
        parent_ids=[str(parent_id) for parent_id in event.get("parent_ids") or []],
        name=str(event.get("name") or component),
        metadata=event.get("metadata") if isinstance(event.get("metadata"), Mapping) else None,
        extra={"data_keys": sorted(event_data.keys())},
    )

    return EvidencePayload(
        actor=str(event.get("name") or component),
        action=event_name,
        inputs=ensure_json_object(_stream_inputs(event_data)),
        outputs=ensure_json_object(_stream_outputs(event_data)),
        metadata=metadata,
        tags=_merge_tags(["langchain", component], to_jsonable(event.get("tags") or [])),
    )


def record_langchain_event(
    recorder: EvidenceRecorder,
    event: Mapping[str, Any],
) -> Any:
    payload = evidence_from_langchain_event(event)
    return recorder.record(
        actor=payload.actor,
        action=payload.action,
        inputs=payload.inputs,
        outputs=payload.outputs,
        metadata=payload.metadata,
        tags=payload.tags,
    )


class EvidenceCallbackHandler(LangChainBaseCallbackHandler):
    """LangChain callback handler that persists execution evidence inline."""

    raise_error = False
    run_inline = True

    def __init__(
        self,
        recorder: EvidenceRecorder,
        *,
        actor: str = "langchain",
        base_tags: list[str] | None = None,
        capture_stream_tokens: bool = False,
    ) -> None:
        if not _HAS_LANGCHAIN_CORE:
            raise ModuleNotFoundError(
                "langchain-core is required for EvidenceCallbackHandler. "
                "Install agent-evidence with the [langchain] extra."
            )
        self.recorder = recorder
        self.actor = actor
        self.base_tags = base_tags or []
        self.capture_stream_tokens = capture_stream_tokens

    def _record(
        self,
        *,
        action: str,
        component: str,
        actor: str | None = None,
        inputs: Any = None,
        outputs: Any = None,
        metadata: Mapping[str, Any] | None = None,
        tags: list[str] | None = None,
        run_id: UUID | None = None,
        parent_run_id: UUID | None = None,
        name: str | None = None,
        serialized: Mapping[str, Any] | None = None,
        extra: Mapping[str, Any] | None = None,
    ) -> None:
        evidence_metadata = _langchain_metadata(
            event=action,
            component=component,
            run_id=run_id,
            parent_run_id=parent_run_id,
            name=name,
            serialized=serialized,
            metadata=metadata,
            extra=extra,
        )
        self.recorder.record(
            actor=actor or name or self.actor,
            action=action,
            inputs=inputs,
            outputs=outputs,
            metadata=evidence_metadata,
            tags=_merge_tags(self.base_tags, ["langchain", component], tags),
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
            action="on_chain_start",
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
            action="on_chain_end",
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
            action="on_chain_error",
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
            action="on_tool_start",
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
            action="on_tool_end",
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
            action="on_tool_error",
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
            action="on_retriever_start",
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
            action="on_retriever_end",
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
            action="on_retriever_error",
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
            action="on_llm_start",
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
            action="on_chat_model_start",
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
            action="on_llm_new_token",
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
            action="on_llm_end",
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
            action="on_llm_error",
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
            action="on_agent_action",
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
            action="on_agent_finish",
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
            action="on_text",
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
            action="on_retry",
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
            action="on_custom_event",
            component="custom_event",
            actor=name,
            outputs={"data": data},
            metadata=metadata,
            tags=tags,
            run_id=run_id,
            name=name,
            extra=kwargs,
        )
