#!/usr/bin/env python3
"""Promote Historian-signed border drafts into db/extents/<era>.geojson as zone features.
Owner: Sudan Map Designer. NOT run until the Historian signs off.

Input : db/border_drafts/<era>.geojson in this repo (bd-0.1, see its README), or --drafts DIR.
Each draft feature is promoted ONLY if properties.signoff exists with status == "approved".
Every promoted value (zone, confidence, badges, sources, basis) comes from signoff; nothing is
defaulted from the draft's own properties, nothing is invented. Geometry is the draft's (or
signoff.geometry if the Historian supplies a clipped one).

Expected signoff block (per feature):
  "signoff": {"status": "approved"|"rejected"|"pending", "by": "Sudan Historian", "date": "YYYY-MM-DD",
              "commit": "<hash>", "zone": "core|claimed|influence|contested", "confidence": 0.0-1.0,
              "badges": [...], "sources": ["ID", ...]  (must resolve in data/periods.json meta.sources),
              "basis_en": "... with page refs", "pages": "...", "start": int, "end": int,
              "label_en": "...", "label_ar": "..." (optional), "geometry": {...} (optional, clipped)}

Rules enforced: contested zones are never drawn as polygons (existing CONTESTED policy = points);
a contested signoff must give signoff.contested_point [lon,lat] or it is skipped. No feature
without >=1 resolvable cite. EDITORIAL forced when confidence < 0.4, APPROXIMATE always (draft README).
Existing non-zone features in an extents file are kept untouched; zone features from an earlier
promotion (same draft_id) are replaced. extents_historic.json is read-only and must keep >= 62 items.
Default is a dry run; --write writes db/extents/. Then run tools/verify_citations.py --offline
and db/legends/build_legends.py."""
import argparse, glob, json, os, sys
R = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DEF = os.path.join(R, 'db/border_drafts')  # synced staging folder; this script lives outside it
ZONES = ('core', 'claimed', 'influence', 'contested')
NEED = ('zone', 'confidence', 'badges', 'sources', 'basis_en', 'by', 'date')
# signoff keys consumed by the standard mapping below; any OTHER signoff key (e.g. editorial_scope,
# editorial_note_en) is carried into the promoted properties unchanged.
STD = set(NEED) | {'status', 'commit', 'pages', 'start', 'end', 'label_en', 'label_ar', 'geometry', 'contested_point'}

def load(p): return json.load(open(p, encoding='utf-8'))

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--drafts', default=DEF); ap.add_argument('--write', action='store_true')
    a = ap.parse_args()
    ms = load(os.path.join(R, 'data/periods.json'))['meta']['sources']
    known = set(ms) if isinstance(ms, dict) else {s['id'] for s in ms}
    eras = {os.path.basename(f)[:-8] for f in glob.glob(os.path.join(R, 'db/extents/*.geojson'))}
    nh = len(load(os.path.join(R, 'db/extents_historic.json'))['items'])
    if nh < 62: sys.exit(f'extents_historic.json has {nh} items (<62); refusing')
    rep, errs, out = [], 0, {}
    for f in sorted(glob.glob(os.path.join(a.drafts, '*.geojson'))):
        if os.path.basename(f).startswith('_'): continue
        for k, ft in enumerate(load(f)['features']):
            p = ft['properties']; era = p.get('era_id'); did = f'{era}#{k}:{p.get("zone")}'
            so = p.get('signoff') or {}
            if so.get('status') != 'approved': rep.append(('SKIP', did, 'not signed off (' + str(so.get('status')) + ')')); continue
            miss = [x for x in NEED if so.get(x) in (None, '', [])]
            bad = []
            if miss: bad.append('missing signoff fields ' + ','.join(miss))
            if era not in eras: bad.append('no db/extents file for era')
            if so.get('zone') not in ZONES: bad.append('bad zone')
            c = so.get('confidence')
            if not isinstance(c, (int, float)) or not 0 <= c <= 1: bad.append('confidence not 0-1')
            unk = [s for s in so.get('sources') or [] if s not in known]
            if unk: bad.append('sources not in meta.sources: ' + ','.join(unk))
            if bad: errs += 1; rep.append(('ERROR', did, '; '.join(bad))); continue
            b = set(so['badges']) | {'APPROXIMATE'}
            if c < 0.4: b.add('EDITORIAL')
            if so['zone'] == 'contested':
                pt = so.get('contested_point')
                if not pt: rep.append(('SKIP', did, 'contested polygon not drawn (points-only rule); no signoff.contested_point')); continue
                geom = {'type': 'Point', 'coordinates': pt}; b.add('CONTESTED')
            else:
                geom = so.get('geometry') or ft['geometry']
            if len(so['sources']) == 1: b.add('SINGLE-SOURCE')
            props = {'id': f'zone-{era}-{so["zone"]}-{k}', 'draft_id': did, 'zone': so['zone'], 'confidence': c,
                     'certainty': 'high' if c >= .7 else 'medium' if c >= .4 else 'low',
                     'badges': sorted(b), 'source': so['sources'][0], 'sources': so['sources'],
                     'basis_en': so['basis_en'], 'pages': so.get('pages'), 'start': so.get('start'), 'end': so.get('end'),
                     'label_en': so.get('label_en'), 'label_ar': so.get('label_ar'),
                     'method': p.get('method'), 'signoff': {x: so.get(x) for x in ('by', 'date', 'commit')},
                     'draft_version': p.get('version')}
            for x, v in so.items():
                if x not in STD and x not in props: props[x] = v
            out.setdefault(era, []).append({'type': 'Feature', 'geometry': geom, 'properties': props})
            rep.append(('OK', did, f'{so["zone"]} conf {c} {sorted(b)}'))
    for r in rep: print(*r, sep='\t')
    if errs: sys.exit(f'{errs} signed-off feature(s) failed checks; nothing written')
    for era, feats in out.items():
        fp = os.path.join(R, 'db/extents', era + '.geojson'); fc = load(fp)
        ids = {x['properties']['draft_id'] for x in feats}
        old = {(x.get('properties') or {}).get('draft_id'): x['properties'] for x in fc['features']
               if (x.get('properties') or {}).get('draft_id') in ids}
        for ft in feats:  # carry extra properties set on the earlier promotion (e.g. Alodia editorial_*)
            for x, v in (old.get(ft['properties']['draft_id']) or {}).items():
                if x not in ft['properties']:
                    ft['properties'][x] = v; print('CARRY', ft['properties']['draft_id'], x)
        keep = [x for x in fc['features'] if (x.get('properties') or {}).get('draft_id') not in ids]
        fc['features'] = keep + feats
        fc['extent_rendering'] = {'mode': 'zones', 'zones_from': 'db/border_drafts/promote_drafts.py'}
        print(('WRITE' if a.write else 'DRY'), fp, f'{len(keep)} kept + {len(feats)} zone')
        if a.write: json.dump(fc, open(fp, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    if not out: print('no signed-off features; nothing to write')
if __name__ == '__main__': main()
