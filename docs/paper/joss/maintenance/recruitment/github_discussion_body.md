# Call for External AEP-Media Reproducibility Reviewers

I am looking for one or two external reviewers to try AEP-Media from a fresh
clone and report whether the README and mobile-video walkthrough are actually
reproducible.

This is not a request for praise. Negative feedback is welcome. If installation
fails, a command is unclear, an expected output is missing, or the walkthrough
does not match observed behavior, that is exactly the kind of feedback needed.

Suggested task:

1. Clone the repository.
2. Install the package.
3. Run `agent-evidence --help`.
4. Run the mobile-video fixture validation, bundle build, bundle verification,
   strict-time verification, and targeted tests.
5. Post the environment, commands, outputs, failures, ambiguities, and
   suggestions in a GitHub issue or PR.

If payment is agreed separately, it compensates time spent testing and
reporting. It does not buy positive feedback, endorsement, stars, citations,
authorship, or any publication outcome.

Please use only the repository's small synthetic fixtures. Do not upload
private media, confidential logs, real evidence files, or large binaries.

Claim boundary: AEP-Media supports local validation and fixture-based adapter
ingestion. It does not claim legal admissibility, chain of custody, real PTP
proof, real C2PA verification, or production deployment.

If you are interested, please comment with your operating system, Python
version, and whether you are willing to post the result publicly as an issue or
PR.
