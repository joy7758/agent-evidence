from __future__ import annotations

from typing import Any

from .crypto.chain import chain_digest_for_record
from .crypto.hashing import hash_payload
from .models import EvidenceEnvelope, EvidencePayload
from .serialization import ensure_json_object, to_jsonable
from .storage.base import EvidenceStore


class EvidenceRecorder:
    """Compose payload creation, hashing, and persistence into one step."""

    def __init__(self, store: EvidenceStore):
        self.store = store

    def build(
        self,
        *,
        actor: str,
        action: str,
        inputs: Any | None = None,
        outputs: Any | None = None,
        metadata: Any | None = None,
        tags: list[str] | None = None,
    ) -> EvidenceEnvelope:
        payload = EvidencePayload(
            actor=actor,
            action=action,
            inputs=ensure_json_object(inputs),
            outputs=ensure_json_object(outputs),
            metadata=ensure_json_object(metadata),
            tags=[str(tag) for tag in to_jsonable(tags or [])],
        )
        payload_digest = hash_payload(payload.model_dump(mode="json"))
        previous_digest = self.store.latest_chain_digest()
        chain_digest = chain_digest_for_record(
            payload_digest=payload_digest,
            previous_digest=previous_digest,
        )
        return EvidenceEnvelope(
            payload=payload,
            payload_digest=payload_digest,
            previous_digest=previous_digest,
            chain_digest=chain_digest,
        )

    def record(self, **kwargs: Any) -> EvidenceEnvelope:
        envelope = self.build(**kwargs)
        self.store.append(envelope)
        return envelope
