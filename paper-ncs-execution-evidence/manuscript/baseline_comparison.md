# Baseline comparison draft

The proposed method is not a competing workflow metadata standard. It is a validator-backed operation-evidence layer that can be embedded into, or linked from, existing packaging and provenance systems.

| Baseline | Captures provenance | Packages artifacts | Hash/integrity support | Deterministic validator | Explicit failure taxonomy | Operation-level accountability | Agent/tool-use support | Best use |
|---|---|---|---|---|---|---|---|---|
| Logs-only | Partial | No | Rare | No | No | Weak | Partial | debugging and operational records |
| Traces / OpenTelemetry | Partial | No | Limited | No | No | Partial | Strong for runtime tracing | observability and distributed tracing |
| W3C PROV | Yes | No | Optional/external | No | No | Partial | Possible with modeling | provenance graph representation |
| RO-Crate | Yes | Yes | Optional/external | No | No | Partial | Possible with extensions | research object packaging |
| Workflow Run RO-Crate | Yes | Yes | Optional/external | Partial | No | Partial | Limited | workflow run packaging |
| BioCompute Object | Yes | Partial | Yes | Partial | No | Partial | No | regulated biomedical computation descriptions |
| Agent tracing tools | Partial | No | Limited | Tool-specific | No | Partial | Yes | inspecting agent/tool interactions |
| Proposed execution-evidence boundary | Yes | Yes | Yes | Yes | Yes | Yes | Secondary generalization | independently verifiable operation evidence |
