import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

os.environ["REQ_GRAPH_QUIET"] = "1"  # in-process builds stay quiet; run() removes it for subprocess checks
ROOT = Path(__file__).resolve().parents[1]
RGS = ROOT / "skills/requirements/graph-sync/scripts/req-graph.py"
CHK = ROOT / "skills/requirements/audit-traceability/scripts/check-ids.py"
CANVAS = ROOT / "skills/requirements/project-canvas/scripts/canvas-check.py"
EXAMPLE = ROOT / "examples/order-status-portal"
spec = importlib.util.spec_from_file_location("req_graph", RGS)
rg = importlib.util.module_from_spec(spec)
spec.loader.exec_module(rg)

VISION = "| GOAL-001 | g |\n| CAP-001 | c | GOAL-001 |\n"
STORY = """# US-001: first

**Serves:** CAP-001

## Functional requirements

| ID | Behavior | Source |
| --- | --- | --- |
| FR-001 | does a thing | |

## Acceptance criteria

**AC-001**
```gherkin
Scenario: ok
```

## Test scenarios

| ID | Setup |
| --- | --- |
| TC-001 | x |

## Canonical traceability

| US | Requirement | AC | TC |
| --- | --- | --- | --- |
| US-001 | FR-001 | AC-001 | TC-001 |
"""


def project(files):
    d = tempfile.TemporaryDirectory()
    root = Path(d.name)
    for rel, text in files.items():
        f = root / rel
        f.parent.mkdir(parents=True, exist_ok=True)
        if isinstance(text, bytes):
            f.write_bytes(text)
        else:
            f.write_text(text, encoding="utf-8")
    return d, root


def run(script, *args, **env):
    e = {k: v for k, v in os.environ.items() if k != "REQ_GRAPH_QUIET"}
    e.update(env)
    return subprocess.run([sys.executable, str(script), *map(str, args)], capture_output=True, text=True, env=e)


class ExitCodes(unittest.TestCase):
    def test_clean_project_is_zero(self):
        d, root = project({"01-vision/PRODUCT-VISION.md": VISION, "04-stories/US-001.md": STORY})
        with d:
            r = run(RGS, "validate", root)
            self.assertEqual(0, r.returncode, r.stdout + r.stderr)
            self.assertEqual(0, run(CHK, root).returncode)

    def test_orphans_are_one(self):
        d, root = project({"01-vision/PRODUCT-VISION.md": VISION, "04-stories/US-001.md": STORY.replace("| TC-001 |", "| |", 1).replace("TC-001", "")})
        with d:
            r = run(RGS, "validate", root)
            self.assertEqual(1, r.returncode, r.stdout)
            self.assertIn("has no TC", r.stdout)

    def test_cycles_are_two(self):
        backlog = ("| Order | Capability | Story | Name | Blocked by | Status |\n| --- | --- | --- | --- | --- | --- |\n"
                   "| 1 | CAP-001 | US-001 | a | US-002 | Draft |\n| 2 | CAP-001 | US-002 | b | US-001 | Draft |\n")
        d, root = project({"01-vision/PRODUCT-VISION.md": VISION, "02-backlog/BACKLOG.md": backlog})
        with d:
            r = run(RGS, "validate", root)
            self.assertEqual(2, r.returncode, r.stdout)
            self.assertIn("cycle: US-001 -> US-002 -> US-001", r.stdout)
            self.assertEqual(2, run(CHK, root).returncode)

    def test_three_color_dfs_reports_each_cycle_once(self):
        import reqmd
        cycles = reqmd.find_cycles_adj({"A": ["B"], "B": ["C"], "C": ["A", "D"], "D": []}, ["A", "B", "C", "D"])
        self.assertEqual([["A", "B", "C", "A"]], cycles)
        self.assertEqual([], reqmd.find_cycles_adj({"A": ["B"], "B": ["C"]}, ["A", "B", "C"]))
        self.assertEqual([["A", "A"]], reqmd.find_cycles_adj({"A": ["A"]}, ["A"]))

    def test_superseded_cycle_between_changes(self):
        chg = "# CHG-001: a\n\n**Status:** Proposed\n\nSuperseded by CHG-002\n"
        chg2 = "# CHG-002: b\n\n**Status:** Proposed\n\nSuperseded by CHG-001\n"
        d, root = project({"05-changes/CHG-001.md": chg, "05-changes/CHG-002.md": chg2})
        with d:
            r = run(RGS, "validate", root)
            self.assertEqual(2, r.returncode, r.stdout)
            self.assertIn("CHG-001 -> CHG-002 -> CHG-001", r.stdout)

    def test_change_records_pointing_at_each_other_are_not_cycles(self):
        r = run(RGS, "validate", EXAMPLE)
        self.assertNotIn("cycle", r.stdout)

    def test_critical_failures_are_three(self):
        self.assertEqual(3, run(RGS, "validate", "/no/such/root").returncode)
        d, root = project({"graph/aliases.json": "{not json", "04-stories/US-001.md": STORY, "01-vision/PRODUCT-VISION.md": VISION})
        with d:
            self.assertEqual(3, run(RGS, "validate", root).returncode)
        d, root = project({"notes.md": "nothing here"})
        with d:
            self.assertEqual(3, run(RGS, "validate", root).returncode)

    def test_strict_turns_warnings_into_three(self):
        d, root = project({"01-vision/PRODUCT-VISION.md": VISION, "04-stories/US-001.md": STORY + "\nSee FR-1 here.\n"})
        with d:
            self.assertEqual(0, run(RGS, "validate", root).returncode)
            self.assertEqual(3, run(RGS, "validate", root, "--strict").returncode)

    def test_usage_and_unknown_target(self):
        self.assertEqual(64, run(RGS).returncode)
        self.assertEqual(64, run(CHK).returncode)
        self.assertEqual(66, run(RGS, "explain", EXAMPLE, "NOPE-001").returncode)
        self.assertEqual(66, run(RGS, "plan", EXAMPLE, "SPEC-999").returncode)

    def test_validate_flag_alias(self):
        self.assertEqual(run(RGS, "validate", EXAMPLE).returncode, run(RGS, "--validate", EXAMPLE).returncode)

    def test_canvas_cycle_is_two(self):
        canvas = ("| ID | Item | Traces to |\n| --- | --- | --- |\n| JUS-001 | a | |\n| OBJ-001 | b | JUS-001, ENT-001 |\n"
                  "| ENT-001 | c | OBJ-001 |\n")
        d, root = project({"00-canvas/PROJECT-CANVAS.md": canvas})
        with d:
            r = run(CANVAS, root / "00-canvas/PROJECT-CANVAS.md", "--no-judgment")
            self.assertEqual(2, r.returncode, r.stdout)
            self.assertIn("Trace cycle", r.stdout)


class TolerantParsing(unittest.TestCase):
    def test_ids_are_case_insensitive_and_normalized(self):
        story = STORY.replace("US-001", "us-001").replace("FR-001", "fr-001").replace("AC-001", "Ac-001").replace("TC-001", "tc-001")
        d, root = project({"01-vision/PRODUCT-VISION.md": VISION.replace("GOAL", "goal"), "04-stories/US-001.md": story})
        with d:
            g, _ = rg.build(root)
            self.assertTrue({"US-001", "FR-001", "AC-001", "TC-001", "GOAL-001"} <= set(g.nodes))
            self.assertEqual(0, run(RGS, "validate", root).returncode)

    def test_irregular_tables_are_tolerated_and_reported(self):
        story = STORY.replace("| FR-001 | does a thing | |", "fr-001|   does   a    thing |\n|   FR-002| has a pipe \\| inside and<br>a break |\n| FR-003 | row that\n   continues here |")
        d, root = project({"01-vision/PRODUCT-VISION.md": VISION, "04-stories/US-001.md": story})
        with d:
            r = run(RGS, "build", root, "--force", "--out", root / "g.json")
            g, _ = rg.build(root)
            self.assertTrue({"FR-001", "FR-002", "FR-003"} <= set(g.nodes), sorted(g.nodes))
            self.assertIn("[PARSE-WARNING]", r.stderr)
            self.assertIn("without leading pipe", r.stderr)

    def test_malformed_rows_and_ids_warn_on_stderr(self):
        story = STORY + "\nBroken reference TC-9 and a bad one FR_12.\n"
        story = story.replace("| TC-001 | x |", "| TC-001 | x | extra |")
        d, root = project({"01-vision/PRODUCT-VISION.md": VISION, "04-stories/US-001.md": story})
        with d:
            r = run(RGS, "validate", root)
            self.assertIn("malformed ID 'TC-9'", r.stderr)
            self.assertIn("malformed ID 'FR_12'", r.stderr)
            self.assertIn("row has 3 cells but the header has 2", r.stderr)
            self.assertTrue(all(l.startswith("[PARSE-WARNING] ") for l in r.stderr.splitlines()))

    def test_invalid_utf8_is_replaced_not_fatal(self):
        d, root = project({"01-vision/PRODUCT-VISION.md": VISION.encode() + b"\xff\xfe broken bytes\n", "04-stories/US-001.md": STORY})
        with d:
            r = run(RGS, "validate", root)
            self.assertEqual(0, r.returncode, r.stdout + r.stderr)
            self.assertIn("not valid UTF-8", r.stderr)

    def test_quiet_env_suppresses_printing(self):
        d, root = project({"01-vision/PRODUCT-VISION.md": VISION, "04-stories/US-001.md": STORY + "\nFR-1\n"})
        with d:
            self.assertEqual("", run(RGS, "validate", root, REQ_GRAPH_QUIET="1").stderr)


class Metrics(unittest.TestCase):
    def test_top_critical_artifacts(self):
        res = rg.validate(EXAMPLE)
        self.assertEqual(5, len(res["top"]))
        self.assertEqual("JUS-001", res["top"][0]["id"])
        self.assertTrue(all(res["top"][k]["cascade"] >= res["top"][k + 1]["cascade"] for k in range(4)))
        self.assertNotIn("CHG-001", [r["id"] for r in res["top"]])
        out = json.loads(run(RGS, "critical", EXAMPLE, "--top", "3", "--json").stdout)
        self.assertEqual(3, len(out))
        self.assertIn("Top 5 critical artifacts", run(RGS, "validate", EXAMPLE).stdout)


class Lifecycle(unittest.TestCase):
    def test_frontmatter_status_and_version(self):
        fm = "---\nid: US-001\nstatus: review   # lifecycle\nversion: 1.2.0\n---\n"
        story = fm + STORY + "\n**Status:** Ready for human review\n"
        d, root = project({"01-vision/PRODUCT-VISION.md": VISION, "04-stories/US-001.md": story})
        with d:
            r = run(RGS, "validate", root)
            self.assertNotIn("does not match", r.stderr)
            g, _ = rg.build(root)
            self.assertEqual("review", g.nodes["US-001"]["lifecycle"])
            self.assertEqual("1.2.0", g.nodes["US-001"]["version"])

    def test_mismatch_and_bad_values_warn(self):
        fm = "---\nid: US-001\nstatus: approved\nversion: 1.2\n---\n"
        d, root = project({"01-vision/PRODUCT-VISION.md": VISION, "04-stories/US-001.md": fm + STORY + "\n**Status:** Draft\n"})
        with d:
            err = run(RGS, "validate", root).stderr
            self.assertIn("does not match Status 'Draft' (expected 'draft')", err)
            self.assertIn("version '1.2' is not X.Y.Z", err)

    def test_example_headers_are_consistent(self):
        g, _ = rg.build(EXAMPLE)
        self.assertEqual("approved", g.nodes["SPEC-001"]["lifecycle"])
        self.assertEqual("1.1.0", g.nodes["US-001"]["version"])
        self.assertEqual("", run(RGS, "validate", EXAMPLE).stderr)


class ViewerSanitization(unittest.TestCase):
    def test_payload_has_no_markup_characters_and_round_trips(self):
        evil = "</script><img src=x onerror=alert(1)> & <!-- \u2028 \"quote\" \\"
        d, root = project({"01-vision/PRODUCT-VISION.md": "| GOAL-001 | " + evil + " |\n"})
        with d:
            g, digest = rg.build(root)
            html = rg.viewer_html(g, digest, evil)
            data = html.split('type="application/json">', 1)[1].split("</script>", 1)[0]
            for ch in "<>&":
                self.assertNotIn(ch, data)
            payload = json.loads(data)
            self.assertIn("</script>", payload["nodes"][0]["label"])
            self.assertEqual(evil, payload["title"])
            self.assertTrue(data.isascii())

    def test_viewer_needs_no_network(self):
        import re
        g, digest = rg.build(EXAMPLE)
        urls = set(re.findall(r"https?://[^\"' <]+", rg.viewer_html(g, digest, "t")))
        self.assertEqual({"http://www.w3.org/2000/svg"}, urls)


if __name__ == "__main__":
    unittest.main()
