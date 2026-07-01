# Supplementary Materials

**A cell-type-resolved atlas of deep-space stress susceptibility in the dry and germinating Arabidopsis seed**
Richard Barker (Purdue University; The Collaborative Science Environment, PBC). *npj Microgravity.*

Contents: Supplementary Methods · Supplementary Tables S1–S6 · Supplementary Figures S1–S5 · Evidence-tier
audit. All tables are provided as machine-readable files in the code repository (paths given); key items are
summarised inline. Figures are reproduced by `scripts/20`–`scripts/26`.

---

## Supplementary Methods

**Seed single-cell reference.** Developmental atlas: Gehring lab snRNA-seq, 3/5/7 DAP (GEO GSE295007;
23,374 genes × 54,210 nuclei; level_1 5 tissues → level_2 13 cell types → level_3 85 states + 43 GO
module scores). Germination atlas: Liew/Lewsey scRNA-seq, 12/24/48 h (matrix via GEO mirror GSE182331;
13,501 genes × 12,798 cells; 15 clusters named from the source paper, clusters 9/14 in-situ validated).
Marker panels: Wilcoxon `rank_genes_groups`, top-50 genes/group, ≥20 cells → 122 panels (GMT in
`panels/panel_library.gmt`). The **dry/0 h pole** is anchored by a bulk-tier `dry_seed` panel (top-50 genes
up in mature dry seed, 21 vs 15 DAP, GSE76015, mean of 3 WT ecotypes) → 123 panels total.

**Stressor signatures (27 contrasts, 10 families).** Genome-wide differential expression / treatment-vs-
control signatures harmonised to AGI/TAIR (Entrez, Affymetrix ATH1/GPL198 and Agilent GPL9020 maps in
`data/raw/`). Sources in Table S1/S2. Null-magnetic-field (NMF) handled by **expression-localization**
(panel too small for GSEA; ≤7-gene marker overlap): NMF-up/down gene specificity (z) vs 1,000 random sets;
two panels (2022 oxidative; 2021 Sci Rep S7 DEGs).

**Projection (DSRS / GSAD).** Each signature ranked by log2FC and projected onto the panels by pre-ranked
GSEA (`gseapy`; 200 permutations; seed 42) → NES + FDR per panel. DSRS scores query↔reference fingerprint
similarity (rank correlation). GSAD returns the per cell-type/tissue/stage susceptibility profile.

**Bridge (shared latent).** Germinating-seed score space (15 axes). Adult stress placed by decoder NES;
late-seed-dev by ssGSEA of Gehring pseudobulk. **Within-source scaling** removes a score-type artefact
(PC1↔source |r| 0.38→0.00). Embryo-lineage variant recovers textbook developmental lineages (positive
control).

**Atlas / convergence.** A cell type/stage is "susceptible" to a family if any contrast in that family has
|NES| ≥ 1.5 & FDR < 0.25 (or NMF localization |z| ≥ 2). Convergence = number of the 10 families meeting the
threshold (family-level voting prevents data-rich families from dominating).

**NMF radicle-risk genes & root pictograms (scripts 28–29).** NMF-responsive genes (per-gene NMF shoot
late-timepoint log2 ratio; up > 0.1, down < −0.1) were intersected with germinating-seed cell-type
expression specificity (z of log-CPM pseudobulk across the 15 germination clusters). A gene is a
radicle-risk locus if its specificity in the radicle apical meristem (cluster 14) is ≥ 1.0. For the
ePlant-style pictograms, germination clusters were mapped to root anatomical compartments — root cap
(columella/root cap), meristem/QC (radicle apical meristem), epidermis (radicle epidermis),
cortex/endodermis, and stele/vasculature (provasculature + protoxylem + protophloem) — and each locus's
per-compartment expression (log-CPM) painted onto a longitudinal root schematic. Collective panels use the
set-mean specificity per compartment; a NET (up−down) contrast identifies zones of synergy (both sets
concentrated) vs antagonism (opposite bias).

**Software / reproducibility.** `deepspace` Python package (DSRS + GSAD + CLI); numbered scripts 01–29;
deterministic seeds; `REPRODUCE.md`. MIT license.

---

## Supplementary Tables (machine-readable in repo)
- **Table S1 — Data inventory** (all datasets, accessions, platform, role, evidence tier, caveats):
  `data/data_inventory.csv`.
- **Table S2 — Stressor contrast manifest** (27 contrasts: family, dataset, dose/time, genotype):
  `results/tables/contrast_classes.csv` + `radiation_contrasts_manifest.csv`.
- **Table S3 — Decoder NES/FDR matrix** (123 panels × 27 contrasts): `results/tables/decoder_nes_matrix_v7.csv`,
  `decoder_fdr_matrix_v7.csv`.
- **Table S4 — Atlas convergence** (cell-type and tissue/stage): `results/tables/deepspace_atlas_convergence.csv`,
  `deepspace_atlas_tissue_stage_convergence.csv`.
- **Table S5 — NMF localization** (2022 + 2021 panels): `results/tables/nmf_localization.csv`,
  `nmf2021_localization.csv`.
- **Table S6 — Panel library** (123 seed cell-type/state panels): `panels/panel_library.csv` /
  `panel_library.gmt`.
- **Table S7 — NMF radicle-risk genes** (NMF-responsive genes specifically expressed in the radicle
  apical meristem, with TAIR IDs + symbols, NMF direction, and per-compartment root expression):
  `results/tables/nmf_radicle_risk_genes.csv` (up, n=32), `nmf_radicle_risk_genes_down.csv` (down, n=2),
  `nmf_root_zone_expression.csv` (root-compartment log-CPM).

---

## Evidence-tier audit (key claims)
| Claim | Tier | Basis | Falsification |
|---|---|---|---|
| Root/radicle tip = top multi-stressor hotspot (columella 9/10, radicle meristem 6/10) | D×A→H | genome-wide DGE projected onto validated panels | per-stressor knock-down / spaceflight germination; predict root-tip-program shift |
| Early germination (12 h) = most vulnerable stage | D→H | family convergence over stage panels | tissue-matched stress panel; predict 12 h > 24/48 h |
| NMF-up genes → radicle apical meristem (z +7.96) | L×A→H | expression localization (2022 oxidative panel) | NNMF germination + cry1cry2; radicle-meristem markers |
| NMF radicle signal is oxidative-panel-specific | L×A | 2021 DEG panel does not reproduce it (r=0.35) | full genome-wide NNMF arrays (pending) |
| NMF-up radicle set = ROS-producing peroxidase/oxidase battery; NMF-down = ROS scavengers (SOD1, MSRB7) | L×A→H | NMF gene directions × radicle-apical-meristem specificity (Table S7) | genome-wide NNMF germination + redox reporters at the radicle tip |
| Meristem/QC is a redox synergy hotspot (up + down sets both concentrate); surrounding tissues down-biased | A→H | collective root-compartment localization (Fig S8) | spatial ROS imaging under NNMF germination |
| Embryo lineage recovered (hypophysis→radicle meristem etc.) | A | positive control, transcriptome-only | lineage tracing / marker persistence |
| Dry-seed program induced by desiccation, suppressed by ethylene | D×A | decoder NES on dry_seed panel | ABA/ethylene dose; dormancy markers |

All atlas/decoder outputs are **predicted concordance (signature transfer), not proven causation.**

---

## Supplementary Figures
*(embedded below; high-res PNG+SVG in `results/figures/`)*

- **Fig S1** — Combined 27-contrast perturbation model (10 stressor families) → seed programs.
- **Fig S2** — Shared-latent bridge (within-source scaled): heatmap + PCA embedding.
- **Fig S3** — Atlas at tissue + germination-stage level (incl. dry-seed anchor).
- **Fig S4** — NMF-responsive gene localization (2022 oxidative panel).
- **Fig S5** — NMF localization cross-check: 2022 oxidative panel vs 2021 Sci Rep NNMF DEGs.
- **Fig S6** — NMF radicle-risk genes: expression specificity (z) across germinating-seed cell types for
  the NMF-up set (n=32) and NMF-down set (n=2); radicle apical meristem column boxed.
- **Fig S7** — ePlant-style root pictograms per NMF-up threat locus: expression (log-CPM) across root
  compartments (root cap, meristem/QC, epidermis, cortex/endodermis, stele) of the germinating-seed radicle.
- **Fig S8** — Collective NMF localization in the root: NMF-up vs NMF-down set specificity per compartment,
  with a NET (up−down) panel identifying the meristem/QC as a synergy hotspot.

*Root-map provenance: the "root" in Figs S7–S8 is the germinating-seed single-cell radicle (GSE182331) mapped
to anatomical compartments — the seed's own root, not the mature-root eFP.*
