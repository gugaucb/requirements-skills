---
name: wayfinder
description: Plan a huge, foggy requirements effort (more than one session can hold) as a shared map of decision tickets, and resolve them one at a time until the way to the destination is clear.
disable-model-invocation: true
---

A loose idea has arrived, too big for one session and wrapped in fog: a whole product, a new business line, a regulation to absorb. The way from here to the **destination** is not visible yet. This skill charts the way as a **shared map**, then works its **decision tickets** (questions whose resolution is a decision, not slices of a build) one at a time until the route is clear.

Where grilling sharpens an idea you can hold in one session, wayfinder is for the idea you cannot. It is slower and denser: never use it on a well-scoped story.

## Plan, don't specify

The map produces **decisions, not deliverables**. It is done when nothing is left to decide before someone writes the vision or spec. The pull to just write the stories is the signal you reached the edge of the map: hand off.

## Refer by name

Every map and ticket has a title. In everything the human reads, refer to it by that name, never by a bare number. The id or link rides inside the name.

## The map

One map per effort, the canonical artifact. It is an **index**: it gists decisions and links the tickets that hold the detail. A decision lives in exactly one place, its ticket.

```markdown
## Destination
<what reaching the end looks like: a PRODUCT-VISION draft, a SPEC, a locked decision. One or two lines.>

## Notes
<domain, skills every session should use, standing preferences>

## Decisions so far
- [<closed ticket title>](link) (DEC-NNN): <one-line gist>

## Not yet specified
<in-scope fog you cannot ticket yet; graduates as the frontier advances>

## Out of scope
<work ruled beyond the destination; closed, never graduates>
```

Where the map, tickets, blocking and frontier physically live depends on the tracker: read the "Wayfinding operations" section of `docs/agents/issue-tracker.md`. If missing, tell the user to run `/setup-requirements-repo`; meanwhile default to local Markdown.

## Tickets

Each ticket is a child of the map; its body is the question, sized to one session:

```markdown
## Question
<the decision or investigation this ticket resolves>
```

It carries a type, and only `wayfinder:` labels (never triage labels). A session **claims** a ticket first, before any work. Blocking uses the tracker's native dependency; a ticket is **unblocked** when its blockers are closed; the **frontier** is the open, unblocked, unclaimed tickets.

**HITL** tickets resolve only through a live exchange with a human who speaks for themselves; the agent never answers for them.

| Type | Mode | Use when | Resolved by |
| --- | --- | --- | --- |
| `research` | AFK | A fact outside the repo is needed (law, contract, existing system) | A sub-agent with a fresh context invokes the `research` skill |
| `sketch` | HITL | "How should it behave or read" is the question | A cheap concrete artifact to react to: example scenarios, a Mermaid flow, a sample report or message |
| `grilling` | HITL | The default: a decision for the PO | Invoke the `grilling` skill and the `domain-modeling` skill |
| `ask` | HITL | The answer sits with someone not in the session | Draft the questions; the user may run `/to-questionnaire` to send them; resolve when answers are pasted back |
| `task` | HITL or AFK | Manual work must precede a decision (get access, gather samples) | Do it, or hand the human a precise checklist; record resulting facts |

## Fog of war

The map is deliberately incomplete. Beyond the live tickets lies the **fog**: decisions you can see coming but cannot pin down. Resolving a ticket clears the fog ahead of it, graduating what is now specifiable into new tickets.

**Fog or ticket?** The test is whether you can state the question precisely now, not whether you can answer it. Sharp but blocked: ticket. Not yet sharp: **Not yet specified**. Do not pre-slice fog.

Work beyond the destination is **out of scope**, not fog. Close such a ticket, leave one line with the reason in **Out of scope**, and keep it out of **Decisions so far**.

## Invocation

Never resolve more than one ticket per session, except `research` tickets.

### Chart the map

The user arrives with a loose idea.

1. **Name the destination.** Invoke `grilling` and `domain-modeling` to pin down what the map finds its way to. Scope is fixed here.
2. **Map the frontier.** Grill again, breadth first: fan out across the whole space. If no fog appears (the way is clear, the journey fits one session), skip the map and tell the user to run `/grill-with-docs` or `/create-product-vision`.
3. **Create the map** with Destination and Notes filled, Decisions so far empty, fog sketched.
4. **Create the specifiable tickets**, then wire blocking edges in a **second pass** (ids exist first; use real ids in cross-references).
5. **Fire research tickets** in parallel, each in a sub-agent with a fresh context window; capture findings under `research/` with a pointer from the ticket.
6. Stop. Charting is one session's work and resolves nothing by hand.

### Work through the map

The user gives a map (path or link); a ticket is optional.

1. Load the map (low resolution, not every ticket body).
2. Pick the ticket (the named one, else the first frontier ticket). **Claim it.**
3. Resolve it as its type. Zoom into related tickets on demand.
4. **Record**: post the answer as a resolution, close the ticket, add a DEC row in `DECISIONS.md` that points at the ticket (Confirmed only if the accountable human answered), and append the gist to Decisions so far.
5. Add newly surfaced tickets (create, then wire). Graduate specifiable fog. Rule out-of-scope items out. Update or delete tickets the decision invalidated.

Others may run unblocked tickets in parallel, so expect concurrent edits.

## Next steps

When the map is clear it **hands off, it does not specify**. End with `➡️ **Next step:** ...`.

- Destination was a vision: `/create-product-vision`, collapsing the map's linked decisions.
- Destination was a feature or capability: `/to-spec`, then `/split-backlog`.
- Effort turned out small: `/refine-request`.
