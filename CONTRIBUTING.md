# Contributing

Read `AGENTS.md` and `docs/AUTHORING-SKILLS.md`. A change clears the bar when it describes an observed failure in a real session and does not compose from existing skills.

When you add, rename, remove or re-route a skill: update `skills/*/README.md`, `ask-req`, the README catalog and flow, `docs/FLOW.md`, `docs/DE-PARA.md`, the evaluations and the CHANGELOG, then run `python3 scripts/sync_adapters.py` (generates `agents/agent.yaml` and `agents/openai.yaml`) and the validation commands. Never put confidential PO data in examples. Contributions are covered by MIT.
