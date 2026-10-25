# Seligman 1932 Tribal Map of Southern Sudan: georeferencing and drafts (Sudan Map Designer, 2026-10-25)

Source: C.G. & B.Z. Seligman, *Pagan Tribes of the Nilotic Sudan* (Routledge, 1932), folding plate "Tribal Map of Southern Sudan"
(unpaginated, end of volume). Scan: https://archive.org/details/in.gov.ignca.2109/page/n717/mode/1up (leaf n717, 4982×5181 px, full sheet with title, scale bar and
graticule 24–36°E, 4–16°N; checked visually). Registry: **not registered** (proposed ID `SELIGMAN1932`).

## Rights
Not confirmed PD, so the scan is **not committed** (kept on the shared box at /workspace/seligman/).
IA item metadata has no licence or rights field (Digital Library of India upload). C.G. Seligman died 1940 (UK PD for his share since 2011),
but co-author Brenda Z. Seligman died 1965 (UK term runs to end-2035). In the US, a 1932 publication enters PD on 1 Jan 2028.
The cartographer is not credited. Only derived label positions (facts) are used here.

## Georeferencing
30 GCPs at printed graticule intersections, 28–36°E × 4–14°N (pixel coords on the full-res leaf n717_w4000.jpg).
24°E, 26°E and 16°N lines were left out: they're faint and broken by labels and rivers, so automatic picks were unreliable.
GDAL 3.10 `gdal_translate -gcp …` then `gdalwarp -order 2`.

| Fit | RMS (km) | max (km) | leave-one-out RMS (km) |
|---|---|---|---|
| order 2 (used) | 1.33 | 2.91 (32°E 14°N) | 1.71 |
| affine (reference) | 4.83 | 10.2 (36°E 4°N) | 5.65 |

As with Prout in OVERLAY_CHECK.md, an all-graticule fit only shows the graticule is self-consistent; it doesn't measure the accuracy of 1932 positions.

| lon | lat | px x | px y |
|---|---|---|---|
| 28°E | 14°N | 1944 | 1234 |
| 28°E | 12°N | 1929 | 1877 |
| 28°E | 10°N | 1917 | 2520 |
| 28°E | 8°N | 1902 | 3157 |
| 28°E | 6°N | 1890 | 3803 |
| 28°E | 4°N | 1878 | 4449 |
| 30°E | 14°N | 2560 | 1243 |
| 30°E | 12°N | 2548 | 1886 |
| 30°E | 10°N | 2539 | 2529 |
| 30°E | 8°N | 2536 | 3172 |
| 30°E | 6°N | 2527 | 3821 |
| 30°E | 4°N | 2515 | 4464 |
| 32°E | 14°N | 3191 | 1243 |
| 32°E | 12°N | 3182 | 1883 |
| 32°E | 10°N | 3176 | 2532 |
| 32°E | 8°N | 3173 | 3175 |
| 32°E | 6°N | 3167 | 3824 |
| 32°E | 4°N | 3164 | 4470 |
| 34°E | 14°N | 3801 | 1240 |
| 34°E | 12°N | 3807 | 1883 |
| 34°E | 10°N | 3813 | 2532 |
| 34°E | 8°N | 3810 | 3178 |
| 34°E | 6°N | 3810 | 3830 |
| 34°E | 4°N | 3810 | 4482 |
| 36°E | 14°N | 4436 | 1225 |
| 36°E | 12°N | 4445 | 1874 |
| 36°E | 10°N | 4451 | 2532 |
| 36°E | 8°N | 4454 | 3178 |
| 36°E | 6°N | 4457 | 3836 |
| 36°E | 4°N | 4463 | 4491 |

## Drafts (confidence 0.3, APPROXIMATE + SINGLE-SOURCE + EDITORIAL)
The plate draws **no tribal boundary lines**, only spread-letter labels. Each draft is a 0.3° buffer around the centres of the
spread letters of the main label, so every edge is inferred (EDITORIAL). Shows the 1910s–30s distribution, not each era's span.

| File | Label | bbox (W,S,E,N) |
|---|---|---|
| seligman1932-nuer-naath-communities.geojson | NUER | 29.48, 8.37, 33.64, 9.02 |
| seligman1932-dinka-jieng-communities.geojson | DINKA ×2 (W and E of White Nile) | 27.39, 5.95, 33.60, 12.14 |
| seligman1932-anuak-anywaa-communities.geojson | ANUAK | 32.99, 6.42, 34.73, 8.14 |
| seligman1932-shilluk-kingdom.geojson | SHILLUK | 30.98, 9.33, 32.37, 10.52 |

Not used: Evans-Pritchard 1940 (in-copyright upload; lead only, not opened). Not built into `_all_drafts.geojson` (build_drafts.py not run).
