from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime

from agent_evidence.models import EvidenceEnvelope


class EvidenceStore(ABC):
    @abstractmethod
    def append(self, envelope: EvidenceEnvelope) -> None:
        raise NotImplementedError

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
    def query(
        self,
        *,
        event_type: str | None = None,
        actor: str | None = None,
        source: str | None = None,
        component: str | None = None,
        since: datetime | None = None,
        until: datetime | None = None,
        limit: int | None = None,
    ) -> list[EvidenceEnvelope]:
        raise NotImplementedError
