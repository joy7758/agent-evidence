# AEP-Media SoftwareX Metadata

## Software Name

AEP-Media, within `agent-evidence`

## Repository

https://github.com/joy7758/agent-evidence

## GitHub Release

https://github.com/joy7758/agent-evidence/releases/tag/aep-media-v0.1.0

## Primary Package / Module

`agent_evidence`

## Relevant Modules

- `agent_evidence/media_profile.py`
- `agent_evidence/media_bundle.py`
- `agent_evidence/media_time.py`
- `agent_evidence/media_evaluation.py`
- `agent_evidence/media_adapter_evaluation.py`
- `agent_evidence/media_optional_tools.py`
- `agent_evidence/media_release_pack.py`
- `agent_evidence/media_submission_pack.py`
- `agent_evidence/adapters/linuxptp.py`
- `agent_evidence/adapters/ffmpeg_prft.py`
- `agent_evidence/adapters/c2pa_manifest.py`

## Command-line Entry Points

- `agent-evidence validate-media-profile`
- `agent-evidence build-media-bundle`
- `agent-evidence verify-media-bundle`
- `agent-evidence validate-media-time-profile`
- `agent-evidence run-media-evaluation`
- `agent-evidence build-aep-media-release-pack`
- `agent-evidence build-aep-media-submission-pack`

## Programming Language

Python 3.11+

## Operating Systems

The repository is developed and tested in a Python 3.11+ environment. AEP-Media v0.1.0 reports record fixture-based validation paths that do not require LinuxPTP, FFmpeg, ffprobe, or C2PA to be installed.

## License

Apache-2.0. The repository contains `LICENSE`, and `pyproject.toml` declares `license = "Apache-2.0"`.

## Documentation

- `spec/`
- `schema/`
- `examples/media/`
- `demo/`
- `docs/reports/`
- `docs/paper/softwarex/`

## Test Suite

AEP-Media v0.1.0 final validation results:

- Targeted AEP-Media tests: `48 passed, 1 warning`;
- SoftwareX/readiness tests: `23 passed, 1 warning`;
- Full repository tests: `155 passed, 1 skipped, 15 warnings`;
- Default evaluation: `PASS aep-media-evaluation@0.1 cases=18 unexpected=0`;
- Adapter-inclusive evaluation: `PASS aep-media-evaluation@0.1 cases=26 unexpected=0 adapters=included`;
- Optional-tool evaluation: `PASS aep-media-evaluation@0.1 cases=23 unexpected=0 optional_tools=included`;
- Combined evaluation: `PASS aep-media-evaluation@0.1 cases=31 unexpected=0 adapters=included optional_tools=included`.

## Archive / DOI

AEP-Media-specific archive DOI: `10.5281/zenodo.20107097`.

Zenodo record: <https://zenodo.org/records/20107097>.

## Software Availability Notes

The SoftwareX package points to the tagged release, archived DOI, installation instructions, examples, test commands, and release notes. Final portal metadata should use the AEP-Media-specific DOI above.
