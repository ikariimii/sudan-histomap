#!/usr/bin/env python3
"""Build db/legends/eras/<slug>.json from real data files. Owner: Sudan Map Designer.
Reads only: data/periods.json, db/extents/*.geojson, db/extents_historic.json,
db/group_layers/*.geojson, db/city_layers/cities.geojson. Writes only db/legends/eras/."""
import json, glob, os, re, unicodedata
R = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
J = lambda p: json.load(open(os.path.join(R, p), encoding='utf-8'))
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

def flag_layer(sl):
    v = SYM.get(sl) or {}; fl = v.get('flag'); anc = (FOC.get(sl) or {}).get('flag_anchor')
    items = []
    if fl:
        for x in (fl.get('flags') if fl.get('type') == 'joint_flags' else [fl]):
            items.append({'symbol_class': 'flag', 'file_page': x.get('file_page'), 'image_url': x.get('image_url'),
                          'author': x.get('author'), 'licence': x.get('licence'), 'used_years': x.get('used_years'),
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
    if 'CONTESTED' in b and 'Line' in t: return 'contested_boundary_line'
    if 'CONTESTED' in b: return 'contested_point'
    if t == 'Point': return 'reported_point' if 'REPORTED' in b else 'extent_label_point'
    if 'Line' in t: return 'boundary_line'
    return 'control_extent_approx' if 'APPROXIMATE' in b or p.get('certainty') == 'low' else 'control_extent'

def city_cls(p, s, e):
    roles = [r for r in p['roles'] if (r.get('start') is None or r['start'] <= e) and (r.get('end') is None or r['end'] >= s)]
    if any(r['role'] == 'capital' for r in roles): return 'city_capital', roles
    vt = p.get('visible_to')
    ends = [r['end'] for r in p['roles'] if r.get('end') is not None]
    if p.get('inhabited_today') is False and not roles and ends and s > max(ends): return 'ruin', roles
    rl = roles[0]['role'] if roles else 'other'
    return {'garrison': 'city_garrison', 'religious': 'city_religious', 'port': 'city_port', 'trade': 'city_trade'}.get(rl, 'city_other'), roles

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
    out['layers']['extents'] = {'file': f'db/extents/{sl}.geojson' if ext else None, 'features': ext}
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
    out['layers']['cities'] = {'file': 'db/city_layers/cities.geojson', 'features': cit}
    out['layers']['homelands'] = {'file': 'db/group_layers/homelands.geojson', 'note': 'Homeland points carry no dates; shown as a background toggle in every era, off by default.',
                                  'drawn': sum(1 for f in HOM if f['geometry']), 'list_only': sum(1 for f in HOM if not f['geometry'])}
    out['layers']['flags'] = flag_layer(sl)
    if out['layers']['flags']['flags'] and out['layers']['flags']['anchor']: cls['flag'] = len(out['layers']['flags']['flags'])
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
