# Failure taxonomy and exit-code contract

| Exit code | Failure class | Meaning | Example |
|---:|---|---|---|
| 0 | PASS | Pack satisfies profile and verification checks | untouched pack |
| 2 | CONTENT_OR_DIGEST_MISMATCH | Recomputed digest differs from declared digest | tampered input/output |
| 3 | INCOMPLETE_EVIDENCE | Required artifact, field or evidence link is missing | missing bundle field |
| 4 | VERSION_OR_PROFILE_MISMATCH | Pack uses unsupported profile/schema/validator version | old profile version |
| 5 | POLICY_LINKAGE_FAILURE | Operation is not linked to the declared policy | missing or mismatched policy reference |
| 6 | TEMPORAL_INCONSISTENCY | Timestamps violate allowed ordering or declared runtime interval | validation before execution |
| 7 | OUTCOME_UNVERIFIABLE | Claimed outcome cannot be linked to verifiable output evidence | output claim without digest |
| 8 | IMPLEMENTATION_COUPLING | Evidence depends on unverifiable local runtime state | local absolute path only |
| 9 | AMBIGUOUS_OPERATION | Operation semantics are too underspecified to verify | operation = "process data" |
| 10 | SIGNATURE_OR_KEY_FAILURE | Signature or public-key verification fails | wrong public key |
| 11 | REFERENCE_RESOLUTION_FAILURE | Referenced URI/artifact cannot be resolved inside the pack or declared manifest | missing input artifact |
