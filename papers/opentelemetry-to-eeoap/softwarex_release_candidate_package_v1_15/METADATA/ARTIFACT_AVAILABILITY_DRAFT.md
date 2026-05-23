# Artifact Availability Draft

Draft; not final for submission.

The current OpenTelemetry-to-EEOAP artifacts are local to the
`agent-evidence` repository and the isolated release-candidate branch
`softwarex-otel-eeoap-release-candidate`.

The package includes:

- adapter source at `tools/opentelemetry_to_eeoap_adapter.py`;
- OpenTelemetry-style trace fixtures under `examples/opentelemetry/`;
- generated EEOAP statements and adapter reports under `generated/`;
- scoped tests at `tests/test_opentelemetry_to_eeoap_adapter.py`;
- frozen package documentation under
  `papers/opentelemetry-to-eeoap/frozen_v0_5/`;
- clean-clone verification and checksum verification materials in the paper
  package;
- SoftwareX route, release isolation, preparation, metadata strategy, and
  metadata draft materials under `papers/opentelemetry-to-eeoap/`.

Two local related artifact tags exist:

- `eeoap-v0.1-artifact`
- `aep-v0.1-artifact`

These tags are local only. They have not been pushed to a remote repository and
have not been archived.

No DOI or public GitHub Release has been created for the
OpenTelemetry-to-EEOAP package. The final external artifact availability
statement must be updated after a public release, archive, pushed tag, or DOI is
created.
