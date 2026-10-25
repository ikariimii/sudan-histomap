# CHANGELOG – research pass 1 (Sudan Historian, 2026-10-19)

Backups: `data/backup/periods.v1.orig.json`, `data/backup/periods.v1.orig.js`, `data/backup/build_data.v1.orig.py`.
Mechanism: all edits live in `research_patch.py`, called by `build_data.py` right before it writes the files, so running the build again keeps them. Schema unchanged: same 9 keys. `sources` stays a list of URLs because index.html renders them as links. The rendered link label is the URL's last path segment, so book links can show up as ids, for example `34888835`.
Result: 61 → 68 entries. JSON valid; periods.js regenerated and loads (68).

## Sources consulted (all verified online this session)
| Key | Reference | URL used |
|---|---|---|
| HD | P.M. Holt & M.W. Daly, *A History of the Sudan*, 6th ed., Routledge/Longman 2011, ISBN 978-1-4058-7445-8 (read in full: Introduction pp.1–9 and ToC) | doi.org/10.4324/9781315834030 |
| GHA2 | UNESCO *General History of Africa* II, ed. G. Mokhtar, 1981 (CC BY-SA IGO). Read: ch.9 Sherif "Nubia before Napata" p.245; ch.10 Leclant "The empire of Kush: Napata and Meroe" pp.278–297 | unesdoc.unesco.org/ark:/48223/pf0000184265 |
| WEL96 | D.A. Welsby, *The Kingdom of Kush*, British Museum Press 1996 (catalogue/ToC only, with an appendix listing the rulers) | WorldCat 34888835 |
| WEL02 | D.A. Welsby, *The Medieval Kingdoms of Nubia*, BMP 2002 (record via JAH review only) | doi 10.1017/s002185370323855x |
| OF08 | R.S. O'Fahey, *The Darfur Sultanate: A History*, Hurst/Columbia 2008 (blurb and ToC only; gives c.1650–1916) | Google Books HQxYJWkO7EEC |
| OFS72 | O'Fahey & Spaulding, "Hāshim and the Musabba'āt", BSOAS 1972 (abstract only) | doi 10.1017/s0041977x00109383 |
| SP85 | J. Spaulding, *The Heroic Age in Sinnār* (LoC ToC record only) | catdir.loc.gov |
| EP | Evans-Pritchard, *The Nuer* (1940, full PDF read for intro) and *The Political System of the Anuak* (1940, record only) | monoskop PDF; doi 10.4324/9781003135395 |
| KERMA | Swiss-Sudanese Archaeological Mission at Kerma, chronology page | kerma.ch/en/history/ |
| WHC | UNESCO WHC 1073 (Gebel Barkal) and 1336 (Island of Meroe), brief synthesis | whc.unesco.org |
| Geo | Wikidata P625 / Pleiades reprPoint for site coordinates | per site |

"Record/ToC only" means I confirmed the book exists and what it covers, but I did not read the specific pages. For those books I cite no page numbers.

## Corrections (dates/facts)
1. **Kingdom of Kerma**: −2500/−1500 → **−2450/−1480**, using the Kerma mission's phases (Early 2450–2050, Middle 2050–1750, Classic 1750–1480, Final to 1450). GHA II's 1981 range of −1730/−1580 covers only the Classic phase and is noted as superseded.
2. **Sultanate of Darfur (Keira)**: start 1603 → **1650** (O'Fahey 2008: c.1650–1916). Flagged as genuinely uncertain.
3. **Psamtik II's raid on Napata**: was "593 BCE". It now reads "GHA: 591 BCE; often 593 BCE" in both the Napatan and Late Period entries.
4. **Rome vs Kush**: "Petronius campaign 24 BCE" → **Napata taken 23 BCE** (GHA), after the Meroitic sack of Aswan. Samos 21/20 BCE confirmed; frontier at Hiera Sycaminos added.
5. **Amanirenas "resists Rome 25–21 BCE"** replaced with the GHA wording: which kandake (Amanirenas or Amanishakheto) negotiated is unresolved.
6. Coordinates corrected: Esh-Shaheinab 16.13→16.0624 N; Qustul 22.1/31.5 → 22.2333/31.6167; Faras lon 31.48→31.46; Jebel Barkal, Kerma, Meroë, Naqa, Musawwarat and Suakin refined to Wikidata/Pleiades values (changes ≤0.01°).

## Enrichment of existing entries
- **Napatan**: Alara, Kashta, Peye, Shabaka, Shabataka, Taharqa, Tanwetamani, Atlanarsa, Senkamanisken, Anlamani and Aspelta, with GHA II reign dates. Sites added: El-Kurru, Nuri, Kawa.
- **Meroitic**: Arkamani/Ergamenes, Shanakdakhete, Taniydamani, Amanirenas, Amanishakheto, Akinidad, Natakamani & Amanitore; Griffith's 1909 transliteration; Ezana's campaign. Sites added: Wad ban Naqa, Hamadab.
- Other sites added: Kadero (Khartoum Neolithic), Faras (A-Group), Soleb and Kurgus (New Kingdom), Qasr Ibrim (Nobadia), Banganarti (Makuria).
- Funj: Upper Nubia suzerainty, vassal Dongola, 'Abdallab status (HD). Shilluk: reach to Aba Island and the tradition of a Shilluk origin for the Funj (HD). Darfur: Tayrab's Kordofan conquest, al-Fashir c.1790/91.

## Source swaps (Wikipedia kept as a secondary link; stronger source added first)
HD added to: Alodia, Funj, Turkiyya, Mahdiyya, Condominium, all five Republic periods 1956–1989, Bashir era, Southern Sudan 1899–2011, Darfur (Keira), Ali Dinar, Taqali, Shilluk, Suakin.
GHA2 added to: A-Group, C-Group, Kerma, New Kingdom rule in Nubia, Napatan, Meroitic, Ballana, Nobadia, Late Period, Ptolemaic, Roman Egypt, Old/Middle/New Kingdom Egypt, Aksum, D'mt, Garamantes, Sabaean.
Others: Welsby 1996 (Napatan, Meroitic); Welsby 2002 (Ballana, Nobadia, Makuria, Alodia); O'Fahey 2008 (Daju, Tunjur, Keira, Ali Dinar); Spaulding (Funj); WHC 1073/1336; kerma.ch.
**Still Wikipedia-only (22):** Khartoum Mesolithic, December Revolution, 2023 war, Republic of South Sudan, and the 18 regional context entries: Egypt after 641, Zagwe, Solomonic, Derg, Eritrea, Kanem, Bornu, Wadai, Chad, Libya, Zande, CAR, Rise of Islam, Saudi.

## Additions (7)
'Abdallab chiefdom (1480–1821); Ja'aliyyin kingdom/Sa'dab (1500–1821); Musabba'at sultanate (1680–1785); Beja peoples (700–2026); Dinka (Jieng), Nuer (Naath) and Anuak (Anywaa) communities (1500–2026).

## Open uncertainties / to-do
- **Ain Farah (Tunjur)**: Wikidata's 16.76N 29.19E conflicts with the original 15.0N 24.9E. The original is kept and flagged.
- Taqali start 1750 and end 1969 are unverified. The Shilluk end date of 1861 is unverified.
- Not checked this pass: coordinates for Soba, Ballana, Aniba and Sedeinga. Pleiades (20.54N) and Wikidata (20.38N) disagree on Sedeinga, so I did not add it.
- Napatan/Meroitic reign dates come from GHA 1981. Later work revises several of them, including the order of Shabaka and Shebitku. These need checking against Welsby 1996's appendix of rulers, which I did not read.
- The dated Musabba'at events (1734/1772/1782/1785) come from a Wikipedia summary of O'Fahey 2008 pp.49–59. I have not checked the book itself.
- The start dates for Beja, Dinka, Nuer and Anuak (700/1500) are display conventions only, and each entry's dating_note says so. These are peoples, not states. Not yet sourced: Nuer eastward expansion in the 19th c., Anuak geography, Beja–Blemmyes links.
- I did not read Nobadia's c.543 conversion or Makuria's 651/652 date in a primary source this pass.
- Visual: the new Middle Nile and South Sudan entries overlap existing bands, and index.html supports only 2 lanes, so some bands will overlap on screen. Consider lower prominence or a third lane.

# Pass 2 – follow-up (2026-10-19, ~18:55 EDT)
Schema unchanged. Edits are in `research_patch.py` under `apply2()`. Rebuilt: 68 entries; JSON valid.

## 1. Coordinates
| Site | Old | New | Source | Status |
|---|---|---|---|---|
| Ain Farah (Tunjur) | 15.0, 24.9 | **14.2657, 24.3161** | Wikidata Q405860 (2nd value; same as de/ar Wikipedia) | MEDIUM confidence. The other Wikidata value (16.76, 29.19) falls outside Darfur and is rejected. The "15 km NW of Kutum" description doesn't fit (this point is about 35 km W of Kutum). No excavation-report coordinate found. **Open.** |
| Soba (Alodia) | 15.52, 32.68 | 15.524, 32.6809 | Wikidata Q1247214 | Confirmed. No Pleiades entry. |
| Ballana | 22.27, 31.58 | 22.2667, 31.5667 | Pleiades 795783 (Barrington Atlas 81 B3) | Verified |
| Aniba | 22.67, 32.03 | 22.6683, 32.017 | Pleiades 795777 (BAtlas 81 C3) | Verified |
| Sedeinga (added to Meroitic) | – | 20.5435, 30.2871 | Pleiades 795855 | Verified. Fits Rilly (SARS *Sudan & Nubia* 22): "14 km north of Soleb". Wikidata's 20.38N (south of Soleb) and French Wikipedia's temple coordinates (which match Soleb) are rejected. |

## 2. Placeholder starts
- **Beja**: 700 → **275 CE**. This is the earliest dated activity of the Blemmyes in GHA II ch.7 (suppressed under Probus, 276–282). GHA II ch.10 calls the Blemmyes "customarily identified with the Bedja", so I flagged the equation as customary, not proven. Earlier Majai/Reheres ancestry is flagged as possible (GHA II ch.11). Sources: Holt & Daly and GHA II only; Wikipedia removed.
- **Dinka / Nuer / Anuak**: no source gives a datable start. They stay at 1500 and are now marked "UNSOURCED START (display placeholder)".

## 3. Wikipedia-only entries: 22 → 0 (Wikipedia kept as a secondary link)
- **Khartoum Mesolithic**: −8000/−4900 → **−8500/−5000** (Early Khartoum ceramics c.8500–5000 cal BC; *African Archaeological Review* 2021 review).
- **December Revolution**: Crisis Group Report 281 (2019), Crisis Group statement of 26 Oct 2021, UNSC res. 2524 (2020). Added events: Constitutional Document of 17 Aug 2019 and UNITAMS.
- **War in Sudan**: UN News (15 Apr 2023), UNSC press statement SC/15257, IPC Famine Review Committee (1 Aug 2024), Jeddah Declaration (11 May 2023). "Government to Port Sudan" is still not backed by a non-Wikipedia source.
- **Republic of South Sudan**: UNSC res. 1996 (2011), Crisis Group Report 217 (2014), R-ARCSS text (12 Sep 2018), ACCORD on the transitional government formed 22 Feb 2020. Key events rewritten with these dates.
- **18 regional entries**: cited at volume level to UNESCO General History of Africa III–VIII. I confirmed what each volume covers but did not read the chapters. Saudi entry: Jeddah Declaration.

## 4. Database
Per the new rule, I wrote nothing to `sudan.db` directly. I added `db/history_sources.json` (36 records, same format as `geopolitics_sources.json`) and a guarded loader in `db/seed.py`. A copy is in `data/sources.json`. Ran `python3 seed.py && python3 checkurls.py && python3 ideas.py`: all three exited 0. DB now has 68 periods, 82 places, 89 sources (36 HIS-*), 35 datasets, 64 ideas. Seven HIS URLs fail the check: six return 403 because the sites block bots (WorldCat, Crisis Group ×3, IPC, state.gov), and the SARS PDF timed out. Each was read or found in search earlier in this session.

# Pass 3: meta.sources and key_events_ar (2026-10-19, ~19:05 EDT)
Code: `research_patch.py` → `REFS`, `AR_EVENTS`, `apply3()`, `finalize()`. `build_data.py` gained one line, `research_patch.finalize()`, which adds `meta.sources` and also writes `meta` into `periods.js`. Previously `periods.js` held only `periods`, so the details panel could not resolve IDs.

## meta.sources
- Format matches `cite()` in index.html: `HISTO.meta.sources[id] = {author, year, title, publisher, pages, url}`. Extra fields `edition`, `isbn` and `note` are stored too; the panel does not display them.
- 118 IDs, all referenced and all resolving:
  - 31 curated (e.g. `HD2011`, `GHA2`, `WELSBY1996`, `OFAHEY2008`, `ICG2019`, `UNSC1996`, `GHAIII`–`GHAVIII`)
  - 80 `WP:<slug>` (Wikipedia, secondary)
  - 7 `WD:`/`PL:` (Wikidata/Pleiades coordinates)
- Each period's `sources` array now holds IDs, not URLs.
- ISBNs are included only where I saw them online: Holt & Daly 978-1-4058-7445-8; Welsby 1996 978-0-7141-0986-2; Welsby 2002 0-7141-1947-4; O'Fahey 978-0-231-70038-2 / 978-1-85065-853-5; GHA II 92-3-101708-X.
- No ISBN or year is given for GHA III–VIII, Spaulding, Evans-Pritchard, or the web sources (year left blank where unverified).

## key_events_ar
- 165/165 events translated into Modern Standard Arabic across all 68 periods. Translation only; no added content. Validated: no period is missing translations, and no Latin script remains.
- Standard forms used: كوش، مروي، نبتة، كرمة، الفونج، سنار، العبدلاب، الجعليون/السعداب، دارفور، الكيرا، كردفان، المقرة، علوة، سوبا، البجة، الشلك، فشودة، النوير، الأنواك، الدينكا.

## Transliteration uncertainties (please review with an Arabic-speaking specialist)
- **Kushite royal names**: Arabic has no fixed academic standard for these. Used: بيي (بعنخي), شباكا, شبتاكا, طهارقا, تانوت أماني, أتلانرسا, سنكامانيسكن, أنلاماني, أسبلتا, أركاماني, شنكداخيتي, تانيدأماني, أماني ريناس, أماني شاخيتو, أكينيداد, نتكاماني, أماني تيري.
- **Sulayman "Solongdungu"** → سليمان (سولونج). Shortened form; check against Arabic Darfur histories.
- **Darfur/Kordofan names**: تيراب (Tayrab), الغديات (Ghudiyat), النابتاب (Nabtab), قرّي (Qarri), قوز رجب, حلفاية الملوك, أم دبيكرات (Umm Diwaykarat, using the common Sudanese spelling).
- **Other place names**: Hiera Sycaminos → هيرا سيكامينوس (المحرقة). Petronius → بترونيوس. Blemmyes → البليميون. Nobades → النوباديون. Avungara → الأفونغارا. D'mt → دعمت.
- **Organisation acronyms** spelled out or transliterated: يونيتامس (UNITAMS), أونميس (UNMISS), مجموعة الأزمات الدولية (ICG), التصنيف المرحلي المتكامل (IPC), أكورد (ACCORD).
- **"Kandakes"** → الكنداكتان (dual form).

## Rebuild
`build_data.py`, then `seed.py && checkurls.py && ideas.py`: all exited 0. DB: 68 periods, 82 places, 89 sources. The DB `periods.sources` field now stores IDs.

# Pass 4: eras (2026-10-20, ~00:55 EDT)
Following the scope change, I did not build data/views/<lang>.json. The language-only sets in db/lens_*.json belong to the Geopolitical Analyst.

- **data/eras/index.json**: 68 eras, each with id, English and Arabic name, and dates. Generated by `write_eras_index()`.
- **data/eras/<id>.json**: 68 files from `write_era_files()`, with events in English and Arabic.
  - 11 eras have curated geopolitics, culture and economy text in English and Arabic: Kerma, Napatan, Meroitic, Funj, 'Abdallab, Ja'aliyyin, Darfur (Keira), Beja, Shilluk, Condominium, 2023 war.
  - The other 57 eras have events only. Their empty sections are null and flagged; there are 239 flags in total.
  - **regional_power**: one score only, Kush under the 25th Dynasty = 0.9, based on GHA II ("brought the entire Nile valley as far as the Delta under the empire of Kush"). Every other actor is null and flagged.
- **New language-tagged sources** (all checked online):
  - zh: two PRC Embassy in Sudan history pages. These are government popular texts, not academic.
  - ru: the Great Russian Encyclopedia article "Anglo-Egyptian Sudan" (Orlov), and the record for *История Судана в новое и новейшее время* (Nauka 1992, ISBN 5-02-017341-X). The book itself was not read.
  - fr: SFDAS, *Histoire et civilisations du Soudan* (2017, ISBN 978-2-918157-24-3, free PDF), and the French Culture Ministry's virtual national-museum page "Méroé et les royaumes médiévaux".
  - de: DAI page for the Musawwarat project, and the Naga project page (Munich).
  - All 126 sources in meta.sources now carry a `lang` field. They were also added to db/history_sources.json (now 44 records, with the language set).
- **data/eras/comparison.json**: 11 divergences I read directly (status: 3 agree, 3 conflict, 4 partial, 1 no-conflict). The `auto` section is empty because no db/lens_*.json files exist yet; the comparator runs on every build.
- **Rebuild**: build_data.py, then seed.py, checkurls.py and ideas.py, all exited 0. DB sources by language: en 36, zh 2, ru 2, fr 2, de 2.
- **Gaps**:
  - No Arabic or Spanish sources yet. The NCAM and Sudanese university publications I planned to look for were not found this pass.
  - No CNKI or 中国大百科全书 text was reachable; the Chinese sources are embassy pages only.
  - Great Russian Encyclopedia articles on Kush and the Mahdiyya were not found.

## Pass 5 (2026-10-19): filling the priority eras
- Added REFS (all lang en): GHA6_CH14 (Ibrahim/Ogot, Sudan in the 19th c.), GHA7_CH4 (Ibrahim, NE Africa resistance), GHA8 (Sudan passages pp.148–150 and others), GHA2_CH12 (Michałowski). The ICG2019 wording was verified against the live report page.
- ERA entries added: a-group, c-group, noba-x-group-ballana, nobadia, makuria, alodia-alwa, turkiyya, mahdiyya, independent-sudan-first-parliamentary, abboud, nimeiry, transitional-third-parliamentary, december-revolution. The condominium entry was extended with economy and culture text.
- Power: added Mahdist state = 0.9 (GHA VII: "dominated the Sudan for fourteen years"; editorial ordinal). The Turkiyya-eve balance and Anglo-Egyptian superiority are null with flags (the sources are qualitative only).
- Divergence noted: Makuria was first Melkite (567–70) and later Monophysite (660–700), against a simplified "Monophysite Nubia" (GHA II ch.12).
- No db/lens_*.json yet, so the comparison was not rerun.

## Pass 6 (2026-10-20): end of Meroe and comparison fixes
- Meroitic key event (EN/AR) changed from "Collapse by time of Ezana of Aksum's campaign…" to "Collapsed in the 4th century CE; cause debated (Noba per GHA II; Aksumite campaign of Ezana)". The dating note now says 350 is a placeholder year and quotes GHA II. The period already cites GHA2.
- comparison.json: FR_MUSEE_MEROE end of Meroe changed from conflict to partial (agent agrees, date differs); ZH_EMB_HIST2020 end changed from agree to partial (date agrees, Aksum attribution conflicts with GHA II); ZH_EMB_HIST2020 Kerma 1700 BCE changed from conflict to phase-difference (Classic Kerma).
- The built data/periods.js and periods.json were copied to /workspace/sudan-histomap-site/data/ (not committed, not pushed).

## Pass 7 (2026-10-20)
- Added a Makuria divergence to KNOWN_DIVERGENCES (EN/AR, cites GHA2 ch.12): Makuria was Melkite from c.567–70 and Monophysite only from c.660–700, against the "Monophysite Nubia" simplification. Rebuilt; changed data files copied to the site folder (not pushed).

## Pass 8 (2026-10-20)
- Added EDWARDS2011 (D.N. Edwards, "From Meroe to 'Nubia': exploring culture change without the 'Noba'", in Rondot, Alpi & Villeneuve (eds), La Pioche et la Plume, PUPS 2011, pp.501–514, ISBN 978-2-84050-760-4) to meta.sources and to db/history_sources.json (HIS-026), lang en. Checked from title and abstract only. Attached as a secondary source on the Meroitic period and era file.
- Pass 9 (2026-10-20): merged 46 lens source IDs from db/lens_*.json into meta.sources (177 total, 0 unresolved); comparison rerun: 38 auto + 12 known.

## Pass 9 (2026-10-20): al-Bashir era
- Filled data/eras/al-bashir-ncp-ingaz-regime.json (EN/AR geopolitics, culture, economy) from the six db/lens_*.json al-Bashir items plus ICG2019. Lens source IDs were imported into REFS read-only (lens files were not modified). Power scores are null with flags. write_era_files now also carries ERA flags and power flags.

## Pass 10–11 (2026-10-20): extents for the Map Designer
- New db/extents_historic.json, generated by research_patch.write_extents() on every build.
  - 13 sourced eras, 18 left empty (items:null with a reason), 9 modern eras with CShapes references only.
  - Anchor coordinates come from Wikidata QIDs and Pleiades 795815.
- New refs: PLEIADES_795815, CSHAPES2 (NON-COMMERCIAL, reference only), and OHM_<id> for the relations used.
- db/extents/<era-id>.geojson written from OHM (CC0) relations, with raw downloads in db/extents/raw/: makuria (3), turkiyya (1), anglo-egyptian-sudan-condominium (5), shilluk-kingdom (1). Each feature has properties.source = OHM_<id>, certainty low, and a license field.
- OHM 2690836 was dropped (Egypt-only polygon). Conflicts between OHM shapes and the texts are noted per item.

## Pass 12 (2026-10-20): Nobadia–Makuria merger, Darfur limits, Sennar anchor
- New refs: DERDA_LAJTAR2019 (JÖB 69, open PDF read in full, p.136 and n.4), OFAHEY2018_FWD (O'Fahey's foreword to al-Tunisi, In Darfur, NYU 2018, pp.ix–xxi; read through the search index only), TAKANA2016 (CMI 2016, open PDF, p.9). OFAHEY2008 note: table of contents seen only.
- Nobadia/Makuria dating notes now record the merger dispute: c.630 / pre-652 (Derda & Łajtar), mid-7th c. Qalidurut (Maqrizi via GHA II pp.332–333), Merkurios from 697 (GHA II), late 6th c. (Godlewski hypothesis). Welsby 2002 not read.
- extents_historic.json: Darfur raised to medium, with west/south/north limits (al-Tunisi via Takana), Wadai stalemate and tributaries, and Kordofan 1785–1821 (O'Fahey). Funj anchored at Sennar (Wikidata Q611867 / GeoNames 367644). Nobadia/Makuria merger notes added. db/extents/*.geojson not touched (Map Designer owns them).

## Pass 13 (2026-10-20): economy/culture fill
- New refs: GHA7_CH12 (Crowder, p.283), GHA7_CH17 (Abdussalam & Abusedra, pp.455–456). Added page notes to GHA8 (pp.6, 33–34, 322, 761). All texts read in full on the box (UNESCO PDFs; Holt & Daly intro pp.1–9; Evans-Pritchard 1940).
- Filled (EN+AR): Kerma econ; C-Group econ; Egyptian New Kingdom rule in Nubia (geo/culture/econ); Condominium econ; Southern Sudan under the Condominium (culture); first parliamentary period econ; Abboud econ; second parliamentary period geo; Ali Dinar's sultanate geo; 'Abdallab culture; Ja'aliyyin culture; Taqali culture; Dinka geo+econ; Nuer econ.
- Null with reason (flagged in era files): Ballana econ, Alwa econ, Shilluk culture/econ, 1985–89 culture/econ, Nimeiri econ, 2019 culture, 2023 war culture/econ. Khartoum Mesolithic/Neolithic left uncurated (GHA I not available).
- Arabic is a working translation, flagged for native review. No power scores added. db/extents/*.geojson, sudan.db, lens and Analyst files not touched.
- Pass 14: Darfur frontier anchors (al-Tuwaisha OSM node 7730407134; Geneina Q311309; Dar Masalit Q56545571; Dar Fertit Q1165582). al-Mazroob unresolved (candidates in notes).

## Extents: Sudan-proper eras (Map Designer, 2026-10-20 09:xx EDT)
- New db/extents/*.geojson, points only (no sourced limit closes a polygon; no edges invented; no CShapes/ACLED): Funj/Sennar (Sennar medium; Old Dongola by 1523, Third Cataract stand-in for Hannik after 1585, Kordofan contested: low; HD2011, ZH_EMB_HIST2020), Alodia (Soba, low; GHA2_CH12, ZH_EMB_HIST2020), Egyptian New Kingdom rule in Nubia (Kurgus GHA II p.265 and Napata p.270 medium; Soleb low), Ballana (Ballana Pleiades 795783, Qustul; low), Ali Dinar (El Fasher, low; HD2011), Daju (Jebel Marra Q886772, low; OFAHEY2008), Tunjur (Ain Farah Q405860, low; OFAHEY2008), Taqali (Nuba Mountains Q1129989 stand-in, low; HD2011), Musabba'at (Kordofan Q867052, low; OFAHEY_SPAULDING1972).
- Gaps: Hannik and Taqali have no Wikidata coordinate; Funj south/east limits, Alodia borders, Ali Dinar extent, Daju/Tunjur/Taqali/Musabba'at limits unsourced. Arabic labels pending native review. Script: scratch/build_sudan_proper.py (run from build_regional.py).

## Pass 27 (2026-10-24): power_cinc_share for eras ending before 1900
- 37 pre-1900 eras without a CINC entry now carry power_cinc_share null with null_reason, cite COW_NMC6 (method RP-CINC-SHARE-1). No scores, no estimates.
- 30 eras end before 1816: "outside COW NMC v6.0 coverage: era ends before 1816, so there is no CINC data; not estimated".
- 7 eras overlap 1816+ but the actor is not a COW system member ('Abdallab, Funj, Ja'aliyyin, Shilluk, Keira Darfur, Turkiyya, Mahdist state): "not a COW system member: ... not estimated".
- Existing pre-1900 entries kept: Ottoman Egypt (only one state in the comparison set), Bornu (not a COW member, Pass 22d). Editorial regional_power ordinals unchanged. sudan.db and db/extents* not touched.

## 2026-10-24 — Pass 28: QASIM_MAWSUA (user-supplied, vol. 4)
- Registered QASIM_MAWSUA: 'Awn al-Sharif Qasim, Mawsu'at al-qaba'il wa-al-ansab fi al-Sudan, 1st ed. 1996, Khartoum. The user supplied vol. 4 only (letters ظ ع غ ف, printed pp.1409–1820; PDF p.N = printed p.N+1408). The scan and OCR are kept off-repo for copyright reasons.
- Groups: Shaigiyya homeland text, Korti anchor (APPROXIMATE), subgroups and Shayiq genealogy (TRADITION); Mahas sections; Funj Jibal Lul homeland, origin debate (CONTESTED) and Sennar 1504; Fur origin (CONTESTED), Banu Hilal genealogy (TRADITION), al-Tunisi subgroups and kingdom dating vs GHA (CONTESTED); Ja'aliyyin and Beja subgroups.
- New stub groups: abdallab (Qerri anchor, 1505–1821, Juhayna genealogy TRADITION), tunjur (Kutum anchor APPROXIMATE, Furra), kababish, rashaida, zaghawa, azande.
- Relations: Funj–'Abdallab alliance against Alwa; Kayra Fur vs Tunjur.
- Quotes are Arabic originals with working English translations. OCR-only quotes carry VERIFY.

## 2026-10-24 — Pass 29: Ethiopian Empire power_cinc_share (IM ruling)
- ethiopian-empire-solomonic: power_cinc_share = 0.24 PARTIAL, 1941–1974 only, COW_NMC6 (RP-CINC-SHARE-1), taken from db/regional_power_scores_post1900.json (Analyst, 44078a3).
- Retired the 0.65 [VERIFY] over 1898–1974 (dd154c8) and its "near 1.0 by construction" flag.
- Excluded: 1898–1936 (Ethiopia the only state of the comparison set, same ruling as Ottoman Egypt); 1937–1940 (no COW rows during the Italian occupation); before 1898 (not a COW member).
