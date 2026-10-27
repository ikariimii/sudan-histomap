#!/usr/bin/env python3
"""Draft builder: ethnic-groups layer (review only). Geometry is copied from
existing cited project data only (community-era extents, group_layers/homelands).
No coordinates are created here."""
import json, re, glob, math, os
R = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
J = lambda p: json.load(open(os.path.join(R, p)))
TAG = " [يحتاج تحقق]"
GROUPS = {  # group -> (EN name, community-era id, homelands group key)
 "shilluk": ("Shilluk (Chollo)", "shilluk-kingdom", "shilluk"),
 "azande":  ("Azande (Zande)", "zande-kingdoms", "azande"),
 "dinka":   ("Dinka (Jieng)", "dinka-jieng-communities", "dinka"),
 "nuer":    ("Nuer (Naath)", "nuer-naath-communities", "nuer"),
 "anuak":   ("Anuak (Anywaa)", "anuak-anywaa-communities", "anuak"),
}
CANON = {"APPROXIMATE","VERIFY","DERIVED","CONTESTED","SINGLE-SOURCE"}
periods = {p["name"]: p for p in J("data/periods.json")["periods"]}
ERA_NAME = {"shilluk-kingdom":"Shilluk Kingdom","zande-kingdoms":"Zande kingdoms",
 "dinka-jieng-communities":"Dinka (Jieng) communities","nuer-naath-communities":"Nuer (Naath) communities",
 "anuak-anywaa-communities":"Anuak (Anywaa) communities"}
def ar(s):
    if not s: return None
    s = re.sub(r"\s*\[Arabic text pending native-speaker review\.\]", "", s).strip()
    return s if s.endswith("[يحتاج تحقق]") else s + TAG
def cites(p):
    out = []
    for k in ("source_ids","sources"):
        out += [x for x in (p.get(k) or []) if x not in out]
    if p.get("source") and p["source"] not in out: out.append(p["source"])
    return out
def badges(p, extra):
    b = list(p.get("badges") or ([p["badge"]] if p.get("badge") else []))
    b = [x for x in b if x in CANON]
    for x in extra:
        if x not in b: b.append(x)
    return b
feats = []
homes = [f for f in J("db/group_layers/homelands.geojson")["features"]]
for g,(en,era,hk) in GROUPS.items():
    per = periods.get(ERA_NAME[era], {})
    span = {"start": per.get("start"), "end": per.get("end")}
    ext = J(f"db/extents/{era}.geojson")
    for i,f in enumerate(ext["features"]):
        p = f["properties"]
        ex = ["APPROXIMATE","DERIVED"] + (["VERIFY"] if p.get("certainty")=="low" or "check" in (p.get("note") or "") else [])
        feats.append({"type":"Feature","geometry":f["geometry"],"properties":{
          "id": p.get("id") or f"eg-{g}-ext-{i+1}", "group": g, "name_en": en,
          "label_en": p.get("label_en"), "label_ar": ar(p.get("label_ar")),
          "detail_en": p.get("label_detail_en"), "detail_ar": ar(p.get("label_detail_ar")),
          "kind": "area" if f["geometry"]["type"]!="Point" else "marker",
          "present_start": (p.get("start") or span["start"]), "present_end": (p.get("end") or span["end"]),
          "present_eras": None, "eras_rule": "eras overlapping present_start..present_end (until Historian supplies era ids)",
          "badges": badges(p, ex), "source_ids": cites(p), "cite": p.get("cite"),
          "pages": p.get("pages"), "license": p.get("license"),
          "geometry_from": f"db/extents/{era}.geojson#{i}"}})
    for f in homes:
        p = f["properties"]
        if p.get("group") != hk or not f.get("geometry"): continue
        feats.append({"type":"Feature","geometry":f["geometry"],"properties":{
          "id": p["id"], "group": g, "name_en": en,
          "label_en": p.get("label_en"), "label_ar": ar(p.get("label_ar")),
          "detail_en": p.get("label_detail_en"), "detail_ar": ar(p.get("label_detail_ar")),
          "kind": "marker", "present_start": (p.get("start") or span["start"]), "present_end": (p.get("end") or span["end"]),
          "present_eras": None, "eras_rule": "eras overlapping present_start..present_end (until Historian supplies era ids)",
          "badges": badges(p, ["APPROXIMATE"]), "source_ids": cites(p), "cite": p.get("cite"),
          "gazetteer": p.get("gazetteer"), "coord_source": p.get("coord_source"),
          "geometry_from": "db/group_layers/homelands.geojson#"+p["id"]}})
# de-duplicate identical ids (homelands features already copied into extents)
seen, out = set(), []
for f in feats:
    if f["properties"]["id"] in seen: continue
    seen.add(f["properties"]["id"]); out.append(f)
# shared points: same coordinate used by >1 group -> overlap, drawn as such
from collections import defaultdict
at = defaultdict(set)
for f in out:
    if f["geometry"]["type"]=="Point": at[tuple(f["geometry"]["coordinates"])].add(f["properties"]["group"])
for f in out:
    if f["geometry"]["type"]=="Point":
        gs = at[tuple(f["geometry"]["coordinates"])]
        f["properties"]["shared_with"] = sorted(gs - {f["properties"]["group"]}) or None
fc = {"type":"FeatureCollection","draft":True,"status":"DRAFT for review; not wired into the build",
 "generated_by":"Sudan Map Designer","date":"2026-10-27",
 "note":"Geometry copied verbatim from existing cited project data (community-era extents + group_layers/homelands.geojson). No new coordinates. Arabic tagged [يحتاج تحقق]; null where not in project data. Group areas are anchor zones/limit points, not borders.",
 "features":out}
json.dump(fc, open(os.path.join(R,"db/ethnic_groups/ethnic_groups.geojson"),"w"), ensure_ascii=False, indent=1)
print(len(out), {g:sum(f["properties"]["group"]==g for f in out) for g in GROUPS})
