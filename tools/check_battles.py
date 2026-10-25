#!/usr/bin/env python3
"""Validate data/battles.json (<=1956), db/battles_post1956.json (>1956), db/wars.json, data/era_events.json."""
import json,re,glob,sys
REG=json.load(open('data/periods.json'))['meta']['sources'];src=set(REG)
for f in glob.glob('db/lens_*.json'):
  try: src|=set(json.load(open(f)).get('meta',{}).get('sources',{}))
  except Exception: pass
eras={e['id'] for e in json.load(open('data/eras/index.json'))['eras']}
err=[];warn=[]
TAG='[يحتاج تحقق]'
KEB=re.compile(r'^[a-z0-9]+(-[a-z0-9]+)*--?\d{1,4}$')
EVT=('primary account','inscription/archaeology','scholarly synthesis')
POSTSRC=re.compile(r'^(UN|UNSC|UNMISS|OCHA|ACLED|HRW|OHCHR|GEONAMES)')
ORG=re.compile(r'\bUN\b|United Nations|UN Security Council|OCHA|ACLED|Human Rights Watch|OHCHR')
FORBID=re.compile(r'fatal|death|casualt|killed|control',re.I)
def cite(c,w):
  if not isinstance(c,dict) or not c.get('source_id') or not str(c.get('pages','')).strip(): err.append(f'{w}: cite needs source_id+pages')
  elif c['source_id'] not in src: err.append(f"{w}: unregistered source {c['source_id']}")
def year(s):
  m=re.match(r'^(-?\d+)',str(s or '')); return int(m.group(1)) if m else None
W=json.load(open('db/wars.json'))['wars'];wid=set()
for w in W:
  i=w.get('id','?')
  if i in wid: err.append(f'war {i}: duplicate')
  wid.add(i)
  for k in ('id','name_en','name_ar','era_ids','start','cites'):
    if k not in w: err.append(f'war {i}: missing {k}')
  if TAG not in w.get('name_ar',''): err.append(f'war {i}: name_ar not tagged')
  for e in w.get('era_ids',[]):
    if e not in eras: err.append(f'war {i}: unknown era {e}')
  if not w.get('cites'): err.append(f'war {i}: no cites')
  for n,c in enumerate(w.get('cites',[])): cite(c,f'war {i} cites[{n}]')
def common(b,i,F):
  if TAG not in b.get('name_ar',''): err.append(f'{F} {i}: name_ar not tagged')
  if b.get('war_id') not in wid: err.append(f'{F} {i}: unknown war_id {b.get("war_id")}')
  for e in b.get('era_ids',[]):
    if e not in eras: err.append(f'{F} {i}: unknown era {e}')
ids=set()
for b in json.load(open('data/battles.json'))['battles']:
  i=b.get('id','?')
  if i in ids: err.append(f'{i}: duplicate id')
  ids.add(i)
  if not KEB.match(i): err.append(f'{i}: id not <place>-<year>')
  for k in ('id','war_id','name_en','name_ar','label','sides','outcome_en','era_ids','cite','cites','precision','evidence_type','decisive'):
    if k not in b: err.append(f'{i}: missing {k}')
  if not ('date' in b or ('date_from' in b and 'date_to' in b)): err.append(f'{i}: no date')
  y=str(b.get('date',b.get('date_from','')))
  m=re.match(r'^(-?\d+)',y)
  if not m or not i.endswith('-'+m.group(1).lstrip('-')) or (m.group(1).startswith('-')!=i[:i.rfind('-')].endswith('-')): err.append(f'{i}: id year != start year {y}')
  if year(y) is not None and year(y)>1956: err.append(f'{i}: after 1956 (post-1956 items belong in db/battles_post1956.json)')
  p=b.get('precision')
  if p not in ('exact','approximate','region'): err.append(f'{i}: bad precision')
  if p=='region' and ('lat' in b or 'lon' in b): err.append(f'{i}: region must not have lat/lon')
  if p!='region' and not (isinstance(b.get('lat'),(int,float)) and isinstance(b.get('lon'),(int,float))): err.append(f'{i}: needs lat/lon')
  if b.get('evidence_type') not in EVT: err.append(f'{i}: bad evidence_type')
  if not isinstance(b.get('decisive'),bool): err.append(f'{i}: decisive must be boolean')
  if b.get('decisive') and not b.get('decisive_note'): err.append(f'{i}: decisive true needs decisive_note')
  if 'commanders' in b and not isinstance(b['commanders'],dict): err.append(f'{i}: commanders must be {{side:[names]}}')
  common(b,i,'battle')
  cite(b.get('cite'),i)
  for n,c in enumerate(b.get('cites',[])): cite(c,f'{i} cites[{n}]')
# post-1956 (Analyst-owned; validated, never edited here)
for b in json.load(open('db/battles_post1956.json'))['battles']:
  i=b.get('id','?')
  if i in ids: err.append(f'post1956 {i}: duplicate id')
  ids.add(i)
  y=year(b.get('date_from') or i.rsplit('-',1)[-1])
  if y is None or y<=1956: err.append(f'post1956 {i}: date must be after 1956')
  bad=[k for k in b if FORBID.search(k)]
  if bad: err.append(f'post1956 {i}: forbidden fields {bad}')
  bg=b.get('badges',[])
  if y and y>=2023 and 'REPORTED' not in bg: err.append(f'post1956 {i}: 2023+ needs REPORTED')
  if b.get('war_id')=='south-sudan-civil-war' and y==2013 and 'CONTESTED' not in bg: err.append(f'post1956 {i}: SSCW 2013 needs CONTESTED')
  cs=[b['cite']] if b.get('cite') else []
  cs+=b.get('cites',[])
  if not cs: err.append(f'post1956 {i}: no cite')
  for c in cs:
    cite(c,f'post1956 {i}')
    if isinstance(c,dict) and not (POSTSRC.match(c.get('source_id','')) or ORG.search(str(REG.get(c.get('source_id'),{}).get('publisher',''))+' '+str(REG.get(c.get('source_id'),{}).get('author','')))): err.append(f'post1956 {i}: cite {c.get("source_id")} not UN/OCHA/ACLED/HRW/OHCHR')
  common(b,i,'post1956')
EV=json.load(open('data/era_events.json'))
for e,L in EV.items():
  if e not in eras: err.append(f'era_events: unknown era {e}')
  for n,x in enumerate(L):
    for k in ('date','en','ar','cite'):
      if k not in x: err.append(f'{e}[{n}]: missing {k}')
    if x.get('cite')!='NO-SOURCE': cite(x.get('cite'),f'{e}[{n}]')
print('\n'.join(err) or 'check_battles: OK');sys.exit(1 if err else 0)
