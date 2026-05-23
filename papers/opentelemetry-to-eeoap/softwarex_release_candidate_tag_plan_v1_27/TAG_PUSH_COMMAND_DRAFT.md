# Tag Push Command Draft

Purpose: draft commands for future tag push without executing them.

Do not run these commands in version 1.27.

Use placeholders:

- `<REMOTE>`
- `<TAG_NAME>`

## Verify Remote

```bash
git remote -v
```

Confirm the intended remote explicitly before pushing.

## Push One Tag Only

```bash
git push <REMOTE> <TAG_NAME>
```

Do not use commands that push all tags.

## Verify Remote Tag

```bash
git ls-remote --tags <REMOTE> <TAG_NAME>
```

## Avoid Accidental All-Tag Push

Do not run:

```bash
git push --tags
```

## Rollback Caution

If a tag is pushed incorrectly, deleting or moving a public tag can confuse
reviewers, release archives, and DOI workflows. Treat pushed tags as public
release evidence. Do not push until release scope, metadata, support package,
and author approval are final for the RC push.
