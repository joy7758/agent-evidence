from __future__ import annotations

from collections.abc import Sequence

from agent_evidence.models import EvidenceEnvelope

from .hashing import compute_hash


def chain_digest_for_event(*, event_hash: str, previous_chain_hash: str | None) -> str:
    link = {
        "event_hash": event_hash,
        "previous_chain_hash": previous_chain_hash,
    }
    return compute_hash(link)


def verify_chain(envelopes: Sequence[EvidenceEnvelope]) -> list[str]:
    issues: list[str] = []
    previous_event_hash: str | None = None
    previous_chain_hash: str | None = None

    for index, envelope in enumerate(envelopes):
        expected_event_hash = compute_hash(envelope.event.model_dump(mode="json"))
        if envelope.hashes.event_hash != expected_event_hash:
            issues.append(f"record {index}: event_hash mismatch")

        if envelope.hashes.previous_event_hash != previous_event_hash:
            issues.append(f"record {index}: previous_event_hash mismatch")

        expected_chain_hash = chain_digest_for_event(
            event_hash=expected_event_hash,
            previous_chain_hash=previous_chain_hash,
        )
        if envelope.hashes.chain_hash != expected_chain_hash:
            issues.append(f"record {index}: chain_hash mismatch")

        previous_event_hash = expected_event_hash
        previous_chain_hash = expected_chain_hash

    return issues
