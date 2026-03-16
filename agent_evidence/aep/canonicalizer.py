from __future__ import annotations

import json
from datetime import date, datetime, time
from pathlib import Path
from typing import Any, Mapping
from uuid import UUID


def canonicalize(value: Any) -> Any:
    """Normalize Python values into a deterministic JSON-compatible shape."""

    if hasattr(value, "model_dump"):
        return canonicalize(value.model_dump(mode="json"))
    if isinstance(value, Mapping):
        return {
            str(key): canonicalize(item)
            for key, item in sorted(value.items(), key=lambda entry: str(entry[0]))
        }
    if isinstance(value, (list, tuple, set, frozenset)):
        return [canonicalize(item) for item in value]
    if isinstance(value, (datetime, date, time)):
        return value.isoformat()
    if isinstance(value, UUID):
        return str(value)
    if isinstance(value, Path):
        return str(value)
    return value


def canonical_json_bytes(value: Any) -> bytes:
    return json.dumps(
        canonicalize(value),
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
    ).encode("utf-8")


def canonical_json_text(value: Any) -> str:
    return canonical_json_bytes(value).decode("utf-8")
