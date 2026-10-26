#!/usr/bin/env python3
"""Build db/map_sources.json (one entry per era id) and db/border_transitions.json from existing files only.
Owner: Sudan Map Designer. Reads: data/periods.json, db/extents/*.geojson, db/trade_routes/*.geojson,
db/border_overlay_maps.json. Writes only db/map_sources.json and db/border_transitions.json. No geometry is created.
Usage: python3 db/map_sources/build_map_sources.py"""
import json, glob, os, re, unicodedata, math
from shapely.geometry import shape
R = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
J = lambda p: json.load(open(os.path.join(R, p), encoding='utf-8'))
def slug(s):
    s = unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode().lower()
    return re.sub(r'[^a-z0-9]+', '-', s).strip('-')
P = J('data/periods.json')['periods']
OV = J('db/border_overlay_maps.json')
# keyword -> base source type; matched only against the feature's own provenance properties
BASE = [('OpenHistoricalMap', r'openhistoricalmap|\bohm\b|OHM_'), ('CShapes', r'cshapes'), ('Natural Earth', r'natural.?earth|NATURAL_EARTH'),
        ('HDX COD-AB', r'cod-ab|hdx'), ('OpenStreetMap', r'openstreetmap|\bosm\b'), ('Pleiades', r'pleiades'), ('GeoNames', r'geonames'),
        ('NGA GNS', r'nga[_ ]gns|\bnga\b'), ('Wikidata', r'wikidata'), ('PCA Abyei Award coordinates', r'pca abyei'),
        ('Hand-placed anchor/buffer draft (bd-0.1)', r'anchor points \+|anchor/buffer|hand-placed')]
def badges(p):
    b = set(p.get('badges') or [])
    if p.get('badge'): b.add(str(p['badge']).split(' ')[0])
    return sorted(b)
def cites(p, hn=None):
    out, pages = [], p.get('pages')
    for s in (p.get('sources') or ([p['source']] if p.get('source') else [])):
        sid = s.get('id') if isinstance(s, dict) else s
        if sid: out.append({'id': sid, 'pages': pages})
    c = p.get('cite')
    for x in (c if isinstance(c, list) else [c] if c else []):
        if isinstance(x, dict): out.append({'id': x.get('source_id'), 'pages': x.get('page')})
        elif isinstance(x, str): out.append({'id': x.split(' ')[0], 'pages': ' '.join(x.split(' ')[1:]) or pages})
    # a bare source id with no page: take the page only from a cite of that same id that the file itself records
    # (collection historian_note, checked on the page image), and only if no other page is already given for that id
    for x in out:
        if x['pages'] is None and x['id'] in (hn or {}) and not any(y['id'] == x['id'] and y['pages'] for y in out):
            x['pages'] = hn[x['id']]
    seen, res = set(), []
    for x in out:
        k = (x['id'], str(x['pages']))
        if x['id'] and k not in seen: seen.add(k); res.append(x)
    return res
def base_source(p):
    txt = ' | '.join(str(p.get(k)) for k in ('geometry_source', 'license', 'method', 'coord_source', 'ohm_relation') if p.get(k))
    hits = [n for n, rx in BASE if re.search(rx, txt, re.I)]
    if not txt: return None, None, 'no geometry_source, license, method or coord_source property'
    if not hits: return None, txt, 'provenance text present but names no known base source'
    return hits, txt, None
def overlay(era, p, geom):
    did = (p.get('draft_id') or '').split('#')[0]
    maps = [{'title': m['title'], 'mean_error_km': m.get('mean_error_km'), 'gcp_count': m.get('gcp_count')} for m in OV if did and did in m.get('draft_ids', [])]
    if geom is None: return None, [], 'no geometry'
    if maps: return None, maps, 'not traced; this draft was only checked against the maps in checked_against'
    return None, [], 'not traced from a georeferenced map'
def zone_type(p, g):
    if p.get('zone'): return p['zone']
    if g is None: return 'list_only'
    if 'CONTESTED' in badges(p): return 'contested_point' if g['type'] == 'Point' else 'contested'
    return {'Point': 'point', 'MultiPoint': 'point', 'LineString': 'line', 'MultiLineString': 'line'}.get(g['type'], 'extent')
AR = json.load(open(os.path.join(R, 'db/map_sources/labels_ar.json'), encoding='utf-8'))['ar']
def add_ar(x):  # Arabic label/reason translations from labels_ar.json (all [VERIFY]); inserted after each English key
    out = {}
    for k, v in x.items():
        out[k] = v
        if k in ('label_en', 'base_source_null_reason', 'overlay_null_reason'):
            out['label_ar' if k == 'label_en' else k + '_ar'] = AR.get(v) if v else None
    return out
def main():
    eras, shapes = {}, {}
    for p in P:
        e = slug(p['name']); items = []
        f = os.path.join(R, 'db/extents', e + '.geojson')
        fc = json.load(open(f, encoding='utf-8')) if os.path.exists(f) else {'features': []}
        hn = {}
        for c in ((fc.get('historian_note') or {}).get('cites') or []):
            if c.get('source_id') and c.get('page'): hn.setdefault(c['source_id'], (f"vol.{c['vol']} " if c.get('vol') else '') + c['page'])
        for k, ft in enumerate(fc['features']):
            pr, g = ft['properties'], ft['geometry']
            fid = pr.get('id') or f'{e}#{k}'
            bs, txt, nr = base_source(pr); err, maps, er = overlay(e, pr, g)
            items.append({'layer': 'extents', 'file': f'db/extents/{e}.geojson', 'feature_index': k, 'feature_id': pr.get('id'),
                          'label_en': pr.get('label_en'), 'zone_type': zone_type(pr, g), 'geometry_type': g['type'] if g else None,
                          'cites': cites(pr, hn), 'base_source': bs, 'base_source_text': txt, 'base_source_null_reason': nr,
                          'badges': badges(pr), 'confidence': pr.get('confidence'), 'certainty': pr.get('certainty'),
                          'start': pr.get('start'), 'end': pr.get('end'),
                          'checked_against': maps, 'overlay_mean_error_km': err, 'overlay_null_reason': er})
            if g and g['type'] in ('Polygon', 'MultiPolygon'): shapes.setdefault(e, []).append((fid, k, pr, shape(g)))
        tf = os.path.join(R, 'db/trade_routes', e + '.geojson')
        for k, ft in enumerate(json.load(open(tf, encoding='utf-8'))['features'] if os.path.exists(tf) else []):
            pr = ft['properties']
            items.append({'layer': 'trade_routes', 'file': f'db/trade_routes/{e}.geojson', 'feature_index': k, 'feature_id': pr.get('id'),
                          'label_en': pr.get('label_en'), 'zone_type': 'trade_route', 'geometry_type': ft['geometry']['type'],
                          'cites': [{'id': c, 'pages': None} for c in (pr.get('cite') if isinstance(pr.get('cite'), list) else [pr.get('cite')]) if c],
                          'base_source': ['schematic great-circle between place-data endpoints'], 'base_source_text': ', '.join(map(str, pr.get('endpoint_sources') or [])),
                          'base_source_null_reason': None, 'badges': pr.get('badges') or [], 'confidence': None, 'certainty': None,
                          'checked_against': [], 'overlay_mean_error_km': None, 'overlay_null_reason': 'schematic line, not traced'})
        mf = os.path.join(R, 'db/ethno_markers/seligman1932.geojson')
        for k, ft in enumerate(json.load(open(mf, encoding='utf-8'))['features'] if os.path.exists(mf) and p['start'] < 1956 else []):
            pr = ft['properties']
            if pr['era_id'] != e or pr.get('hold'): continue
            items.append({'layer': 'ethno_markers', 'file': 'db/ethno_markers/seligman1932.geojson', 'feature_index': k, 'feature_id': pr['id'],
                          'label_en': pr['label_en'], 'zone_type': 'label_marker', 'geometry_type': 'Point',
                          'cites': [{'id': 'SELIGMAN1932', 'pages': pr['sources'][0]['plate']}],
                          'base_source': ['georeferenced period map (Seligman 1932, RMS 1.33 km)'], 'base_source_text': pr['method'],
                          'base_source_null_reason': None, 'badges': pr['badges'], 'confidence': None, 'certainty': None,
                          'date_note': pr['date_note'], 'note': pr['note'],
                          'checked_against': [], 'overlay_mean_error_km': None, 'overlay_null_reason': 'label position, not a traced shape'})
        items = [add_ar(x) for x in items]
        eras[e] = {'name_en': p['name'], 'stream': p['stream'], 'start': p['start'], 'end': p['end'], 'shapes': items,
                   'counts': {'shapes': len(items), 'contested': sum(1 for x in items if 'contested' in x['zone_type'] or 'CONTESTED' in x['badges']),
                              'trade_routes': sum(1 for x in items if x['layer'] == 'trade_routes'),
                              'base_source_null': sum(1 for x in items if x['base_source'] is None)}}
    meta = {'generated_by': 'db/map_sources/build_map_sources.py', 'owner': 'Sudan Map Designer',
            'inputs': ['data/periods.json', 'db/extents/*.geojson', 'db/trade_routes/*.geojson', 'db/ethno_markers/seligman1932.geojson', 'db/border_overlay_maps.json'],
            'schema': {'eras.<era_id>.shapes[]': {'layer': 'extents|trade_routes|ethno_markers', 'file': 'path', 'feature_index': 'int', 'feature_id': 'properties.id or null',
                       'label_en': 'str|null', 'label_ar': 'Arabic of label_en from labels_ar.json, ends [VERIFY]', 'zone_type': 'core|claimed|influence|contested|contested_point|extent|point|line|list_only|trade_route',
                       'cites': '[{id, pages}] from sources/source/cite/pages', 'base_source': 'list of base-source types matched in the feature own provenance properties, or null',
                       'base_source_text': 'the provenance text matched', 'base_source_null_reason': 'why base_source is null', 'badges': 'list', 'confidence': 'number|null',
                       'certainty': 'word|null', 'checked_against': '[{title, mean_error_km, gcp_count}] maps in border_overlay_maps.json this draft was checked against; mean_error_km is the georeferencing error of the MAP (2nd-order polynomial RMS), not of the shape', 'overlay_mean_error_km': 'error of the shape if traced from a georeferenced map; null everywhere (none traced)',
                       'overlay_null_reason': 'why null', 'base_source_null_reason_ar / overlay_null_reason_ar': 'Arabic of the reason from labels_ar.json, ends [VERIFY]'}},
            'checked_against_note': 'mean_error_km values are the errors of the maps the shape was checked against, not of the shape.',
            'rules': 'Derived only from the input files; nothing inferred. Base source is null when the properties do not name one.',
            'totals': {'eras': len(eras), 'shapes': sum(v['counts']['shapes'] for v in eras.values()),
                       'base_source_null': sum(v['counts']['base_source_null'] for v in eras.values()),
                       'overlay_error_non_null': 0,
                       'checked_against_shapes': sum(1 for v in eras.values() for x in v['shapes'] if x['checked_against'])}}
    json.dump({'meta': meta, 'eras': eras}, open(os.path.join(R, 'db/map_sources.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('map_sources:', meta['totals'])
    transitions(eras, shapes)

def km(deg_len, lat):  # rough length conversion for display only
    return round(deg_len * 111.32 * (0.5 + 0.5 * math.cos(math.radians(lat))), 1)
def sides(a, b):
    out = {}
    for n, i, s in (('west', 0, -1), ('south', 1, -1), ('east', 2, 1), ('north', 3, 1)):
        d = round((b.bounds[i] - a.bounds[i]) * s, 3)
        out[n] = 'unchanged' if abs(d) < 0.01 else ('expands' if d > 0 else 'contracts') + f' {abs(d)} deg'
    return out
EXCLUDE_CITES = {'mamluk-sultanate': ('WP_MAKURIA', 'WP_MAKURIA_2026')}
EXCLUDE_NOTE = 'WP_MAKURIA and WP_MAKURIA_2026 (same Wikipedia Makuria article) excluded from mamluk-sultanate transition cites: the Makuria post-1276 reach (Lower Nubia to Kordofan under Siti) and the Abu Hamad anchor are unsourced and removed. The OHM Mamluk polygons are reference only; they stop at c.19.9N and do not draw the Makuria reach, so no pair or shape part depended on it and geometry is unchanged. Makuria 1276-1364 rests on SFDAS_HCS2017 p.419 only (vassalage, cession of whole provinces), with no drawn limit.'
def transitions(eras, shapes):
    order = sorted(eras, key=lambda e: (eras[e]['stream'], eras[e]['start'], eras[e]['end']))
    out, pairs = [], 0
    for a, b in zip(order, order[1:]):
        if eras[a]['stream'] != eras[b]['stream']: continue
        A, B = shapes.get(a, []), shapes.get(b, []); used = set(); prs = []
        cite0 = lambda e, k: next(x['cites'] for x in eras[e]['shapes'] if x['layer'] == 'extents' and x['feature_index'] == k)
        # Makuria after 1276: the Kordofan reach / Abu Hamad anchor are unsourced (only WP_MAKURIA); excluded per Innovation Manager ruling.
        cite = lambda e, k: [c for c in cite0(e, k) if c['id'] not in EXCLUDE_CITES.get(e, ())]
        for fa, ka, pa, ga in A:
            best = None
            for fb, kb, pb, gb in B:
                if not ga.is_valid or not gb.is_valid: continue
                inter = ga.intersection(gb).area
                if inter <= 0: continue
                iou = inter / ga.union(gb).area
                if not best or iou > best[0]: best = (iou, fb, kb, pb, gb)
            if not best: continue
            iou, fb, kb, pb, gb = best; used.add(kb)
            shared = ga.boundary.intersection(gb.boundary.buffer(0.01)).length
            lat = ga.centroid.y
            prs.append({'from': {'era_id': a, 'feature_id': fa, 'feature_index': ka, 'zone': pa.get('zone'), 'cites': cite(a, ka)},
                        'to': {'era_id': b, 'feature_id': fb, 'feature_index': kb, 'zone': pb.get('zone'), 'cites': cite(b, kb)},
                        'mode': 'hold' if ga.equals(gb) else ('morph' if iou >= 0.3 else 'cross_fade'), 'iou': round(iou, 3),
                        'shared_edge_km_approx': km(shared, lat), 'changed_sides': sides(ga, gb),
                        'area_change_pct': round((gb.area - ga.area) / ga.area * 100, 1) if ga.area else None})
        pairs += len(prs)
        out.append({'from_era': a, 'to_era': b, 'stream': eras[a]['stream'], 'pairs': prs,
                    'fade_out': [f for f, k, _, _ in A if f not in {p['from']['feature_id'] for p in prs}],
                    'fade_in': [f for f, k, _, _ in B if k not in used]})
    meta = {'generated_by': 'db/map_sources/build_map_sources.py', 'owner': 'Sudan Map Designer',
            'era_order': 'data/periods.json, consecutive eras in the same stream sorted by start, end (same as db/legends what_changed)',
            'rules': 'Pairs only live db/extents polygons; no new geometry. Each from-polygon is paired with the next-era polygon of highest overlap (IoU). mode: hold (identical), morph (IoU >= 0.3), cross_fade (overlap but IoU < 0.3). Non-overlapping shapes go to fade_out / fade_in. shared_edge_km_approx and changed_sides are display aids computed from the two live geometries (bbox side deltas), not sourced limits.',
            'overlay_maps_file': 'db/border_overlay_maps.json (maps listed in db/map_sources.json checked_against per shape)',
            'exclusions': {'cites': {k: list(v) for k, v in EXCLUDE_CITES.items()}, 'note': EXCLUDE_NOTE},
            'totals': {'era_steps': len(out), 'pairs': pairs}}
    json.dump({'meta': meta, 'transitions': out}, open(os.path.join(R, 'db/border_transitions.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('transitions:', meta['totals'])
if __name__ == '__main__': main()
