import math

import pytest

from agent_evidence.aep.canonicalizer import canonical_json_bytes as aep_canonical_json_bytes
from agent_evidence.crypto.chain import chain_digest_for_event
from agent_evidence.crypto.hashing import canonical_json_bytes, compute_hash
from agent_evidence.serialization import to_jsonable


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


def test_aep_canonical_json_sorts_unordered_collections() -> None:
    payload = {
        "tags": {"beta", "alpha"},
        "nested": frozenset({("team", "ops"), ("team", "ml")}),
    }

    expected = b'{"nested":[["team","ml"],["team","ops"]],"tags":["alpha","beta"]}'

    assert aep_canonical_json_bytes(payload) == expected


def test_hash_is_stable_for_jsonable_payloads_with_sets() -> None:
    left = {
        "tags": {"beta", "alpha"},
        "nested": frozenset({("team", "ops"), ("team", "ml")}),
    }
    right = {
        "tags": {"alpha", "beta"},
        "nested": frozenset({("team", "ml"), ("team", "ops")}),
    }

    assert compute_hash(to_jsonable(left)) == compute_hash(to_jsonable(right))


def test_unordered_collection_with_mixed_jsonable_types_is_stable() -> None:
    left = {"values": {1, "1", None}}
    right = {"values": {None, "1", 1}}

    left_aep = aep_canonical_json_bytes(left)
    right_aep = aep_canonical_json_bytes(right)

    assert left_aep == right_aep
    assert compute_hash(to_jsonable(left)) == compute_hash(to_jsonable(right))
