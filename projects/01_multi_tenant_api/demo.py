"""Original public synthetic tenant isolation demonstration (no HTTP server)."""
import json
class Notes:
    def __init__(self):self.rows={};self.counter=0
    def create(self,tenant,request_id,title):
        if not tenant or not request_id or not title:raise ValueError('required input')
        key=(tenant,request_id)
        if key in self.rows:
            if self.rows[key]['title']!=title:raise ValueError('idempotency conflict')
            return {**self.rows[key], 'duplicate':True}
        self.counter+=1;row={'id':self.counter,'tenant':tenant,'title':title};self.rows[key]=row
        return {**row,'duplicate':False}
    def list(self,tenant,limit=10):
        if not 1<=limit<=100:raise ValueError('invalid page size')
        return [r for (t,_),r in self.rows.items() if t==tenant][:limit]
if __name__=='__main__':
    demo=Notes();first=demo.create('tenant-a','fake-001','Example task')
    print(json.dumps({'created':first,'tenant_b_items':demo.list('tenant-b'),'production_approved':False},sort_keys=True))
