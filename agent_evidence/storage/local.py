from __future__ import annotations

import json
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

    def latest_chain_digest(self) -> str | None:
        records = self.list()
        if not records:
            return None
        return records[-1].chain_digest

    def export_json(self) -> str:
        return json.dumps(
            [record.model_dump(mode="json") for record in self.list()],
            indent=2,
            sort_keys=True,
        )
