from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path

DEFAULT_MANIFEST_PATH = Path("protocol/manifest.json")
DEFAULT_CLAUSE_INDEX_PATH = Path("protocol/clause-index.json")
DEFAULT_CLAUSES_MD_PATH = Path("docs/protocol/clauses.md")
DEFAULT_PR_TEMPLATE_PATH = Path(".github/pull_request_template.md")
CLAUSE_RE = re.compile(r"\bEEOAP-\d{3}\b")


def load_json(path: Path) -> object:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def fail(summary: dict[str, object], message: str, code: str | None = None) -> None:
    summary.setdefault("errors", []).append(message)
    if code is not None:
        error_codes = summary.setdefault("error_codes", [])
        if isinstance(error_codes, list):
            error_codes.append(code)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate EEOAP protocol citation metadata.")
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST_PATH)
    parser.add_argument("--clause-index", type=Path, default=DEFAULT_CLAUSE_INDEX_PATH)
    parser.add_argument("--clauses-md", type=Path, default=DEFAULT_CLAUSES_MD_PATH)
    parser.add_argument("--pr-template", type=Path, default=DEFAULT_PR_TEMPLATE_PATH)
    parser.add_argument(
        "--root",
        type=Path,
        default=Path.cwd(),
        help="Base directory for repository-relative paths and related_files checks.",
    )
    return parser.parse_args()


def resolve_input_path(path: Path, root: Path) -> Path:
    return path if path.is_absolute() else root / path


def display_path(path: Path, root: Path) -> str:
    try:
        return str(path.resolve().relative_to(root.resolve()))
    except ValueError:
        return str(path)


def related_file_path(path: str, root: Path) -> Path | None:
    candidate = Path(path)
    if candidate.is_absolute() or ".." in candidate.parts:
        return None
    return root / candidate


def main() -> int:
    args = parse_args()
    root = args.root.resolve()
    manifest_path = resolve_input_path(args.manifest, root)
    clause_index_path = resolve_input_path(args.clause_index, root)
    clauses_md_path = resolve_input_path(args.clauses_md, root)
    pr_template_path = resolve_input_path(args.pr_template, root)

    summary: dict[str, object] = {
        "ok": True,
        "checked_files": [
            display_path(manifest_path, root),
            display_path(clause_index_path, root),
            display_path(clauses_md_path, root),
            display_path(pr_template_path, root),
        ],
        "errors": [],
    }

    try:
        manifest = load_json(manifest_path)
        clause_index = load_json(clause_index_path)
        clauses_md = read_text(clauses_md_path)
        pr_template = read_text(pr_template_path)
    except Exception as exc:  # pragma: no cover - this is a command-line guard.
        summary["ok"] = False
        summary["errors"] = [f"load_error: {exc}"]
        print(json.dumps(summary, sort_keys=True))
        return 1

    if not isinstance(manifest, dict):
        fail(summary, "manifest_not_object")
        manifest = {}
    if not isinstance(clause_index, dict):
        fail(summary, "clause_index_not_object")
        clause_index = {}

    if manifest.get("short_name") not in (None, "EEOAP"):
        fail(summary, "manifest_short_name_not_EEOAP")
    if manifest.get("clause_prefix") not in (None, "EEOAP"):
        fail(summary, "manifest_clause_prefix_not_EEOAP")
    manifest_clause_index = manifest.get("clause_index")
    if manifest_clause_index is not None and not isinstance(manifest_clause_index, str):
        fail(summary, "manifest_clause_index_not_string")
    elif isinstance(manifest_clause_index, str):
        manifest_clause_index_path = resolve_input_path(Path(manifest_clause_index), root)
        if not manifest_clause_index_path.exists():
            fail(summary, f"manifest_clause_index_missing:{manifest_clause_index}")

    raw_clauses = clause_index.get("clauses")
    if not isinstance(raw_clauses, list):
        fail(summary, "clause_index_clauses_not_list")
        raw_clauses = []

    index_ids: list[str] = []
    missing_related_files: list[dict[str, str]] = []
    for item in raw_clauses:
        if not isinstance(item, dict):
            fail(summary, "clause_index_item_not_object")
            continue
        clause_id = item.get("clause_id")
        if not isinstance(clause_id, str):
            fail(summary, "clause_index_item_missing_clause_id")
            continue
        index_ids.append(clause_id)
        if not re.fullmatch(r"EEOAP-\d{3}", clause_id):
            fail(summary, f"invalid_clause_id_format:{clause_id}")
        related_files = item.get("related_files", [])
        if related_files is None:
            related_files = []
        if not isinstance(related_files, list):
            fail(summary, f"related_files_not_list:{clause_id}")
            continue
        for related_file in related_files:
            if not isinstance(related_file, str):
                fail(summary, f"related_file_not_string:{clause_id}")
                continue
            resolved_related_file = related_file_path(related_file, root)
            if resolved_related_file is None or not resolved_related_file.exists():
                missing_related_files.append({"clause_id": clause_id, "path": related_file})

    missing_related_files.sort(key=lambda item: (item["clause_id"], item["path"]))
    if missing_related_files:
        fail(summary, "missing_related_file", "missing_related_file")
        summary["missing_related_files"] = missing_related_files

    md_ids = sorted(set(CLAUSE_RE.findall(clauses_md)))
    index_id_set = set(index_ids)
    md_id_set = set(md_ids)
    expected_ids = {f"EEOAP-{number:03d}" for number in range(1, 6)}

    missing_from_index = sorted(md_id_set - index_id_set)
    if missing_from_index:
        fail(summary, f"clauses_md_ids_missing_from_index:{','.join(missing_from_index)}")

    missing_from_md = sorted(index_id_set - md_id_set)
    if missing_from_md:
        fail(summary, f"index_ids_missing_from_clauses_md:{','.join(missing_from_md)}")

    if index_id_set != expected_ids:
        fail(summary, "clause_index_ids_do_not_match_expected_EEOAP_001_to_005")
    if md_id_set != expected_ids:
        fail(summary, "clauses_md_ids_do_not_match_expected_EEOAP_001_to_005")

    for clause_id in sorted(expected_ids):
        if clause_id not in pr_template:
            fail(summary, f"pull_request_template_missing:{clause_id}")

    duplicate_index_ids = sorted(
        clause_id for clause_id, count in Counter(index_ids).items() if count > 1
    )
    if duplicate_index_ids:
        fail(summary, f"duplicate_index_ids:{','.join(duplicate_index_ids)}")

    summary["manifest_protocol"] = manifest.get("protocol_name")
    summary["manifest_version"] = manifest.get("version")
    summary["clause_count"] = len(index_ids)
    summary["clause_ids"] = sorted(index_id_set)
    summary["checked_related_files"] = True
    error_codes = summary.get("error_codes")
    if isinstance(error_codes, list):
        summary["error_codes"] = sorted(set(error_codes))
        if "missing_related_file" in error_codes:
            summary["error_code"] = "missing_related_file"
    summary["ok"] = not summary["errors"]

    print(json.dumps(summary, sort_keys=True))
    return 0 if summary["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
