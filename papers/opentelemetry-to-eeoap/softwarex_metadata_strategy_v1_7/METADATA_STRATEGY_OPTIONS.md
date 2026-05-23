# Metadata Strategy Options

## Option A: Update Root Metadata for the Whole Repository

Description:
Update root `CITATION.cff` and `codemeta.json` to represent the whole
`agent-evidence` repository, including OpenTelemetry-to-EEOAP.

Advantages:

- Gives SoftwareX a conventional root-level metadata surface.
- Keeps citation and CodeMeta files at standard repository locations.
- Could represent `agent-evidence` as the primary software object.

Risks:

- Root metadata currently represents AEP-Media and includes an AEP-Media DOI.
- Changing it now could corrupt or confuse the AEP-Media paper/release line.
- It may make OpenTelemetry-to-EEOAP appear broader than the actual adapter
  package.
- It requires a repository-level release-scope decision that has not been made.

SoftwareX suitability: medium later, low now.

Impact on existing AEP-Media metadata: high risk.

Requires code or repo layout changes? no, but it requires release-scope and
metadata-policy decisions.

Recommendation: no for now.

## Option B: Keep Root Metadata Unchanged and Create Paper-Local Metadata

Description:
Keep root `CITATION.cff` and `codemeta.json` unchanged for now, and create
OpenTelemetry-to-EEOAP-specific metadata files under
`papers/opentelemetry-to-eeoap/`.

Advantages:

- Avoids overwriting AEP-Media metadata.
- Keeps the current route bounded to OpenTelemetry-to-EEOAP.
- Allows metadata drafting before public release or DOI decisions.
- Fits the current release-candidate branch as a preparation surface.

Risks:

- Paper-local metadata may not be sufficient as final SoftwareX submission
  metadata if SoftwareX expects root-level metadata.
- A future release may still require root metadata or release-asset metadata.
- Reviewers may need a clear artifact availability statement explaining the
  metadata location.

SoftwareX suitability: high for preparation, medium for final submission unless
converted into final release metadata.

Impact on existing AEP-Media metadata: low.

Requires code or repo layout changes? no.

Recommendation: yes now.

## Option C: Focused Release Branch with Root Metadata Changed

Description:
Create or use a focused release branch where root metadata is changed
specifically for OpenTelemetry-to-EEOAP after the SoftwareX route is confirmed.

Advantages:

- Provides a clean root-level SoftwareX metadata surface.
- Avoids changing the original dirty worktree.
- Makes a release candidate easier to inspect.

Risks:

- Could diverge from main repository metadata.
- Needs careful branch naming, release notes, and tag strategy.
- Premature use could still conflict with AEP-Media release references.

SoftwareX suitability: high later.

Impact on existing AEP-Media metadata: medium, depending on branch/release
policy.

Requires code or repo layout changes? no code change required; metadata files
would change later.

Recommendation: not now, but keep as a later option if SoftwareX route is
confirmed.

## Option D: Subpackage-Style Metadata Set

Description:
Create a dedicated OpenTelemetry-to-EEOAP metadata set under a focused package
or release directory if repository policy allows.

Advantages:

- Clearly scopes metadata to the adapter package.
- Avoids root AEP-Media metadata conflict.
- Could support a focused release payload.

Risks:

- The repository does not currently expose OpenTelemetry-to-EEOAP as a formal
  Python subpackage.
- May invite layout changes if interpreted too broadly.
- SoftwareX final expectations may still favor root-level release metadata.

SoftwareX suitability: medium to high if the release package is clearly
documented.

Impact on existing AEP-Media metadata: low.

Requires code or repo layout changes? no if metadata-only; yes if it becomes a
real source-layout refactor.

Recommendation: no as a first step, but compatible with Option B.
