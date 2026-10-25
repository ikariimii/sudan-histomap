#!/usr/bin/env python3
"""Rebuild db/era_badge_counts.json. Read-only scan of data/eras/*.json and db/**/*.json|geojson."""
import json, glob, os, re, datetime
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BADGES = ["SINGLE-SOURCE","CONTESTED","VERIFY","REPORTED","MODEL","EDITORIAL","APPROXIMATE","PARTIAL","DERIVED"]
RX = re.compile(r'^\s*(%s)\b' % "|".join(map(re.escape, BADGES)))
ERA_KEYS = {"era","era_id","era_ids","eras","period_id"}
SKIP = {"all.json"}  # aggregate copy of data/eras
SKIP_PREFIX = ("lens_",)  # translations duplicate source badges
# Only these keys carry real badges (surveyed 2026-10-24): badge/badges everywhere,
# flags in data/eras + era_fill files ("SINGLE-SOURCE: ..."), from_/to_badges in group_layers.
BADGE_KEYS = {"badge","badges","flags","flag","from_badges","to_badges"}
# Legend/summary/handoff files restate badges already counted at source.
SKIP_DIRS = ("/db/border_drafts/", "/db/legends/")
SKIP_FILES = {"legend_spec.json","second_sources_for_historian.json"}
OUT = "era_badge_counts.json"

def load(p):
    try: return json.load(open(p, encoding="utf-8"))
    except Exception: return None

era_files = sorted(f for f in glob.glob(os.path.join(ROOT,"data/eras/*.json")) if os.path.basename(f) not in SKIP)
eras = {}
for f in era_files:
    d = load(f)
    if isinstance(d, dict) and d.get("id"): eras[d["id"]] = f
counts = {e: {b: 0 for b in BADGES} for e in eras}
srcs = {e: set() for e in eras}

def ids_in(v):
    vs = v if isinstance(v, list) else [v]
    return [x for x in vs if isinstance(x, str) and x in eras]

def walk(o, ctx, rel, key=None):
    if isinstance(o, dict):
        c = ctx
        for k in ERA_KEYS & o.keys():
            got = ids_in(o[k])
            if got: c = got
        for k, v in o.items():
            walk(v, [k] if k in eras else c, rel, k)
    elif isinstance(o, list):
        for v in o: walk(v, ctx, rel, key)
    elif isinstance(o, str) and ctx and key in BADGE_KEYS:
        m = RX.match(o)
        if m:
            for e in ctx:
                counts[e][m.group(1)] += 1; srcs[e].add(rel)

files = era_files + sorted(glob.glob(os.path.join(ROOT,"db/**/*.json"), recursive=True) + glob.glob(os.path.join(ROOT,"db/**/*.geojson"), recursive=True))
for f in files:
    b = os.path.basename(f)
    if any(x in f.replace(os.sep,"/") for x in SKIP_DIRS) or b in SKIP_FILES or "summary" in b: continue
    if b == OUT or b in SKIP or b.startswith(SKIP_PREFIX): continue
    d = load(f)
    if d is None: continue
    rel = os.path.relpath(f, ROOT)
    stem = os.path.splitext(b)[0]
    walk(d, [stem] if stem in eras else [], rel)

per = {e: {"counts": counts[e], "total": sum(counts[e].values()), "files": sorted(srcs[e])} for e in sorted(eras)}
tot = {b: sum(counts[e][b] for e in eras) for b in BADGES}
out = {"meta": {"generated": datetime.date.today().isoformat(), "generator": "db/build_badge_counts.py",
  "method": "Read-only recursive scan of data/eras/*.json (excluding all.json) and db/**/*.json|*.geojson, excluding lens_* translations, db/border_drafts/ (unpublished drafts; published data only), db/legends/ and legend_spec.json (legend summaries: badges_present, badge_filter, per-entry badge copies), summary/handoff files (second_sources_for_historian.json, *summary*) and this output. Only values under real badge keys count: badge, badges, flags, flag, from_badges, to_badges (array or string). A value counts once if it equals or begins with a badge name (flags use 'SINGLE-SOURCE: <detail>'). Free text (basis_en, note, claim, etc.) is ignored. Attribution: the era file data/eras/<id>.json, a file named after an era id, a dict key equal to an era id, or an enclosing era/era_id/era_ids/eras/period_id field. Unlinked badges are not counted.",
  "badges": BADGES, "era_count": len(eras), "files_scanned": len(files)},
  "totals": tot, "grand_total": sum(tot.values()),
  "eras_with_zero_badges": [e for e in per if per[e]["total"] == 0], "eras": per}
json.dump(out, open(os.path.join(ROOT,"db",OUT),"w",encoding="utf-8"), ensure_ascii=False, indent=1)
print(json.dumps({"totals": tot, "grand": out["grand_total"], "zero": out["eras_with_zero_badges"], "eras": len(eras)}))
