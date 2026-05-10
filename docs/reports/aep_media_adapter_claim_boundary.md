# AEP-Media Adapter Claim Boundary

Surface | Current status | Not claimed
--- | --- | ---
LinuxPTP trace | ptp4l/phc2sys-style fixture ingestion into `aep-media-time-trace@0.1` | real PTP synchronization or hardware clock discipline
FFmpeg PRFT metadata | ffprobe-style JSON fixture ingestion and PRFT marker detection | direct MP4 box parsing or FFmpeg as a trusted oracle
C2PA manifest | C2PA-like manifest metadata ingestion with declared signature status | real C2PA signature creation or verification
strict-time bundle | adapter-generated clock trace can pass local strict-time validation | trusted timestamping or external time anchor
evaluation pack | optional adapter cases can be appended with `--include-adapters` | change to default 18-case Mission 004 claim
optional smoke demos | environment-dependent tool availability can be reported | reproducible proof that external systems were used
