"""Safety gate for synthetic public artifacts. Run before every publication."""
from pathlib import Path
import argparse,hashlib,json,re,subprocess
BAD_NAMES={'.env','.env.local','id_rsa','credentials.json'}
BAD_SUFFIXES={'.bundle','.pem','.key','.zip','.sqlite','.db','.bak'}
BAD_WORDS=['D:'+chr(92)+'AERON_WORKSPACE',chr(92)+'.ssh'+chr(92)]
def audit(root):
    findings=[];rows=[]
    for p in root.rglob('*'):
        if not p.is_file() or '.git' in p.parts or '__pycache__' in p.parts:continue
        rel=p.relative_to(root).as_posix(); data=p.read_bytes()
        if p.name in BAD_NAMES or p.suffix in BAD_SUFFIXES:findings.append({'file':rel,'reason':'prohibited artifact type'})
        if p.stat().st_size>2_000_000:findings.append({'file':rel,'reason':'unreviewed large file'})
        if p.suffix in {'.md','.txt','.py','.json','.yaml','.yml'} and p.name!='public_release_audit.py':
            t=data.decode('utf-8','replace')
            for name,pattern in {'token':r'gh[pousr]_[A-Za-z0-9_]{30,}',
                'api-key':r'sk-[A-Za-z0-9_-]{20,}',
                'aws':r'AKIA[A-Z0-9]{16}',
                'private':r'-----BEGIN [A-Z ]+PRIVATE KEY-----'}.items():
                if re.search(pattern,t):findings.append({'file':rel,'reason':name})
            if any(term in t for term in BAD_WORDS):findings.append({'file':rel,'reason':'private path'})
        rows.append({'path':rel,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()})
    return {'status':'PASS' if not findings else 'BLOCKED','files_scanned':len(rows),'files':rows,'findings':findings}
def history_scan(root):
    # Include all reachable revisions, not just the latest tree.
    try:
        log=subprocess.check_output(['git','-C',str(root),'log','--all','--format=%H','--name-only'],text=True,stderr=subprocess.PIPE)
        patches=subprocess.check_output(['git','-C',str(root),'log','--all','-p','--no-ext-diff'],text=True,stderr=subprocess.PIPE)
    except subprocess.CalledProcessError as e:raise RuntimeError('Git history unavailable; do not publish') from e
    bad=[x for x in ('.env','id_rsa','.bundle','credentials.json') if any(x in line for line in log.splitlines())]
    # Secrets scanner split to avoid matching its own literal source string.
    bad += ['credential pattern'] if re.search('gh[pousr]_'+'[A-Za-z0-9_]{30,}',patches) else []
    return {'status':'PASS' if not bad else 'BLOCKED','unsafe_entries':bad,'commit_count':len([x for x in log.splitlines() if len(x)==40 and all(c in '0123456789abcdef' for c in x)])}
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--root',type=Path,default=Path('.'));ap.add_argument('--report',type=Path,required=True);ap.add_argument('--history',action='store_true');a=ap.parse_args()
    r=audit(a.root);r['history']=history_scan(a.root) if a.history else {'status':'PENDING_REMOTE_GIT_HISTORY_CHECK'}
    if r['history']['status']=='BLOCKED':r['status']='BLOCKED'
    a.report.parent.mkdir(exist_ok=True,parents=True);a.report.write_text(json.dumps(r,indent=2)+'\n')
    print(json.dumps({'status':r['status'],'files':r['files_scanned'],'findings':len(r['findings']),'history':r['history']['status']}))
    raise SystemExit(0 if r['status']=='PASS' else 2)
