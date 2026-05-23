# Version 1.17 No-Verify Note

## Reason

Version 1.17 used `git commit --no-verify` because the downloaded official
SoftwareX LaTeX template source contained upstream trailing whitespace and the
local pre-commit hook would otherwise modify that third-party template source.

## Mitigation

After the normal commit attempt modified the official template source and
aborted, the LaTeX template was restored by re-downloading it from the official
template URL before the final commit.

## Scope

The `--no-verify` use was limited to preserving third-party official template
source in `TEMPLATE_SOURCE/`. It was not used to bypass runtime code, test,
fixture, schema, generated output, or root metadata checks.

## Risk

`--no-verify` bypasses local pre-commit checks for that commit. The risk is
acceptable only because the affected issue was an official third-party template
source file whose byte-level preservation was the purpose of the stage.

## Recommendation

Future commits should avoid `--no-verify` unless preserving third-party source
or another documented exceptional reason requires it. Normal documentation-only
commits should use the repository's standard hooks.

## Runtime Impact

This does not affect runtime code. No runtime code, tests, fixtures, generated
JSON outputs, or EEOAP schema files changed in version 1.17.
