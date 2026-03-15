from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

from agent_evidence.models import EvidenceEnvelope
from agent_evidence.storage.base import EvidenceStore


class LocalEvidenceStore(EvidenceStore):
    """Append-only JSONL storage for local development and simple deployments."""

    def __init__(self, path: str | Path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def append(self, envelope: EvidenceEnvelope) -> None:
        with self.path.open("a", encoding="utf-8") as handle:
            handle.write(envelope.model_dump_json())
            handle.write("\n")

    def list(self) -> list[EvidenceEnvelope]:
        if not self.path.exists():
            return []

        records: list[EvidenceEnvelope] = []
        with self.path.open("r", encoding="utf-8") as handle:
            for line in handle:
                line = line.strip()
                if not line:
                    continue
                records.append(EvidenceEnvelope.model_validate_json(line))
        return records

    def latest_event_hash(self) -> str | None:
        records = self.list()
        if not records:
            return None
        return records[-1].hashes.event_hash

    def latest_chain_hash(self) -> str | None:
        records = self.list()
        if not records:
            return None
        return records[-1].hashes.chain_hash

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
        records = self.list()

        def matches(envelope: EvidenceEnvelope) -> bool:
            event = envelope.event
            context = event.context
            if event_type is not None and event.event_type != event_type:
                return False
            if actor is not None and event.actor != actor:
                return False
            if source is not None and context.source != source:
                return False
            if component is not None and context.component != component:
                return False
            if since is not None and event.timestamp < since:
                return False
            if until is not None and event.timestamp > until:
                return False
            return True

        filtered = [envelope for envelope in records if matches(envelope)]
        if limit is not None:
            return filtered[:limit]
        return filtered

    def export_json(self) -> str:
        return json.dumps(
            [record.model_dump(mode="json") for record in self.list()],
            indent=2,
            sort_keys=True,
        )
