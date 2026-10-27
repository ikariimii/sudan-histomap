#!/usr/bin/env python3
"""Draft builder: ethnic-groups layer (review only).
Group records, areas, anchors and cites come from db/ethnic_groups.json (Historian).
Geometry: cited anchor points (city_id -> db/cities.json, or lat/lon given in the record),
group_layers/homelands.geojson points, and db/ethnic_groups/group_points.geojson (cited points
kept verbatim from the removed community eras). No coordinates are created here.
Style: db/ethnic_groups/ethnic_groups_layer_style.json (ink #a278ba; halo/outline >=3.82:1 era-fill waiver)."""
import json, re, os
from collections import defaultdict
R = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
J = lambda p: json.load(open(os.path.join(R, p), encoding="utf-8"))
TAG = " [يحتاج تحقق]"
CANON = {"SOURCED","APPROXIMATE","VERIFY","DERIVED","CONTESTED","SINGLE-SOURCE","TRADITION","REPORTED"}
BANNED = {"SFDAS_HCS2017"}
EG = J("db/ethnic_groups.json")
CITY = {c["id"]: c for c in J("db/cities.json")["places"]}
def ar(s):
    if not s: return None
    s = re.sub(r"\s*\[Arabic text pending native-speaker review\.\]", "", s).strip()
    return s if s.endswith("[يحتاج تحقق]") else s + TAG
def cid(c): return c.get("source_id") or c.get("id")
def cites(p):
    out = []
    for k in ("source_ids","sources"):
        out += [x for x in (p.get(k) or []) if x not in out]
    if p.get("source") and p["source"] not in out: out.append(p["source"])
    return [x for x in out if x not in BANNED]
def badges(b, extra=()):
    b = [x for x in (b or []) if x in CANON]
    for x in extra:
        if x not in b: b.append(x)
    return b
def name(g): return f'{g["name_en"]} ({g["endonym"]})' if g.get("endonym") else g["name_en"]
G = {g["id"]: g for g in EG["groups"]}
AAR = J("db/ethnic_groups/anchor_ar.json")["anchors"]  # working Arabic for anchors (Map Designer)
feats = []
for gid, g in G.items():
    a = g.get("area") or {}
    pres = g.get("presence") or {}
    base = {"group": gid, "name_en": name(g), "present_start": pres.get("from_year"), "present_end": pres.get("to_year"),
            "present_eras": [e["era_id"] for e in g.get("era_ids") or []] or None,
            "area_text_en": a.get("text_en"), "area_cites": a.get("cites"), "area_badges": badges(a.get("badges"))}
    for i, an in enumerate(a.get("anchors") or []):
        if an.get("city_id"):
            c = CITY.get(an["city_id"])
            if not c or c.get("lat") is None: continue
            lon, lat, csrc = c["lon"], c["lat"], f'db/cities.json#{an["city_id"]}'
            label = c.get("name_en") or an["city_id"]
        elif an.get("lat") is not None:
            lon, lat, csrc, label = an["lon"], an["lat"], an.get("coord_source"), an.get("name")
        else: continue
        cc = an.get("cite") or {}
        feats.append({"type":"Feature","geometry":{"type":"Point","coordinates":[lon, lat]},"properties":dict(base, **{
            "id": f"eg-{gid}-anchor-{i+1}", "kind": "anchor", "label_en": f'{label}: {an.get("role")}' if an.get("role") else label,
            "label_ar": ar(AAR.get(f"eg-{gid}-anchor-{i+1}", {}).get("label_ar")), "detail_ar": ar(AAR.get(f"eg-{gid}-anchor-{i+1}", {}).get("detail_ar")),
            "badges": badges(an.get("badges"), ["APPROXIMATE"]), "source_ids": [cid(cc)] if cid(cc) else [],
            "cite": cc, "coord_source": csrc, "note": an.get("note"), "geometry_from": "db/ethnic_groups.json"})})
def add_points(fc, src):
    for f in fc["features"]:
        p = f["properties"]; gid = p.get("group")
        if gid not in G or not f.get("geometry"): continue
        feats.append({"type":"Feature","geometry":f["geometry"],"properties":dict({k:v for k,v in feats[0]["properties"].items() if False}, **{
            "group": gid, "name_en": name(G[gid]), "id": p.get("id"), "kind": "marker",
            "label_en": p.get("label_en"), "label_ar": ar(p.get("label_ar")),
            "detail_en": p.get("label_detail_en"), "detail_ar": ar(p.get("label_detail_ar")),
            "present_eras": [e["era_id"] for e in G[gid].get("era_ids") or []] or None,
            "badges": badges(p.get("badges") or ([p["badge"]] if p.get("badge") else []), ["APPROXIMATE"]),
            "source_ids": cites(p), "cite": p.get("cite"), "pages": p.get("pages"),
            "gazetteer": p.get("gazetteer"), "coord_source": p.get("coord_source"),
            "geometry_from": src + "#" + str(p.get("id"))})})
add_points(J("db/ethnic_groups/group_points.geojson"), "db/ethnic_groups/group_points.geojson")
homes = J("db/group_layers/homelands.geojson")
for f in homes["features"]:
    f["properties"] = dict(f["properties"]); f["properties"]["group"] = f["properties"].get("group")
add_points(homes, "db/group_layers/homelands.geojson")
for i, f in enumerate(feats):
    if not f["properties"].get("id"): f["properties"]["id"] = f'eg-{f["properties"]["group"]}-pt-{i+1}'
seen, out = set(), []
for f in feats:
    if f["properties"]["id"] in seen: continue
    seen.add(f["properties"]["id"]); out.append(f)
at = defaultdict(set)
for f in out: at[tuple(f["geometry"]["coordinates"])].add(f["properties"]["group"])
for f in out:
    f["properties"]["shared_with"] = sorted(at[tuple(f["geometry"]["coordinates"])] - {f["properties"]["group"]}) or None
fc = {"type":"FeatureCollection","draft":True,"status":"DRAFT for review; not wired into the build",
 "generated_by":"Sudan Map Designer","date":"2026-10-27",
 "groups": {gid: {"name_en": name(g), "area_text_en": (g.get("area") or {}).get("text_en"), "area_cites": (g.get("area") or {}).get("cites"),
                  "area_badges": badges((g.get("area") or {}).get("badges"))} for gid, g in sorted(G.items())},
 "note":"Group records and cites from db/ethnic_groups.json (Historian). Points only: cited anchors (cities.json / record lat-lon), homelands layer, and cited points kept from the removed community eras. Areas are textual (area_text_en); no polygon is drawn because no source gives a boundary. No new coordinates. Arabic tagged [يحتاج تحقق]. Style: ink #a278ba, halo/outline >=3.82:1 against every era fill (waiver).",
 "features":out}
json.dump(fc, open(os.path.join(R,"db/ethnic_groups/ethnic_groups.geojson"),"w",encoding="utf-8"), ensure_ascii=False, indent=1)
print(len(out), {g:sum(f["properties"]["group"]==g for f in out) for g in sorted(G)})
