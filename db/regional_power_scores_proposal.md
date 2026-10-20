# Regional power scores – PROPOSAL (Sudan Geopolitical Analyst, 2026-10-20)

**Status: needs the Innovation Manager's sign-off on the method before anything is merged into data/eras.**

## Method (RP-CINC-SHARE-1)
- Formula: score = mean over era years y in [max(start,1816), min(end,2016)] with data of CINC_actor(y) / Σ_{c in set} CINC_c(y); rounded to 2 dp
- Regional set: Sudan 625, South Sudan 626, Egypt 651, Ethiopia 530, Eritrea 531, Chad 483, Libya 620, CAR 482 (states in data that year)
- Null rule: null when no CINC year overlaps the era (pre-statehood, pre-1816 or post-2016). Not extrapolated; WDI given as context only
- WDI: context indicators only (population, GDP current US$, armed forces personnel, military expenditure current US$, surface area); not in the score
- Schema: same as data/eras `regional_power` ({actor, score, basis, method, flag}). The two scores already there (Kush 0.9, Mahdist 0.9) are editorial ordinals, so these computed shares are not on the same footing. That needs deciding.

## Caveats
- The set changes over time: Egypt's early share is inflated because few states existed before 1960. CINC favours population and industry and is weak for low-industry states.
- COW Sudan includes South Sudan before 2011. WDI Sudan excludes it in every year.
- NMC v6 ends in 2016, so 2019–2026 eras are null.
- COW licence wording: free academic use with citation [VERIFY].

## Scores
| era | actor | score | flag |
|---|---|---|---|
| independent-sudan-first-parliamentary-period | Republic of Sudan | 0.1 | COW Sudan (ccode 625) includes South Sudan before 2011 |
| abboud-military-regime | Republic of Sudan | 0.1 | COW Sudan (ccode 625) includes South Sudan before 2011 |
| second-parliamentary-period | Republic of Sudan | 0.09 | COW Sudan (ccode 625) includes South Sudan before 2011 |
| nimeiry-era-democratic-republic-of-sudan | Democratic Republic of the Sudan | 0.11 | COW Sudan (ccode 625) includes South Sudan before 2011 |
| transitional-third-parliamentary-period | Republic of Sudan | 0.12 | COW Sudan (ccode 625) includes South Sudan before 2011 |
| al-bashir-ncp-ingaz-regime | Republic of Sudan (Government of Sudan / NCP) | 0.13 | [PARTIAL COVERAGE] era 1989–2019; scored on 1989–2016 only; years outside are null (pre-state, pre-1816 or post-2016); COW Sudan (ccode 625) includes South Sudan before 2011 |
| december-revolution-transition | Republic of Sudan | None | no CINC: COW NMC v6 ends 2016 and era starts 2019; WDI indicators listed for context only, not scored |
| war-in-sudan-saf-vs-rsf | Republic of Sudan (SAF-led government) | None | no CINC: COW NMC v6 ends 2016 and era starts 2023; WDI indicators listed for context only, not scored |
| republic-of-south-sudan | Republic of South Sudan | 0.07 | [PARTIAL COVERAGE] era 2011–2026; scored on 2011–2016 only; years outside are null (pre-state, pre-1816 or post-2016) |
| republic-of-egypt | Egypt (Republic / UAR / ARE) | 0.55 | [PARTIAL COVERAGE] era 1953–2026; scored on 1953–2016 only; years outside are null (pre-state, pre-1816 or post-2016) |
| derg-federal-ethiopia | Ethiopia | 0.2 | [PARTIAL COVERAGE] era 1974–2026; scored on 1974–2016 only; years outside are null (pre-state, pre-1816 or post-2016) |
| eritrea-italian-colony-independent | Eritrea (state) | 0.08 | [PARTIAL COVERAGE] era 1890–2026; scored on 1993–2016 only; years outside are null (pre-state, pre-1816 or post-2016) |
| french-chad-republic-of-chad | Chad (state) | 0.03 | [PARTIAL COVERAGE] era 1900–2026; scored on 1960–2016 only; years outside are null (pre-state, pre-1816 or post-2016) |
| libya-ottoman-italian-independent | Libya (state) | 0.07 | [PARTIAL COVERAGE] era 1551–2026; scored on 1951–2016 only; years outside are null (pre-state, pre-1816 or post-2016) |
| central-african-republic-ubangi-shari | Central African Republic (state) | 0.01 | [PARTIAL COVERAGE] era 1903–2026; scored on 1960–2016 only; years outside are null (pre-state, pre-1816 or post-2016) |

Indicator values (CINC components for the first and last years, WDI at the last CINC year and latest) are in the JSON for each era.

## Sources
- COW_NMC6: Correlates of War National Material Capabilities v6.0 (abridged CSV) – https://correlatesofwar.org/data-sets/national-material-capabilities/
- WB_WDI_API: World Development Indicators (API v2): SP.POP.TOTL, NY.GDP.MKTP.CD, MS.MIL.TOTL.P1 (IISS), MS.MIL.XPND.CD (SIPRI), AG.SRF.TOTL.K2 – https://api.worldbank.org/v2/country/SDN;EGY;ETH;ERI;TCD;LBY;CAF;SSD/indicator/SP.POP.TOTL
