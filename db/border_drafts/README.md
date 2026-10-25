# Border drafts (staging, NOT live) — bd-0.1, 2026-10-24

15 era files, 22 features (+ `_all_drafts.geojson`), built by `build_drafts.py`. Eras: a-group, c-group, middle-kingdom-egypt,
egyptian-new-kingdom-rule-in-nubia, ptolemaic-egypt, roman-byzantine-egypt, alodia-alwa, funj-sultanate-of-sennar,
ja-aliyyin, abdallab, tunjur, daju, restored-darfur (Ali Dinar), kingdom-of-taqali, musabba-at. All currently points-only.

Not drafted on purpose: Dinka/Nuer/Anuak (stay on Homelands layer), Beja, Zande, Wadai, Bornu, Garamantes, Punt, Sabaean,
Zagwe, rise-of-islam, Ottoman Hejaz, Late Period Egypt, Noba/X-Group, Suakin, Khartoum Neolithic/Mesolithic: no source
read this round supports a limit. War era: no control polygons without a UN/aid-agency cite (rule unchanged).

## Feature schema
`zone`: core | claimed | contested | influence · `confidence` 0–1 · `badges` (APPROXIMATE always; EDITORIAL forced when
confidence < 0.4) · `basis` (one-line reasoning, with page refs) · `sources[]` {id,citation,url} · `version` · `status`.
Geometry = hand-placed anchor points (most reused from the cited points already in `extents/*.json`) buffered in degrees
along the Nile or around a centre. The widths are editorial; that is why every feature carries APPROXIMATE.

## Gate before merge (Historian)
1. Check each `basis` page ref against the book; add a second source or keep SINGLE-SOURCE.
2. Resolve VERIFY items: Alwa southern limit, Roman withdrawal date, Ali Dinar west edge.
3. Clip corridors to the Natural Earth river/terrain mask (v0.2: buffer the NE 10m river line, not straight segments).
4. Append to `extents/<era>.json` with `extent_rendering.mode = "zones"`; run the offline verify.

## map.js implementation notes
- Layer order (bottom→top): relief basemap → influence → claimed → core → contested hatch → boundary lines →
  homelands → cities → labels → flags.
- Styles (reuse current purple `#7a6bd0` for control):
  core: fill-opacity .35, solid 1.2px stroke · claimed: fill-opacity .18, stroke-dasharray `4 3` (matches
  `control_extent_approx` legend swatch) · influence: no stroke, fill-opacity .08 with a radial/feathered edge
  (SVG `filter: blur(6px)` on a clipped copy, or a 3-step inset ring at .08/.05/.02) · contested: amber `#e0a63e`
  hatch, already the CONTESTED colour.
- Confidence hatch: one `<pattern id="lowconf">` 45° hairlines, 6px spacing, stroke `#e8eef2` opacity
  `= 0.5*(1-confidence)`; overlay on any zone with confidence < 0.5. Expose as a legend row "Low-confidence estimate".
- Legend: add rows zone_core / zone_claimed / zone_influence / zone_contested / low_confidence (EN+AR, AR marked * for review).
- Transitions: on era change, cross-fade outgoing zones (opacity →0, 350ms) and fade in new ones staged
  core→claimed→influence (+80ms each). If both eras share an id-matched zone, interpolate with flubber-style
  path morph or simply cross-fade. Respect `prefers-reduced-motion` (instant swap).
- Tap a zone → card shows zone, confidence as words (high ≥.7, medium ≥.4, low), badges, basis, sources.
- Performance: simplify to 0.02°; total drafts are a few KB. Lazy-load per era like `/lg/<id>.json`.
