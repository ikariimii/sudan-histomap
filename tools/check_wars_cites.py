#!/usr/bin/env python3
"""Analyst check: every cite source ID in db/wars_post1956.json must be registered in the source registry
(data/periods.js meta.sources, the same registry verify_citations.py reads). Read-only.
Collects source_id from 'cite', 'cites' and any key containing 'cite' (at any depth inside a war).
Exits 1 listing each unregistered ID with its war_id and field; exits 0 with a count otherwise."""
import json,os,sys
R=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REG=json.loads(open(f'{R}/data/periods.js').read().split('=',1)[1].rstrip().rstrip(';'))['meta'].get('sources',{})
W=json.load(open(f'{R}/db/wars_post1956.json'))
found=[]
def ids(x,path):
    if isinstance(x,dict):
        if 'source_id' in x: found.append((path,x['source_id']))
        for k,v in x.items():
            if k!='source_id': ids(v,f'{path}.{k}')
    elif isinstance(x,list):
        for i,v in enumerate(x): ids(v,f'{path}[{i}]')
    elif isinstance(x,str) and path.rsplit('.',1)[-1].lower().find('cite')>=0: found.append((path,x))
for w in W.get('wars') or []:
    for k,v in w.items():
        if 'cite' in k.lower(): ids(v,f"{w.get('war_id','?')}:{k}")
bad=[(p,s) for p,s in found if s not in REG]
for p,s in bad:
    war,field=p.split(':',1); print(f'UNREGISTERED {s}  war={war}  field={field}')
print(f'check_wars_cites: {len(found)} cites, {len(set(s for _,s in found))} IDs; unregistered: {len(bad)}')
sys.exit(1 if bad else 0)
