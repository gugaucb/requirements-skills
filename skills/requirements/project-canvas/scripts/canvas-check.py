#!/usr/bin/env python3
"""Mechanical integrity checks for a Project Model Canvas file (stdlib only).

Usage: canvas-check.py <PROJECT-CANVAS.md or folder> [--json] [--no-judgment]

Every post-it is a table row whose first cell is an ID (JUS OBJ BEN PRD RQT STK PRM ENT RSK TMP CST EQP RST).
The "Traces to" links are the IDs found in the rest of the row. A rule is waived for one row by writing
[waive C5: reason] in that row; waivers are listed so a human can acknowledge them.
Exit codes: 0 consistent, 1 a rule failed, 2 a cycle in the traces, 3 file missing or unreadable, 64 usage error.
Malformed rows and IDs are reported on stderr as [PARSE-WARNING]. Judgment rules (100% scope, SMART math, timeline vs constraints) are printed as questions.
"""
import json
import re
import sys
import unicodedata
from collections import defaultdict
from pathlib import Path

_SHARED = Path(__file__).resolve().parents[2] / "graph-sync" / "scripts"
if not (_SHARED / "reqmd.py").exists():
    print("canvas-check.py needs the graph-sync skill next to it (graph-sync/scripts/reqmd.py)", file=sys.stderr)
    sys.exit(3)
sys.path.insert(0, str(_SHARED))
import reqmd  # noqa: E402

BLOCKS = ("JUS", "OBJ", "BEN", "PRD", "RQT", "STK", "PRM", "ENT", "RSK", "TMP", "CST", "EQP", "RST")
ID = re.compile(r"\b(?:%s)-\d{3,}\b" % "|".join(BLOCKS), re.I)
WAIVE = re.compile(r"\[waive\s+(C\d+|R)\b[^\]]*\]", re.I)
HIGH = ("alta", "alto", "high")
OPPOSED = ("contrario", "neutro", "neutral", "opposed", "against", "resistente")

JUDGMENT = [
    "J1 Rule of 100%: do all delivery groups (ENT) together equal exactly the whole Product (PRD), nothing more, nothing less?",
    "J2 SMART math: if 100% of the deliveries are made, is each Objective (OBJ) actually reached, in numbers and by its deadline?",
    "J3 Constraints: do the Timeline (TMP) and Costs (CST) respect every Constraint (RST), for example a legal date or a budget cap?",
    "J4 Requirements: does each RQT describe an attribute, service level or compliance of the product, never an activity or a delivery?",
    "J5 Assumptions: is every assumption (PRM) that you do not control either low impact or covered by a risk?",
    "J6 Risks: do the response plans include contingency reserve in time and money (TMP, CST)?",
]


def norm(t):
    return unicodedata.normalize("NFKD", str(t)).encode("ascii", "ignore").decode().lower().strip()


cells = reqmd.split_row


def parse(path):
    items, headers, prev = {}, [], None
    lines, _ = reqmd.load_lines(path, path.name)
    for line in lines:
        if not line.startswith("|"):
            prev, headers = None, []
            continue
        c = cells(line)
        if set(line.strip()) <= set("|- :"):
            headers = [norm(x) for x in prev or []]
            continue
        prev = c
        first = c[0].strip("* ")
        if not re.fullmatch(r"(?:%s)-\d{3,}" % "|".join(BLOCKS), first):
            continue
        rest = WAIVE.sub("", " | ".join(c[1:]))
        waived = {w.upper() for w in WAIVE.findall(" ".join(c))}
        rowd = dict(zip(headers, c))
        items[first] = {"type": first.split("-")[0], "traces": sorted(set(ID.findall(rest)) - {first}),
                        "waived": waived, "row": rowd, "text": c[1] if len(c) > 1 else ""}
    return items


def field(item, *keys):
    for h, v in item["row"].items():
        if any(k in h for k in keys):
            return v
    return ""


def check(items):
    problems, waivers = [], []
    rev = defaultdict(set)
    for i, it in items.items():
        for t in it["traces"]:
            rev[t].add(i)
    of = lambda ids, p: [x for x in ids if x.split("-")[0] == p]
    unknown = sorted({t for it in items.values() for t in it["traces"] if t not in items})
    for u in unknown:
        problems.append(f"Dangling link: {u} is referenced but never defined")

    def need(rule, i, ok, msg):
        if ok:
            return
        if rule in items[i]["waived"]:
            waivers.append(f"{i}: {rule} waived ({msg})")
        else:
            problems.append(f"{rule} {i}: {msg}")

    for i, it in sorted(items.items()):
        t, tr, back = it["type"], it["traces"], rev.get(i, set())
        if t == "JUS":
            need("C1", i, of(back, "OBJ"), "Justification has no Objective tracing to it (the problem is not being resolved)")
            need("C1", i, of(back, "BEN"), "Justification has no Benefit tracing to it (no value for the pain)")
        if t in ("OBJ", "BEN"):
            need("C2", i, of(tr, "JUS"), f"{'Objective' if t == 'OBJ' else 'Benefit'} traces to no Justification (peripheral value nobody asked for)")
        if t == "RQT":
            need("C3", i, of(tr, "PRD"), "Requirement qualifies no Product item (orphan requirement)")
            need("C3", i, of(tr, "STK"), "Requirement traces to no Stakeholder expectation")
        if t == "PRD":
            need("C4", i, of(back, "ENT"), "Product item has no Delivery group building it")
        if t == "ENT":
            need("C4", i, of(tr, "PRD"), "Delivery group builds no Product item (not part of the Product)")
            need("C5", i, of(back, "TMP"), "Delivery group has no milestone or period in the Timeline")
            eq = of(back, "EQP")
            need("C5", i, of(back, "CST") or any(of(rev.get(e, set()), "CST") for e in eq), "Delivery group has no Cost line (own or for its team)")
            need("C6", i, eq or of(back, "CST") or of(back, "RSK"), "No Team competence, no Cost (outsourcing or training) and no Risk (lack of skills) for this delivery")
        if t == "PRM" and norm(field(it, "impact")) in HIGH:
            need("C7", i, of(back, "RSK"), "High-impact Assumption has no mirror Risk")
        if t == "STK" and norm(field(it, "power", "poder")) in HIGH and norm(field(it, "attitude", "atitude", "postura")) in OPPOSED:
            need("C8", i, of(back, "RSK"), "Powerful neutral or opposed Stakeholder has no Risk (resistance, blockage, approval delay)")
        if t == "OBJ":
            need("C9", i, of(back, "PRD"), "No Product item answers this Objective")
        if t == "RSK":
            need("C10", i, field(it, "mitigation", "mitigacao", "resposta", "response").strip(), "Risk has no mitigation or response plan")
            if norm(field(it, "impact")) in HIGH:
                need("C10", i, of(back, "CST") or of(back, "TMP"), "High-impact Risk has no contingency reserve in Costs or Timeline")
    # reverse traceability: cost -> delivery/team -> product -> requirement/objective -> justification
    def reaches_jus(i, seen=None):
        seen = seen or set()
        if i in seen:
            return False
        seen.add(i)
        return any(x.startswith("JUS-") or reaches_jus(x, seen) for x in items[i]["traces"] if x in items)
    for i, it in sorted(items.items()):
        if it["type"] in ("ENT", "PRD", "RQT", "EQP", "TMP", "CST"):
            contingency = it["traces"] and all(x.startswith("RSK-") for x in it["traces"])
            need("R", i, reaches_jus(i) or contingency, "Reverse test failed: no path to a Justification (fat to remove, or a missing link)")
    return problems, waivers


def main(argv):
    args = [a for a in argv if not a.startswith("--")]
    if not args:
        print(__doc__)
        return 64
    p = Path(args[0])
    if p.is_dir():
        found = list(p.rglob("PROJECT-CANVAS.md"))
        if not found:
            print("no PROJECT-CANVAS.md found", file=sys.stderr)
            return 3
        p = found[0]
    if not p.exists():
        print(f"file not found: {p}", file=sys.stderr)
        return 3
    items = parse(p)
    problems, waivers = check(items)
    counts = defaultdict(int)
    for it in items.values():
        counts[it["type"]] += 1
    adj = {i: [t for t in it["traces"] if t in items] for i, it in items.items()}
    cycles = reqmd.find_cycles_adj(adj, items)
    for c in cycles:
        problems.append("Trace cycle: " + " -> ".join(c))
    code = 2 if cycles else 1 if problems else 0
    if "--json" in argv:
        print(json.dumps({"file": str(p), "counts": counts, "problems": problems, "waivers": waivers, "cycles": cycles, "exit_code": code, "judgment": JUDGMENT}, indent=1))
    else:
        print(f"{p.name}: " + ", ".join(f"{k}={v}" for k, v in sorted(counts.items())))
        for x in problems:
            print("-", x)
        for w in waivers:
            print("~", w)
        print("PASS" if not problems else f"CYCLES ({len(cycles)})" if cycles else f"FAIL ({len(problems)})")
        if "--no-judgment" not in argv:
            print("Judgment checks (answer with the sponsor; the script cannot):")
            for q in JUDGMENT:
                print(" ?", q)
    return code


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
