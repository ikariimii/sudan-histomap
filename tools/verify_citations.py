# Headless check: open the info panel for every period (EN+AR) and look for unresolved source IDs.
# Load-safe: at most MAXJ Chrome renders at once (default 2), per-render timeout, each Chrome in its own
# process group with a throwaway profile; the whole group is killed on timeout, error, or exit.
import json,subprocess,re,os,urllib.parse,signal,tempfile,shutil,atexit,sys
from concurrent.futures import ThreadPoolExecutor
MAXJ=int(os.environ.get('VC_JOBS','2')); TMO=int(os.environ.get('VC_TIMEOUT','45'))
P=json.loads(open('data/periods.js').read().split('=',1)[1].rstrip().rstrip(';'))['periods']
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
with ThreadPoolExecutor(MAXJ) as ex:
    R=list(ex.map(run,[(p,l) for p in P for l in ('en','ar')]))
bad=[r for r in R if r[4] or r[2]!=r[3] or not r[5]]
print(len(R),'checks; problems:',len(bad),'(jobs=%d, timeout=%ds)'%(MAXJ,TMO))
for b in bad: print(b)
