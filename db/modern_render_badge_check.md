# Modern-era render check + badge flags (Sudan Geopolitical Analyst, 2026-10-24, head 36b5ae0)

Static read of generated files only (no Chrome, no server needed: era.html renders client-side from data/eras/<id>.json). Flag-only; no data edited.

## Task 1 — modern4 render check

| Check | Result |
|---|---|
| data/eras/<id>.json, 10 eras in modern4 (anuak, british-occupied-egypt, CAR, derg-federal-ethiopia, eritrea, french-chad, libya, republic-of-egypt, restored-darfur, southern-sudan-condominium) | **PASS** – every filled culture_dominance/economy EN+AR field byte-identical to db/era_fill_modern4.json |
| Source IDs | **PASS** – all modern4 source_ids resolve in data/periods.json meta.sources and appear in each era's `sources` |
| Inline badges | **PASS** – [SINGLE-SOURCE], [VERIFY], [dated 1991]/[مؤرخ 1991] (LOC cutoff) preserved; every modern4 Arabic field ends with the native-review tag; WORKING TRANSLATION flag present so era.html shows the Arabic-review pill |
| Null fields | **PASS** – culture_dominance_en/_ar null for british-occupied-kingdom-of-egypt, central-african-republic-ubangi-shari, restored-darfur-sultanate-ali-dinar; era.html `txt()` shows flagBox (unfilled), no text invented. Null reasons carried into `flags` |
| 2019 / 2023 eras | **PASS** – december-revolution-transition and war-in-sudan-saf-vs-rsf carry "no CINC: COW NMC v6 ends 2016 and era starts 2019/2023" |
| **data/eras/all.json** | **FAIL – stale** (mtime 18:23 vs era files 18:36). For all 10 eras it lacks the modern4 fields and `power_cinc_share`. eras.html loads all.json first (`all.json[e.id] || loadJSON(e.file)`), so the era list/compare view shows the old (empty) text. Needs a rebuild of all.json. |
| data/periods.json / periods.js | Not applicable – period schema has no culture/economy fields (name, dates, events, capitals, sources only); nothing to check beyond source registry (passes) |
| **power_cinc_share rendering** | **FAIL** – present in 7 era files (CAR, derg, eritrea, chad, libya, egypt + others), but era.html/web.js have no code for it; it is visible only as text inside the generic "Flags:" line. No CINC bar/table. |
| **EDITORIAL badge** | **FAIL – absent** – the string EDITORIAL occurs only in db/regional_power_scores_proposal.{json,md}; not in any data/eras file, era.html or web.js. The only editorial note is the generic power-balance caption ("the number mapping is editorial"). |
| Flag hygiene (minor) | british-occupied-kingdom-of-egypt still carries stale flag "economy: left null – no source read…" although economy is now filled; restored-darfur has 3 near-duplicate culture null reasons. southern-sudan-condominium culture_dominance_ar (pre-modern4 text) has no native-review tag inline (era-level flag covers it). |

## Task 2 — proposed badges (modern eras, ~1820–present)

| Era id | Field | Claim (quoted) | Proposed badge | Reason / source |
|---|---|---|---|---|
| derg-federal-ethiopia | geopolitics_en | "al-Fashaga: Sudan's claim rests on the 1902 Anglo-Ethiopian Treaty and the 1903 Gwynn Line; … until the SAF retook almost all of it" | CONTESTED + SINGLE-SOURCE (GEO-015) | Sovereignty/demarcation of al-Fashaga is disputed by Ethiopia; whole passage rests on GEO-015 only; extents already mark al-Fashaga contested, text does not |
| republic-of-egypt | geopolitics_en | "From 1 Feb 1958 Egypt claimed the territory north of the 22nd parallel, opening the Halaib dispute" | CONTESTED (formal badge) | Live sovereignty dispute (IBS18_1962 sets out both the 1899 and 1902 lines); text says "contested" only for control dates, not for sovereignty |
| british-occupied-kingdom-of-egypt | geopolitics_en | "The 1902 administrative line that later underlies the Halaib dispute" | CONTESTED | Legal status of the 1902 administrative line vs the 1899 22nd-parallel line is the core of the dispute (IBS18_1962) |
| republic-of-south-sudan | geopolitics_en | "the disputed Heglig/Panthou oilfield, which the BBC says … is internationally recognised as Sudanese" | CONTESTED (keep VERIFY) | South Sudan claims Panthou; recognition claim attributed to BBC_HEGLIG2012 only |
| french-chad-republic-of-chad | geopolitics_en | "allegedly let the UAE ship arms into Sudan from its territory (ICG_B204)" | CONTESTED (replace free-text "allegation") | Single ICG brief; allegation, so badge consistently with Libya's REPORTED/SINGLE-SOURCE treatment. Denials not read on box – do not add text about them until sourced |
| french-chad-republic-of-chad | culture_dominance_en | "Sudan's cotton schemes employed an estimated 500,000 Chadian workers in 1978" | SINGLE-SOURCE (inline) | LOC_TCD1988_NIGSUDAN only; era flag says SINGLE-SOURCE but sentence has no inline badge |
| war-in-sudan-saf-vs-rsf | economy_en | "See also GEO-002, GEO-067, GEO-074 for gold flows to the UAE." | CONTESTED | UAE-gold/RSF financing claims are disputed and source quality of GEO refs varies; pointer currently unbadged |
| eritrea-italian-colony-independent | geopolitics_en | "camps there held over a million people at their late-1980s peak" | SINGLE-SOURCE (SAS_HSBA_WP3) | Refugee totals vary by source/agency; one source read |
| eritrea-italian-colony-independent | geopolitics_en | "Eritrea kept influence among cross-border tribes such as the Beni Amer (GEO-015)" | SINGLE-SOURCE | GEO-015 only |
| central-african-republic-ubangi-shari | geopolitics_en | "UNHCR reports allegations of RSF presence in Vakaga" | REPORTED | Text itself says allegations; align with REPORTED badge used in the era flags |
| derg-federal-ethiopia | geopolitics_en | "the SPLA and several hundred thousand refugees fled back into Sudan" | SINGLE-SOURCE (keep VERIFY) | HRW1998_SPLA only; figure unquantified |

Already correctly badged (no action): Libya Kufra supply line (REPORTED + SINGLE-SOURCE); Ethiopia–RSF (SINGLE-SOURCE, contested); Fashaga 600,000 acres (SINGLE-SOURCE); 1984–85 famine 400–500k (SINGLE-SOURCE); South Sudan 382,900 excess deaths (SINGLE-SOURCE; VERIFY); war-era displacement, GDP, inflation (DIFFERING ESTIMATES); gold 64.4 t (SINGLE-SOURCE).

Gaps (no claim to flag): no modern era text mentions Abyei or Kafia Kingi; no 2023-war death toll is stated. If added later they must carry CONTESTED / DIFFERING ESTIMATES.
