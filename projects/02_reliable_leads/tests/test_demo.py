import pathlib,sys,unittest
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]))
from demo import LeadDemo
class TestLead(unittest.TestCase):
 def test_dedup_and_manual_review(self):
  q=LeadDemo();q.receive('x','Synthetic',True);self.assertEqual(q.process('x','ok'),'review')
  self.assertEqual(len(q.items),1)
  with self.assertRaises(ValueError):q.receive('x','Different')
 def test_bounded_failure(self):
  q=LeadDemo();q.receive('x','Synthetic')
  self.assertEqual(q.process('x','fail',2),'queued')
  self.assertEqual(q.process('x','fail',2),'dead_letter')
