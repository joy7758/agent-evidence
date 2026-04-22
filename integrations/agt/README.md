# AGT-to-EEOAP Interoperability Adapter

This integration is a reference interoperability adapter, not an AGT plugin and
not a replacement for AGT runtime evidence verification.

This directory contains a minimal reference adapter that maps a synthetic
AGT-like runtime evidence fixture into the Execution Evidence and Operation
Accountability Profile v0.1.

The fixture is synthetic. It is not an official Microsoft Agent Governance
Toolkit schema and should not be treated as one. The purpose is to demonstrate a
stable interoperability boundary:

```text
AGT-like runtime evidence
-> EEOAP v0.1 statement
-> agent-evidence validate-profile
-> PASS / FAIL result
```

AGT remains the upstream runtime governance source. EEOAP v0.1 remains the
external operation-accountability profile. This adapter does not replace
`agt verify --evidence`.

## Usage

Run the converter:

```bash
python integrations/agt/convert_agt_evidence_to_eeoap.py \
  --input integrations/agt/fixtures/agt-evidence-minimal.synthetic.json \
  --output integrations/agt/fixtures/eeoap-from-agt.generated.json
```

Validate the generated statement:

```bash
agent-evidence validate-profile integrations/agt/fixtures/eeoap-from-agt.generated.json
```

You can also compare the generated output with the deterministic expected
fixture:

```bash
diff -u \
  integrations/agt/fixtures/eeoap-from-agt.expected.json \
  integrations/agt/fixtures/eeoap-from-agt.generated.json
```

## Mapping Boundary

The EEOAP statement does not add AGT-specific top-level fields. Synthetic AGT
runtime material is represented through `evidence.artifacts[]`, including a
digest of the source fixture and the AGT-like decision receipt artifact.

Non-goals:

- No AGT runtime modification
- No AGT policy engine modification
- No new EEOAP v0.1 fields
- No AGT package dependency
- No replacement of `agt verify --evidence`
