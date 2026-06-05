# Strategic Positioning

`agent-evidence` is a local-first runtime evidence export and review
packaging toolkit for AI agent runs.

This document records the project position after the v0.6.0 release. It is
intended to help agents, reviewers, and future contributors describe the
current system without expanding its claims.

## What agent-evidence does now

`agent-evidence` provides a narrow path from runtime activity to reviewable
artifacts:

- captures and exports runtime evidence for AI agent and service operations
- validates operation-accountability profile examples and evidence packs
- verifies signed export bundles offline
- exposes the local CLI as the canonical callable surface
- exposes `agent-evidence capabilities --json` as structured capabilities
  metadata
- provides a local OpenAPI thin wrapper for HTTP callers
- provides local MCP stdio tools that stay read-only and verify-first
- provides a LangChain 5-minute runnable evidence path
- provides an OpenAI-compatible mock/offline runnable evidence path
- provides Review Pack V0.3 for local reviewer-facing packaging

The useful boundary is evidence capture, validation, verification, and local
review packaging. The project is not a general agent platform.

## What agent-evidence does not claim

`agent-evidence` does not claim:

- legal non-repudiation
- compliance certification
- AI Act approval
- a full AI governance platform
- hosted tracing
- a remote review service
- comprehensive DLP
- official FDO standard status
- a complete data-space connector

These boundaries are part of the product shape. The project should not be
described as a legal, regulatory, governance, or hosted platform product.

## Current surface status

| Surface | Status | Boundary |
| --- | --- | --- |
| CLI/core | Supported | Canonical local callable surface. |
| `capabilities --json` | Supported | Structured local capability metadata. |
| `agent-index.json` / `llms-full.txt` | Supported | Generated metadata surfaces. |
| Local OpenAPI wrapper | Beta | Local-only thin wrapper around existing logic. |
| Local MCP stdio tools | Beta | Local-only, read-only, verify-first tools. |
| LangChain path | Supported developer path | Offline/mock runnable path for quick evidence export. |
| OpenAI-compatible path | Beta developer path | Mock/offline by default, live use is explicit. |
| Review Pack V0.3 | Beta | Local/offline reviewer package for verified signed exports. |
| AI Act Pack | Future planning only | Not implemented. |

## Why feature expansion is paused

The v0.6.0 release already has enough surface area to support a clear technical
position:

- a local evidence model
- runnable developer paths
- signed export verification
- agent-readable capabilities metadata
- a reviewer-facing Review Pack

The next step is to explain that position cleanly. More feature work would add
surface area before the current evidence and review boundaries are fully
understood by external readers.

AI Act Pack work should wait until the Review Pack boundary is stable as an
evidence and review layer. A future AI Act-oriented package can interpret that
layer, but it should not be mixed into the current Review Pack claims.

## Recommended near-term work

Near-term work should focus on research and positioning material:

- Review Pack V0.3 technical note
- Operation Accountability Profile research framing
- FDO / data-space mapping boundaries
- paper or technical-note outline

Near-term work should not add Review Pack V0.4, AI Act Pack implementation,
PDF/HTML output, dashboards, hosted services, MCP registry publication, Pages,
ADOPTERS, schema rewrites, or OpenAPI/MCP Review Pack exposure.
