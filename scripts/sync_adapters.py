#!/usr/bin/env python3
"""Generate the per-skill manifests from each SKILL.md (single source of truth, harness-neutral).

  skills/<bucket>/<name>/agents/agent.yaml   neutral manifest: invocation, required inputs, contract, scripts,
                                             next steps, plus an MCP-tool-shaped block for hosts that wrap skills as tools
  skills/<bucket>/<name>/agents/openai.yaml  Codex UI metadata (optional sidecar)

Usage: sync_adapters.py [--check]      Exit codes: 0 in sync, 1 out of sync.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def rd(p):
    return Path(p).read_text(encoding="utf-8", errors="replace")


def wr(p, s):
    Path(p).write_text(s, encoding="utf-8", errors="replace")


def frontmatter(text):
    m = re.match(r"---\n(.*?)\n---\n", text, re.S)
    out = {}
    if m:
        for line in m.group(1).splitlines():
            if ":" in line and not line.startswith(" "):
                k, v = line.split(":", 1)
                out[k.strip()] = v.strip().strip('"')
    return out


def section(text, title_start):
    m = re.search(rf"^## {re.escape(title_start)}[^\n]*\n(.*?)(?=^## |\Z)", text, re.S | re.M)
    return m.group(1) if m else ""


def q(s):
    return json.dumps(s, ensure_ascii=False)


def lst(items, indent="  "):
    return "".join(f"{indent}- {q(i)}\n" for i in items) if items else f"{indent}[]\n"


def render(skill_dir):
    """Codex sidecar."""
    fm = frontmatter(rd(skill_dir / "SKILL.md"))
    name = fm["name"]
    display = " ".join(w.capitalize() for w in name.split("-"))
    desc = fm["description"].split(". ")[0].rstrip(".").replace('"', "'")
    if len(desc) > 100:
        desc = desc[:100].rsplit(" ", 1)[0].rstrip(" ,;")
    lines = ["interface:", f'  display_name: "{display}"', f'  short_description: "{desc}"']
    if fm.get("disable-model-invocation") == "true":
        lines += ["policy:", "  allow_implicit_invocation: false"]
    return "\n".join(lines) + "\n"


def skill_names():
    return {f.parent.name for f in (ROOT / "skills").glob("*/*/SKILL.md") if f.parent.parent.name != "deprecated"}


def render_agent(skill_dir, names):
    text = rd(skill_dir / "SKILL.md")
    fm = frontmatter(text)
    name = fm["name"]
    pre = section(text, "Preflight")
    required = []
    for line in pre.split("If any of them")[0].splitlines():
        if line.startswith("- "):
            required.append(re.sub(r"`", "", line[2:]).strip())
    contract = {}
    for key in ("Reads", "Writes", "Gate"):
        m = re.search(rf"\*\*{key}:\*\*\s*(.+)", section(text, "Contract"))
        if m:
            contract[key.lower()] = re.sub(r"\s+", " ", m.group(1)).strip()
    scripts = sorted(f"scripts/{p.name}" for p in (skill_dir / "scripts").glob("*") if p.is_file() and not p.name.startswith("__")) if (skill_dir / "scripts").exists() else []
    nxt = []
    for n in re.findall(r"`/?([a-z][a-z0-9-]+)`", section(text, "Next steps")):
        if n in names and n != name and n not in nxt:
            nxt.append(n)
    invocation = "user" if fm.get("disable-model-invocation") == "true" else "model"
    out = ["schema: requirements-skills/agent-manifest/1", f"name: {q(name)}", f"description: {q(fm['description'])}",
           f"invocation: {invocation}   # user: only when the human types it; model: the agent may reach for it",
           'instructions: "AGENTS.md"   # root instructions; CLAUDE.md and GEMINI.md point there',
           "requires:   # Preflight: stop and ask when any is missing; never invent",
           lst(required).rstrip("\n")]
    out.append("contract:" + ("" if contract else " {}"))
    for k, v in contract.items():
        out.append(f"  {k}: {q(v)}")
    out.append("scripts:" + ("" if scripts else " []"))
    out += [f"  - {q(s)}" for s in scripts]
    out.append("next_steps:" + ("" if nxt else " []"))
    out += [f"  - {q(n)}" for n in nxt]
    props = {"arguments": {"type": "string", "description": fm.get("argument-hint", "Free text: what to do, or the ID to work on")}}
    out += ["mcp_tool:   # shaped like an MCP tool definition, for hosts that expose skills as tools",
            f"  name: {q(name)}", f"  description: {q(fm['description'])}",
            "  inputSchema: " + json.dumps({"type": "object", "properties": props}, ensure_ascii=False)]
    return "\n".join(out) + "\n"


def skill_dirs():
    for f in sorted((ROOT / "skills").glob("*/*/SKILL.md")):
        if f.parent.parent.name != "deprecated":
            yield f.parent


def main():
    check = "--check" in sys.argv
    names = skill_names()
    bad = []
    for d in skill_dirs():
        for fname, want in (("openai.yaml", render(d)), ("agent.yaml", render_agent(d, names))):
            target = d / "agents" / fname
            if check:
                if not target.exists() or rd(target) != want:
                    bad.append(str(target.relative_to(ROOT)))
            else:
                target.parent.mkdir(exist_ok=True)
                wr(target, want)
    if check and bad:
        print("Out of sync (run scripts/sync_adapters.py):", *bad, sep="\n- ")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
