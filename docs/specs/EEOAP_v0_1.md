# EEOAP v0.1 Local Specification

Affected clauses: EEOAP-001, EEOAP-002, EEOAP-003, EEOAP-004, EEOAP-005.

## Definition

EEOAP means Execution Evidence and Operation Accountability Profile. In this
repository it is a local, profile-aware validation surface for completed
operations. It packages operation identity, actor, subject, policy, provenance,
evidence references, and a validator-readable validation result into a
reviewable evidence statement.

For the SoftwareX v2 grounding repair, the repository also defines a
trace-grounded EEOAP record shape for OpenTelemetry inputs. That record has:

- `execution_id`: execution identifier.
- `timestamp`: selected event time.
- `trace_source`: OpenTelemetry source metadata.
- `spans[]`: normalized execution spans.
- `evidence[]`: audit evidence objects and derived outputs.
- `status`: execution status.
- `version`: fixed to `v0.1`.

The canonical local profile validator remains:

```bash
agent-evidence validate-profile examples/minimal-valid-evidence.json
```

## Scope

This specification covers local conversion from an OTLP JSON trace into a
reviewable EEOAP evidence statement and a small trace-grounding record.

It supports:

- trace-source digest binding;
- span identity preservation;
- input/output evidence references;
- repository-local validation with `agent-evidence validate-profile`;
- review examples and experiment receipts.

It does not claim:

- official FDO or standards-body adoption;
- legal non-repudiation;
- compliance certification;
- trusted timestamping;
- production deployment readiness;
- external validation or publication status.

## Schema Link

The trace-grounded schema is:

```text
specs/eeoap/v0.1/eeoap.schema.json
```

The existing operation-accountability statement schema remains:

```text
schema/execution-evidence-operation-accountability-profile-v0.1.schema.json
```

The protocol clause index remains:

```text
protocol/clause-index.json
```

## Versioning Rules

- `v0.1` is the local trace-grounding record version used for this repair
  surface.
- Compatible changes may add optional documentation, examples, or experiments
  without changing the schema version.
- Any change that removes required fields, changes field meaning, or changes
  validation semantics requires a new versioned schema path.
- Clause IDs `EEOAP-001` through `EEOAP-005` remain stable and must be cited
  in task or PR summaries when evidence/profile behavior is changed.

## Minimal Example

```json
{
  "version": "v0.1",
  "execution_id": "eeoap:otel-demo:5b8efff798038103d269b633813fc60c",
  "timestamp": "2018-12-13T14:51:00Z",
  "trace_source": {
    "system": "opentelemetry",
    "format": "otlp-json",
    "locator": "data/otel/raw_demo_trace.json",
    "digest": "sha256:<64 lowercase hex chars>"
  },
  "spans": [
    {
      "trace_id": "5B8EFFF798038103D269B633813FC60C",
      "span_id": "EEE19B7EC3C1B174",
      "parent_span_id": "EEE19B7EC3C1B173",
      "name": "I'm a server span",
      "start_time_unix_nano": "1544712660000000000",
      "end_time_unix_nano": "1544712661000000000",
      "kind": 2,
      "attributes": {
        "my.span.attr": "some value"
      }
    }
  ],
  "evidence": [
    {
      "evidence_id": "evidence:raw-otlp-trace",
      "role": "input",
      "object_ref": "trace:5B8EFFF798038103D269B633813FC60C",
      "digest": "sha256:<64 lowercase hex chars>",
      "locator": "data/otel/raw_demo_trace.json",
      "derived_from_span_ids": [
        "EEE19B7EC3C1B174"
      ]
    }
  ],
  "status": "succeeded"
}
```

The example is illustrative. Real generated evidence must be checked through
the local validator and must not be reported as external certification or
publication evidence.
