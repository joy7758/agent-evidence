from __future__ import annotations

from .hashing import hash_payload


def chain_digest_for_record(*, payload_digest: str, previous_digest: str | None) -> str:
    link = {
        "payload_digest": payload_digest,
        "previous_digest": previous_digest,
    }
    return hash_payload(link)
