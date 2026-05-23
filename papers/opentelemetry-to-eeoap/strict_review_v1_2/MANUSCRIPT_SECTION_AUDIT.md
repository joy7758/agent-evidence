# Manuscript Section Audit

| Section | What works | What is weak | What must be changed before submission | Severity |
|---|---|---|---|---|
| Abstract | States problem, method, evidence, and non-claims. | May over-signal journal maturity relative to evidence. | Adjust for selected route and avoid broad title implications. | major |
| Introduction | Clear gap and four contributions. | Novelty beyond EEOAP/AEP still needs sharper defense. | Add sharper "not EEOAP, not AEP" positioning if journal route continues. | major |
| Problem | Good distinction between telemetry and evidence. | Conceptual, with limited external support. | Add stronger related-work support for evidence portability. | minor |
| Background | Useful OpenTelemetry and EEOAP context. | OpenTelemetry semantic conventions are evolving; EEOAP/AEP citations are local. | Resolve artifact references and version OpenTelemetry claims. | blocker |
| Method | Clear mapping pipeline and checks. | Not formalized enough for a methods journal claim. | Add algorithm sketch or failure taxonomy for JSS/IST route. | major |
| Adapter Implementation | Concrete and reproducible. | May read as implementation notes. | For SoftwareX, add software metadata; for journal, compress implementation details. | major |
| Evaluation | Tables are clear and evidence is honest. | Synthetic-only, two valid cases, no baseline. | Add real runtime fixture for JSS/IST or pivot to SoftwareX/artifact. | blocker |
| Discussion | Explains why this is more than field copying. | Still somewhat defensive rather than demonstrative. | Add baseline comparison or example showing raw telemetry cannot pass EEOAP validation. | major |
| Threats to Validity | Honest and useful. | The threats are severe enough to redirect route choice. | Keep threats but do not bury route implications. | ok |
| Related Work | Covers required placeholders. | Too thin for journal submission. | Expand if JSS/IST; keep concise for SoftwareX. | major |
| Conclusion | Bounded and accurate. | Could sound stronger than evaluation supports. | Tie final claim directly to controlled fixture scope. | minor |
| References | v0.9 improves them. | TODOs and local artifacts remain. | Finalize references and stable artifact identifiers. | blocker |
| Artifact Availability and Reproducibility Note | Identifies frozen package and generated outputs. | Not a public final artifact availability statement. | Add public archive/release/DOI before submission. | blocker |
