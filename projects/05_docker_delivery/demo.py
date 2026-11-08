"""Public release-readiness example: validates configuration syntax, never deploys."""
import json,re
PIN=re.compile(r'^demo@sha256:[0-9a-f]{64}$')
def check(config):
 if not isinstance(config,dict) or not PIN.fullmatch(config.get('image','')):
  raise ValueError('reviewed immutable demo image digest required')
 return {'config_valid':True,'production_approved':False,'deployment_started':False}
if __name__=='__main__':print(json.dumps(check({'image':'demo@sha256:'+'a'*64}),sort_keys=True))
