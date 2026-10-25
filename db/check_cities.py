#!/usr/bin/env python3
"""Check db/cities.json: source_ids in registry (data/periods.js meta.sources ∪ db/lens_*.json meta.sources,
which research_patch Pass 9 merges), era_ids exist in data/eras, coords in regional bbox, no duplicate QIDs/ids;
first_attested {year,badge FIRST_ATTESTED,source_id,page,basis} kept separate from founded; map_from = founded else first_attested, else list_only_reason;
last_attested {year,badge LAST_ATTESTED[+APPROXIMATE|+CONTESTED],source_id,page,basis} required (or null + last_attested_reason) on ruins with no abandoned year and no role end."""
import json,glob,os,sys
root=sys.argv[1] if len(sys.argv)>1 else os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
t=open(os.path.join(root,'data/periods.js')).read()
reg=set(json.loads(t[t.index('=')+1:t.rstrip().rindex(';')])['meta']['sources'])
for f in glob.glob(os.path.join(root,'db/lens_*.json')):
    reg|=set(json.load(open(f)).get('meta',{}).get('sources',{}))
eras={os.path.basename(f)[:-5] for f in glob.glob(os.path.join(root,'data/eras/*.json'))}-{'all','index','comparison'}
P=json.load(open(os.path.join(root,'db/cities.json')))['places']
bad=[];seenq={};seeni=set()
B=dict(lat=(-5,37),lon=(10,45));BADGES={'ATTESTED','APPROXIMATE','CONTESTED'};ROLES={'capital','trade','port','religious','garrison','town','cult_centre','political_centre'}
def src(r,x,w):
    if x.get('source_id') not in reg: bad.append(f"{r['id']}: {w} source {x.get('source_id')} not in registry")
    if not x.get('page'): bad.append(f"{r['id']}: {w} missing page")
for r in P:
    i=r['id']
    if i in seeni: bad.append(f'dup id {i}')
    seeni.add(i)
    q=r.get('wikidata')
    if q is None:
        if r.get('coord_source',{}).get('source_id')=='WIKIDATA_CITIES': bad.append(f'{i}: null QID but coords cite Wikidata')
    else:
        if not q.startswith('Q'): bad.append(f'{i}: bad QID')
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
    fa=r.get('first_attested')
    if fa is not None:
        if fa.get('badge')!='FIRST_ATTESTED': bad.append(f'{i}: first_attested badge must be FIRST_ATTESTED')
        if not isinstance(fa.get('year'),int): bad.append(f'{i}: first_attested without integer year')
        if not fa.get('basis'): bad.append(f'{i}: first_attested without basis')
        src(r,fa,'first_attested')
    mf=r.get('map_from')
    exp=({'year':f['year'],'basis':'founded'} if f else {'year':fa['year'],'basis':'first_attested'} if fa else None)
    if mf!=exp: bad.append(f'{i}: map_from {mf} != expected {exp}')
    if not f and not fa and not r.get('list_only_reason'): bad.append(f'{i}: list-only place without list_only_reason')
    if (f or fa) and r.get('list_only_reason'): bad.append(f'{i}: list_only_reason on a dated place')
    hs=r.get('history_source')
    if hs: src(r,hs,'history')
    a=r.get('abandoned')
    if isinstance(a,dict):
        if a.get('year') is None and not a.get('reason'): bad.append(f'{i}: abandoned without year or reason')
        if a.get('year') is not None: src(r,a,'abandoned')
    la=r.get('last_attested','__absent__')
    undated_ruin=isinstance(a,dict) and a.get('year') is None and not any(ro.get('end') is not None for ro in r.get('roles',[]))
    if undated_ruin and la=='__absent__': bad.append(f'{i}: undated ruin without last_attested field')
    if la not in (None,'__absent__'):
        if not undated_ruin: bad.append(f'{i}: last_attested only for ruins with no abandoned year and no role end')
        bg=str(la.get('badge','')).split('+')
        if bg[0]!='LAST_ATTESTED' or any(b not in ('APPROXIMATE','CONTESTED') for b in bg[1:]): bad.append(f'{i}: bad last_attested badge {la.get("badge")}')
        if not isinstance(la.get('year'),int): bad.append(f'{i}: last_attested without integer year')
        if not la.get('basis'): bad.append(f'{i}: last_attested without basis')
        src(r,la,'last_attested')
        if mf and la.get('year') is not None and isinstance(la.get('year'),int) and la['year']<mf['year']: bad.append(f'{i}: last_attested {la["year"]} before map_from {mf["year"]}')
    if la is None and not r.get('last_attested_reason'): bad.append(f'{i}: null last_attested without last_attested_reason')
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
