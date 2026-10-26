#!/usr/bin/env python3
"""Render 1080x1080 per-era share images from db/share/era_share_spec.json.

Output: out/share/<id>.png (not committed). Writes db/share/share_manifest.json.
Inputs only: spec, data/eras/<id>.json, db/extents/<id>.geojson (area_mode 'extent'),
db/legends/legend_spec.json (zone_styling), img/relief-1800.webp + basemap-region.json
(Natural Earth, PD). Text, map and credit stay above the bottom 15% (y < 918).
No data is invented: missing fields are omitted from the card and logged in the manifest.
Usage: python3 db/share/build_share.py
"""
import json, math, os
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import PathPatch
from matplotlib.path import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
import arabic_reshaper
from bidi.algorithm import get_display

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
J = lambda *p: os.path.join(ROOT, *p)
SPEC, LEG = J("db/share/era_share_spec.json"), J("db/legends/legend_spec.json")
RELIEF, RELIEF_BOX, BASEMAP = J("img", "relief-1800.webp"), (12, -3, 48, 27), J("basemap-region.json")
OUT, MANIFEST = J("out", "share"), J("db/share/share_manifest.json")
W = H = 1080
SAFE_BOTTOM = int(H * 0.85)  # 918
FD = "/usr/share/fonts/truetype/sand-box/google/"
F_AR = FD + "Noto Naskh Arabic/NotoNaskhArabic-VariableFont_wght.ttf"
F_SANS = FD + "Noto Sans/NotoSans-VariableFont_wdth,wght.ttf"
F_SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
COL, AMBER = "#8c2d19", "#e69f00"  # same zone colours as db/og/build_og.py

def font(p, s):  # BASIC layout: shaping/RTL done by arabic_reshaper + python-bidi (avoids double reordering by raqm)
    try: return ImageFont.truetype(p, s, layout_engine=ImageFont.Layout.BASIC)
    except OSError: return ImageFont.truetype(F_SANS, s, layout_engine=ImageFont.Layout.BASIC)

def my(lat): return math.degrees(math.log(math.tan(math.pi / 4 + math.radians(max(min(lat, 85), -85)) / 2)))
def yr(y): return f"{-y} BCE" if y < 0 else f"{y} CE" if y < 1000 else str(y)
def rings(g): return [g["coordinates"]] if g["type"] == "Polygon" else g["coordinates"] if g["type"] == "MultiPolygon" else []

def poly_path(g):
    v, c = [], []
    for poly in rings(g):
        for r in poly:
            pts = [(x, my(y)) for x, y in r]; v += pts; c += [Path.MOVETO] + [Path.LINETO] * (len(pts) - 2) + [Path.CLOSEPOLY]
    return Path(v, c) if v else None

def is_contested(pr):
    return pr.get("zone") == "contested" or pr.get("contested") is True or str(pr.get("badge", "")).upper() == "CONTESTED"

def render_map(e, feats, zs, relief, base, mw, mh, path):
    b = e.get("camera_bbox")
    x0, x1, y0, y1 = b[0], b[2], my(b[1]), my(b[3])
    cx, cy, w, h = (x0 + x1) / 2, (y0 + y1) / 2, max(x1 - x0, 1), max(y1 - y0, 1)
    if w / h < mw / mh: w = h * mw / mh
    else: h = w * mh / mw
    fig = plt.figure(figsize=(mw / 100, mh / 100), dpi=100)
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(cx - w / 2, cx + w / 2); ax.set_ylim(cy - h / 2, cy + h / 2); ax.axis("off")
    fig.patch.set_facecolor("#c9c7bf")  # beyond the relief raster (east of 48E): plain neutral
    ax.imshow(relief, extent=(RELIEF_BOX[0], RELIEF_BOX[2], my(RELIEF_BOX[1]), my(RELIEF_BOX[3])), zorder=0, interpolation="bilinear")
    for f in base["features"]:
        p = poly_path(f["geometry"])
        if p: ax.add_patch(PathPatch(p, fill=False, ec="#4a4a4a", lw=0.9, alpha=0.75, zorder=1))
    op = zs["fill_opacity_by_zone"]; ncont = 0
    for f in feats:
        g = f.get("geometry"); pr = f.get("properties") or {}
        if not g: continue
        con = is_contested(pr); ncont += con; z = pr.get("zone") or "core"
        if g["type"] in ("Polygon", "MultiPolygon"):
            p = poly_path(g)
            if con:
                ax.add_patch(PathPatch(p, fc=AMBER, ec="none", alpha=0.25, zorder=3))
                ax.add_patch(PathPatch(p, fill=False, ec="#7a4f00", lw=0, hatch="///", zorder=4))
                ax.add_patch(PathPatch(p, fill=False, ec="#0f1b24", lw=1.5, ls=(0, (4, 3)), zorder=5))
            else:
                ax.add_patch(PathPatch(p, fc=COL, ec="none", alpha=op.get(z, .35), zorder=3))
                ax.add_patch(PathPatch(p, fill=False, ec="#0f1b24", lw=1.5, ls=(0, (5, 3)) if z == "claimed" else "-", zorder=5))
        elif g["type"] in ("LineString", "MultiLineString"):
            for ln in ([g["coordinates"]] if g["type"] == "LineString" else g["coordinates"]):
                ax.plot([a[0] for a in ln], [my(a[1]) for a in ln], color=AMBER if con else COL, lw=2, ls="--" if con else "-", zorder=5)
        elif g["type"] == "Point":
            x, y = g["coordinates"][0], my(g["coordinates"][1])
            if con: ax.scatter([x], [y], s=300, c=AMBER, alpha=.6, edgecolors="#7a4f00", linewidths=1.5, hatch="///", zorder=6)
            else: ax.scatter([x], [y], s=90, c=COL, edgecolors="#0f1b24", linewidths=1.5, zorder=6)
    fig.savefig(path, dpi=100); plt.close(fig)
    return ncont

def main():
    spec = json.load(open(SPEC)); lay = spec["meta"]["layout"]
    zs = json.load(open(LEG))["zone_styling"]; base = json.load(open(BASEMAP))
    im = ImageEnhance.Color(Image.open(RELIEF).convert("RGB")).enhance(.35)
    im = ImageEnhance.Contrast(ImageEnhance.Brightness(im).enhance(1.9)).enhance(.75)
    relief = np.asarray(Image.blend(im, Image.new("RGB", im.size, (236, 232, 222)), .35))
    os.makedirs(OUT, exist_ok=True)
    mx0, my0, mx1, my1 = lay["map"]["box"]; mw, mh = mx1 - mx0, my1 - my0
    assert my1 <= SAFE_BOTTOM and lay["credit"]["y"] <= 900
    f_en, f_ar, f_yr, f_cr = font(F_SERIF, 56), font(F_AR, 50), font(F_SANS, 30), font(F_SANS, 20)
    items = []
    for e in spec["eras"]:
        eid = e["era_id"]; missing = []; out = os.path.join(OUT, eid + ".png")
        feats, badges = [], []
        if e.get("area_mode") == "extent":
            try: feats = json.load(open(J(e["area_layer"])))["features"]
            except (OSError, ValueError, KeyError, TypeError): missing.append("area_layer")
            badges = sorted({(f.get("properties") or {}).get("badge") for f in feats} - {None})
            if not badges:  # fall back to the extent's own certainty label, copied as-is
                badges = sorted({"certainty: " + str((f.get("properties") or {}).get("certainty")) for f in feats if (f.get("properties") or {}).get("certainty")})
            if feats and not badges: missing.append("area_badge (no badge or certainty on extent features)")
        area_badge = "NO CONTROL CLAIM (post-1956)" if e.get("area_mode") != "extent" else (" / ".join(badges) or None)
        if not e.get("camera_bbox"): missing.append("camera_bbox (rendered with build_og DEFAULT_BBOX Sudan frame)"); e = dict(e, camera_bbox=[21.0, 3.0, 39.0, 23.0])
        tmp = out + ".map.png"
        ncont = render_map(e, feats, zs, relief, base, mw, mh, tmp)
        card = Image.new("RGB", (W, H), "#f4efe4"); card.paste(Image.open(tmp).convert("RGB"), (mx0, my0)); os.remove(tmp)
        d = ImageDraw.Draw(card); d.rectangle([mx0, my0, mx1 - 1, my1 - 1], outline="#0f1b24", width=2)
        m = lay["safe_margin_px"]
        name = e.get("name_en") or ""; 
        if not name: missing.append("name_en")
        while name and d.textlength(name, font=f_en) > W - 2 * m: f_en = font(F_SERIF, f_en.size - 2)
        d.text((m, lay["title_en"]["y"]), name, font=f_en, fill="#1f1f1f", anchor="ls")
        f_en = font(F_SERIF, 56)
        if e.get("name_ar"):
            ar = get_display(arabic_reshaper.reshape(e["name_ar"]))
            tag = get_display(arabic_reshaper.reshape(e.get("name_ar_badge") or ""))
            d.text((W - m, lay["title_ar"]["y"]), ar, font=f_ar, fill="#1f1f1f", anchor="rs")
            if tag.strip(): d.text((m, lay["title_ar"]["y"]), tag, font=font(F_AR, 24), fill="#a33", anchor="ls")
        else: missing.append("name_ar")
        ys = e.get("years") or []
        if len(ys) == 2 and None not in ys: d.text((m, lay["years"]["y"]), f"{yr(ys[0])} – {yr(ys[1])}", font=f_yr, fill="#444", anchor="ls")
        else: missing.append("years")
        srcs = e.get("source_ids") or []
        if not srcs: missing.append("source_ids")
        short = ", ".join(srcs[:4]) + (f" +{len(srcs) - 4}" if len(srcs) > 4 else "")
        credit = lay["credit"]["text"].format(short_source_ids=short or "—", area_badge=area_badge or "—")
        while d.textlength(credit, font=f_cr) > W - 2 * m: f_cr = font(F_SANS, f_cr.size - 1)
        d.text((m, lay["credit"]["y"]), credit, font=f_cr, fill="#333", anchor="ls"); f_cr = font(F_SANS, 20)
        card.save(out, optimize=True)
        items.append({"era_id": eid, "file": os.path.relpath(out, ROOT), "area_mode": e.get("area_mode"),
                      "area_badge": area_badge, "contested_features": ncont, "source_ids": srcs,
                      "status": "INTERNAL_AR_REVIEW" if "يحتاج تحقق" in (e.get("name_ar_badge") or "") else "INTERNAL",
                      "missing_fields": missing})
    json.dump({"meta": {"owner": "Sudan Map Designer", "generator": "db/share/build_share.py", "size_px": [W, H],
                        "output_dir": "out/share/ (not committed)",
                        "publishing": "INTERNAL. Nothing goes to social without Agrescatti's approval. Images with Arabic tagged [يحتاج تحقق] stay internal until a native Arabic reviewer has checked them.",
                        "og_images": "img/og 1200x630 untouched (still used for link cards)",
                        "safe_zone": "era name, Arabic name, credit and map all above y=918 (bottom 15% clear)",
                        "count": len(items)}, "images": items}, open(MANIFEST, "w"), ensure_ascii=False, indent=1)
    print(len(items), "rendered;", sum(bool(i["missing_fields"]) for i in items), "with missing fields")

if __name__ == "__main__": main()
