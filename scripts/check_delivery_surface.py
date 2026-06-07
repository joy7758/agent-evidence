from __future__ import annotations

import argparse
import fnmatch
import json
from pathlib import Path, PurePosixPath
from typing import Any

DEFAULT_SURFACE_PATH = Path("packaging/commercial-delivery-surface.json")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate the commercial delivery surface.")
    parser.add_argument("--surface", type=Path, default=DEFAULT_SURFACE_PATH)
    parser.add_argument(
        "--root",
        type=Path,
        default=Path.cwd(),
        help="Repository root for resolving delivery-surface paths.",
    )
    return parser.parse_args()


def resolve_input_path(path: Path, root: Path) -> Path:
    return path if path.is_absolute() else root / path


def display_path(path: Path, root: Path) -> str:
    try:
        return str(path.resolve().relative_to(root.resolve()))
    except ValueError:
        return str(path)


def load_surface(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)
    if not isinstance(payload, dict):
        raise ValueError("delivery_surface_not_object")
    return payload


def repo_relative_parts(path: str) -> tuple[str, ...] | None:
    candidate = PurePosixPath(path)
    if not path or path.startswith("/") or "\\" in path or ".." in candidate.parts:
        return None
    return tuple(part for part in candidate.parts if part not in ("", "."))


def contains_subsequence(parts: tuple[str, ...], pattern_parts: tuple[str, ...]) -> bool:
    if not pattern_parts:
        return False
    if len(pattern_parts) > len(parts):
        return False
    for start in range(0, len(parts) - len(pattern_parts) + 1):
        if parts[start : start + len(pattern_parts)] == pattern_parts:
            return True
    return False


def path_matches_excluded_pattern(path: str, pattern: str) -> bool:
    parts = repo_relative_parts(path)
    if parts is None:
        return True

    normalized_pattern = pattern.strip()
    if not normalized_pattern:
        return False

    if normalized_pattern.endswith("/"):
        pattern_parts = tuple(
            part for part in PurePosixPath(normalized_pattern.rstrip("/")).parts if part
        )
        return contains_subsequence(parts, pattern_parts)

    joined = "/".join(parts)
    basename = parts[-1]
    path_matches = fnmatch.fnmatch(joined, normalized_pattern)
    basename_matches = fnmatch.fnmatch(basename, normalized_pattern)
    if path_matches or basename_matches:
        return True

    return any(fnmatch.fnmatch(part, normalized_pattern) for part in parts)


def list_strings(payload: dict[str, Any], key: str) -> list[str]:
    raw_value = payload.get(key, [])
    if not isinstance(raw_value, list):
        raise ValueError(f"{key}_not_list")
    values: list[str] = []
    for item in raw_value:
        if not isinstance(item, str):
            raise ValueError(f"{key}_item_not_string")
        values.append(item)
    return values


def emit(payload: dict[str, Any], exit_code: int) -> int:
    print(json.dumps(payload, sort_keys=True))
    return exit_code


def main() -> int:
    args = parse_args()
    root = args.root.resolve()
    surface_path = resolve_input_path(args.surface, root)

    try:
        surface = load_surface(surface_path)
        included_paths = list_strings(surface, "included_paths")
        excluded_patterns = list_strings(surface, "excluded_patterns")
    except Exception as exc:  # pragma: no cover - command-line guard.
        return emit(
            {
                "ok": False,
                "checked_surface": display_path(surface_path, root),
                "error_code": "delivery_surface_load_error",
                "error": str(exc),
            },
            1,
        )

    forbidden: list[str] = []
    missing: list[str] = []

    for include_path in included_paths:
        parts = repo_relative_parts(include_path)
        if parts is None:
            forbidden.append(include_path)
            continue

        if any(
            path_matches_excluded_pattern(include_path, pattern) for pattern in excluded_patterns
        ):
            forbidden.append(include_path)
            continue

        resolved = root / Path(*parts)
        if not resolved.exists():
            missing.append(include_path)

    forbidden = sorted(set(forbidden))
    missing = sorted(set(missing))

    if forbidden:
        return emit(
            {
                "ok": False,
                "checked_surface": display_path(surface_path, root),
                "error_code": "forbidden_delivery_surface_path",
                "forbidden": forbidden,
            },
            1,
        )

    if missing:
        return emit(
            {
                "ok": False,
                "checked_surface": display_path(surface_path, root),
                "error_code": "missing_delivery_surface_path",
                "missing": missing,
            },
            1,
        )

    return emit(
        {
            "ok": True,
            "checked_surface": display_path(surface_path, root),
            "included_count": len(included_paths),
            "status": "surface_ok",
        },
        0,
    )


if __name__ == "__main__":
    raise SystemExit(main())
