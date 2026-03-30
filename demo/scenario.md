# Scenario

## Name

Metadata enrichment for one client note object.

## Goal

Show one minimal closed loop where an agent transforms one input object into one
derived output object under an explicit metadata policy, emits evidence, and
gets independently validated.

## Policy Boundary

- Only approved metadata fields may be added.
- The note body must remain unchanged.

## Chosen Operation

`metadata.enrich`

The operation reads one client note, adds reviewed metadata tags, and emits one
derived note object plus one operation log artifact.

## Expected Outputs

- `input-object.json`
- `derived-object.json`
- `operation-log.json`
- `minimal-profile-evidence.json`
- `validation-report.json`
