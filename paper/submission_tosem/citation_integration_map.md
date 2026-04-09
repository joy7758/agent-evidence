# Citation Integration Map

| claim or section in the paper | reference category needed | candidate reference(s) | integration priority |
| --- | --- | --- | --- |
| Related Work §1: ordinary logs and audit trails are useful but do not by themselves form the same minimal accountability object | logs / audit trails | [LOGS-1], [LOGS-2], [LOGS-3] | high |
| Related Work §2: provenance is necessary for linkage and derivation context, but provenance-only representations do not by themselves bind policy, evidence, and validation | provenance | [PROV-1], [PROV-2], [PROV-3] | high |
| Related Work §3: policy-oriented approaches provide rule basis and constraints, but policy-only representations do not establish one executed and independently checkable operation statement | policy / governance constraints | [POLICY-1], [POLICY-2], [POLICY-3] | high |
| Related Work §4: the paper is about a profile plus conformance path rather than unconstrained JSON exchange or schema-only checking | profile / conformance / validation | [VALIDATION-1], [VALIDATION-3], [VALIDATION-4] | high |
| Related Work §4: explicit comparison to validation-oriented standards or profile-resource descriptions | profile / conformance / validation | [VALIDATION-1], [VALIDATION-2], [VALIDATION-4] | high |
| Evaluation §1: the evaluation is framed as conformance checking, boundary coverage inspection, and diagnostic usefulness rather than a benchmark study | profile / conformance / validation | [VALIDATION-2], [VALIDATION-4] | medium |
| Evaluation §4: the retention-review comparative case treats logs, provenance-only, and policy-only as partial capability holders rather than as strawman baselines | logs / audit trails; provenance; policy / governance constraints | [LOGS-2], [PROV-1], [POLICY-1] | high |
| Discussion §5.1: the construct is intentionally narrow because the paper operationalizes accountability through one profile structure and one set of validation rules | profile / conformance / validation | [VALIDATION-1], [VALIDATION-2], [VALIDATION-4] | medium |
| Discussion §5.4: artifact validity is repository-grounded and should not be confused with broader external validity | profile / conformance / validation | [VALIDATION-1] | low |

## Priority Note

The highest-priority integration points are the four category-defining claims in Related Work plus the comparative-case paragraph in Evaluation. Those are the places where the manuscript most clearly benefits from explicit literature support without expanding into a broad survey.
