# Setup once per repository

The explicitly invoked `setup-requirements-repo` inspects existing project instructions, tracker choices, paths, ID policy, output language, triage labels, status policy and domain location. It proposes changes and requests confirmation before writing four project-local files: `docs/agents/{issue-tracker,requirements-workflow,domain,triage-labels}.md`. A tracker selection never permits creating remote issues or labels. Re-running setup must preserve approved settings and produce a diff of proposed changes.

[Configuration templates](../templates/setup/requirements-workflow.md) provide the four file structures for confirmed consumer-project settings.
