from __future__ import annotations

from agent_evidence.storage.base import EvidenceStore


def migrate_records(
    source_store: EvidenceStore,
    target_store: EvidenceStore,
    *,
    allow_existing: bool = False,
) -> int:
    if not allow_existing and target_store.query(limit=1):
        raise ValueError("Target store is not empty. Pass allow_existing=True to append records.")

    migrated = 0
    for envelope in source_store.list():
        target_store.append(envelope)
        migrated += 1
    return migrated
