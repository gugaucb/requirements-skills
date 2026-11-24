#!/usr/bin/env python3
"""Requirements artifacts -> typed knowledge graph (deterministic, stdlib only, no LLM).

Usage:
  req-graph.py build    <artifact-root> [--out FILE] [--force] [--view]
  req-graph.py view     <artifact-root> [--out FILE] [--title TEXT]
  req-graph.py query    <artifact-root> "<text>" [--depth N] [--limit N] [--budget TOKENS] [--type US,FR] [--status Stale] [--weak] [--json]
  req-graph.py path     <artifact-root> <ID> <ID> [--directed] [--all]
  req-graph.py explain  <artifact-root> <ID>
  req-graph.py backlog  <artifact-root> [--json]
  req-graph.py plan     <artifact-root> <SPEC-ID> [--json]
  req-graph.py affected <artifact-root> <ID> [--up] [--depth N] [--no-weak] [--json]
  req-graph.py frontier <artifact-root>
  req-graph.py stale    <artifact-root>
  req-graph.py validate <artifact-root> [--json] [--strict]     (alias: req-graph.py --validate <root>)
  req-graph.py critical <artifact-root> [--top N] [--json]

Exit codes of `validate` (the CI contract, shared with check-ids.py and canvas-check.py):
  0 consistent   1 orphan IDs or untested rules   2 dependency cycles   3 critical parse or file failure
  (64 usage error, 66 unknown target. `query` and `path` use 1 for "nothing found".)
Malformed rows and IDs are reported on stderr as [PARSE-WARNING]; `--strict` turns any warning into exit 3.

The graph file is node-link JSON that Graphify tools (merge-graphs, query, affected, path)
can read. IDs are the product's own IDs, so nodes never drift. Direction of every relation is
documented in ../GRAPH.md. Section headings are matched by canonical English keys; localized
headings go in <artifact-root>/graph/aliases.json: {"headings": {"impact": ["Impacto"]}, "status_values": {"Rascunho": "Draft"}}.
"""
import hashlib
import json
import math
import re
import sys
import unicodedata
from collections import defaultdict, deque
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import reqmd  # noqa: E402
from reqmd import (CANVAS, DEF_LINE, EXIT_CRITICAL, EXIT_CYCLES, EXIT_NOT_FOUND, EXIT_OK, EXIT_PROBLEMS,  # noqa: E402
                   EXIT_USAGE, ID, P, PREFIXES, ids_of, load_lines, rd, split_row as cells, warn, wr)

VERSION = 1
STATUSES = ["Draft", "Stale", "Blocked", "Needs changes", "Ready for human review", "Ready (team agreement)", "Retired"]
DEC_STATUS = re.compile(r"^(Confirmed|Proposed|Pending|Superseded)\b")
IMPACT_WORDS = ("Invalidated", "Needs review", "Unaffected (checked)")
DONE = {"Ready (team agreement)", "Retired"}
# One rule: an edge points at what its source DEPENDS on (dependent -> dependency).
# Impact therefore flows against edge direction, which is what `graphify affected` already does.
DEPENDENCY = {"serves", "part_of", "decided_by", "blocked_by", "verifies", "proves", "uses", "traces_to", "references"}
# Records that carry history but never propagate impact: changes, impacts, plans, needs_decision, changed_by, superseded_by
WEAK = {"references"}
HEAD_KEYS = {
    "change": ["change"], "impact": ["impact"], "decisions needed": ["decisions needed"],
    "canonical traceability": ["canonical traceability"], "change history": ["change history"],
}


def nid(i):
    return i.lower().replace("-", "_")


ALIAS_ERRORS = []


def load_aliases(root):
    f = root / "graph" / "aliases.json"
    if f.exists():
        try:
            return json.loads(rd(f))
        except ValueError:
            warn("graph/aliases.json", 1, "invalid JSON (aliases ignored)")
            ALIAS_ERRORS.append(str(f))
    return {}


def section_key(text, aliases):
    t = text.strip().lower()
    for key, names in HEAD_KEYS.items():
        extra = [x.lower() for x in aliases.get("headings", {}).get(key, [])]
        if t in names or t in extra:
            return key
    return t


def norm_status(text, aliases):
    text = text.strip().strip("*")
    text = aliases.get("status_values", {}).get(text, text)
    for s in STATUSES:
        if text == s:
            return s
    return None


def role(path):
    n = path.name
    if n == "PROJECT-CANVAS.md":
        return "canvas"
    if n == "PRODUCT-VISION.md":
        return "vision"
    if n == "DECISIONS.md":
        return "decisions"
    if n == "BACKLOG.md":
        return "backlog"
    if n.startswith("SPEC-"):
        return "spec"
    if n.startswith("CHG-"):
        return "chg"
    if n.startswith("US-"):
        return "story"
    return None


def owns(r, prefix):
    return prefix in {
        "vision": ("GOAL", "CAP"), "decisions": ("DEC",), "backlog": ("US", "EPIC"),
        "spec": ("SPEC", "PLN"), "chg": ("CHG",), "canvas": CANVAS, "story": ("US", "FR", "NFR", "AC", "TC", "DG", "FLD", "SCR"),
    }[r]


def pfx(i):
    return i.split("-")[0]


def frontmatter(lines):
    if not lines or lines[0].strip() != "---":
        return {}, 0
    out = {}
    for n, line in enumerate(lines[1:], 1):
        if line.strip() == "---":
            return out, n + 1
        if ":" in line:
            k, v = line.split(":", 1)
            v = re.sub(r"\s+#.*$", "", v.strip())
            out[k.strip()] = [x.strip() for x in v[1:-1].split(",") if x.strip()] if v.startswith("[") else v
    return {}, 0


class Graph:
    def __init__(self):
        self.nodes, self.edges, self.unresolved = {}, {}, set()
        self.cache, self.defs, self.matrix_files, self.declared = {}, defaultdict(list), set(), set()

    def node(self, i, label, f, line, **attrs):
        (self.declared.add(i) if f.endswith("BACKLOG.md") else self.defs[i].append((f, line)))
        if i in self.nodes:
            cur = self.nodes[i]
            if cur["source_file"].endswith("BACKLOG.md") and not f.endswith("BACKLOG.md"):
                cur.update(source_file=f, source_location=f"L{line}")
            return
        self.nodes[i] = {"id": nid(i), "label": f"{i}: {label}".rstrip(": ").strip() if label else i,
                         "file_type": "concept", "source_file": f, "source_location": f"L{line}",
                         "req_id": i, "req_type": pfx(i), **attrs}

    def edge(self, s, t, rel, f, line, **attrs):
        if s == t:
            return
        self.edges.setdefault((s, t, rel), {"source": nid(s), "target": nid(t), "relation": rel,
                                            "confidence": "EXTRACTED", "source_file": f,
                                            "source_location": f"L{line}", **attrs})


LIFECYCLE = ("draft", "review", "approved", "deprecated")


def expected_lifecycle(status):
    st = (status or "").strip()
    low = st.lower()
    if st in ("Ready (team agreement)",) or low.startswith(("approved", "applied", "confirmed")):
        return "approved"
    if st == "Ready for human review":
        return "review"
    if st in ("Retired",) or low.startswith(("superseded", "deprecated")):
        return "deprecated"
    if st in ("Draft", "Blocked", "Needs changes", "Stale") or low.startswith(("pending", "proposed")):
        return "draft"
    return ""


def hget(rowd, *keys):
    for h, v in rowd.items():
        if any(k in h for k in keys):
            return v
    return ""


def scan_backlog(g, f, rel, lines, numbers, aliases, defs_only):
    """BACKLOG.md: one table row per story (first US ID owns the row); `### US-NNN` blocks hold the operations checklist."""
    headers, prev, cur = [], None, None
    ops = defaultdict(lambda: [0, 0])
    for n, line in zip(numbers, lines):
        if line.startswith("|"):
            c = cells(line)
            if set(line.strip()) <= set("|- :"):
                headers = [norm(x) for x in prev or []]
                continue
            prev = c
        else:
            prev, headers = None, []
        h = re.match(r"#{2,4}\s+(US-\d{3,})\b", line)
        if h:
            cur = h.group(1)
            continue
        if line.startswith("#"):
            cur = None
        ck = re.match(r"\s*[-*]\s+\[( |x|X)\]\s+", line)
        if ck and cur:
            ops[cur][1] += 1
            ops[cur][0] += ck.group(1) != " "
            continue
        if not line.startswith("|") or not headers:
            continue
        cs = cells(line)
        idx = next((k for k, x in enumerate(cs) if re.fullmatch(r"US-\d{3,}", x.strip("* "))), None)
        if idx is None:
            continue
        owner = cs[idx].strip("* ")
        rowd = dict(zip(headers, cs))
        if defs_only:
            attrs = {}
            for x in cs:
                st = norm_status(x, aliases)
                if st:
                    attrs["req_status"] = st
            prog = hget(rowd, "progress", "progresso")
            if prog:
                attrs["progress"] = prog
            g.node(owner, cs[idx + 1] if idx + 1 < len(cs) else "", rel, n, **attrs)
            for x in cs:
                e = re.match(r"(EPIC-\d{3,})\b\s*[:\-]?\s*(.*)", x.strip("* "))
                if e:
                    g.node(e.group(1), e.group(2), rel, n)
            continue
        epic = next((re.match(r"EPIC-\d{3,}", x.strip("* ")).group(0) for x in cs if re.match(r"EPIC-\d{3,}", x.strip("* "))), None)
        for x in cs[:idx]:
            for i in ids_of(x):
                if pfx(i) in ("GOAL", "CAP"):
                    if i not in g.nodes:
                        g.unresolved.add(i)
                        continue
                    g.edge(owner, i, "serves", rel, n)
                    if epic and pfx(i) == "CAP" and epic in g.nodes:
                        g.edge(epic, i, "serves", rel, n)
        if epic:
            g.edge(owner, epic, "part_of", rel, n)
        for x in cs[idx + 2:]:
            for i in ids_of(x):
                if pfx(i) == "US":
                    (g.edge(owner, i, "blocked_by", rel, n) if i in g.nodes else g.unresolved.add(i))
    if defs_only:
        for u, (done, total) in ops.items():
            if u in g.nodes:
                g.nodes[u]["ops_done"], g.nodes[u]["ops_total"] = done, total


def scan_file(g, f, root, aliases, defs_only):
    r = role(f)
    if not r:
        return
    rel = f.relative_to(root).as_posix()
    if f not in g.cache:
        g.cache[f] = load_lines(f, rel)
    lines, numbers = g.cache[f]
    if r == "backlog":
        scan_backlog(g, f, rel, lines, numbers, aliases, defs_only)
        return
    fm, start = frontmatter(lines)
    headers, prev = [], None
    section, header_block, owner, primary = "", True, None, None
    pending_ac = None
    for n, line in zip(numbers[start:], lines[start:]):
        rowd = {}
        if line.startswith("|"):
            if set(line.strip()) <= set("|- :"):
                headers = [norm(x) for x in prev or []]
            else:
                prev = cells(line)
                rowd = dict(zip(headers, prev))
        else:
            prev, headers = None, []
        if line.startswith("#"):
            header_block = header_block and not line.startswith("##")
            section = section_key(line.lstrip("#"), aliases) if line.startswith("##") else section
            if line.startswith("##"):
                owner = None if r != "chg" else owner
        in_matrix = section == "canonical traceability" or section == "change history"
        ids = ids_of(line)
        m = DEF_LINE.match(line)
        is_def = bool(m) and owns(r, pfx(m.group(1))) and not in_matrix
        if is_def:
            i, label = m.group(1), re.sub(r"\s*\|.*", "", m.group(2)).strip().strip("*")[:90]
            if r == "story" and pfx(i) == "US":
                primary = i
            attrs = {}
            if r == "spec" and pfx(i) == "PLN":
                label = hget(rowd, "change", "mudan") or label
                st = re.match(r"(Pending|Done|Skipped|Blocked)", hget(rowd, "status"), re.I)
                attrs.update({"plan_kind": hget(rowd, "kind", "tipo"), "plan_target": hget(rowd, "target", "alvo"),
                              "req_status": st.group(1).capitalize() if st else "Pending"})
            if r == "decisions":
                cs = cells(line)
                label = cs[1] if len(cs) > 1 else label
                for c in cs[1:]:
                    mm = DEC_STATUS.match(c)
                    if mm:
                        attrs["req_status"] = mm.group(1)
                        break
            if r == "vision":
                cs = cells(line)
                label = cs[1] if len(cs) > 1 else label
            if pfx(i) == "AC":
                pending_ac = i
                label = ""
            if defs_only:
                g.node(i, label, rel, n, **attrs)
                continue
            owner = i
        elif pending_ac and defs_only and line.strip().startswith("Scenario"):
            g.nodes[pending_ac]["label"] = f"{pending_ac}: {line.strip().split(':', 1)[-1].strip()}"
            pending_ac = None
        if defs_only:
            if r in ("story", "spec", "chg") and re.match(r"\*\*Status:\*\*", line.strip()):
                st = re.sub(r"\*\*Status:\*\*\s*", "", line.strip()).split("|")[0].strip().strip("*")
                key = (primary if r == "story" else None) or next(
                    (i for i in g.nodes if g.nodes[i]["source_file"] == rel and pfx(i) in ("SPEC", "CHG", "US")), None)
                ns = norm_status(st, aliases)
                if key and key in g.nodes:
                    g.nodes[key]["req_status"] = ns or st.split(" by ")[0].strip()
            continue
        # relations pass
        if not ids:
            continue
        subject = primary if r == "story" else owner
        def link(s, t, relname, **a):
            if t in g.nodes and s in g.nodes:
                g.edge(s, t, relname, rel, n, **a)
            else:
                g.unresolved.add(t if t not in g.nodes else s)
        uniq = list(dict.fromkeys(ids))
        if line.startswith("|") and in_matrix and section == "canonical traceability":
            g.matrix_files.add(rel)
            rq = [i for i in uniq if pfx(i) in ("FR", "NFR")]
            ac = [i for i in uniq if pfx(i) == "AC"]
            tc = [i for i in uniq if pfx(i) == "TC"]
            for x in rq:
                for a in ac:
                    link(a, x, "verifies")
            for a in ac:
                for t in tc:
                    link(t, a, "proves")
            continue
        if r == "story":
            if section == "change history" and line.startswith("|"):
                for c in uniq:
                    if pfx(c) == "CHG":
                        link(primary, c, "changed_by")
                continue
            if header_block and not is_def:
                for i in uniq:
                    if pfx(i) in ("GOAL", "CAP"):
                        link(primary, i, "serves")
                    elif pfx(i) in ("EPIC", "SPEC"):
                        link(primary, i, "part_of")
                continue
            if is_def and pfx(owner) != "US":
                link(owner, primary, "part_of")
                for i in uniq:
                    if i == owner:
                        continue
                    if pfx(i) == "DEC":
                        link(owner, i, "decided_by")
                    elif pfx(owner) == "SCR" and pfx(i) == "FLD":
                        link(owner, i, "uses")
                    elif pfx(i) not in ("US", "CHG"):
                        link(owner, i, "references")
                continue
            if owner and pfx(owner) in ("SCR", "AC", "FR", "NFR", "TC") and not is_def:
                for i in uniq:
                    if i == owner:
                        continue
                    if pfx(i) == "DEC":
                        link(owner, i, "decided_by")
                    elif pfx(owner) == "SCR" and pfx(i) == "FLD":
                        link(owner, i, "uses")
                    elif pfx(i) not in ("US", "CHG"):
                        link(owner, i, "references")
                continue
        if r == "decisions" and is_def:
            for i in uniq:
                if i != owner:
                    link(i, owner, "decided_by")
            continue
        if r == "canvas" and is_def:
            for i in dict.fromkeys(ids_of(re.sub(r"\[waive[^\]]*\]", "", line))):
                if i != owner:
                    link(owner, i, "traces_to")
            continue
        if r == "spec" and is_def and pfx(owner) == "PLN":
            spec = next((k for k, v in g.nodes.items() if pfx(k) == "SPEC" and v["source_file"] == rel), None)
            if spec:
                link(owner, spec, "part_of")
            for i in dict.fromkeys(ids_of(hget(rowd, "target", "alvo"))):
                link(owner, i, "plans")
            for i in dict.fromkeys(ids_of(hget(rowd, "depend"))):
                link(owner, i, "blocked_by")
            continue
        if r == "chg" and line.startswith("|"):
            target = next((i for i in uniq), None)
            if section == "change" and target:
                link(subject, target, "changes")
            elif section == "impact" and target:
                word = next((w for w in IMPACT_WORDS if w in line), "")
                link(subject, target, "impacts", **({"impact": word} if word else {}))
            elif section == "decisions needed":
                for i in uniq:
                    if pfx(i) == "DEC":
                        link(subject, i, "needs_decision")
            continue
        if r == "vision" and is_def:
            for i in uniq:
                if i == owner:
                    continue
                link(owner, i, "serves" if pfx(i) == "GOAL" else "decided_by" if pfx(i) == "DEC"
                     else "traces_to" if pfx(i) in CANVAS else "references")
            continue
        sup = re.search(rf"Superseded by ({P}-\d{{3,}})", line)
        if sup and subject:
            link(subject, sup.group(1), "superseded_by")
        if subject:
            for i in uniq:
                if i == subject:
                    continue
                if r in ("story", "spec") and pfx(i) == "DEC":
                    link(subject, i, "decided_by")
                elif pfx(i) == "CHG" and r == "story":
                    link(subject, i, "changed_by")
                elif r == "spec" and pfx(i) in ("GOAL", "CAP") and header_block:
                    link(subject, i, "serves")
                elif r == "spec" and pfx(i) == "EPIC":
                    link(subject, i, "part_of")
                elif r == "spec" and pfx(i) == "US":
                    continue
                elif r == "chg":
                    link(subject, i, "references")
                else:
                    link(subject, i, "references")
    # frontmatter (optional): status, serves, blocked_by
    if fm and not defs_only:
        key = fm.get("id")
        if key in g.nodes:
            for t in fm.get("serves", []) if isinstance(fm.get("serves"), list) else []:
                if t in g.nodes:
                    g.edge(key, t, "part_of" if pfx(t) in ("EPIC", "SPEC") else "serves", rel, 1)
            for t in fm.get("blocked_by", []) if isinstance(fm.get("blocked_by"), list) else []:
                if t in g.nodes:
                    g.edge(key, t, "blocked_by", rel, 1)
    if fm and defs_only and fm.get("id") in g.nodes:
        node = g.nodes[fm["id"]]
        if isinstance(fm.get("status"), str):
            s = norm_status(fm["status"], aliases)
            if s:
                node["req_status"] = s
            lc = fm["status"].strip().lower()
            if lc in LIFECYCLE:
                node["lifecycle"] = lc
            elif not s:
                warn(rel, 1, f"frontmatter status '{fm['status']}' is not one of {', '.join(LIFECYCLE)}")
        if isinstance(fm.get("version"), str):
            if re.fullmatch(r"\d+\.\d+\.\d+", fm["version"].strip()):
                node["version"] = fm["version"].strip()
            else:
                warn(rel, 1, f"frontmatter version '{fm['version']}' is not X.Y.Z")
        det = node.get("req_status", "")
        want = expected_lifecycle(det)
        if node.get("lifecycle") and want and node["lifecycle"] != want and not (fm.get("status", "").strip().lower() == det.lower()):
            warn(rel, 1, f"frontmatter status '{node['lifecycle']}' does not match Status '{det}' (expected '{want}')")


def md_files(root):
    return [f for f in sorted(root.rglob("*.md")) if "graph" not in f.relative_to(root).parts[:1]]


def build(root, collect_refs=False):
    root = Path(root)
    aliases = load_aliases(root)
    g = Graph()
    g.refs = defaultdict(set)
    files = md_files(root)
    for defs_only in (True, False):
        for f in files:
            scan_file(g, f, root, aliases, defs_only)
    if collect_refs:
        for f in files:
            rel = f.relative_to(root).as_posix()
            lines, _ = g.cache[f] if f in g.cache else load_lines(f, rel, report=False)
            for line in lines:
                for i in ids_of(line):
                    g.refs[i].add(rel)
    digest = hashlib.sha256()
    digest.update(str(VERSION).encode())
    for f in files:
        digest.update(f.relative_to(root).as_posix().encode() + f.read_bytes())
    digest.update(json.dumps(aliases, sort_keys=True).encode())
    return g, digest.hexdigest()


def to_json(g, digest):
    return {"directed": True, "multigraph": False,
            "graph": {"req_graph_version": VERSION, "digest": digest, "unresolved": sorted(g.unresolved)},
            "nodes": list(g.nodes.values()), "links": list(g.edges.values()), "hyperedges": []}


def viewer_html(g, digest, title):
    """Self-contained interactive HTML (no CDN, no network): layered layout, impact highlight, search."""
    by_nid = {n["id"]: n["req_id"] for n in g.nodes.values()}
    data = {
        "title": title, "digest": digest, "unresolved": sorted(g.unresolved),
        "nodes": [{"id": n["req_id"], "type": n["req_type"], "status": n.get("req_status", ""),
                   "label": n["label"].split(": ", 1)[1] if ": " in n["label"] else "",
                   "file": n["source_file"], "loc": n["source_location"]} for n in g.nodes.values()],
        "edges": [{"s": by_nid[e["source"]], "t": by_nid[e["target"]], "r": e["relation"],
                   **({"impact": e["impact"]} if e.get("impact") else {})} for e in g.edges.values()],
    }
    blob = (json.dumps(data, ensure_ascii=True).replace("<", "\\u003c").replace(">", "\\u003e")
            .replace("&", "\\u0026"))
    tpl = rd(Path(__file__).with_name("viewer.html.tpl"))
    return tpl.replace("__DATA__", blob, 1)


def adjacency(g, weak=True):
    """down[X] = items that depend on X (impacted when X changes); up[X] = items X depends on."""
    down, up = defaultdict(list), defaultdict(list)
    for (src, tgt, rel) in g.edges:
        if rel in DEPENDENCY and (weak or rel not in WEAK):
            down[tgt].append((src, rel))
            up[src].append((tgt, rel))
    return down, up


def walk(start, adj, depth):
    seen, out, q = {start}, [], deque([(start, 0, [])])
    while q:
        cur, d, path = q.popleft()
        if d == depth:
            continue
        for nxt, rel in adj.get(cur, []):
            if nxt in seen:
                continue
            seen.add(nxt)
            step = path + [f"{cur} -{rel}-> {nxt}"]
            out.append({"id": nxt, "depth": d + 1, "via": rel, "weak": rel in WEAK, "path": step})
            q.append((nxt, d + 1, step))
    return out


def affected(g, target, up=False, depth=3, weak=True):
    down, upadj = adjacency(g, weak)
    main = walk(target, upadj if up else down, depth)
    shared = {}
    if not up:
        hit = {m["id"] for m in main}
        for anc in walk(target, upadj, 1):
            for sib in walk(anc["id"], down, 1):
                if sib["id"] != target and sib["id"] not in hit:
                    shared.setdefault(sib["id"], []).append(anc["id"])
    return main, [{"id": k, "via_shared": ", ".join(v)} for k, v in shared.items()]


STOP = set("a an the of and or to in on for with what which who how is are was were be it this that does do did where when why "
           "o os as de da do das dos e ou para por com um uma que qual quais como em no na nos nas se ao aos".split())
TYPE_WORDS = {"FLD": "field fields", "SCR": "screen screens form", "GOAL": "goal objective", "CAP": "capability", "EPIC": "epic", "SPEC": "spec", "US": "story stories",
              "FR": "functional requirement", "NFR": "nonfunctional quality performance", "AC": "acceptance criterion criteria",
              "TC": "test tests", "DG": "diagram", "DEC": "decision decisions", "CHG": "change"}


def norm(text):
    text = unicodedata.normalize("NFKD", str(text)).encode("ascii", "ignore").decode().lower()
    return text


def words(text):
    return [w for w in re.findall(r"[a-z0-9]+(?:-[0-9]+)?", norm(text)) if w]


def search(g, text, types=None, status=None):
    """Rank nodes for a free-text query: ID match, then IDF-weighted word, prefix and substring matches."""
    ids = {i.upper() for i in ids_of(text.upper())}
    qwords = [w for w in words(ID.sub(" ", text.upper())) if w not in STOP and len(w) > 1]
    docs = {}
    for i, n in g.nodes.items():
        body = n["label"].split(": ", 1)[1] if ": " in n["label"] else ""
        docs[i] = {"w": set(words(body)), "n": norm(body), "meta": set(words(n.get("req_status", "") + " " + TYPE_WORDS.get(n["req_type"], "")))}
    N = max(len(docs), 1)
    df = defaultdict(int)
    for d in docs.values():
        for w in d["w"] | d["meta"]:
            df[w] += 1
    idf = lambda w: math.log(1 + N / (1 + df.get(w, 0)))
    scored = {}
    for i, d in docs.items():
        n = g.nodes[i]
        if types and n["req_type"] not in types:
            continue
        if status and norm(n.get("req_status", "")) != norm(status):
            continue
        sc = 100.0 if i in ids else 0.0
        for w in qwords:
            if w in d["w"]:
                sc += 2 * idf(w)
            elif w in d["meta"]:
                sc += 0.8 * idf(w)
            elif len(w) >= 3 and any(x.startswith(w) for x in d["w"]):
                sc += idf(w)
            elif len(w) >= 4 and w in d["n"]:
                sc += 0.5 * idf(w)
        if sc > 0 or (status and not qwords and not ids):
            scored[i] = sc
    return sorted(scored.items(), key=lambda kv: (-kv[1], kv[0]))


def neighbours(g, weak):
    nb = defaultdict(list)
    for (s_, t_, rel) in g.edges:
        if rel in WEAK and not weak:
            continue
        nb[s_].append((t_, rel, "out"))
        nb[t_].append((s_, rel, "in"))
    return nb


def query(g, text, depth=1, limit=8, types=None, status=None, weak=False, max_nodes=30):
    ranked = search(g, text, types, status)
    seeds = ranked[:limit]
    nb = neighbours(g, weak)
    shown = {i: {"score": sc, "dist": 0, "via": None} for i, sc in seeds}
    frontier = [i for i, _ in seeds]
    for d in range(1, depth + 1):
        nxt = []
        for cur in frontier:
            for other, rel, direction in sorted(nb.get(cur, []), key=lambda x: x[0]):
                if other not in shown and len(shown) < max_nodes:
                    shown[other] = {"score": 0, "dist": d, "via": (cur, rel, direction)}
                    nxt.append(other)
        frontier = nxt
    hit = {i for i, _ in seeds}
    links = [(s_, t_, rel) for (s_, t_, rel) in g.edges
             if s_ in shown and t_ in shown and (s_ in hit or t_ in hit) and (weak or rel not in WEAK)]
    return {"matches": seeds, "total_matches": len(ranked), "shown": shown, "links": sorted(links)}


def shortest_path(g, a, b, directed=False, include_all=False):
    steps = defaultdict(list)
    for (s_, t_, rel) in g.edges:
        if not include_all and (rel in WEAK or rel not in DEPENDENCY):
            continue
        steps[s_].append((t_, rel, "out"))
        if not directed:
            steps[t_].append((s_, rel, "in"))
    prev, q = {a: None}, deque([a])
    while q:
        cur = q.popleft()
        if cur == b:
            break
        for nxt, rel, d in sorted(steps.get(cur, [])):
            if nxt not in prev:
                prev[nxt] = (cur, rel, d)
                q.append(nxt)
    if b not in prev:
        return None
    hops, cur = [], b
    while prev[cur]:
        p_, rel, d = prev[cur]
        hops.append((p_, rel, d, cur))
        cur = p_
    return list(reversed(hops))


def derived_progress(n):
    t, d = n.get("ops_total", 0), n.get("ops_done", 0)
    return "No checklist" if not t else "Pending" if d == 0 else "Done" if d == t else "In progress"


def backlog_rows(g):
    rows = []
    for i, n in sorted(g.nodes.items()):
        if n["req_type"] != "US":
            continue
        caps = sorted(t for (s_, t, r) in g.edges if s_ == i and r == "serves" and pfx(t) == "CAP")
        epic = next((t for (s_, t, r) in g.edges if s_ == i and r == "part_of" and pfx(t) == "EPIC"), "")
        flags = []
        prog = derived_progress(n)
        declared = n.get("progress", "")
        if declared and norm(declared) != norm(prog) and prog != "No checklist":
            flags.append(f"progress column says {declared}, checklist says {prog}")
        if n.get("req_status", "").startswith("Ready") and prog not in ("Done", "No checklist"):
            flags.append("status is Ready but the operations checklist is not complete")
        if not caps and not epic:
            flags.append("no capability link")
        rows.append({"id": i, "name": n["label"].split(": ", 1)[-1], "epic": epic, "caps": caps,
                     "status": n.get("req_status", "-"), "ops": f"{n.get('ops_done', 0)}/{n.get('ops_total', 0)}",
                     "progress": prog, "flags": flags})
    return rows


def plan_rows(g, spec):
    items = {i: n for i, n in g.nodes.items() if n["req_type"] == "PLN" and (i, spec, "part_of") in g.edges}
    deps = {i: sorted(t for (s_, t, r) in g.edges if s_ == i and r == "blocked_by" and t in items) for i in items}
    order, seen = [], set()

    def visit(i):
        if i in seen:
            return
        seen.add(i)
        for d in deps[i]:
            visit(d)
        order.append(i)
    for i in sorted(items):
        visit(i)
    done = lambda i: items[i].get("req_status") in ("Done", "Skipped")
    rows = []
    for i in order:
        n = items[i]
        tgt = n.get("plan_target", "")
        tids = ids_of(tgt)
        warn = []
        if not tids and n.get("plan_kind", "") in ("new-story", "modify-story"):
            warn.append("story line has no US ID: run /split-backlog first (new story) or name the story")
        for t in tids:
            if t not in g.nodes:
                warn.append(f"target {t} does not exist yet")
        rows.append({"id": i, "kind": n.get("plan_kind", ""), "target": tgt, "change": n["label"].split(": ", 1)[-1],
                     "status": n.get("req_status", "Pending"), "depends_on": deps[i],
                     "ready": not done(i) and all(done(d) for d in deps[i]), "warnings": warn})
    return rows


def source_line(root, n):
    try:
        lines = rd(Path(root) / n["source_file"]).splitlines()
        return lines[int(n["source_location"][1:]) - 1].strip()[:200]
    except (OSError, ValueError, IndexError):
        return ""


def fmt(g, i):
    n = g.nodes[i]
    return f"{i}" + (f" [{n['req_status']}]" if n.get("req_status") else "")


def label(g, i):
    return g.nodes[i]["label"] if i in g.nodes else i


CYCLE_RELS = DEPENDENCY | {"superseded_by"}


def find_cycles(g):
    """Directed cycles over dependency relations (plus `superseded_by`), by iterative DFS with three colors.

    Change records (`changes`, `impacts`, `changed_by`, `needs_decision`) are deliberately outside the check:
    a change and the story it impacts always point at each other by design, so they would be false cycles.
    A cycle that passes through a CHG node therefore only appears when the CHG sits on a real dependency
    edge (for example a change that `blocked_by` another change)."""
    adj = defaultdict(list)
    for (s_, t_, rel) in g.edges:
        if rel in CYCLE_RELS:
            adj[s_].append(t_)
    return reqmd.find_cycles_adj(adj, g.nodes)


def critical_nodes(g, top=5):
    """Rank artifacts by how much breaks if they change: transitive dependents first, direct dependents second.
    (Edges point at dependencies, so this is the in-degree of dependency edges: the out-degree of impact.)"""
    down, _ = adjacency(g, weak=False)
    rows = []
    for i in g.nodes:
        if g.nodes[i]["req_type"] in ("CHG", "PLN"):
            continue
        cascade = len(walk(i, down, 99))
        rows.append({"id": i, "direct": len(down.get(i, [])), "cascade": cascade, "label": g.nodes[i]["label"].split(": ", 1)[-1]})
    rows.sort(key=lambda r: (-r["cascade"], -r["direct"], r["id"]))
    return rows[:top]


def validate(root, strict=False):
    """One validation for the whole artifact root. Exit-code contract: see reqmd (0, 1, 2, 3)."""
    reqmd.reset_warnings()
    ALIAS_ERRORS.clear()
    root = Path(root)
    res = {"problems": [], "cycles": [], "critical": [], "counts": {}, "top": [], "warnings": []}
    if not root.exists():
        res["critical"].append(f"artifact root not found: {root}")
        return res
    try:
        g, _ = build(root, collect_refs=True)
    except (OSError, ValueError, RecursionError) as e:
        res["critical"].append(f"cannot read or parse artifacts: {e}")
        return res
    if not g.cache:
        res["critical"].append("no recognizable artifact files found (expected PROJECT-CANVAS, PRODUCT-VISION, BACKLOG, SPEC-*, US-*, CHG-*, DECISIONS)")
    for e in ALIAS_ERRORS:
        res["critical"].append(f"{e} is not valid JSON")
    problems = res["problems"]
    for i, entries in sorted(g.defs.items()):
        if len(entries) > 1:
            where = sorted({f"{f}:L{ln}" for f, ln in entries})
            problems.append(f"Duplicate definition {i}: {', '.join(where)}")
    for i in sorted(g.refs):
        if i not in g.defs and i not in g.declared:
            problems.append(f"Dangling reference {i} (e.g. in {sorted(g.refs[i])[0]})")
    covered = {t for (s_, t, r) in g.edges if r == "verifies"}
    proven = {t for (s_, t, r) in g.edges if r == "proves"}
    story_files = sorted({n["source_file"] for n in g.nodes.values() if n["req_type"] == "US" and Path(n["source_file"]).name.startswith("US-")})
    for sf in story_files:
        name = Path(sf).name
        if sf not in g.matrix_files:
            problems.append(f"{name}: no canonical traceability rows")
            continue
        own = {i: n for i, n in g.nodes.items() if n["source_file"] == sf}
        for i in sorted(own):
            if own[i]["req_type"] in ("FR", "NFR") and i not in covered:
                problems.append(f"{name}: {i} has no AC in the matrix")
        for i in sorted(own):
            if own[i]["req_type"] == "AC" and i not in proven:
                problems.append(f"{name}: {i} has no TC in the matrix")
    for i, n in sorted(g.nodes.items()):
        if n.get("req_status") == "Stale":
            problems.append(f"Stale item: {i} ({n['source_file']})")
    res["cycles"] = find_cycles(g)
    res["top"] = critical_nodes(g, 5)
    res["counts"] = {p_: sum(1 for i in g.nodes if i.startswith(p_ + "-")) for p_ in PREFIXES}
    res["warnings"] = [f"{f}:L{ln}: {m}" for f, ln, m in reqmd.WARNINGS]
    if strict and res["warnings"]:
        res["critical"].append(f"{len(res['warnings'])} parse warning(s) under --strict")
    return res


def exit_code(res):
    return (EXIT_CRITICAL if res["critical"] else EXIT_CYCLES if res["cycles"] else EXIT_PROBLEMS if res["problems"] else EXIT_OK)


def print_validation(res, as_json=False):
    code = exit_code(res)
    if as_json:
        print(json.dumps({**res, "exit_code": code}, indent=1))
        return code
    print("Unique IDs defined:", ", ".join(f"{k}={v}" for k, v in res["counts"].items() if v))
    for p_ in res["problems"]:
        print("-", p_)
    for c in res["cycles"]:
        print("! cycle:", " -> ".join(c))
    for c in res["critical"]:
        print("!! critical:", c)
    if res["top"]:
        print("Top 5 critical artifacts (what breaks in cascade if they change):")
        for k, r_ in enumerate(res["top"], 1):
            print(f"  {k}. {r_['id']}  cascade {r_['cascade']}  direct {r_['direct']}  {r_['label'][:50]}")
    if res["warnings"]:
        print(f"{len(res['warnings'])} parse warning(s) on stderr")
    verdict = {EXIT_OK: "PASS", EXIT_PROBLEMS: f"FAIL ({len(res['problems'])})", EXIT_CYCLES: f"CYCLES ({len(res['cycles'])})",
               EXIT_CRITICAL: "CRITICAL"}[code]
    print(f"{verdict} (exit {code})")
    return code


def main(argv):
    if argv and argv[0] == "--validate":
        argv = ["validate"] + argv[1:]
    if len(argv) < 2 or argv[0] not in ("build", "affected", "frontier", "stale", "view", "query", "path", "explain", "backlog", "plan", "validate", "critical"):
        print(__doc__)
        return EXIT_USAGE
    cmd, root = argv[0], Path(argv[1])
    flags = argv[2:]
    if cmd == "validate":
        return print_validation(validate(root, strict="--strict" in flags), as_json="--json" in flags)
    g, digest = build(root)
    title = flags[flags.index("--title") + 1] if "--title" in flags else (root.resolve().name or "Requirements") + ": requirements graph"
    if cmd == "view":
        out = Path(flags[flags.index("--out") + 1]) if "--out" in flags else root / "graph" / "req-graph.html"
        out.parent.mkdir(parents=True, exist_ok=True)
        wr(out, viewer_html(g, digest, title))
        print(f"viewer -> {out}")
        return 0
    if cmd == "build":
        out = Path(flags[flags.index("--out") + 1]) if "--out" in flags else root / "graph" / "req-graph.json"
        html = out.with_suffix(".html")
        fresh = False
        if out.exists() and "--force" not in flags:
            try:
                fresh = json.loads(rd(out))["graph"].get("digest") == digest
            except (ValueError, KeyError):
                fresh = False
        if fresh:
            print(f"up to date: {out}")
        else:
            out.parent.mkdir(parents=True, exist_ok=True)
            wr(out, json.dumps(to_json(g, digest), indent=1))
            print(f"{len(g.nodes)} nodes, {len(g.edges)} edges -> {out}")
        if "--view" in flags and (not fresh or not html.exists()):
            wr(html, viewer_html(g, digest, title))
            print(f"viewer -> {html}")
        if fresh:
            return 0
        if g.unresolved:
            print("unresolved IDs (referenced, never defined):", ", ".join(sorted(g.unresolved)))
        return 0
    if cmd == "critical":
        n_top = int(flags[flags.index("--top") + 1]) if "--top" in flags else 5
        rows = critical_nodes(g, n_top)
        if "--json" in flags:
            print(json.dumps(rows, indent=1))
            return EXIT_OK
        print(f"Top {n_top} critical artifacts (cascade = items that depend on it, directly or not):")
        for k, r_ in enumerate(rows, 1):
            print(f"  {k}. {r_['id']}  cascade {r_['cascade']}  direct {r_['direct']}  {r_['label'][:50]}")
        return EXIT_OK
    if cmd == "backlog":
        rows = backlog_rows(g)
        if "--json" in flags:
            print(json.dumps(rows, indent=1))
            return 0
        if not rows:
            print("no stories in the graph")
            return 1
        for r_ in rows:
            where = r_["epic"] or ", ".join(r_["caps"]) or "-"
            print(f"{r_['id']}  {r_['name'][:50]}  [{where}]  status {r_['status']}  progress {r_['progress']} ({r_['ops']})")
            for fl in r_["flags"]:
                print(f"  ! {fl}")
        return 0
    if cmd == "plan":
        spec = argv[2].upper() if len(argv) > 2 else ""
        if spec not in g.nodes or g.nodes[spec]["req_type"] != "SPEC":
            print(f"unknown spec {spec}")
            return EXIT_NOT_FOUND
        rows = plan_rows(g, spec)
        if "--json" in flags:
            print(json.dumps({"spec": spec, "status": g.nodes[spec].get("req_status", ""), "plan": rows}, indent=1))
            return 0
        print(f"{spec} [{g.nodes[spec].get('req_status', '-')}]: {len(rows)} plan line(s), {sum(1 for r_ in rows if r_['status'] in ('Done', 'Skipped'))} closed")
        for r_ in rows:
            nxt = "  <- NEXT" if r_["ready"] else ""
            print(f"- {r_['id']} [{r_['status']}] {r_['kind']} {r_['target']}: {r_['change'][:70]}{nxt}")
            for w in r_["warnings"]:
                print(f"    ! {w}")
        return 0 if rows else 1
    if cmd == "query":
        if len(argv) < 3:
            print(__doc__)
            return EXIT_USAGE
        arg = lambda name, default: flags[flags.index(name) + 1] if name in flags else default
        text = argv[2]
        res = query(g, text, depth=int(arg("--depth", 1)), limit=int(arg("--limit", 8)),
                    types={t.strip().upper() for t in arg("--type", "").split(",") if t.strip()} or None,
                    status=arg("--status", None), weak="--weak" in flags)
        if "--json" in flags:
            print(json.dumps({"query": text, "matches": [{"id": i, "score": round(sc, 2)} for i, sc in res["matches"]],
                              "related": [{"id": i, "via": v["via"]} for i, v in res["shown"].items() if v["dist"]],
                              "links": res["links"]}, indent=1))
            return 0
        lines = [f'Query "{text}": {res["total_matches"]} match(es), {len(res["shown"]) - len(res["matches"])} related, {len(g.nodes)} nodes in graph']
        body = ["MATCHES"] + [f"- {fmt(g, i)}  {g.nodes[i]['label'].split(': ', 1)[-1][:90]}  ({g.nodes[i]['source_file']}:{g.nodes[i]['source_location']})  score {sc:.1f}" for i, sc in res["matches"]]
        rel_ = [(i, v) for i, v in res["shown"].items() if v["dist"]]
        if rel_:
            body.append("RELATED")
            body += [f"- {fmt(g, i)}  {g.nodes[i]['label'].split(': ', 1)[-1][:70]}  (via {v['via'][0]} {v['via'][1]})" for i, v in rel_]
        if res["links"]:
            body.append("LINKS")
            body += [f"- {s_} -{rel}-> {t_}" for s_, t_, rel in res["links"]]
        budget = int(arg("--budget", 1500)) * 4
        used, kept = len(lines[0]), []
        for ln in body:
            if used + len(ln) + 1 > budget and ln[0] == "-":
                continue
            used += len(ln) + 1
            kept.append(ln)
        print("\n".join(lines + kept))
        if len(kept) < len(body):
            need = (sum(len(x) + 1 for x in body) + len(lines[0])) // 4 + 1
            print(f"[!] TRUNCATED: showing {len(kept)} of {len(body)} lines; raise --budget to {need} or narrow the query (--type, --status, --depth 0)")
        return 0 if res["total_matches"] else 1
    if cmd == "path":
        if len(argv) < 4:
            print(__doc__)
            return EXIT_USAGE
        a, b = argv[2].upper(), argv[3].upper()
        for x in (a, b):
            if x not in g.nodes:
                print(f"unknown ID {x}")
                return EXIT_NOT_FOUND
        hops = shortest_path(g, a, b, directed="--directed" in flags, include_all="--all" in flags)
        if hops is None:
            print(f"no path between {a} and {b}" + ("" if "--all" in flags else " (try --all to include records and weak links)"))
            return 1
        print(f"Shortest path ({len(hops)} hop{'s' if len(hops) != 1 else ''}):")
        for p_, rel, d, c in hops:
            print(f"  {p_} --{rel}--> {c}" if d == "out" else f"  {p_} <--{rel}-- {c}")
        return 0
    if cmd == "explain":
        target = argv[2].upper() if len(argv) > 2 else ""
        if target not in g.nodes:
            print(f"unknown ID {target}")
            return EXIT_NOT_FOUND
        n = g.nodes[target]
        print(f"{label(g, target)}\n  type: {n['req_type']}  status: {n.get('req_status', '-')}\n  source: {n['source_file']}:{n['source_location']}")
        text_ = source_line(root, n)
        if text_:
            print(f"  text: {text_}")
        out_, in_ = defaultdict(list), defaultdict(list)
        for (s_, t_, rel), e in g.edges.items():
            if s_ == target:
                out_[rel].append(t_ + (f" ({e['impact']})" if e.get("impact") else ""))
            if t_ == target:
                in_[rel].append(s_)
        print("Depends on / points to:")
        for rel, xs in sorted(out_.items()):
            print(f"  {rel}: {', '.join(sorted(xs))}")
        print("Referenced by:")
        for rel, xs in sorted(in_.items()):
            print(f"  {rel}: {', '.join(sorted(xs))}")
        main_, _ = affected(g, target, depth=9, weak=False)
        print(f"Transitive dependents (strong links): {len(main_)}")
        return 0
    if cmd == "affected":
        target = argv[2].upper()
        if target not in g.nodes:
            print(f"unknown ID {target}")
            return EXIT_NOT_FOUND
        depth = int(flags[flags.index("--depth") + 1]) if "--depth" in flags else 3
        main_, side = affected(g, target, up="--up" in flags, depth=depth, weak="--no-weak" not in flags)
        if "--json" in flags:
            print(json.dumps({"target": target, "affected": main_, "sideways": side}, indent=1))
            return 0
        print(f"{'Upstream of' if '--up' in flags else 'Affected by'} {label(g, target)} (depth {depth}):")
        for m in main_:
            print(f"- {label(g, m['id'])} [{m['via']}{', weak' if m['weak'] else ''}, depth {m['depth']}]")
        if side:
            print("Sideways (share an upstream item):")
            for s in side:
                print(f"- {label(g, s['id'])} [via {s['via_shared']}]")
        return 0
    stories = {i: n for i, n in g.nodes.items() if n["req_type"] == "US"}
    if cmd == "stale":
        for i, n in stories.items():
            if n.get("req_status") == "Stale":
                print(label(g, i))
        return 0
    blockers = defaultdict(list)
    for (s, t, rel) in g.edges:
        if rel == "blocked_by":
            blockers[s].append(t)
    for i, n in stories.items():
        if n.get("req_status") in DONE or n.get("req_status") == "Stale":
            continue
        if all(stories.get(b, {}).get("req_status") in DONE for b in blockers[i]):
            print(label(g, i), f"[{n.get('req_status', 'no status')}]")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv[1:]))
    except BrokenPipeError:
        sys.exit(0)
