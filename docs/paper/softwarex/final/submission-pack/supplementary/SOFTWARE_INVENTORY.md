# Software Inventory

## Core Modules

- `agent_evidence/media_profile.py`
- `agent_evidence/media_bundle.py`
- `agent_evidence/media_time.py`
- `agent_evidence/media_evaluation.py`
- `agent_evidence/media_adapter_evaluation.py`
- `agent_evidence/media_optional_tools.py`
- `agent_evidence/media_release_pack.py`

## Adapter Modules

- `agent_evidence/adapters/linuxptp.py`
- `agent_evidence/adapters/ffmpeg_prft.py`
- `agent_evidence/adapters/c2pa_manifest.py`

## Specifications

- `spec/aep-media-profile-v0.1.md`
- `spec/aep-media-bundle-v0.1.md`
- `spec/aep-media-time-trace-v0.1.md`
- `spec/aep-media-adapters-v0.1.md`

## Schemas

- `schema/aep_media_profile_v0_1.schema.json`
- `schema/aep_media_bundle_v0_1.schema.json`
- `schema/aep_media_time_trace_v0_1.schema.json`
- `schema/aep_media_adapter_report_v0_1.schema.json`

## Examples

- `examples/media/minimal-valid-media-evidence.json`
- `examples/media/invalid-missing-time-context.json`
- `examples/media/invalid-broken-media-hash.json`
- `examples/media/invalid-unresolved-policy-ref.json`
- `examples/media/time/`
- `examples/media/adapters/`

## Demos

- `demo/run_media_evidence_demo.py`
- `demo/run_media_bundle_demo.py`
- `demo/run_media_time_demo.py`
- `demo/run_media_adapter_demo.py`
- `demo/run_media_evaluation_demo.py`
