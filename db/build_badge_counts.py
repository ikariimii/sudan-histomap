#!/usr/bin/env python3
"""Rebuild db/era_badge_counts.json. Read-only scan of data/eras/*.json and db/**/*.json|geojson.

source_types (per era + grand total): each DISTINCT registry ID listed in the era file's
`sources` (data/eras/<id>.json; string or {"id":..}) is classified once, using only the
registry entry in data/periods.json meta.sources (the registry verify_citations.py uses;
read-only). Pass 1: publisher+author text against the rules below; pass 2: url domain; then ISBN -> scholarly;
then note text (fallback only). Within a pass the first matching rule wins, in this order:
  wikipedia_only : url domain wikipedia.org / wikidata.org (or publisher/author Wikipedia/Wikidata)
  intl_financial : World Bank, IMF / International Monetary Fund (worldbank.org, imf.org)
  un_aid_agency  : UN, OCHA, UNHCR, WFP, IOM, IPC, UNICEF, UNDP, UNMIS/UNAMID, AU, IGAD, ReliefWeb
                   (un.org, unocha.org, unhcr.org, wfp.org, iom.int, ipcinfo.org, reliefweb.int, au.int, igad.int)
  government     : CBOS / Central Bank of Sudan, EIA, US Library of Congress country studies (publisher says US government), ministries, Government of ..., .gov / .gov.* domains
  scholarly      : UNESCO General History of Africa, university press, journal, Springer, JSTOR,
                   Brill, Routledge, Cambridge/Oxford, doi.org, .edu / .ac.* domains, ISBN present
  news           : Reuters, AFP, AP, BBC, Al Jazeera, Guardian, NYT, Sudan Tribune, Dabanga, Radio Tamazuj, etc.
  other          : anything else, unregistered IDs, or no rule match. Unclear -> other; no guessing.
Note-field matches are applied only if url/publisher/author matched nothing.
IDs that verify's registry does not hold go to other.
"""
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

# Inline bracketed tags, e.g. "[VERIFY]", in data/eras text fields (not badge keys).
# Kept separate from structured counts. Arabic (_ar / ar) fields are skipped as
# translations of the English text (same reason lens_* files are excluded). A tag
# is skipped when the enclosing object already carries that badge structurally.
IRX = re.compile(r'\[(%s)(?=\]|:)' % "|".join(map(re.escape, BADGES)))
inline = {e: {b: 0 for b in BADGES} for e in eras}
def struct_badges(d):
    got = set()
    for k in BADGE_KEYS & d.keys():
        for v in (d[k] if isinstance(d[k], list) else [d[k]]):
            m = RX.match(v) if isinstance(v, str) else None
            if m: got.add(m.group(1))
    return got
def iwalk(o, e, have=frozenset(), key=None):
    if isinstance(o, dict):
        h = have | struct_badges(o)
        for k, v in o.items():
            if k in BADGE_KEYS or k == "ar" or k.endswith("_ar"): continue
            iwalk(v, e, h, k)
    elif isinstance(o, list):
        for v in o: iwalk(v, e, have, key)
    elif isinstance(o, str):
        for m in IRX.finditer(o):
            if m.group(1) not in have: inline[e][m.group(1)] += 1
for e, f in eras.items():
    iwalk(load(f), e)
itot = {b: sum(inline[e][b] for e in eras) for b in BADGES}


# ---- source_types ----
from urllib.parse import urlparse
REG = load(os.path.join(ROOT,"data/periods.json"))["meta"]["sources"]
STYPES = ["un_aid_agency","intl_financial","government","scholarly","wikipedia_only","news","other"]
RULES = [
 ("wikipedia_only", r"wikipedia\.org|wikidata\.org", r"\bwiki(pedia|data)\b"),
 ("intl_financial", r"worldbank\.org|imf\.org", r"world bank|\bimf\b|international monetary fund"),
 ("un_aid_agency", r"(^|\.)un\.org|unocha\.org|unhcr\.org|wfp\.org|iom\.int|ipcinfo\.org|reliefweb\.int|(^|\.)au\.int|igad\.int|unicef\.org|undp\.org|unmis|unamid",
   r"\bun\b|united nations|\bocha\b|unhcr|\bwfp\b|world food programme|\biom\b|\bipc\b|unicef|undp|unmis|unamid|african union|\bigad\b|reliefweb|security council|panel of experts"),
 ("government", r"\.gov(\.|$)|cbos\.gov\.sd|eia\.gov", r"\bcbos\b|central bank of sudan|library of congress|us government|\beia\b|energy information administration|ministry|government of|state department|foreign office"),
 ("scholarly", r"doi\.org|jstor\.org|springer|brill\.com|cambridge\.org|oup\.com|academic\.oup|tandfonline|\.edu$|\.ac\.[a-z]+$|persee\.fr|cairn\.info|openedition",
   r"unesco|general history of africa|university|journal|springer|brill|routledge|cambridge|oxford|press\b|review\b|presses|academic"),
 ("news", r"reuters\.com|afp\.com|apnews\.com|bbc\.|aljazeera\.|theguardian\.com|nytimes\.com|sudantribune|dabanga|radiotamazuj|washingtonpost|ft\.com|economist\.com|france24|citizen\.co\.za",
   r"reuters|\bafp\b|associated press|\bbbc\b|al jazeera|الجزيرة|guardian|new york times|sudan tribune|dabanga|radio tamazuj|washington post|financial times|economist|france 24"),
]
def classify(sid):
    r = REG.get(sid)
    if not isinstance(r, dict): return "other"
    dom = (urlparse(str(r.get("url") or "")).netloc or "").lower()
    meta = (" ".join(str(r.get(k) or "") for k in ("publisher","author"))).lower()
    for cat, drx, trx in RULES:
        if re.search(trx, meta): return cat
    for cat, drx, trx in RULES:
        if dom and re.search(drx, dom): return cat
    if r.get("isbn"): return "scholarly"
    note = str(r.get("note") or "").lower()
    for cat, drx, trx in RULES:
        if re.search(trx, note): return cat
    return "other"
CLS = {}
stypes = {}
for e, f in eras.items():
    d = load(f) or {}
    ids = set()
    for sid in d.get("sources") or []:
        sid = sid if isinstance(sid, str) else (sid.get("id") if isinstance(sid, dict) else None)
        if sid: ids.add(sid)
    c = {t: 0 for t in STYPES}
    for sid in ids:
        CLS.setdefault(sid, classify(sid)); c[CLS[sid]] += 1
    stypes[e] = c
per = {e: {"source_types": stypes[e], "source_types_total": sum(stypes[e].values()), "counts": counts[e], "total": sum(counts[e].values()), "inline_badges": inline[e], "inline_total": sum(inline[e].values()), "files": sorted(srcs[e])} for e in sorted(eras)}
tot = {b: sum(counts[e][b] for e in eras) for b in BADGES}
out = {"meta": {"generated": datetime.date.today().isoformat(), "generator": "db/build_badge_counts.py",
  "method": "Read-only recursive scan of data/eras/*.json (excluding all.json) and db/**/*.json|*.geojson, excluding lens_* translations, db/border_drafts/ (unpublished drafts; published data only), db/legends/ and legend_spec.json (legend summaries: badges_present, badge_filter, per-entry badge copies), summary/handoff files (second_sources_for_historian.json, *summary*) and this output. Only values under real badge keys count: badge, badges, flags, flag, from_badges, to_badges (array or string). A value counts once if it equals or begins with a badge name (flags use 'SINGLE-SOURCE: <detail>'). Free text (basis_en, note, claim, etc.) is ignored. Attribution: the era file data/eras/<id>.json, a file named after an era id, a dict key equal to an era id, or an enclosing era/era_id/era_ids/eras/period_id field. Unlinked badges are not counted.",
  "badges": BADGES, "era_count": len(eras), "files_scanned": len(files)},
  "totals": tot, "grand_total": sum(tot.values()), "inline_totals": itot, "inline_grand_total": sum(itot.values()),
  "inline_method": "Exact bracketed tags [NAME] or [NAME: note] for the 9 badge names in data/eras/*.json text fields (excluding all.json, badge keys and Arabic _ar/ar fields); a tag is not counted when the enclosing object already has the same structured badge. Not included in totals/grand_total.",
  "source_types_totals": {t: sum(stypes[e][t] for e in eras) for t in STYPES},
  "source_types_grand_total": sum(sum(v.values()) for v in stypes.values()),
  "source_types_distinct_ids": {t: sum(1 for v in CLS.values() if v == t) for t in STYPES},
  "source_types_method": "Per era: distinct registry IDs in data/eras/<id>.json sources, each classified once from data/periods.json meta.sources fields (publisher/author, then url domain, ISBN, note as fallback). Totals sum era counts (an ID cited by several eras counts once per era); source_types_distinct_ids counts each ID once overall. Rules in db/build_badge_counts.py header; unclear IDs -> other.",
  "eras_with_zero_badges": [e for e in per if per[e]["total"] == 0], "eras": per}
json.dump(out, open(os.path.join(ROOT,"db",OUT),"w",encoding="utf-8"), ensure_ascii=False, indent=1)
print(json.dumps({"source_types_totals": out["source_types_totals"], "distinct": out["source_types_distinct_ids"], "totals": tot, "grand": out["grand_total"], "zero": out["eras_with_zero_badges"], "eras": len(eras), "inline_totals": itot, "inline_grand": sum(itot.values())}))
