#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import sys
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

PACK_ID = "ncs-scientific-workflow-drosophila-srna-qc-public-v0.1"
PROFILE_NAME = "execution-evidence-operation-accountability"
PROFILE_VERSION = "ncs-v1.0-draft"
OPERATION_TYPE = "fastq_qc"
OPERATION_TOOL = "paper-fastq-qc-v0.2"
DOI = "10.5281/zenodo.826906"
ZENODO_RECORD_URL = "https://zenodo.org/records/826906"
SOURCE_DESCRIPTION = "Galaxy Training Network small RNA-seq tutorial dataset."
BIOLOGICAL_CONTEXT = "Downsampled Drosophila small RNA-seq FASTQ data from Harrington et al."
GEO_ACCESSION = "GSE82128"
EXECUTION_START = "2026-04-24T00:10:00Z"
EXECUTION_END = "2026-04-24T00:10:01Z"
VALIDATION_TIME = "2026-04-24T00:10:02Z"
RECEIPT_GENERATED_AT = "2026-04-24T00:10:03Z"
SOURCE_METADATA_RECORD = "source_metadata/public_dataset_source_metadata_verification.json"

FILES = [
    {
        "id": "blank_rnai_rep1",
        "filename": "Blank_RNAi_sRNA-seq_rep1_downsampled.fastqsanger.gz",
        "expected_md5": "6638232f458ed3abbb642d2eb59a5c2b",
    },
    {
        "id": "blank_rnai_rep2",
        "filename": "Blank_RNAi_sRNA-seq_rep2_downsampled.fastqsanger.gz",
        "expected_md5": "d9e71d0c98d7c3102a02c9ce69343f84",
    },
    {
        "id": "blank_rnai_rep3",
        "filename": "Blank_RNAi_sRNA-seq_rep3_downsampled.fastqsanger.gz",
        "expected_md5": "782a05b6387f7d98372f75ac9033db1f",
    },
    {
        "id": "symp_rnai_rep1",
        "filename": "Symp_RNAi_sRNA-seq_rep1_downsampled.fastqsanger.gz",
        "expected_md5": "c9119dbc9d50ab654eb55dfc48548257",
    },
    {
        "id": "symp_rnai_rep2",
        "filename": "Symp_RNAi_sRNA-seq_rep2_downsampled.fastqsanger.gz",
        "expected_md5": "c0ad66cf30bc5bd8056f86ea6efe52b2",
    },
    {
        "id": "symp_rnai_rep3",
        "filename": "Symp_RNAi_sRNA-seq_rep3_downsampled.fastqsanger.gz",
        "expected_md5": "c12859e9a9f8ea88fe0e047751038b00",
    },
]

FAILURE_CASES = {
    "tampered_input": 2,
    "tampered_output": 2,
    "missing_policy": 5,
    "broken_evidence_link": 11,
    "version_mismatch": 4,
    "temporal_inconsistency": 6,
    "outcome_unverifiable": 7,
}


def canonical_json(obj: Any) -> bytes:
    return json.dumps(
        obj,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def sha256_json(obj: Any) -> str:
    return "sha256:" + hashlib.sha256(canonical_json(obj)).hexdigest()


def sha256_file(path: Path) -> str:
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def md5_file(path: Path) -> str:
    return hashlib.md5(path.read_bytes()).hexdigest()


def write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(obj, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
        encoding="utf-8",
    )


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def load_verified_source_metadata(paper_root: Path) -> dict[str, Any] | None:
    path = paper_root / SOURCE_METADATA_RECORD
    if not path.exists():
        return None
    metadata = load_json(path)
    if metadata.get("verification_status") != "PASS":
        return None
    return metadata


def source_metadata_file_index(source_metadata: dict[str, Any] | None) -> dict[str, dict[str, Any]]:
    if not source_metadata:
        return {}
    return {item.get("filename"): item for item in source_metadata.get("files", [])}


def source_license(source_metadata: dict[str, Any] | None) -> dict[str, Any]:
    if source_metadata and source_metadata.get("license_status") == "verified":
        license_info = source_metadata.get("license") or {}
        return {
            "id": license_info.get("id"),
            "source": license_info.get("source"),
            "status": "verified",
            "title": license_info.get("title"),
            "url": license_info.get("url"),
            "verified_at_utc": source_metadata.get("verified_at_utc"),
        }
    return {
        "note": "License could not be verified from Zenodo/DataCite metadata.",
        "status": "unknown",
    }


def direct_download_url(filename: str) -> str:
    return "https://zenodo.org/records/826906/files/" + urllib.parse.quote(filename) + "?download=1"


def reset_generated_pack_content(pack: Path) -> None:
    for name in [
        "bundle.json",
        "dataset_source_manifest.json",
        "expected_digest.txt",
        "manifest.json",
        "policy.json",
        "provenance.json",
        "receipt.json",
        "source_metadata_verification.json",
        "summary.json",
    ]:
        target = pack / name
        if target.exists():
            target.unlink()

    for name in ["outputs", "evidence", "failures", "repo_compat"]:
        target = pack / name
        if target.exists():
            shutil.rmtree(target)


def download_file(url: str, path: Path) -> None:
    temp_path = path.with_suffix(path.suffix + ".download")
    with urllib.request.urlopen(url, timeout=120) as response:
        with temp_path.open("wb") as handle:
            shutil.copyfileobj(response, handle)
    temp_path.replace(path)


def prepare_inputs(pack: Path, *, skip_download: bool, offline: bool) -> list[dict[str, Any]]:
    inputs_dir = pack / "inputs"
    inputs_dir.mkdir(parents=True, exist_ok=True)
    records: list[dict[str, Any]] = []
    for item in FILES:
        filename = item["filename"]
        path = inputs_dir / filename
        url = direct_download_url(filename)
        expected_md5 = item["expected_md5"]
        status = "cached"

        if path.exists() and md5_file(path) == expected_md5:
            status = "cached"
        elif skip_download or offline:
            raise RuntimeError(f"missing or invalid input and download disabled: {path}")
        else:
            download_file(url, path)
            status = "downloaded"

        observed_md5 = md5_file(path)
        if observed_md5 != expected_md5:
            raise RuntimeError(
                f"MD5 mismatch for {filename}: expected {expected_md5}, observed {observed_md5}"
            )
        records.append(
            {
                "direct_download_url": url,
                "doi": DOI,
                "expected_md5": expected_md5,
                "file_size_bytes": path.stat().st_size,
                "filename": filename,
                "id": item["id"],
                "local_path": f"inputs/{filename}",
                "observed_md5": observed_md5,
                "retrieval_status": status,
                "sha256": sha256_file(path),
                "zenodo_record": ZENODO_RECORD_URL,
            }
        )
    return records


def write_dataset_source_manifest(
    pack: Path,
    input_records: list[dict[str, Any]],
    source_metadata: dict[str, Any] | None,
) -> dict[str, Any]:
    source_files = source_metadata_file_index(source_metadata)
    files: list[dict[str, Any]] = []
    for item in input_records:
        source_file = source_files.get(item["filename"], {})
        files.append(
            {
                **item,
                "local_md5_verified_from_source_metadata": source_file.get("local_md5"),
                "local_sha256_verified_from_source_metadata": source_file.get("local_sha256"),
                "zenodo_md5": source_file.get("zenodo_md5"),
            }
        )

    manifest = {
        "biological_context": BIOLOGICAL_CONTEXT,
        "doi": DOI,
        "files": files,
        "geo_accession": GEO_ACCESSION,
        "license": source_license(source_metadata),
        "notes": [
            "Data are public, downsampled, reviewer-lightweight FASTQ files.",
            (
                "The pack does not assert biological conclusions; "
                "it tests verifiable execution evidence."
            ),
            (
                "Zenodo/DataCite metadata is used for data-file license status, "
                "not the GTN tutorial content license."
            ),
        ],
        "source_description": SOURCE_DESCRIPTION,
        "source_metadata_status": "verified" if source_metadata else "unverified",
        "source_metadata_verification": (
            "source_metadata_verification.json" if source_metadata else None
        ),
        "zenodo_record_url": ZENODO_RECORD_URL,
    }
    write_json(pack / "dataset_source_manifest.json", manifest)
    return manifest


def run_workflow(pack: Path, workflow_script: Path, input_records: list[dict[str, Any]]) -> None:
    metrics_path = pack / "outputs" / "qc_metrics.json"
    report_path = pack / "outputs" / "qc_report.txt"
    metrics_path.parent.mkdir(parents=True, exist_ok=True)

    command = [sys.executable, str(workflow_script)]
    for item in input_records:
        command.extend(["--input", str(pack / item["local_path"])])
    command.extend(["--metrics", str(metrics_path), "--report", str(report_path)])
    subprocess.run(command, check=True)


def workflow_command(input_records: list[dict[str, Any]]) -> list[str]:
    command = ["python", "evidence/run_fastq_qc.py"]
    for item in input_records:
        command.extend(["--input", item["local_path"]])
    command.extend(["--metrics", "outputs/qc_metrics.json", "--report", "outputs/qc_report.txt"])
    return command


def build_policy(
    input_records: list[dict[str, Any]],
    source_metadata_present: bool,
) -> dict[str, Any]:
    required_artifacts = [
        "manifest.json",
        "bundle.json",
        "receipt.json",
        "summary.json",
        "dataset_source_manifest.json",
        "outputs/qc_metrics.json",
        "outputs/qc_report.txt",
        "evidence/run_fastq_qc.py",
        *[item["local_path"] for item in input_records],
    ]
    if source_metadata_present:
        required_artifacts.append("source_metadata_verification.json")
    return {
        "allowed_operation_types": [OPERATION_TYPE],
        "dataset_doi": DOI,
        "external_dependencies": [],
        "policy_id": "ncs-drosophila-srna-qc-public-policy-v0.1",
        "profile": {
            "name": PROFILE_NAME,
            "version": PROFILE_VERSION,
        },
        "required_artifacts": required_artifacts,
        "scope": "Deterministic QC of public downsampled Drosophila small RNA-seq FASTQ files.",
    }


def build_provenance(input_records: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "dataset": {
            "doi": DOI,
            "geo_accession": GEO_ACCESSION,
            "zenodo_record_url": ZENODO_RECORD_URL,
        },
        "environment": {
            "external_dependencies": [],
            "runtime": "python-stdlib",
        },
        "execution_end": EXECUTION_END,
        "execution_start": EXECUTION_START,
        "input_paths": [item["local_path"] for item in input_records],
        "output_paths": ["outputs/qc_metrics.json", "outputs/qc_report.txt"],
        "provenance_id": "ncs-drosophila-srna-qc-public-provenance-v0.1",
        "validation_time": VALIDATION_TIME,
        "workflow": {
            "command": workflow_command(input_records),
            "script": "evidence/run_fastq_qc.py",
            "tool": OPERATION_TOOL,
            "type": OPERATION_TYPE,
        },
    }


def build_bundle(
    pack: Path,
    policy: dict[str, Any],
    provenance: dict[str, Any],
    input_records: list[dict[str, Any]],
) -> dict[str, Any]:
    metrics = load_json(pack / "outputs" / "qc_metrics.json")
    aggregate = metrics["aggregate"]
    evidence = [
        {
            "id": "workflow_script",
            "path": "evidence/run_fastq_qc.py",
            "sha256": sha256_file(pack / "evidence" / "run_fastq_qc.py"),
        },
        {
            "id": "dataset_source_manifest",
            "path": "dataset_source_manifest.json",
            "sha256": sha256_file(pack / "dataset_source_manifest.json"),
        },
    ]
    source_metadata_path = pack / "source_metadata_verification.json"
    if source_metadata_path.exists():
        evidence.append(
            {
                "id": "source_metadata_verification",
                "path": "source_metadata_verification.json",
                "sha256": sha256_file(source_metadata_path),
            }
        )
    return {
        "actor": {
            "id": "paper-public-pack-builder",
            "type": "script",
        },
        "evidence": evidence,
        "inputs": [
            {
                "doi": DOI,
                "id": item["id"],
                "kind": "public_dataset_file",
                "md5": item["observed_md5"],
                "path": item["local_path"],
                "sha256": item["sha256"],
                "zenodo_record": ZENODO_RECORD_URL,
            }
            for item in input_records
        ],
        "operation": {
            "command": workflow_command(input_records),
            "execution_end": EXECUTION_END,
            "execution_start": EXECUTION_START,
            "id": "drosophila_srna_fastq_qc_public_run_001",
            "semantics": (
                "Compute deterministic FASTQ QC metrics from six public downsampled "
                "Drosophila small RNA-seq FASTQ files."
            ),
            "tool": OPERATION_TOOL,
            "type": OPERATION_TYPE,
        },
        "outcome": {
            "claims": [
                {
                    "json_path": "$.aggregate.sample_count",
                    "name": "sample_count",
                    "output": "qc_metrics",
                    "value": aggregate["sample_count"],
                },
                {
                    "json_path": "$.aggregate.total_read_count",
                    "name": "total_read_count",
                    "output": "qc_metrics",
                    "value": aggregate["total_read_count"],
                },
                {
                    "json_path": "$.aggregate.aggregate_gc_fraction",
                    "name": "aggregate_gc_fraction",
                    "output": "qc_metrics",
                    "value": aggregate["aggregate_gc_fraction"],
                },
                {
                    "json_path": "$.aggregate.mean_phred_quality",
                    "name": "mean_phred_quality",
                    "output": "qc_metrics",
                    "value": aggregate["mean_phred_quality"],
                },
            ],
            "primary_output": "qc_metrics",
        },
        "outputs": [
            {
                "id": "qc_metrics",
                "path": "outputs/qc_metrics.json",
                "sha256": sha256_file(pack / "outputs" / "qc_metrics.json"),
            },
            {
                "id": "qc_report",
                "path": "outputs/qc_report.txt",
                "sha256": sha256_file(pack / "outputs" / "qc_report.txt"),
            },
        ],
        "pack_id": PACK_ID,
        "policy": {
            "path": "policy.json",
            "policy_id": policy["policy_id"],
            "sha256": sha256_json(policy),
        },
        "profile": {
            "name": PROFILE_NAME,
            "version": PROFILE_VERSION,
        },
        "provenance": {
            "path": "provenance.json",
            "provenance_id": provenance["provenance_id"],
            "sha256": sha256_json(provenance),
        },
        "subject": {
            "doi": DOI,
            "geo_accession": GEO_ACCESSION,
            "id": "zenodo_826906_drosophila_srna_fastq",
            "type": "public_drosophila_srna_fastq_dataset",
            "zenodo_record": ZENODO_RECORD_URL,
        },
        "validation": {
            "expected_exit_code": 0,
            "strict": True,
            "validation_time": VALIDATION_TIME,
            "validator": "agent-evidence validate-pack",
        },
    }


def build_receipt(bundle: dict[str, Any], verdict: str, exit_code: int) -> dict[str, Any]:
    return {
        "bundle_digest": sha256_json(bundle),
        "expected_exit_code": exit_code,
        "generated_at": RECEIPT_GENERATED_AT,
        "pack_id": bundle.get("pack_id"),
        "profile": bundle.get("profile"),
        "validator": "agent-evidence validate-pack",
        "verdict": verdict,
    }


def build_summary(
    pack: Path,
    receipt: dict[str, Any],
    verdict: str,
    exit_code: int,
) -> dict[str, Any]:
    metrics = load_json(pack / "outputs" / "qc_metrics.json")
    return {
        "dataset_doi": DOI,
        "expected_exit_code": exit_code,
        "metrics": metrics["aggregate"],
        "pack_id": receipt.get("pack_id"),
        "primary_output": "outputs/qc_metrics.json",
        "receipt_digest": sha256_json(receipt),
        "verdict": verdict,
        "workflow_name": "drosophila_small_rna_fastq_qc_public",
    }


def build_manifest(
    pack: Path,
    receipt: dict[str, Any],
    input_records: list[dict[str, Any]],
    exit_code: int,
) -> dict[str, Any]:
    return {
        "evidence_objects": {
            "bundle": "bundle.json",
            "receipt": "receipt.json",
            "summary": "summary.json",
        },
        "expected": {
            "exit_code": exit_code,
            "receipt_digest": sha256_json(receipt),
            "verdict": "PASS" if exit_code == 0 else "FAIL",
        },
        "failure_cases": [
            {
                "expected_exit_code": expected,
                "id": case,
                "path": f"failures/{case}",
            }
            for case, expected in FAILURE_CASES.items()
        ],
        "inputs": [
            {
                "doi": DOI,
                "id": item["id"],
                "kind": "public_dataset_file",
                "local_path": item["local_path"],
                "md5": item["observed_md5"],
                "sha256": item["sha256"],
                "zenodo_record": ZENODO_RECORD_URL,
            }
            for item in input_records
        ],
        "outputs": [
            {
                "id": "qc_metrics",
                "path": "outputs/qc_metrics.json",
                "sha256": sha256_file(pack / "outputs" / "qc_metrics.json"),
            },
            {
                "id": "qc_report",
                "path": "outputs/qc_report.txt",
                "sha256": sha256_file(pack / "outputs" / "qc_report.txt"),
            },
        ],
        "pack_id": PACK_ID,
        "profile": {
            "name": PROFILE_NAME,
            "version": PROFILE_VERSION,
        },
        "runtime": {
            "command": workflow_command(input_records),
            "container_image": "ghcr.io/joy7758/agent-evidence:ncs-v0.1",
            "container_digest": "sha256:TODO",
            "random_seed": None,
        },
        "task": {
            "domain": "bioinformatics",
            "scientific_purpose": (
                "Demonstrate third-party verification of a public scientific workflow "
                "execution using downsampled Drosophila small RNA-seq FASTQ files."
            ),
            "workflow_name": "drosophila_small_rna_fastq_qc_public",
            "workflow_version": "v0.1",
        },
    }


def write_receipt_summary_manifest(
    pack: Path,
    input_records: list[dict[str, Any]],
    verdict: str,
    exit_code: int,
) -> None:
    bundle = load_json(pack / "bundle.json")
    receipt = build_receipt(bundle, verdict, exit_code)
    summary = build_summary(pack, receipt, verdict, exit_code)
    manifest = build_manifest(pack, receipt, input_records, exit_code)
    write_json(pack / "receipt.json", receipt)
    write_json(pack / "summary.json", summary)
    write_json(pack / "manifest.json", manifest)
    (pack / "expected_digest.txt").write_text(sha256_json(receipt) + "\n", encoding="utf-8")


def copy_valid_pack(pack: Path, destination: Path) -> list[dict[str, Any]]:
    if destination.exists():
        shutil.rmtree(destination)
    destination.mkdir(parents=True)
    for name in [
        "bundle.json",
        "dataset_source_manifest.json",
        "expected_digest.txt",
        "manifest.json",
        "policy.json",
        "provenance.json",
        "receipt.json",
        "source_metadata_verification.json",
        "summary.json",
    ]:
        source = pack / name
        if source.exists():
            shutil.copy2(source, destination / name)
    for name in ["inputs", "outputs", "evidence"]:
        shutil.copytree(pack / name, destination / name)
    return load_json(destination / "dataset_source_manifest.json")["files"]


def create_failure_cases(pack: Path) -> None:
    failures = pack / "failures"
    failures.mkdir(parents=True, exist_ok=True)

    for case, expected_code in FAILURE_CASES.items():
        case_dir = failures / case
        input_records = copy_valid_pack(pack, case_dir)

        if case == "tampered_input":
            target = case_dir / input_records[0]["local_path"]
            with target.open("ab") as handle:
                handle.write(b"\n#tampered\n")
        elif case == "tampered_output":
            metrics_path = case_dir / "outputs" / "qc_metrics.json"
            metrics = load_json(metrics_path)
            metrics["tamper_marker"] = "digest mismatch"
            write_json(metrics_path, metrics)
        elif case == "missing_policy":
            (case_dir / "policy.json").unlink()
        elif case == "broken_evidence_link":
            bundle = load_json(case_dir / "bundle.json")
            bundle["evidence"][0]["path"] = "evidence/missing_run_fastq_qc.py"
            write_json(case_dir / "bundle.json", bundle)
            write_receipt_summary_manifest(case_dir, input_records, "FAIL", expected_code)
        elif case == "version_mismatch":
            bundle = load_json(case_dir / "bundle.json")
            bundle["profile"]["version"] = "ncs-v0-broken"
            write_json(case_dir / "bundle.json", bundle)
            write_receipt_summary_manifest(case_dir, input_records, "FAIL", expected_code)
        elif case == "temporal_inconsistency":
            provenance = load_json(case_dir / "provenance.json")
            provenance["validation_time"] = "2026-04-24T00:09:59Z"
            write_json(case_dir / "provenance.json", provenance)
            bundle = load_json(case_dir / "bundle.json")
            bundle["provenance"]["sha256"] = sha256_json(provenance)
            write_json(case_dir / "bundle.json", bundle)
            write_receipt_summary_manifest(case_dir, input_records, "FAIL", expected_code)
        elif case == "outcome_unverifiable":
            bundle = load_json(case_dir / "bundle.json")
            for output in bundle["outputs"]:
                if output.get("id") == bundle["outcome"]["primary_output"]:
                    output.pop("sha256", None)
            write_json(case_dir / "bundle.json", bundle)
            write_receipt_summary_manifest(case_dir, input_records, "FAIL", expected_code)


def build_pack(pack: Path, *, force: bool, skip_download: bool, offline: bool) -> None:
    paper_root = Path(__file__).resolve().parents[1]
    workflow_script = paper_root / "experiments" / "scientific_workflow" / "run_fastq_qc.py"
    if not workflow_script.exists():
        raise FileNotFoundError(f"Workflow script not found: {workflow_script}")

    pack.mkdir(parents=True, exist_ok=True)
    for name in ["inputs", "outputs", "evidence", "failures"]:
        (pack / name).mkdir(parents=True, exist_ok=True)
    if force:
        reset_generated_pack_content(pack)
        for name in ["inputs", "outputs", "evidence", "failures"]:
            (pack / name).mkdir(parents=True, exist_ok=True)

    source_metadata = load_verified_source_metadata(paper_root)
    if source_metadata:
        write_json(pack / "source_metadata_verification.json", source_metadata)

    input_records = prepare_inputs(pack, skip_download=skip_download, offline=offline)
    write_dataset_source_manifest(pack, input_records, source_metadata)
    run_workflow(pack, workflow_script, input_records)

    evidence_script = pack / "evidence" / "run_fastq_qc.py"
    evidence_script.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(workflow_script, evidence_script)

    policy = build_policy(input_records, source_metadata is not None)
    provenance = build_provenance(input_records)
    write_json(pack / "policy.json", policy)
    write_json(pack / "provenance.json", provenance)
    write_json(pack / "bundle.json", build_bundle(pack, policy, provenance, input_records))
    write_receipt_summary_manifest(pack, input_records, "PASS", 0)
    create_failure_cases(pack)


def main() -> int:
    parser = argparse.ArgumentParser(description="Build the public NCS scientific workflow pack.")
    parser.add_argument("--pack", required=True, type=Path)
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--skip-download", action="store_true")
    parser.add_argument("--offline", action="store_true")
    args = parser.parse_args()

    build_pack(
        args.pack,
        force=args.force,
        skip_download=args.skip_download,
        offline=args.offline,
    )
    print(f"Built public scientific workflow pack: {args.pack}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
