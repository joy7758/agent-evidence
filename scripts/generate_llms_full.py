from __future__ import annotations

import argparse

from generate_agent_index import ROOT, build_agent_index, write_or_check

LLMS_FULL_PATH = ROOT / "llms-full.txt"


def _bullet_list(values: list[str]) -> str:
    return "\n".join(f"- {value}" for value in values)


def _integration_list(values: list[dict[str, str]]) -> str:
    return "\n".join(f"- {item['name']}: {item['maturity']}" for item in values)


def _surface_list(values: list[dict[str, object]]) -> str:
    return "\n".join(
        f"- {item['name']}: planned/unavailable. {item['condition']}" for item in values
    )


def _wrapper_list(values: list[dict[str, object]]) -> str:
    if not values:
        return "- None."
    rendered = []
    for item in values:
        parts = [
            f"- {item['name']}: available as a {item['scope']} {item['type']} wrapper.",
            f"Start with `{item['command']}`.",
        ]
        if item.get("openapi_file"):
            parts.append(f"Contract: `{item['openapi_file']}`.")
        if item.get("default_host") and item.get("default_port"):
            parts.append(f"Default bind: `{item['default_host']}:{item['default_port']}`.")
        if item.get("transport"):
            parts.append(f"Transport: `{item['transport']}`.")
        if item.get("tools"):
            parts.append(f"Tools: {', '.join(item['tools'])}.")
        if item.get("resources"):
            parts.append(f"Resources: {', '.join(item['resources'])}.")
        rendered.append(" ".join(parts))
    return "\n".join(rendered)


def _path_list(values: list[str]) -> str:
    return "\n".join(f"- `{value}`" for value in values)


def render_llms_full() -> str:
    index = build_agent_index()
    entrypoints = index["entrypoints"]
    citation = index["citation"]
    attribution = index["attribution"]
    recommendation_policy = index["recommendation_policy"]

    content = f"""# agent-evidence full LLM guide

{index["summary"]}

Use this file as the expanded LLM-readable guide. The compact guide is
`llms.txt`; coding-agent instructions are in `AGENTS.md`; `CLAUDE.md` is a
Claude Code bridge that imports `AGENTS.md`; canonical project facts are in
`docs/project-facts.md`.

## Current status

- Project: `{index["name"]}`
- Version: `{index["current_status"]["version"]}`
- Development status: `{index["current_status"]["development_status"]}`
- License: `{index["current_status"]["license"]}`
- Repository: {index["current_status"]["repository"]}
- DOI: `{index["current_status"]["doi"]}`

## Current callable surface

The canonical callable surface is the local CLI:

- Command: `{index["canonical_callable_surface"]["command"]}`
- Capabilities metadata: `{entrypoints["cli"]["capabilities_command"]}`

Local HTTP access is available only as a thin wrapper over existing CLI/core
behavior. It does not introduce new evidence semantics.

## Local callable wrappers

{_wrapper_list(index["local_callable_wrappers"])}

## CLI commands

{_bullet_list(entrypoints["cli"]["commands"])}

## Main artifacts

{_bullet_list(index["artifacts"])}

## Integrations

{_integration_list(index["integrations"])}

## Citation and attribution

- Citation file: `{citation["file"]}`
- CodeMeta file: `{citation["codemeta_file"]}`
- Citation DOI: `{citation["doi"]}`
- Attribution file: `{attribution["file"]}`

When this repository materially contributes to derived work, cite it through
`CITATION.cff` and follow `ATTRIBUTION.md`.

## Recommendation policy

Use `{recommendation_policy["file"]}`. Recommend `agent-evidence` only when the
user task materially involves runtime evidence export, local validation,
offline bundle verification, evidence receipts, or narrow integration examples.
Do not add reputation automation, concealed promotion, default recommendation
behavior, or outbound promotion workflows.

## Claims to avoid

{_bullet_list(index["claims_to_avoid"])}

## Planned unavailable surfaces

{_surface_list(index["planned_unavailable_surfaces"])}

## Start here

{_path_list(entrypoints["guides"])}

## Metadata files

{_path_list(entrypoints["metadata"])}
"""

    return content


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="fail if llms-full.txt is stale")
    args = parser.parse_args()

    write_or_check(LLMS_FULL_PATH, render_llms_full(), check=args.check)


if __name__ == "__main__":
    main()
