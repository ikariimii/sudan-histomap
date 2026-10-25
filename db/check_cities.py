#!/usr/bin/env python3
"""Check db/cities.json: source_ids in registry (data/periods.js meta.sources ∪ db/lens_*.json meta.sources,
which research_patch Pass 9 merges), era_ids exist in data/eras, coords in regional bbox, no duplicate QIDs/ids."""
import json,glob,os,sys
root=sys.argv[1] if len(sys.argv)>1 else os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
t=open(os.path.join(root,'data/periods.js')).read()
reg=set(json.loads(t[t.index('=')+1:t.rstrip().rindex(';')])['meta']['sources'])
for f in glob.glob(os.path.join(root,'db/lens_*.json')):
    reg|=set(json.load(open(f)).get('meta',{}).get('sources',{}))
eras={os.path.basename(f)[:-5] for f in glob.glob(os.path.join(root,'data/eras/*.json'))}-{'all','index','comparison'}
P=json.load(open(os.path.join(root,'db/cities.json')))['places']
bad=[];seenq={};seeni=set()
B=dict(lat=(-1,32),lon=(10,45));BADGES={'ATTESTED','APPROXIMATE','CONTESTED'};ROLES={'capital','trade','port','religious','garrison'}
def src(r,x,w):
    if x.get('source_id') not in reg: bad.append(f"{r['id']}: {w} source {x.get('source_id')} not in registry")
    if not x.get('page'): bad.append(f"{r['id']}: {w} missing page")
for r in P:
    i=r['id']
    if i in seeni: bad.append(f'dup id {i}')
    seeni.add(i)
    q=r.get('wikidata')
    if not q or not q.startswith('Q'): bad.append(f'{i}: bad QID')
    if q in seenq: bad.append(f'{i}: dup QID {q} with {seenq[q]}')
    seenq[q]=i
    if not(B['lat'][0]<=r['lat']<=B['lat'][1] and B['lon'][0]<=r['lon']<=B['lon'][1]): bad.append(f'{i}: coords out of bbox')
    f=r.get('founded')
    if f is None:
        if not r.get('founded_reason'): bad.append(f'{i}: null founded without reason')
    else:
        if f.get('badge') not in BADGES: bad.append(f'{i}: bad badge')
        if f.get('year') is None: bad.append(f'{i}: founded object without year')
        src(r,f,'founded')
    a=r.get('abandoned')
    if isinstance(a,dict):
        if a.get('year') is None and not a.get('reason'): bad.append(f'{i}: abandoned without year or reason')
        if a.get('year') is not None: src(r,a,'abandoned')
    for ro in r.get('roles',[]):
        if ro.get('era_id') not in eras: bad.append(f"{i}: era {ro.get('era_id')} missing")
        if ro.get('role') not in ROLES: bad.append(f"{i}: bad role {ro.get('role')}")
        src(r,ro,'role')
    for s in r.get('source_ids',[]): src(r,{'source_id':s['id'],'page':s['page']},'source_ids')
    src(r,r['coord_source'],'coords')
    for k in ('name_en','name_ar','history_en','history_ar'):
        if not r.get(k): bad.append(f'{i}: missing {k}')
    for k in ('population','war_status'):
        if k in r: bad.append(f'{i}: forbidden field {k}')
for b in bad: print('PROBLEM',b)
print(f'{len(P)} places, {len(bad)} problems'); sys.exit(1 if bad else 0)
