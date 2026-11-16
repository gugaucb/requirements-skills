import subprocess
import sys
import unittest
from pathlib import Path

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
            (root / "stories").mkdir()
            (root / "PRODUCT-VISION.md").write_text("| CAP-001 | x |\n")
            story = "# US-001: a\n\n| ID | B |\n| --- | --- |\n| FR-001 | x |\n| FR-002 | y |\n\n**AC-001**\n\n## Canonical traceability\n\n| US | R | AC | TC | C |\n| --- | --- | --- | --- | --- |\n| US-001 | FR-001 | AC-001 | | x |\n\nSee CAP-009\n"
            (root / "stories" / "US-001.md").write_text(story)
            (root / "stories" / "US-002.md").write_text("# US-002: b\n\n| FR-001 | dup |\n\n## Canonical traceability\n\n| US | R | AC | TC |\n| --- | --- | --- | --- |\n| US-002 | FR-001 | AC-009 | TC-009 |\n")
            problems, _ = check_ids.check(root)
            text = "\n".join(problems)
            self.assertIn("Duplicate definition FR-001", text)
            self.assertIn("Dangling reference CAP-009", text)
            self.assertIn("FR-002 has no AC", text)
            self.assertIn("AC-001 has no TC", text)


if __name__ == "__main__":
    unittest.main()
