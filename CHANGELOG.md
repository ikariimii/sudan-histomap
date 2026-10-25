# Changelog

Site changes for sudan.indomando.com (built from `web/` by `web/build.py`). Newest first.

## 2026-10-24 (one continuous map)
- Open line features (LineString/MultiLineString) are now drawn in the control and group layers: never filled, dashed when the feature says so (PCA 2009 Abyei award lines), arrowheads only on arrows; each line opens its citation, source pins and badges on tap.

- The site root `/` is now one full-screen map of all 68 eras. A timeline scrubber, the arrow buttons, the arrow keys or a swipe on the card moves between eras; these are mirrored in Arabic. Matching control areas morph from one era to the next and everything else crossfades. Animation is off under reduced motion. Pinch or scroll zooms the map, and a reset button returns to the full view.
- Each era's story card sits in a bottom sheet with peek, half and full sizes; on desktop it becomes a side panel. The card keeps every badge the era pages had: geometry state, Arabic under review, regional context, REPORTED/CONTESTED/SINGLE-SOURCE, CINC and EDITORIAL. It also keeps the events, culture, economy, power and sources sections and the dating note. There are no tables, and nothing scrolls sideways at 390px.
- Eras with several dated snapshots get a "Year within era" slider. Tapping an area or point shows its label, badge, certainty, dates and citation. Labels are thinned by priority and use leader lines, as on the old era map; labels that don't fit are listed under the card.
- South Sudan is drawn as a neighbouring state from 2011 and as part of Sudan before that.
- Layers you can turn on and off: Areas of control, Peoples, Relations and Population. The layers are built from the delivered data files:
  - Peoples: db/group_layers. Points are keyed by stable ID, so they glide between eras.
  - Relations: arrows coloured by type (alliance, conflict, trade, subjugation, migration), with a legend. Low certainty is drawn dashed. Relations that have no anchor are listed as text with the reason.
  - Population: db/population.json, shown as a sparkline plus the era figure, range, badges, territory, caveat and sources.
  - Every item shows its own badges and sources. Where an era has no data for a layer, the card says "Research in progress".
- Deep links: `?era=<id>`, `?lang=ar` and `?layers=` can be combined. Old URLs are now static redirects, with a meta refresh and a JS fallback, to the matching map view: era pages (EN and AR), chapters, `/eras/`, `/compare/`, `/ar/`, `era.html`, `eras.html`, and `histomap.html` without tool parameters. The share pages at /eras/<id>/ keep their OG cards. `histomap.html` with lens/diff/poster/print parameters still opens the tool.
- First load is about 245KB uncompressed and about 95KB gzipped: a d3 subset bundle, a simplified basemap and one era card.

## 2026-10-24 (regional power visual, mobile legibility)

- Regional power: the CINC line shows the 'CINC share' label and the COW NMC v6.0 citation from the data's own source ID (COW_NMC6). Where the data's null_reason is 'data ends 2016' (war era, December revolution), it says so (Arabic 'تنتهي البيانات عام ٢٠١٦').
- Editorial scores in `regional_power` (Kush 25th Dynasty 0.9, Mahdist state 0.9) are shown separately, with a blue EDITORIAL badge (Arabic 'تقييم تحريري', pending native review), a 0–1 bar, and the data's basis and method. Unscored actors keep 'Research in progress'.
- Geometry states: eras with sourced points but no polygon (28) now show 'Located by points, no sourced border' (Arabic pending native review) on the map, the era page and era lists. 'Border not yet mapped' is kept for the 9 eras with no geometry at all.
- Map badges use 11px text.
- Era pages: where the data has the approved, merged `power_cinc_share` (modern eras only), a compact bar shows each actor's CINC share, with years, method flag and citation (Arabic numerals on Arabic pages). Rows without a value keep 'Research in progress' with the data's null reason. Proposal scores (db/regional_power_scores_proposal.*) are not used.
- Chapter pages with scored eras get a collapsible comparison strip.
- Map: on narrow screens the REPORTED/CONTESTED/SINGLE-SOURCE map badge text is scaled up so it stays legible; Arabic map tooltip source citations are isolated left-to-right, so mixed-direction punctuation no longer jumbles.

## 2026-10-24 (single-source badge)

- Points the data badges 'SINGLE-SOURCE (Wikipedia)' (Pi-Ramesses, Kurgus frontier) show an amber badge in the same style as REPORTED and CONTESTED; Arabic 'مصدر واحد' is pending native review.

## 2026-10-24 (new extents: contested points, reference points)

- Rebuilt with the new extents (Egypt stream, modern-neighbour eras, dated reference points). Places the data badges CONTESTED (Badme, Aouzou) now show a purple 'CONTESTED' / 'متنازع عليها' badge on the map label, in the hover title, in the list under the map and on era pages, instead of the raw '[CONTESTED]' text. Dated reference points keep their own labels and dates from the data.

## 2026-10-24 (HTTPS, border state)

- Era pages and chapter maps now say 'Border not yet mapped' / 'الحدود لم تُرسم بعد' on the map itself when an era has no sourced border polygon, instead of a blank or missing map. This one badge replaces the old 'area: research in progress' note under chapter maps; the explanation under era maps stays as plain text. Self-links were already all https://sudan.indomando.com (none on http:// or github.io).

## 2026-10-20 (explorer: Arabic review badge)

- The explorer's era view (era.html) and the histomap details panel show the same 'Arabic under review' / 'الترجمة العربية قيد المراجعة' badge, driven by the WORKING TRANSLATION entry in the era's flags (prominent in Arabic, subtle in English).

## 2026-10-20 (chapters index)

- New chapters index at /chapters/ and /ar/chapters/ (all 7 chapters with dates, era counts, the interaction line and in-progress counts), linked from the header and from chapter and era breadcrumbs, with its own OG card and sitemap entries.
- Era pages whose data carries the 'WORKING TRANSLATION – needs native Arabic review' flag show a small 'Arabic under review' / 'الترجمة العربية قيد المراجعة' badge (subtler on English pages).

## 2026-10-20 (point labels)

- Fixed: a point label that had to move away from its marker could never be placed, because its own marker counted as an obstacle for its leader line; on Arabic maps one of El Malha / Mellit was therefore always moved to the list under the map. Every visible point is now labelled or listed with its badge.
- Labels try nearer positions first (one line up or down before two), which shortens leader lines (e.g. Tegali / Tasi, Fashoda).

## 2026-10-20 (label margins)

- The wider marker margin now applies only to main capital labels; point labels test against bare markers again, so El Malha and Mellit are labelled on the war map at 1440px with their REPORTED badges. Main capital labels moved off their dot's row get a short leader line (e.g. El Fasher).

## 2026-10-20 (reported entries)

- Sourced extent entries with no geometry (e.g. Bir Mirgui and Jebel Eredi, UN PoE S/2025/239 paras 98 and 104) are never drawn; they are listed under the war map with their REPORTED badge, paragraph (`pages`) and `as_of` date. Unsourced entries without geometry are still listed as not drawn.
- REPORTED is now a real badge element in the reference-point list and in the 'not labelled on the map' list (e.g. Mellit at 390px).
- Main capital labels can switch to the other side of their dot, and markers are kept at a small distance (El Fasher vs Abéché on the Turkiyya map).

## 2026-10-20 (map labels)

- Map labels are thinned by priority (main-era capitals, then area labels, cited points, context capitals). Labels that would overlap another label or marker, or leave the frame, are hidden and listed under the map; markers always stay. Long point labels fall back to a shorter form before being hidden.
- A capital shared by two eras at the same place (e.g. Suakin, capital of both the Suakin port era and the Beja era) is drawn once; its tooltip lists both eras.
- Points marked `badge: REPORTED` in the extents data show a red REPORTED / مُبلَّغ عنه badge on the label and in the tooltip (2 points: El Malha and Mellit, war in Sudan, UN Panel of Experts S/2025/239).

## 2026-10-20 (later)

- Map point labels can also switch to the other side of their marker, and a moved label's leader line now avoids crossing other labels (e.g. Sennar in Arabic at 390px).
- Arabic map pages: capital and point labels now sit beside their markers instead of on top of them (the SVG text inherits right-to-left direction, so the anchor was flipped).
- The in-progress list is whatever `data/eras/regional-wip.json` holds at build time; counts on the site update automatically.
- Chapter maps, timelines and the "neighbours at a glance" cards now mark the in-progress regional eras (defined by the build-time list `data/eras/regional-wip.json`; 13 as of 2026-10-20, after that day's data update): hollow dashed capital dots, muted dashed names with a ° marker and one "Regional context · research in progress" badge line, tooltips in English and Arabic; timeline bars of such eras are dashed and lighter.
- Map point labels move at most two lines from their marker when nudged apart, and a thin leader line ties a moved label back to its marker (e.g. Kordofan on the Funj map).

## 2026-10-20

- Regional-context eras with no source-backed narrative yet (29 of 68 at the time of this entry, before that day's data update; 13 afterwards: no geopolitics, culture or economy text in English or Arabic) are now marked "Regional context · research in progress" / "سياق إقليمي · البحث جارٍ":
  - era pages: one note box replaces the four repeated "no source yet" flags; dates, capitals, events and citations from the dataset are still shown;
  - chapter "neighbouring eras" lists and the era wiki: muted cards with a badge and an "N of M in progress" count;
  - explorer views (histomap.html, eras.html, era.html): muted dashed bands, a count in the lens bar, muted rows with per-stream counts, a single note box on the era view.
  - No text was added to any era; the list is generated at build time (`data/eras/regional-wip.json`).
- Explorer views, mobile/console pass: eras.html uses one column under 640px; era.html shows the Arabic stream name and Arabic labels inside "under research" flags, and no longer requests a missing era file for an unknown id (404 in the console).
- Chapter and era maps use a regional base map clipped from Natural Earth 1:50m (236 KB → 47 KB gzipped). (commit 6e3c218)
