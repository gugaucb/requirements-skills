#!/usr/bin/env python3
"""check-ids.py: traceability check for requirements artifacts (stdlib only).

Kept as a stable entry point. The single implementation lives in graph-sync/scripts/req-graph.py
(`validate`), so the graph, the viewer and this check can never disagree about what an ID is.

Usage: check-ids.py <artifact-root> [--json] [--strict]
Exit codes: 0 consistent, 1 orphan IDs or untested rules (duplicate, dangling, FR without AC, AC without TC,
Stale items), 2 dependency cycles, 3 critical parse or file failure, 64 usage error.
Malformed rows and IDs are reported on stderr as [PARSE-WARNING].
"""
import importlib.util
import sys
from pathlib import Path

RG = Path(__file__).resolve().parents[2] / "graph-sync" / "scripts" / "req-graph.py"


def _load():
    if not RG.exists():
        print("check-ids.py needs the graph-sync skill next to it (graph-sync/scripts/req-graph.py)", file=sys.stderr)
        sys.exit(3)
    spec = importlib.util.spec_from_file_location("req_graph", RG)
    mod = importlib.util.module_from_spec(spec)
    sys.modules["req_graph"] = mod
    spec.loader.exec_module(mod)
    return mod


def check(root):
    """Compatibility helper: (problems, counts), cycles included as problems."""
    res = _load().validate(root)
    problems = res["problems"] + [f"Dependency cycle: {' -> '.join(c)}" for c in res["cycles"]] + res["critical"]
    return problems, res["counts"]


def main(argv):
    args = [a for a in argv if not a.startswith("--")]
    if not args:
        print(__doc__)
        return 64
    rg = _load()
    return rg.print_validation(rg.validate(args[0], strict="--strict" in argv), as_json="--json" in argv)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
