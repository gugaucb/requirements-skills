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
        text = f.read_text(encoding="utf-8")
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
    if len(S) != 26:
        p.append(f"Expected 26 skills, found {len(S)}")
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
        if not y.exists() or y.read_text(encoding="utf-8") != render(f.parent):
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
    router = S["ask-req"][1]
    for n in S:
        if n != "ask-req" and n not in router:
            p.append(f"ask-req does not mention {n}")
    readme = (R / "README.md").read_text(encoding="utf-8")
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
        s = f.read_text(encoding="utf-8")
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
    for d in ("docs/FLOW.md", "docs/DE-PARA.md", "docs/INVOCATION.md", "docs/AUTHORING-SKILLS.md"):
        if not (R / d).exists():
            p.append(f"missing {d}")
    return p


if __name__ == "__main__":
    problems = check()
    for x in problems:
        print(x)
    print("PASS" if not problems else f"FAIL ({len(problems)})", len(skills()), "skills")
    sys.exit(bool(problems))
