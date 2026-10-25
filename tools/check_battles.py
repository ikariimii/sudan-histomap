#!/usr/bin/env python3
"""Validate data/battles.json, data/wars.json, data/era_events.json."""
import json,re,glob,sys
src=set(json.load(open('data/periods.json'))['meta']['sources'])
for f in glob.glob('db/lens_*.json'):
  try: src|=set(json.load(open(f)).get('meta',{}).get('sources',{}))
  except Exception: pass
eras={e['id'] for e in json.load(open('data/eras/index.json'))['eras']}
err=[]
KEB=re.compile(r'^[a-z0-9]+(-[a-z0-9]+)*--?\d{1,4}$')
def cite(c,w):
  if not isinstance(c,dict) or not c.get('source_id') or not str(c.get('pages','')).strip(): err.append(f'{w}: cite needs source_id+pages')
  elif c['source_id'] not in src: err.append(f"{w}: unregistered source {c['source_id']}")
W=json.load(open('data/wars.json'))['wars'];wid=set()
for w in W:
  i=w.get('war_id','?');wid.add(i)
  for k in ('war_id','name_en','name_ar','date_from','era_ids','cite'):
    if k not in w: err.append(f'war {i}: missing {k}')
  if '[يحتاج تحقق]' not in w.get('name_ar',''): err.append(f'war {i}: name_ar not tagged')
  for e in w.get('era_ids',[]):
    if e not in eras: err.append(f'war {i}: unknown era {e}')
  cite(w.get('cite'),f'war {i}')
ids=set()
for b in json.load(open('data/battles.json'))['battles']:
  i=b.get('id','?')
  if i in ids: err.append(f'{i}: duplicate id')
  ids.add(i)
  if not KEB.match(i): err.append(f'{i}: id not <place>-<year>')
  for k in ('id','war_id','name_en','name_ar','sides','outcome_en','era_ids','cite','precision'):
    if k not in b: err.append(f'{i}: missing {k}')
  if not ('date' in b or ('date_from' in b and 'date_to' in b)): err.append(f'{i}: no date')
  y=str(b.get('date',b.get('date_from','')))
  m=re.match(r'^(-?\d+)',y)
  if not m or not i.endswith('-'+m.group(1).lstrip('-')) or (m.group(1).startswith('-')!=i[:i.rfind('-')].endswith('-')): err.append(f'{i}: id year != start year {y}')
  if b.get('war_id') not in wid: err.append(f'{i}: unknown war_id')
  p=b.get('precision')
  if p not in ('exact','approximate','region'): err.append(f'{i}: bad precision')
  if p=='region' and ('lat' in b or 'lon' in b): err.append(f'{i}: region must not have lat/lon')
  if p!='region' and not (isinstance(b.get('lat'),(int,float)) and isinstance(b.get('lon'),(int,float))): err.append(f'{i}: needs lat/lon')
  if '[يحتاج تحقق]' not in b.get('name_ar',''): err.append(f'{i}: name_ar not tagged')
  for e in b.get('era_ids',[]):
    if e not in eras: err.append(f'{i}: unknown era {e}')
  cite(b.get('cite'),i)
  try:
    if int(y.split('-')[0] if not y.startswith('-') else '-'+y[1:].split('-')[0])>1956: err.append(f'{i}: after 1956')
  except ValueError: pass
EV=json.load(open('data/era_events.json'))
for e,L in EV.items():
  if e not in eras: err.append(f'era_events: unknown era {e}')
  for n,x in enumerate(L):
    for k in ('date','en','ar','cite'):
      if k not in x: err.append(f'{e}[{n}]: missing {k}')
    if x.get('cite')!='NO-SOURCE': cite(x.get('cite'),f'{e}[{n}]')
print('\n'.join(err) or 'check_battles: OK');sys.exit(1 if err else 0)
