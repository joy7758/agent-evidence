# Reviewer Objection Matrix

| Reviewer objection | Short answer | Evidence source | Manuscript already handles it? | Action needed |
|---|---|---|---|---|
| This is just an adapter script. | The contribution is the bounded adapter path, mapping model, diagnostics, validator routing, and reproducibility package. | `paper_v1_0_submission_candidate.md`, v0.9 route assessment. | Partly. | Ask pre-reviewers whether method framing is strong enough. |
| This is just field copying. | The adapter selects accountable spans, checks parent closure, resolves tool spans, preserves provenance, emits EEOAP statements, and invokes the validator. | Adapter tests, v1.0 Method and Discussion. | Yes. | Keep this paragraph prominent. |
| This duplicates EEOAP. | EEOAP defines the target evidence object and validator; this paper studies how telemetry enters it. | `reviewer_positioning.md`, v1.0 Related Work. | Yes. | Preserve distinction in abstract and introduction. |
| This duplicates AEP. | AEP concerns broader evidence bundles and packaging; this paper focuses on span-to-operation-evidence transformation. | `reviewer_positioning.md`, v1.0 Related Work. | Yes. | Stabilize AEP artifact reference before submission. |
| The evaluation is too small. | It is intentionally bounded: two valid trace contexts and four invalid diagnostics. | v0.7 evaluation update, v1.0 Evaluation. | Yes. | If reviewers require more, consider one targeted runtime fixture later. |
| Synthetic traces are not enough. | They support controlled reproducibility but do not prove production compatibility. | Threats to Validity, claim boundary files. | Yes. | Use external feedback to decide whether runtime evidence is necessary. |
| OpenTelemetry compatibility is not proven. | Correct; broad compatibility is a non-claim. The source is OpenTelemetry-style controlled fixtures. | v1.0 Background and Threats. | Yes. | Keep wording precise. |
| Why not modify the EEOAP schema? | Schema reuse is the point: the adapter proves entry into the existing validator path. | v1.0 Discussion; reviewer positioning. | Yes. | No action unless reviewers demand a schema extension, which would change the paper. |
| Why no real LangChain runtime? | Runtime integration is deferred to keep the current claim narrow and reproducible. | v1.0 Threats; v0.6 gap analysis. | Yes. | Consider only if external reviewers require it for journal route. |
| Why is this a software engineering contribution? | It studies an interface between telemetry, transformation logic, evidence objects, and validation. | v1.0 Discussion and Evaluation. | Partly. | Strengthen venue-specific framing after route decision. |
| Where is the artifact availability? | Frozen package, generated outputs, clean-clone note, and checksums exist; final public archive is still pending. | `frozen_v0_5/`, v1.0 Artifact Availability note. | Yes. | Create public archive/DOI or immutable tag before submission. |
| Are references stable? | Official sources are mostly verified, but EEOAP/AEP local artifact references require stable identifiers. | v0.9 citation verification. | Yes. | Resolve artifact references before submission. |
