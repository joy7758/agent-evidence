# Reviewer Onboarding Message

Subject: Paid external review request for AEP-Media reproducibility

Hello,

I am preparing AEP-Media, an open-source Python package for local validation of
mobile-video-style media evidence bundles, for a future JOSS submission after
the public-history waiting period.

I am looking for real criticism, not praise. The paid task is to spend a small
fixed amount of time reproducing or reviewing one specific part of the project
and then report the result publicly through a GitHub issue or pull request.
Payment compensates your time; it does not require a positive conclusion.

Please use only the repository's small synthetic fixtures. Do not upload private
media, real evidence files, confidential logs, or large binaries.

Current suggested tasks:

- Task A: reproduce the README and mobile-video walkthrough from a fresh clone;
- Task B: review the adapter-boundary documentation for clarity and claim risk;
- Task C: submit a small regression-test PR for the mobile-video fixture.

The claim boundary is narrow: AEP-Media supports local validation and
fixture-based adapter ingestion. It does not claim legal sufficiency, external
authenticity, real PTP proof, full MP4 PRFT parsing, real C2PA signature
verification, chain of custody, or production deployment.

If you find a failure or confusing point, that is a useful outcome. Please
include exact commands, environment details, observed behavior, and suggested
fixes.

Thank you,

Bin Zhang
