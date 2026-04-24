# Public scientific dataset note

## Dataset selection

The manuscript-facing pack uses Zenodo DOI `10.5281/zenodo.826906`, a Galaxy Training Network small RNA-seq tutorial dataset containing downsampled Drosophila small RNA-seq FASTQ files.

This dataset was selected because it has:

- a public DOI;
- small files suitable for reviewer execution;
- real FASTQ data;
- a non-human Drosophila context;
- downsampled source data;
- a deterministic QC workflow surface.

## What the workflow proves

The workflow does not prove biological correctness or make a biological discovery claim.

It tests:

- verifiable execution evidence;
- input and output digest stability;
- deterministic receipt and summary linkage;
- failure detection for tampered inputs, tampered outputs, missing policy, broken evidence links, profile mismatch, temporal inconsistency and unverifiable outcomes.

## Remaining work

- verify source license before final submission;
- archive the generated evidence pack with DOI;
- run the cross-environment verification matrix.
