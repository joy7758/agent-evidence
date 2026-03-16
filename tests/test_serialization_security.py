from agent_evidence.serialization import (
    MAX_COLLECTION_SIZE,
    MAX_STRING_LENGTH,
    to_jsonable,
)


def test_to_jsonable_redacts_sensitive_fields() -> None:
    payload = {
        "api_key": "123456",
        "prompt": "hello world",
        "nested": {"authorization": "Bearer secret"},
    }

    serialized = to_jsonable(payload)

    assert serialized["api_key"] == "[REDACTED]"
    assert serialized["prompt"] == "[REDACTED]"
    assert serialized["nested"]["authorization"] == "[REDACTED]"


def test_to_jsonable_enforces_max_depth() -> None:
    deep: dict[str, object] = {}
    cursor = deep
    for _ in range(50):
        next_value: dict[str, object] = {}
        cursor["a"] = next_value
        cursor = next_value

    serialized = to_jsonable(deep)

    assert "[MAX_DEPTH_EXCEEDED]" in str(serialized)


def test_to_jsonable_detects_cycles() -> None:
    payload: dict[str, object] = {}
    payload["self"] = payload

    serialized = to_jsonable(payload)

    assert serialized["self"] == "[CYCLE]"


def test_to_jsonable_truncates_large_strings() -> None:
    payload = "x" * (MAX_STRING_LENGTH + 1_000)

    serialized = to_jsonable(payload)

    assert serialized.endswith("...[TRUNCATED]")
    assert len(serialized) == MAX_STRING_LENGTH + len("...[TRUNCATED]")


def test_to_jsonable_limits_collection_sizes() -> None:
    payload = {
        "items": list(range(MAX_COLLECTION_SIZE + 50)),
        "mapping": {f"k{i}": i for i in range(MAX_COLLECTION_SIZE + 50)},
    }

    serialized = to_jsonable(payload)

    assert len(serialized["items"]) == MAX_COLLECTION_SIZE
    assert len(serialized["mapping"]) == MAX_COLLECTION_SIZE
