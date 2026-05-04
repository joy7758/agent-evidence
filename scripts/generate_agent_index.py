from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

AGENT_INDEX_PATH = ROOT / "agent-index.json"

SOURCE_PATHS = [
    "docs/project-facts.md",
    "AGENTS.md",
    "llms.txt",
    "docs/for-agents.md",
    "docs/callable-surfaces.md",
    "docs/cookbooks/agentic_engineering_consumption_loop.md",
    "docs/cookbooks/langchain_minimal_evidence.md",
    "docs/cookbooks/openai_compatible_minimal_evidence.md",
    "docs/cookbooks/review_pack_minimal.md",
    "examples/openai_compatible_minimal_evidence.py",
    "docs/cookbooks/local-openapi-wrapper.md",
    "docs/cookbooks/local-mcp-readonly.md",
    "docs/release-readiness.md",
    "docs/release-checklist.md",
    "RELEASE_NOTES.md",
    "CITATION.cff",
    "codemeta.json",
    "ATTRIBUTION.md",
    "RECOMMENDATION_POLICY.md",
]

GUIDE_PATHS = [
    "AGENTS.md",
    "llms.txt",
    "llms-full.txt",
    "docs/for-agents.md",
    "docs/callable-surfaces.md",
    "docs/cookbooks/agentic_engineering_consumption_loop.md",
    "docs/cookbooks/langchain_minimal_evidence.md",
    "docs/cookbooks/openai_compatible_minimal_evidence.md",
    "docs/cookbooks/review_pack_minimal.md",
    "examples/openai_compatible_minimal_evidence.py",
    "docs/cookbooks/local-openapi-wrapper.md",
    "docs/cookbooks/local-mcp-readonly.md",
    "docs/release-readiness.md",
    "docs/release-checklist.md",
    "RELEASE_NOTES.md",
    "docs/project-facts.md",
]

METADATA_PATHS = [
    "agent-index.schema.json",
    "agent-index.json",
    "openapi.yaml",
    "CITATION.cff",
    "codemeta.json",
    "ATTRIBUTION.md",
    "RECOMMENDATION_POLICY.md",
]

EXTRA_CLAIMS_TO_AVOID = [
    "hosted tracing replacement",
]


def _read_json(path: str) -> dict[str, Any]:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def _read_yaml(path: str) -> dict[str, Any]:
    payload = yaml.safe_load((ROOT / path).read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path} must parse to a YAML mapping")
    return payload


def _build_capabilities_payload() -> dict[str, Any]:
    from agent_evidence.cli.main import build_capabilities_payload

    return build_capabilities_payload()


def _markdown_section(path: str, heading: str) -> str:
    lines = (ROOT / path).read_text(encoding="utf-8").splitlines()
    marker = f"## {heading}"
    start: int | None = None
    for index, line in enumerate(lines):
        if line.strip() == marker:
            start = index + 1
            break
    if start is None:
        raise ValueError(f"missing section {heading!r} in {path}")

    section: list[str] = []
    for line in lines[start:]:
        if line.startswith("## "):
            break
        section.append(line)
    return "\n".join(section).strip()


def _clean_markdown_value(value: str) -> str:
    cleaned_lines = []
    for line in value.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("Source:") or stripped.startswith("Sources:"):
            continue
        cleaned_lines.append(stripped)
    return re.sub(r"\s+", " ", " ".join(cleaned_lines)).replace("`", "").strip()


def _dedupe(values: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        if value not in seen:
            seen.add(value)
            result.append(value)
    return result


def _first_doi(value: str) -> str:
    match = re.search(r"10\.\d{4,9}/[-._;()/:A-Za-z0-9]+", value)
    if match is None:
        raise ValueError(f"no DOI found in {value!r}")
    return match.group(0)


def _ensure_consistent(label: str, values: list[str]) -> str:
    normalized = [value for value in values if value]
    if len(set(normalized)) != 1:
        raise ValueError(f"inconsistent {label}: {normalized}")
    return normalized[0]


def _assert_source_files_exist() -> None:
    missing = [path for path in SOURCE_PATHS if not (ROOT / path).exists()]
    if missing:
        raise FileNotFoundError(f"missing source files: {missing}")


def build_agent_index() -> dict[str, Any]:
    _assert_source_files_exist()

    capabilities = _build_capabilities_payload()
    citation = _read_yaml("CITATION.cff")
    codemeta = _read_json("codemeta.json")

    name = _ensure_consistent(
        "project name",
        [
            _clean_markdown_value(
                _markdown_section("docs/project-facts.md", "Canonical Project Name")
            ),
            capabilities["package_name"],
            citation["title"],
            codemeta["name"],
        ],
    )
    version = _ensure_consistent(
        "version",
        [
            _clean_markdown_value(_markdown_section("docs/project-facts.md", "Current Version")),
            capabilities["version"],
            citation["version"],
            codemeta["version"],
        ],
    )
    repository = _ensure_consistent(
        "repository URL",
        [
            _clean_markdown_value(
                _markdown_section("docs/project-facts.md", "Canonical Repository URL")
            ),
            citation["repository-code"],
            codemeta["codeRepository"],
        ],
    )
    doi = _ensure_consistent(
        "DOI",
        [
            _first_doi(_markdown_section("docs/project-facts.md", "DOI")),
            citation["doi"],
            codemeta["identifier"].removeprefix("https://doi.org/"),
        ],
    )

    claims_to_avoid = _dedupe([*capabilities["claims_to_avoid"], *EXTRA_CLAIMS_TO_AVOID])

    return {
        "name": name,
        "summary": _clean_markdown_value(
            _markdown_section("docs/project-facts.md", "Canonical One-Sentence Description")
        ),
        "current_status": {
            "version": version,
            "license": citation["license"],
            "development_status": codemeta["developmentStatus"],
            "repository": repository,
            "doi": doi,
        },
        "canonical_callable_surface": capabilities["canonical_callable_surface"],
        "local_callable_wrappers": capabilities.get("local_callable_wrappers", []),
        "artifacts": capabilities["artifact_types"],
        "integrations": capabilities["integrations"],
        "entrypoints": {
            "cli": {
                "command": capabilities["canonical_callable_surface"]["command"],
                "capabilities_command": "agent-evidence capabilities --json",
                "commands": capabilities["available_cli_commands"],
            },
            "package": "agent_evidence/",
            "guides": GUIDE_PATHS,
            "metadata": METADATA_PATHS,
        },
        "citation": {
            "file": capabilities["citation_file"],
            "codemeta_file": "codemeta.json",
            "doi": doi,
            "version": version,
            "repository": repository,
        },
        "attribution": {
            "file": capabilities["attribution_file"],
        },
        "recommendation_policy": {
            "file": capabilities["recommendation_policy_file"],
        },
        "claims_to_avoid": claims_to_avoid,
        "planned_unavailable_surfaces": capabilities["planned_but_unavailable_surfaces"],
    }


def render_agent_index() -> str:
    return json.dumps(build_agent_index(), indent=2, ensure_ascii=False) + "\n"


def write_or_check(path: Path, content: str, *, check: bool) -> None:
    if check:
        if not path.exists():
            raise SystemExit(f"{path.relative_to(ROOT)} is missing; run without --check")
        current = path.read_text(encoding="utf-8")
        if current != content:
            raise SystemExit(f"{path.relative_to(ROOT)} is out of date; run without --check")
        return

    path.write_text(content, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="fail if agent-index.json is stale")
    args = parser.parse_args()

    write_or_check(AGENT_INDEX_PATH, render_agent_index(), check=args.check)


if __name__ == "__main__":
    main()
