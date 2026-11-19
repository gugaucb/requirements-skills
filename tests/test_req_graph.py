import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills/requirements/graph-sync/scripts/req-graph.py"
EXAMPLE = ROOT / "examples/order-status-portal"

spec = importlib.util.spec_from_file_location("req_graph", SCRIPT)
rg = importlib.util.module_from_spec(spec)
spec.loader.exec_module(rg)
spec2 = importlib.util.spec_from_file_location("check_ids", ROOT / "skills/requirements/audit-traceability/scripts/check-ids.py")
ci = importlib.util.module_from_spec(spec2)
spec2.loader.exec_module(ci)


def rels(g):
    return {(s, t, r) for (s, t, r) in g.edges}


class ReqGraph(unittest.TestCase):
    def setUp(self):
        self.g, self.digest = rg.build(EXAMPLE)

    def test_nodes_agree_with_check_ids(self):
        defs, _, _, _ = ci.analyse(EXAMPLE)
        self.assertEqual(set(defs), set(self.g.nodes))

    def test_no_unresolved_in_example(self):
        self.assertEqual(set(), self.g.unresolved)

    def test_direction_rule(self):
        e = rels(self.g)
        self.assertIn(("FR-003", "US-001", "part_of"), e)
        self.assertIn(("AC-003", "FR-003", "verifies"), e)
        self.assertIn(("TC-003", "AC-003", "proves"), e)
        self.assertIn(("FR-003", "DEC-003", "decided_by"), e)
        self.assertIn(("US-002", "US-001", "blocked_by"), e)
        self.assertIn(("US-001", "CAP-001", "serves"), e)
        self.assertIn(("CAP-001", "GOAL-001", "serves"), e)

    def test_fields_and_screens(self):
        e = rels(self.g)
        self.assertIn(("FLD-002", "US-001", "part_of"), e)
        self.assertIn(("SCR-001", "US-001", "part_of"), e)
        self.assertIn(("SCR-001", "FLD-002", "uses"), e)
        self.assertIn(("FLD-002", "DEC-003", "decided_by"), e)
        main, _ = rg.affected(self.g, "FLD-002", depth=1, weak=False)
        self.assertEqual({"SCR-001"}, {m["id"] for m in main})

    def test_decisions_affected_ids_are_reversed(self):
        self.assertIn(("US-002", "DEC-003", "decided_by"), rels(self.g))

    def test_affected_is_downstream_and_sideways(self):
        main, side = rg.affected(self.g, "DEC-003", depth=3)
        ids = {m["id"] for m in main}
        self.assertTrue({"US-001", "US-002", "FR-003", "AC-003", "TC-003"} <= ids)
        self.assertNotIn("DEC-003", ids)
        main, side = rg.affected(self.g, "FR-002", depth=1, weak=False)
        self.assertEqual({"AC-002"}, {m["id"] for m in main})
        main, side = rg.affected(self.g, "FR-002", depth=2, weak=False)
        self.assertEqual({"AC-002", "TC-002"}, {m["id"] for m in main})
        main, _ = rg.affected(self.g, "FR-002", depth=2)  # weak links included: the field whose rule cites it
        self.assertIn("FLD-001", {m["id"] for m in main})

    def test_upstream(self):
        main, _ = rg.affected(self.g, "FR-003", up=True, depth=3)
        ids = {m["id"] for m in main}
        self.assertTrue({"US-001", "DEC-003", "CAP-001", "GOAL-001"} <= ids)

    def test_records_do_not_propagate(self):
        main, _ = rg.affected(self.g, "CHG-001", depth=3)
        self.assertEqual([], main)
        self.assertIn(("CHG-001", "US-002", "impacts"), rels(self.g))
        e = [x for k, x in self.g.edges.items() if k == ("CHG-001", "US-002", "impacts")][0]
        self.assertEqual("Needs review", e.get("impact"))

    def test_statuses(self):
        self.assertEqual("Stale", self.g.nodes["US-002"]["req_status"])
        self.assertEqual("Ready for human review", self.g.nodes["US-001"]["req_status"])
        self.assertEqual("Pending", self.g.nodes["DEC-004"]["req_status"])

    def test_cli_frontier_and_stale(self):
        out = subprocess.run([sys.executable, str(SCRIPT), "frontier", str(EXAMPLE)], capture_output=True, text=True).stdout
        self.assertIn("US-001", out)
        self.assertNotIn("US-002", out)
        out = subprocess.run([sys.executable, str(SCRIPT), "stale", str(EXAMPLE)], capture_output=True, text=True).stdout
        self.assertIn("US-002", out)

    def test_build_is_incremental_and_deterministic(self):
        with tempfile.TemporaryDirectory() as d:
            out = Path(d) / "g.json"
            cmd = [sys.executable, str(SCRIPT), "build", str(EXAMPLE), "--out", str(out)]
            first = subprocess.run(cmd, capture_output=True, text=True).stdout
            self.assertIn("nodes", first)
            snap = out.read_text()
            self.assertIn("up to date", subprocess.run(cmd, capture_output=True, text=True).stdout)
            subprocess.run(cmd + ["--force"], capture_output=True)
            self.assertEqual(snap, out.read_text())

    def test_unresolved_and_aliases(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / "graph").mkdir()
            (root / "changes").mkdir()
            (root / "PRODUCT-VISION.md").write_text("| GOAL-001 | g |\n| CAP-001 | c | GOAL-001 |\n")
            (root / "changes" / "CHG-001.md").write_text(
                "# CHG-001: x\n\n**Status:** Proposed\n\n## Impacto\n\n| ID | R | C |\n| --- | --- | --- |\n| CAP-001 | up | Needs review |\n| US-009 | down | Invalidated |\n")
            (root / "graph" / "aliases.json").write_text(json.dumps({"headings": {"impact": ["Impacto"]}}))
            g, _ = rg.build(root)
            self.assertIn(("CHG-001", "CAP-001", "impacts"), rels(g))
            self.assertIn("US-009", g.unresolved)

    def test_frontmatter_status_and_links(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / "stories").mkdir()
            (root / "PRODUCT-VISION.md").write_text("| GOAL-001 | g |\n| CAP-001 | c | GOAL-001 |\n")
            (root / "stories" / "US-001.md").write_text("---\nid: US-001\nstatus: Stale\nserves: [CAP-001]\n---\n# US-001: a\n")
            g, _ = rg.build(root)
            self.assertEqual("Stale", g.nodes["US-001"]["req_status"])
            self.assertIn(("US-001", "CAP-001", "serves"), rels(g))


def run(*args):
    return subprocess.run([sys.executable, str(SCRIPT), *args], capture_output=True, text=True)


class QueryPathExplain(unittest.TestCase):
    def setUp(self):
        self.g, _ = rg.build(EXAMPLE)

    def test_query_ranks_text_matches_first(self):
        res = rg.query(self.g, "fraud review", depth=0)
        top = [i for i, _ in res["matches"][:3]]
        self.assertEqual({"DEC-003", "FR-003", "TC-003"}, set(top))

    def test_query_typed_id_wins_and_accents_ignored(self):
        self.assertEqual("US-002", rg.query(self.g, "what blocks US-002 ?", depth=0)["matches"][0][0])
        self.assertTrue(rg.search(self.g, "órdér"))

    def test_query_filters(self):
        res = rg.query(self.g, "status", types={"AC"}, depth=0)
        self.assertTrue(res["matches"] and all(self.g.nodes[i]["req_type"] == "AC" for i, _ in res["matches"]))
        res = rg.query(self.g, "", status="Stale", depth=0)
        self.assertEqual(["US-002"], [i for i, _ in res["matches"]])

    def test_query_depth_expands_and_links_touch_matches(self):
        res = rg.query(self.g, "FR-003", depth=1)
        self.assertIn("US-001", res["shown"])
        hit = {i for i, _ in res["matches"]}
        self.assertTrue(all(s_ in hit or t_ in hit for s_, t_, _ in res["links"]))

    def test_query_cli_budget_and_exit_code(self):
        out = run("query", str(EXAMPLE), "fraud", "--budget", "40").stdout
        self.assertIn("TRUNCATED", out)
        r = run("query", str(EXAMPLE), "zzzzqq")
        self.assertEqual(1, r.returncode)
        data = json.loads(run("query", str(EXAMPLE), "fraud", "--json").stdout)
        self.assertTrue(data["matches"])

    def test_path(self):
        hops = rg.shortest_path(self.g, "TC-003", "GOAL-001")
        self.assertEqual(2, len(hops))
        self.assertIsNone(rg.shortest_path(self.g, "CHG-001", "US-002"))
        self.assertIsNotNone(rg.shortest_path(self.g, "CHG-001", "US-002", include_all=True))
        self.assertIn("2 hops", run("path", str(EXAMPLE), "TC-003", "GOAL-001").stdout)
        self.assertEqual(4, run("path", str(EXAMPLE), "NOPE-001", "GOAL-001").returncode)

    def test_explain(self):
        out = run("explain", str(EXAMPLE), "FR-003").stdout
        for needle in ("stories/US-001.md", "decided_by: DEC-003", "verifies: AC-003", "Transitive dependents (strong links): 2", "On hold"):
            self.assertIn(needle, out)


class Viewer(unittest.TestCase):
    def html(self, root=EXAMPLE):
        g, digest = rg.build(root)
        return rg.viewer_html(g, digest, "T")

    def test_self_contained_and_complete(self):
        import re
        h = self.html()
        urls = set(re.findall(r"https?://[^\"' <]+", h))
        self.assertEqual({"http://www.w3.org/2000/svg"}, urls)
        for i in ("US-001", "DEC-003", "CHG-001", "TC-003"):
            self.assertIn(i, h)
        self.assertNotIn("__DATA__", h)

    def test_deterministic(self):
        self.assertEqual(self.html(), self.html())

    def test_data_cannot_break_out_of_script(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / "PRODUCT-VISION.md").write_text("| GOAL-001 | </script><img src=x onerror=alert(1)> |\n")
            h = self.html(root)
            data = h.split('type="application/json">', 1)[1].split("</script>", 1)[0]
            self.assertNotIn("</", data)
            self.assertNotIn("<!--", data)
            self.assertIn("textContent", h)
            self.assertNotIn("innerHTML", h)

    def test_build_view_writes_and_refreshes(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d) / "p"
            root.mkdir()
            for f in EXAMPLE.rglob("*.md"):
                t = root / f.relative_to(EXAMPLE)
                t.parent.mkdir(parents=True, exist_ok=True)
                t.write_text(f.read_text())
            cmd = [sys.executable, str(SCRIPT), "build", str(root), "--view"]
            out = subprocess.run(cmd, capture_output=True, text=True).stdout
            html = root / "graph" / "req-graph.html"
            self.assertIn("viewer", out)
            self.assertTrue(html.exists())
            html.unlink()
            out = subprocess.run(cmd, capture_output=True, text=True).stdout
            self.assertIn("up to date", out)
            self.assertTrue(html.exists())
            (root / "stories" / "US-002.md").write_text((root / "stories" / "US-002.md").read_text() + "\nNote DEC-001.\n")
            subprocess.run(cmd, capture_output=True)
            self.assertIn("DEC-001", html.read_text())


class GraphifyCompat(unittest.TestCase):
    def test_native_path_agrees_on_hops(self):
        try:
            import graphify  # noqa: F401
        except ImportError:
            self.skipTest("graphifyy not installed")
        with tempfile.TemporaryDirectory() as d:
            gp = Path(d) / "g.json"
            gp.write_text(json.dumps(rg.to_json(*rg.build(EXAMPLE))))
            out = subprocess.run(["graphify", "path", "TC-003", "GOAL-001", "--graph", str(gp)], capture_output=True, text=True).stdout
        self.assertIn("2 hops", out)

    def test_schema_and_native_affected_agree(self):
        try:
            from graphify.validate import validate_extraction
        except ImportError:
            self.skipTest("graphifyy not installed")
        data = rg.to_json(*rg.build(EXAMPLE))
        self.assertEqual([], validate_extraction({"nodes": data["nodes"], "edges": data["links"]}))
        with tempfile.TemporaryDirectory() as d:
            gp = Path(d) / "req-graph.json"
            gp.write_text(json.dumps(data))
            out = subprocess.run(
                ["graphify", "affected", "DEC-003", "--graph", str(gp), "--relation", "serves", "--relation", "part_of",
                 "--relation", "decided_by", "--relation", "blocked_by", "--relation", "verifies", "--relation", "proves",
                 "--depth", "3"], capture_output=True, text=True).stdout
        main, _ = rg.affected(rg.build(EXAMPLE)[0], "DEC-003", depth=3)
        native = {t.split(":")[0].split()[-1] for t in out.splitlines() if t.startswith("- ")}
        strong = {m["id"] for m in main if not m["weak"]}
        self.assertEqual(strong - {"DEC-003"}, native)


if __name__ == "__main__":
    unittest.main()
