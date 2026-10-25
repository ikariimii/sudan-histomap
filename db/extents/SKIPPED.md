# Extents not drawn as polygons (Sudan Map Designer, 2026-10-25)

Rule: a polygon is drawn only where a readable, citable source gives limits. No coordinates are inferred.
extents_historic.json is unchanged (62 items); the existing anchor points stay as they are.

| Era | What exists now | Why no polygon |
|---|---|---|
| khartoum-mesolithic-early-khartoum | Empty FeatureCollection with a null reason (8681594) | GHA I pp.642, 720 name Early Khartoum, Saggai and Sarurab but give no coordinates or limits ("a site in Khartoum itself"). No Wikidata item for the site. Arkell's *Early Khartoum* (1949) is not on the box and not in data/sources.json, so it can't be cited. A site scatter is not a territory, so an area would be invented. |
| anuak-anywaa-communities | 1 APPROXIMATE Pibor river point (EP1940_NUER p.112) | EP1940_NUER p.112 gives only one river divide ("the Pibor separates the Lou tribe from the Anuak people"). EP1940_ANUAK is registered but has not been read for limits. One river edge can't close a polygon. |
| dinka-jieng-communities | 1 APPROXIMATE point (LOC1991, GHA5_CH7 p.193, GHA7_CH23 p.594) | Sources give regions (Upper Nile, Bahr al-Ghazal) and a Renk-to-Uganda range (QASIM_MAWSUA vol.2 p.911), not limits. This is a people, not a polity, so it's rendered on the Homelands layer. |
| nuer-naath-communities | 2 APPROXIMATE river points (EP1940_NUER p.112: Pibor, Zeraf) | Text gives river divides only (Pibor, Zeraf, Sobat, White Nile, Lake Jorr; GHA7_CH4 p.81). The sketch map in Evans-Pritchard's *The Nuer* (1940) was not read on the box, and it is still in copyright in the UK (author d. 1973), so it isn't a PD source to trace. |

What would unblock a polygon:
- Nuer and Anuak: a page-level read of the EP1940 sketch maps (cite only, no tracing), or a PD/CC map with tribal limits.
- Dinka: Seligman 1932 *Pagan Tribes of the Nilotic Sudan* map, if a scan is placed on the box and read.
- Early Khartoum: Arkell 1949, registered and read.

## Update 2026-10-25: Seligman 1932 drafts
Draft (not promoted) homeland shapes now exist for Nuer, Dinka and Anuak, plus Shilluk, from the Seligman 1932 folding Tribal Map of Southern Sudan.
They are label-span buffers at confidence 0.3 (APPROXIMATE, SINGLE-SOURCE, EDITORIAL); the plate draws no boundary lines. See
db/border_drafts/SELIGMAN1932_GEOREF.md. The rows above still describe the live state. Khartoum Mesolithic stays point-only (no Arkell map found).
