Suggested title: [External Review Needed] Reproduce AEP-Media mobile-video fixture from fresh clone

# External reproducibility review needed

## Summary

AEP-Media is an open-source Python research software component for local
validation of time-aware media evidence bundles.

This issue invites an external reviewer to test whether a new user can
reproduce the AEP-Media mobile-video-style fixture from a fresh clone.

The goal is reproducibility feedback, not praise.

## Project facts

- Repository: https://github.com/joy7758/agent-evidence
- Software: AEP-Media
- Language: Python
- License: Apache-2.0
- Release: aep-media-v0.1.0
- Archive DOI: 10.5281/zenodo.20107097
- Task type: external reproducibility review
- Expected effort: 1-2 hours
- Skill level: Python CLI user
- Good for: documentation review, reproducibility testing, first-time
  contributor

## What AEP-Media does

AEP-Media validates local media evidence bundles.

A media evidence bundle is a local review package that connects:

- a media artifact or media reference;
- a declared operation;
- actor, subject, and policy context;
- provenance sidecars;
- declared timing evidence;
- file hashes;
- bundle checksums;
- adapter reports;
- validation output.

AEP-Media checks whether the package is internally complete, hash-consistent,
path-safe, time-bounded, and diagnosable.

## What AEP-Media does not claim

AEP-Media does not claim:

- legal admissibility;
- chain of custody;
- non-repudiation;
- trusted timestamping;
- real PTP proof;
- full MP4 PRFT parsing;
- real C2PA signature verification;
- production deployment;
- proof that the underlying event is truthful.

## Review task

Please start from a fresh clone and run the mobile-video-style walkthrough.

Report whether the instructions are clear, whether the commands run, and where
the documentation or output is confusing.

## Commands to run

```bash
git clone https://github.com/joy7758/agent-evidence
cd agent-evidence

python -m pip install -e .

agent-evidence --help

agent-evidence validate-media-profile \
  examples/media/use_cases/mobile_video_network_timing/mobile-video-operation-evidence.json

agent-evidence build-media-bundle \
  examples/media/use_cases/mobile_video_network_timing/mobile-video-operation-evidence.json \
  --out /tmp/aep-media-mobile-video-bundle

agent-evidence verify-media-bundle \
  /tmp/aep-media-mobile-video-bundle

agent-evidence verify-media-bundle \
  /tmp/aep-media-mobile-video-bundle \
  --strict-time

python -m pytest \
  tests/test_media_cli_registration.py \
  tests/test_media_evaluation.py \
  -q
```

## Please report

Please comment with:

- operating system;
- Python version;
- shell used;
- install command used;
- exact commands run;
- output summary;
- first failure, if any;
- unclear documentation;
- confusing terminology;
- missing expected output;
- suggested fix.

## Acceptance criteria

A useful review comment or PR should include:

- environment information;
- commands run;
- reproducible output or error;
- at least one actionable suggestion;
- no private media files;
- no large binary files;
- no unsupported forensic or legal claims.

## Good outcomes

Any of these outcomes is useful:

- "Everything worked; here is my environment and output."
- "Command X failed; here is the error."
- "Step Y was unclear; here is a suggested wording fix."
- "The output was correct but hard to interpret."
- "I opened a PR to improve the walkthrough."

## Payment and disclosure

If this is a paid review, payment compensates time spent testing and reporting.

Payment does not buy:

- positive feedback;
- stars;
- citations;
- endorsement;
- authorship;
- publication outcome.

Negative feedback is welcome.

## Labels

Suggested labels:

- help wanted
- reproducibility
- documentation
- good first issue
- Python
- CLI
