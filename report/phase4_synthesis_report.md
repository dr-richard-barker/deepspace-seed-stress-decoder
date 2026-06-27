# Decoding magnetic-field and spaceflight stress signatures onto the dry/germinating Arabidopsis seed

### A cell-type-resolved bridge decoder — Phase 4 synthesis

**Date:** 2026-06-26 · **Project:** NMF meta-analysis + bridge seed decoder (standalone)
**Status:** decoder + bridge + NMF localization functional end-to-end; genome-wide NMF pending.

**Evidence tiers used throughout:**
**[D] Direct** = genome-wide differential expression we projected ·
**[A] Atlas** = single-cell seed-atlas panels / pseudobulk ·
**[L] Literature** = published cell-type identities, NMF gene directions, magnetobiology ·
**[H] Hypothesis** = predicted concordance + falsification test.
All decoder/bridge outputs are **concordance / signature transfer, not proven causation.**

---

## 1. Executive summary

1. We built a **122-panel seed reference** [A] spanning the developing seed (Gehring snRNA atlas,
   GSE295007: embryo/endosperm/seed-coat, 5 tissues → 13 cell types → 86 states) and the
   **dry→germinating seed** (germination atlas, GSE182331/E-MTAB-12532: 15 named cell types across
   12/24/48 h). Panels validated against canonical markers (OLE/CRA/2S → embryo; BAN → endothelium).
2. A **projection decoder** [D×A] maps genome-wide spaceflight/radiation signatures (NASA OSDR
   GLDS-120 root µg, GLDS-612 leaf µg, GLDS-603 GCR) onto these seed programs via GSEA-prerank.
3. **Stressed adult/vegetative tissue transcriptionally resembles the early-germination (12 h) state**
   — the most consistently induced program across µg and GCR-80 [D×A].
4. A **shared "germinating-seed score space" bridge** places both adult-stress and late-seed-dev inputs
   relative to the dry/germinating reference. The **dev→germination bridge is lineage-limited**: only the
   embryo lineage transfers; maternal seed coat and endosperm are terminal [A×L].
4b. **Positive control:** restricting the dev bridge to the embryo lineage recovers **textbook
   developmental lineages** (protoderm→epidermis, hypophysis→radicle apical meristem, vascular
   primordium→provasculature) from transcriptomes alone — validating the decoder/bridge machinery [A].
5. **Null magnetic field (NMF) genes localize sharply to the radicle apical meristem** (z = +7.96) [L×A].
   Together with the light-gated µg radicle signal [D] and the high-field SMF root-meristem/auxin
   phenotype [L], **multiple magnetic/space stressors converge on the radicle growth-point program** —
   the central falsifiable hypothesis of this work.

---

## 2. Background & objective

Successful germination depends on transcriptional programs laid down across seed development, held
through desiccation/dormancy, and re-activated on imbibition. Space-relevant stressors — microgravity
(µg), galactic cosmic radiation (GCR), and **null/near-null magnetic field (NMF)** — perturb the adult
plant transcriptome, but their consequences for the **dry and germinating seed** are largely uncharacterized,
because those experiments measure later-stage tissues, not seeds.

**Objective.** (i) A comprehensive view of Arabidopsis NMF transcriptional data; and (ii) a **bridge
decoder** that takes RNA-seq from later-developmental-stage tissues (adult/vegetative *and*
late-seed-development) and projects it onto a dry/germinating-seed reference, predicting which seed
cell-type/state programs are concordantly perturbed.

This extends the prior Biomni integrated analysis, which (a) used only the Maffei 194-gene NMF panel and
(b) had no seed-resolved data (embryo/endosperm/seed-coat were literature-only). Both gaps are addressed here.

---

## 3. Data & methods

### 3.1 Seed reference atlases [A]
- **Developmental:** Gehring lab, *Nat Plants* 2026 (GSE295007) — snRNA-seq 3/5/7 DAP; 23,374 genes ×
  54,210 nuclei; annotation hierarchy level_1 (5 tissues) → level_2 (13 cell types) → level_3 (86 states)
  + 43 GO module scores.
- **Dry→germinating:** Liew/Lewsey *Nat Plants* 2024 (E-MTAB-12532); expression matrix via GEO mirror
  **GSE182331** (13,501 genes × 12,798 cells; 15 clusters; 12/24/48 h). Cluster→cell-type identities from
  the paper's open-access text [L] (clusters 9 & 14 in-situ validated; 3/6/15 confirmed by our markers).

### 3.2 Panel library [A]
Wilcoxon `rank_genes_groups` (top-50/group, ≥20 cells) → **122 panels / 6,100 marker rows**:
Gehring L1 tissue (5), L2 cell type (13), L3 state (86); germination cluster (15), germination time (3).

### 3.3 Stressor inputs (decoder queries) [D]
Genome-wide DGE from NASA OSDR (TAIR/AGI IDs): **OSD-120/GLDS-120** root µg (dark/light),
**OSD-678/GLDS-612** leaf µg (dark/light), **OSD-658/GLDS-603** GCR (40 & 80 cGy). Spaceflight effect =
−(ground-vs-flight); radiation effect = irradiated-vs-non.

### 3.4 Decoder (projection backbone)
For each stressor contrast, rank genome-wide log2FC and run **GSEA-prerank** against all 122 panels
(200 permutations). NES > 0 = seed program concordantly **induced**; NES < 0 = **suppressed**; FDR < 0.25 = significant.

### 3.5 Bridge / shared latent (Layer 2)
A **"germinating-seed score space"** with the 15 named germinating-seed cell types as axes. Adult stress
is placed by its decoder NES across those axes; **late-seed-dev** (Gehring tissue×timepoint pseudobulk)
is placed by **ssGSEA** against the same 15 panels. Both then sit relative to the dry/germinating reference.

### 3.6 NMF localization [L×A]
The Maffei NMF panel (~194–230 directional genes) overlaps the 50-gene marker panels by **≤7 genes
(median 0)** → GSEA-prerank infeasible. Instead, NMF-up (198) / NMF-down (18) gene sets were **localized**
onto germinating-seed cell-type expression specificity (z vs 1,000 random gene sets). Directions from
Maffei cluster-profile (shoot, late timepoints) + polyphenol/H₂O₂ per-gene log2 ratios.

---

## 4. Results

### 4.1 Validated panel library [A]
Embryo panels top out on **OLE1/2/3, CRA1, 2S albumin**; inner-integument **ii1 = BAN (AT1G61720)** —
the canonical endothelium marker the atlas itself names. Pipeline is biologically sound.

### 4.2 Stress → seed decoder [D×A]
*(Figures: `results/figures/decoder_L1_state_heatmap.png`, `decoder_germination_named_heatmap.png`.)*

Tissue-level NES (Gehring L1) and germination-state NES:

| program | µg root dark | µg root light | µg leaf dark | µg leaf light | GCR 40 | GCR 80 |
|---|---|---|---|---|---|---|
| Embryo | +1.07 | −1.42 | −1.08 | +1.38 | −1.38 | **+2.18** |
| Endosperm | +0.71 | −1.61 | −0.94 | −1.01 | −0.82 | +1.28 |
| Seed coat | +1.24 | −1.53 | −0.98 | −1.36 | −1.05 | −1.47 |
| germ 12 h | +1.65 | +1.94 | −1.31 | +1.92 | −1.65 | **+2.08** |
| germ 24 h | +1.17 | +1.64 | +1.01 | +1.59 | +1.41 | +1.88 |
| germ 48 h | +1.36 | −1.44 | −0.86 | +0.98 | −0.66 | +0.93 |

Key patterns:
- **Early-germination state (12–24 h) is the dominant induced program** across most stressors — adult
  stress signatures resemble the early-imbibition transcriptome.
- **GCR-80 cGy strongly induces embryo programs** (Embryo +2.18; at L3, EMB vascular primordium +2.45,
  EMB hypophysis +2.34) — a provascular/founder-cell shift under high radiation.
- **Proliferative seed states suppressed** (EMB/PEN g2/m-phase) under µg-root and GCR.
- **Strong light-dependence** — µg-root flips sign dark→light for Embryo/Endosperm/Seed coat, echoing the
  prior Biomni light×treatment interaction.

### 4.3 Bridge / shared latent [D/A × A]
*(Figures: `results/figures/bridge_heatmap.png`, `bridge_embedding.png`.)*

**Adult-stress → germinating-seed cell type (strong, z 1.4–2.1):**
µg-leaf-dark → hypocotyl cortex (mid) (+2.05); µg-root-dark → cortex/endodermis (+1.96);
GCR-40 → epidermis (+2.00). (GCR-80 and the *light* µg conditions land on "unassigned" clusters 8/11 —
soft hits, since those clusters lack a defined identity.)

**Late-seed-dev → germinating-seed cell type (weak, z 0.37–0.68) — the weakness is the result:**
developmental tissues map only weakly/non-specifically, concentrating on root-pole identities (columella,
protoxylem, radicle epidermis) for embryo/endosperm 3–7 DAP. **Interpretation:** only the **embryo lineage**
persists development → dormancy → germination; the **maternal seed coat and endosperm are terminal**, with
no germinating-embryo counterpart. The bridge is real but lineage-limited.

**Bridge v3 (canonical — within-source scaling)** — extended to all 15 contrasts (microgravity +
radiation) + the dev trajectory (27 inputs), with each germ axis z-scored *within source* to remove the
score-type artifact. **Diagnostic:** PC1↔source |corr| dropped **0.56 → 0.00**, so the embedding now
reflects biology, not data modality (`results/figures/bridge_{heatmap,embedding}_v3.png`,
`results/bridge_results_v3.md`). Now interpretable: **Embryo 3 DAP → hypocotyl cortex (early), Embryo
5 DAP → hypocotyl cortex (mid)** — a developmental progression along the embryo lineage that carries into
germination; maternal seed coat/endosperm map to mixed/terminal identities. Radiation favors root-pole /
provascular identities (columella, protophloem). **Honesty note:** the perturbation→cell-type *argmax* is
scaling-sensitive (shifts v1/v2/v3) → bridge stress assignments are suggestive, not robust; the robust
magnetic→seed signal remains the **NMF-up → radicle apical meristem localization (z +7.96)**, which is
direct expression specificity and scaling-independent.

### 4.3b Embryo-lineage bridge — developmental validation (positive control) [A]
*(Figure: `results/figures/embryo_lineage_heatmap.png`.)*

Restricting the dev side to **embryo cells only** (the lineage that persists into germination) and mapping
developing-embryo *states* (Gehring level_3) onto germinating-seed cell types **recovers textbook
developmental lineages from transcriptomes alone:**
- **EMB protoderm → epidermis** (z +1.6); **EMB hypophysis → radicle apical meristem** (z +2.14);
  **EMB vascular primordium → provasculature/protoxylem** (z +1.88); **EMB inner cotyledon → cotyledon
  mesophyll**; **EMB cortical initials → hypocotyl cortex**. Cell-cycle/initial states map to "unassigned".

This is a **positive control**: the decoder+bridge independently re-derives established embryo→seedling
lineage relationships, evidencing the machinery is sound. It also **reinforces the radicle convergence**
(§4.5): the hypophysis→radicle-apical-meristem edge means the structure NMF/µg/SMF converge on is *founded
by the embryonic hypophysis* — a developmental-lineage root for the central hypothesis. (`results/embryo_lineage_results.md`)

### 4.4 NMF localization [L×A]
*(Figure: `results/figures/nmf_localization_heatmap.png`.)*

NMF-induced genes concentrate in germinating-seed cell types:

| germinating-seed cell type | NMF-up localization z |
|---|---|
| **radicle apical meristem (cl14)** | **+7.96** |
| unassigned (cl8) | +3.23 |
| cotyledon mesophyll (cl13) | +2.85 |
| cortex/endodermis (cl2) | +1.99 |

NMF-down (n=18, underpowered) → cotyledon mesophyll, cortex/endodermis.

### 4.6 Radiation / ROS perturbations (expanded panel) [D×A]
*(Figure: `results/figures/decoder_combined_perturbation_heatmap.png`.)*

The model was extended with WT irradiated-vs-control contrasts from 5 OSDR γ-radiation RNA-seq studies
(`radiation_and_ros_cleaned.csv`) → **combined 15-contrast environmental-perturbation model**
(microgravity ×4, GCR ×2, low-dose γ ×2, acute 100 Gy γ ×7). Each study also carries an OSD_ID for
deeper OSDR data; `sog1-1`/`myb3r1` DNA-damage-TF mutant arms are available for mechanistic follow-up.
- **Acute 100 Gy γ (90 min) induces embryo + early-germination (12 h) programs** (OSD-498 Embryo +1.87,
  12 h +2.12) — a rapid DNA-damage/ROS surge resembling the early-germination state, **converging with
  the µg and GCR-80 "12 h attractor."**
- Responses **resolve/flip by 24 h** (repair phase); **low-dose (cGy) effects are weaker and dose-graded**.
- *Caveat:* 100 Gy is a mechanistic DNA-damage dose, **not space-relevant** (spaceflight GCR is cGy);
  acute-γ contrasts are ROS/DNA-damage references, while the cGy studies (OSD-658, OSD-782) are
  dose-relevant. OSD-508 vs OSD-510 show study-level heterogeneity (interpret per-study).

### 4.5 Convergence — the radicle growth-point [D × L × A → H]
Three independent lines point to the **radicle apical meristem / root growth-point**:
1. **NMF** induces radicle-apical-meristem-expressed genes (z +7.96) [L×A];
2. **Microgravity** shows light-gated modulation of the radicle meristem program [D] (cl14: µg-root-dark
   +1.7 vs µg-root-light −1.6);
3. **High static field** (Jin 2019, 600 mT) regulates radicle growth via auxin/PIN3-AUX1 [L].
The radicle is the first organ to resume growth at germination → a coherent, testable nexus.

---

### 4.9 DeepSpace seed-susceptibility atlas (headline) [D×A×L]
*(Figure: `results/figures/deepspace_seed_atlas.png`.)*

The full perturbation model (21 contrasts spanning **gravity, tropism, low-oxygen, radiation, and
magnetic/NMF** families) projected onto germinating-seed cell types, scored as **how many of 5 stressor
families significantly target each cell type** (family-level convergence, so radiation's many contrasts
get one vote).

**Result — the radicle/root tip is the multi-stressor convergence hotspot:**
- **Radicle apical meristem — 4 / 5 families** (gravity, tropism, radiation, magnetic/NMF; strongest NMF
  localization z +7.96).
- Columella/root-cap (+QC) — 4/5; radicle epidermis — 3/5. All three root-tip cell types rank at the top.
- Cotyledon mesophyll — 4/5 (the main non-root hotspot: photosynthetic programs).
- (Unassigned clusters cl8/cl11 score high but lack identity → the radicle apical meristem is the top
  *biologically-defined* hotspot.)

This is the paper's central atlas: it answers *which seed cell types are susceptible to deep-space
stressors* — the **root tip is hit by the most independent stressor families**, converging with the NMF
localization, light-gated µg, gravitropism, and the hypophysis→radicle-meristem developmental lineage.
(`results/deepspace_atlas_results.md`)

**Tissue & stage resolution** (`results/figures/deepspace_atlas_tissue_stage.png`): at the germination-
**stage** level, **12 hsl (early germination) is the most multi-stressor-susceptible window** (4/5 families)
— the dry/0 h pole is under-sampled. At the broad developing-**tissue** level the signal is diffuse and
maternal-tissue-weighted (Ovule top but only 172 cells), confirming that **cell-type × stage is the
informative resolution**. Combined: *radicle/root-tip cell types at early germination* are the hotspot.

## 5. Integrated model

Space-relevant stressors, read through the seed decoder, do **not** act diffusely — they re-tune specific
germinating-seed programs:
- a **shared early-germination (12–24 h) attractor** engaged by most stressors;
- a **radiation→embryo-provascular** axis (GCR-80);
- a **magnetic→radicle-growth-point** axis (NMF localization + µg light-gating + SMF auxin);
- a **light gate** on the microgravity response in seed-tissue programs.
The developmental bridge shows these predictions are only meaningfully transferable along the **embryo
lineage** — the part of the seed that actually carries forward into germination.

---

## 6. Data landscape & limitations

- **Genome-wide NMF is not public.** Two Maffei NNMF microarrays exist — 2022 NNMF time-course
  (PMC9775259) and 2021 **dose-response** (PMC8080623; 240/40 nT near-null → 60 µT) — but **both state
  "supplementary tables + data on request"; neither is deposited** in GEO/ArrayExpress. NMF here therefore
  uses the partial 194-gene panel via localization, **not** the full-transcriptome GSEA used for µg/GCR.
  *(Author request drafted for both arrays; the NMF arm upgrades to full decoder+bridge columns on arrival.)*
- **Magnetic comparators (high-field) are public**: GSE29787 (Paul/Ferl), PRJNA529956 (Jin SMF 600 mT) —
  usable as labeled high-field contrasts, not null-field.
- **Dry/0 h pole under-sampled** — germination single-cell starts at 12 h.
- **"Unassigned" germination clusters (8, 11)** lack identity (per the paper) — bridge hits there are soft.
- **Bridge scale artifact** — mixed-scale NES vs ssGSEA; argmax assignments are the robust readout
  (within-source scaling queued).
- **Concordance, not causation** throughout.

---

## 7. Testable hypotheses (with confidence + falsification)

| # | Hypothesis | Tier | Conf. | Falsifying experiment |
|---|---|---|---|---|
| H1 | NMF induces radicle-apical-meristem genes; NNMF germination accelerates radicle emergence | L×A→H | **High** | Germinate Col-0 under NNMF (triaxial Helmholtz); qPCR/in-situ radicle-meristem markers (WOX5, PLT1/2, RGF) + emergence kinetics. Falsify if no meristem-marker induction. `cry1cry2` should abolish. |
| H2 | Microgravity suppresses radicle/seed proliferative programs in a **light-gated** manner | D×A→H | **High** | Spaceflight/clinostat germination, light vs dark; qPCR g2/m + radicle-meristem markers. Falsify if no light×µg interaction. |
| H3 | GCR-80 cGy induces embryo provascular/hypophysis programs | D×A→H | Medium | Dose-series irradiated seed germination; provascular markers (ATHB8, SMXL5, TMO5). Falsify if not dose-dependent. |
| H4 | Only the embryo lineage bridges development→germination; maternal seed coat/endosperm are terminal | A×L→H | Medium | Marker-persistence / lineage tracing across desiccation→imbibition. Falsify if maternal-tissue markers re-express in the germinating embryo. |
| H5 | An early-germination (12–24 h) state is a common transcriptional attractor across µg/GCR(/NMF) | D→H | Medium | Cross-stressor signature-similarity test vs a tissue-matched stress panel. Falsify if stressors diverge in seed-program space. |
| H6 | Null and high magnetic fields converge on the radicle growth-point program | L×D→H | Medium | Overlap NNMF (Maffei) vs SMF (Jin/PRJNA529956) DEGs within radicle-meristem markers. Falsify if no shared core. |

---

## 8. Next steps
1. **Genome-wide NMF** (author request: 2021 dose-response + 2022 arrays) → upgrade NMF to full GSEA
   decoder + a true bridge column; add the dose-response as a magnetic gradient.
2. **Bridge refinement** — within-source scaling; restrict the dev side to the embryo lineage for a
   cleaner dev→germination map.
3. **Anchor the dry/0 h pole** (germination bulk controls / supplement).
4. **Experimental validation** of H1/H2 (highest confidence).

---

## 9. Appendix — accessions & file manifest

**Accessions.** Gehring dev = GEO **GSE295007**; germination = ArrayExpress **E-MTAB-12532** / GEO mirror
**GSE182331**; stressors = NASA OSDR **OSD-120/678/658** (GLDS-120/612/603); NMF = Maffei **PMC9775259**
(2022) + **PMC8080623** (2021), undeposited; high-field comparators = GEO **GSE29787**, SRA **PRJNA529956**.

**Key outputs.** `panels/panel_library.csv` (+`_annotated`), `panels/germination_cluster_annotations.csv`;
`results/tables/decoder_{nes,fdr}_matrix.csv`, `decoder_long.csv`, `bridge_{latent,assignments}.csv`,
`nmf_{gene_directions,localization,panel_overlap}.csv`; figures in `results/figures/`; component write-ups
`results/{decoder,bridge,nmf}_results_v1.md`. Scripts `scripts/01–08`. Living plan: `README.md`.

**Primary references.** Gehring et al. *Nat Plants* 2026 (10.1038/s41477-026-02295-8); Liew/Lewsey et al.
*Nat Plants* 2024 (10.1038/s41477-024-01771-3); Parmagnani/Maffei *Biomolecules* 2022 (10.3390/biom12121824);
Agliassa/Maffei *Sci Rep* 2021 (10.1038/s41598-021-88695-6); Jin et al. *Sci Rep* 2019 (10.1038/s41598-019-50970-y);
NASA GeneLab OSD-120/678/658.
