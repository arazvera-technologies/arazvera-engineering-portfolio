import pathlib,sys,unittest
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]))
from demo import check
class TestConfig(unittest.TestCase):
 def test_pinned_digest(self):self.assertTrue(check({'image':'demo@sha256:'+'a'*64})['config_valid'])
 def test_tag_rejected(self):
  with self.assertRaises(ValueError):check({'image':'demo:latest'})
