import unittest,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from validate_repository import check
class ContractTests(unittest.TestCase):
 def test_repository(self):self.assertEqual([],check())
 def test_manual_gates(self):
  for n in ('setup-requirements-repo','create-product-vision'):
   self.assertIn('disable-model-invocation: true',(ROOT/'.agents/skills'/n/'SKILL.md').read_text())
 def test_shared_vocabulary(self):self.assertIn('Definition of Done',(ROOT/'docs/VOCABULARY.md').read_text())
 def test_vision_template(self):self.assertIn('CAP-001',(ROOT/'templates/PRODUCT-VISION.md').read_text())
 def test_activation_doc(self):self.assertIn('activate_skill',(ROOT/'docs/SKILL-ACTIVATION.md').read_text())
