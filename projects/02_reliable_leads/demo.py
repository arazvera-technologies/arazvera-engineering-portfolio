"""Public, pure-Python mock queue: no real CRM or outbound messages."""
import json
class LeadDemo:
    def __init__(self):self.items={};self.audit=[]
    def receive(self,key,name,review=False):
        if not key or not name:raise ValueError('missing synthetic fields')
        item=self.items.get(key)
        if item:
            if item['name']!=name:raise ValueError('conflicting replay')
            return item
        item={'name':name,'state':'review' if review else 'queued','attempts':0};self.items[key]=item
        self.audit.append('accepted');return item
    def process(self,key,adapter_result,max_attempts=3):
        x=self.items[key]
        if x['state']!='queued':return x['state']
        x['attempts']+=1
        if adapter_result=='ok':x['state']='done'
        elif x['attempts']>=max_attempts:x['state']='dead_letter'
        self.audit.append(x['state']);return x['state']
if __name__=='__main__':
    q=LeadDemo();q.receive('demo-id','Synthetic visitor');q.process('demo-id','fail');q.process('demo-id','ok')
    print(json.dumps({'item':q.items['demo-id'],'external_calls':0,'production_approved':False},sort_keys=True))
