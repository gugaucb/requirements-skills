#!/usr/bin/env python3
"""Shared Markdown and ID layer for the requirements scripts (stdlib only).

One place for: the ID vocabulary and regexes, safe file I/O (utf-8, errors=replace), tolerant table
normalization (irregular spacing, missing edge pipes, escaped pipes, <br>, rows continued on the next
line), upper-casing of every ID, and [PARSE-WARNING] reporting on stderr.

Exit codes shared by every validating script (CI contract):
  0 consistent    1 orphan IDs or untested rules    2 dependency cycles
  3 critical parse or file failure    64 usage error    66 unknown target (ID, spec, file)
"""
import os
import re
import sys
from pathlib import Path

EXIT_OK, EXIT_PROBLEMS, EXIT_CYCLES, EXIT_CRITICAL, EXIT_USAGE, EXIT_NOT_FOUND = 0, 1, 2, 3, 64, 66

CANVAS = ("JUS", "OBJ", "BEN", "PRD", "RQT", "STK", "PRM", "ENT", "RSK", "TMP", "CST", "EQP", "RST")
PREFIXES = ("GOAL", "CAP", "EPIC", "SPEC", "PLN", "US", "FR", "NFR", "AC", "TC", "DG", "FLD", "SCR", "DEC", "CHG") + CANVAS
P = "|".join(PREFIXES)
ID = re.compile(rf"\b(?:{P})-\d{{3,}}\b", re.I)
BAD_ID = re.compile(rf"\b(?:{P})(?:-\d{{1,2}}|_\d+)\b(?!-)", re.I)
DEF_LINE = re.compile(rf"^(?:\|\s*(?:\*\*)?|#{{1,3}}\s+|\*\*)((?:{P})-\d{{3,}})(?:\*\*)?\s*[:|]?\s*(.*)$", re.I)

WARNINGS = []
_SEEN = set()


def _warn(rel, line, msg):
    """Record and print `[PARSE-WARNING] file:Lnn: message` on stderr (once per distinct warning)."""
    key = (rel, line, msg)
    if key in _SEEN:
        return
    _SEEN.add(key)
    WARNINGS.append(key)
    if not os.environ.get("REQ_GRAPH_QUIET"):
        print(f"[PARSE-WARNING] {rel}:L{line}: {msg}", file=sys.stderr)


warn = _warn


def reset_warnings():
    WARNINGS.clear()
    _SEEN.clear()


def rd(path):
    return Path(path).read_text(encoding="utf-8", errors="replace")


def wr(path, text):
    Path(path).write_text(text, encoding="utf-8", errors="replace")


def ids_of(text):
    """All IDs in `text`, upper-cased, in order."""
    return [m.upper() for m in ID.findall(text)]


def upper_ids(text):
    return ID.sub(lambda m: m.group(0).upper(), text)


_PIPE = re.compile(r"(?<!\\)\|")


def split_row(line):
    """Cells of a table row. Tolerates edge pipes, irregular spacing, escaped pipes and <br>."""
    s = line.strip()
    if s.startswith("|"):
        s = s[1:]
    if s.endswith("|") and not s.endswith("\\|"):
        s = s[:-1]
    out = []
    for c in _PIPE.split(s):
        c = re.sub(r"<br\s*/?>", " ", c.replace("\\|", "|"), flags=re.I)
        out.append(re.sub(r"\s+", " ", c).strip())
    return out


def is_sep(line):
    s = line.strip()
    return bool(s) and "-" in s and set(s) <= set("|-: ")


def load_lines(path, rel, report=True):
    """Read a Markdown file and return (lines, numbers) normalized for the parsers.

    - IDs are upper-cased everywhere (fr-003 and FR-003 are the same artifact).
    - A table row that is continued on following lines is joined into one row.
    - A body row that lost its leading pipe inside a table gets it back.
    - Malformed rows and IDs are reported with [PARSE-WARNING] instead of being skipped silently.
    """
    raw = rd(path)
    warn = _warn if report else (lambda *a, **k: None)
    if "\ufffd" in raw:
        warn(rel, 1, "file contains bytes that are not valid UTF-8 (replaced)")
    src = raw.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    lines, numbers = [], []
    in_fence, in_table, ncols, header_seen, i = False, False, 0, False, 0
    while i < len(src):
        line, n = src[i], i + 1
        i += 1
        if line.strip().startswith("```"):
            in_fence = not in_fence
            lines.append(line)
            numbers.append(n)
            in_table = False
            continue
        if in_fence:
            lines.append(upper_ids(line))
            numbers.append(n)
            continue
        s = line.strip()
        looks_row = s.startswith("|") or (in_table and s.count("|") >= 2 and not s.startswith("#"))
        if looks_row:
            if not s.startswith("|"):
                line, s = "| " + s, "| " + s
                warn(rel, n, "table row without leading pipe (repaired)")
            joined = 0
            while not (s.endswith("|") and not s.endswith("\\|")) and i < len(src) and joined < 8:
                nxt = src[i].strip()
                if not nxt or nxt.startswith("#"):
                    break
                line = line.rstrip() + " " + nxt
                s = line.strip()
                i += 1
                joined += 1
            if joined and not s.endswith("|"):
                warn(rel, n, "table row is not closed by a pipe after joining continuation lines")
            if is_sep(s):
                in_table = True
                header_seen = True
            else:
                cs = split_row(s)
                if in_table and header_seen and ncols and len(cs) != ncols:
                    warn(rel, n, f"row has {len(cs)} cells but the header has {ncols}")
                if not in_table:
                    ncols = len(cs)
                    header_seen = False
                    in_table = True
                else:
                    header_seen = True
        else:
            if s == "" or s.startswith("#"):
                in_table = False
                ncols = 0
            elif in_table and not looks_row:
                in_table = False
        for m in BAD_ID.finditer(line):
            warn(rel, n, f"malformed ID '{m.group(0)}' (expected PREFIX-NNN with at least 3 digits)")
        lines.append(upper_ids(line))
        numbers.append(n)
    return lines, numbers


def find_cycles_adj(adj, nodes):
    """Directed cycles of `adj` (node -> iterable of nodes) by iterative DFS with three colors (white, grey, black).
    Each cycle is returned once, rotated to start at its smallest node and closed (first node repeated)."""
    WHITE, GREY, BLACK = 0, 1, 2
    color = {i: WHITE for i in nodes}
    cycles, seen = [], set()
    for root in sorted(nodes):
        if color[root] != WHITE:
            continue
        stack, path = [(root, iter(sorted(adj.get(root, []))))], [root]
        color[root] = GREY
        while stack:
            node, it = stack[-1]
            for nxt in it:
                if nxt not in color:
                    continue
                if color[nxt] == GREY:
                    cyc = path[path.index(nxt):] + [nxt]
                    k = min(range(len(cyc) - 1), key=lambda x: cyc[x])
                    canon = tuple(cyc[k:-1] + cyc[:k] + [cyc[k]])
                    if canon not in seen:
                        seen.add(canon)
                        cycles.append(list(canon))
                elif color[nxt] == WHITE:
                    color[nxt] = GREY
                    stack.append((nxt, iter(sorted(adj.get(nxt, [])))))
                    path.append(nxt)
                    break
            else:
                color[node] = BLACK
                stack.pop()
                path.pop()
    return cycles
