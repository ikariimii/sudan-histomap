#!/usr/bin/env python3
"""Analyst check: every override in db/era_events_post1956.json (era#index) must point to an existing
key_events line in data/periods.json whose English text sha1[:8] equals the stored text_hash.
Entries marked "standalone": true replace no line and are skipped. Exits 1 on any problem."""
import json,hashlib,os,sys
R=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
d=json.load(open(f'{R}/db/era_events_post1956.json'))
P={x['name']:x for x in json.load(open(f'{R}/data/periods.json'))['periods']}
bad=[];n=0
for era,L in (d.get('events') or {}).items():
    try: ke=P[json.load(open(f'{R}/data/eras/{era}.json'))['name_en']]['key_events']
    except Exception as x: bad.append(f'{era}: era not found in periods.json ({x})');continue
    for e in L:
        i=e.get('event_id','?')
        if e.get('standalone'): continue
        n+=1
        try: k=int(i.rsplit('#',1)[1])
        except Exception: bad.append(f'{i}: bad event_id');continue
        if k>=len(ke): bad.append(f'{i}: no key_events line at index {k} (era has {len(ke)})');continue
        h=hashlib.sha1(ke[k].encode()).hexdigest()[:8]
        if e.get('text_hash')!=h: bad.append(f'{i}: text_hash {e.get("text_hash")} != current {h} ({ke[k][:70]!r})')
for b in bad: print('PROBLEM',b)
print(f'check_era_overrides: {n} overrides checked; problems: {len(bad)}')
sys.exit(1 if bad else 0)
