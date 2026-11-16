---
name: setup-requirements-repo
description: Configure this repo for the requirements skills (artifact root, issue tracker, output language, ID and status policy, triage labels, domain doc layout). Run once per repo before the other requirements skills.
disable-model-invocation: true
---

# Setup Requirements Repo

Scaffold the per-repo configuration the requirements skills assume. This is a prompt-driven skill, not a script: explore, present, confirm, then write.

## Process

### 1. Explore

Read what exists; assume nothing:

- `git remote -v`: which tracker host, if any?
- `CLAUDE.md`, `AGENTS.md`, `GEMINI.md` at the root, and any existing `## Agent skills` block.
- `GLOSSARY.md`, `GLOSSARY-MAP.md`, `DECISIONS.md`, `PRODUCT-VISION.md`, `artifacts/`, `.scratch/`.
- `docs/agents/`: a previous run of this skill.
- Is the `triage` skill installed? (decides Section D.)
- Monorepo signals (workspaces, several products): decides Section E.

### 2. Present findings and ask

Summarise what is present and missing. Take the sections in order, one answer each. Lead with the recommended answer so it can be accepted in a word; skip a section the exploration already settled.

**A. Artifact root and output language.** Recommend `artifacts/<product>/`. Ask the language of written artifacts (Gherkin keywords follow it, e.g. pt-BR). Conversation follows the user's own language.

**B. Issue tracker.** Where stories and wayfinder maps are published: **local Markdown** (default, no remote), **GitHub**, **GitLab**, or **other** (user describes it in a paragraph). Selecting a tracker never authorizes remote writes; each publish is confirmed.

**C. ID and status policy.** IDs product-wide and immutable. Story statuses default: Draft, Stale, Blocked, Needs changes, Ready for human review, Ready (team agreement), Retired. Ask whether the team has a Definition of Ready; record it as a team agreement, never infer one.

**D. Triage roles** (only if `triage` is installed). One question: keep the defaults (`needs-triage`, `needs-info`, `ready-for-refinement`, `ready-for-po`, `out-of-scope`)? On no, collect label overrides.

**E. Domain docs.** Default single context (`GLOSSARY.md`, `DECISIONS.md` at the product root). Offer multi-context (`GLOSSARY-MAP.md`) only on monorepo signals.

### 3. Confirm and edit

Show a draft of the `## Agent skills` block and of each `docs/agents/*.md`. Let the user edit before anything is written.

### 4. Write

Pick the file to edit: `CLAUDE.md` if it exists, else `AGENTS.md`, else `GEMINI.md`; if none exists, ask which to create. Never create a second one. Update an existing `## Agent skills` block in place.

```markdown
## Agent skills

### Requirements workflow
Artifact root, language, ID and status policy. See `docs/agents/requirements-workflow.md`. Shared process vocabulary: `docs/agents/requirements-vocabulary.md`.

### Issue tracker
[one line]. See `docs/agents/issue-tracker.md`.

### Triage roles
[one line]. See `docs/agents/triage-labels.md`.

### Domain docs
[single-context or multi-context]. See `docs/agents/domain.md`.
```

Write the files from the seeds in this folder: [requirements-workflow.md](requirements-workflow.md), [requirements-vocabulary.md](requirements-vocabulary.md), [issue-tracker-local.md](issue-tracker-local.md), [issue-tracker-github.md](issue-tracker-github.md), [issue-tracker-gitlab.md](issue-tracker-gitlab.md), [triage-labels.md](triage-labels.md), [domain.md](domain.md). For "other" trackers, write `issue-tracker.md` from the user's description. Create product folders and files **lazily**; the skill that first needs one creates it. Re-runs preserve confirmed settings and show a diff of proposed changes.

### 5. Done

Say what was written. Mention that `docs/agents/*.md` can be edited by hand and that re-running is only for switching trackers or restarting.

## Next steps

End with `➡️ **Next step:** ...`.

- New product or vague idea: `/grill-with-docs`, then `/create-product-vision`.
- Product narrative or brief in hand: `/create-product-vision`.
- Raw requests waiting: `/triage`.
- Unsure: `/ask-req`.
