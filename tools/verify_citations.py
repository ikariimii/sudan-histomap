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
    def _be_y(v):
        if isinstance(v,bool): return None
        if isinstance(v,int): return v
        m=re.match(r'^\s*(-?\d{1,4})(?:-\d|$)',str(v)) if v is not None else None
        return int(m.group(1)) if m else None
    def _be_src_list(it):
        """Accept sources:[{id,page}] (schema) or cite:{source_id,pages}|[...]|"NO-SOURCE" (Historian file)."""
        if it.get('sources'): return it['sources']
        c=it.get('cite') or it.get('cites');c=c if isinstance(c,list) else [c]
        return [dict(id=x.get('source_id'),page=x.get('pages')) for x in c if isinstance(x,dict) and x.get('source_id')]
    def _be_norm_b(b):
        b=dict(b);b['sources']=_be_src_list(b)
        a=_be_y(b.get('start',b.get('date_from',b.get('date'))));z=_be_y(b.get('end',b.get('date_to')));b['start']=a;b['end']=z if z is not None else a
        d=b.get('date') or ''
        if not b.get('date_text_en') and re.match(r'^-?\d{1,4}-\d',str(d)): b['date_text_en']=str(d)
        b.setdefault('place_precision',b.get('precision'))
        b['sides']=[x if isinstance(x,dict) else dict(en=x) for x in b.get('sides') or []]
        return b
    def _be_norm_ev(doc):
        """era_events.json: {events:[...]} (schema) or {era_id:[{date,en,ar,cite}], meta} (Historian file)."""
        if isinstance(doc.get('events'),list): return [dict(v,sources=_be_src_list(v)) for v in doc['events']]
        out=[]
        for k,L in doc.items():
            if k=='meta' or not isinstance(L,list): continue
            for j,v in enumerate(L):
                if v.get('removed'): continue
                out.append(dict(id=v.get('id') or f'{k}#{j}',era_id=k,year=_be_y(v.get('year',v.get('date'))),year_end=_be_y(v.get('year_end')),approx=v.get('approx'),
                    text_en=v.get('text_en',v.get('en')),text_ar=v.get('text_ar',v.get('ar')),place=v.get('place'),sources=_be_src_list(v)))
        return out

    # battles layer + era events timeline (data/battles.json, data/era_events.json; VC_STUB=1 checks data/_stub/ instead, allowing STUB_EXAMPLE)
    warn=[];info=[]
    DESCRIPTIVE_KEPT={'dinka-jieng-communities#0','dinka-jieng-communities#1','nuer-naath-communities#1','nuer-naath-communities#2','anuak-anywaa-communities#1'}  # IM ruling 2026-10-25
    stub=os.environ.get('VC_STUB')=='1';bd='data/_stub/' if stub else 'data/';EIDS={os.path.basename(f)[:-5] for f in glob.glob('data/eras/*.json')}
    def be(kind,it):
        nonlocal n
        ss=it.get('sources') or []
        if not ss: warn.append((kind,it.get('id'),'no cite - dropped at build')); return
        for c in ss:
            n+=1; sid=c.get('id') if isinstance(c,dict) else c; pg=str((c.get('page') if isinstance(c,dict) else '') or '')
            if sid not in REG and not (stub and sid=='STUB_EXAMPLE'): bad.append((kind+'-unregistered',it.get('id'),sid))
            if re.match(r'^p{1,2}\.',pg) and not re.search(r'[0-9ivxlc]',pg): bad.append((kind+'-page-format',it.get('id'),pg))
    if os.path.isfile(bd+'battles.json'):
        for b in map(_be_norm_b,json.load(open(bd+'battles.json',encoding='utf-8')).get('battles') or []):
            be('battle',b); n+=1
            if not isinstance(b.get('start'),int) or not isinstance(b.get('end',b.get('start')),int) or b.get('end',b.get('start'))<b.get('start',0): bad.append(('battle-dates',b.get('id'),''))
            if b.get('precision')!='region' and not all(isinstance(b.get(k),(int,float)) for k in ('lon','lat')): bad.append(('battle-lonlat',b.get('id'),''))
            for x in b.get('era_ids') or []:
                if x not in EIDS: bad.append(('battle-era',b.get('id'),x))
            im=b.get('image')
            if im and im.get('src') and not im.get('credit'): bad.append(('battle-image-no-credit',b.get('id'),im.get('src')))
    if os.path.isfile(bd+'era_events.json'):
        for v in _be_norm_ev(json.load(open(bd+'era_events.json',encoding='utf-8'))):
            be('event',v); n+=1
            if v.get('era_id') not in EIDS: bad.append(('event-era',v.get('id'),v.get('era_id')))
            if not isinstance(v.get('year'),int):
                if v.get('id') in DESCRIPTIVE_KEPT: info.append(('event',v.get('id'),'descriptive, kept by ruling (IM 2026-10-25)'))
                else: warn.append(('event',v.get('id'),'no year - dropped at build'))
    [print('  INFO',*w) for w in info]
    if warn: print('battles/events warnings (not failures; these items are left out of the build):',len(warn));[print('  WARN',*w) for w in warn]
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
