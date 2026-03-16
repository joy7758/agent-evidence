# What AEP proves and what it does not prove

AEP proves four things, and it stops there unless stronger collection and anchoring layers are added.

1. AEP proves evidence bundle internal integrity.
   Canonicalization, payload digests, record hashes, the hash chain, and the bundle root hash make the bundle internally checkable offline.

2. AEP proves post-export tamper detection.
   If a record or manifest-relevant value is changed after export, `verify-bundle` rejects the bundle.

3. AEP does not currently prove strong non-repudiation.
   AEP v0.1 is not a court-grade audit system, host attestation system, or cryptographically anchored non-repudiation layer.

4. AEP strength depends on the capture boundary and anchoring model.
   The practical strength of an AEP specimen depends on where data was captured, whether external signatures were applied, whether bundles were archived remotely, and whether hashes were anchored to an external registry or ledger.
