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

## Source metadata verification

Source metadata was verified from the Zenodo record API and the DataCite DOI API.

- Zenodo API: `https://zenodo.org/api/records/826906`
- DataCite API: `https://api.datacite.org/dois/10.5281/zenodo.826906`
- License status: `verified`
- License id: `cc-by-4.0`
- License title: `Creative Commons Attribution 4.0`
- License URL: `https://creativecommons.org/licenses/by/4.0`
- License source: `Zenodo API / DataCite API`

The six FASTQ MD5 values were checked against Zenodo API file metadata. Local SHA-256 values are recorded in the pack.

The GTN tutorial content license is not treated as the data-file license.

## Remaining work

- archive the generated evidence pack with DOI;
- maintain the cross-environment verification matrix;
- publish an immutable OCI image digest before submission.
