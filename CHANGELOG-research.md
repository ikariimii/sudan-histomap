
## Analyst pass (2026-10-20): modern regional neighbours – db/era_fill_modern3.json
- Staging file (not merged into data/eras): geopolitics_en/ar for republic-of-egypt, british-occupied-kingdom-of-egypt, derg-federal-ethiopia, eritrea-italian-colony-independent, french-chad-republic-of-chad, libya-ottoman-italian-independent, central-african-republic-ubangi-shari; economy_en/ar for all except british-occupied-kingdom-of-egypt (null, no source read).
- New source IDs (23, no clashes with periods.json or era_fill_modern/2): LOC1991_FOREIGN, LOC1991_EGYPT, LOC1991_LIBYA, LOC1991_CHAD, LOC1991_CONDO, LOC1991_NATIONALISM, LOC1991_INDEP, LOC_ETH1991_BORDER, LOC_LBY1987_SANUSI, LOC_LBY1987_ITALOSANUSI, LOC_LBY1987_FOURTHSHORE, UNTS6519_1959, HRW1998_SPLA, EJOSSAH_DERG_SPLA, SAS_HSBA_WP3, NDJAMENA2010, UNSC_S2010_217, ICG_B204, ICG_ETH_ERI, ICG_RADAR2024, UNHCR_CAR2024, LSM_KUFRA2024, SWM_ERI2024. Reused: IBS18_1962, WP_HALAIB, GEO-012/015/016/017/037/038/056/079, AR_AJCS_5653.
- Flags: [VERIFY] on search-excerpt sources; [SINGLE-SOURCE] marked; Halaib control dates shown side by side; ACLED/ISW data not used. Arabic is a working translation needing native review.
- Thin: colonial phases (Italian Eritrea, French Chad, Ubangi-Shari, Ottoman Libya), CAR before 2023, Libya after 2011, 1929 Nile agreement terms.

## Extents: Sudan-proper eras (Map Designer, 2026-10-20, commit b368a5b)
- New db/extents/*.geojson, points only (no sourced limit closes a polygon; no edges invented; no CShapes/ACLED): Funj/Sennar (Sennar medium; Old Dongola by 1523, Third Cataract stand-in for Hannik after 1585, Kordofan contested: low; HD2011, ZH_EMB_HIST2020), Alodia (Soba, low; GHA2_CH12, ZH_EMB_HIST2020), Egyptian New Kingdom rule in Nubia (Kurgus GHA II p.265 and Napata p.270 medium; Soleb low), Ballana (Ballana Pleiades 795783, Qustul; low), Ali Dinar (El Fasher, low; HD2011), Daju (Jebel Marra Q886772, low; OFAHEY2008), Tunjur (Ain Farah Q405860, low; OFAHEY2008), Taqali (Nuba Mountains Q1129989 stand-in, low; HD2011), Musabba'at (Kordofan Q867052, low; OFAHEY_SPAULDING1972).
- Gaps: Hannik and Taqali have no Wikidata coordinate; Funj south/east limits, Alodia borders, Ali Dinar extent, Daju/Tunjur/Taqali/Musabba'at limits unsourced. Arabic labels pending native review. Script: scratch/build_sudan_proper.py (run from build_regional.py).

## Historian Pass 20 / 20b (Sudan Historian, 2026-10-20)
- Pass 20 (db/era_fill_hist20.json, merged by research_patch.py `_p20`). Filled: economy for Alodia (GHA IV ch.16 p.406, SINGLE-SOURCE), Daju (GHA V ch.7 p.187, oral tradition, SINGLE-SOURCE), Tunjur (GHA V pp.187–188), Taqali (GHA V p.177, regional context, CONTESTED tributary status), Ballana (GHA II pp.215, 294, imports and Roman payments only); culture for Shilluk (GHA V pp.193, 197) and Dinka/Jieng (GHA V pp.171, 193, 196, SINGLE-SOURCE); geopolitics for Khartoum Mesolithic and Neolithic (contacts and exchange only, AAR2021, CONTESTED).
- Left null with reasons: Anuak culture, Ali Dinar culture, Southern Sudan (Condominium) economy.
- Egypt stream, all 9 eras (geopolitics, culture, economy, EN+AR): Old, Middle and New Kingdom, Late/Persian, Ptolemaic, Roman/Byzantine (GHA II chs 2–4, 6–12), Islamic (GHA II ch.12 p.333, GHA IV ch.16 pp.398–402; GHA III not on the box), Mamluk (GHA IV ch.16 pp.402–405, 416), Ottoman/Muhammad Ali (GHA V ch.6 pp.142, 145; ch.7 pp.178–188; GHA VI ch.13 p.329; ch.14 pp.356–361). 13 new chapter-level source IDs (GHA2_CH2…GHA6_CH13).
- Pass 20b: merges the Analyst's db/era_fill_modern3.json through `_p15`, plus a Pass 18b-style force-add of WP:/WD:/PL: IDs. The Analyst's flags are kept, and british-occupied-kingdom-of-egypt economy stays null. The Libya Kufra passage is replaced with the merged wording from db/kufra_poe_check.md (2970ffe), with the [REPORTED – UN PoE, interview-based] badge and [SINGLE-SOURCE – S/2024/65 para. 47] on the Subul al-Salam / 128 Brigade clause. LSM_KUFRA2024 is replaced by UNPOE_S2024_65 and UNPOE_S2025_239, and the old 'Kufra corridor … VERIFY' flag is replaced by REPORTED and SINGLE-SOURCE flags.
- All Arabic is a working translation pending native review. verify_citations: 136 checks, 0 problems. checkurls: no new failures (44 existing 403/406/000 bot-blocks).

## Extents: UN PoE S/2025/239 points on the current war (Map Designer, 2026-10-20)
- war-in-sudan-saf-vs-rsf: two [REPORTED] points, para. 71 (p. 24, Kufra fuel-route endpoints), as of 2025-04-17, source UNPOE_S2025_239 (already registered). El Malha 15.0941N 26.1612E (GeoNames 379152, matches OSM node 3246118934; low: town vs locality). Mellit 14.1333N 25.55E (Wikidata Q12245024 / GeoNames 370181; medium). Points only: no routes, arrows or areas; SAF/RSF control layer still untraced.
- Skipped, no GeoNames/Wikidata/OSM match (Nominatim and GeoNames search empty; Overpass at capacity): Bir Mirgui (para. 98, p. 30) and Jebel Eredi (para. 104, p. 32, 19 Nov 2024 ambush). Paragraph text checked in db/refs/S_2025_239_EN.pdf. Arabic labels pending native review.

## Historian Pass 21 + follow-up extents search (Sudan Historian, 2026-10-20)
- GHA III obtained from https://sahistory.org.za/sites/default/files/archive_files/general_history_africa_iii.pdf (891 PDF pages; printed = PDF − 22). It is kept in /workspace and not in this repo.
- Pass 21 adds GHA3_CH7 (Bianquis) and GHA3_CH8 (Jakobielski).
  - Islamic Egypt geopolitics: the bakt terms (pp.194–195), jurists' view of the bakt and the gold/emerald-mine clashes (p.168), the 836–7 revision (p.209) and the Fatimid renewal (p.182).
  - Islamic Egypt economy: Nubian imports and exports, barter, and the customs frontier at 'Akasha (p.207), plus Kordofan/Darfur as a possible source of bakt slaves (p.199).
  - Alodia economy: Ibn Salim via al-Maqrizi (p.196) and Ibn Hawqal (p.199).
  - The "GHA III not on box" flag is removed.
- Unchanged:
  - Ballana economy: GHA III starts in the 7th century and does not cover Ballana.
  - The three nulls (Anuak culture, Ali Dinar culture, southern Condominium economy): GHA III does not cover them.
- db/regional_extents_answers_2026-10-20.md has a new follow-up section:
  - Funj southern limit FOUND (GHA V p.177: "to the south of Fazughli", text only).
  - Hannik coordinate NOT FOUND (GHA V p.175 text only; Wikidata and OSM gave no match, and Wadi Hanik at 15.8N 34.0E was rejected).
  - Ali Dinar's named limits NOT FOUND (GHA VII p.283 has none).
- verify_citations: 136 checks, 0 problems. checkurls: no new failures.

## Modern-neighbour extents sources + regional_power proposal (Sudan Geopolitical Analyst, 2026-10-20)
- db/extents_sources_modern_neighbours.json is a proposal and has not been merged. It has 17 phases across 5 eras (Eritrea, Derg/federal Ethiopia, Chad, CAR, Libya). Geometry comes from 22 dated OHM admin_level=2 relations (CC0, found by tag search; geometry not checked) and from Natural Earth admin_0 and geoBoundaries for current borders.
  - Limits are cited to IBS 3, 10, 15 and 16 (read), the ICJ Libya/Chad judgment of 3 Feb 1994, S/RES/915, UNGA 390(V) and 289(IV), EEBC 2002 and PCA Abyei 2009.
  - Disputed areas: Aouzou 1973–94, Badme, al-Fashaga and the Sarra Triangle. The Sarra date is [CONTESTED]: IBS10 gives 20 Jul 1934 and IBS3 gives 29 Jul 1934. Kafia Kingi and Abyei are included as context only.
  - Gaps: Libya 1551–1934 has no open polygon. Italian Eritrea 1936–41 has no polygon. Insurgent control and Libya 2014– are left untraced.
- db/regional_power_scores_proposal.json and .md use method RP-CINC-SHARE-1: the mean share of COW NMC v6 CINC within the 8-state set over the years each era overlaps 1816–2016. WDI values are included for context only.
  - 13 eras are scored. December-revolution and the 2023 war era are null because NMC ends in 2016.
  - The method NEEDS INNOVATION MANAGER SIGN-OFF, because these computed scores are not comparable with the existing editorial ordinal scores.

## Historian Pass 21b – 2026-10-24
- db/egypt_points_citecheck.md: I checked the 13 points in the six ancient-Egypt eras from f23668a against the GHA II PDF. All 12 GHA page cites are OK and none need correcting. One precision note: Semna p.240 is in ch.8. Pi-Ramesses cites Wikipedia only, with no page.
- research_patch.py Pass 21b registers 35 sources from db/extents_sources_modern_neighbours.json meta.sources into REFS (Pass 19 style): OHM_*, IBS*, ICJ_LBY_TCD1994, UNSC_RES915_1994, UNGA_RES289IV/390V, EEBC2002, PCA_ABYEI2009, LOC_TCD1988, EXT_NE_ADMIN0, EXT_GEOBOUNDARIES_NB. Three are tagged [VERIFY]: EEBC2002, LOC_TCD1988 and EXT_GEOBOUNDARIES_NB.
- Checks: verify_citations ran 136 checks with 0 problems. checkurls shows only the known pre-existing 403/406/429/000 hosts.

## Historian Pass 22 – 2026-10-24
- db/era_fill_hist22.json plus a Pass 22 loader in research_patch.py fill geopolitics, culture_dominance and economy (EN and AR) for 13 eras that were empty: Bornu, Solomonic Ethiopia, Garamantes, Kanem, Aksum, Punt/D'mt, Ottoman Hejaz/Saudi, Rise of Islam, Sabaean, Suakin, Wadai, Zagwe and Zande. Everything is written from Sudan's side and cites UNESCO GHA II–VII by printed page. JEDDAH2023 is used for the 2023 talks.
- 20 GHA chapter references are new (GHA2_CH13–16, GHA2_CH20, GHA3_CH2/3/15/19, GHA4_CH10/15/17, GHA5_CH17/18, GHA6_CH12/15/17/20/22, GHA7_CH11).
- Badges: SINGLE-SOURCE (Garamantes, Dawit's Aswan raid), CONTESTED (Punt's location, Aksum's conquest of Meroe), INDIRECT (Sabaean, Zagwe–Nubia), GAP (Hejaz 1820–2023).
- All Arabic is marked as a working translation that needs native review. No field is left null, and the "no source-backed text yet" flags are cleared.

## 2026-10-24 – Sudan Geopolitical Analyst: modern fill 4, per-era neighbour extents, CINC rulings
- db/era_fill_modern4.json (staging, not merged): filled culture_dominance EN+AR for anuak, derg-federal-ethiopia, eritrea, french-chad, libya, republic-of-egypt; economy EN+AR for british-occupied-kingdom-of-egypt and southern-sudan-under-condominium. Left null with reasons: culture_dominance for british-occupied-kingdom-of-egypt, central-african-republic-ubangi-shari, restored-darfur-sultanate-ali-dinar (no source read). New IDs: LOC1991_SOUTHPOL, LOC1991_SOUTHUNITY, LOC1991_NONMUSLIM, LOC1991_MUSLIMPEOPLES, LOC1991_INDSUDAN, LOC1991_EDUCATION, LOC_ETH1991_NILOSAHARAN, LOC_ETH1991_ETHIOSEMITIC, LOC_ETH1991_TOPO, LOC_ETH1991_ERITREANMOV, LOC_ETH1991_ISLAM, LOC_TCD1988_NILOSAHARAN, LOC_TCD1988_NIGSUDAN (no clashes with periods.json). GHA VIII cite re-read: ch.30 (Mazrui) p.924, corrected from p.923.
- db/extents_per_era_modern_neighbours.json: 5 per-era entries (17 phases) in extents_historic.json format, phases identical to db/extents_sources_modern_neighbours.json; badges/nulls kept.
- [VERIFY] cleared after reading: UNSC 915, UNGA 390(V), UNGA 289(IV) A content, PCA Abyei 2009 (case page), EEBC 2002 mandate, ICJ 1994 holding (case page), COW NMC licence wording (no licence stated; citation requested). Kept: ICJ paragraph cites (judgment PDF behind Cloudflare), Badme award wording, Libya 24 Dec 1951 date, treaty texts, Gwynn line, EPLF Asmara date, Chad north 1910s, Aouzou 1973 start, OHM 2839926 naming, geoBoundaries licence, LOC_TCD1988 index.
- db/regional_power_scores_proposal.json/.md: `power_cinc_share` (COW NMC v6 CINC, year range per era, 1816–2016 only) and separate `power_editorial` (Kush, Mahdist 0.9, EDITORIAL, unchanged); 2019 and 2023 eras null "data ends 2016"; caveats added (low-industry bias, Egypt pre-1960 inflation, South Sudan inside COW Sudan pre-2011 vs WDI, scale not comparable with editorial).
- verify_citations: 136 checks, 0 problems (run serially).

## Historian Pass 22b — merge era_fill_modern4 + COW NMC v6.0 CINC shares (derived)
- Merged db/era_fill_modern4.json (Analyst 677d6c5/7cff461/04a1505, final): empty fields filled; all SINGLE-SOURCE / VERIFY / EDITORIAL / native-review badges preserved; 13 LOC source IDs registered; GHA VIII ch.30 Mazrui p.924 used.
- Null fields keep explicit "null reason" flags (culture: British-occupied Egypt, CAR/Ubangi-Shari, Ali Dinar's Darfur); stale null-reason flags removed where fields are now filled.
- `power_cinc_share` added as a DERIVED figure from COW NMC v6.0 CINC (1816–2016; method RP-CINC-SHARE-1), not comparable with editorial regional_power. Licence: none stated by COW; cited per COW's request (version + Singer, Bremer & Stuckey 1972). War era (2023–) = null (data ends 2016).
- Front-end rendering of power_cinc_share is left to Web.

## Historian Pass 22c — register Map Designer extent-only sources
- Registered db/extents_sources_map_designer.json (Map Designer 5f1fada, 36 entries: 33 OHM relations + 3 refs); IDs already registered skipped; entries without OHM source tags carry a visible "[VERIFY – no source tags]" title flag.

## Historian Pass 22d — culture for 3 eras + CINC for unscored 1816–2016 eras
- british-occupied-kingdom-of-egypt culture_dominance EN/AR filled from GHA VII ch.21 pp.555–556 (Y.A. Talib section: press 169→282 titles 1898–1913, al-Azhar reform) and ch.23 p.601 (H.A. Ibrahim: Wafd claim to Sudan, 'Unity of the Nile Valley'); [SINGLE-SOURCE per point]; Arabic = working translation.
- central-african-republic-ubangi-shari and restored-darfur-sultanate-ali-dinar culture left null with reasons (no page-cited culture passage in GHA VII / LOC).
- power_cinc_share (COW NMC v6.0, RP-CINC-SHARE-1) added for british-occupied Egypt 0.77, Ethiopian Empire 0.65, Ottoman/Muhammad Ali Egypt 1.00 — all flagged [VERIFY]: regional set has very few COW members in those years, share near 1.0 by construction. Null with reason (not COW members / outside set) for Hejaz-Saudi, southern Sudan (condominium), Ali Dinar, Wadai, Taqali, Zande, Bornu, Suakin, Beja, Anuak, Dinka, Nuer. No editorial scores pre-1816.

## Historian Pass 23 — Analyst badge proposals (db/modern_render_badge_check.md, e5d7fa2)
- Applied the 11 badges exactly as proposed (CONTESTED / SINGLE-SOURCE / REPORTED; existing VERIFY kept); french-chad 'allegedly'/'[VERIFY; allegation]' replaced by [VERIFY] [CONTESTED]; no denials added, no other wording changed.
- Flag hygiene: stale 'left null'/'null reason' flags removed where a field is filled (incl. british-occupied Egypt economy); Ali Dinar's 4 culture null reasons merged into one.
- Full rebuild incl. web/build.py; data/eras/all.json regenerated after the era files.

## Pass 23b (Historian): research_patch.py no longer writes extents files
- `write_era_files` no longer calls `write_extents()`. `write_extents()` and `write_extent_geojson()` are now no-ops at the end of research_patch.py, so the pipeline never writes db/extents_historic.json or db/extents/*. Map Designer owns those files.
- Checked across a full rebuild: db/extents_historic.json kept 62 items and sha256 1a70489b…c510c0, and every db/extents/* file hash was unchanged.

## Pass 23c (Historian): CINC coverage checked against the COW NMC v6.0 rows
- British-occupied Egypt (1882–1922): share set to null. The only in-era Egypt (651) row is for 1882. Egypt is a system member for 1855–1882 and from 1937. [VERIFY]
- Ethiopian Empire: share 0.65, the mean over the 73 in-era Ethiopia (530) rows, 1898–1936 and 1941–1974. There are no rows for 1937–1940. Min 0.14, max 1.00. [VERIFY]
- Ottoman Egypt: share set to null because only one state is in the comparison set. [VERIFY]
