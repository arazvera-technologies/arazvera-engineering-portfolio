import pathlib,sys,unittest
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]))
from demo import ReviewFirstDemo
class TestIntake(unittest.TestCase):
 def test_unknown_goes_to_human(self):self.assertEqual(ReviewFirstDemo().decide('not sure')['status'],'manual_review')
 def test_mock_never_calls_provider(self):self.assertEqual(ReviewFirstDemo().decide('hello')['provider'],'local-rule-mock')
