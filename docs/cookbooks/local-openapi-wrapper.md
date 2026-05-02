# Local OpenAPI Wrapper

The local API is a stdlib HTTP wrapper for agents that need to call
`agent-evidence` through HTTP on the same machine. The CLI/core remains the
canonical implementation surface; this wrapper delegates to existing behavior
and does not introduce new evidence semantics.

## Start the Server

```bash
agent-evidence serve --host 127.0.0.1 --port 8765
```

Defaults are local:

- host: `127.0.0.1`
- port: `8765`

The OpenAPI contract is `openapi.yaml`.

## Health Check

```bash
curl -s http://127.0.0.1:8765/healthz | python -m json.tool
```

Expected shape:

```json
{
  "service": "agent-evidence-local-api",
  "status": "ok"
}
```

## Capabilities

```bash
curl -s http://127.0.0.1:8765/v1/capabilities | python -m json.tool
```

This returns the same structured payload as:

```bash
agent-evidence capabilities --json
```

## Validate a Profile

Validate an inline profile:

```bash
curl -s http://127.0.0.1:8765/v1/profiles/validate \
  -H 'Content-Type: application/json' \
  --data @profile-request.json | python -m json.tool
```

Where `profile-request.json` has this shape:

```json
{
  "profile": {}
}
```

Validate a local profile file:

```json
{
  "profile_path": "examples/minimal-valid-evidence.json"
}
```

Optional field:

```json
{
  "profile_path": "examples/minimal-valid-evidence.json",
  "fail_fast": true
}
```

The endpoint calls the existing profile validation implementation and rejects
unsupported request shapes.

## Verify a Bundle

Verify a local bundle directory:

```bash
curl -s http://127.0.0.1:8765/v1/bundles/verify \
  -H 'Content-Type: application/json' \
  --data '{"bundle_path":"tests/fixtures/agent_evidence_profile/valid/basic-bundle"}' \
  | python -m json.tool
```

The endpoint calls `agent_evidence.aep.verify_bundle()`.

## Limitations

- CLI/core remains canonical.
- The server is intended for local use on `127.0.0.1`.
- There is no hosted mode.
- There is no auth system.
- There is no MCP server yet.
- There is no telemetry.
- There is no Review Pack endpoint.
- The wrapper does not duplicate validation or verification logic.
