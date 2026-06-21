#!/usr/bin/env python3
"""Run a local hygiene audit over a SoftwareX package ZIP."""

from __future__ import annotations

import argparse
import hashlib
import json
import stat
from pathlib import Path
from zipfile import ZipFile


REQUIRED_FILES = [
    "LICENSE",
    "pyproject.toml",
    "README.md",
    "README_SOFTWAREX_SUBMISSION.md",
    "agent_evidence/oap.py",
    "agent_evidence/cli/main.py",
    "schema/execution-evidence-operation-accountability-profile-v0.1.schema.json",
    "spec/execution-evidence-operation-accountability-profile-v0.1.md",
    "protocol/manifest.json",
    "protocol/clause-index.json",
    "docs/protocol/clauses.md",
    "specs/eeoap/v0.1/eeoap.schema.json",
    "docs/specs/EEOAP_v0_1.md",
    "docs/public/EEOAP_v0.1_public_spec.md",
    "data/otel/raw_demo_trace.json",
    "data/otel/trace_provenance_record.json",
    "data/eeoap/real_trace_evidence.json",
    "docs/softwarex_environment.md",
    "examples/minimal-valid-evidence.json",
    "experiments/baselines/otel_native_vs_eeoap.py",
    "experiments/results/otel_native_vs_eeoap.md",
    "experiments/results/otel_native_vs_eeoap.json",
    "experiments/exp4_determinism_oracle.py",
    "experiments/results/exp4_determinism_oracle.json",
    "scripts/reproduce_paper.sh",
    "paper/cover_letter.md",
    "paper/softwarex_v2_revised.md",
    "paper/highlights.txt",
    "paper/data_availability_statement.md",
    "paper/ai_use_declaration.md",
    "tests/__init__.py",
    "tests/test_aep_profile.py",
    "tests/test_automaton_integration.py",
    "tests/test_cli.py",
    "tests/fixtures/agent_evidence_profile/valid/basic-bundle/manifest.json",
]

INTERNAL_ONLY_SUBMISSION_FILES = [
    "paper/reviewer_checklist.md",
    "paper/response_letter.md",
    "paper/rebuttal_response.md",
]

BANNED_AMBIGUITY_PHRASES = [
    "governance",
    "standard proposal",
    "framework for future systems",
    "auditability in general systems",
    "semantic reconstruction of intelligence systems",
    "trace-to-semantic-reconstruction",
    "audit-grade",
    "interpretability score",
    "audit readiness",
]

BANNED_CONFLICTING_CLAIM_PATTERNS = [
    "we introduce a new telemetry system",
    "this work introduces a new telemetry system",
    "we introduce a new tracing protocol",
    "this work introduces a new tracing protocol",
    "we introduce a new observability standard",
    "this work introduces a new observability standard",
    "replacement for opentelemetry",
    "competes on performance metrics",
    "competes on latency",
    "competes on scalability",
    "positioned as a protocol proposal",
    "positioned as a theoretical framework",
    "positioned as a standard specification",
]

BANNED_OVERCLAIM_PHRASES = [
    "certified by",
    "accepted by softwarex",
    "published in softwarex",
    "production ready",
    "standard-body adopted",
]

BANNED_INTERNAL_DRAFT_MARKERS = [
    "repair draft",
    "not submitted",
    "not accepted",
    "local candidate",
    "before any real resubmission",
]

BANNED_MANUSCRIPT_BODY_PHRASES = [
    "prepared as a softwarex",
    "this manuscript is prepared for softwarex",
    "this manuscript is prepared as a softwarex",
    "editorial classification signal",
    "editorial summary",
    "target journal fit",
    "review scope constraint",
    "reviewers should",
    "review scope",
    "external-action gate",
]

REQUIRED_PAPER_PHRASES = [
    "# A Software Artifact for Deterministic Conversion of OpenTelemetry Traces into Structured Execution Evidence",
    "This software artifact implements a deterministic transformation from",
    "OpenTelemetry trace data into structured execution evidence representations.",
    "## Primary Artifact Entry Point",
    "`scripts/reproduce_paper.sh`",
    "## Execution Environment",
    "No network access is required during reproduction",
    "## Environment Stability Boundary",
    "docs/softwarex_environment.md",
    "semantic equivalence of generated evidence content",
    "## Readiness Statement",
    "single entry script",
    "standard Python environment",
    "## Evaluation Interpretation",
    "The evaluation is not a performance benchmark.",
    "## Validation Independence Clarification",
    "faithful field transfer from OTLP input",
    "self-sufficient proof of conceptual correctness",
    "## Evaluation Scope Justification",
    "deterministic mapping fidelity",
    "schema validity",
    "provenance preservation across representative trace conditions",
    "## Remaining Real-Trace Robustness Gap",
    "does not yet include an additional public multi-span real trace",
    "## Determinism Boundary",
    "fixed OTLP JSON input processed within",
    "file locators as provenance metadata",
    "## Determinism Test Oracle",
    "content-equivalence oracle",
    "canonicalized evidence content",
    "## Software Artifact Scope",
    "strictly software-centric",
    "## Why This Matters",
    "minimal deterministic mapping",
    "## Why a Named Repository-Scoped Schema",
    "repository-scoped structured JSON",
    "evidence contract required by the validator",
    "does not imply external standard status",
    "## Necessity of the EEOAP Abstraction",
    "stable, schema-bound representation",
    "minimal contract layer between telemetry",
    "## Task-Based Necessity Clarification",
    "task-bound rather than ontological",
    "validator-readable form",
    "## Distinction from Data Processing Pipelines",
    "schema-constrained output validity",
    "trace provenance preservation",
    "## Practical Utility",
    "structured view of execution behavior",
    "## Supported OpenTelemetry Surface",
    "does not claim exhaustive preservation",
    "schema URL metadata remain extension points",
    "## OTLP Field Coverage Matrix",
    "events | not interpreted",
    "links | not interpreted",
    "## Concrete Usage Scenario",
    "post-execution failure analysis and review",
    "### Minimal debugging walkthrough",
    "Which trace produced this",
    "pass schema and integrity",
    "### Debugging outcome demonstration",
    "trace identity",
    "provenance binding",
    "### Example CLI invocation",
    "scripts/convert_otel_trace_to_eeoap.py",
    "--adapter-record",
    "## Baseline Scope Expansion",
    "raw OTLP retention",
    "OTLP exported as generic structured JSON",
    "feature-coverage comparison",
    "## Data Availability",
    "public repository release record",
    "package manifest with checksums",
    "## Declaration of Generative AI and AI-assisted Technologies",
    "takes full responsibility for",
    "## Keywords",
    "OpenTelemetry; tracing; evidence; validation; reproducibility",
    "## 13. References",
    "OpenTelemetry. Trace API specification.",
    "Jaeger Documentation.",
    "OpenZipkin.",
]

REQUIRED_COVER_LETTER_PHRASES = [
    "Dear Editor,",
    "We submit this manuscript as a SoftwareX research software article.",
    "implements a deterministic",
    "OpenTelemetry trace data",
    "repository-scoped structured execution",
    "schema definition",
    "trace conversion pipeline",
    "validation framework",
    "baseline comparison",
    "reproducibility scripts",
    "does not claim a new telemetry standard, protocol replacement",
    "aligns with SoftwareX scope as a research software",
    "publicly available for inspection",
    "validation, and reuse",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True)
    return parser.parse_args()


def read_json(archive: ZipFile, path: str) -> dict:
    with archive.open(path) as handle:
        payload = json.loads(handle.read().decode("utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return payload


def sha256_bytes(payload: bytes) -> str:
    return "sha256:" + hashlib.sha256(payload).hexdigest()


def check_reproduce_executable(archive: ZipFile) -> bool:
    info = archive.getinfo("scripts/reproduce_paper.sh")
    mode = (info.external_attr >> 16) & 0o777
    return bool(mode & stat.S_IXUSR)


def check_no_banned_phrases(archive: ZipFile, paths: list[str]) -> tuple[bool, list[str]]:
    findings = []
    phrases = BANNED_AMBIGUITY_PHRASES + BANNED_OVERCLAIM_PHRASES + BANNED_INTERNAL_DRAFT_MARKERS
    for path in paths:
        text = archive.read(path).decode("utf-8").lower()
        for phrase in phrases:
            if phrase in text:
                findings.append(f"{path}: {phrase}")
    return not findings, findings


def check_schema_spec_consistency(schema: dict, spec_text: str) -> bool:
    required = schema.get("required", [])
    if not isinstance(required, list):
        return False
    return all(isinstance(field, str) and field in spec_text for field in required)


def check_paper_required_phrases(paper_text: str) -> tuple[bool, list[str]]:
    missing = [phrase for phrase in REQUIRED_PAPER_PHRASES if phrase not in paper_text]
    return not missing, missing


def check_cover_letter_required_phrases(cover_text: str) -> tuple[bool, list[str]]:
    missing = [phrase for phrase in REQUIRED_COVER_LETTER_PHRASES if phrase not in cover_text]
    return not missing, missing


def check_no_conflicting_contribution_claims(paper_text: str) -> tuple[bool, list[str]]:
    lowered = paper_text.lower()
    lowered = lowered.replace("not positioned as a protocol proposal", "")
    lowered = lowered.replace("not positioned as a theoretical framework", "")
    lowered = lowered.replace("not positioned as a standard specification", "")
    findings = []
    for phrase in BANNED_CONFLICTING_CLAIM_PATTERNS:
        if phrase in lowered:
            findings.append(phrase)
    return not findings, findings


def check_no_journal_facing_manuscript_language(paper_text: str) -> tuple[bool, list[str]]:
    lowered = paper_text.lower()
    findings = [phrase for phrase in BANNED_MANUSCRIPT_BODY_PHRASES if phrase in lowered]
    return not findings, findings


def check_no_local_absolute_paths(archive: ZipFile) -> tuple[bool, list[str]]:
    findings = []
    local_home_marker = "/Users/" + "zhangbin"
    text_suffixes = {
        ".json",
        ".md",
        ".mmd",
        ".py",
        ".sh",
        ".toml",
        ".txt",
    }
    for path in archive.namelist():
        if Path(path).suffix not in text_suffixes:
            continue
        text = archive.read(path).decode("utf-8", errors="ignore")
        if local_home_marker in text:
            findings.append(path)
    return not findings, findings


def data_availability_status(statement_text: str) -> dict[str, bool]:
    has_placeholder = "[TO BE FILLED BEFORE SUBMISSION]" in statement_text
    has_url = "http://" in statement_text or "https://" in statement_text
    has_persistent_identifier = (
        "doi.org/" in statement_text
        or "swh:" in statement_text.lower()
        or "/releases/tag/" in statement_text
    )
    return {
        "data_availability_url_filled": has_url and not has_placeholder,
        "doi_or_persistent_identifier_filled": has_persistent_identifier and not has_placeholder,
    }


def main() -> int:
    args = parse_args()
    results: dict[str, object] = {}

    with ZipFile(args.input) as archive:
        names = set(archive.namelist())
        missing = [path for path in REQUIRED_FILES if path not in names]
        if missing:
            raise FileNotFoundError("missing package files: " + ", ".join(missing))

        schema = read_json(archive, "specs/eeoap/v0.1/eeoap.schema.json")
        results["schema_valid"] = schema.get("$schema") is not None and schema.get("type") == "object"
        spec_text = archive.read("docs/specs/EEOAP_v0_1.md").decode("utf-8")
        results["schema_spec_consistency"] = check_schema_spec_consistency(schema, spec_text)

        provenance = read_json(archive, "data/otel/trace_provenance_record.json")
        raw_trace = archive.read("data/otel/raw_demo_trace.json")
        recorded_digest = provenance["extracted_artifact"]["local_file_sha256"]
        results["trace_provenance_valid"] = (
            provenance["upstream"]["repository_url"] == "https://github.com/open-telemetry/opentelemetry-proto"
            and provenance["upstream"]["commit_hash"] == "c56093a326ec7d9c2436c778c50f656cb73b718c"
            and recorded_digest == sha256_bytes(raw_trace)
        )

        baseline = read_json(archive, "experiments/results/otel_native_vs_eeoap.json")
        constraints = baseline.get("comparison_constraints", [])
        results["baseline_consistent"] = (
            isinstance(constraints, list)
            and len(constraints) == 3
            and baseline.get("input_trace") == "data/otel/raw_demo_trace.json"
            and len(baseline.get("rows", [])) == 3
        )

        determinism = read_json(archive, "experiments/results/exp4_determinism_oracle.json")
        runs = determinism.get("runs", [])
        results["determinism_oracle_passed"] = (
            determinism.get("deterministic_content_equivalence") is True
            and determinism.get("validator_ok") is True
            and isinstance(runs, list)
            and len(runs) >= 3
            and len({run.get("canonical_evidence_digest") for run in runs if isinstance(run, dict)})
            == 1
        )

        results["reproducibility_script_executable"] = check_reproduce_executable(archive)
        results["single_entry_script_exists"] = "scripts/reproduce_paper.sh" in names

        text_paths = [
            "README_SOFTWAREX_SUBMISSION.md",
            "paper/softwarex_v2_revised.md",
            "paper/cover_letter.md",
            "paper/highlights.txt",
            "paper/ai_use_declaration.md",
            "docs/public/EEOAP_v0.1_public_spec.md",
            "docs/softwarex_environment.md",
            "experiments/results/otel_native_vs_eeoap.md",
        ]
        no_banned, findings = check_no_banned_phrases(archive, text_paths)
        results["no_ambiguity_keywords_detected"] = no_banned
        results["no_overclaim_phrases_detected"] = no_banned
        results["phrase_findings"] = findings

        paper_text = archive.read("paper/softwarex_v2_revised.md").decode("utf-8")
        cover_text = archive.read("paper/cover_letter.md").decode("utf-8")
        data_statement_text = archive.read("paper/data_availability_statement.md").decode("utf-8")
        softwarex_readme_text = archive.read("README_SOFTWAREX_SUBMISSION.md").decode("utf-8")
        required_ok, missing_required = check_paper_required_phrases(paper_text)
        cover_ok, missing_cover = check_cover_letter_required_phrases(cover_text)
        contribution_ok, contribution_findings = check_no_conflicting_contribution_claims(paper_text)
        manuscript_tone_ok, manuscript_tone_findings = check_no_journal_facing_manuscript_language(
            paper_text
        )
        readme_ok = all(
            phrase in softwarex_readme_text
            for phrase in [
                "# SoftwareX Submission Artifact",
                "scripts/reproduce_paper.sh",
                "release/softwarex_v2_EDITORIAL_LOCKED_FINAL_manifest.json",
                "paper/data_availability_statement.md",
                "It does not claim:",
            ]
        )
        results["cover_letter_routing_signal_present"] = cover_ok
        results["evaluation_interpreted_correctly"] = required_ok
        results["softwarex_readme_present"] = readme_ok
        results["software_artifact_classification_clear"] = required_ok and cover_ok and readme_ok
        results["no_protocol_standard_language_leakage"] = contribution_ok
        results["missing_required_paper_phrases"] = missing_required
        results["missing_required_cover_letter_phrases"] = missing_cover
        results["no_conflicting_contribution_claims"] = contribution_ok
        results["contribution_claim_findings"] = contribution_findings
        results["no_journal_facing_manuscript_language"] = manuscript_tone_ok
        results["journal_facing_manuscript_findings"] = manuscript_tone_findings
        results.update(data_availability_status(data_statement_text))
        results["external_submission_ready"] = (
            results["data_availability_url_filled"]
            and results["doi_or_persistent_identifier_filled"]
        )

        script_text = archive.read("scripts/reproduce_paper.sh").decode("utf-8")
        results["no_undefined_external_dependency"] = "curl " not in script_text and "wget " not in script_text
        results["no_internal_review_artifacts_in_submission_zip"] = not any(
            path in names for path in INTERNAL_ONLY_SUBMISSION_FILES
        )
        no_local_paths, local_path_findings = check_no_local_absolute_paths(archive)
        results["no_local_absolute_paths_in_package"] = no_local_paths
        results["local_absolute_path_findings"] = local_path_findings

    ok = all(
        bool(results[key])
        for key in [
            "schema_valid",
            "schema_spec_consistency",
            "trace_provenance_valid",
            "baseline_consistent",
            "determinism_oracle_passed",
            "single_entry_script_exists",
            "reproducibility_script_executable",
            "evaluation_interpreted_correctly",
            "software_artifact_classification_clear",
            "softwarex_readme_present",
            "cover_letter_routing_signal_present",
            "no_journal_facing_manuscript_language",
            "no_protocol_standard_language_leakage",
            "no_conflicting_contribution_claims",
            "no_ambiguity_keywords_detected",
            "no_overclaim_phrases_detected",
            "no_undefined_external_dependency",
            "no_internal_review_artifacts_in_submission_zip",
            "no_local_absolute_paths_in_package",
        ]
    )
    results["ok"] = ok
    print(json.dumps(results, indent=2, sort_keys=True))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
