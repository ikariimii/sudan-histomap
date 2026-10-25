# Badge audit, db/extents (Sudan Map Designer, 2026-10-25)

238 features in 68 files. 'Cite' means any of cite, cites, sources, source or source_ids. 'hatch' means confidence < 0.5. 'mapped' means confidence came from the table below.

## Confidence mapping table

Approved by the Innovation Manager on 2026-10-25. It applies only to features that had no badge and only a `certainty` word.

| certainty | confidence | badges added |
|---|---|---|
| low | 0.3 | APPROXIMATE, DERIVED |
| medium | 0.6 | APPROXIMATE, DERIVED |
| high | not mapped (left unchanged) | none |

DERIVED means the numeric confidence comes from this table, not from a source. APPROXIMATE means the outline is a schematic or digitised shape, not a surveyed limit. Only the `confidence` and `badges` keys were added; geometry and every other property are byte-identical (checked by stripping the inserted text and comparing it with HEAD). The low-certainty features (0.3) now get the < 0.5 hatching.

Mapped: 117 features (78 low, 39 medium). Left unchanged: 33 'high' features with no badge, listed below.

## Flags

- **No cite:** 0 features. None.
- **No badge, certainty only (not mapped):** 33 features. abboud-military-regime #0 (high), abboud-military-regime #1 (high), al-bashir-ncp-ingaz-regime #4 (high), bornu-empire #0 (high), central-african-republic-ubangi-shari #5 (high), central-african-republic-ubangi-shari #6 (high), central-african-republic-ubangi-shari #7 (high), december-revolution-transition #0 (high), derg-federal-ethiopia #2 (high), eritrea-italian-colony-independent #3 (high), eritrea-italian-colony-independent #6 (high), french-chad-republic-of-chad #5 (high), french-chad-republic-of-chad #6 (high), independent-sudan-first-parliamentary-period #0 (high), libya-ottoman-italian-independent #2 (high), libya-ottoman-italian-independent #5 (high), libya-ottoman-italian-independent #6 (high), mamluk-sultanate #0 (high), mamluk-sultanate #1 (high), mamluk-sultanate #2 (high), mamluk-sultanate #3 (high), mamluk-sultanate #4 (high), mamluk-sultanate #5 (high), mamluk-sultanate #6 (high), mamluk-sultanate #7 (high), mamluk-sultanate #8 (high), nimeiry-era-democratic-republic-of-sudan #0 (high), ptolemaic-egypt #0 (high), republic-of-south-sudan #0 (high), roman-byzantine-egypt #0 (high), second-parliamentary-period #0 (high), transitional-third-parliamentary-period #0 (high), war-in-sudan-saf-vs-rsf #0 (high)
- **No badge and no certainty:** 0 features. None.

## Hover fields the Web Lead needs to show (view code is the Web Lead's; not edited here)

- `badges` (plus legacy `badge`) as chips, named as in legend_spec.json borders_legend.rows
- `confidence` with its word from zone_styling.confidence_badge, plus the hatch when < 0.5; if DERIVED, add 'from certainty table'; if there's no `confidence`, show `certainty`
- `zone` (core / claimed / influence / contested)
- `sources` / `source` / `cite`, with `pages` or `cite.page`, resolved via data/sources.json
- `basis_en` / `basis_ar`, `note`, and `editorial_note_en` when EDITORIAL is present
- `method` when DERIVED is present, and `license` for OHM-derived shapes
- CONTESTED points: both claims (uncertainty_encoding.CONTESTED)
- per-era legend rows: db/legends/eras/<id>.json, at layers.extents.borders_legend

## All features

| era | # | geometry | zone | badges | confidence | certainty | cite | flags |
|---|---|---|---|---|---|---|---|---|
| a-group-lower-nubia | 0 | Point |  | APPROXIMATE |  | low | yes |  |
| a-group-lower-nubia | 1 | Polygon | influence | APPROXIMATE, EDITORIAL, SINGLE-SOURCE | 0.35 | low | yes | hatch |
| abboud-military-regime | 0 | MultiPolygon |  |  |  | high | yes | NO BADGE (certainty only) |
| abboud-military-regime | 1 | Polygon |  |  |  | high | yes | NO BADGE (certainty only) |
| abdallab-chiefdom-funj-vassal | 0 | Point |  | APPROXIMATE |  | low | yes |  |
| abdallab-chiefdom-funj-vassal | 1 | Polygon | core | APPROXIMATE, EDITORIAL, SINGLE-SOURCE | 0.4 | medium | yes | hatch |
| al-bashir-ncp-ingaz-regime | 0 | Polygon |  | APPROXIMATE, DERIVED | 0.6 | medium | yes | mapped |
| al-bashir-ncp-ingaz-regime | 1 | Polygon |  | APPROXIMATE, DERIVED | 0.6 | medium | yes | mapped |
| al-bashir-ncp-ingaz-regime | 2 | Point |  | CONTESTED |  | medium | yes |  |
| al-bashir-ncp-ingaz-regime | 3 | Point |  | CONTESTED |  | medium | yes |  |
| al-bashir-ncp-ingaz-regime | 4 | MultiPolygon |  |  |  | high | yes | NO BADGE (certainty only) |
| al-bashir-ncp-ingaz-regime | 5 | MultiPolygon |  | APPROXIMATE, DERIVED | 0.6 | medium | yes | mapped |
| al-bashir-ncp-ingaz-regime | 6 | LineString |  | CONTESTED |  | medium | yes |  |
| al-bashir-ncp-ingaz-regime | 7 | LineString |  | APPROXIMATE, CONTESTED |  | medium | yes |  |
| al-bashir-ncp-ingaz-regime | 8 | LineString |  | APPROXIMATE, CONTESTED |  | medium | yes |  |
| alodia-alwa | 0 | Point |  | APPROXIMATE, DERIVED | 0.3 | low | yes | hatch; mapped |
| alodia-alwa | 1 | Polygon | core | APPROXIMATE, EDITORIAL | 0.4 | medium | yes | hatch |
| alodia-alwa | 2 | MultiPolygon | claimed | APPROXIMATE, EDITORIAL | 0.25 | low | yes | hatch |
| anglo-egyptian-sudan-condominium | 0 | MultiPolygon |  | APPROXIMATE, DERIVED | 0.3 | low | yes | hatch; mapped |
| anglo-egyptian-sudan-condominium | 1 | MultiPolygon |  | APPROXIMATE, DERIVED | 0.3 | low | yes | hatch; mapped |
| anglo-egyptian-sudan-condominium | 2 | MultiPolygon |  | APPROXIMATE, DERIVED | 0.3 | low | yes | hatch; mapped |
| anglo-egyptian-sudan-condominium | 3 | MultiPolygon |  | APPROXIMATE, DERIVED | 0.3 | low | yes | hatch; mapped |
| anglo-egyptian-sudan-condominium | 4 | MultiPolygon |  | APPROXIMATE, DERIVED | 0.3 | low | yes | hatch; mapped |
| anglo-egyptian-sudan-condominium | 5 | MultiPolygon |  | APPROXIMATE, DERIVED | 0.3 | low | yes | hatch; mapped |
| anuak-anywaa-communities | 0 | Point |  | APPROXIMATE |  | low | yes |  |
| beja-red-sea-hills-peoples | 0 | Point |  | APPROXIMATE |  | low | yes |  |
| bornu-empire | 0 | Point |  |  |  | high | yes | NO BADGE (certainty only) |
| bornu-empire | 1 | Point |  | APPROXIMATE, DERIVED | 0.3 | low | yes | hatch; mapped |
| british-occupied-kingdom-of-egypt | 0 | MultiPolygon |  | APPROXIMATE, DERIVED | 0.6 | medium | yes | mapped |
| british-occupied-kingdom-of-egypt | 1 | MultiPolygon |  | APPROXIMATE, DERIVED | 0.6 | medium | yes | mapped |
| british-occupied-kingdom-of-egypt | 2 | MultiPolygon |  | APPROXIMATE, DERIVED | 0.6 | medium | yes | mapped |
| british-occupied-kingdom-of-egypt | 3 | MultiPolygon |  | APPROXIMATE, DERIVED | 0.6 | medium | yes | mapped |
| british-occupied-kingdom-of-egypt | 4 | MultiPolygon |  | APPROXIMATE, DERIVED | 0.6 | medium | yes | mapped |
| c-group-lower-nubia | 0 | Point |  | APPROXIMATE |  | low | yes |  |
| c-group-lower-nubia | 1 | Polygon | influence | APPROXIMATE, EDITORIAL, SINGLE-SOURCE | 0.35 | low | yes | hatch |
| central-african-republic-ubangi-shari | 0 | none |  | APPROXIMATE, DERIVED | 0.3 | low | yes | hatch; mapped |
| central-african-republic-ubangi-shari | 1 | Polygon |  | APPROXIMATE |  | low | yes |  |
| central-african-republic-ubangi-shari | 2 | Polygon |  | APPROXIMATE |  | low | yes |  |
| central-african-republic-ubangi-shari | 3 | Polygon |  | APPROXIMATE |  | low | yes |  |
| central-african-republic-ubangi-shari | 4 | none |  | APPROXIMATE, DERIVED | 0.3 | low | yes | hatch; mapped |
| central-african-republic-ubangi-shari | 5 | Polygon |  |  |  | high | yes | NO BADGE (certainty only) |
| central-african-republic-ubangi-shari | 6 | Polygon |  |  |  | high | yes | NO BADGE (certainty only) |
| central-african-republic-ubangi-shari | 7 | Polygon |  |  |  | high | yes | NO BADGE (certainty only) |
| daju-kingdom | 0 | Point |  | APPROXIMATE, DERIVED | 0.3 | low | yes | hatch; mapped |
| daju-kingdom | 1 | Polygon | core | APPROXIMATE, EDITORIAL | 0.3 | low | yes | hatch |
| december-revolution-transition | 0 | Polygon |  |  |  | high | yes | NO BADGE (certainty only) |
| december-revolution-transition | 1 | Point |  | CONTESTED |  | medium | yes |  |
| december-revolution-transition | 2 | Point |  | CONTESTED |  | medium | yes |  |
| december-revolution-transition | 3 | MultiPolygon |  | APPROXIMATE, DERIVED | 0.6 | medium | yes | mapped |
| december-revolution-transition | 4 | Polygon |  | APPROXIMATE, DERIVED | 0.6 | medium | yes | mapped |
| december-revolution-transition | 5 | LineString |  | CONTESTED |  | medium | yes |  |
| december-revolution-transition | 6 | LineString |  | APPROXIMATE, CONTESTED |  | medium | yes |  |
| december-revolution-transition | 7 | LineString |  | APPROXIMATE, CONTESTED |  | medium | yes |  |
| derg-federal-ethiopia | 0 | MultiPolygon |  | APPROXIMATE, DERIVED | 0.6 | medium | yes | mapped |
| derg-federal-ethiopia | 1 | Polygon |  | APPROXIMATE, DERIVED | 0.6 | medium | yes | mapped |
| derg-federal-ethiopia | 2 | Polygon |  |  |  | high | yes | NO BADGE (certainty only) |
| derg-federal-ethiopia | 3 | none |  | CONTESTED |  | low | yes |  |
| derg-federal-ethiopia | 4 | Point |  | CONTESTED |  | low | yes |  |
| dinka-jieng-communities | 0 | Point |  | APPROXIMATE |  | low | yes |  |
| early-dynastic-old-kingdom-egypt | 0 | Point |  | APPROXIMATE, DERIVED | 0.6 | medium | yes | mapped |
| early-dynastic-old-kingdom-egypt | 1 | Point |  | APPROXIMATE, DERIVED | 0.3 | low | yes | hatch; mapped |
| egyptian-new-kingdom-rule-in-nubia | 0 | Point |  | APPROXIMATE, DERIVED | 0.6 | medium | yes | mapped |
| egyptian-new-kingdom-rule-in-nubia | 1 | Point |  | APPROXIMATE, DERIVED | 0.6 | medium | yes | mapped |
| egyptian-new-kingdom-rule-in-nubia | 2 | Point |  | APPROXIMATE, DERIVED | 0.3 | low | yes | hatch; mapped |
| egyptian-new-kingdom-rule-in-nubia | 3 | Polygon | core | APPROXIMATE, SINGLE-SOURCE | 0.6 | medium | yes |  |
| egyptian-new-kingdom-rule-in-nubia | 4 | Polygon | claimed | APPROXIMATE | 0.6 | medium | yes |  |
| eritrea-italian-colony-independent | 0 | MultiPolygon |  | APPROXIMATE, DERIVED | 0.6 | medium | yes | mapped |
| eritrea-italian-colony-independent | 1 | none |  | APPROXIMATE, DERIVED | 0.3 | low | yes | hatch; mapped |
| eritrea-italian-colony-independent | 2 | MultiPolygon |  | APPROXIMATE, DERIVED | 0.6 | medium | yes | mapped |
| eritrea-italian-colony-independent | 3 | MultiPolygon |  |  |  | high | yes | NO BADGE (certainty only) |
| eritrea-italian-colony-independent | 4 | MultiPolygon |  | APPROXIMATE, DERIVED | 0.6 | medium | yes | mapped |
| eritrea-italian-colony-independent | 5 | Polygon |  | APPROXIMATE, DERIVED | 0.6 | medium | yes | mapped |
| eritrea-italian-colony-independent | 6 | MultiPolygon |  |  |  | high | yes | NO BADGE (certainty only) |
| eritrea-italian-colony-independent | 7 | Point |  | CONTESTED |  | low | yes |  |
| ethiopian-empire-solomonic | 0 | Point |  | APPROXIMATE, DERIVED | 0.6 | medium | yes | mapped |
| ethiopian-empire-solomonic | 1 | Polygon |  | APPROXIMATE, DERIVED | 0.3 | low | yes | hatch; mapped |
| ethiopian-empire-solomonic | 2 | Polygon |  | APPROXIMATE, DERIVED | 0.3 | low | yes | hatch; mapped |
| ethiopian-empire-solomonic | 3 | Polygon |  | APPROXIMATE, DERIVED | 0.3 | low | yes | hatch; mapped |
| ethiopian-empire-solomonic | 4 | Polygon |  | APPROXIMATE, DERIVED | 0.3 | low | yes | hatch; mapped |
| ethiopian-empire-solomonic | 5 | MultiPolygon |  | APPROXIMATE, DERIVED | 0.3 | low | yes | hatch; mapped |
| ethiopian-empire-solomonic | 6 | MultiPolygon |  | APPROXIMATE, DERIVED | 0.3 | low | yes | hatch; mapped |
| french-chad-republic-of-chad | 0 | Polygon |  | APPROXIMATE |  | low | yes |  |
| french-chad-republic-of-chad | 1 | Polygon |  | APPROXIMATE |  | low | yes |  |
| french-chad-republic-of-chad | 2 | Polygon |  | APPROXIMATE |  | low | yes |  |
| french-chad-republic-of-chad | 3 | Polygon |  | APPROXIMATE |  | low | yes |  |
| french-chad-republic-of-chad | 4 | none |  | APPROXIMATE, DERIVED | 0.3 | low | yes | hatch; mapped |
| french-chad-republic-of-chad | 5 | Polygon |  |  |  | high | yes | NO BADGE (certainty only) |
| french-chad-republic-of-chad | 6 | Polygon |  |  |  | high | yes | NO BADGE (certainty only) |
| french-chad-republic-of-chad | 7 | Point |  | CONTESTED |  | low | yes |  |
| funj-sultanate-of-sennar | 0 | Point |  | APPROXIMATE, DERIVED | 0.6 | medium | yes | mapped |
| funj-sultanate-of-sennar | 1 | Point |  | APPROXIMATE, DERIVED | 0.3 | low | yes | hatch; mapped |
| funj-sultanate-of-sennar | 2 | Point |  | APPROXIMATE, DERIVED | 0.3 | low | yes | hatch; mapped |
| funj-sultanate-of-sennar | 3 | Point |  | APPROXIMATE, DERIVED | 0.3 | low | yes | hatch; mapped |
| funj-sultanate-of-sennar | 4 | Point |  | APPROXIMATE, DERIVED | 0.3 | low | yes | hatch; mapped |
| funj-sultanate-of-sennar | 5 | Polygon | core | APPROXIMATE | 0.6 | medium | yes |  |
| garamantes-fezzan | 0 | Point |  | APPROXIMATE |  | low | yes |  |
| independent-sudan-first-parliamentary-period | 0 | MultiPolygon |  |  |  | high | yes | NO BADGE (certainty only) |
| islamic-egypt-rashidunfatimidayyubid | 0 | Point |  | APPROXIMATE, DERIVED | 0.6 | medium | yes | mapped |
| islamic-egypt-rashidunfatimidayyubid | 1 | Point |  | APPROXIMATE, DERIVED | 0.6 | medium | yes | mapped |
| ja-aliyyin-kingdom-sa-dab-funj-vassal | 0 | Point |  | APPROXIMATE |  | low | yes |  |
| ja-aliyyin-kingdom-sa-dab-funj-vassal | 1 | Point |  | APPROXIMATE |  | low | yes |  |
| ja-aliyyin-kingdom-sa-dab-funj-vassal | 2 | Polygon | core | APPROXIMATE, EDITORIAL | 0.45 | medium | yes | hatch |
| kanem-empire | 0 | Polygon |  | APPROXIMATE, DERIVED | 0.3 | low | yes | hatch; mapped |
| khartoum-neolithic-shaheinab | 0 | Point |  | SINGLE-SOURCE |  | low | yes |  |
| khartoum-neolithic-shaheinab | 1 | Point |  | APPROXIMATE |  | low | yes |  |
| kingdom-of-aksum | 0 | MultiPolygon |  | APPROXIMATE, DERIVED | 0.3 | low | yes | hatch; mapped |
| kingdom-of-aksum | 1 | MultiPolygon |  | APPROXIMATE, DERIVED | 0.6 | medium | yes | mapped |
| kingdom-of-aksum | 2 | MultiPolygon |  | APPROXIMATE, DERIVED | 0.6 | medium | yes | mapped |
| kingdom-of-aksum | 3 | MultiPolygon |  | APPROXIMATE, DERIVED | 0.3 | low | yes | hatch; mapped |
| kingdom-of-aksum | 4 | MultiPolygon |  | APPROXIMATE, DERIVED | 0.3 | low | yes | hatch; mapped |
| kingdom-of-kerma | 0 | MultiPolygon |  | APPROXIMATE, DERIVED | 0.3 | low | yes | hatch; mapped |
| kingdom-of-kush-meroitic-period | 0 | Polygon |  | APPROXIMATE, DERIVED | 0.3 | low | yes | hatch; mapped |
| kingdom-of-kush-meroitic-period | 1 | Point |  | APPROXIMATE, DERIVED | 0.3 | low | yes | hatch; mapped |
| kingdom-of-kush-meroitic-period | 2 | Point |  | APPROXIMATE, DERIVED | 0.3 | low | yes | hatch; mapped |
| kingdom-of-kush-meroitic-period | 3 | Point |  | APPROXIMATE, DERIVED | 0.3 | low | yes | hatch; mapped |
| kingdom-of-kush-meroitic-period | 4 | Point |  | APPROXIMATE, DERIVED | 0.3 | low | yes | hatch; mapped |
| kingdom-of-kush-napatan-period | 0 | Polygon |  | APPROXIMATE, DERIVED | 0.3 | low | yes | hatch; mapped |
| kingdom-of-kush-napatan-period | 1 | MultiPolygon |  | APPROXIMATE, DERIVED | 0.3 | low | yes | hatch; mapped |
| kingdom-of-kush-napatan-period | 2 | Point |  | APPROXIMATE, DERIVED | 0.3 | low | yes | hatch; mapped |
| kingdom-of-taqali | 0 | Point |  | APPROXIMATE, DERIVED | 0.3 | low | yes | hatch; mapped |
| kingdom-of-taqali | 1 | Polygon | core | APPROXIMATE, EDITORIAL | 0.4 | medium | yes | hatch |
| land-of-punt-d-mt | 0 | Point |  | APPROXIMATE |  | low | yes |  |
| late-period-persian-egypt | 0 | Point |  | APPROXIMATE, DERIVED | 0.6 | medium | yes | mapped |
| libya-ottoman-italian-independent | 0 | Point |  | APPROXIMATE, DERIVED | 0.3 | low | yes | hatch; mapped |
| libya-ottoman-italian-independent | 1 | Point |  | APPROXIMATE, DERIVED | 0.3 | low | yes | hatch; mapped |
| libya-ottoman-italian-independent | 2 | Polygon |  |  |  | high | yes | NO BADGE (certainty only) |
| libya-ottoman-italian-independent | 3 | Polygon |  | APPROXIMATE |  | medium | yes |  |
| libya-ottoman-italian-independent | 4 | Polygon |  | APPROXIMATE |  | medium | yes |  |
| libya-ottoman-italian-independent | 5 | Polygon |  |  |  | high | yes | NO BADGE (certainty only) |
| libya-ottoman-italian-independent | 6 | Polygon |  |  |  | high | yes | NO BADGE (certainty only) |
| libya-ottoman-italian-independent | 7 | none |  | APPROXIMATE, DERIVED | 0.3 | low | yes | hatch; mapped |
| libya-ottoman-italian-independent | 8 | Point |  | CONTESTED |  | low | yes |  |
| mahdist-state-mahdiyya | 0 | Polygon |  | APPROXIMATE, DERIVED | 0.3 | low | yes | hatch; mapped |
| makuria | 0 | Polygon |  | APPROXIMATE, DERIVED | 0.3 | low | yes | hatch; mapped |
| makuria | 1 | Polygon |  | APPROXIMATE, DERIVED | 0.3 | low | yes | hatch; mapped |
| makuria | 2 | Polygon |  | APPROXIMATE, DERIVED | 0.3 | low | yes | hatch; mapped |
| makuria | 3 | Polygon |  | APPROXIMATE, DERIVED | 0.3 | low | yes | hatch; mapped |
| makuria | 4 | Point |  | APPROXIMATE, DERIVED | 0.3 | low | yes | hatch; mapped |
| makuria | 5 | Point |  | APPROXIMATE, DERIVED | 0.3 | low | yes | hatch; mapped |
| makuria | 6 | Point |  | APPROXIMATE, DERIVED | 0.3 | low | yes | hatch; mapped |
| mamluk-sultanate | 0 | MultiPolygon |  |  |  | high | yes | NO BADGE (certainty only) |
| mamluk-sultanate | 1 | MultiPolygon |  |  |  | high | yes | NO BADGE (certainty only) |
| mamluk-sultanate | 2 | MultiPolygon |  |  |  | high | yes | NO BADGE (certainty only) |
| mamluk-sultanate | 3 | MultiPolygon |  |  |  | high | yes | NO BADGE (certainty only) |
| mamluk-sultanate | 4 | MultiPolygon |  |  |  | high | yes | NO BADGE (certainty only) |
| mamluk-sultanate | 5 | MultiPolygon |  |  |  | high | yes | NO BADGE (certainty only) |
| mamluk-sultanate | 6 | MultiPolygon |  |  |  | high | yes | NO BADGE (certainty only) |
| mamluk-sultanate | 7 | MultiPolygon |  |  |  | high | yes | NO BADGE (certainty only) |
| mamluk-sultanate | 8 | MultiPolygon |  |  |  | high | yes | NO BADGE (certainty only) |
| mamluk-sultanate | 9 | Point |  | APPROXIMATE, DERIVED | 0.3 | low | yes | hatch; mapped |
| mamluk-sultanate | 10 | Point |  | APPROXIMATE, DERIVED | 0.3 | low | yes | hatch; mapped |
| middle-kingdom-egypt | 0 | Point |  | APPROXIMATE, DERIVED | 0.6 | medium | yes | mapped |
| middle-kingdom-egypt | 1 | Point |  | APPROXIMATE, DERIVED | 0.6 | medium | yes | mapped |
| middle-kingdom-egypt | 2 | Polygon | core | APPROXIMATE, DERIVED, SINGLE-SOURCE | 0.7 | high | yes |  |
| middle-kingdom-egypt | 3 | Polygon | claimed | APPROXIMATE, SINGLE-SOURCE | 0.6 | medium | yes |  |
| musabba-at-sultanate-kordofan | 0 | Point |  | APPROXIMATE, DERIVED | 0.3 | low | yes | hatch; mapped |
| musabba-at-sultanate-kordofan | 1 | Polygon | influence | APPROXIMATE, EDITORIAL | 0.3 | low | yes | hatch |
| new-kingdom-egypt | 0 | Point |  | SINGLE-SOURCE |  | low | yes |  |
| new-kingdom-egypt | 1 | Point |  | SINGLE-SOURCE |  | low | yes |  |
| new-kingdom-egypt | 2 | Point |  | APPROXIMATE, DERIVED | 0.6 | medium | yes | mapped |
| nimeiry-era-democratic-republic-of-sudan | 0 | Polygon |  |  |  | high | yes | NO BADGE (certainty only) |
| noba-x-group-ballana-culture | 0 | Point |  | APPROXIMATE, DERIVED | 0.3 | low | yes | hatch; mapped |
| noba-x-group-ballana-culture | 1 | Point |  | APPROXIMATE, DERIVED | 0.3 | low | yes | hatch; mapped |
| nobadia | 0 | Polygon |  | APPROXIMATE, DERIVED | 0.3 | low | yes | hatch; mapped |
| nuer-naath-communities | 0 | Point |  | APPROXIMATE |  | low | yes |  |
| nuer-naath-communities | 1 | Point |  | APPROXIMATE |  | low | yes |  |
| ottoman-egypt-muhammad-ali-dynasty | 0 | MultiPolygon |  | APPROXIMATE, DERIVED | 0.3 | low | yes | hatch; mapped |
| ottoman-egypt-muhammad-ali-dynasty | 1 | MultiPolygon |  | APPROXIMATE, DERIVED | 0.3 | low | yes | hatch; mapped |
| ottoman-egypt-muhammad-ali-dynasty | 2 | MultiPolygon |  | APPROXIMATE, DERIVED | 0.3 | low | yes | hatch; mapped |
| ottoman-egypt-muhammad-ali-dynasty | 3 | MultiPolygon |  | APPROXIMATE, DERIVED | 0.3 | low | yes | hatch; mapped |
| ottoman-hejaz-saudi-state | 0 | Point |  | APPROXIMATE |  | low | yes |  |
| ptolemaic-egypt | 0 | Point |  |  |  | high | yes | NO BADGE (certainty only) |
| ptolemaic-egypt | 1 | Point |  | APPROXIMATE, DERIVED | 0.3 | low | yes | hatch; mapped |
| ptolemaic-egypt | 2 | Polygon | core | APPROXIMATE, DERIVED | 0.75 | high | yes |  |
| ptolemaic-egypt | 3 | Point | contested | APPROXIMATE, CONTESTED | 0.4 | medium | yes | hatch |
| republic-of-egypt | 0 | MultiPolygon |  | APPROXIMATE, DERIVED | 0.6 | medium | yes | mapped |
| republic-of-egypt | 1 | MultiPolygon |  | APPROXIMATE, DERIVED | 0.6 | medium | yes | mapped |
| republic-of-egypt | 2 | MultiPolygon |  | APPROXIMATE, DERIVED | 0.6 | medium | yes | mapped |
| republic-of-egypt | 3 | MultiPolygon |  | APPROXIMATE, DERIVED | 0.6 | medium | yes | mapped |
| republic-of-egypt | 4 | Polygon |  | APPROXIMATE, DERIVED | 0.6 | medium | yes | mapped |
| republic-of-egypt | 5 | Polygon |  | APPROXIMATE, DERIVED | 0.6 | medium | yes | mapped |
| republic-of-south-sudan | 0 | Polygon |  |  |  | high | yes | NO BADGE (certainty only) |
| republic-of-south-sudan | 1 | Point |  | CONTESTED |  | medium | yes |  |
| republic-of-south-sudan | 2 | Point |  | CONTESTED |  | medium | yes |  |
| republic-of-south-sudan | 3 | Point |  | CONTESTED |  | medium | yes |  |
| republic-of-south-sudan | 4 | LineString |  | CONTESTED |  | medium | yes |  |
| republic-of-south-sudan | 5 | LineString |  | APPROXIMATE, CONTESTED |  | medium | yes |  |
| republic-of-south-sudan | 6 | LineString |  | APPROXIMATE, CONTESTED |  | medium | yes |  |
| restored-darfur-sultanate-ali-dinar | 0 | Point |  | APPROXIMATE, DERIVED | 0.3 | low | yes | hatch; mapped |
| restored-darfur-sultanate-ali-dinar | 1 | Polygon | core | APPROXIMATE | 0.5 | medium | yes |  |
| restored-darfur-sultanate-ali-dinar | 2 | Point | contested | APPROXIMATE, CONTESTED | 0.4 | medium | yes | hatch |
| rise-of-islam-caliphates | 0 | Point |  | APPROXIMATE |  | low | yes |  |
| roman-byzantine-egypt | 0 | Point |  |  |  | high | yes | NO BADGE (certainty only) |
| roman-byzantine-egypt | 1 | Point |  | APPROXIMATE, DERIVED | 0.6 | medium | yes | mapped |
| roman-byzantine-egypt | 2 | Point |  | APPROXIMATE, DERIVED | 0.3 | low | yes | hatch; mapped |
| roman-byzantine-egypt | 3 | Polygon | core | APPROXIMATE, DERIVED, SINGLE-SOURCE | 0.75 | high | yes |  |
| roman-byzantine-egypt | 4 | Polygon | claimed | APPROXIMATE | 0.5 | medium | yes |  |
| sabaean-south-arabian-kingdoms | 0 | Point |  | APPROXIMATE |  | low | yes |  |
| second-parliamentary-period | 0 | Polygon |  |  |  | high | yes | NO BADGE (certainty only) |
| shilluk-kingdom | 0 | Polygon |  | APPROXIMATE, DERIVED | 0.3 | low | yes | hatch; mapped |
| southern-sudan-under-condominium-sudan | 0 | Polygon |  | APPROXIMATE |  | low | yes |  |
| southern-sudan-under-condominium-sudan | 1 | Polygon |  | APPROXIMATE |  | low | yes |  |
| southern-sudan-under-condominium-sudan | 2 | Polygon |  | APPROXIMATE, SINGLE-SOURCE |  | low | yes |  |
| southern-sudan-under-condominium-sudan | 3 | Polygon |  | APPROXIMATE |  | low | yes |  |
| southern-sudan-under-condominium-sudan | 4 | Point |  | CONTESTED |  | medium | yes |  |
| southern-sudan-under-condominium-sudan | 5 | Point |  | CONTESTED |  | medium | yes |  |
| southern-sudan-under-condominium-sudan | 6 | Point |  | CONTESTED |  | medium | yes |  |
| suakin-red-sea-port-beja-ottoman | 0 | Point |  | APPROXIMATE |  | low | yes |  |
| sultanate-of-darfur-keira | 0 | Polygon |  | APPROXIMATE, DERIVED | 0.3 | low | yes | hatch; mapped |
| sultanate-of-darfur-keira | 1 | Polygon |  | APPROXIMATE, DERIVED | 0.3 | low | yes | hatch; mapped |
| sultanate-of-darfur-keira | 2 | Polygon |  | APPROXIMATE, DERIVED | 0.3 | low | yes | hatch; mapped |
| sultanate-of-darfur-keira | 3 | Point |  | APPROXIMATE, DERIVED | 0.3 | low | yes | hatch; mapped |
| sultanate-of-darfur-keira | 4 | Point |  | APPROXIMATE, DERIVED | 0.3 | low | yes | hatch; mapped |
| sultanate-of-darfur-keira | 5 | Point |  | APPROXIMATE, DERIVED | 0.3 | low | yes | hatch; mapped |
| sultanate-of-darfur-keira | 6 | Point |  | APPROXIMATE, DERIVED | 0.3 | low | yes | hatch; mapped |
| transitional-third-parliamentary-period | 0 | Polygon |  |  |  | high | yes | NO BADGE (certainty only) |
| tunjur-kingdom | 0 | Point |  | APPROXIMATE, DERIVED | 0.3 | low | yes | hatch; mapped |
| tunjur-kingdom | 1 | Polygon | core | APPROXIMATE, EDITORIAL | 0.35 | low | yes | hatch |
| turkiyya-ottoman-egyptian-rule | 0 | MultiPolygon |  | APPROXIMATE, DERIVED | 0.3 | low | yes | hatch; mapped |
| turkiyya-ottoman-egyptian-rule | 1 | MultiPolygon |  | APPROXIMATE, DERIVED | 0.3 | low | yes | hatch; mapped |
| turkiyya-ottoman-egyptian-rule | 2 | Point |  | APPROXIMATE, DERIVED | 0.3 | low | yes | hatch; mapped |
| wadai-sultanate | 0 | Point |  | APPROXIMATE, DERIVED | 0.3 | low | yes | hatch; mapped |
| wadai-sultanate | 1 | Point |  | APPROXIMATE, DERIVED | 0.3 | low | yes | hatch; mapped |
| war-in-sudan-saf-vs-rsf | 0 | Polygon |  |  |  | high | yes | NO BADGE (certainty only) |
| war-in-sudan-saf-vs-rsf | 1 | Point |  | CONTESTED |  | medium | yes |  |
| war-in-sudan-saf-vs-rsf | 2 | Point |  | CONTESTED |  | medium | yes |  |
| war-in-sudan-saf-vs-rsf | 3 | MultiPolygon |  | APPROXIMATE, DERIVED | 0.6 | medium | yes | mapped |
| war-in-sudan-saf-vs-rsf | 4 | Polygon |  | APPROXIMATE, DERIVED | 0.6 | medium | yes | mapped |
| war-in-sudan-saf-vs-rsf | 5 | Point |  | REPORTED |  | low | yes |  |
| war-in-sudan-saf-vs-rsf | 6 | Point |  | REPORTED |  | medium | yes |  |
| war-in-sudan-saf-vs-rsf | 7 | none |  | REPORTED |  | low | yes |  |
| war-in-sudan-saf-vs-rsf | 8 | none |  | REPORTED |  | low | yes |  |
| war-in-sudan-saf-vs-rsf | 9 | LineString |  | CONTESTED |  | medium | yes |  |
| war-in-sudan-saf-vs-rsf | 10 | LineString |  | APPROXIMATE, CONTESTED |  | medium | yes |  |
| war-in-sudan-saf-vs-rsf | 11 | LineString |  | APPROXIMATE, CONTESTED |  | medium | yes |  |
| zagwe-dynasty | 0 | Point |  | APPROXIMATE |  | low | yes |  |
| zande-kingdoms | 0 | Point |  | APPROXIMATE, DERIVED | 0.6 | medium | yes | mapped |
| zande-kingdoms | 1 | Point |  | APPROXIMATE, DERIVED | 0.3 | low | yes | hatch; mapped |
