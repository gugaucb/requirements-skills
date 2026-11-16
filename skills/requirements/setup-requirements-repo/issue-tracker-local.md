# Issue tracker: local Markdown

Stories, specs and wayfinder maps live as files under the artifact root. No remote.

## Conventions

- Stories: `<artifact-root>/stories/US-NNN.md`; backlog index: `BACKLOG.md`.
- Triage state is a `Status:` line near the top of each incoming request file in `<artifact-root>/requests/NN-slug.md`; comments append under `## Comments`.

## When a skill says "publish to the issue tracker"

Write or update the file under the artifact root.

## Wayfinding operations

Used by `/wayfinder`. The **map** is a file with one **child** file per ticket.

- **Map**: `<artifact-root>/wayfinder/<effort>/map.md` (Destination, Notes, Decisions so far, Not yet specified, Out of scope).
- **Child ticket**: `<artifact-root>/wayfinder/<effort>/NN-slug.md`, numbered from `01`. Lines: `Type:` (research, sketch, grilling, ask, task), `Status:` (open, claimed, resolved), `Blocked by: NN, NN`.
- **Frontier**: tickets that are open, unclaimed and whose blockers are all resolved; lowest number first.
- **Claim**: set `Status: claimed` and save before any work.
- **Resolve**: append the answer under `## Answer`, set `Status: resolved`, then add the gist and a link to the map's Decisions so far.
