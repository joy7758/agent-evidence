# Discussion Draft: Origin AEP v0.1

Origin AEP v0.1 is a local protocol-candidate package for representing agent execution evidence in a deterministic, reviewable form. It models a pull request or agent run through a common event surface: intent, context, action, evidence, risk, and authority.

The goal is narrow: make agent-generated software changes easier to inspect after the original runtime has ended. The package includes a small spec release kit, canonical local example, validator, reviewer pack, execution runbook, and publication gate.

This is not an official standard, not external certification, not legal compliance, not production readiness, and not a vendor integration claim. The release decision remains `PENDING_HUMAN_APPROVAL` until a human maintainer reviews the gate record.

Suggested checks:

```bash
python3 external_submission_v1/publish_gate/RELEASE_READINESS_SUMMARY.py
python3 spec_release_v0_1/validator/spec_validator.py spec_release_v0_1/examples/github_pr_example.json
make demo
```

Useful feedback should focus on the event shape, adapter boundary, local validator behavior, reviewer pack clarity, execution channel guidance, and claim boundary. Maintainers can treat this as a local reproducibility review before any public decision.
