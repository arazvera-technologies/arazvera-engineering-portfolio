import pathlib,sys,unittest
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]))
from demo import Notes
class TestNotes(unittest.TestCase):
 def test_tenant_isolation_and_replay(self):
  n=Notes();n.create('a','x','Demo');self.assertEqual(n.list('b'),[])
  self.assertTrue(n.create('a','x','Demo')['duplicate'])
  with self.assertRaises(ValueError):n.create('a','x','Changed')
 def test_validation_and_page(self):
  n=Notes()
  with self.assertRaises(ValueError):n.create('','','')
  with self.assertRaises(ValueError):n.list('a',0)
