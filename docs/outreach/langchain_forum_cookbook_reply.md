Thanks — I put together a very small local-first cookbook that stays at the callback/export boundary and does not touch LangGraph persistence internals.

- Cookbook: [GitHub cookbook link after push]
- Example: [GitHub example link after push]
- Verify: `agent-evidence verify-export --bundle examples/artifacts/langchain-minimal-evidence/langchain-evidence.bundle.json --public-key examples/artifacts/langchain-minimal-evidence/manifest-public.pem`

One boundary note: detached anchoring is still an external handoff point in this repo, not something the example verifies today.
