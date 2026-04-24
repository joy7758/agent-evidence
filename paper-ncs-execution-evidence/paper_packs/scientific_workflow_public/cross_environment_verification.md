# Cross-environment verification record

Pack: `paper-ncs-execution-evidence/paper_packs/scientific_workflow_public`
Workflow file: `/Users/zhangbin/GitHub/agent-evidence/paper-ncs-execution-evidence/.github/workflows/ncs-cross-environment.yml`

## CI matrix

| Dimension | Values |
|---|---|
| Native OS | ubuntu-latest, macos-latest |
| Python | 3.11, 3.12, 3.13 |
| Container | ghcr.io/joy7758/agent-evidence:ncs-v0.1 |

## Local verification

| Check | Exit code | Status |
|---|---:|---|
| Repository strict validator | 0 | PASS |
| Paper-local validator | 0 | PASS |
| Public failure matrix | 0 | PASS |
| Independent checker agreement | 0 | PASS |
| Local Docker container | not run | PASS |

Receipt digest: `sha256:e7fb03d517699d03e0a369727f7a200f0738d6c224b6b3b3f48a12b043ce57c2`

Remote CI status: configured, not run in this local session.

Local Docker note: Docker execution is optional locally; CI runs the declared container matrix.
