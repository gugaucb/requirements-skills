#!/usr/bin/env python3
"""Deterministic traceability check for requirements artifacts (stdlib only).

Usage: check-ids.py <artifact-root> [--json]

Where each ID type may be DEFINED (anywhere else it is only a reference):
  PRODUCT-VISION.md: GOAL, CAP      DECISIONS.md: DEC      BACKLOG.md: US, EPIC
  specs/SPEC-*.md: SPEC             changes/CHG-*.md: CHG
  stories/US-*.md (or US-*.md): US, FR, NFR, AC, TC, DG, FLD, SCR
Exit code 1 when problems are found.
"""
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

PREFIXES = ("GOAL", "CAP", "EPIC", "SPEC", "US", "FR", "NFR", "AC", "TC", "DG", "FLD", "SCR", "DEC", "CHG")
P = "|".join(PREFIXES)
ID = re.compile(rf"\b(?:{P})-\d{{3,}}\b")
DEF_LINE = re.compile(rf"^(?:\|\s*(?:\*\*)?|#{{1,3}}\s+|\*\*)((?:{P})-\d{{3,}})\b")
STALE = re.compile(r"\*\*Status:\*\*\s*Stale|\|\s*Stale\s*\|")


def may_define(path: Path, prefix: str) -> bool:
    n = path.name
    if n == "PRODUCT-VISION.md":
        return prefix in ("GOAL", "CAP")
    if n == "DECISIONS.md":
        return prefix == "DEC"
    if n == "BACKLOG.md":
        return prefix in ("US", "EPIC")
    if n.startswith("SPEC-"):
        return prefix == "SPEC"
    if n.startswith("CHG-"):
        return prefix == "CHG"
    if n.startswith("US-"):
        return prefix in ("US", "FR", "NFR", "AC", "TC", "DG", "FLD", "SCR")
    return False


def split_row(line):
    return [c.strip() for c in line.strip().strip("|").split("|")]


def analyse(root: Path):
    defs = defaultdict(list)
    refs = defaultdict(set)
    stale = []
    stories = {}
    for f in sorted(root.rglob("*.md")):
        in_matrix = False
        matrix = []
        for line in f.read_text(encoding="utf-8").splitlines():
            if line.startswith("#"):
                in_matrix = "canonical traceability" in line.lower()
            if in_matrix and line.startswith("|"):
                if not set(line) <= set("|- :"):
                    matrix.append(split_row(line))
            else:
                m = DEF_LINE.match(line)
                if m and may_define(f, m.group(1).split("-")[0]):
                    defs[m.group(1)].append(f)
            for i in ID.findall(line):
                refs[i].add(f)
            if STALE.search(line):
                stale.append(f"{f.name}: {line.strip()[:70]}")
        if f.name.startswith("US-"):
            stories[f.stem.split(":")[0].split(" ")[0][:6]] = (f, matrix)
    return defs, refs, stale, stories


def check(root: Path):
    problems = []
    defs, refs, stale, stories = analyse(root)
    for i, files in sorted(defs.items()):
        if len(files) > 1:
            problems.append(f"Duplicate definition {i}: {sorted({x.name for x in files})}")
    for i in sorted(refs):
        if i not in defs:
            problems.append(f"Dangling reference {i} (e.g. in {sorted(x.name for x in refs[i])[0]})")
    for sid, (f, matrix) in sorted(stories.items()):
        if not matrix:
            problems.append(f"{f.name}: no canonical traceability rows")
            continue
        own = {i for i, fs in defs.items() if f in fs}
        linked, proven = defaultdict(set), set()
        for row in matrix:
            ids = ID.findall(" ".join(row))
            tcs = [i for i in ids if i.startswith("TC-")]
            acs = [i for i in ids if i.startswith("AC-")]
            for r in (i for i in ids if i.startswith(("FR-", "NFR-"))):
                linked[r].update(acs)
            if tcs:
                proven.update(acs)
        for r in sorted(i for i in own if i.startswith(("FR-", "NFR-"))):
            if not linked[r]:
                problems.append(f"{f.name}: {r} has no AC in the matrix")
        for a in sorted(i for i in own if i.startswith("AC-")):
            if a not in proven:
                problems.append(f"{f.name}: {a} has no TC in the matrix")
    problems += [f"Stale item: {s}" for s in stale]
    counts = {p: sum(1 for i in defs if i.startswith(p + "-")) for p in PREFIXES}
    return problems, counts


def main(argv):
    args = [a for a in argv if not a.startswith("--")]
    if not args:
        print(__doc__)
        return 2
    problems, counts = check(Path(args[0]))
    if "--json" in argv:
        print(json.dumps({"problems": problems, "unique_ids": counts}, indent=2))
    else:
        print("Unique IDs defined:", ", ".join(f"{k}={v}" for k, v in counts.items() if v))
        for p in problems:
            print("-", p)
        print("PASS" if not problems else f"FAIL ({len(problems)})")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
