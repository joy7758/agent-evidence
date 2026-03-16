# Demo Runbook

## Demo order

1. Verify the canonical object
2. Run the human-readable prototype demo
3. Preview the FDO-style object example

## Exact commands

```bash
bash scripts/run_poster_demo.sh
```

## Expected outputs

### Step 1: verification

Expected line:

`VERIFY_OK`

What to say:

This confirms that the specimen object matches the schema and passes integrity
verification.

### Step 2: human-readable demo

Expected sections:

- `Loaded object`
- `Schema validation`
- `Integrity check`
- `Provenance summary`
- `FDO mapping summary`
- `Final result`

What to say:

This is the shortest human-readable explanation of what the object is, what is
verified, and how it maps toward an FDO-style shell.

### Step 3: FDO-style object preview

Expected sections:

- `object_id`
- `pid_placeholder`
- `integrity`
- `provenance`

What to say:

This shows the outer object-facing wrapper. The evidence payload stays bounded,
while the wrapper carries object identity and FDO-style reading surfaces.

## What not to explain during a short demo

- Do not explain every schema field
- Do not explain framework-specific internals
- Do not describe future registry deployment
- Do not claim formal standard adoption

Keep the demo focused on:

- bounded object
- verification
- portability
- FDO relevance
