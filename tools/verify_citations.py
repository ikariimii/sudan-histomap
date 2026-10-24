# Headless check: open the info panel for every period (EN+AR) and look for unresolved source IDs.
# Load-safe: at most MAXJ Chrome renders at once (default 2), per-render timeout, each Chrome in its own
# process group with a throwaway profile; the whole group is killed on timeout, error, or exit.
import json,subprocess,re,os,urllib.parse,signal,tempfile,shutil,atexit,sys,time,glob,argparse
# --offline: ID/registry/page-format consistency only (no Chrome). --max-seconds N: stop launching renders after N s and report partial results.
AP=argparse.ArgumentParser(); AP.add_argument('--offline',action='store_true'); AP.add_argument('--max-seconds',type=float,default=float(os.environ.get('VC_MAX_SECONDS','0')) or None); A=AP.parse_args(); T0=time.time()
from concurrent.futures import ThreadPoolExecutor
MAXJ=int(os.environ.get('VC_JOBS','2')); TMO=int(os.environ.get('VC_TIMEOUT','45'))
D=json.loads(open('data/periods.js').read().split('=',1)[1].rstrip().rstrip(';')); P=D['periods']; REG=D['meta'].get('sources',{})
PG=re.compile(r'^(|p\.\s?\S+|pp\.\s?\S+([–-]\S+)?)([,;] .*| \(.*\)| .*)?$')
def offline():
    bad=[]; n=0
    for p in P:
        for sid in p.get('sources',[]):
            n+=1
            if sid not in REG: bad.append(('unregistered',p['name'],sid))
    for f in sorted(glob.glob('data/eras/*.json')):
        if f.endswith('all.json'): continue
        e=json.load(open(f,encoding='utf-8'))
        for sid in e.get('sources',[]) or []:
            sid=sid if isinstance(sid,str) else sid.get('id')
            n+=1
            if sid not in REG: bad.append(('era-unregistered',os.path.basename(f),sid))
    for k,r in REG.items():
        n+=1
        if not isinstance(r,dict): bad.append(('bad-entry',k,'')); continue
        if not r.get('title') or not (r.get('url') or r.get('note')): bad.append(('missing-title/url',k,''))
        pg=str(r.get('pages','') or '')
        if re.match(r'^p{1,2}\.',pg) and not re.search(r'[0-9ivxlc]',pg): bad.append(('page-format',k,pg))
        if re.search(r'GHA',k) and pg=='' : pass
    print(n,'offline checks; problems:',len(bad),'(registry %d IDs)'%len(REG),flush=True)
    for b in bad: print(b,flush=True)
    sys.exit(1 if bad else 0)
if A.offline: offline()
U='file://'+os.path.abspath('index.html')
LIVE=set()
def _killall(*_):
    for pg in list(LIVE):
        try: os.killpg(pg,signal.SIGKILL)
        except ProcessLookupError: pass
    LIVE.clear()
atexit.register(_killall)
for s in (signal.SIGINT,signal.SIGTERM): signal.signal(s,lambda *a:(_killall(),sys.exit(130)))
def run(a):
    p,l=a; url=U+'?lang=%s&select=%s'%(l,urllib.parse.quote(p['name'],safe=''))
    prof=tempfile.mkdtemp(prefix='vc-chrome-')
    cmd=['google-chrome','--headless=new','--no-sandbox','--disable-gpu','--no-first-run','--disable-extensions',
         '--user-data-dir='+prof,'--allow-file-access-from-files','--virtual-time-budget=3000','--dump-dom',url]
    pr=subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.DEVNULL,text=True,start_new_session=True)
    LIVE.add(pr.pid); h=''
    try: h,_=pr.communicate(timeout=TMO)
    except subprocess.TimeoutExpired: h='__TIMEOUT__'
    finally:
        try: os.killpg(pr.pid,signal.SIGKILL)
        except ProcessLookupError: pass
        pr.wait(); LIVE.discard(pr.pid); shutil.rmtree(prof,ignore_errors=True)
    if h=='__TIMEOUT__': return l,p['name'],-1,len(p['sources']),['TIMEOUT'],False
    m=re.search(r'<div id="info">(.*?)</div></div></div>',h,re.S); i=m.group(1) if m else ''
    ol=re.search(r'<ol.*?</ol>',i,re.S); ol=ol.group(0) if ol else ''
    return l,p['name'],ol.count('<li>'),len(p['sources']),re.findall(r'<li>([^<]*) <small>\(unresolved',i),('<h3' in i)
JOBS=[(p,l) for p in P for l in ('en','ar')]; R=[]; SKIP=0
def job(a):
    if A.max_seconds and time.time()-T0>A.max_seconds: return None
    r=run(a); R.append(r)
    print('[%d/%d %.0fs] %s %s %s'%(len(R),len(JOBS),time.time()-T0,r[0],r[1],'OK' if not(r[4] or r[2]!=r[3] or not r[5]) else 'PROBLEM'),flush=True)
    return r
with ThreadPoolExecutor(MAXJ) as ex: SKIP=sum(1 for x in ex.map(job,JOBS) if x is None)
bad=[r for r in R if r[4] or r[2]!=r[3] or not r[5]]
print(len(R),'checks; problems:',len(bad),'(jobs=%d, timeout=%ds)'%(MAXJ,TMO)+(' PARTIAL: %d of %d not run (--max-seconds %g)'%(SKIP,len(JOBS),A.max_seconds) if SKIP else ''),flush=True)
for b in bad: print(b)
