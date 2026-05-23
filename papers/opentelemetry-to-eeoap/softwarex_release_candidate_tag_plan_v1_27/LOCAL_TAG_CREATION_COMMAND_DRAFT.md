# Local Tag Creation Command Draft

Purpose: draft commands for future local annotated tag creation.

Do not run these commands in version 1.27.

Use placeholders:

- `<TAG_NAME>`
- `<TARGET_COMMIT>`

## Check Whether The Tag Already Exists

```bash
git tag --list <TAG_NAME>
```

Expected for new tag creation: empty output.

## Inspect Target Commit

```bash
git show --stat --oneline --summary <TARGET_COMMIT>
git status --short
```

Expected: target commit is the selected audited commit and status is clean.

## Create Annotated Local Tag

```bash
git tag -a opentelemetry-to-eeoap-softwarex-rc-v1.0 <TARGET_COMMIT> -m "OpenTelemetry-to-EEOAP SoftwareX release candidate v1.0"
```

## Verify Tag Object

```bash
git show --no-patch --decorate --format=fuller <TAG_NAME>
git rev-parse <TAG_NAME>
git rev-parse <TAG_NAME>^{}
```

## Verify Target Commit

```bash
test "$(git rev-parse <TAG_NAME>^{})" = "$(git rev-parse <TARGET_COMMIT>)"
```

## List Tag

```bash
git tag --list <TAG_NAME>
```

## Delete Local Tag If Created Incorrectly

Caution: only delete a local tag before it is pushed, and only after confirming
that it points to the wrong target or has the wrong message.

```bash
git tag -d <TAG_NAME>
```

Do not run these commands in version 1.27.
