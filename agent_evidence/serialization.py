from __future__ import annotations

from dataclasses import fields, is_dataclass
from datetime import date, datetime, time
from decimal import Decimal
from enum import Enum
from pathlib import Path
from typing import Any, Mapping, Sequence
from uuid import UUID

DEFAULT_REDACT_KEYS = {
    "api_key",
    "authorization",
    "cookie",
    "set_cookie",
    "password",
    "secret",
    "token",
    "access_token",
    "refresh_token",
    "prompt",
}
MAX_SERIALIZATION_DEPTH = 20
MAX_STRING_LENGTH = 10_000
MAX_COLLECTION_SIZE = 1_000


def redact_value(key: str, value: Any) -> Any:
    if key.lower() in DEFAULT_REDACT_KEYS:
        return "[REDACTED]"
    return value


def _truncate_string(value: str) -> str:
    if len(value) > MAX_STRING_LENGTH:
        return value[:MAX_STRING_LENGTH] + "...[TRUNCATED]"
    return value


def _object_to_mapping(value: Any) -> Mapping[str, Any] | None:
    if is_dataclass(value):
        return {field.name: getattr(value, field.name) for field in fields(value)}
    if hasattr(value, "model_dump"):
        try:
            dumped = value.model_dump(mode="python")
        except TypeError:
            dumped = value.model_dump()
        if isinstance(dumped, Mapping):
            return dumped
    if hasattr(value, "dict"):
        try:
            dumped = value.dict()
        except TypeError:
            dumped = None
        if isinstance(dumped, Mapping):
            return dumped
    return None


def _to_jsonable(value: Any, depth: int, seen: set[int]) -> Any:
    if depth > MAX_SERIALIZATION_DEPTH:
        return "[MAX_DEPTH_EXCEEDED]"

    if value is None or isinstance(value, bool | int | float):
        return value
    if isinstance(value, str):
        return _truncate_string(value)
    if isinstance(value, bytes | bytearray):
        return _truncate_string(value.decode("utf-8", errors="replace"))
    if isinstance(value, UUID | Path):
        return _truncate_string(str(value))
    if isinstance(value, Enum):
        return _to_jsonable(value.value, depth + 1, seen)
    if isinstance(value, datetime | date | time):
        return _truncate_string(value.isoformat())
    if isinstance(value, Decimal):
        return _truncate_string(str(value))

    object_id = id(value)
    if object_id in seen:
        return "[CYCLE]"

    object_mapping = _object_to_mapping(value)
    seen.add(object_id)
    try:
        if isinstance(value, BaseException):
            return {
                "type": value.__class__.__name__,
                "message": _truncate_string(str(value)),
                "args": [
                    _to_jsonable(arg, depth + 1, seen)
                    for arg in list(value.args)[:MAX_COLLECTION_SIZE]
                ],
            }
        if object_mapping is not None:
            limited_items = list(object_mapping.items())[:MAX_COLLECTION_SIZE]
            return {
                str(key): redact_value(
                    str(key),
                    _to_jsonable(item, depth + 1, seen),
                )
                for key, item in limited_items
            }
        if isinstance(value, Mapping):
            limited_items = list(value.items())[:MAX_COLLECTION_SIZE]
            return {
                str(key): redact_value(
                    str(key),
                    _to_jsonable(item, depth + 1, seen),
                )
                for key, item in limited_items
            }
        if isinstance(value, Sequence) and not isinstance(value, str | bytes | bytearray):
            return [
                _to_jsonable(item, depth + 1, seen) for item in list(value)[:MAX_COLLECTION_SIZE]
            ]
        if isinstance(value, set | frozenset):
            return [
                _to_jsonable(item, depth + 1, seen) for item in list(value)[:MAX_COLLECTION_SIZE]
            ]
        return _truncate_string(repr(value))
    finally:
        seen.remove(object_id)


def to_jsonable(value: Any) -> Any:
    """Best-effort conversion for evidence payloads that may contain runtime objects."""

    return _to_jsonable(value, depth=0, seen=set())


def ensure_json_object(value: Any) -> dict[str, Any]:
    if value is None:
        return {}

    normalized = to_jsonable(value)
    if isinstance(normalized, dict):
        return normalized
    return {"value": normalized}
