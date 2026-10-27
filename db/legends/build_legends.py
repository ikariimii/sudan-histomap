#!/usr/bin/env python3
"""Build db/legends/eras/<slug>.json from real data files. Owner: Sudan Map Designer.
Reads only: data/periods.json, db/extents/*.geojson, db/extents_historic.json,
db/group_layers/*.geojson, db/city_layers/cities.geojson. Writes only db/legends/eras/.
Also reads db/era_economy.json, db/era_events_post1956.json (merged per web/mapsite.py; committed HEAD copy only, so uncommitted
Analyst work is never baked into legends), db/border_drafts/*.geojson (signed-off only), b.json (battles, same rule as map.js rel()),
db/markers/battle_style.json (battle swatches)."""
import json, glob, os, re, subprocess, unicodedata
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
    ro = e.get('rating'); rv = ro.get('value') if isinstance(ro, dict) else ro
    r = rv if rv in ('good', 'mixed', 'bad', 'unknown') else 'unknown'
    b = badges(e) | set(e.get('rating_badges') or []) | set((ro.get('badges') if isinstance(ro, dict) else None) or [])
    rb = e.get('rating_basis_en')
    if isinstance(rb, dict): b |= set(rb.get('badges') or [])
    sty = next(c for c in SPEC['economy_rating']['classes'] if c['rating'] == r)
    return {'file': 'db/era_economy.json', 'rating': r, 'symbol_class': sty['id'], 'badges': sorted(b),
            'editorial_marker': 'EDITORIAL' in b, 'rating_basis_en': e.get('rating_basis_en'),
            'cite': e.get('cite') or e.get('rating_cite') or (ro.get('cite') if isinstance(ro, dict) else None)}

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


# --- post-1956 Analyst events: mirrors web/mapsite.py _be_post56_ev (IM r26): the Analyst line REPLACES the base line at the same
# era#index when it has a registered cite; P56_BOTH keeps both; an Analyst line with no (or a blanked) base line shows on its own.
SRCREG = set((J('data/periods.json').get('meta') or {}).get('sources') or {})
def _committed(rel):
    try: return json.loads(subprocess.run(['git', '-C', R, 'show', 'HEAD:' + rel], capture_output=True, check=True).stdout.decode('utf-8'))
    except Exception: return J(rel) if os.path.exists(os.path.join(R, rel)) else {}
_p56 = _committed('db/era_events_post1956.json')
P56 = _p56.get('events') or {}
P56_BOTH = {'second-parliamentary-period#0'}
def _rmsid(t):
    m = re.search(r'\s*\(([A-Z][A-Z0-9_]+)\b[^()]*\)\s*$', t or '')
    return t[:m.start()] if m and m.group(1) in SRCREG else t
def _blank(t): return not (t or '').strip()
def key_events(sl, p):
    """Merged key events (list of dicts) for one era. Blank base lines are dropped (an index is skipped only when its EN is blank)."""
    en, ar = p.get('key_events') or [], p.get('key_events_ar') or []
    base = [{'event_id': f'{sl}#{k}', 'en': x, 'ar': ar[k] if k < len(ar) else None, 'cite': None, 'source_ids': p.get('sources') or [],
             'badges': [], 'origin': 'data/periods.json'} for k, x in enumerate(en)]
    rep, extra = {}, []
    for v in P56.get(sl) or []:
        i = v.get('event_id') or '?'
        cs = [c for c in [v.get('cite'), v.get('cite_extra')] + (v.get('cites') or []) if isinstance(c, dict) and c.get('source_id')]
        if not any(c['source_id'] in SRCREG for c in cs): continue
        rec = {'event_id': i, 'en': _rmsid(v.get('en')).strip(), 'ar': (_rmsid(v.get('ar')) or '').strip() or None, 'date': v.get('date'),
               'cite': [{'source_id': c['source_id'], 'pages': c.get('pages')} for c in cs], 'source_ids': [c['source_id'] for c in cs],
               'badges': [v['badge']] if v.get('badge') else list(v.get('badges') or []), 'origin': 'db/era_events_post1956.json'}
        try: k = int(i.rsplit('#', 1)[1])
        except Exception: k = None
        h = base[k] if k is not None and k < len(base) and i.startswith(sl + '#') else None
        if i in P56_BOTH or h is None or _blank(h['en']): extra.append((k, rec)) if (i in P56_BOTH or h is None) else rep.__setitem__(k, rec)
        else: rep[k] = rec
    out = [rep.get(k, b) for k, b in enumerate(base)]
    for k, rec in extra:
        if rec['event_id'] in P56_BOTH and k is not None and k < len(out): out.insert(k + 1, rec)
        else: out.append(rec)
    out = [x for x in out if not _blank(x['en'])]
    for x in out:
        if _blank(x['ar']): x['ar'] = None
    return out

# --- border drafts: only features the Historian signed off (properties.signoff.status == 'approved')
def draft_layer(sl):
    rows = []; ZS = {c['id']: c for c in SPEC['symbol_classes'] if c.get('id')}
    for f in sorted(glob.glob(os.path.join(R, 'db/border_drafts', '*.geojson'))):
        if os.path.basename(f).startswith('_'): continue
        for k, x in enumerate(json.load(open(f, encoding='utf-8'))['features']):
            pr = x['properties']; so = pr.get('signoff') or {}
            if pr.get('era_id') != sl or not isinstance(so, dict) or so.get('status') != 'approved': continue
            z = so.get('zone') or pr.get('zone'); cf = so.get('confidence', pr.get('confidence')); b = sorted(set(so.get('badges') or pr.get('badges') or []))
            cw = conf_word(cf); cs = 'contested' if ('CONTESTED' in b or z == 'contested') else 'solid' if z == 'core' else 'hatched'
            zk = 'zone_contested' if cs == 'contested' else 'zone_' + str(z)
            zc = ZS.get(zk) or {}
            sw = {k2: zc.get(k2) for k2 in ('geometry', 'fill', 'fill_opacity', 'stroke', 'stroke_colour', 'stroke_colour_pre1899_solid', 'dash', 'feather') if zc.get(k2) is not None}
            sw['confidence_style'] = cs
            # map.js CKS: the low-confidence hatch follows confidence_style == 'hatched' only (not numeric confidence), never on contested
            if cs == 'hatched': sw['overlay'] = ZS.get('low_confidence', {}).get('pattern'); sw['overlay_opacity'] = ZS.get('low_confidence', {}).get('opacity')
            rows.append({'file': os.path.relpath(f, R), 'feature_index': k, 'zone': z, 'confidence': cf, 'confidence_word': cw,
                         'legend_en': f"Draft border (confidence: {cw + ' ' + str(cf) if cw else 'not stated'})", 'symbol_class': zk,
                         'swatch': sw, 'badges': b, 'source_ids': so.get('sources') or [], 'pages': so.get('pages'),
                         'signoff': {'by': so.get('by'), 'date': so.get('date')}})
    return rows

BAT = (J('b.json').get('battles') or []) if os.path.exists(os.path.join(R, 'b.json')) else []
BST = J('db/markers/battle_style.json')['battle']['variants'] if os.path.exists(os.path.join(R, 'db/markers/battle_style.json')) else {}
DELETED_BATTLES = {'dongola-642'}  # IM ruling 2026-10-26: deleted; arab-nubian-wars starts 651 (GHA III)
def battle_layer(s, e):
    """Battles the map draws for this era: map.js rel(b) = battle span overlaps the era, or its war span (w) does."""
    rows = []
    for b in BAT:
        if b.get('id') in DELETED_BATTLES: continue
        w = b.get('w') or {}
        on = (b.get('a') is not None and b['a'] <= e and (b.get('b') if b.get('b') is not None else b['a']) >= s) or \
             (w.get('a') is not None and w['a'] <= e and (w.get('b') if w.get('b') is not None else w['a']) >= s)
        if not on: continue
        v = b.get('pr') if b.get('pr') in BST else 'approximate'
        rows.append({'id': b['id'], 'label_en': b.get('en'), 'label_ar': b.get('ar'), 'start': b.get('a'), 'end': b.get('b'),
                     'precision': b.get('pr'), 'symbol_class': 'battle_' + v, 'drawn': bool(b.get('ll') or (b.get('hz') or {}).get('ll')), 'list_only': not (b.get('ll') or (b.get('hz') or {}).get('ll')), 'via_war': not ((b.get('a') or 0) <= e and (b.get('b') if b.get('b') is not None else b.get('a') or 0) >= s),
                     'war_en': w.get('en'), 'swatch': BST.get(v), 'cite': [{'c': c.get('c'), 'p': c.get('p'), 'u': c.get('u')} for c in b.get('s') or []]})
    return rows

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

LID_PREFIX = {'extents': 'extent', 'groups': 'group', 'cities': 'city', 'battles': 'battle', 'border_drafts': 'draft',
              'trade_routes': 'route', 'ethno_markers': 'ethno'}
def legend_ids(out, sl):
    # stable ids: one per legend ROW (<layer>:<symbol_class>) and one per listed feature. Rows used to be keyed by
    # symbol_class alone, so homelands list-only and extents/groups list-only rows collided on 'list_only_text'.
    rows = {}
    for lk, L in out['layers'].items():
        if not isinstance(L, dict): continue
        pf = LID_PREFIX.get(lk, lk)
        for k, f in enumerate(L.get('features') or []):
            c = f.get('symbol_class')
            if not c: continue
            fid = f.get('id') if f.get('id') is not None else f'idx{k}'
            f['legend_id'] = (f'{pf}-list:{sl}:{fid}' if c == 'list_only_text' else f'{pf}:{sl}:{fid}')
            rows[f'{lk}:{c}'] = rows.get(f'{lk}:{c}', 0) + 1
    h = out['layers']['homelands']
    h['legend_ids'] = [f"homelands:{f['properties']['id']}" for f in HOM if f['geometry']]
    h['list_only_legend_ids'] = [f"homelands-list:{f['properties']['id']}" for f in HOM if not f['geometry']]
    if h['drawn']: rows['homelands:homeland_point'] = h['drawn']
    if h['list_only']: rows['homelands:list_only_text'] = h['list_only']
    out['legend_rows'] = [{'row_id': r, 'layer': r.split(':')[0], 'symbol_class': r.split(':')[1], 'n': n} for r, n in rows.items()]
    ids = [x['row_id'] for x in out['legend_rows']] + [f['legend_id'] for L in out['layers'].values() if isinstance(L, dict)
           for f in L.get('features') or [] if 'legend_id' in f] + h['legend_ids'] + h['list_only_legend_ids']
    dup = {i for i in ids if ids.count(i) > 1}
    assert not dup, (sl, sorted(dup)[:5])

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
            lbl, lb = pr.get('label_en'), None
            if not lbl and pr.get('zone'):
                # no feature label: use the era's own registered name (periods) + the drafted zone; nothing new is asserted
                lbl = f"{p.get('name') or sl} – {pr['zone']} zone (draft)"; lb = 'era name + zone (feature has no label_en)'
            ext.append({'feature_index': k, 'id': pr.get('id'), 'label_en': lbl, **({'label_basis': lb} if lb else {}), 'symbol_class': c,
                        'certainty': pr.get('certainty'), 'badges': sorted(b), 'start': pr.get('start'), 'end': pr.get('end'),
                        'source_ids': sids})
            if pr.get('zone'):
                cf = pr.get('confidence')
                cs = pr.get('confidence_style')
                ext[-1].update({'zone': pr['zone'], 'confidence': cf, 'confidence_word': conf_word(cf), 'confidence_style': cs,
                                'low_confidence_overlay': cs == 'hatched' and pr['zone'] != 'contested'})
            if ext[-1].get('low_confidence_overlay'):
                cls['low_confidence'] = cls.get('low_confidence', 0) + 1
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
    dr = draft_layer(sl)
    if dr:
        out['layers']['border_drafts'] = {'note': 'Historian-signed-off drafts only (properties.signoff.status == approved); not live extents.', 'features': dr}
        cls['border_draft'] = len(dr)
        for x in dr: bs |= set(x['badges'])
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
    bt = battle_layer(s, e)
    if bt:
        out['layers']['battles'] = {'file': 'b.json', 'style_file': 'db/markers/battle_style.json',
                                    'note': 'Same selection as map.js rel(): battle years overlap the era, or the battle belongs to a war whose span overlaps it.', 'features': bt}
        for x in bt: cls[x['symbol_class']] = cls.get(x['symbol_class'], 0) + 1
    legend_ids(out, sl)
    out['symbol_classes_present'] = sorted(cls); out['counts'] = dict(sorted(cls.items()))
    out['counts'].update({'extent_features': len(ext), 'group_features': len(grp), 'cities': len(cit), 'battles': len(bt)})
    out['badges_present'] = sorted(bs)
    # context, cited fields only
    ke = key_events(sl, p)
    ctx = {'key_events_en': [x['en'] for x in ke], 'key_events_ar': [x['ar'] for x in ke], 'key_events': ke,
           'key_events_source_ids': list(dict.fromkeys((p.get('sources') or []) + [s2 for x in ke if x['origin'] != 'data/periods.json' for s2 in x['source_ids']])),
           'dating_note': p.get('dating_note') or None, 'capitals': p.get('capitals') or []}
    if p.get('capital_note'):
        ctx['capital_note'] = p['capital_note']
        for k2 in ('capital_note_ar', 'capital_note_cite', 'capital_note_source_ids'):
            if p.get(k2) is not None: ctx[k2] = p[k2]
    h = H.get(sl)
    if h:
        ctx['control_limits_en'] = h.get('control_limits_en'); ctx['control_limits_ar'] = h.get('control_limits_ar')
        ctx['control_limits_source_ids'] = h.get('source_ids'); ctx['control_confidence'] = h.get('confidence')
    out['context'] = ctx
    out['_sets'] = {'ext': {x['label_en'] for x in ext if x['label_en']}, 'cit': {x['id'] for x in cit},
                    'grp': {x['id'] for x in grp}, 'cap': {x['id'] for x in cit if x['symbol_class'] == 'city_capital'}}
    out['interactive'] = {
        'click_to_source': 'Click any feature: open popup listing its source_ids (resolve in data/periods.json meta.sources) with page/cite.',
        'layer_toggles': [k for k in ('extents', 'groups', 'cities') if out['layers'][k]['features']] + (['battles'] if bt else []) + ['homelands', 'basemap_rivers', 'basemap_terrain', 'graticule'],
        'hover_highlight': 'Hover a legend row: highlight all features of that symbol_class; hover a feature: highlight its legend row.',
        'badge_filter': out['badges_present']}
    return out

# Canonical badge mapping (IM rulings 2026-10-27). Only the 12 canonical badges stay in badge fields.
BADGE_CANON = {'SINGLE-SOURCE', 'CONTESTED', 'REPORTED', 'VERIFY', 'TRADITION', 'MODEL', 'APPROXIMATE', 'EDITORIAL', 'PARTIAL', 'DERIVED', 'NO-SOURCE', 'CENSUS'}
CANON = {'LOW-CONFIDENCE-HATCH': ['APPROXIMATE'], 'LAST-ATTESTED': ['VERIFY'], 'RUIN-UNDATED': ['VERIFY'],
         'LAST-ATTESTED+APPROXIMATE': ['VERIFY', 'APPROXIMATE'], 'APPROXIMATE-COORDS': ['APPROXIMATE'], 'MODERN_SVG_RENDERING': ['DERIVED']}
WORKFLOW = {'AR-REVIEW', 'LIST-ONLY', 'NO-DATE'}  # internal flags, never shown to visitors
SPEC_AR = json.load(open(os.path.join(R, 'db/legends/legend_spec.json'), encoding='utf-8'))
_RU_AR = ((SPEC_AR.get('uncertainty_encoding') or {}).get('RUIN-UNDATED') or {}).get('legend_ar')
CITY_FA = {c['id']: c.get('first_attested') for c in CJ}
def _yr(y): return f"{-y} BCE" if y < 0 else f"{y} CE"
def _note(o, en, ar):
    o.setdefault('card_notes', [])
    if not any(n['en'] == en for n in o['card_notes']): o['card_notes'].append({'en': en, 'ar': ar})
def canon(o):
    if isinstance(o, dict):
        if isinstance(o.get('badge'), str) and o['badge'] in CANON: o['badge'] = CANON[o['badge']][0]
        if isinstance(o.get('badges'), list):
            cited = bool(o.get('source_ids') or o.get('cite') or o.get('sources'))
            b, wf = [], list(o.get('workflow_flags') or [])
            for x in o['badges']:
                if x in WORKFLOW:
                    if x not in wf: wf.append(x)
                    continue
                if x == 'RUIN-UNDATED': _note(o, 'end undated', (_RU_AR + ' [يحتاج تحقق]') if _RU_AR else None)
                if x == 'FIRST-ATTESTED':
                    fa = CITY_FA.get(o.get('id')) or {}
                    if cited and fa.get('year') is not None:
                        c = ' '.join(str(v) for v in (fa.get('source_id'), fa.get('page')) if v)
                        _note(o, f"first attested ({_yr(fa['year'])}, {c})" if c else f"first attested ({_yr(fa['year'])})", None)
                        continue
                    xs = ['VERIFY']
                else: xs = CANON.get(x, [x])
                for y in xs:
                    if y not in b: b.append(y)
            o['badges'] = sorted(b)
            if wf: o['workflow_flags'] = wf
        for v in o.values(): canon(v)
    elif isinstance(o, list):
        for v in o: canon(v)
    return o
def _allb(o):
    if isinstance(o, dict):
        if isinstance(o.get('badge'), str): yield o['badge']
        for x in (o.get('badges') if isinstance(o.get('badges'), list) else []): yield x
        for v in o.values(): yield from _allb(v)
    elif isinstance(o, list):
        for v in o: yield from _allb(v)
def canon_era(o):
    canon(o.get('layers'))
    if isinstance(o.get('badges_present'), list): o['badges_present'] = sorted({b for l in o.get('layers', {}).values() for b in _allb(l)})
    if isinstance(o.get('interactive'), dict) and 'badge_filter' in o['interactive']: o['interactive']['badge_filter'] = o.get('badges_present')
    return o

def toggle_block():
    # shared, toggle-scoped legend block (DEM / heatmap): same in every era, never merged into era files
    sp = json.load(open(os.path.join(R, 'db/legends/legend_spec.json'), encoding='utf-8'))['toggle_legends']
    out = {'scope': sp['scope'], 'source': 'db/legends/legend_spec.json toggle_legends', 'toggles': []}
    for k in ('dem', 'heatmap'):
        b = sp[k]
        css = 'linear-gradient(to right,' + ','.join(f"{c} {round(100*(v-b['domain'][0])/(b['domain'][1]-b['domain'][0]),1)}%" for v, c in b['stops']) + ')'
        out['toggles'].append({'id': k, 'row_id': f'toggle:{k}', 'hidden_by_default': b.get('hidden_by_default', False), 'show_rule': b.get('show_rule'), 'show_when_chip_on': b['toggle_key'], 'kind': b['kind'],
            'label_en': b['title_en'], 'label_ar': b['title_ar'], 'unit': b['unit'], 'domain': b['domain'],
            'stops': b['stops'], 'css_gradient': css, 'opacity': b.get('opacity', 1), 'ticks': b['ticks'],
            'tick_format_en': b.get('tick_format_en'), 'tick_format_ar': b.get('tick_format_ar'),
            'counts': b.get('counts'), 'note_en': b['note_en'], 'note_ar': b['note_ar'], 'drawn_status': b['drawn_status']})
    json.dump(out, open(os.path.join(R, 'db/legends/toggles.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('toggle legend block written')

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
        o.pop('__sets', None); canon_era(o)
        json.dump(o, open(os.path.join(R, 'db/legends/eras', o['era_id'] + '.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(len(eras), 'era legends written')
    toggle_block()
if __name__ == '__main__':
    import sys
    if '--canon-only' in sys.argv:  # apply the badge mapping to existing era files without rebuilding them
        for f in sorted(glob.glob(os.path.join(R, 'db/legends/eras/*.json'))):
            o = json.load(open(f, encoding='utf-8')); n = json.dumps(canon_era(json.loads(json.dumps(o))), ensure_ascii=False, indent=1)
            if n != json.dumps(o, ensure_ascii=False, indent=1): open(f, 'w', encoding='utf-8').write(n)
    else: main()
