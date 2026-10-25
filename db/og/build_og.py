#!/usr/bin/env python3
"""Build 1200x630 Open Graph previews per era -> img/og/<id>.png.

Inputs (all already in repo, no network): db/era_focus.json (era list, zoom),
data/eras/<id>.json (name_en, start, end, focus_view.bbox), db/extents/<id>.geojson
(zones), db/legends/legend_spec.json (zone_styling), img/relief-1800.webp
(Natural Earth shaded relief, PD, Mercator over RELIEF_BOX from map.js),
basemap-region.json (Natural Earth admin-0, PD). Idempotent: a sha256 of every
input + this script is stored in db/og/manifest.json; up-to-date images are skipped.
Usage: python3 db/og/build_og.py [--force]
"""
import hashlib, json, math, os, sys
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import PathPatch
from matplotlib.path import Path
import numpy as np
from PIL import Image, ImageEnhance

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
J = lambda *p: os.path.join(ROOT, *p)
RELIEF, RELIEF_BOX = J("img", "relief-1800.webp"), (12, -3, 48, 27)  # map.js RELIEF_BOX
BASEMAP, SPEC, FOCUS = J("basemap-region.json"), J("db/legends/legend_spec.json"), J("db/era_focus.json")
OUT, MANIFEST = J("img", "og"), J("db/og/manifest.json")
W, H, DPI = 1200, 630, 100
DEFAULT_BBOX = (21.0, 3.0, 39.0, 23.0)  # Sudan frame when an era has no focus_view and no extent
ZONE_COLOR = {"core": "#8c2d19", "claimed": "#8c2d19", "influence": "#8c2d19", None: "#8c2d19"}
AMBER = "#e69f00"

def sha(paths):
    h = hashlib.sha256()
    for p in paths:
        h.update(p.encode()); h.update(open(p, "rb").read() if os.path.exists(p) else b"<missing>")
    return h.hexdigest()

def my(lat): return math.degrees(math.log(math.tan(math.pi / 4 + math.radians(max(min(lat, 85), -85)) / 2)))

def yr(y): return f"{-y} BCE" if y < 0 else f"{y} CE" if y < 1000 else str(y)

def rings(geom):
    t, c = geom["type"], geom["coordinates"]
    return [c] if t == "Polygon" else c if t == "MultiPolygon" else []

def poly_path(geom):
    verts, codes = [], []
    for poly in rings(geom):
        for ring in poly:
            pts = [(x, my(y)) for x, y in ring]
            verts += pts; codes += [Path.MOVETO] + [Path.LINETO] * (len(pts) - 2) + [Path.CLOSEPOLY]
    return Path(verts, codes) if verts else None

def all_xy(geom, acc):
    c = geom["coordinates"]
    if geom["type"] == "Point": acc.append(c); return
    def walk(a):
        if isinstance(a[0], (int, float)): acc.append(a)
        else: [walk(b) for b in a]
    walk(c)

def frame(bbox):
    x0, y0, x1, y1 = bbox[0], my(bbox[1]), bbox[2], my(bbox[3])
    cx, cy, w, h = (x0 + x1) / 2, (y0 + y1) / 2, max(x1 - x0, 2), max(y1 - y0, 2)
    ar = W / H
    if w / h < ar: w = h * ar
    else: h = w / ar
    return cx - w / 2, cx + w / 2, cy - h / 2, cy + h / 2

def render(eid, era, feats, spec, relief, base, out):
    zs = spec["zone_styling"]; op = zs["fill_opacity_by_zone"]; thr = 0.5
    # camera = union of era_focus/focus_view bbox and the extent bbox (+0.75 deg pad)
    fv = (era.get("focus_view") or {}).get("bbox")
    acc = []
    for f in feats:
        if f.get("geometry"): all_xy(f["geometry"], acc)
    boxes, parts = [], []
    if fv: boxes.append(fv); parts.append("focus_view")
    if acc:
        xs, ys = [a[0] for a in acc], [a[1] for a in acc]
        boxes.append((min(xs) - .75, min(ys) - .75, max(xs) + .75, max(ys) + .75)); parts.append("extent")
    if not boxes: boxes, parts = [DEFAULT_BBOX], ["default"]
    bbox = (min(b[0] for b in boxes), min(b[1] for b in boxes), max(b[2] for b in boxes), max(b[3] for b in boxes))
    basis = "+".join(parts)
    xa, xb, ya, yb = frame(bbox)
    ya -= (yb - ya) * .25  # room below for the title band (map area stays the bbox)
    xm, xw = (xa + xb) / 2, (yb - ya) * W / H / 2; xa, xb = xm - xw, xm + xw
    fig = plt.figure(figsize=(W / DPI, H / DPI), dpi=DPI)
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(xa, xb); ax.set_ylim(ya, yb); ax.axis("off")
    ax.set_facecolor("#dfe3e2")
    ax.imshow(relief, extent=(RELIEF_BOX[0], RELIEF_BOX[2], my(RELIEF_BOX[1]), my(RELIEF_BOX[3])), zorder=0, interpolation="bilinear")
    for f in base["features"]:
        p = poly_path(f["geometry"])
        if p: ax.add_patch(PathPatch(p, fill=False, ec="#6b6b6b", lw=0.6, alpha=0.6, zorder=1))
    order = {z.replace("zone_", ""): i for i, z in enumerate(zs["draw_order_bottom_to_top"])}
    for f in sorted([f for f in feats if f.get("geometry")], key=lambda f: order.get((f.get("properties") or {}).get("zone") or "core", 2)):
        pr = f.get("properties") or {}; z = pr.get("zone"); g = f["geometry"]
        conf = pr.get("confidence")
        low = (conf is not None and float(conf) < thr) or (conf is None and str(pr.get("certainty", "")).lower() == "low")
        col = ZONE_COLOR.get(z, ZONE_COLOR[None])
        if g["type"] in ("Polygon", "MultiPolygon"):
            p = poly_path(g); zz = z or "core"
            if zz == "influence":  # feathered: stacked soft strokes + faint fill
                ax.add_patch(PathPatch(p, fc=col, ec="none", alpha=op["influence"], zorder=2))
                for lw, a in ((14, .05), (8, .07), (3, .09)):
                    ax.add_patch(PathPatch(p, fill=False, ec=col, lw=lw, alpha=a, zorder=2, joinstyle="round"))
            else:
                ax.add_patch(PathPatch(p, fc=col, ec="none", alpha=op.get(zz, .35), zorder=3))
                ax.add_patch(PathPatch(p, fill=False, ec=col, lw=1.6, ls=(0, (5, 3)) if zz == "claimed" else "-", alpha=.9, zorder=4))
            if low:
                ax.add_patch(PathPatch(p, fill=False, ec=col, lw=0, hatch="///", alpha=.45, zorder=4))
        elif g["type"] in ("LineString", "MultiLineString"):
            for ln in ([g["coordinates"]] if g["type"] == "LineString" else g["coordinates"]):
                ax.plot([a[0] for a in ln], [my(a[1]) for a in ln], color=col, lw=1.6, ls="--" if low else "-", zorder=4)
        elif g["type"] == "Point":
            x, y = g["coordinates"][0], my(g["coordinates"][1])
            if z == "contested":
                ax.scatter([x], [y], s=260, c=AMBER, alpha=op["contested"], edgecolors="#7a4f00", linewidths=1.5, zorder=6)
            else:
                ax.scatter([x], [y], s=60, c="white" if low else col, edgecolors=col, linewidths=1.5, zorder=5)
    # title band from data
    ax.add_patch(plt.Rectangle((0, 0), 1, .2, transform=ax.transAxes, fc="#1f1f1f", alpha=.78, zorder=10))
    name = era.get("name_en") or eid
    ax.text(.03, .125, name if len(name) < 70 else name[:67] + "…", transform=ax.transAxes, color="white", fontsize=26, weight="bold", va="center", zorder=11)
    ax.text(.03, .05, f"{yr(era['start'])} – {yr(era['end'])}", transform=ax.transAxes, color="#e8d9b0", fontsize=17, va="center", zorder=11)
    ax.text(.985, .05, "Sudan HistoMap · relief & borders: Natural Earth (PD)", transform=ax.transAxes, color="#bbbbbb", fontsize=10, ha="right", va="center", zorder=11)
    fig.savefig(out, dpi=DPI, metadata={"Software": None}); plt.close(fig)
    Image.open(out).convert("RGB").quantize(256, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE).save(out, optimize=True)
    return basis

def main():
    force = "--force" in sys.argv
    os.makedirs(OUT, exist_ok=True)
    man = json.load(open(MANIFEST)) if os.path.exists(MANIFEST) else {"images": {}}
    spec = json.load(open(SPEC)); base = json.load(open(BASEMAP))
    relief = None
    common = [os.path.abspath(__file__), SPEC, RELIEF, BASEMAP, FOCUS]
    built = skipped = 0
    for eid in sorted(json.load(open(FOCUS))["eras"]):
        ep, xp, out = J("data/eras", eid + ".json"), J("db/extents", eid + ".geojson"), os.path.join(OUT, eid + ".png")
        if not os.path.exists(ep): continue
        h = sha(common + [ep, xp])
        if not force and man["images"].get(eid, {}).get("inputs_sha256") == h and os.path.exists(out):
            skipped += 1; continue
        if relief is None:
            im = ImageEnhance.Color(Image.open(RELIEF).convert("RGB")).enhance(.35)
            im = ImageEnhance.Contrast(ImageEnhance.Brightness(im).enhance(1.9)).enhance(.75)
            relief = np.asarray(Image.blend(im, Image.new("RGB", im.size, (236, 232, 222)), .35))
        era = json.load(open(ep))
        try: feats = json.load(open(xp))["features"]
        except (OSError, ValueError, KeyError): feats = []  # missing or empty extent file
        basis = render(eid, era, feats, spec, relief, base, out)
        man["images"][eid] = {"png": f"img/og/{eid}.png", "inputs_sha256": h, "frame": basis}
        built += 1
    man["meta"] = {"script": "db/og/build_og.py", "size": [W, H], "note": "inputs_sha256 = sha256 of script, legend_spec, relief, basemap, era_focus, data/eras/<id>.json, db/extents/<id>.geojson"}
    json.dump(man, open(MANIFEST, "w"), indent=1, sort_keys=True)
    print(f"built {built}, skipped {skipped}, total {len(man['images'])}")

if __name__ == "__main__": main()
