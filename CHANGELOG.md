# Changelog

Site changes for sudan.indomando.com (built from `web/` by `web/build.py`). Newest first.

## 2026-10-20 (later)

- Chapter maps, timelines and the "neighbours at a glance" cards now mark the 29 in-progress regional eras (defined by the build-time list `data/eras/regional-wip.json`): hollow dashed capital dots, muted dashed names with a ° marker and one "Regional context · research in progress" badge line, tooltips in English and Arabic; timeline bars of such eras are dashed and lighter.
- Map point labels move at most two lines from their marker when nudged apart, and a thin leader line ties a moved label back to its marker (e.g. Kordofan on the Funj map).

## 2026-10-20

- Regional-context eras with no source-backed narrative yet (29 of 68: no geopolitics, culture or economy text in English or Arabic) are now marked "Regional context · research in progress" / "سياق إقليمي · البحث جارٍ":
  - era pages: one note box replaces the four repeated "no source yet" flags; dates, capitals, events and citations from the dataset are still shown;
  - chapter "neighbouring eras" lists and the era wiki: muted cards with a badge and an "N of M in progress" count;
  - explorer views (histomap.html, eras.html, era.html): muted dashed bands, a count in the lens bar, muted rows with per-stream counts, a single note box on the era view.
  - No text was added to any era; the list is generated at build time (`data/eras/regional-wip.json`).
- Explorer views, mobile/console pass: eras.html uses one column under 640px; era.html shows the Arabic stream name and Arabic labels inside "under research" flags, and no longer requests a missing era file for an unknown id (404 in the console).
- Chapter and era maps use a regional base map clipped from Natural Earth 1:50m (236 KB → 47 KB gzipped). (commit 6e3c218)
