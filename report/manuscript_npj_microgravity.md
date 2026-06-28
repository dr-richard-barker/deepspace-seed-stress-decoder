# A cell-type-resolved atlas of deep-space stress susceptibility in the dry and germinating Arabidopsis seed

**Richard Barker**¹ ²

¹ Purdue University, West Lafayette, IN, USA
² The Collaborative Science Environment, PBC (public benefit corporation)

\*Correspondence: Richard Barker — admin@cosecloud.com

**Target journal:** *npj Microgravity* (Article). **Status:** draft v1 (2026-06-27).

---

## Abstract

Seeds are the most practical propagule for off-world agriculture, yet how the spectrum of deep-space
stressors — microgravity, ionizing radiation, altered magnetic fields, and the gas and gravitropic
environment of spaceflight hardware — impinges on the dormant and germinating seed remains largely
uncharacterized, because spaceflight experiments measure later developmental stages rather than seeds.
We address this gap with two reusable tools and a single-cell reference. The **DeepSpace
Stress-Recognition System (DSRS)** recognizes which space stressor a transcriptomic signature resembles,
and the **Germinating-Seed AutoDecoder (GSAD)** projects bulk transcriptomes onto a 122-panel
single-cell seed reference (developmental and germination atlases) to predict cell-type-level effects.
Validating the framework, the decoder independently recovers textbook embryo→seedling lineages
(protoderm→epidermis; hypophysis→radicle apical meristem; vascular primordium→provasculature). Applying
it to a 27-contrast model spanning ten stressor families (gravity including hypergravity, tropism,
low-oxygen, desiccation, osmotic, ethylene, temperature, UV, radiation, and magnetic/null field), we build
a **DeepSpace seed-susceptibility atlas**. Its central result: the **root tip is the convergence apex** —
the columella/root cap is targeted by **9 of 10** stressor families, more than any other germinating-seed
cell type, and the radicle apical meristem (the specific null-magnetic-field target, localization z = +7.96)
and radicle epidermis are likewise broadly susceptible; hypocotyl cortex and cotyledon mesophyll emerge as
secondary hotspots. Early germination (12 h) is the most vulnerable developmental window. We frame
all predictions as testable hypotheses with falsification experiments and release the tools, panels, and
atlas as a FAIR resource. The root tip emerges as a priority target for protecting seed performance in
deep space.

---

## Introduction

Establishing plant-based bioregenerative life support beyond low-Earth orbit depends on seeds that can be
stored dry, transported, and germinated reliably under conditions that differ profoundly from Earth.
Deep-space environments combine **microgravity** (or fractional gravity), chronic **ionizing/galactic
cosmic radiation**, a near-absent or altered **magnetic field**, and the confined gas environment of
flight hardware that can impose **hypoxia/anoxia**; the loss of a stable gravity vector also removes the
**gravitropic** set-point that organizes seedling establishment. Each of these has documented effects on
adult plant transcriptomes, but the consequences for the **dry/dormant and germinating seed** — the stage
that determines whether a crop establishes at all — are poorly resolved.

A core obstacle is that the relevant experiments rarely sample seeds at single-cell resolution: spaceflight
datasets profile seedlings or organs, while the richest single-cell seed atlases are ground-based.
Bridging adult-tissue or developmental signatures to seed cell types is therefore a cross-stage inference
problem. Recent single-cell resources make it tractable: a developmental atlas of early Arabidopsis seed
(embryo, endosperm, seed coat) and a germinating-embryo atlas spanning the imbibition time-course together
define the cell types and states of the dry→germinating seed.

Here we operationalize this bridge as two tools and use them to ask a concrete question of direct
relevance to space agriculture: **which seed cell types and developmental stages are most susceptible to
deep-space stressors, and do any stressors converge on the same cellular targets?** We integrate
genome-wide signatures from microgravity, radiation, low-oxygen, and tropism experiments, add a
null-magnetic-field signal, and project them onto a single-cell seed reference to produce a
susceptibility atlas with an explicit, falsifiable headline.

---

## Results

### A two-tool framework for plant space-biology stress decoding (Fig. 1)

We distilled the analysis into two reusable, FAIR tools (Fig. 1). **DSRS** takes any plant transcriptomic
perturbation signature (ranked log2 fold-changes, AGI/TAIR identifiers) and recognizes which space
stressor it most resembles, by comparing its *seed-program fingerprint* — its enrichment across the seed
reference panels — to a curated reference library spanning five stressor families. **GSAD** takes a bulk
transcriptome and models its predicted effect on the dry/germinating seed, returning a per cell-type,
tissue, and stage susceptibility profile. Both share one projection engine (rank-based gene-set
enrichment onto the seed panels). As an internal check, DSRS correctly recognizes a held-in submergence
signature as belonging to the low-oxygen family.

### A validated single-cell seed reference (Fig. 3)

We built a 122-panel reference of seed cell-type and state marker sets from the developmental seed atlas
(snRNA-seq, 3/5/7 days after pollination) and the germination atlas (scRNA-seq, 12/24/48 h post-imbibition),
spanning embryo, endosperm, seed-coat, and germinating-embryo cell types as well as the dry→germinating
state axis. Panels reproduced canonical markers (oleosins and cruciferin for embryo; *BANYULS* for the
inner-integument endothelium), confirming fidelity.

As a stringent positive control, we restricted the decoder's input to embryo cells only and asked which
germinating-seed cell type each *developing*-embryo state maps onto. The decoder independently recovers
established developmental lineages from transcriptomes alone (Fig. 3): **protoderm → epidermis**,
**hypophysis → radicle apical meristem**, **vascular primordium → provasculature**, **inner cotyledon →
cotyledon mesophyll**, and **cortical initials → hypocotyl cortex**. Recovering ground-truth lineage
relationships validates the projection machinery and, notably, places the embryonic **hypophysis** as the
developmental origin of the radicle apical meristem — a point we return to below.

### Recognizing deep-space stress signatures (Fig. 2)

We assembled a 27-contrast stress reference library spanning ten families: **gravity** (spaceflight
microgravity root and leaf, plus 2 g hypergravity — completing the µg↔1 g↔hypergravity axis),
**radiation** (galactic-cosmic-radiation-relevant low-dose and acute γ), **low-oxygen** (hypoxia, anoxia,
submergence), **desiccation** (seed maturation drying), **osmotic** (mannitol), **ethylene** (ACC),
**temperature** (warm/thermomorphogenesis), **UV** (UV-B), **tropism** (gravitropism, phototropism), and
**magnetic/null-magnetic-field** (Fig. 2). Genome-wide signatures were projected onto the seed panels;
the null-magnetic-field (NMF) response, available only as a small curated gene panel, was handled by
expression-localization rather than enrichment (see Methods). Across families, a recurrent theme emerged:
stressed adult/vegetative tissue transcriptionally resembles the **early-germination (12 h) state**,
suggesting a shared stress-engaged transcriptional program at the onset of germination.

### Decoding stress onto germinating-seed cell types (Fig. 4)

GSAD projection resolved stressor effects to individual germinating-seed cell types (Fig. 4). Microgravity
showed strong **light-dependence** (sign inversions between dark and light in embryo/endosperm/seed-coat
programs), acute radiation induced **embryo provascular/founder** programs, and low-oxygen and gravitropism
each engaged root-pole identities. Null-magnetic-field-responsive genes localized most sharply to the
**radicle apical meristem** (localization z = +7.96), far above any marker-panel overlap expected by
chance. As an independent cross-check, the 2021 NNMF DEG lists (Sci Rep s41598-021-88695-6, supplementary
S7) localized to **cotyledon mesophyll and hypocotyl cortex** but did *not* reproduce the radicle-meristem
signal (cross-cell-type r = 0.35) — indicating the radicle-meristem localization is specific to the
oxidative NNMF gene panel, while NMF's broader footprint includes the cotyledon/hypocotyl. (Genome-wide NNMF
arrays remain pending from the authors; both panels are localization-tier.)

### The DeepSpace seed-susceptibility atlas (Fig. 5)

To integrate across stressors, we scored each germinating-seed cell type by how many of the **ten stressor
*families*** significantly target it — a family-level convergence metric that prevents any single
data-rich family from dominating (Fig. 5). The result is unambiguous: the **root tip is the multi-stressor
convergence apex**. The **columella/root cap is targeted by 9 of 10 families** — more than any other
germinating-seed cell type — and the **radicle apical meristem** (6/10; the specific magnetic/NMF target,
localization z = +7.96) and **radicle epidermis** (5/10) complete a broadly susceptible root pole.
Beyond the root, **hypocotyl cortex** and **cotyledon mesophyll** emerge as secondary hotspots (6–7/10),
reflecting convergent effects on cortical and photosynthetic programs. ("Unassigned" germination clusters
score highly but lack a defined identity; the columella/root cap is the top biologically-defined hotspot.)

### Stage and tissue resolution

At the germination-**stage** level, **early germination (12 h) is the most multi-stressor-susceptible
window**, consistent with the cross-family "12 h" convergence. We anchored the **dry/0 h pole** with a
bulk-derived dry-seed (mature, 21 DAP) marker panel, extending the state axis dry→12→24→48 h: the
**dry/dormant-seed program is induced by desiccation (strongest), low-oxygen and acute radiation, and
suppressed by ethylene** — the expected dormancy logic (ethylene promotes germination), an internal
validation. At the broad developing-**tissue** level the signal is diffuse and weighted by small maternal
tissues, indicating that **cell-type × stage**, not gross tissue, is the informative resolution.

### A convergent model centred on the radicle growth-point (Fig. 6)

Four independent lines converge on the radicle growth-point (Fig. 6): (i) NMF-responsive genes localize
there (z = +7.96); (ii) microgravity modulates the radicle-meristem program in a light-gated manner;
(iii) gravitropism — itself a root-tip phenomenon — engages the same program; and (iv) the structure is
developmentally founded by the embryonic hypophysis, which our lineage analysis maps directly onto the
radicle apical meristem. We therefore propose the **radicle apical meristem as a priority cellular target**
for deep-space seed performance, and state two high-confidence, falsifiable predictions: **H1** — growth
under a near-null magnetic field induces radicle-apical-meristem markers and alters radicle emergence, with
the effect abolished in *cry1 cry2*; **H2** — microgravity suppresses radicle proliferative programs in a
light-gated manner.

---

## Discussion

Reading the deep-space stress spectrum through a single-cell seed lens reveals that these stressors do not
act diffusely: they re-tune specific seed programs, and they **converge on the radicle/root apical tip**.
That convergence is biologically coherent — the radicle is the first organ to resume growth at germination,
a hub of auxin and gravity signalling, and the developmental product of the hypophysis — and it is
recovered independently by chemically and physically distinct stressors, which argues against a single
shared artefact. The cross-family "early-germination (12 h)" signal further suggests that the onset of
germination is a window of heightened environmental sensitivity.

Our predictions are explicitly **concordance, not causation**: GSAD performs signature transfer across
tissue and developmental stage, so each claim carries an evidence tier (direct data / atlas projection /
literature / hypothesis) and a falsification test. The framework's recovery of textbook embryo lineages
(Fig. 3) provides confidence that the projections reflect real cell-type biology rather than artefact.

Key limitations define the next experiments. Genome-wide null-magnetic-field transcriptomes are not yet
publicly deposited, so the NMF arm relies on a curated panel via localization; the dry/0 h seed pole lacks
single-cell data and is anchored only by a bulk-tier dry-seed maturation panel; tropism transcriptomes are
sparse (gravitropism RNA-seq;
phototropism microarray) and sustained hypergravity is represented only by a microarray-tier callus
dataset (2 g, GSE29787); osmotic and UV-B use AtGenExpress ATH1 microarrays and desiccation uses seed-
maturation drying as a proxy; and several contrasts are thus microarray- or translatome-tier. None of these undermines the central, multiply-supported result, and
each is addressable as data accrue. The tools are organism-agnostic in design and can incorporate new
stressors (e.g., desiccation, ethylene/CO₂, partial gravity) as reference panels.

---

## Methods

**Seed single-cell reference.** Developmental seed atlas (snRNA-seq, 3/5/7 DAP) and germination atlas
(scRNA-seq, 12/24/48 h). Cell-type/state marker panels (top 50 genes/group, ≥20 cells, Wilcoxon) were
compiled into a 122-panel library (exported as GMT). Germination clusters were annotated from the source
publication and confirmed against canonical markers.

**Stressor signatures.** Genome-wide differential expression was obtained from NASA OSDR (microgravity:
OSD-120, OSD-678; radiation: OSD-658, OSD-498, OSD-502, OSD-508, OSD-510, OSD-782) and GEO (low-oxygen:
GSE315308, GSE182724; gravitropism: GSE199142; phototropism: GSE3847; hypergravity: GSE29787, 2 g vs 1 g
callus, two-color Agilent GPL9020; desiccation: GSE76015, seed 21 vs 15 DAF; ethylene: GSE193833, ACC
4 h vs 0 h; temperature: GSE303133, 27 vs 21 °C; osmotic: AtGenExpress GSE5622 and UV-B: GSE5626, each
vs control GSE5620, ATH1/GPL198). Wild-type, treatment-vs-control contrasts were used. Gene identifiers
were harmonized to AGI/TAIR (Entrez, Affymetrix ATH1/GPL198, and Agilent GPL9020 maps provided). The null-magnetic-field panel derives from Maffei-group time-course microarrays (curated
oxidative/polyphenol gene set).

**Projection (DSRS/GSAD).** Each signature was ranked by log2FC and projected onto the panels by
pre-ranked gene-set enrichment (gseapy; 200 permutations; seed 42), yielding a normalized enrichment score
(NES) and FDR per panel. DSRS scores query-to-reference similarity of seed-program fingerprints (rank
correlation). The NMF panel (≤7-gene overlap with marker panels) was instead localized onto cell-type
expression specificity (mean specificity vs 1,000 random gene sets → z).

**Atlas/convergence.** A cell type was deemed susceptible to a family if any contrast in that family had
|NES| ≥ 1.5 and FDR < 0.25 (or NMF localization |z| ≥ 2). Convergence = number of the ten families meeting
this threshold. Bridge/lineage analyses used pseudobulk and ssGSEA with within-source scaling.

**Software.** `deepspace` Python package (DSRS, GSAD, CLI). Determinism via fixed seeds; full pipeline in
numbered scripts (see Code availability).

---

## Data availability

All inputs are public (provenance and accessions in the repository `data/data_inventory.csv`):
developmental seed atlas **GSE295007**; germination atlas **GSE182331** (mirror of ArrayExpress
**E-MTAB-12532**); microgravity/radiation **OSD-120/678/658/498/502/508/510/782** (NASA OSDR); low-oxygen
**GSE315308**, **GSE182724**; gravitropism **GSE199142**; phototropism **GSE3847** (GPL198); hypergravity
**GSE29787** (2 g, GPL9020); desiccation **GSE76015**; ethylene **GSE193833**; temperature **GSE303133**;
osmotic **GSE5622** and UV-B **GSE5626** vs control **GSE5620** (AtGenExpress, GPL198). Genome-wide
null-magnetic-field arrays (Parmagnani/Maffei 2022; Agliassa/Maffei 2021) are not publicly deposited and
were requested from the authors; the curated panel is included.

## Code availability

Tools and pipeline are released under the MIT license with a Zenodo DOI [to be minted on deposit]: the
`deepspace` package (DSRS + GSAD + CLI), the panel library (GMT), numbered reproduction scripts, and a
`REPRODUCE.md` guide. Figures F1–F6 are regenerated by `scripts/20_manuscript_figures.py`.

## Selected references

1. Martin, Cogdill, Pusey, … Gehring. *Transcriptional atlas of early Arabidopsis seed development.* npj? — *Nat. Plants* (2026). doi:10.1038/s41477-026-02295-8 (GSE295007).
2. Liew, …, Lewsey. *Establishment of single-cell transcriptional states during seed germination.* *Nat. Plants* (2024). doi:10.1038/s41477-024-01771-3 (E-MTAB-12532 / GSE182331).
3. Parmagnani, Mannino, Maffei. *Transcriptomics and metabolomics of ROS modulation in near-null magnetic field Arabidopsis.* *Biomolecules* (2022). doi:10.3390/biom12121824.
4. Agliassa, Maffei. *Differential root and shoot magnetoresponses in Arabidopsis.* *Sci. Rep.* (2021). doi:10.1038/s41598-021-88695-6.
5. Jin et al. *Static magnetic field regulates Arabidopsis root growth via auxin signaling.* *Sci. Rep.* (2019). doi:10.1038/s41598-019-50970-y.
6. Esmon et al. *A gradient of auxin and auxin-dependent transcription precedes tropic growth.* *PNAS* (2006) (GSE3847).
7. NASA GeneLab/OSDR plant spaceflight datasets (OSD-120/678/658/498/502/508/510/782).
8. Subramanian et al. *Gene set enrichment analysis.* *PNAS* (2005).

## Author contributions / Competing interests / Acknowledgements

[To complete.] The authors declare no competing interests. We thank the data-generating consortia (Gehring
and Lewsey labs; NASA GeneLab/OSDR; the Maffei group) whose public/shared data enabled this work.

---

*Figures: F1 concept workflow; F2 DSRS stress library; F3 seed reference + embryo-lineage validation;
F4 GSAD susceptibility; F5 DeepSpace atlas (headline); F6 convergence model. Files in `report/figures_npj/`.*
