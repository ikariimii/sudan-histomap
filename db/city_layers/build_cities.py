#!/usr/bin/env python3
"""Build db/city_layers/cities.geojson from db/cities.json (Sudan Map Designer).
Rule: visible_from = map_from (founded, else first_attested, badge FIRST-ATTESTED); no map_from = list_only;
abandoned null = inhabited_today; abandoned {year:null} = ruin (RUIN-UNDATED) ending at last_attested
(carrying its badge), else last cited role end, else open. Usage: build_cities.py [src] [out]"""
import json, sys, subprocess
SRC = sys.argv[1] if len(sys.argv) > 1 else 'db/cities.json'
OUT = sys.argv[2] if len(sys.argv) > 2 else 'db/city_layers/cities.geojson'
RULE = ('visible_from = map_from (founded, else first_attested, badge FIRST-ATTESTED); no map_from = list_only; '
        'abandoned null = inhabited_today; abandoned {year:null} = ruin (RUIN-UNDATED, inhabited_today false) ending at '
        'last_attested (carrying its badge), else last cited role end, else open')
B = lambda s: s.replace('_', '-') if s else s

def feat(p):
    mf = p['map_from']; basis = mf['basis']; bs = []
    if basis == 'founded': bs.append(B((p['founded'] or {}).get('badge')) or 'FOUNDED')
    else: bs.append('FIRST-ATTESTED')
    if 'needs native review' in (p.get('history_ar_status') or ''): bs.append('AR-REVIEW')
    ab = p['abandoned']; vt = None; vtb = None; inh = ab is None
    if ab is not None and ab.get('year') is not None: vt, vtb = ab['year'], 'abandoned'
    elif ab is not None:
        bs.append('RUIN-UNDATED')
        la = p.get('last_attested')
        ends = [r['end'] for r in p['roles'] if r.get('end') is not None]
        if la and la.get('year') is not None: vt, vtb = la['year'], 'last_attested'; bs.append(B(la.get('badge')) or 'LAST-ATTESTED')
        elif ends: vt, vtb = max(ends), 'last_cited_role'
    if (p.get('coord_source') or {}).get('badge') == 'APPROXIMATE': bs.append('APPROXIMATE-COORDS')
    pr = {'id': p['id'], 'name_en': p['name_en'], 'name_ar': p['name_ar'], 'wikidata': p['wikidata'], 'category': p['category'],
          'visible_from': mf['year'], 'visible_from_basis': basis, 'visible_to': vt, 'inhabited_today': inh,
          'roles': p['roles'], 'badges': bs, 'history_en': p['history_en'], 'history_ar': p['history_ar'],
          'history_source': p.get('history_source'), 'source_ids': p['source_ids'], 'map_from': mf['year']}
    if vtb: pr['visible_to_basis'] = vtb
    return {'type': 'Feature', 'geometry': {'type': 'Point', 'coordinates': [p['lon'], p['lat']]}, 'properties': pr}

def main():
    pl = json.load(open(SRC))['places']
    try: h = subprocess.check_output(['git', 'log', '-1', '--format=%h', '--', SRC], text=True, stderr=subprocess.DEVNULL).strip()
    except Exception: h = '?'
    fs = [feat(p) for p in pl if p.get('map_from')]
    lo = [{'id': p['id'], 'name_en': p['name_en'], 'reason': p.get('list_only_reason') or 'no cited founded or first-attested date in sources read'} for p in pl if not p.get('map_from')]
    out = {'type': 'FeatureCollection', 'meta': {'source': f'{SRC} @{h}', 'rule': RULE}, 'list_only': lo, 'features': fs}
    json.dump(out, open(OUT, 'w'), ensure_ascii=False, indent=1); open(OUT, 'a').write('\n')
    print(f'{OUT}: {len(fs)} drawn, {len(lo)} list-only')
if __name__ == '__main__': main()
