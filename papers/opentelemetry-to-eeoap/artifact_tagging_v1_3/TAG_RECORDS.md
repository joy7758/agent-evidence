# Tag Records

| Artifact | Tag name | Tag object hash | Target commit hash | Status | Message | Pushed to remote | Notes |
|---|---|---|---|---|---|---|---|
| EEOAP | `eeoap-v0.1-artifact` | `f4270a575517f987dcd45d8ef80a7d30d808f39f` | `96f444b7ed39b39fe9f47e428af835952e843cb0` | created | `EEOAP v0.1 artifact used by OpenTelemetry-to-EEOAP paper` | no | Created as a local annotated alias for the existing `eeoap-v0.1-paper` target. |
| AEP | `aep-v0.1-artifact` | `a58aa33501252b26acde085fed3dfa0104e255a0` | `af2b90c14587718a8ed6982131ba9c98e3274054` | created | `AEP v0.1 artifact referenced by OpenTelemetry-to-EEOAP paper` | no | Created as a local annotated tag for the AEP live-chain specimen target identified by `v0.1-live-chain-security`. |

## Verification Commands

```bash
git show --no-patch --decorate --format=fuller eeoap-v0.1-artifact
git rev-parse eeoap-v0.1-artifact
git rev-parse eeoap-v0.1-artifact^{}
git show --no-patch --decorate --format=fuller aep-v0.1-artifact
git rev-parse aep-v0.1-artifact
git rev-parse aep-v0.1-artifact^{}
```

## Push Status

No tag was pushed to a remote. No GitHub Release or DOI was created.
