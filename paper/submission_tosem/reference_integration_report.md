# Reference Integration Report

## Integrated into the Manuscript

- `kent2006sp80092`
- `oliner2012loganalysis`
- `moreau2013provdm`
- `herschel2017surveyprovenance`
- `iannella2018odrl`
- `hu2014abac`
- `atkinson2019profiles`
- `knublauch2017shacl`
- `wright2022jsonschema`
- `wright2022jsonschemavalidation`

## Shortlisted but Not Yet Used

- `schneier1999secureauditlogs`
  Reason: useful audit-trail depth reference, but not necessary for the current low-density related-work integration.
- `simmhan2005provenance`
  Reason: foundational provenance survey retained in the shortlist, but the current manuscript already has one standard provenance reference plus one mature survey.
- `rissanen2017xacml`
  Reason: useful authorization-standard reference, but the current manuscript keeps the policy category intentionally narrow and avoids overloading the policy subsection.

## Sentences Softened During Integration

- In `paper/tosem_en/06_related_work.md`, the policy subsection was tightened from a broad policy-only limitation claim to a narrower structural claim:
  `In the setting studied here, a policy-oriented representation therefore does not by itself establish a minimal executed operation-accountability object, because policy, provenance, evidence, and validation remain unbound.`
- In `paper/tosem_en/05_evaluation.md`, the comparative-case policy sentence was tightened to:
  `Policy-oriented representations can describe the governing rule basis [@iannella2018odrl], but in the setting studied here they do not by themselves establish a minimal executed operation-accountability object because policy, provenance, evidence, and validation remain unbound.`

## Policy / Governance Category Assessment

Yes. The policy / governance category is now handled more safely. The citations support the importance of policy constraints and policy-expression formalisms, while the manuscript keeps the stronger limitation claim as this paper's own structural argument rather than attributing that conclusion directly to prior literature.
