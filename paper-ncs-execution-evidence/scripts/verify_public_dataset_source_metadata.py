#!/usr/bin/env python3
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import html
import json
import re
import sys
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

DOI = "10.5281/zenodo.826906"
ZENODO_RECORD_ID = 826906
ZENODO_RECORD_URL = "https://zenodo.org/records/826906"
ZENODO_API_URL = "https://zenodo.org/api/records/826906"
DATACITE_API_URL = "https://api.datacite.org/dois/10.5281/zenodo.826906"
RELATED_PUBLICATION_DOI = "10.1186/s12864-017-3692-8"
GEO_ACCESSION = "GSE82128"
BIOLOGICAL_CONTEXT = "Drosophila small RNA-seq"

EXPECTED_FILES = {
    "Blank_RNAi_sRNA-seq_rep1_downsampled.fastqsanger.gz": "6638232f458ed3abbb642d2eb59a5c2b",
    "Blank_RNAi_sRNA-seq_rep2_downsampled.fastqsanger.gz": "d9e71d0c98d7c3102a02c9ce69343f84",
    "Blank_RNAi_sRNA-seq_rep3_downsampled.fastqsanger.gz": "782a05b6387f7d98372f75ac9033db1f",
    "Symp_RNAi_sRNA-seq_rep1_downsampled.fastqsanger.gz": "c9119dbc9d50ab654eb55dfc48548257",
    "Symp_RNAi_sRNA-seq_rep2_downsampled.fastqsanger.gz": "c0ad66cf30bc5bd8056f86ea6efe52b2",
    "Symp_RNAi_sRNA-seq_rep3_downsampled.fastqsanger.gz": "c12859e9a9f8ea88fe0e047751038b00",
}

EXIT_LICENSE = 12
EXIT_CHECKSUM = 13
EXIT_CONTEXT = 14
EXIT_NETWORK = 15
EXIT_LOCAL_MISSING = 16


class VerificationError(Exception):
    def __init__(self, code: int, message: str) -> None:
        super().__init__(message)
        self.code = code


def paper_root() -> Path:
    return Path(__file__).resolve().parents[1]


def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat().replace("+00:00", "Z")


def write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(obj, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
        encoding="utf-8",
    )


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256_bytes(data: bytes) -> str:
    return "sha256:" + hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def md5_file(path: Path) -> str:
    return hashlib.md5(path.read_bytes()).hexdigest()


def fetch_json_bytes(url: str, timeout_seconds: int) -> tuple[bytes, Any]:
    request = urllib.request.Request(url, headers={"Accept": "application/json"})
    with urllib.request.urlopen(request, timeout=timeout_seconds) as response:
        raw = response.read()
    return raw, json.loads(raw.decode("utf-8"))


def direct_download_url(filename: str) -> str:
    quoted = urllib.parse.quote(filename)
    return f"https://zenodo.org/records/{ZENODO_RECORD_ID}/files/{quoted}?download=1"


def strip_html(text: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", html.unescape(text))).strip()


def lowercase_blob(*values: Any) -> str:
    parts: list[str] = []
    for value in values:
        if value is None:
            continue
        if isinstance(value, str):
            parts.append(strip_html(value))
        else:
            parts.append(json.dumps(value, ensure_ascii=False, sort_keys=True))
    return "\n".join(parts).lower()


def nested_license_candidates(obj: Any, source: str) -> list[dict[str, Any]]:
    candidates: list[dict[str, Any]] = []
    license_keys = {
        "id",
        "title",
        "url",
        "rights",
        "rights_uri",
        "rightsidentifier",
        "rightsuri",
        "rightsidentifierscheme",
    }

    def walk(value: Any, path: str) -> None:
        if isinstance(value, dict):
            lowered = {str(k).lower(): v for k, v in value.items()}
            if license_keys.intersection(lowered):
                candidate = {
                    "id": lowered.get("id") or lowered.get("rightsidentifier"),
                    "title": lowered.get("title") or lowered.get("rights"),
                    "url": (
                        lowered.get("url") or lowered.get("rights_uri") or lowered.get("rightsuri")
                    ),
                    "source": source,
                    "source_path": path,
                    "raw": value,
                }
                if candidate["id"] or candidate["title"] or candidate["url"]:
                    candidates.append(candidate)
            for key, child in value.items():
                walk(child, f"{path}.{key}" if path else str(key))
        elif isinstance(value, list):
            for index, child in enumerate(value):
                walk(child, f"{path}[{index}]")

    walk(obj, "")
    return candidates


def canonical_license_key(candidate: dict[str, Any]) -> str | None:
    blob = lowercase_blob(candidate.get("id"), candidate.get("title"), candidate.get("url"))
    if "creativecommons.org/licenses/by/4.0" in blob:
        return "cc-by-4.0"
    if "cc-by-4.0" in blob or "cc by 4.0" in blob:
        return "cc-by-4.0"
    if "creative commons attribution 4.0" in blob:
        return "cc-by-4.0"
    if "open access" in blob and not any(
        token in blob for token in ["creative commons", "cc-by", "license"]
    ):
        return None
    if candidate.get("id"):
        return str(candidate["id"]).strip().lower()
    if candidate.get("url"):
        return str(candidate["url"]).strip().lower()
    if candidate.get("title"):
        return str(candidate["title"]).strip().lower()
    return None


def select_license(zenodo: Any, datacite: Any) -> tuple[str, dict[str, Any], list[dict[str, Any]]]:
    zmeta = zenodo.get("metadata", {})
    dattrs = datacite.get("data", {}).get("attributes", {})
    candidates: list[dict[str, Any]] = []

    for key in ["license", "licenses", "rights", "access_right"]:
        if key in zmeta:
            candidates.extend(nested_license_candidates({key: zmeta[key]}, "Zenodo API"))
    if "access" in zenodo:
        candidates.extend(nested_license_candidates({"access": zenodo["access"]}, "Zenodo API"))

    for key in ["rightsList", "rights"]:
        if key in dattrs:
            candidates.extend(nested_license_candidates({key: dattrs[key]}, "DataCite API"))

    concrete: list[tuple[str, dict[str, Any]]] = []
    for candidate in candidates:
        key = canonical_license_key(candidate)
        if key:
            concrete.append((key, candidate))

    if not concrete:
        return "unknown", {}, candidates

    keys = {key for key, _candidate in concrete}
    if len(keys) > 1:
        return "conflict", {"conflicting_keys": sorted(keys)}, candidates

    selected_key = concrete[0][0]
    selected = {
        "id": selected_key,
        "title": "Creative Commons Attribution 4.0" if selected_key == "cc-by-4.0" else None,
        "url": (
            "https://creativecommons.org/licenses/by/4.0" if selected_key == "cc-by-4.0" else None
        ),
        "source": "Zenodo API / DataCite API",
    }
    for _key, candidate in concrete:
        if not selected.get("title") and candidate.get("title"):
            selected["title"] = candidate["title"]
        if not selected.get("url") and candidate.get("url"):
            selected["url"] = candidate["url"]
        if candidate.get("source") == "Zenodo API" and candidate.get("id"):
            selected["id"] = str(candidate["id"]).strip().lower()
    return "verified", selected, candidates


def zenodo_file_index(zenodo: Any) -> dict[str, dict[str, Any]]:
    return {item.get("key") or item.get("filename"): item for item in zenodo.get("files", [])}


def checksum_md5(value: str | None) -> str | None:
    if not value:
        return None
    value = value.strip()
    if value.startswith("md5:"):
        return value.split(":", 1)[1]
    return value


def related_identifiers(zenodo: Any, datacite: Any) -> list[dict[str, Any]]:
    values: list[dict[str, Any]] = []
    for item in zenodo.get("metadata", {}).get("related_identifiers", []) or []:
        values.append({"source": "Zenodo API", **item})
    for item in datacite.get("data", {}).get("attributes", {}).get("relatedIdentifiers", []) or []:
        values.append({"source": "DataCite API", **item})
    return values


def verify_context(zenodo: Any, datacite: Any) -> None:
    zmeta = zenodo.get("metadata", {})
    dattrs = datacite.get("data", {}).get("attributes", {})
    doi = zmeta.get("doi") or zenodo.get("doi") or dattrs.get("doi")
    if str(doi).lower() != DOI:
        raise VerificationError(EXIT_CONTEXT, f"DOI mismatch: {doi}")
    if int(zenodo.get("id", 0)) != ZENODO_RECORD_ID:
        raise VerificationError(EXIT_CONTEXT, f"Zenodo record id mismatch: {zenodo.get('id')}")

    title = zmeta.get("title") or " ".join(
        item.get("title", "") for item in dattrs.get("titles", []) or []
    )
    if not re.search(r"small\s+rna-seq", title, flags=re.IGNORECASE):
        raise VerificationError(EXIT_CONTEXT, f"title does not identify small RNA-seq: {title}")

    creators_blob = lowercase_blob(zmeta.get("creators"), dattrs.get("creators"))
    if "freeberg" not in creators_blob:
        raise VerificationError(EXIT_CONTEXT, "creator list does not include Freeberg")

    description_blob = lowercase_blob(zmeta.get("description"), dattrs.get("descriptions"))
    for token in ["drosophila", "gse82128", "harrington"]:
        if token not in description_blob:
            raise VerificationError(EXIT_CONTEXT, f"description missing {token}")

    related_blob = lowercase_blob(related_identifiers(zenodo, datacite))
    if RELATED_PUBLICATION_DOI not in related_blob:
        raise VerificationError(EXIT_CONTEXT, f"related DOI missing: {RELATED_PUBLICATION_DOI}")


def verify_files(pack: Path, zenodo: Any) -> list[dict[str, Any]]:
    file_index = zenodo_file_index(zenodo)
    records: list[dict[str, Any]] = []
    for filename, expected_md5 in EXPECTED_FILES.items():
        zfile = file_index.get(filename)
        if not zfile:
            raise VerificationError(EXIT_CHECKSUM, f"Zenodo file metadata missing: {filename}")

        zenodo_md5 = checksum_md5(zfile.get("checksum"))
        if zenodo_md5 != expected_md5:
            raise VerificationError(
                EXIT_CHECKSUM,
                (
                    f"Zenodo MD5 mismatch for {filename}: "
                    f"expected {expected_md5}, observed {zenodo_md5}"
                ),
            )

        local_path = pack / "inputs" / filename
        if not local_path.exists():
            raise VerificationError(EXIT_LOCAL_MISSING, f"local pack input missing: {local_path}")

        local_md5 = md5_file(local_path)
        if local_md5 != expected_md5:
            raise VerificationError(
                EXIT_CHECKSUM,
                f"local MD5 mismatch for {filename}: expected {expected_md5}, observed {local_md5}",
            )

        links = zfile.get("links") or {}
        records.append(
            {
                "download_url": links.get("self") or direct_download_url(filename),
                "expected_md5": expected_md5,
                "filename": filename,
                "local_md5": local_md5,
                "local_path": f"inputs/{filename}",
                "local_sha256": sha256_file(local_path),
                "size_bytes": zfile.get("size") or local_path.stat().st_size,
                "zenodo_md5": zenodo_md5,
            }
        )
    return records


def build_record(
    pack: Path,
    zenodo_raw: bytes,
    zenodo: Any,
    datacite_raw: bytes,
    datacite: Any,
    *,
    allow_unknown_license: bool,
) -> tuple[int, dict[str, Any]]:
    verify_context(zenodo, datacite)
    files = verify_files(pack, zenodo)
    license_status, license_info, license_candidates = select_license(zenodo, datacite)

    if license_status == "conflict":
        code = EXIT_LICENSE
        verification_status = "BLOCKED"
    elif license_status == "unknown" and not allow_unknown_license:
        code = EXIT_LICENSE
        verification_status = "BLOCKED"
    else:
        code = 0
        verification_status = "PASS"

    zmeta = zenodo.get("metadata", {})
    dattrs = datacite.get("data", {}).get("attributes", {})
    title = zmeta.get("title") or " ".join(
        item.get("title", "") for item in dattrs.get("titles", []) or []
    )
    creators = [
        item.get("name")
        or " ".join(part for part in [item.get("givenName"), item.get("familyName")] if part)
        for item in (zmeta.get("creators") or dattrs.get("creators") or [])
    ]
    record = {
        "access_right": zmeta.get("access_right"),
        "biological_context": BIOLOGICAL_CONTEXT,
        "creators": creators,
        "datacite_api_url": DATACITE_API_URL,
        "doi": DOI,
        "files": files,
        "geo_accession": GEO_ACCESSION,
        "license": license_info,
        "license_candidates": license_candidates,
        "license_status": license_status,
        "notes": [
            (
                "The public pack does not assert biological conclusions; "
                "it tests verifiable execution evidence."
            ),
            "Tutorial-content license is not used as a substitute for Zenodo data-file license.",
        ],
        "publication_date": zmeta.get("publication_date") or dattrs.get("publicationYear"),
        "raw_snapshot_digests": {
            "datacite_api_sha256": sha256_bytes(datacite_raw),
            "zenodo_api_sha256": sha256_bytes(zenodo_raw),
        },
        "related_identifiers": related_identifiers(zenodo, datacite),
        "related_publication_doi": RELATED_PUBLICATION_DOI,
        "resource_type": zmeta.get("resource_type", {}).get("title")
        or dattrs.get("types", {}).get("resourceTypeGeneral"),
        "title": title,
        "tutorial_content_license_not_data_file_license": True,
        "verification_status": verification_status,
        "verified_at_utc": utc_now(),
        "zenodo_api_url": ZENODO_API_URL,
        "zenodo_record_id": ZENODO_RECORD_ID,
        "zenodo_record_url": ZENODO_RECORD_URL,
    }
    return code, record


def write_note(path: Path, record: dict[str, Any]) -> None:
    license_info = record.get("license") or {}
    content = f"""# Public dataset source metadata verification

## Dataset

- Zenodo DOI: `{record.get("doi")}`
- Zenodo record: `{record.get("zenodo_record_url")}`
- DataCite API: `{record.get("datacite_api_url")}`
- Related publication DOI: `{record.get("related_publication_doi")}`
- GEO accession: `{record.get("geo_accession")}`

## Verification result

- Verification status: `{record.get("verification_status")}`
- License status: `{record.get("license_status")}`
- License id: `{license_info.get("id")}`
- License title: `{license_info.get("title")}`
- License URL: `{license_info.get("url")}`
- License source: `{license_info.get("source")}`
- Verified at UTC: `{record.get("verified_at_utc")}`

## File checks

All six target FASTQ files were checked against Zenodo API file metadata and local pack
inputs. The compact JSON record stores Zenodo MD5, local MD5 and local SHA-256 values
for each input file.

## Boundary

The GTN tutorial content license is not treated as the data-file license. The data-file
license is taken from Zenodo/DataCite metadata only.

The public pack does not assert a biological conclusion; it tests validator-backed
execution evidence over a public scientific workflow.
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def copy_record_to_pack(pack: Path, record: dict[str, Any]) -> None:
    write_json(pack / "source_metadata_verification.json", record)


def run(args: argparse.Namespace) -> int:
    root = paper_root()
    source_root = root / "source_metadata"
    raw_root = source_root / "raw"
    record_path = source_root / "public_dataset_source_metadata_verification.json"
    zenodo_raw_path = raw_root / "zenodo_826906_record_api.json"
    datacite_raw_path = raw_root / "datacite_10.5281_zenodo.826906.json"
    note_path = root / "manuscript" / "public_dataset_source_metadata.md"

    if not args.refresh and record_path.exists():
        existing = load_json(record_path)
        if existing.get("verification_status") == "PASS":
            if args.write:
                copy_record_to_pack(args.pack, existing)
                write_note(note_path, existing)
            print(f"Reused verified source metadata record: {record_path}")
            return 0 if existing.get("license_status") == "verified" else EXIT_LICENSE

    try:
        zenodo_raw, zenodo = fetch_json_bytes(ZENODO_API_URL, args.timeout_seconds)
        datacite_raw, datacite = fetch_json_bytes(DATACITE_API_URL, args.timeout_seconds)
    except Exception as exc:
        print(f"ERROR: API/network failure: {exc}", file=sys.stderr)
        return EXIT_NETWORK

    try:
        code, record = build_record(
            args.pack,
            zenodo_raw,
            zenodo,
            datacite_raw,
            datacite,
            allow_unknown_license=args.allow_unknown_license,
        )
    except VerificationError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return exc.code

    if args.write:
        raw_root.mkdir(parents=True, exist_ok=True)
        zenodo_raw_path.write_bytes(zenodo_raw)
        datacite_raw_path.write_bytes(datacite_raw)
        write_json(record_path, record)
        copy_record_to_pack(args.pack, record)
        write_note(note_path, record)

    if code == 0:
        print(f"PASS: source metadata verified: {record_path}")
    else:
        print(
            (
                "BLOCKED: source metadata "
                f"license_status={record.get('license_status')}: {record_path}"
            ),
            file=sys.stderr,
        )
    return code


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Verify Zenodo/DataCite source metadata for the public NCS dataset."
    )
    parser.add_argument("--pack", required=True, type=Path)
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--refresh", action="store_true")
    parser.add_argument("--allow-unknown-license", action="store_true")
    parser.add_argument("--timeout-seconds", type=int, default=30)
    return run(parser.parse_args(argv))


if __name__ == "__main__":
    raise SystemExit(main())
