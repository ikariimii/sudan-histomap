#!/usr/bin/env python3
"""Build db/legends/eras/<slug>.json from real data files. Owner: Sudan Map Designer.
Reads only: data/periods.json, db/extents/*.geojson, db/extents_historic.json,
db/group_layers/*.geojson, db/city_layers/cities.geojson. Writes only db/legends/eras/."""
import json, glob, os, re, unicodedata
R = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
J = lambda p: json.load(open(os.path.join(R, p), encoding='utf-8'))
CJ = J('db/cities.json')['places']
def slug(s):
    s = unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode().lower()
    return re.sub(r'[^a-z0-9]+', '-', s).strip('-')
def badges(p):
    b = set(p.get('badges') or [])
    if p.get('badge'): b.add(p['badge'].split(' ')[0])
    return b
P = J('data/periods.json')['periods']
H = {i['era_id']: i for i in J('db/extents_historic.json')['items']}
C = J('db/city_layers/cities.geojson')
HOM = J('db/group_layers/homelands.geojson')['features']
NOW = 2026
SYM = J('db/era_symbols.json')['eras']
FOC = J('db/era_focus.json')['eras']
SPEC = J('db/legends/legend_spec.json')
_eco = J('db/era_economy.json') if os.path.exists(os.path.join(R, 'db/era_economy.json')) else {}
ECO = (_eco.get('eras') if isinstance(_eco.get('eras'), dict) else {k: v for k, v in _eco.items() if k != 'meta' and isinstance(v, dict)}) if isinstance(_eco, dict) else {}

def economy_layer(sl):
    """Economy rating legend row; only for eras with an entry in db/era_economy.json."""
    e = ECO.get(sl)
    if not e: return None
    r = e.get('rating') if e.get('rating') in ('good', 'mixed', 'bad', 'unknown') else 'unknown'
    b = badges(e) | set(e.get('rating_badges') or [])
    sty = next(c for c in SPEC['economy_rating']['classes'] if c['rating'] == r)
    return {'file': 'db/era_economy.json', 'rating': r, 'symbol_class': sty['id'], 'badges': sorted(b),
            'editorial_marker': 'EDITORIAL' in b, 'rating_basis_en': e.get('rating_basis_en'),
            'cite': e.get('cite') or e.get('rating_cite')}

def route_layer(sl):
    f = os.path.join(R, 'db/trade_routes', sl + '.geojson')
    if not os.path.exists(f): return []
    return [{'id': x['properties']['id'], 'label_en': x['properties'].get('label_en'), 'commodity': x['properties'].get('commodity'),
             'symbol_class': 'trade_route', 'badges': x['properties'].get('badges') or [], 'cite': x['properties'].get('cite')}
            for x in json.load(open(f, encoding='utf-8'))['features']]

def ethno_layer(sl, start):
    f = os.path.join(R, 'db/ethno_markers/seligman1932.geojson')
    if not os.path.exists(f) or start >= 1956: return []
    return [{'id': x['properties']['id'], 'label_en': x['properties']['label_en'], 'symbol_class': 'ethno_label_marker',
             'coord': x['geometry']['coordinates'], 'badges': x['properties']['badges'], 'note': x['properties']['note'],
             'date_note': x['properties']['date_note'], 'caption_en': x['properties']['caption_en'],
             'display_hint': x['properties']['display_hint'], 'source_ids': [c['id'] for c in x['properties']['sources']],
             'plate': x['properties']['sources'][0]['plate']}
            for x in json.load(open(f, encoding='utf-8'))['features'] if x['properties']['era_id'] == sl and not x['properties'].get('hold')]

def flag_layer(sl):
    v = SYM.get(sl) or {}; fl = v.get('flag'); anc = (FOC.get(sl) or {}).get('flag_anchor')
    items = []
    if fl:
        for x in (fl.get('flags') if fl.get('type') == 'joint_flags' else [fl]):
            items.append({'symbol_class': 'flag', 'file_page': x.get('file_page'), 'image_url': x.get('image_url'),
                          'author': x.get('author'), 'licence': x.get('licence'), 'used_windows': (lambda u: [] if not u else ([list(w) for w in u] if isinstance(u[0], list) else [list(u)]))(x.get('used_years')),
                          'badges': x.get('badges') or [], 'verify': 'VERIFY' in (x.get('badges') or []), 'note': x.get('note')})
    em = v.get('emblem')
    return {'file': 'db/era_symbols.json', 'anchor': anc if items else None, 'anchor_file': 'db/era_focus.json',
            'flags': items, 'popup_text_only': em if em and em.get('text_only') else None,
            'display_hint': v.get('display_hint'), 'null_reason': v.get('flag_null_reason') if not items else None}

def ext_class(f):
    p, g = f['properties'], f['geometry']
    b = badges(p)
    if g is None: return 'list_only_text'
    t = g['type']
    z = p.get('zone')
    if z == 'contested' or (z and t == 'Point'): return 'zone_contested' if z == 'contested' else 'extent_label_point'
    if z in ('core', 'claimed', 'influence'): return 'zone_' + z
    if 'CONTESTED' in b and 'Line' in t: return 'contested_boundary_line'
    if 'CONTESTED' in b: return 'contested_point'
    if t == 'Point': return 'reported_point' if 'REPORTED' in b else 'extent_label_point'
    if 'Line' in t: return 'boundary_line'
    return 'control_extent_approx' if 'APPROXIMATE' in b or p.get('certainty') == 'low' else 'control_extent'

def conf_word(c):
    if not isinstance(c, (int, float)): return None
    return 'high' if c >= 0.7 else 'medium' if c >= 0.4 else 'low'

def city_cls(p, s, e):
    roles = [r for r in p['roles'] if (r.get('start') is None or r['start'] <= e) and (r.get('end') is None or r['end'] >= s)]
    if any(r['role'] == 'capital' for r in roles): return 'city_capital', roles
    vt = p.get('visible_to')
    ends = [r['end'] for r in p['roles'] if r.get('end') is not None]
    if p.get('inhabited_today') is False and not roles and ends and s > max(ends): return 'ruin', roles
    rl = roles[0]['role'] if roles else 'other'
    return {'garrison': 'city_garrison', 'religious': 'city_religious', 'port': 'city_port', 'trade': 'city_trade', 'town': 'city_town', 'cult_centre': 'city_cult_centre', 'political_centre': 'city_political_centre'}.get(rl, 'city_other'), roles

def era(i, p):
    s, e = p['start'], p['end']; sl = slug(p['name'])
    out = {'era_id': sl, 'name_en': p['name'], 'stream': p['stream'], 'start': s, 'end': e,
           'layers': {}, 'symbol_classes_present': [], 'badges_present': [], 'counts': {}}
    cls, bs, src = {}, set(), set(p.get('sources') or [])
    # extents
    ef = os.path.join(R, 'db/extents', sl + '.geojson'); ext = []
    if os.path.exists(ef):
        for k, f in enumerate(json.load(open(ef))['features']):
            pr = f['properties']; c = ext_class(f); b = badges(pr); bs |= b
            cls[c] = cls.get(c, 0) + 1
            sids = pr.get('sources') or ([pr['source']] if pr.get('source') else [])
            ext.append({'feature_index': k, 'id': pr.get('id'), 'label_en': pr.get('label_en'), 'symbol_class': c,
                        'certainty': pr.get('certainty'), 'badges': sorted(b), 'start': pr.get('start'), 'end': pr.get('end'),
                        'source_ids': sids})
            if pr.get('zone'):
                cf = pr.get('confidence')
                ext[-1].update({'zone': pr['zone'], 'confidence': cf, 'confidence_word': conf_word(cf),
                                'low_confidence_overlay': isinstance(cf, (int, float)) and cf < 0.5})
            if isinstance(pr.get('confidence'), (int, float)) and pr['confidence'] < 0.5:
                cls['low_confidence'] = cls.get('low_confidence', 0) + 1
                ext[-1]['low_confidence_overlay'] = True
    out['layers']['extents'] = {'file': f'db/extents/{sl}.geojson' if ext else None, 'features': ext}
    BL = {r['badge']: r for r in SPEC['borders_legend']['rows']}
    eb = sorted({x for f in ext for x in f['badges']})
    for x in eb:
        if x not in BL: print('BORDERS-LEGEND MISSING', sl, x)
    out['layers']['extents']['borders_legend'] = [{'badge': x, 'legend_en': BL[x]['legend_en']} for x in eb if x in BL] + (
        [{'badge': 'LOW-CONFIDENCE-HATCH', 'legend_en': SPEC['borders_legend']['low_confidence_hatching']['legend_en']}] if any(f.get('low_confidence_overlay') for f in ext) else [])
    # groups
    gf = os.path.join(R, 'db/group_layers', sl + '.geojson'); grp = []
    if os.path.exists(gf):
        for f in json.load(open(gf))['features']:
            pr = f['properties']; k = pr.get('kind')
            c = 'relation_arrow' if k == 'relation' else ('group_control_point' if f['geometry'] else 'list_only_text')
            if k == 'relation': c = 'relation_arrow_' + pr.get('type', 'other')
            b = badges(pr); bs |= b; cls[c] = cls.get(c, 0) + 1
            grp.append({'id': pr['id'], 'kind': k, 'type': pr.get('type'), 'group': pr.get('group'), 'symbol_class': c,
                        'drawn': f['geometry'] is not None, 'label_en': pr.get('label_en'), 'badges': sorted(b),
                        'source_ids': pr.get('source_ids') or [], 'cite': pr.get('cite') or []})
    out['layers']['groups'] = {'file': f'db/group_layers/{sl}.geojson' if grp else None, 'features': grp}
    # cities
    cit = []
    for f in C['features']:
        pr = f['properties']; vf = pr.get('visible_from'); vt = pr.get('visible_to') if pr.get('visible_to') is not None else NOW
        if vf is None or vf > e or vt < s: continue
        c, roles = city_cls(pr, s, e); b = set(pr.get('badges') or []); bs |= b; cls[c] = cls.get(c, 0) + 1
        cit.append({'id': pr['id'], 'name_en': pr['name_en'], 'name_ar': pr.get('name_ar'), 'symbol_class': c,
                    'roles_in_era': [{k: r.get(k) for k in ('role', 'era_id', 'start', 'end', 'source_id', 'page')} for r in roles],
                    'badges': sorted(b), 'source_ids': pr.get('source_ids') or []})
    # list-only places (no cited map_from) that hold a cited role in this era: listed, not drawn, no date
    for q in CJ:
        if q.get('map_from'): continue
        rr = [r for r in q.get('roles') or [] if r.get('era_id') == sl and r.get('source_id')]
        if not rr: continue
        c = 'city_capital_list_only' if any(r.get('role') == 'capital' for r in rr) else 'city_list_only'
        b = {'LIST-ONLY', 'NO-DATE'}; bs |= b; cls[c] = cls.get(c, 0) + 1
        cit.append({'id': q['id'], 'name_en': q['name_en'], 'name_ar': q.get('name_ar'), 'symbol_class': c, 'drawn': False,
                    'display_en': q['name_en'] + (f" (to {max(r['end'] for r in rr if r.get('end') is not None)})" if any(r.get('end') is not None for r in rr) else ''),
                    'roles_in_era': [{k: r.get(k) for k in ('role', 'era_id', 'start', 'end', 'source_id', 'page')} for r in rr],
                    'badges': sorted(b), 'source_ids': q.get('source_ids') or []})
    out['layers']['cities'] = {'file': 'db/city_layers/cities.geojson', 'features': cit}
    out['layers']['homelands'] = {'file': 'db/group_layers/homelands.geojson', 'note': 'Homeland points carry no dates; shown as a background toggle in every era, off by default.',
                                  'drawn': sum(1 for f in HOM if f['geometry']), 'list_only': sum(1 for f in HOM if not f['geometry'])}
    out['layers']['flags'] = flag_layer(sl)
    if out['layers']['flags']['flags'] and out['layers']['flags']['anchor']: cls['flag'] = len(out['layers']['flags']['flags'])
    ec = economy_layer(sl)
    if ec:
        out['layers']['economy'] = ec; cls[ec['symbol_class']] = 1; bs |= set(ec['badges'])
        if ec['editorial_marker']: cls['economy_editorial_marker'] = 1
    rt = route_layer(sl)
    if rt:
        out['layers']['trade_routes'] = {'file': f'db/trade_routes/{sl}.geojson', 'features': rt}
        cls['trade_route'] = len(rt)
        for x in rt: bs |= set(x['badges'])
    em = ethno_layer(sl, s)
    if em:
        out['layers']['ethno_markers'] = {'file': 'db/ethno_markers/seligman1932.geojson', 'og_preview': False,
                                          'note': 'Soft unfilled halo at the label position; not a boundary or claim. Excluded from OG images.', 'features': em}
        cls['ethno_label_marker'] = len(em)
        for x in em: bs |= set(x['badges'])
    out['symbol_classes_present'] = sorted(cls); out['counts'] = dict(sorted(cls.items()))
    out['counts'].update({'extent_features': len(ext), 'group_features': len(grp), 'cities': len(cit)})
    out['badges_present'] = sorted(bs)
    # context, cited fields only
    ctx = {'key_events_en': p.get('key_events') or [], 'key_events_ar': p.get('key_events_ar') or [],
           'key_events_source_ids': p.get('sources') or [], 'dating_note': p.get('dating_note') or None,
           'capitals': p.get('capitals') or []}
    h = H.get(sl)
    if h:
        ctx['control_limits_en'] = h.get('control_limits_en'); ctx['control_limits_ar'] = h.get('control_limits_ar')
        ctx['control_limits_source_ids'] = h.get('source_ids'); ctx['control_confidence'] = h.get('confidence')
    out['context'] = ctx
    out['_sets'] = {'ext': {x['label_en'] for x in ext if x['label_en']}, 'cit': {x['id'] for x in cit},
                    'grp': {x['id'] for x in grp}, 'cap': {x['id'] for x in cit if x['symbol_class'] == 'city_capital'}}
    out['interactive'] = {
        'click_to_source': 'Click any feature: open popup listing its source_ids (resolve in data/periods.json meta.sources) with page/cite.',
        'layer_toggles': [k for k in ('extents', 'groups', 'cities') if out['layers'][k]['features']] + ['homelands', 'basemap_rivers', 'basemap_terrain', 'graticule'],
        'hover_highlight': 'Hover a legend row: highlight all features of that symbol_class; hover a feature: highlight its legend row.',
        'badge_filter': out['badges_present']}
    return out

def main():
    order = sorted(range(len(P)), key=lambda k: (P[k]['stream'], P[k]['start'], P[k]['end']))
    eras = {k: era(k, P[k]) for k in range(len(P))}
    prev = {}
    for a, b in zip(order, order[1:]):
        if P[a]['stream'] == P[b]['stream']: prev[b] = a
    os.makedirs(os.path.join(R, 'db/legends/eras'), exist_ok=True)
    for k, o in eras.items():
        S = o.pop('_sets'); d = None
        if k in prev:
            Q = eras[prev[k]]['_sets'] if '_sets' in eras[prev[k]] else eras[prev[k]]['__sets']
            d = {'previous_era_id': eras[prev[k]]['era_id'], 'basis': 'previous era in same stream by start year',
                 'extents_added': sorted(S['ext'] - Q['ext']), 'extents_removed': sorted(Q['ext'] - S['ext']),
                 'cities_added': sorted(S['cit'] - Q['cit']), 'cities_removed': sorted(Q['cit'] - S['cit']),
                 'capitals_added': sorted(S['cap'] - Q['cap']), 'capitals_removed': sorted(Q['cap'] - S['cap']),
                 'groups_added': sorted(S['grp'] - Q['grp']), 'groups_removed': sorted(Q['grp'] - S['grp'])}
        o['__sets'] = S
        o['interactive']['what_changed'] = d
    for o in eras.values():
        o.pop('__sets', None)
        json.dump(o, open(os.path.join(R, 'db/legends/eras', o['era_id'] + '.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(len(eras), 'era legends written')
if __name__ == '__main__': main()
