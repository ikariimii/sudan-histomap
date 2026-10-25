# Legend / GIS handoff for the Web Lead (Sudan Map Designer, 2026-10-24)

Files (data only, no view code touched): `legend_spec.json` (symbol classes, uncertainty encoding, GIS furniture, six declarations), `eras/<era-slug>.json` (68, one per `data/periods.json` era; slug = ASCII-folded lowercase name, hyphenated, same as `db/extents/`), `build_legends.py` (rebuild after any data change: `python3 db/legends/build_legends.py`).

## Interactive legend
- On scrub, load `eras/<slug>.json`; render **only** rows in `symbol_classes_present`, with counts from `counts`. Never show a row for a class not drawn.
- Row hover → highlight all features of that `symbol_class`; feature hover → highlight its row (two-way).
- Row click → toggle that class. Layer group toggles from `interactive.layer_toggles` (extents, groups, cities, homelands, rivers, terrain, graticule). Homelands off by default (undated).
- Badge chips from `badges_present`; clicking a chip filters/outlines features with that badge, using `legend_spec.uncertainty_encoding`.
- Feature click → popup with `source_ids` (+ page/cite) resolved via `data/periods.json meta.sources`.
- "What changed" drawer: `interactive.what_changed` (vs previous era in same stream): extents/cities/capitals/groups added/removed. Null for the first era of a stream.
- Context card: `context.key_events_*` (cite `key_events_source_ids`), `control_limits_*` (cite `control_limits_source_ids`), `dating_note`.

## GIS furniture
- Credit/datum line always visible (collapsed to "WGS 84 · Web Mercator ⓘ" on mobile).
- Scale bar latitude-corrected; graticule 5°; north arrow only in equal-area mode.
- Projection switch: Web Mercator (default) ↔ LAEA 30°E 15°N for size comparison (e.g. MapLibre globe/custom projection or d3-geo `geoAzimuthalEqualArea().rotate([-30,-15])`). Show the disclosure sentence on switch.
- Contested: points/dashed lines only, amber hatch; never polygons owned by a state. South Sudan as separate neighbour from 2011-07-09.

## Accessibility & 390 px
- Legend becomes a bottom sheet (peek 56 px: era name + class icons; drag to full). Tap targets ≥44 px. Hover behaviours map to tap-and-hold.
- Colour never the only cue: every class has a distinct shape/dash (Okabe-Ito palette). Contrast ≥4.5:1 for text; `aria-pressed` on toggles; legend rows are buttons with `aria-label` including count; `lang="ar" dir="rtl"` for Arabic labels (flagged working translation).
- Respect `prefers-reduced-motion` for fades.

## PDF concept → feature
| Concept (El Hiloush / guide) | Feature |
|---|---|
| Six declarations; marginalia | `six_declarations`, credit line, info panel |
| Datum/ellipsoid named together; EPSG | WGS 84 / EPSG:4326 statement |
| Projection distorts; Mercator not for area | equal-area LAEA toggle + disclosure |
| Classification by scale | small-scale statement, no measurement claims |
| Visual hierarchy, figure-ground | `visual_hierarchy` ordering, muted basemap |
| Qualitative symbolisation, no ramps | Okabe-Ito hues + shapes per class |
| Generalisation disclosed | approximate extents dashed/feathered |
| Lineage: no layer without source | click-to-source popups, per-era source ids |
| Borders are claims | contested points/dashed lines policy |
| Legend explains every symbol | per-era `symbol_classes_present` |
| Hillshade not alone | terrain + hypsometric tint key |
| Pre-delivery checklist | `pre_delivery_checklist` |

## Known gaps
- `ruin` class currently never triggers: `visible_to` = last role end, so ruins vanish rather than persist as ruins. Decide whether to show them past their end.
- No river/terrain asset is committed yet; pick a PD/CC0/CC BY source (Natural Earth suggested), not done by me.
- Homelands have no dates, so they are not tied to eras.
