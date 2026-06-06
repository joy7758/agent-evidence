# EEOAP Evidence Gate Skill

This directory contains a repo-local agent skill for applying the existing EEOAP evidence gate during coding-agent work.

The skill does not introduce new protocol clauses. It only points agents to the existing EEOAP profile, clause index, validator command, PR guidance, and claim-scope boundaries.

Primary file:

- SKILL.md

This skill is advisory for agent workflow routing. The enforceable checks remain:

- scripts/check_protocol_citations.py
- agent-evidence validate-profile examples/minimal-valid-evidence.json
- GitHub Actions required checks on main
