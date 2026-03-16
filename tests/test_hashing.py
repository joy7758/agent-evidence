import math

import pytest

from agent_evidence.crypto.chain import chain_digest_for_event
from agent_evidence.crypto.hashing import canonical_json_bytes, compute_hash


def test_canonical_json_is_stable() -> None:
    left = canonical_json_bytes({"b": 1, "a": 2})
    right = canonical_json_bytes({"a": 2, "b": 1})
    assert left == right


def test_chain_digest_changes_with_previous_link() -> None:
    event_hash = compute_hash({"actor": "planner"})
    first = chain_digest_for_event(event_hash=event_hash, previous_chain_hash=None)
    second = chain_digest_for_event(event_hash=event_hash, previous_chain_hash=first)
    assert first != second


def test_canonical_json_rejects_non_finite_floats() -> None:
    with pytest.raises(ValueError):
        canonical_json_bytes({"value": math.nan})
