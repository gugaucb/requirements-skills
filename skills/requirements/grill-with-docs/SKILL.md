---
name: grill-with-docs
description: A relentless interview to sharpen a requirement, change or plan that also records the glossary, decisions and change impact as you go.
disable-model-invocation: true
---

Invoke the `grilling` skill, then the `domain-modeling` skill, and run them as one session.

Beyond what those two do:

- Persist answers as they land: terms to `GLOSSARY.md`, decisions to `DECISIONS.md` (Confirmed only when the accountable human answered).
- In change mode, persist the impact report from `impact-analysis` as `05-changes/CHG-NNN.md` and mark impacted items `Stale`.
- If `docs/agents/graph.md` exists, invoke the `graph-sync` skill after persisting.
- Create product files lazily; read `docs/agents/requirements-workflow.md` for the artifact root. If it is missing, tell the user to run `/setup-requirements-repo` and carry on with defaults.

## Preflight (Pré-condições / Insumos Obrigatórios)

Check that these exist before doing anything else:

- `docs/agents/requirements-workflow.md`
- `<artifact-root>/shared/GLOSSARY.md`
- `<artifact-root>/shared/DECISIONS.md`

If any of them is missing, **stop**. Do not invent, assume or reconstruct the missing data. Tell the user which inputs are missing and which skill produces each (`/setup-requirements-repo` for configuration, `/project-canvas` or `/create-product-vision` for the vision, `/split-backlog` for the backlog, `/spec-req` for specs, `/grill-with-docs` or `/to-questionnaire` for missing decisions); when several are missing or the way forward is unclear, tell the user to run `/wayfinder`.

## Next steps

End with `➡️ **Next step:** ...`.

- Capability or feature clear: `/spec-req`.
- Change confirmed with Stale items: `/refine-request` per impacted story.
- Product still undefined: `/create-product-vision`.
- Knowledge missing from a person outside the session: `/to-questionnaire`. Too big for one session: `/wayfinder`.
