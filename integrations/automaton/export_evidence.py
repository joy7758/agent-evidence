from __future__ import annotations

import argparse
import json
from pathlib import Path

from agent_evidence.aep import verify_bundle
from agent_evidence.integrations import export_automaton_bundle


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Experimental thin wrapper around the Automaton AEP exporter."
    )
    parser.add_argument(
        "--state-db",
        type=Path,
        required=True,
        help="Path to Automaton state.db",
    )
    parser.add_argument(
        "--repo-root",
        "--repo",
        dest="repo_root",
        type=Path,
        help="Path to the Automaton state git repository",
    )
    parser.add_argument(
        "--output-dir",
        "--out",
        dest="output_dir",
        type=Path,
        required=True,
        help="Directory to write the AEP bundle",
    )
    parser.add_argument(
        "--runtime-root",
        type=Path,
        help="Optional Automaton runtime checkout used to resolve version metadata",
    )
    parser.add_argument("--limit", type=int, default=50, help="Per-source record limit")
    args = parser.parse_args()

    bundle_dir = export_automaton_bundle(
        state_db_path=args.state_db,
        repo_root=args.repo_root,
        runtime_root=args.runtime_root,
        output_dir=args.output_dir,
        limit=args.limit,
    )
    print(bundle_dir)
    print(json.dumps(verify_bundle(bundle_dir), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
