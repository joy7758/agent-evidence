from agent_evidence.crypto.chain import chain_digest_for_record
from agent_evidence.crypto.hashing import canonical_json_bytes, hash_payload


def test_canonical_json_is_stable() -> None:
    left = canonical_json_bytes({"b": 1, "a": 2})
    right = canonical_json_bytes({"a": 2, "b": 1})
    assert left == right


def test_chain_digest_changes_with_previous_link() -> None:
    payload_digest = hash_payload({"actor": "planner"})
    first = chain_digest_for_record(payload_digest=payload_digest, previous_digest=None)
    second = chain_digest_for_record(payload_digest=payload_digest, previous_digest=first)
    assert first != second
