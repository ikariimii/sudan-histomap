# Border-zone overlay check against period maps — 2026-10-24 (Sudan Map Designer)

Method: the 6 maps in `db/border_overlay_maps.json` were downloaded, downscaled to 25 %, and given the
Archivist's control points (GCPs). They were then warped to EPSG:4326 with GDAL 3.10 `gdalwarp -order 2`
(2nd-order polynomial for every map, never affine). Each promoted zone in `db/extents/<id>.geojson` was drawn over
the warped map and judged by eye. The PNGs and warped rasters are in `/workspace/overlay_checks/`
on the shared box and are not committed. Zones were not changed; this file only raises flags.

## Georeferencing residuals (km, computed from GCP fit)

| Map | GCPs | RMS order-2 | max (worst GCP) | leave-one-out RMS order-2 | RMS affine (reference only) |
|---|---|---|---|---|---|
| War Office 1904 (LoC 2013590282) | 10 | 6.95 | 16.5 (El Dueim) | 20.7 | 12.7 |
| Prout 1876 Kordofan | 8 | 0.01 | 0.02 | 0.05 | 0.01 |
| Letts 1884 Eastern Sudan | 7 | 2.30 | 4.5 (Soba ruins) | unstable (1 dof) | 10.5 |
| Stanford 1883 Nile | 9 | 21.28 | 33.3 (Khartoum) | 99 | 27.5 |
| Parke & Scoles 1824 Nubia | 9 | 1.95 | 3.9 (Abu Simbel) | 9.0 | 4.9 |
| Jacotin 1818 Egypt | 9 | 11.10 | 18.7 (Damietta) | 61.6 | 17.0 |

Notes:
- Prout's GCPs are all graticule intersections. The near-zero RMS only shows the graticule is self-consistent. It says nothing about how accurate the 1876 longitudes are.
- Letts has 7 GCPs, which leaves an order-2 fit with 1 degree of freedom. Its low RMS overstates how good the fit is.
- Stanford's fit is too weak for any judgement at the 25 km scale.
- An order-2 warp is unreliable outside the area the GCPs cover. Only the parts of each map that lie inside the GCP area were judged.
- The ~25 km flag threshold is about the same size as the War Office, Stanford and Jacotin residuals. Offsets close to 25 km are within the error of the method.

## Per-zone findings

Verdicts: **FLAG** means the zone is more than ~25 km off what the map shows. **OK** means within ~25 km. **not judgeable** means the map draws no limit for this polity or period, or the warp is too weak.

| Zone (extents id / feature) | Map | Named limit compared | Offset estimate | Verdict |
|---|---|---|---|---|
| restored-darfur-sultanate-ali-dinar / core | War Office 1904 | W edge vs the map's western frontier band (13–15°N) | zone ~20–30 km W of the band (22.45°E vs ~22.7°E at 13.5°N); the zone takes in the "Dar Tama" label | **FLAG (borderline, ~25 km; within warp error)** |
| restored-darfur-sultanate-ali-dinar / core | War Office 1904 | E edge vs the dash-dot line E of Um Kadada (~13.5–14.5°N) | zone ~25–35 km E of the line, but the line is not clearly identified as the Darfur–Kordofan limit | **FLAG (low confidence)** |
| restored-darfur-sultanate-ali-dinar / core | War Office 1904 | S edge | map draws no southern limit | not judgeable |
| restored-darfur-sultanate-ali-dinar / core | Stanford 1883 | W/E edges | the 1883 green frontier is the Egyptian provincial limit, not Ali Dinar's realm; warp RMS 21 km | not judgeable |
| daju-kingdom / core (circle) | War Office 1904, Stanford 1883 | — | no Daju limit drawn; the Jebel Marra anchor sits inside the zone on both maps | not judgeable |
| tunjur-kingdom / core (circle) | War Office 1904, Stanford 1883 | — | no Tunjur limit drawn | not judgeable |
| musabba-at-sultanate-kordofan / influence (circle) | War Office 1904, Prout 1876, Stanford 1883 | — | no Musabba'at limit drawn (pre-1821 polity); El Obeid and Bara fall inside on WO 1904 | not judgeable |
| kingdom-of-taqali / core (circle) | Prout 1876 | E edge vs the map's "TAGALLA"/Dar Tagalla hill mass | the map's Tagalla hills start ~20–25 km E of the zone edge (31.2°E vs ~31.4°E) and run to ~31.95°E; the label is ~90 km E of the zone centre. Prout's longitudes may be shifted east (modern Rashad is ~31.05°E) | **FLAG (low confidence; possible map longitude error)** |
| kingdom-of-taqali / core | War Office 1904 | — | no Taqali limit drawn | not judgeable |
| funj-sultanate-of-sennar / core | War Office 1904, Letts 1884 | — | no Funj limit drawn (later period); Sennar, Roseires and Khartoum sit inside the corridor | not judgeable |
| abdallab-chiefdom-funj-vassal / core | War Office 1904, Letts 1884 | — | no Abdallab limit drawn | not judgeable |
| ja-aliyyin-kingdom-sa-dab-funj-vassal / core | War Office 1904, Letts 1884 | — | no limit drawn; the "El Djahalin" label on Letts sits inside the zone | not judgeable |
| alodia-alwa / core + claimed | Letts 1884 | — | no Alodia limit drawn; the Soba GCP sits inside the core. (Separately from the map check: the core polygon reaches ~13.1°N, south of the Historian's Wad Hedani ruling, so that part is EDITORIAL per the ruling.) | not judgeable |
| a-group-lower-nubia / influence | Parke 1824 | Nile valley, First → Second Cataract | the map's Nile stays inside the zone along its whole length | OK (no polity limit on the map) |
| c-group-lower-nubia / influence | Parke 1824 | Nile valley, First → Second Cataract | the map's Nile stays inside the zone | OK (no polity limit on the map) |
| egyptian-new-kingdom-rule-in-nubia / core | Parke 1824 | E edge vs the Nile, ~23.0–23.4°N (Gerf Hussein bend) | the map's Nile runs up to ~15–20 km E of, i.e. outside, the core edge on that stretch | OK (<25 km), worth tidying |
| middle-kingdom-egypt / core + claimed | Parke 1824 | Nile, Aswan → Semna (Second Cataract) | Nile within the claimed zone; the S end (~21.3–21.5°N) agrees with the Second Cataract on the map to ~10 km | OK |
| middle-kingdom-egypt / core | Jacotin 1818 | Nile valley and Delta | the valley sits inside the corridor at the map's resolution | OK |
| ptolemaic-egypt / core | Jacotin 1818 | N edge vs the Mediterranean coast of the Delta (30.3–32.3°E) | the zone's N edge at 31.2°N runs ~25–35 km S of the coast shown (~31.45–31.5°N, Rosetta/Damietta), leaving out the northern Delta | **FLAG (~25–35 km)** |
| roman-byzantine-egypt / core | Jacotin 1818 | N edge vs the Delta coast | same 31.2°N edge, ~25–35 km S of the coast | **FLAG (~25–35 km)** |
| roman-byzantine-egypt / claimed | Jacotin 1818 | S limit (Hiera Sycaminos area) | no period limit drawn | not judgeable |

Summary of flags: Ptolemaic core and Roman-Byzantine core (N edge vs Delta coast, ~25–35 km); Ali Dinar core
(W edge ~20–30 km, E edge ~25–35 km, low confidence); Taqali core (map's Tagalla hills ~20–25 km E of the edge, low
confidence). The Historian should decide on each of these. No geometry was edited.
