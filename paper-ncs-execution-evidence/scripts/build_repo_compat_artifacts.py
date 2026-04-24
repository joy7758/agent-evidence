#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

OLD_PROFILE_NAME = "execution-evidence-operation-accountability-profile"
OLD_PROFILE_VERSION = "0.1"


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


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(obj, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
        encoding="utf-8",
    )


def digest_json_file(path: Path) -> str:
    return sha256_json(read_json(path))


def path_digest(pack: Path, relative_path: str) -> str:
    return sha256_file(pack / relative_path)


def build_artifact_index(pack: Path, bundle: dict[str, Any]) -> dict[str, Any]:
    json_files = [
        "manifest.json",
        "bundle.json",
        "receipt.json",
        "summary.json",
        "policy.json",
        "provenance.json",
    ]
    return {
        "compatibility_status": "derived_view",
        "digest_rule": "canonical JSON for JSON files; byte SHA-256 for non-JSON artifacts",
        "json_objects": [
            {
                "path": name,
                "sha256": digest_json_file(pack / name),
            }
            for name in json_files
            if (pack / name).exists()
        ],
        "inputs": [
            {
                "id": item.get("id"),
                "path": item.get("path"),
                "sha256": path_digest(pack, item["path"]),
            }
            for item in bundle.get("inputs", [])
            if item.get("path")
        ],
        "outputs": [
            {
                "id": item.get("id"),
                "path": item.get("path"),
                "sha256": path_digest(pack, item["path"]),
            }
            for item in bundle.get("outputs", [])
            if item.get("path") and (pack / item["path"]).exists()
        ],
        "evidence": [
            {
                "id": item.get("id"),
                "path": item.get("path"),
                "sha256": path_digest(pack, item["path"]),
            }
            for item in bundle.get("evidence", [])
            if item.get("path") and (pack / item["path"]).exists()
        ],
    }


def old_statement_core(statement: dict[str, Any]) -> dict[str, Any]:
    return {
        "actor": statement["actor"],
        "subject": statement["subject"],
        "operation": statement["operation"],
        "policy": statement["policy"],
        "constraints": statement["constraints"],
        "provenance": statement["provenance"],
    }


def build_operation_accountability_statement(
    pack: Path,
    bundle: dict[str, Any],
    artifact_index: dict[str, Any],
) -> dict[str, Any]:
    input_entry = bundle["inputs"][0]
    output_entries = bundle.get("outputs", [])
    output_ids = [item["id"] for item in output_entries]
    input_ref_id = f"ref:{input_entry['id']}"
    output_ref_ids = [f"ref:{item['id']}" for item in output_entries]
    policy_id = bundle["policy"].get("policy_id") or "ncs-fastq-qc-smoke-policy-v0.1"
    subject_id = bundle["subject"]["id"]
    operation_id = bundle["operation"]["id"]
    provenance_id = (
        bundle["provenance"].get("provenance_id") or "ncs-fastq-qc-smoke-provenance-v0.1"
    )
    evidence_id = "ncs-fastq-qc-smoke-evidence-v0.1"

    references = [
        {
            "digest": input_entry["sha256"],
            "locator": input_entry["path"],
            "object_id": subject_id,
            "ref_id": input_ref_id,
            "role": "input",
        }
    ]
    references.extend(
        {
            "digest": output["sha256"],
            "locator": output["path"],
            "object_id": output["id"],
            "ref_id": f"ref:{output['id']}",
            "role": "output",
        }
        for output in output_entries
        if output.get("sha256")
    )

    artifacts = [
        {
            "artifact_id": "artifact:manifest",
            "digest": digest_json_file(pack / "manifest.json"),
            "locator": "manifest.json",
            "type": "manifest",
        },
        {
            "artifact_id": "artifact:bundle",
            "digest": digest_json_file(pack / "bundle.json"),
            "locator": "bundle.json",
            "type": "ncs_bundle",
        },
        {
            "artifact_id": "artifact:receipt",
            "digest": digest_json_file(pack / "receipt.json"),
            "locator": "receipt.json",
            "type": "receipt",
        },
        {
            "artifact_id": "artifact:summary",
            "digest": digest_json_file(pack / "summary.json"),
            "locator": "summary.json",
            "type": "summary",
        },
        {
            "artifact_id": "artifact:policy",
            "digest": digest_json_file(pack / "policy.json"),
            "locator": "policy.json",
            "type": "policy",
        },
        {
            "artifact_id": "artifact:provenance",
            "digest": digest_json_file(pack / "provenance.json"),
            "locator": "provenance.json",
            "type": "provenance",
        },
    ]
    for item in bundle.get("evidence", []):
        artifacts.append(
            {
                "artifact_id": f"artifact:{item['id']}",
                "digest": item["sha256"],
                "locator": item["path"],
                "type": "workflow_script",
            }
        )

    statement = {
        "actor": {
            "id": bundle["actor"]["id"],
            "name": "NCS paper-local pack builder",
            "runtime": "python-stdlib",
            "type": bundle["actor"]["type"],
        },
        "constraints": [
            {
                "description": (
                    "The operation must be the deterministic FASTQ QC smoke workflow "
                    "and must retain local policy, provenance, evidence and digest links."
                ),
                "id": "constraint:ncs-fastq-qc-smoke-boundary",
            }
        ],
        "evidence": {
            "artifacts": artifacts,
            "id": evidence_id,
            "integrity": {
                "artifacts_digest": "",
                "references_digest": "",
                "statement_digest": "",
            },
            "operation_ref": operation_id,
            "policy_ref": policy_id,
            "references": references,
            "subject_ref": subject_id,
        },
        "operation": {
            "description": bundle["operation"]["semantics"],
            "id": operation_id,
            "input_refs": [input_ref_id],
            "output_refs": output_ref_ids,
            "policy_ref": policy_id,
            "result": {
                "status": "succeeded",
                "summary": f"Generated {', '.join(output_ids)} for a local FASTQ QC smoke fixture.",
            },
            "subject_ref": subject_id,
            "type": bundle["operation"]["type"],
        },
        "policy": {
            "constraint_refs": ["constraint:ncs-fastq-qc-smoke-boundary"],
            "id": policy_id,
            "name": "NCS FASTQ QC smoke policy",
        },
        "profile": {
            "name": OLD_PROFILE_NAME,
            "version": OLD_PROFILE_VERSION,
        },
        "provenance": {
            "actor_ref": bundle["actor"]["id"],
            "id": provenance_id,
            "input_refs": [input_ref_id],
            "operation_ref": operation_id,
            "output_refs": output_ref_ids,
            "subject_ref": subject_id,
        },
        "statement_id": f"compat:{bundle['pack_id']}",
        "subject": {
            "digest": input_entry["sha256"],
            "id": subject_id,
            "locator": input_entry["path"],
            "type": bundle["subject"]["type"],
        },
        "timestamp": bundle["validation"]["validation_time"],
        "validation": {
            "evidence_ref": evidence_id,
            "id": "validation:ncs-fastq-qc-smoke-compat",
            "method": "derived compatibility statement for repository validate-profile probe",
            "policy_ref": policy_id,
            "provenance_ref": provenance_id,
            "status": "verifiable",
            "validator": "agent-evidence validate-profile",
        },
    }
    statement["evidence"]["integrity"] = {
        "artifacts_digest": sha256_json(statement["evidence"]["artifacts"]),
        "references_digest": sha256_json(statement["evidence"]["references"]),
        "statement_digest": sha256_json(old_statement_core(statement)),
    }
    return statement


def write_readme(compat_dir: Path) -> None:
    compat_dir.joinpath("README.md").write_text(
        """# Repository compatibility artifacts

This directory contains derived views for probing existing repository validators.

The NCS pack contract is not changed by these files. The strict NCS validator is
still `paper-ncs-execution-evidence/scripts/validate_ncs_pack.py`.

## Files

- `ncs_bundle_view.json`: canonical JSON copy of the NCS `bundle.json` with no semantic changes.
- `operation_accountability_statement.json`: conservative mapping into the repository's older
  `execution-evidence-operation-accountability-profile@0.1` statement shape.
- `artifact_index.json`: digest index for the NCS pack and derived compatibility files.

## Compatibility adjustments

The repository schema requires profile name `execution-evidence-operation-accountability-profile`
and version `0.1`, plus single-operation fields such as `statement_id`,
`constraints`, `evidence.references`, `evidence.artifacts` and
`evidence.integrity`. The derived statement therefore maps the NCS FASTQ QC
operation into that older single-operation shape. This is advisory compatibility,
not strict validation of the whole NCS pack.
""",
        encoding="utf-8",
    )


def build(pack: Path) -> None:
    bundle = read_json(pack / "bundle.json")
    compat_dir = pack / "repo_compat"
    compat_dir.mkdir(parents=True, exist_ok=True)

    write_json(compat_dir / "ncs_bundle_view.json", bundle)
    artifact_index = build_artifact_index(pack, bundle)
    statement = build_operation_accountability_statement(pack, bundle, artifact_index)
    write_json(compat_dir / "operation_accountability_statement.json", statement)

    artifact_index["derived"] = [
        {
            "path": "repo_compat/ncs_bundle_view.json",
            "sha256": digest_json_file(compat_dir / "ncs_bundle_view.json"),
        },
        {
            "path": "repo_compat/operation_accountability_statement.json",
            "sha256": digest_json_file(compat_dir / "operation_accountability_statement.json"),
        },
    ]
    write_json(compat_dir / "artifact_index.json", artifact_index)
    write_readme(compat_dir)
    print(f"Wrote repository compatibility artifacts: {compat_dir}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Build repository compatibility artifacts.")
    parser.add_argument("--pack", required=True, type=Path)
    args = parser.parse_args()
    build(args.pack)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
