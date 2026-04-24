# Independent checker protocol

## Purpose

The independent checker protocol compares the repository strict validator with a separate paper-local checker over the same public scientific workflow pack and failure cases.

The goal is not to prove biological correctness. The goal is to show that failure detection is consistent across independently executed checking paths for the NCS execution-evidence boundary.

## Checkers

| Checker | Command | Role |
|---|---|---|
| Repository validator | `.venv/bin/agent-evidence validate-pack --pack <pack> --strict` | Manuscript-facing strict validator |
| Independent checker | `python paper-ncs-execution-evidence/scripts/independent_check_ncs_pack.py --pack <pack> --strict` | Separate checker for agreement testing |

The independent checker must not import `agent_evidence` and must not call `agent-evidence`.

## Agreement Rule

A case agrees only if all are true:

1. the expected exit code matches the repository validator exit code;
2. the expected exit code matches the independent checker exit code;
3. the independent checker reports the expected failure class.

## Failure Classes

| Exit code | Failure class | Checker description |
|---:|---|---|
| 0 | PASS | Pack satisfies profile and verification checks |
| 2 | CONTENT_OR_DIGEST_MISMATCH | Recomputed artifact or receipt digest differs from the declared digest |
| 3 | INCOMPLETE_EVIDENCE | Required pack object or field is missing |
| 4 | VERSION_OR_PROFILE_MISMATCH | Pack declares an unsupported profile version |
| 5 | POLICY_LINKAGE_FAILURE | Policy reference, policy file or policy digest linkage is broken |
| 6 | TEMPORAL_INCONSISTENCY | Execution and validation timestamps violate required ordering |
| 7 | OUTCOME_UNVERIFIABLE | Claimed outcome cannot be linked to digest-backed primary output evidence |
| 8 | IMPLEMENTATION_COUPLING | Artifact reference depends on absolute or pack-external local state |
| 9 | AMBIGUOUS_OPERATION | Operation semantics are absent or too underspecified |
| 10 | SIGNATURE_OR_KEY_FAILURE | Signature or key verification fails |
| 11 | REFERENCE_RESOLUTION_FAILURE | Referenced evidence artifact cannot be resolved inside the pack |

## Public Pack Cases

| Case | Expected failure class | Expected exit code | Failure description |
|---|---|---:|---|
| `scientific_workflow_public` | PASS | 0 | untouched public Drosophila small RNA-seq QC pack |
| `failures/tampered_input` | CONTENT_OR_DIGEST_MISMATCH | 2 | one input FASTQ gzip file is modified after receipt generation |
| `failures/tampered_output` | CONTENT_OR_DIGEST_MISMATCH | 2 | `outputs/qc_metrics.json` is modified after receipt generation |
| `failures/missing_policy` | POLICY_LINKAGE_FAILURE | 5 | `policy.json` is removed |
| `failures/broken_evidence_link` | REFERENCE_RESOLUTION_FAILURE | 11 | an evidence reference points to a missing workflow script |
| `failures/version_mismatch` | VERSION_OR_PROFILE_MISMATCH | 4 | bundle profile version is changed to `ncs-v0-broken` |
| `failures/temporal_inconsistency` | TEMPORAL_INCONSISTENCY | 6 | validation time is earlier than execution start |
| `failures/outcome_unverifiable` | OUTCOME_UNVERIFIABLE | 7 | primary output digest is removed while retaining outcome claims |

## Run Command

```bash
bash paper-ncs-execution-evidence/scripts/run_independent_checker_agreement.sh \
  paper-ncs-execution-evidence/paper_packs/scientific_workflow_public
```

## Outputs

The runner writes:

- `paper-ncs-execution-evidence/paper_packs/scientific_workflow_public/independent_checker_agreement.json`
- `paper-ncs-execution-evidence/paper_packs/scientific_workflow_public/independent_checker_agreement.md`
