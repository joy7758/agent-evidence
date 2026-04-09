# Reference Shortlist

## 1. Logs / Audit Trails

### [LOGS-1]

- Full title:
  Guide to Computer Security Log Management
- Author(s):
  Karen Kent; Murugiah Souppaya
- Year:
  2006
- Venue / source:
  NIST Special Publication 800-92
- DOI or stable link:
  https://doi.org/10.6028/NIST.SP.800-92
- Why it supports this paper:
  Authoritative baseline for what log management and audit-oriented logging are expected to provide in practice, which helps support the paper's claim that logging is useful but not identical to a minimal accountability object.

### [LOGS-2]

- Full title:
  Advances and Challenges in Log Analysis
- Author(s):
  Adam Oliner; Archana Ganapathi; Wei Xu
- Year:
  2012
- Venue / source:
  Communications of the ACM
- DOI or stable link:
  https://doi.org/10.1145/2076450.2076466
- Why it supports this paper:
  Widely recognized software-systems reference for the engineering role of logs in diagnosis and analysis, useful for positioning ordinary logs as an important but partial capability holder.

### [LOGS-3]

- Full title:
  Secure Audit Logs to Support Computer Forensics
- Author(s):
  Bruce Schneier; John Kelsey
- Year:
  1999
- Venue / source:
  ACM Transactions on Information and System Security
- DOI or stable link:
  https://doi.org/10.1145/317087.317089
- Why it supports this paper:
  Canonical audit-log reference showing that audit trails can be strengthened for integrity and forensics while still remaining a different object from the paper's operation-centered accountability profile.

## 2. Provenance

### [PROV-1]

- Full title:
  PROV-DM: The PROV Data Model
- Author(s):
  Luc Moreau; Paolo Missier (eds.)
- Year:
  2013
- Venue / source:
  W3C Recommendation
- DOI or stable link:
  https://www.w3.org/TR/prov-dm/
- Why it supports this paper:
  Primary standard reference for provenance representation and interchange, directly relevant to the paper's claim that provenance is a necessary component but not the whole accountability statement.

### [PROV-2]

- Full title:
  A Survey of Data Provenance in e-Science
- Author(s):
  Yogesh L. Simmhan; Beth Plale; Dennis Gannon
- Year:
  2005
- Venue / source:
  ACM SIGMOD Record
- DOI or stable link:
  https://doi.org/10.1145/1084805.1084812
- Why it supports this paper:
  Foundational survey that frames provenance around why, what, how, and dissemination concerns, useful for distinguishing provenance coverage from the paper's added policy/evidence/validation binding.

### [PROV-3]

- Full title:
  A Survey on Provenance: What for? What form? What from?
- Author(s):
  Melanie Herschel; Ralf Diestelkämper; Houssem Ben Lahmar
- Year:
  2017
- Venue / source:
  The VLDB Journal
- DOI or stable link:
  https://doi.org/10.1007/s00778-017-0486-1
- Why it supports this paper:
  Later survey that helps anchor the paper's provenance discussion in a mature literature without broadening the manuscript into a provenance survey.

## 3. Policy / Governance Constraints

### [POLICY-1]

- Full title:
  ODRL Information Model 2.2
- Author(s):
  Renato Iannella; Serena Villata
- Year:
  2018
- Venue / source:
  W3C Recommendation
- DOI or stable link:
  https://www.w3.org/TR/odrl-model/
- Why it supports this paper:
  Primary policy-expression standard that supports the paper's claim that policy can be represented explicitly, while also showing that policy expression alone is not the same as executed-operation accountability.

### [POLICY-2]

- Full title:
  eXtensible Access Control Markup Language (XACML) Version 3.0 Plus Errata 01
- Author(s):
  Erik Rissanen (ed.)
- Year:
  2017
- Venue / source:
  OASIS Standard
- DOI or stable link:
  https://docs.oasis-open.org/xacml/3.0/xacml-3.0-core-spec-en.pdf
- Why it supports this paper:
  Authoritative policy and authorization standard that helps support the paper's policy-oriented comparison without requiring the paper to argue against policy systems in general.

### [POLICY-3]

- Full title:
  Guide to Attribute Based Access Control (ABAC) Definition and Considerations
- Author(s):
  Vincent C. Hu; David Ferraiolo; Richard Kuhn; Adam Schnitzer; Kenneth Sandlin; Robert Miller; Karen Scarfone
- Year:
  2014
- Venue / source:
  NIST Special Publication 800-162
- DOI or stable link:
  https://doi.org/10.6028/NIST.SP.800-162
- Why it supports this paper:
  Authoritative access-control reference for constraint and policy basis, useful for supporting the paper's claim that policy and authorization models are important but not sufficient to establish one concrete accountable operation statement.

## 4. Profile / Conformance / Validation

### [VALIDATION-1]

- Full title:
  The Profiles Vocabulary
- Author(s):
  Rob Atkinson; Nicholas J. Car
- Year:
  2019
- Venue / source:
  W3C Working Group Note
- DOI or stable link:
  https://www.w3.org/TR/dx-prof/
- Why it supports this paper:
  Directly relevant profile reference for describing a profile together with related resources such as schemas, guidance, and validation artifacts.

### [VALIDATION-2]

- Full title:
  Shapes Constraint Language (SHACL)
- Author(s):
  Holger Knublauch; Dimitris Kontokostas
- Year:
  2017
- Venue / source:
  W3C Recommendation
- DOI or stable link:
  https://www.w3.org/TR/shacl/
- Why it supports this paper:
  Strong validation-oriented standard reference for the idea that profile-like data models often need explicit constraint checking beyond generic serialization.

### [VALIDATION-3]

- Full title:
  JSON Schema: A Media Type for Describing JSON Documents
- Author(s):
  Austin Wright; Henry Andrews; Ben Hutton; Greg Dennis
- Year:
  2022
- Venue / source:
  JSON Schema Draft 2020-12 / Internet-Draft
- DOI or stable link:
  https://json-schema.org/draft/2020-12/json-schema-core.html
- Why it supports this paper:
  Useful baseline for the paper's schema layer, especially when the manuscript distinguishes structural schema checking from profile-aware validation.

### [VALIDATION-4]

- Full title:
  JSON Schema Validation: A Vocabulary for Structural Validation of JSON
- Author(s):
  Austin Wright; Henry Andrews; Ben Hutton
- Year:
  2022
- Venue / source:
  JSON Schema Draft 2020-12 / Internet-Draft
- DOI or stable link:
  https://json-schema.org/draft/2020-12/json-schema-validation
- Why it supports this paper:
  Direct support for the claim that schema-based structural validation is a baseline, not the whole method, because the paper adds closure, cross-field consistency, and profile-specific checks on top.
