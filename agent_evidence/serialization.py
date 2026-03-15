from __future__ import annotations

from dataclasses import asdict, is_dataclass
from datetime import date, datetime, time
from decimal import Decimal
from enum import Enum
from pathlib import Path
from typing import Any, Mapping, Sequence
from uuid import UUID


def to_jsonable(value: Any) -> Any:
    """Best-effort conversion for evidence payloads that may contain runtime objects."""

    if value is None or isinstance(value, str | int | float | bool):
        return value
    if isinstance(value, bytes | bytearray):
        return value.decode("utf-8", errors="replace")
    if isinstance(value, UUID | Path):
        return str(value)
    if isinstance(value, Enum):
        return to_jsonable(value.value)
    if isinstance(value, datetime | date | time):
        return value.isoformat()
    if isinstance(value, Decimal):
        return str(value)
    if isinstance(value, BaseException):
        return {
            "type": value.__class__.__name__,
            "message": str(value),
            "args": [to_jsonable(arg) for arg in value.args],
        }
    if is_dataclass(value):
        return to_jsonable(asdict(value))
    if hasattr(value, "model_dump"):
        try:
            return to_jsonable(value.model_dump(mode="json"))
        except TypeError:
            return to_jsonable(value.model_dump())
    if hasattr(value, "dict"):
        try:
            return to_jsonable(value.dict())
        except TypeError:
            pass
    if isinstance(value, Mapping):
        return {str(key): to_jsonable(item) for key, item in value.items()}
    if isinstance(value, Sequence) and not isinstance(value, str | bytes | bytearray):
        return [to_jsonable(item) for item in value]
    return repr(value)


def ensure_json_object(value: Any) -> dict[str, Any]:
    if value is None:
        return {}

    normalized = to_jsonable(value)
    if isinstance(normalized, dict):
        return normalized
    return {"value": normalized}
