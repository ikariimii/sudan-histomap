# Border overlay maps (draft, uncommitted): 2026-10-24

The data is in `border_overlay_maps.json`. It lists 6 openly licensed maps, each with 7–10 control points. Pixel positions are on the full-resolution image. They were read from 3840-px previews (kept in /workspace/scratch_overlay, not in the repo) and scaled up, so each one is good to about ±5–10 px.

| # | Map | Year | Licence | Drafts | Points | Affine residual |
|---|-----|------|---------|--------|--------|-----------------|
| 1 | War Office / Intelligence Office Khartoum, *The Anglo-Egyptian Sudan* (LoC, 6894×8558) | 1904 | No known restrictions | restored Darfur, Daju, Tunjur, Musabba'at, Taqali, Funj, Abdallab, Ja'aliyyin | 10 towns | 3–28 km |
| 2 | Prout, *Carte du Kordofan* (Commons/BnF, 7340×8156) | 1876 | PD | Musabba'at, Taqali | 8 graticule intersections | 0 (map space) |
| 3 | Letts, *Eastern Sudan, Kordofan, Abyssinia* (Commons/BnF, 8157×6957) | 1884 | PD | Funj, Abdallab, Ja'aliyyin, Alodia | 4 border ticks + 3 towns | 1–18 km |
| 4 | Stanford, *Map of the Nile… Egyptian Sudan* (Commons/BnF, 6969×8426) | 1883 | PD | Daju, Tunjur, restored Darfur, Musabba'at | 9 towns | 4–51 km (conic projection; use TPS) |
| 5 | Parke & Scoles, *Map of Nubia, 1st–2nd Cataract* (Commons/BnF, 8250×10688) | 1824 | PD | A-Group, C-Group, New Kingdom, Middle Kingdom | 9 sites (original, pre-dam) | 0–8 km |
| 6 | Jacotin, *Carte géographique de l'Égypte* sheet 1 (Commons/BnF, 11842×16964) | 1818 | PD | Ptolemaic, Roman/Byzantine, Middle Kingdom | 9 towns | 5–36 km (Sinai edges worst) |

The residuals come from a test fit with a single affine transform. For maps 1, 3, 4 and 6, use a 2nd-order polynomial or a thin-plate spline (TPS) in QGIS or GDAL.

## Gaps and caveats
- **Draft area coverage:**
  - Taqali (Nuba Hills, about 11°N) is near the southern edge of map 2, so map 1 is the better fit there.
  - Alodia uses an 1884 map, because no open map from that period exists. Soba is a control point.
  - Daju and Tunjur get their Darfur context from maps 1 and 4. No open Keira-era survey was found.
- **Map 2:** the points are graticule intersections only. El Obeid was not found near where the graticule puts it, so check 2–3 real features before trusting it.
- **Map 5:** Kalabsha, Sebua and Faras use their original site coordinates, from before the temples were moved and the valley was flooded by Lake Nasser.
- **Possible follow-ups:**
  - The 1909 Sudan 1:250,000 sheets (LoC 87692353-*) were not used, because the CSV doesn't record which sheet is Wadi Halfa.
  - The 1914 War Office map (LoC 2012593694, TIFF) could serve as a second Darfur source.
  - The 1949 CIA map is too faint in the preview.
