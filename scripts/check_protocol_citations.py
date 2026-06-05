from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "protocol" / "manifest.json"
CLAUSE_INDEX_PATH = ROOT / "protocol" / "clause-index.json"
CLAUSES_MD_PATH = ROOT / "docs" / "protocol" / "clauses.md"
PR_TEMPLATE_PATH = ROOT / ".github" / "pull_request_template.md"
CLAUSE_RE = re.compile(r"\bEEOAP-\d{3}\b")


def load_json(path: Path) -> object:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def fail(summary: dict[str, object], message: str) -> None:
    summary.setdefault("errors", []).append(message)


def main() -> int:
    summary: dict[str, object] = {
        "ok": True,
        "checked_files": [
            str(MANIFEST_PATH.relative_to(ROOT)),
            str(CLAUSE_INDEX_PATH.relative_to(ROOT)),
            str(CLAUSES_MD_PATH.relative_to(ROOT)),
            str(PR_TEMPLATE_PATH.relative_to(ROOT)),
        ],
        "errors": [],
    }

    try:
        manifest = load_json(MANIFEST_PATH)
        clause_index = load_json(CLAUSE_INDEX_PATH)
        clauses_md = read_text(CLAUSES_MD_PATH)
        pr_template = read_text(PR_TEMPLATE_PATH)
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

    if manifest.get("short_name") != "EEOAP":
        fail(summary, "manifest_short_name_not_EEOAP")
    if manifest.get("clause_prefix") != "EEOAP":
        fail(summary, "manifest_clause_prefix_not_EEOAP")

    raw_clauses = clause_index.get("clauses")
    if not isinstance(raw_clauses, list):
        fail(summary, "clause_index_clauses_not_list")
        raw_clauses = []

    index_ids: list[str] = []
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
    summary["ok"] = not summary["errors"]

    print(json.dumps(summary, sort_keys=True))
    return 0 if summary["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
