import subprocess
import sys
import os
import unittest
from pathlib import Path

os.environ["REQ_GRAPH_QUIET"] = "1"  # keep in-process parse warnings out of the test log
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "skills/requirements/audit-traceability/scripts"))
from validate_repository import check, skills  # noqa: E402
import importlib.util  # noqa: E402

spec = importlib.util.spec_from_file_location("check_ids", ROOT / "skills/requirements/audit-traceability/scripts/check-ids.py")
check_ids = importlib.util.module_from_spec(spec)
spec.loader.exec_module(check_ids)


class RepositoryContract(unittest.TestCase):
    def test_repository(self):
        self.assertEqual([], check())

    def test_user_invoked_set(self):
        manual = {n for n, (_, _, fm) in skills().items() if fm.get("disable-model-invocation") == "true"}
        for n in ("ask-req", "wayfinder", "grill-me", "grill-with-docs", "setup-requirements-repo", "create-product-vision"):
            self.assertIn(n, manual)
        for n in ("grilling", "impact-analysis", "audit-traceability"):
            self.assertNotIn(n, manual)

    def test_change_mode_documented(self):
        self.assertIn("impact round", (ROOT / "skills/productivity/grilling/SKILL.md").read_text())

    def test_screens_and_versioning_are_wired(self):
        tpl = (ROOT / "skills/requirements/write-user-story/USER-STORY-TEMPLATE.md").read_text()
        self.assertIn("## Fields", tpl)
        self.assertIn("## Screens", tpl)
        self.assertLess(tpl.index("## Fields"), tpl.index("## Screens"))
        self.assertIn("Decide Screens", (ROOT / "skills/requirements/write-user-story/SKILL.md").read_text())
        setup = (ROOT / "skills/requirements/setup-requirements-repo/SKILL.md").read_text()
        for needle in ("**G. Versioning.**", "git local", "git remote", "Screens policy"):
            self.assertIn(needle, setup)
        self.assertIn("Screens policy", (ROOT / "skills/requirements/setup-requirements-repo/requirements-workflow.md").read_text())

    def test_agent_manifests(self):
        import re
        S = skills()
        for n, (f, text, fm) in S.items():
            y = (f.parent / "agents" / "agent.yaml").read_text(encoding="utf-8", errors="replace")
            self.assertIn(f'name: "{n}"', y)
            inv = "user" if fm.get("disable-model-invocation") == "true" else "model"
            self.assertIn(f"invocation: {inv}", y)
            self.assertIn("requires:", y)
            for nxt in re.findall(r'^  - "([a-z][a-z0-9-]+)"$', y.split("next_steps:")[1].split("mcp_tool:")[0], re.M):
                self.assertIn(nxt, S, f"{n}: next_steps names unknown skill {nxt}")
            schema = re.search(r"inputSchema: (\{.*\})", y).group(1)
            self.assertEqual("object", __import__("json").loads(schema)["type"])
        spec = (S["spec-req"][0].parent / "agents" / "agent.yaml").read_text(encoding="utf-8", errors="replace")
        self.assertIn("02-backlog/BACKLOG.md", spec)
        self.assertIn("shared/GLOSSARY.md", spec)
        self.assertIn('instructions: "AGENTS.md"', spec)

    def test_preflight_stops_instead_of_inventing(self):
        for n, (f, text, fm) in skills().items():
            self.assertIn("## Preflight (Pré-condições / Insumos Obrigatórios)", text, n)
        spec = skills()["spec-req"][1]
        self.assertIn("**stop**", spec)
        self.assertIn("/wayfinder", spec)

    def test_grilling_has_quick_and_exhaustive_modes(self):
        g = (ROOT / "skills/productivity/grilling/SKILL.md").read_text()
        self.assertIn("**exhaustive**", g)
        self.assertIn("**quick**", g)
        self.assertIn("quick | exhaustive", (ROOT / "skills/productivity/grill-me/SKILL.md").read_text())

    def test_every_gate_has_a_return_route(self):
        rows = [l for l in (ROOT / "skills/requirements/review-readiness/QUALITY-GATES.md").read_text().splitlines() if l.startswith("| G")]
        self.assertGreaterEqual(len(rows), 10)
        for r in rows:
            self.assertTrue(r.rstrip("|").split("|")[-1].strip(), r)

    def test_validation_skills_demand_evidence(self):
        for n in ("project-canvas", "audit-traceability", "review-readiness", "review-spec"):
            t = skills()[n][1]
            self.assertIn("**before** you write your answer", t, n)
            self.assertIn("Unverified", t, n)

    def test_adapters_in_sync(self):
        r = subprocess.run([sys.executable, str(ROOT / "scripts/sync_adapters.py"), "--check"])
        self.assertEqual(0, r.returncode)


class TraceabilityScript(unittest.TestCase):
    def test_example_only_reports_stale(self):
        problems, counts = check_ids.check(ROOT / "examples/order-status-portal")
        self.assertTrue(problems and all(x.startswith("Stale item") for x in problems), problems)
        self.assertEqual(2, counts["US"])

    def test_detects_duplicates_dangling_and_gaps(self):
        import tempfile
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / "04-stories").mkdir()
            (root / "PRODUCT-VISION.md").write_text("| CAP-001 | x |\n")
            story = "# US-001: a\n\n| ID | B |\n| --- | --- |\n| FR-001 | x |\n| FR-002 | y |\n\n**AC-001**\n\n## Canonical traceability\n\n| US | R | AC | TC | C |\n| --- | --- | --- | --- | --- |\n| US-001 | FR-001 | AC-001 | | x |\n\nSee CAP-009\n"
            (root / "04-stories" / "US-001.md").write_text(story)
            (root / "04-stories" / "US-002.md").write_text("# US-002: b\n\n| FR-001 | dup |\n\n## Canonical traceability\n\n| US | R | AC | TC |\n| --- | --- | --- | --- |\n| US-002 | FR-001 | AC-009 | TC-009 |\n")
            problems, _ = check_ids.check(root)
            text = "\n".join(problems)
            self.assertIn("Duplicate definition FR-001", text)
            self.assertIn("Dangling reference CAP-009", text)
            self.assertIn("FR-002 has no AC", text)
            self.assertIn("AC-001 has no TC", text)


if __name__ == "__main__":
    unittest.main()
