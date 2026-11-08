"""Public stand-alone mock connectors: no customer API calls."""
import hashlib,hmac,json
class DemoGateway:
 def __init__(self,key=b'test-only-key'):
  self.key=key;self.calls=[]
 def signature(self,body):return hmac.new(self.key,body,hashlib.sha256).hexdigest()
 def check(self,body,sig):return hmac.compare_digest(self.signature(body),sig)
 def send(self,name,payload):
  if name not in ('inventory','crm'):raise ValueError('unknown mock adapter')
  if not isinstance(payload,dict):raise ValueError('invalid payload')
  self.calls.append(name)
  return {'status':200,'adapter':name,'synthetic':True}
if __name__=='__main__':
 g=DemoGateway();print(json.dumps({'inventory':g.send('inventory',{'sku':'FAKE'}),'crm':g.send('crm',{'lead':'FAKE'}),'outbound_network_calls':0},sort_keys=True))
