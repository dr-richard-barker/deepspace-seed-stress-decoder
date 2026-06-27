# Decoder v1 — first end-to-end result (2026-06-26)

**Method.** Genome-wide stressor signatures (NASA OSDR DGE, TAIR/AGI gene IDs) ranked by log2FC and
projected onto the 122 seed cell-type/state panels via GSEA-prerank (200 permutations).
NES > 0 = seed program concordantly **induced** by the stressor; NES < 0 = **suppressed**. `*` = FDR < 0.25.

**Inputs (genome-wide, ~24k genes each):**
- µg root — OSD-120/GLDS-120, Col-0 spaceflight-vs-ground, dark & light
- µg leaf — OSD-678/GLDS-612, Col-0 WT spaceflight-vs-ground, dark & light
- GCR    — OSD-658/GLDS-603, mixed radiation 40 & 80 cGy vs non-irradiated

**Outputs:** `results/tables/decoder_{nes,fdr}_matrix.csv`, `decoder_long.csv`;
`results/figures/decoder_L1_state_heatmap.{png,svg}`, `decoder_L2_celltype_heatmap.{png,svg}`.

## Headline patterns (tissue + germination-state level)
- **Early-germination state (12 hsl) is the most consistently INDUCED program** under µg (root dark/light,
  leaf light) and GCR-80 — i.e. stressed *adult/vegetative* tissue transcriptomes resemble the
  **early-imbibition germinating-seed state**. (GCR-40 diverges: suppresses 12 hsl.)
- **Cell-cycle / proliferative seed states are SUPPRESSED** under µg-root and GCR (EMB g2/m-phase,
  PEN g2/m-phase) — coherent with stress dampening seed-tissue proliferation.
- **GCR-80 cGy strongly INDUCES embryo programs** (Embryo L1 NES +2.2*; EMB vascular primordium +2.45*,
  EMB hypophysis +2.34*) — a provascular/founder-cell-like shift under high radiation.
- **Seed coat programs SUPPRESSED** under µg-light and GCR-80.
- **Strong light-dependence**: µg-root flips sign dark→light for Embryo/Endosperm/Seed coat — echoes the
  light×treatment interaction in the prior Biomni analysis.
- Cross-consistency with Biomni repo's "vascular most consistently perturbed" theme (EMB vascular primordium).

## Caveats (carry the tier discipline)
1. **Concordance, not causation** — projection/label-transfer across tissue & developmental stage.
2. **NMF not yet decoded** — the project's headline perturbation. Maffei 194-gene panel is too small to
   project (0–4 gene overlap, as the repo documented). Awaiting genome-wide NMF (author request) to add
   the null-field column. Decoder v1 demonstrates the method on the genome-wide µg/GCR signals.
3. ~~Germination clusters unlabeled~~ **RESOLVED** — labeled from paper text (see
   `panels/germination_cluster_annotations.csv`); named decoder figure
   `results/figures/decoder_germination_named_heatmap.{png,svg}`. Clusters 8 & 11 remain "unassigned"
   per the paper (no clear marker enrichment).
4. **Maternal/residual tissues** (Ovule, Funiculus) — interpret embryo/endosperm/seed-coat primarily;
   Ovule signal may be residual maternal carry-over.
5. **Dry/0h pole under-sampled** — germination single-cell starts at 12 hsl.
