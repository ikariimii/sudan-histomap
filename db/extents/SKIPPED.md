# Extents not drawn as polygons (Sudan Map Designer, 2026-10-25)

Rule: a polygon is drawn only where a readable, citable source gives limits. No coordinates are inferred.
extents_historic.json is unchanged (62 items); the existing anchor points stay as they are.

| Era | What exists now | Why no polygon |
|---|---|---|
| khartoum-mesolithic-early-khartoum | Empty FeatureCollection with a null reason (8681594) | GHA I pp.642, 720 name Early Khartoum, Saggai and Sarurab but give no coordinates or limits ("a site in Khartoum itself"). No Wikidata item for the site. Arkell's *Early Khartoum* (1949) is not on the box and not in data/sources.json, so it can't be cited. A site scatter is not a territory, so an area would be invented. |

What would unblock a polygon:
- Nuer and Anuak: a PD/CC map with tribal limits.
- Dinka: Seligman 1932 *Pagan Tribes of the Nilotic Sudan* map, if a scan is placed on the box and read.
- Early Khartoum: Arkell 1949, registered and read.

## Update 2026-10-25: Seligman 1932 drafts
Draft (not promoted) homeland shapes now exist for Nuer, Dinka and Anuak, plus Shilluk, from the Seligman 1932 folding Tribal Map of Southern Sudan.
They are label-span buffers at confidence 0.3 (APPROXIMATE, SINGLE-SOURCE, EDITORIAL); the plate draws no boundary lines. See
db/border_drafts/SELIGMAN1932_GEOREF.md. The rows above still describe the live state. Khartoum Mesolithic stays point-only (no Arkell map found).
