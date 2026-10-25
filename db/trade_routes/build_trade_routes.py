#!/usr/bin/env python3
"""Build db/trade_routes/<era>.geojson from main_trade routes in db/era_economy.json. Owner: Sudan Map Designer.
A route is drawn ONLY if it has a cite AND both endpoints resolve (by id, else exact name_en/name_ar) to a place
already in the cited city data: db/city_layers/cities.geojson, db/cities.json, db/cities_modern.json.
No waypoint or coordinate is invented: lines are schematic great-circle arcs between the two cited points,
badged APPROXIMATE unless the route itself carries a source path (route['path'] of place ids, each resolved).
Skipped routes are listed with the reason in db/trade_routes/SKIPPED.md. Runs cleanly on a missing or empty file.
Reads only the files above; writes only db/trade_routes/*.geojson and SKIPPED.md."""
import json, os, glob, math
R = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(R, 'db/trade_routes')

def load(p):
    p = os.path.join(R, p)
    return json.load(open(p, encoding='utf-8')) if os.path.exists(p) else None

def places():
    ids, names = {}, {}
    def add(i, en, ar, lon, lat, src):
        if lat is None or lon is None: return
        rec = {'id': i, 'lon': float(lon), 'lat': float(lat), 'from': src}
        if i: ids.setdefault(i, rec)
        for n in (en, ar):
            if n: names.setdefault(n, rec)
    g = load('db/city_layers/cities.geojson')
    for f in (g or {}).get('features', []):
        p, geo = f['properties'], f.get('geometry')
        if geo and geo.get('type') == 'Point':
            add(p.get('id'), p.get('name_en'), p.get('name_ar'), geo['coordinates'][0], geo['coordinates'][1], 'db/city_layers/cities.geojson')
    for fn, key in (('db/cities.json', 'places'), ('db/cities_modern.json', 'cities')):
        d = load(fn) or {}
        v = d.get(key) or []
        it = v.items() if isinstance(v, dict) else ((x.get('id'), x) for x in v)
        for i, x in it:
            if isinstance(x, dict):
                add(x.get('id') or i, x.get('name_en'), x.get('name_ar'), x.get('lon'), x.get('lat'), fn)
    return ids, names

def resolve(ref, ids, names):
    if isinstance(ref, dict):
        for k in ('id', 'place_id'):
            if ref.get(k) in ids: return ids[ref[k]]
        for k in ('name_en', 'name', 'name_ar'):
            if ref.get(k) in names: return names[ref[k]]
        return None
    if isinstance(ref, str): return ids.get(ref) or names.get(ref)
    return None

def gc(a, b, n=24):
    """Great-circle interpolation between two cited points (geometry only; adds no historical waypoint)."""
    la1, lo1, la2, lo2 = map(math.radians, (a['lat'], a['lon'], b['lat'], b['lon']))
    d = 2 * math.asin(math.sqrt(math.sin((la2-la1)/2)**2 + math.cos(la1)*math.cos(la2)*math.sin((lo2-lo1)/2)**2))
    if d < 1e-9: return [[a['lon'], a['lat']], [b['lon'], b['lat']]]
    pts = []
    for k in range(n + 1):
        f = k / n; A = math.sin((1-f)*d)/math.sin(d); B = math.sin(f*d)/math.sin(d)
        x = A*math.cos(la1)*math.cos(lo1) + B*math.cos(la2)*math.cos(lo2)
        y = A*math.cos(la1)*math.sin(lo1) + B*math.cos(la2)*math.sin(lo2)
        z = A*math.sin(la1) + B*math.sin(la2)
        pts.append([round(math.degrees(math.atan2(y, x)), 5), round(math.degrees(math.atan2(z, math.hypot(x, y))), 5)])
    return pts

def ep(r, *ks):
    for k in ks:
        if r.get(k) is not None: return r[k]

def routes_of(entry):
    mt = (entry or {}).get('main_trade') or {}
    if isinstance(mt, list): return mt
    rs = mt.get('routes') or []
    return rs if isinstance(rs, list) else []

def main():
    eco = load('db/era_economy.json')
    data = {}
    if isinstance(eco, dict):
        data = eco.get('eras') if isinstance(eco.get('eras'), dict) else {k: v for k, v in eco.items() if k != 'meta' and isinstance(v, dict)}
    ids, names = places()
    for f in glob.glob(os.path.join(OUT, '*.geojson')): os.remove(f)
    drawn, skipped = [], []
    for era in sorted(data):
        feats = []
        for n, r in enumerate(routes_of(data[era])):
            if not isinstance(r, dict):
                skipped.append((era, n, str(r), 'route is free text, no structured endpoints')); continue
            label = r.get('label_en') or r.get('name') or r.get('id') or f'route {n}'
            cite = r.get('cite') or r.get('source_ids') or r.get('cite_ids')
            if not cite:
                skipped.append((era, n, label, 'no cite on route')); continue
            a_ref, b_ref = ep(r, 'from', 'start', 'origin'), ep(r, 'to', 'end', 'destination')
            a, b = resolve(a_ref, ids, names), resolve(b_ref, ids, names)
            miss = [str(x) for x, y in ((a_ref, a), (b_ref, b)) if y is None]
            if miss:
                skipped.append((era, n, label, 'endpoint not in cited place data: ' + ', '.join(miss))); continue
            badges = list(r.get('badges') or [])
            path = r.get('path')
            if path:
                pp = [resolve(x, ids, names) for x in path]
                if any(x is None for x in pp):
                    skipped.append((era, n, label, 'source path has a point not in cited place data')); continue
                seq = [a] + pp + [b]; coords = []
                for u, v in zip(seq, seq[1:]): coords += gc(u, v)[(1 if coords else 0):]
                schematic_between = 'cited path points'
            else:
                coords = gc(a, b); schematic_between = 'endpoints only'
                if 'APPROXIMATE' not in badges: badges.append('APPROXIMATE')
            pr = {'id': r.get('id') or f'{era}-route-{n}', 'era_id': era, 'label_en': label, 'label_ar': r.get('label_ar'),
                  'from_id': a['id'], 'to_id': b['id'], 'commodity': r.get('commodity') or r.get('goods'),
                  'direction': r.get('direction'), 'partners': r.get('partners'),
                  'schematic': True, 'schematic_between': schematic_between, 'line': 'great_circle',
                  'symbol_class': 'trade_route', 'badges': badges, 'cite': cite,
                  'endpoint_sources': [a['from'], b['from']]}
            feats.append({'type': 'Feature', 'geometry': {'type': 'LineString', 'coordinates': coords}, 'properties': pr})
            drawn.append((era, label, a['id'], b['id']))
        if feats:
            json.dump({'type': 'FeatureCollection', 'crs_note': 'EPSG:4326', 'features': feats},
                      open(os.path.join(OUT, era + '.geojson'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    src = 'db/era_economy.json' + ('' if eco is not None else ' (not present yet)')
    md = ['# Trade routes: skipped', '', f'Generated by build_trade_routes.py from {src}.',
          f'Drawn: {len(drawn)}. Skipped: {len(skipped)}.', '']
    md += ['| era | # | route | reason |', '|---|---|---|---|'] + [f'| {e} | {n} | {l} | {w} |' for e, n, l, w in skipped] if skipped else ['No routes skipped.']
    open(os.path.join(OUT, 'SKIPPED.md'), 'w', encoding='utf-8').write('\n'.join(md) + '\n')
    print(f'{len(drawn)} routes drawn, {len(skipped)} skipped ({src})')
if __name__ == '__main__': main()
