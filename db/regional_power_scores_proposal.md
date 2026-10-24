# Regional power scores – PROPOSAL (Sudan Geopolitical Analyst, 2026-10-20)

**Status: method approved by the Innovation Manager on 2026-10-24 for modern eras only (CINC years 1816–2016). Staging file; not merged into data/eras.**

## Rulings (2026-10-24)
- Field `power_cinc_share`: computed CINC regional share, cited to COW NMC v6.0 with the year range actually scored; valid 1816–2016 only.
- Field `power_editorial`: the existing hand scores (Kush 0.9, Mahdist 0.9), copied unchanged and badged EDITORIAL. Never rescaled or mixed with `power_cinc_share`. No new hand scores before 1816.
- 2019 and 2023 eras: `power_cinc_share` null, reason "data ends 2016".

## Method (RP-CINC-SHARE-1)
- Formula: score = mean over era years y in [max(start,1816), min(end,2016)] with data of CINC_actor(y) / Σ_{c in set} CINC_c(y); rounded to 2 dp
- Regional set: Sudan 625, South Sudan 626, Egypt 651, Ethiopia 530, Eritrea 531, Chad 483, Libya 620, CAR 482 (states in data that year)
- Null rule: null when no CINC year overlaps the era (pre-statehood, pre-1816 or post-2016). Not extrapolated; WDI given as context only
- WDI: context indicators only (population, GDP current US$, armed forces personnel, military expenditure current US$, surface area); not in the score
- Schema: `power_cinc_share` = {actor, share, year_range, cite, basis, method, source_ids, flag, null_reason}; `power_editorial` = {era_id, actor, score, basis, method, badge: EDITORIAL}.

## Caveats
- CINC underrates states with little industry: it weights iron/steel and energy alongside population and military, so low-industry states such as Sudan, Chad, CAR and Eritrea score low regardless of other forms of power.
- Egypt's share is inflated before 1960: the regional set is small then (few states were independent), so Egypt's share of it is high partly because there is little to share with.
- CINC (COW ccode 625) counts South Sudan inside Sudan before 2011; the World Bank WDI figures for Sudan exclude South Sudan in every year. The two sources are not aligned before 2011.
- The CINC share scale is not comparable with the editorial scores (`power_editorial`, Kush and Mahdist 0.9): one is a computed share of a regional set, the other a hand-assigned ordinal.
- The regional set changes over time, so shares are not comparable across eras with different sets.
- NMC v6 ends in 2016, so the 2019 and 2023 eras are null ("data ends 2016"). COW now publishes v7.0 (to 2022); it is not used here.
- COW licence: no licence statement on the COW NMC page or in the v6.0 codebook (both read 2026-10-24); the page asks users to give the version number and cite Singer, Bremer & Stuckey (1972). Reuse rights beyond citation are not stated.

## Scores
| era | actor | power_cinc_share (years scored in flag) | flag |
|---|---|---|---|
| independent-sudan-first-parliamentary-period | Republic of Sudan | 0.1 | COW Sudan (ccode 625) includes South Sudan before 2011 |
| abboud-military-regime | Republic of Sudan | 0.1 | COW Sudan (ccode 625) includes South Sudan before 2011 |
| second-parliamentary-period | Republic of Sudan | 0.09 | COW Sudan (ccode 625) includes South Sudan before 2011 |
| nimeiry-era-democratic-republic-of-sudan | Democratic Republic of the Sudan | 0.11 | COW Sudan (ccode 625) includes South Sudan before 2011 |
| transitional-third-parliamentary-period | Republic of Sudan | 0.12 | COW Sudan (ccode 625) includes South Sudan before 2011 |
| al-bashir-ncp-ingaz-regime | Republic of Sudan (Government of Sudan / NCP) | 0.13 | [PARTIAL COVERAGE] era 1989–2019; scored on 1989–2016 only; years outside are null (pre-state, pre-1816 or post-2016); COW Sudan (ccode 625) includes South Sudan before 2011 |
| december-revolution-transition | Republic of Sudan | null – data ends 2016 | no CINC: COW NMC v6 ends 2016 and era starts 2019; WDI indicators listed for context only, not scored |
| war-in-sudan-saf-vs-rsf | Republic of Sudan (SAF-led government) | null – data ends 2016 | no CINC: COW NMC v6 ends 2016 and era starts 2023; WDI indicators listed for context only, not scored |
| republic-of-south-sudan | Republic of South Sudan | 0.07 | [PARTIAL COVERAGE] era 2011–2026; scored on 2011–2016 only; years outside are null (pre-state, pre-1816 or post-2016) |
| republic-of-egypt | Egypt (Republic / UAR / ARE) | 0.55 | [PARTIAL COVERAGE] era 1953–2026; scored on 1953–2016 only; years outside are null (pre-state, pre-1816 or post-2016) |
| derg-federal-ethiopia | Ethiopia | 0.2 | [PARTIAL COVERAGE] era 1974–2026; scored on 1974–2016 only; years outside are null (pre-state, pre-1816 or post-2016) |
| eritrea-italian-colony-independent | Eritrea (state) | 0.08 | [PARTIAL COVERAGE] era 1890–2026; scored on 1993–2016 only; years outside are null (pre-state, pre-1816 or post-2016) |
| french-chad-republic-of-chad | Chad (state) | 0.03 | [PARTIAL COVERAGE] era 1900–2026; scored on 1960–2016 only; years outside are null (pre-state, pre-1816 or post-2016) |
| libya-ottoman-italian-independent | Libya (state) | 0.07 | [PARTIAL COVERAGE] era 1551–2026; scored on 1951–2016 only; years outside are null (pre-state, pre-1816 or post-2016) |
| central-african-republic-ubangi-shari | Central African Republic (state) | 0.01 | [PARTIAL COVERAGE] era 1903–2026; scored on 1960–2016 only; years outside are null (pre-state, pre-1816 or post-2016) |

Indicator values (CINC components for the first and last years, WDI at the last CINC year and latest) are in the JSON for each era.

## power_editorial (EDITORIAL, unchanged from data/eras)
| era | actor | score |
|---|---|---|
| kingdom-of-kush-napatan-period | Kush (25th Dynasty, c.713–664 BCE) | 0.9 EDITORIAL |
| mahdist-state-mahdiyya | Mahdist state (within Sudan, 1885–98) | 0.9 EDITORIAL |

## Sources
- COW_NMC6: Correlates of War National Material Capabilities v6.0 (abridged CSV) – https://correlatesofwar.org/data-sets/national-material-capabilities/
- WB_WDI_API: World Development Indicators (API v2): SP.POP.TOTL, NY.GDP.MKTP.CD, MS.MIL.TOTL.P1 (IISS), MS.MIL.XPND.CD (SIPRI), AG.SRF.TOTL.K2 – https://api.worldbank.org/v2/country/SDN;EGY;ETH;ERI;TCD;LBY;CAF;SSD/indicator/SP.POP.TOTL
