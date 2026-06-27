# NMF (null magnetic field) → seed localization v1 (2026-06-26)

**Why not GSEA:** the Maffei NNMF panel (~194–230 directional genes) overlaps the 50-gene seed marker
panels by **at most 7 genes (median 0)** across all 122 panels (`results/tables/nmf_panel_overlap.csv`) —
confirming the documented infeasibility of GSEA-prerank for NMF. So we instead **localize** the NMF gene
sets onto germinating-seed cell-type expression specificity.

**Method.** NMF-responsive genes + direction from the Maffei tables (cluster-membership genes via their
shoot-late cluster profile; polyphenol + H₂O₂ panels via per-gene shoot-late log2 ratio). NMF-up = 198,
NMF-down = 18. For each germinating-seed cell type, mean expression-specificity (z across cell types) of
the NMF set vs 1000 random gene sets → localization z. (`scripts/08_nmf_localization.py`)

**Result — NMF-up genes concentrate in:**
| germinating-seed cell type | localization z |
|---|---|
| **radicle apical meristem (cl14)** | **+7.96** |
| unassigned (cl8) | +3.23 |
| cotyledon mesophyll (cl13) | +2.85 |
| cortex/endodermis (cl2) | +1.99 |

NMF-down (n=18, small) → cotyledon mesophyll, cortex/endodermis (weak).

**Interpretation (hypothesis-generating).** Genes induced by near-null magnetic field are preferentially
expressed in the **radicle apical meristem** of the germinating seed — the first structure to resume
growth at germination, and a site of auxin/root-tip signalling. This converges with (i) the high-field
SMF root-meristem/auxin phenotype (Jin 2019) and (ii) the decoder's radicle-meristem light-gated µg
signal — i.e. multiple magnetic/space stressors point at the radicle growth-point program.

**Caveats.** NMF-down set too small (n=18) for a robust direction. Still the partial 194-gene panel, not
genome-wide (full Maffei 2021+2022 arrays pending author request). Concordance/localization, not causation.
