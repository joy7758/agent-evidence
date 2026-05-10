# AEP-Media Non-claims Matrix

claim_not_made | reason | future integration
--- | --- | ---
legal admissibility | local declared-demo validation cannot establish legal admissibility | legal process, chain of custody, jurisdiction-specific review
non-repudiation | no external signing or identity trust fabric in v0.1 | signing, certificate chain, external anchoring
trusted timestamping | current time trace is declared or synthetic | trusted timestamp authority, transparency log, external time anchor
real PTP synchronization | v0.1 does not run ptp4l/phc2sys or inspect hardware clock discipline | linuxptp trace ingestion
real MP4 PRFT extraction | v0.1 does not parse MP4 boxes or call FFmpeg | FFmpeg PRFT extraction adapter
real C2PA signature verification | v0.1 uses placeholder manifest references only | c2pa manifest signing and verification adapter
production deployment | examples and demos are local declared-demo fixtures | field pilot and deployment evidence
complete regulatory compliance | profile validates evidence structure, not legal sufficiency | domain-specific compliance mapping and external review
