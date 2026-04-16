# Review Pack Minimal

## 1) What this path does

This cookbook exposes the current Review Pack as one thin packaging layer above
an existing:

- `bundle`
- `receipt`
- `summary`

It does not create a new canonical artifact type. It packages those existing
artifacts into one stable review directory and renders `review/report.md`.

## 2) What stays primary vs supporting

Primary pack contents remain:

- `bundle`
- `receipt`
- `summary`

Supporting files remain optional:

- manifest sidecar
- verification public key
- runtime JSONL capture
- local private key

The private key is excluded by default.

## 3) Required inputs

The builder takes existing artifact paths as inputs:

- `bundle_path`
- `receipt_path`
- `summary_path`

Optional supporting inputs:

- `manifest_path`
- `public_key_path`
- `runtime_events_path`
- `private_key_path`

Supporting files are copied only when you pass them in. Failure taxonomy and
reviewer-facing labels stay in `review/report.md` only.

## 4) Example script

The thin developer-facing entry path is:

```python
from agent_evidence.review_pack import ReviewPackAssembler

assembler = ReviewPackAssembler.for_output_dir("./artifacts/review-pack")
pack = assembler.assemble(
    bundle_path="./artifacts/run/langchain-evidence.bundle.json",
    receipt_path="./artifacts/run/receipt.json",
    summary_path="./artifacts/run/summary.json",
    supporting_files={
        "manifest": "./artifacts/run/langchain-evidence.manifest.json",
        "public_key": "./artifacts/run/manifest-public.pem",
        "runtime_events": "./artifacts/run/runtime-events.jsonl",
    },
)
```

The example wrapper script lives at:

```bash
python examples/review_pack/build_review_pack.py ...
```

## 5) Run it on an existing artifact set

From the repository root:

```bash
python examples/review_pack/build_review_pack.py \
  --bundle-path ./examples/artifacts/langchain-minimal-evidence/langchain-evidence.bundle.json \
  --receipt-path ./examples/artifacts/langchain-minimal-evidence/receipt.json \
  --summary-path ./examples/artifacts/langchain-minimal-evidence/summary.json \
  --manifest-path ./examples/artifacts/langchain-minimal-evidence/langchain-evidence.manifest.json \
  --public-key-path ./examples/artifacts/langchain-minimal-evidence/manifest-public.pem \
  --runtime-events-path ./examples/artifacts/langchain-minimal-evidence/runtime-events.jsonl \
  --output-dir ./examples/artifacts/review-pack
```

If you want to include the private key for a local-only workflow, you must pass
both of these:

```bash
  --private-key-path ./examples/artifacts/langchain-minimal-evidence/manifest-private.pem \
  --include-private-key
```

Without `--include-private-key`, the pack keeps that file out by default.

## 6) Output layout

The assembled pack keeps a stable layout:

```text
review-pack/
├── index.json
├── primary/
│   ├── bundle.json
│   ├── receipt.json
│   └── summary.json
├── review/
│   └── report.md
└── supporting/
    └── optional supporting files
```

`index.json` is only a pack index. It is not a fourth canonical artifact.

## 7) Boundaries

- no CLI changes
- no schema changes
- no `README.md` or `docs/quickstart.md` changes
- no hosted delivery work
- no cross-repo work
- no back-propagation of renderer labels into canonical schema
