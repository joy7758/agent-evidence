from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Callable
from datetime import datetime

from agent_evidence.models import EvidenceEnvelope

LatestHashes = tuple[str | None, str | None]
AtomicEnvelopeBuilder = Callable[[LatestHashes], EvidenceEnvelope]


class EvidenceStore(ABC):
    @abstractmethod
    def append(self, envelope: EvidenceEnvelope) -> None:
        raise NotImplementedError

    def append_atomic(self, build_envelope_from_tip: AtomicEnvelopeBuilder) -> EvidenceEnvelope:
        latest_hashes = self.latest_hashes()
        envelope = build_envelope_from_tip(latest_hashes)
        self.append(envelope)
        return envelope

    @abstractmethod
    def list(self) -> list[EvidenceEnvelope]:
        raise NotImplementedError

    @abstractmethod
    def latest_event_hash(self) -> str | None:
        raise NotImplementedError

    @abstractmethod
    def latest_chain_hash(self) -> str | None:
        raise NotImplementedError

    @abstractmethod
    def latest_hashes(self) -> tuple[str | None, str | None]:
        raise NotImplementedError

    @abstractmethod
    def query(
        self,
        *,
        event_type: str | None = None,
        actor: str | None = None,
        source: str | None = None,
        component: str | None = None,
        span_id: str | None = None,
        parent_span_id: str | None = None,
        previous_event_hash: str | None = None,
        since: datetime | None = None,
        until: datetime | None = None,
        event_hash_from: str | None = None,
        event_hash_to: str | None = None,
        chain_hash_from: str | None = None,
        chain_hash_to: str | None = None,
        offset: int | None = None,
        limit: int | None = None,
    ) -> list[EvidenceEnvelope]:
        raise NotImplementedError
