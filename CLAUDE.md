# Claude Code routing

Follow AGENTS.md. Claude adapters under `.claude/skills/` point to corresponding canonical skill definitions in `.agents/skills/`. User can invoke `/setup-requirements-repo` and `/create-product-vision`. The `disable-model-invocation: true` metadata prevents automatic Claude invocation for these two. Other skills activate by relevance or explicit slash name.
