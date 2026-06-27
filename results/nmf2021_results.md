# Second NMF localization panel — Maffei/Paponov 2021 (Sci Rep s41598-021-88695-6) — 2026-06-27

**Source.** Public **supplementary Data Set S7** (MOESM2.xlsx) of the 2021 "Differential root and shoot
magnetoresponses" paper — per-timepoint (10 min–96 h) NNMF DEG lists, root + shoot. *(The full genome-wide
arrays are still pending the Maffei author reply; this uses only the published DEG tables.)*
`scripts/25_nmf2021_localization.py` → `results/tables/nmf2021_{gene_directions,localization}.csv`,
`results/figures/nmf_localization_2021v2022.png`.

**Panel.** 2499 NNMF-responsive AGI genes (union across timepoints); 333 localizable in the germination
atlas. Localized onto germinating-seed cell-type expression specificity (z vs 1,000 random sets), same
method as the 2022 panel (`scripts/08`).

## Result — 2021 vs 2022 (cross-check)
| germinating-seed cell type | 2022 NMF-up (oxidative panel) z | 2021 NNMF DEGs (undirected) z |
|---|---|---|
| **radicle apical meristem (cl14)** | **+8.0** | +0.1 |
| cotyledon mesophyll (cl13) | +2.8 | **+4.1** |
| hypocotyl cortex (mid/late) | −1.8 / −4.3 | +1.7 / +1.1 |
| unassigned (cl8) | +3.2 | +9.2 (soft) |

- **Convergence:** both panels are positive at **cotyledon mesophyll** (and the unassigned cl8).
- **Divergence / important qualifier:** the **radicle-apical-meristem signal is specific to the 2022
  oxidative panel** (z +8.0); the broader 2021 NNMF DEG set does *not* reproduce it (z ~0) and instead
  favors cotyledon mesophyll + hypocotyl cortex. Cross-cell-type correlation **r = 0.35** (moderate).
- **Reading:** the NMF→radicle-meristem claim should be stated as **oxidative-NNMF-gene-specific**, not a
  property of all NNMF-responsive genes. NMF's broader footprint includes the cotyledon/hypocotyl.

## Caveats
- **Direction unreliable** from the formatted workbook (up-blocks not in the col-1 layout → net came out
  implausibly down-skewed); the **undirected union** is the robust panel used here.
- Only 333/2499 genes localizable (rest not expressed/specific in the germination atlas).
- Different study/design than 2022 (time-course root+shoot vs oxidative panel) — expected partial overlap.
- **TO UPGRADE on Maffei reply:** replace this DEG-list panel with the full genome-wide 2021 + 2022 arrays
  → full GSEA decoder contrasts (not just localization). See README §1 / author-request email.
