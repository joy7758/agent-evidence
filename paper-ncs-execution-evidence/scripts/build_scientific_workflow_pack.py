#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any

PACK_ID = "ncs-scientific-workflow-fastq-qc-smoke-v0.1"
PROFILE_NAME = "execution-evidence-operation-accountability"
PROFILE_VERSION = "ncs-v1.0-draft"
OPERATION_TYPE = "fastq_qc"
OPERATION_TOOL = "paper-fastq-qc-v0.1"
EXECUTION_START = "2026-04-24T00:00:00Z"
EXECUTION_END = "2026-04-24T00:00:01Z"
VALIDATION_TIME = "2026-04-24T00:00:02Z"
RECEIPT_GENERATED_AT = "2026-04-24T00:00:03Z"
SMOKE_NOTE = "Local FASTQ smoke fixture; not the final public Nature dataset."

FASTQ_CONTENT = """@read1
ACGTACGTACGT
+
IIIIIIIIIIII
@read2
GGGGCCCCAAAA
+
IIIIIIIIIIII
@read3
TTTTAAAACCCC
+
IIIIIIIIIIII
@read4
NNNNACGT
+
IIIIIIII
"""

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


def write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(obj, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
        encoding="utf-8",
    )


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def relative(path: Path, pack: Path) -> str:
    return path.relative_to(pack).as_posix()


def reset_generated_pack_content(pack: Path) -> None:
    for name in [
        "manifest.json",
        "bundle.json",
        "receipt.json",
        "summary.json",
        "expected_digest.txt",
        "policy.json",
        "provenance.json",
    ]:
        target = pack / name
        if target.exists():
            target.unlink()

    for name in ["inputs", "outputs", "evidence"]:
        target = pack / name
        if target.exists():
            shutil.rmtree(target)

    failures = pack / "failures"
    failures.mkdir(parents=True, exist_ok=True)
    for case in FAILURE_CASES:
        target = failures / case
        if target.exists():
            shutil.rmtree(target)


def run_workflow(pack: Path, workflow_script: Path) -> None:
    fastq_path = pack / "inputs" / "smoke_reads.fastq"
    metrics_path = pack / "outputs" / "qc_metrics.json"
    report_path = pack / "outputs" / "qc_report.txt"

    fastq_path.parent.mkdir(parents=True, exist_ok=True)
    fastq_path.write_text(FASTQ_CONTENT, encoding="utf-8")
    metrics_path.parent.mkdir(parents=True, exist_ok=True)

    subprocess.run(
        [
            sys.executable,
            str(workflow_script),
            "--input",
            str(fastq_path),
            "--metrics",
            str(metrics_path),
            "--report",
            str(report_path),
        ],
        check=True,
    )


def build_policy() -> dict[str, Any]:
    return {
        "allowed_operation_types": [OPERATION_TYPE],
        "external_dependencies": [],
        "not_final_nature_dataset": True,
        "policy_id": "ncs-fastq-qc-smoke-policy-v0.1",
        "profile": {
            "name": PROFILE_NAME,
            "version": PROFILE_VERSION,
        },
        "required_artifacts": [
            "manifest.json",
            "bundle.json",
            "receipt.json",
            "summary.json",
            "inputs/smoke_reads.fastq",
            "outputs/qc_metrics.json",
            "outputs/qc_report.txt",
            "evidence/run_fastq_qc.py",
        ],
        "scope": "Deterministic local smoke validation of the NCS execution-evidence pack surface.",
    }


def build_provenance() -> dict[str, Any]:
    return {
        "environment": {
            "external_dependencies": [],
            "runtime": "python-stdlib",
        },
        "execution_end": EXECUTION_END,
        "execution_start": EXECUTION_START,
        "fixture_note": SMOKE_NOTE,
        "input_paths": ["inputs/smoke_reads.fastq"],
        "output_paths": ["outputs/qc_metrics.json", "outputs/qc_report.txt"],
        "provenance_id": "ncs-fastq-qc-smoke-provenance-v0.1",
        "validation_time": VALIDATION_TIME,
        "workflow": {
            "command": [
                "python",
                "evidence/run_fastq_qc.py",
                "--input",
                "inputs/smoke_reads.fastq",
                "--metrics",
                "outputs/qc_metrics.json",
                "--report",
                "outputs/qc_report.txt",
            ],
            "script": "evidence/run_fastq_qc.py",
            "tool": OPERATION_TOOL,
            "type": OPERATION_TYPE,
        },
    }


def build_bundle(pack: Path, policy: dict[str, Any], provenance: dict[str, Any]) -> dict[str, Any]:
    metrics = load_json(pack / "outputs" / "qc_metrics.json")
    return {
        "actor": {
            "id": "paper-local-builder",
            "type": "script",
        },
        "evidence": [
            {
                "id": "workflow_script",
                "path": "evidence/run_fastq_qc.py",
                "sha256": sha256_file(pack / "evidence" / "run_fastq_qc.py"),
            }
        ],
        "fixture_status": SMOKE_NOTE,
        "inputs": [
            {
                "id": "input_reads",
                "kind": "local_fastq_smoke_fixture",
                "path": "inputs/smoke_reads.fastq",
                "sha256": sha256_file(pack / "inputs" / "smoke_reads.fastq"),
            }
        ],
        "operation": {
            "command": [
                "python",
                "evidence/run_fastq_qc.py",
                "--input",
                "inputs/smoke_reads.fastq",
                "--metrics",
                "outputs/qc_metrics.json",
                "--report",
                "outputs/qc_report.txt",
            ],
            "execution_end": EXECUTION_END,
            "execution_start": EXECUTION_START,
            "id": "fastq_qc_smoke_run_001",
            "semantics": (
                "Compute deterministic FASTQ QC metrics from a fixed local FASTQ smoke fixture."
            ),
            "tool": OPERATION_TOOL,
            "type": OPERATION_TYPE,
        },
        "outcome": {
            "claims": [
                {
                    "json_path": "$.read_count",
                    "name": "read_count",
                    "output": "qc_metrics",
                    "value": metrics["read_count"],
                },
                {
                    "json_path": "$.gc_fraction",
                    "name": "gc_fraction",
                    "output": "qc_metrics",
                    "value": metrics["gc_fraction"],
                },
                {
                    "json_path": "$.mean_phred_quality",
                    "name": "mean_phred_quality",
                    "output": "qc_metrics",
                    "value": metrics["mean_phred_quality"],
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
            "id": "smoke_reads_fastq",
            "not_final_nature_dataset": True,
            "type": "local_fastq_fixture",
        },
        "validation": {
            "expected_exit_code": 0,
            "strict": True,
            "validation_time": VALIDATION_TIME,
            "validator": "paper-local validate_ncs_pack.py",
        },
    }


def build_receipt(bundle: dict[str, Any], verdict: str, exit_code: int) -> dict[str, Any]:
    return {
        "bundle_digest": sha256_json(bundle),
        "generated_at": RECEIPT_GENERATED_AT,
        "pack_id": bundle.get("pack_id"),
        "profile": bundle.get("profile"),
        "validator": "paper-local validate_ncs_pack.py",
        "verdict": verdict,
        "expected_exit_code": exit_code,
    }


def build_summary(
    pack: Path,
    receipt: dict[str, Any],
    verdict: str,
    exit_code: int,
) -> dict[str, Any]:
    metrics_path = pack / "outputs" / "qc_metrics.json"
    metrics = load_json(metrics_path) if metrics_path.exists() else {}
    return {
        "expected_exit_code": exit_code,
        "fixture_status": SMOKE_NOTE,
        "metrics": metrics,
        "pack_id": receipt.get("pack_id"),
        "primary_output": "outputs/qc_metrics.json",
        "receipt_digest": sha256_json(receipt),
        "verdict": verdict,
        "workflow_name": "FASTQ QC smoke workflow",
    }


def build_manifest(receipt: dict[str, Any], exit_code: int) -> dict[str, Any]:
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
        "pack_id": PACK_ID,
        "profile": {
            "name": PROFILE_NAME,
            "version": PROFILE_VERSION,
        },
        "status": SMOKE_NOTE,
        "task": {
            "domain": "bioinformatics",
            "scientific_purpose": (
                "Wire reviewer-verifiable execution evidence using a deterministic "
                "local FASTQ QC smoke fixture, not biological discovery."
            ),
            "workflow_name": "FASTQ QC smoke workflow",
            "workflow_version": "0.1",
        },
    }


def write_receipt_summary_manifest(pack: Path, verdict: str, exit_code: int) -> None:
    bundle = load_json(pack / "bundle.json")
    receipt = build_receipt(bundle, verdict, exit_code)
    summary = build_summary(pack, receipt, verdict, exit_code)
    manifest = build_manifest(receipt, exit_code)
    write_json(pack / "receipt.json", receipt)
    write_json(pack / "summary.json", summary)
    write_json(pack / "manifest.json", manifest)
    (pack / "expected_digest.txt").write_text(sha256_json(receipt) + "\n", encoding="utf-8")


def copy_valid_pack(pack: Path, destination: Path) -> None:
    if destination.exists():
        shutil.rmtree(destination)
    destination.mkdir(parents=True)
    for name in [
        "manifest.json",
        "bundle.json",
        "receipt.json",
        "summary.json",
        "expected_digest.txt",
        "policy.json",
        "provenance.json",
    ]:
        shutil.copy2(pack / name, destination / name)
    for name in ["inputs", "outputs", "evidence"]:
        shutil.copytree(pack / name, destination / name)


def create_failure_cases(pack: Path) -> None:
    failures = pack / "failures"
    failures.mkdir(parents=True, exist_ok=True)

    for case, expected_code in FAILURE_CASES.items():
        case_dir = failures / case
        copy_valid_pack(pack, case_dir)

        if case == "tampered_input":
            with (case_dir / "inputs" / "smoke_reads.fastq").open("a", encoding="utf-8") as handle:
                handle.write("@tampered\nACGT\n+\nIIII\n")
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
            write_receipt_summary_manifest(case_dir, "FAIL", expected_code)
        elif case == "version_mismatch":
            bundle = load_json(case_dir / "bundle.json")
            bundle["profile"]["version"] = "ncs-v0-broken"
            write_json(case_dir / "bundle.json", bundle)
            write_receipt_summary_manifest(case_dir, "FAIL", expected_code)
        elif case == "temporal_inconsistency":
            provenance = load_json(case_dir / "provenance.json")
            provenance["validation_time"] = "2026-04-23T23:59:59Z"
            write_json(case_dir / "provenance.json", provenance)
            bundle = load_json(case_dir / "bundle.json")
            bundle["provenance"]["sha256"] = sha256_json(provenance)
            write_json(case_dir / "bundle.json", bundle)
            write_receipt_summary_manifest(case_dir, "FAIL", expected_code)
        elif case == "outcome_unverifiable":
            bundle = load_json(case_dir / "bundle.json")
            for output in bundle["outputs"]:
                if output.get("id") == bundle["outcome"]["primary_output"]:
                    output.pop("sha256", None)
            write_json(case_dir / "bundle.json", bundle)
            write_receipt_summary_manifest(case_dir, "FAIL", expected_code)


def build_pack(pack: Path, force: bool) -> None:
    script_path = Path(__file__).resolve()
    paper_root = script_path.parents[1]
    workflow_script = paper_root / "experiments" / "scientific_workflow" / "run_fastq_qc.py"
    if not workflow_script.exists():
        raise FileNotFoundError(f"Workflow script not found: {workflow_script}")

    pack.mkdir(parents=True, exist_ok=True)
    if force:
        reset_generated_pack_content(pack)

    run_workflow(pack, workflow_script)
    evidence_script = pack / "evidence" / "run_fastq_qc.py"
    evidence_script.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(workflow_script, evidence_script)

    policy = build_policy()
    provenance = build_provenance()
    write_json(pack / "policy.json", policy)
    write_json(pack / "provenance.json", provenance)
    write_json(pack / "bundle.json", build_bundle(pack, policy, provenance))
    write_receipt_summary_manifest(pack, "PASS", 0)
    create_failure_cases(pack)


def main() -> int:
    parser = argparse.ArgumentParser(description="Build the NCS scientific workflow smoke pack.")
    parser.add_argument("--pack", required=True, type=Path)
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()

    build_pack(args.pack, args.force)
    print(f"Built scientific workflow smoke pack: {args.pack}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
