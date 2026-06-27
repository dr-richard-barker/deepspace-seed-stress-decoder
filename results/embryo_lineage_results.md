# Embryo-lineage bridge — developing-embryo state → germinating-seed cell type (2026-06-27)

**Rationale.** Only the embryo lineage persists development → dry/dormant → germination (seed coat,
endosperm, funiculus, ovule are terminal/maternal). So the dev side of the bridge was restricted to
Gehring **embryo cells only** (5,683 of 54,210), pseudobulked by embryo cell-STATE (level_3, 15 states
≥40 cells), ssGSEA'd onto the 15 germinating-seed cell types, within-source scaled (v3 method).
`scripts/14_bridge_embryo_lineage.py` → `results/tables/embryo_lineage_map.csv`,
`results/figures/embryo_lineage_heatmap.png`.

## Result — the map recovers TEXTBOOK developmental lineages (positive control)
| developing-embryo state (3–7 DAP) | → germinating-seed cell type | z | known lineage? |
|---|---|---|---|
| **EMB protoderm** (upper/lower) | **epidermis** (cl6) / radicle epidermis | +1.6 / +1.1 | ✔ protoderm → epidermis |
| **EMB hypophysis** | **radicle apical meristem** (cl14) | +2.14 | ✔ hypophysis founds the root meristem/QC |
| **EMB vascular primordium** | **provasculature: protoxylem** (cl9) / provasc (cl12) | +1.88 | ✔ vascular primordium → provasculature |
| **EMB inner cotyledon** | **cotyledon mesophyll** (cl3) | +1.08 | ✔ |
| **EMB cortical initials** | **hypocotyl cortex (early)** (cl5) | +1.07 | ✔ cortical initials → cortex |
| EMB ground-tissue initials / S-phase / G2M | unassigned (cl8/cl11) | 0.6–1.4 | cycling/initial states → no fixed germ identity (clusters 8/11) |

## Why this matters
1. **Methodological validation (positive control).** The decoder+bridge independently re-derives
   established embryo→seedling lineage relationships from transcriptomes alone — strong evidence the
   panel/projection machinery is sound, not pattern-matching noise.
2. **Cleaner dev→germination bridge.** Removing maternal/endosperm tissue resolves the v1/v2/v3
   "weak/non-specific dev" problem into specific, biologically correct mappings.
3. **Reinforces the radicle convergence story with a developmental origin.** The **hypophysis → radicle
   apical meristem** edge means the very structure that NMF (z+7.96 localization), microgravity
   (light-gated), and high static field (Jin SMF auxin) all converge on is *founded by the embryonic
   hypophysis* — giving the radicle growth-point hypothesis a developmental-lineage root.

## Caveats
- Gehring atlas is **early** development (3–7 DAP); embryo is small (globular/heart-stage), so states are
  young and a few subclusters are noisy (e.g., "EMB up proto I" → protophloem; cell-cycle states →
  unassigned). The major lineages above are robust; minor subclusters are suggestive.
- Concordance/transfer, not lineage tracing; confirms transcriptional similarity, not literal descent.
