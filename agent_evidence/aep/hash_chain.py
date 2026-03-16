from __future__ import annotations

import hashlib
import re
from typing import Any, Sequence

from .canonicalizer import canonical_json_bytes

DIGEST_PREFIX = "sha256:"
DIGEST_PATTERN = re.compile(r"^sha256:[0-9a-f]{64}$")


def sha256_digest(value: Any) -> str:
    if isinstance(value, (bytes, bytearray)):
        payload = bytes(value)
    else:
        payload = canonical_json_bytes(value)
    return DIGEST_PREFIX + hashlib.sha256(payload).hexdigest()


def compute_payload_hash(payload: Any) -> str:
    return sha256_digest(payload)


def compute_record_hash(
    *,
    schema_version: str,
    run_id: str,
    event_type: str,
    timestamp: str,
    payload_hash: str,
    prev_hash: str | None,
) -> str:
    return sha256_digest(
        {
            "schema_version": schema_version,
            "run_id": run_id,
            "event_type": event_type,
            "timestamp": timestamp,
            "payload_hash": payload_hash,
            "prev_hash": prev_hash,
        }
    )


def compute_bundle_root_hash(record_hashes: Sequence[str]) -> str:
    chain_state: str | None = None
    for record_hash in record_hashes:
        chain_state = sha256_digest(
            {
                "prev_root": chain_state,
                "record_hash": record_hash,
            }
        )
    return chain_state or sha256_digest({"records": []})


def is_sha256_digest(value: Any) -> bool:
    return isinstance(value, str) and DIGEST_PATTERN.match(value) is not None
