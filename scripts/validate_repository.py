#!/usr/bin/env python3
"""Static contract checks for the skills repository. Exit 1 on any problem."""
import re
import sys
from pathlib import Path

R = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(R / "scripts"))
from sync_adapters import frontmatter, render  # noqa: E402

NAME = r"[a-z][a-z0-9-]+"


def skills():
    out = {}
    for f in sorted((R / "skills").glob("*/*/SKILL.md")):
        if f.parent.parent.name == "deprecated":
            continue
        text = f.read_text(encoding="utf-8", errors="replace")
        out[f.parent.name] = (f, text, frontmatter(text))
    return out


def next_steps(text):
    m = re.search(r"^## Next steps\n(.*)\Z", text, re.S | re.M)
    return m.group(1) if m else None


def check():
    p = []
    S = skills()
    manual = {n for n, (_, _, fm) in S.items() if fm.get("disable-model-invocation") == "true"}
    model = set(S) - manual
    if len(S) != 32:
        p.append(f"Expected 32 skills, found {len(S)}")
    for n, (f, t, fm) in S.items():
        if fm.get("name") != n:
            p.append(f"{n}: frontmatter name mismatch")
        if len(fm.get("description", "")) < 20:
            p.append(f"{n}: missing description")
        if n in model and not re.search(r"\b(use when|when)\b", fm.get("description", ""), re.I):
            p.append(f"{n}: model-invoked description needs 'Use when' triggers")
        if n in manual and re.search(r"use when", fm.get("description", ""), re.I):
            p.append(f"{n}: user-invoked description must be human-facing (no trigger list)")
        y = f.parent / "agents" / "openai.yaml"
        if not y.exists() or y.read_text(encoding="utf-8", errors="replace") != render(f.parent):
            p.append(f"{n}: agents/openai.yaml missing or out of sync")
        ns = next_steps(t)
        if ns is None:
            p.append(f"{n}: missing '## Next steps'")
        elif not re.search(r"`/?" + NAME + r"`", ns):
            p.append(f"{n}: Next steps names no skill")
        for target in re.findall(r"[Ii]nvoke (?:the )?`(" + NAME + r")`", t):
            if target not in S:
                p.append(f"{n}: invokes unknown skill {target}")
            elif target in manual:
                p.append(f"{n}: invokes user-invoked skill {target} (must suggest instead)")
        for target in re.findall(r"`/(" + NAME + r")`", t):
            if target not in S and target not in ("tmp",):
                p.append(f"{n}: references unknown /{target}")
            elif target in model:
                p.append(f"{n}: /{target} is model-invoked; use 'invoke the `{target}` skill'")
    for n in ("project-canvas", "create-product-vision", "split-backlog", "spec-req", "apply-spec", "review-spec", "refine-request"):
        t = S[n][1]
        for key in ("**Reads:**", "**Writes:**", "**Gate:**"):
            if key not in t:
                p.append(f"{n}: Contract section lacks {key}")
        if "## Contract" not in t:
            p.append(f"{n}: missing '## Contract'")
    flow = (R / "docs/FLOW.md").read_text(encoding="utf-8", errors="replace")
    for n in ("project-canvas", "create-product-vision", "split-backlog", "spec-req", "apply-spec", "review-spec"):
        if f"/{n}" not in flow:
            p.append(f"docs/FLOW.md does not show /{n}")
    allowed_paths = re.compile(r"^(docs/agents/[\w.-]+\.md|<artifact-root>/(00-canvas|01-vision|02-backlog|03-specs|04-stories|05-changes|shared|inputs)/[\w<>./-]+)$")
    pre_head = "## Preflight (Pré-condições / Insumos Obrigatórios)"
    stop_rule = "**stop**. Do not invent, assume or reconstruct the missing data."
    for n, (f, t, fm) in S.items():
        if pre_head not in t:
            p.append(f"{n}: missing '{pre_head}'")
            continue
        body = t.split(pre_head, 1)[1].split("\n## ", 1)[0]
        first_h2 = t.find("\n## ")
        if t.index(pre_head) != first_h2 + 1:
            p.append(f"{n}: Preflight must be the first section")
        bullets = [x[2:].strip() for x in body.split("If any of them")[0].splitlines() if x.startswith("- ")]
        if bullets and (stop_rule not in body or "/wayfinder" not in body):
            p.append(f"{n}: Preflight lists inputs but lacks the stop rule and the /wayfinder fallback")
        if not bullets and "No file is required" not in body:
            p.append(f"{n}: Preflight lists no input and does not say none is required")
        for b in bullets:
            m = re.fullmatch(r"`([^`]+)`(?: .*)?", b)
            if m and ("<artifact-root>" in m.group(1) or m.group(1).startswith("docs/")) and not allowed_paths.match(m.group(1)):
                p.append(f"{n}: Preflight path outside the standard layout: {m.group(1)}")
        if not (f.parent / "agents" / "agent.yaml").exists():
            p.append(f"{n}: missing agents/agent.yaml")
    for n in ("project-canvas", "audit-traceability", "review-readiness", "review-spec"):
        if "## Evidence (run before answering)" not in S[n][1] or "### Evidence" not in S[n][1]:
            p.append(f"{n}: must instruct the agent to run the validation script and attach the output as Evidence")
    qg = (R / "skills/requirements/review-readiness/QUALITY-GATES.md").read_text(encoding="utf-8", errors="replace")
    if "Return to when it fails" not in qg:
        p.append("QUALITY-GATES.md lacks the 'Return to' column")
    flow_t = (R / "docs/FLOW.md").read_text(encoding="utf-8", errors="replace")
    for needle in ("## Return routes", "BLOCKED", "NEEDS CHANGES"):
        if needle not in flow_t:
            p.append(f"docs/FLOW.md lacks '{needle}'")
    router = S["ask-req"][1]
    for n in S:
        if n != "ask-req" and n not in router:
            p.append(f"ask-req does not mention {n}")
    readme = (R / "README.md").read_text(encoding="utf-8", errors="replace")
    block = re.search(r"```mermaid\n(.*?)```", readme, re.S)
    if not block:
        p.append("README has no mermaid flow")
    else:
        for n in manual - {"handoff", "wait-what", "grill-me", "retro", "ask-req"}:
            if f"/{n}" not in block.group(1):
                p.append(f"README flow misses /{n}")
    for n, (f, _, _) in S.items():
        if f"]({f.relative_to(R).as_posix()})" not in readme:
            p.append(f"README catalog does not link {n}")
    for f in list(R.rglob("*.md")) + list(R.rglob("*.py")) + list(R.rglob("*.sh")) + list(R.rglob("*.yaml")):
        if ".git/" in f.as_posix():
            continue
        s = f.read_text(encoding="utf-8", errors="replace")
        if "\u2014" in s:
            p.append(f"em-dash in {f.relative_to(R)}")
        if "Call the Skill tool" in s and f.name not in ("INVOCATION.md", "AGENTS.md", "validate_repository.py"):
            p.append(f"non-portable trigger in {f.relative_to(R)}")
        if f.suffix == ".md":
            prose = re.sub(r"```.*?```", "", s, flags=re.S)
            for t in re.findall(r"(?<!!)\[[^\]]+\]\(([^)]+)\)", prose):
                if t.startswith(("http:", "https:", "#", "mailto:")):
                    continue
                if not (f.parent / t.split("#")[0]).exists():
                    p.append(f"broken link {f.relative_to(R)} -> {t}")
    for d in ("skills/requirements/project-canvas/CANVAS-TEMPLATE.md", "skills/requirements/project-canvas/scripts/canvas-check.py",
              "skills/requirements/setup-requirements-repo/scripts/migrate-layout.py", "skills/requirements/split-backlog/BACKLOG-FORMAT.md",
              "skills/requirements/graph-sync/GRAPH.md", "skills/requirements/graph-sync/scripts/req-graph.py",
              "skills/requirements/setup-requirements-repo/graph.md", "skills/requirements/setup-requirements-repo/versioning.md",
              "skills/requirements/write-user-story/SCREEN-FORMAT.md",
              "skills/requirements/setup-requirements-repo/graphifyignore.template", "docs/FLOW.md", "docs/DE-PARA.md", "docs/INVOCATION.md", "docs/AUTHORING-SKILLS.md"):
        if not (R / d).exists():
            p.append(f"missing {d}")
    return p


if __name__ == "__main__":
    problems = check()
    for x in problems:
        print(x)
    print("PASS" if not problems else f"FAIL ({len(problems)})", len(skills()), "skills")
    sys.exit(bool(problems))
