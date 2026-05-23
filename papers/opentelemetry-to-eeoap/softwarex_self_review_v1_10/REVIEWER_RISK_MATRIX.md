# Reviewer Risk Matrix

| Concern | Likely severity | Why it matters | Current mitigation | v1.11 action |
|---|---|---|---|---|
| Is this software useful enough? | medium | SoftwareX needs reusable research software, not only a paper example. | Adapter, fixtures, generated outputs, reports, tests. | Make user/reviewer run path clearer. |
| Is it too narrow? | medium | Only two valid traces and synthetic data may look small. | Narrow scope is explicit and reproducible. | Emphasize baseline utility and future integration path. |
| Is it actually open-source and released? | high | No package-specific public release exists yet. | Local release-candidate branch and metadata drafts exist. | Keep as blocker; do not overstate availability. |
| Does it have enough documentation? | medium | SoftwareX reviewers expect usable documentation. | Multiple docs exist under `papers/opentelemetry-to-eeoap/`. | Point more clearly to docs and commands. |
| Are tests adequate? | medium | Scope is narrow but tests must support claims. | Scoped tests cover two valid and four invalid cases. | Keep exact test scope; avoid broad claims. |
| Are examples adequate? | medium | Synthetic fixtures may seem weak. | Two valid patterns plus four controlled invalid diagnostics. | Explain why synthetic fixtures are acceptable for a minimal package. |
| Are generated artifacts appropriate to include? | low | Generated files can be viewed as clutter unless justified. | They are reproducibility evidence. | State they are expected review artifacts. |
| Is metadata inconsistent? | high | Root metadata points to AEP-Media. | v1.8 local metadata drafts separate the package. | Keep blocker visible; do not edit root metadata in v1.11. |
| Are claims too research-paper-like? | medium | SoftwareX prefers software utility and impact. | v1.9 largely reframes as software. | Replace remaining method-paper phrases. |
| Is there a real user community? | medium | SoftwareX may ask who benefits. | Draft names researchers/engineers in observability and evidence packaging. | Make target users and use cases more concrete. |
| Is there a permanent archive? | high | Formal submission needs stable availability. | None yet; TODOs are explicit. | Keep as blocker until release strategy is resolved. |
