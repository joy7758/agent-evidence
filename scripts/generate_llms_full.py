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
`llms.txt`; coding-agent instructions are in `AGENTS.md`; canonical project
facts are in `docs/project-facts.md`.

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

OpenAPI and MCP are planned/unavailable until real local wrappers exist and
reuse the existing validation/export logic.

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
