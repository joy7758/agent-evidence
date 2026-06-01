# Mobile Video + Network Timing Fixture

This fixture set is a **fixture-only mobile-video-style review workflow** for
AEP-Media.

- It is intentionally lightweight and uses a tiny placeholder media file.
- It demonstrates a local, reproducible bundle built from declared artifacts:
  - mobile media artifact reference (placeholder binary)
  - network timing trace artifact (AEP-Media time-trace fixture)
  - ffprobe-style metadata fixture
  - C2PA-like provenance sidecar fixture

Scenario:
A mobile app captures a short inspection video. The package records:
- media reference,
- declared time window,
- capture policy,
- network timing fixture,
- ffprobe-style timing metadata,
- C2PA-like provenance sidecar.

The bundle can be validated through `validate-media-profile`, `build-media-bundle`,
and `verify-media-bundle`. This is a **fixture-based demonstration only**.
It does not claim:
- real mobile deployment,
- real network PTP/NTP proof,
- real PRFT binary parsing,
- real C2PA signature verification.

For the step-by-step walkthrough, see
[docs/aep-media/mobile-video-walkthrough.md](../../../../docs/aep-media/mobile-video-walkthrough.md).

## Commands

```bash
python -m pip install -e .

agent-evidence validate-media-profile \
  examples/media/use_cases/mobile_video_network_timing/mobile-video-operation-evidence.json

agent-evidence build-media-bundle \
  examples/media/use_cases/mobile_video_network_timing/mobile-video-operation-evidence.json \
  --out review-output/mobile-video-bundle

agent-evidence verify-media-bundle review-output/mobile-video-bundle

agent-evidence verify-media-bundle review-output/mobile-video-bundle --strict-time
```

Expected high-level outcome for the valid case:

- profile validation passes;
- bundle build prints `PASS aep-media-bundle@0.1 build`;
- normal bundle verification passes;
- strict-time bundle verification passes.

## Controlled negative cases

The `invalid/` directory contains three small mutated statements:

- `invalid-mobile-video-broken-hash.json` should fail profile validation with `media_hash_mismatch`.
- `invalid-mobile-video-missing-timing-ref.json` should pass base profile validation but fail strict-time bundle verification with `missing_clock_trace_ref`.
- `invalid-mobile-video-unresolved-provenance-ref.json` should fail profile validation with `unresolved_actor_ref`.

Expected outcomes are summarized in `expected/expected-validation-summary.json`.
