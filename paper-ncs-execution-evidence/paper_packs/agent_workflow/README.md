# Agent/tool-use workflow evidence pack

This is the secondary generalization experiment.

## Purpose

Show that the same operation-evidence boundary applies to tool-using agent workflows, without making agent evidence the main contribution of the NCS paper.

## Required properties

- fixed prompts or fixtures;
- deterministic tool responses, preferably mocked;
- no private API dependency for reviewer verification;
- bundle/receipt/summary output;
- failure injection for tampered tool result, missing policy, broken evidence link and signature/key mismatch.

## Boundary

Do not reuse the AEP live-chain manuscript as the main result. This pack should be a compact generalization case for the NCS manuscript.
