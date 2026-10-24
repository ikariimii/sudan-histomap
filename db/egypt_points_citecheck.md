# Egypt stream reference points – GHA page cite check (Historian, 2026-10-24)

Checked: every page cite in the 13 point features of the six ancient-Egypt eras added in Map Designer's commit f23668a (db/extents/*.geojson; the same points are in extents_historic.json). I compared each one against the box OCR text of UNESCO *General History of Africa* vol. II. GHA II printed page = PDF page − 17, which is consistent on every page checked. Files were read only, with no edits.

| Era | Point | Cited | Result |
|---|---|---|---|
| early-dynastic-old-kingdom | Elephantine (nomarch under Pepi II; "Elephantine and Thinis") | ch.2 pp.94–95 | OK: p.94 nomarch of Elephantine/Pepi II; p.95 "Elephantine and Thinis" |
| early-dynastic-old-kingdom | Buhen (Old Kingdom colony, copper) | ch.9 p.250; ch.8 p.235 | OK: p.250 "purely Egyptian colony at Buhen in the fourth and fifth dynasties"; p.235 copper-smelting furnaces |
| middle-kingdom | Semna (southern frontier) | pp.240, 255, 258 | OK, but note that p.258 holds the "unquestionably fixed at Semna" quote; p.255 the Senusret III boundary stele; p.240 "Sesostris III fixed the Egyptian frontier at Semna". p.240 is in **ch.8** (pp.226–244), not ch.9. The feature lists GHA2_CH9 + GHA2, so the cite is covered by GHA2, but GHA2_CH8 would be more precise |
| middle-kingdom | Buhen fortress (12th dyn., to Semna) | pp.255, 258 | OK |
| new-kingdom | Pi-Ramesses | WP:New_Kingdom_of_Egypt, no page | N/A (Wikipedia, no GHA page to check) |
| new-kingdom | Kurgus frontier | p.265 | OK: "the whole reach between Kerma and Kurgus" (ch.10). The Hagar el-Merwa part rests on WP_KANISAH_KURGUS, not GHA |
| new-kingdom | Napata / Fourth Cataract | p.270 | OK: viceroy of Kush and Fourth Cataract on p.270 |
| late-period-persian | Elephantine "frontier between Egypt and Ethiopia" | pp.107, 197, 286 | OK: p.197 Herodotus quote (ch.6); p.107 Cambyses (ch.2); p.286 Cambyses/Batn el-Hagar (ch.10) |
| ptolemaic | Alexandria | pp.189–190 | OK: p.190 "the major political role was still held by Memphis … Ptolemy II established the seat … permanently there" (p.189 = founding by Alexander) |
| ptolemaic | Hiera Sycaminos / Dodecaschoenus | p.208 | OK: "had belonged to the Ptolemies" on p.208. Note that p.208 is the first page of ch.7 (Roman Egypt), and the feature correctly cites GHA2_CH7 |
| roman-byzantine | Alexandria | p.210 | OK: "now became the capital instead of Memphis" |
| roman-byzantine | Hiera Sycaminos frontier | pp.208, 290 | OK: p.290 "fixed at Hiera Sycaminos (Muharraqa)" |
| roman-byzantine | Philae / First Cataract | pp.215, 294 | OK: p.215 "gave up Nubia"; p.294 Diocletian "pulled back the frontier to the First Cataract" (Procopius) |

**Result:** 12 of 12 GHA cites are OK, and no page needs correcting. There is one precision note: Semna p.240 is in ch.8. One point is Wikipedia-only and has no page.
