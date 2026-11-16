#!/usr/bin/env python3
"""Generate agents/openai.yaml (Codex UI metadata) for every skill from its SKILL.md frontmatter.

SKILL.md is the single source of truth and stays harness-neutral; this sidecar is optional metadata.
Usage: sync_adapters.py [--check]
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def frontmatter(text):
    m = re.match(r"---\n(.*?)\n---\n", text, re.S)
    out = {}
    if m:
        for line in m.group(1).splitlines():
            if ":" in line and not line.startswith(" "):
                k, v = line.split(":", 1)
                out[k.strip()] = v.strip().strip('"')
    return out


def render(skill_dir):
    fm = frontmatter((skill_dir / "SKILL.md").read_text(encoding="utf-8"))
    name = fm["name"]
    display = " ".join(w.capitalize() for w in name.split("-"))
    desc = fm["description"].split(". ")[0].rstrip(".").replace('"', "'")
    if len(desc) > 100:
        desc = desc[:100].rsplit(" ", 1)[0].rstrip(" ,;")
    lines = ["interface:", f'  display_name: "{display}"', f'  short_description: "{desc}"']
    if fm.get("disable-model-invocation") == "true":
        lines += ["policy:", "  allow_implicit_invocation: false"]
    return "\n".join(lines) + "\n"


def skill_dirs():
    for f in sorted((ROOT / "skills").glob("*/*/SKILL.md")):
        if f.parent.parent.name != "deprecated":
            yield f.parent


def main():
    check = "--check" in sys.argv
    bad = []
    for d in skill_dirs():
        target = d / "agents" / "openai.yaml"
        want = render(d)
        if check:
            if not target.exists() or target.read_text(encoding="utf-8") != want:
                bad.append(str(target.relative_to(ROOT)))
        else:
            target.parent.mkdir(exist_ok=True)
            target.write_text(want, encoding="utf-8")
    if check and bad:
        print("Out of sync (run scripts/sync_adapters.py):", *bad, sep="\n- ")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
