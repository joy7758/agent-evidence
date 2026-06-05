# OpenAI Agents Integration

This example integration captures a minimal OpenAI Agents runtime trace and
exports a JSON runtime evidence export.

Use it as a narrow exporter example for `agent-evidence`, not as a new platform
surface. The current canonical callable surface remains the local
`agent-evidence` CLI.

Run:

```bash
python integrations/openai-agents/export_evidence.py
```

For the provider-agnostic OpenAI-compatible 5-minute path, start with:

```text
docs/cookbooks/openai_compatible_minimal_evidence.md
```

That path defaults to mock/offline behavior and keeps provider configuration
limited to `api_key`, `base_url`, and `model`.
