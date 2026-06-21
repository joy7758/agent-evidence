from __future__ import annotations

import json
from collections.abc import Callable, Collection
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
    values: Collection[Any],
    *,
    normalize_item: Callable[[Any], Any],
    limit: int | None = None,
) -> list[Any]:
    if limit is not None and len(values) > limit:
        raise ValueError(f"unordered collection exceeds maximum size: {len(values)} > {limit}")

    normalized_items = [normalize_item(item) for item in values]
    normalized_items.sort(key=_sort_key)
    return normalized_items
