# Issue tracker: GitLab

Issues live in the project's GitLab Issues (`glab` CLI). Remote writes are confirmed with the user each time.

- **Publish a story**: `glab issue create`, label `ready-for-refinement`.
- **Fetch**: `glab issue view <n> --comments`.
- **Blocking edges**: GitLab linked items ("blocked by") when available, otherwise a `Blocked by` section.
- **Wayfinding**: same shape as the GitHub doc: map issue labelled `wayfinder:map`, children labelled `wayfinder:<type>`, claim by assignment, resolve by comment and close.
