import pathlib,sys,unittest
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]))
from demo import DemoGateway
class TestGateway(unittest.TestCase):
 def test_signature_and_tamper(self):
  g=DemoGateway();self.assertTrue(g.check(b'hello',g.signature(b'hello')))
  self.assertFalse(g.check(b'changed',g.signature(b'hello')))
 def test_two_synthetic_adapters(self):
  g=DemoGateway();g.send('inventory',{});g.send('crm',{})
  self.assertEqual(g.calls,['inventory','crm'])
  with self.assertRaises(ValueError):g.send('payments',{})
