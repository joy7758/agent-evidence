# Examples

## Current primary runnable example

The current primary runnable example in this repository is:

- [`langchain_minimal_evidence.py`](./langchain_minimal_evidence.py)
  - Recommended LangChain entry point for the current quickstart path.
  - Produces the normalized outputs used in this repo today:
    `bundle`, `receipt`, and `summary`.
  - Uses the recommended public API:

    ```python
    from agent_evidence.integrations.langchain import LangChainAdapter

    adapter = LangChainAdapter.for_output_dir("./artifacts/langchain-run")
    callbacks = [adapter.callback_handler()]
    artifacts = adapter.finalize()
    ```

  - Supporting files such as the manifest sidecar, local keys, and runtime JSONL
    remain supporting materials rather than additional primary outputs.

Related docs:

- [`../docs/cookbooks/langchain_minimal_evidence.md`](../docs/cookbooks/langchain_minimal_evidence.md)
- [`../integrations/langchain/README.md`](../integrations/langchain/README.md)

## Operation Accountability Statement examples

These examples are the current primary example surface for
`execution-evidence-operation-accountability-profile@0.1`.

They belong to the current Agent Evidence / AEP v0.1 path rather than the older
`Execution Evidence Object` top-level surface. Historical naming and prototype
materials remain documented in [docs/lineage.md](../docs/lineage.md).

Each file is intended to produce one validation report.

## Files

- `minimal-valid-evidence.json`
  - Passes schema, reference closure, policy/provenance/evidence consistency,
    and integrity recomputation.
- `valid-retention-review-evidence.json`
  - Passes the same profile checks in a second context:
    one dataset package subject, two input references, and one retention decision output.
  - Main value: second-context validity evidence for the same minimal profile.
- `valid-high-risk-payment-review-evidence.json`
  - Passes the same profile checks in a high-risk, reviewer-facing context:
    one flagged payment case subject, two input references, and one review decision output.
  - Main value: a discoverable high-risk scenario entry without changing the v0.1 boundary.
- `valid-trust-binding-evidence.json`
  - Passes the same local profile checks while also carrying one optional
    `validation.trust_bindings[]` entry.
  - Main value: shows how to point to an external trust source without making
    that source mandatory for local conformance.
- `invalid-missing-required.json`
  - Fails because `validation.method` is intentionally removed.
  - Main broken rule: required field completeness.
- `invalid-unclosed-reference.json`
  - Fails because the operation output reference points to `ref:missing-output`,
    which is not defined in `evidence.references`.
  - Main broken rule: reference closure.
- `invalid-policy-link-broken.json`
  - Fails because `evidence.policy_ref` points to `policy:stale-metadata-v1`
    instead of the declared `policy.id`.
  - Main broken rule: policy/evidence link consistency.
- `invalid-high-risk-unclosed-reference.json`
  - Fails because the operation output reference points to
    `ref:missing-review-decision`, which is not defined in `evidence.references`.
  - Main broken rule: reference closure.
- `invalid-high-risk-policy-link-broken.json`
  - Fails because `evidence.policy_ref` points to
    `policy:stale-payment-review-v1` instead of the declared `policy.id`.
  - Main broken rule: policy/evidence link consistency.
- `invalid-provenance-output-mismatch.json`
  - Fails because `provenance.output_refs` points to `ref:input-note`
    instead of matching `operation.output_refs`.
  - Main broken rule: provenance/operation cross-field binding consistency.
- `invalid-validation-provenance-link-broken.json`
  - Fails because `validation.provenance_ref` points to
    `prov:missing-metadata-enrich-001`, which is not defined locally.
  - Main broken rule: validation/provenance reference closure.
- `invalid-trust-binding-digest-mismatch.json`
  - Fails because `validation.trust_bindings[0].target_digest` does not match
    the local digest of the target statement.
  - Main broken rule: trust-binding/local-target consistency.

Command note:

- The commands below assume `agent-evidence` is installed in the active environment.
- If you are using the repository virtualenv directly, run
  `.venv/bin/agent-evidence ...` instead.

## Validate

```bash
agent-evidence validate-profile examples/minimal-valid-evidence.json
agent-evidence validate-profile examples/valid-retention-review-evidence.json
agent-evidence validate-profile examples/valid-high-risk-payment-review-evidence.json
agent-evidence validate-profile examples/valid-trust-binding-evidence.json
agent-evidence validate-profile examples/invalid-missing-required.json
agent-evidence validate-profile examples/invalid-unclosed-reference.json
agent-evidence validate-profile examples/invalid-policy-link-broken.json
agent-evidence validate-profile examples/invalid-high-risk-unclosed-reference.json
agent-evidence validate-profile examples/invalid-high-risk-policy-link-broken.json
agent-evidence validate-profile examples/invalid-provenance-output-mismatch.json
agent-evidence validate-profile examples/invalid-validation-provenance-link-broken.json
agent-evidence validate-profile examples/invalid-trust-binding-digest-mismatch.json
```
