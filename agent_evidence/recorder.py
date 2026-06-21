from __future__ import annotations

from typing import Any

from .crypto.chain import chain_digest_for_event
from .crypto.hashing import compute_hash
from .models import EvidenceContext, EvidenceEnvelope, EvidenceEvent, EvidenceHashes
from .serialization import ensure_json_object, to_jsonable
from .storage.base import EvidenceStore

_CONTEXT_FIELDS = {
    "source",
    "component",
    "source_event_type",
    "span_id",
    "parent_span_id",
    "ancestor_span_ids",
    "name",
    "tags",
    "attributes",
}


def _merge_tags(*parts: list[str] | None) -> list[str]:
    merged: list[str] = []
    for part in parts:
        for tag in part or []:
            tag_text = str(tag)
            if tag_text and tag_text not in merged:
                merged.append(tag_text)
    return merged


class EvidenceRecorder:
    """Compose event creation, hashing, and persistence into one step."""

    def __init__(self, store: EvidenceStore):
        self.store = store

    def _build_context(
        self,
        *,
        context: EvidenceContext | dict[str, Any] | None,
        tags: list[str] | None,
    ) -> EvidenceContext:
        merged_tags = [str(tag) for tag in to_jsonable(tags or [])]

        if isinstance(context, EvidenceContext):
            if not merged_tags:
                return context
            context_data = context.model_dump(mode="json")
            context_data["tags"] = _merge_tags(context.tags, merged_tags)
            return EvidenceContext.model_validate(context_data)

        if context is None:
            return EvidenceContext(tags=merged_tags)

        raw_context = ensure_json_object(context)
        context_data: dict[str, Any] = {}
        passthrough_attributes = ensure_json_object(raw_context.get("attributes"))

        for key, value in raw_context.items():
            if key == "attributes":
                continue
            normalized_value = to_jsonable(value)
            if key in _CONTEXT_FIELDS:
                context_data[key] = normalized_value
            else:
                passthrough_attributes[key] = normalized_value

        context_data["attributes"] = passthrough_attributes
        context_data["tags"] = _merge_tags(
            [str(tag) for tag in to_jsonable(raw_context.get("tags") or [])],
            merged_tags,
        )
        return EvidenceContext.model_validate(context_data)

    def build(
        self,
        *,
        actor: str,
        event_type: str | None = None,
        action: str | None = None,
        inputs: Any | None = None,
        outputs: Any | None = None,
        context: EvidenceContext | dict[str, Any] | None = None,
        metadata: Any | None = None,
        tags: list[str] | None = None,
    ) -> EvidenceEnvelope:
        latest_hashes = getattr(self.store, "latest_hashes", None)
        if callable(latest_hashes):
            tip = latest_hashes()
        else:
            tip = (self.store.latest_event_hash(), self.store.latest_chain_hash())
        return self._build_from_tip(
            tip,
            actor=actor,
            event_type=event_type,
            action=action,
            inputs=inputs,
            outputs=outputs,
            context=context,
            metadata=metadata,
            tags=tags,
        )

    def _build_from_tip(
        self,
        latest_hashes: tuple[str | None, str | None],
        *,
        actor: str,
        event_type: str | None = None,
        action: str | None = None,
        inputs: Any | None = None,
        outputs: Any | None = None,
        context: EvidenceContext | dict[str, Any] | None = None,
        metadata: Any | None = None,
        tags: list[str] | None = None,
    ) -> EvidenceEnvelope:
        resolved_event_type = event_type or action
        if not resolved_event_type:
            raise ValueError("event_type is required.")

        event = EvidenceEvent(
            actor=actor,
            event_type=resolved_event_type,
            inputs=ensure_json_object(inputs),
            outputs=ensure_json_object(outputs),
            context=self._build_context(context=context, tags=tags),
            metadata=ensure_json_object(metadata),
        )
        event_hash = compute_hash(event.model_dump(mode="json"))
        previous_event_hash, previous_chain_hash = latest_hashes
        chain_hash = chain_digest_for_event(
            event_hash=event_hash,
            previous_chain_hash=previous_chain_hash,
        )
        return EvidenceEnvelope(
            event=event,
            hashes=EvidenceHashes(
                event_hash=event_hash,
                previous_event_hash=previous_event_hash,
                chain_hash=chain_hash,
            ),
        )

    def record(self, **kwargs: Any) -> EvidenceEnvelope:
        return self.store.append_atomic(
            lambda latest_hashes: self._build_from_tip(latest_hashes, **kwargs)
        )
