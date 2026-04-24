from __future__ import annotations

import json
from collections.abc import Callable, Iterable
from typing import Any


def _sort_key(value: Any) -> str:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
        allow_nan=True,
    )


def canonicalize_unordered_collection(
    values: Iterable[Any],
    *,
    normalize_item: Callable[[Any], Any],
    limit: int | None = None,
) -> list[Any]:
    normalized_items = [normalize_item(item) for item in values]
    normalized_items.sort(key=_sort_key)
    if limit is not None:
        return normalized_items[:limit]
    return normalized_items
