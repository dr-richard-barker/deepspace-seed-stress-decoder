---
layout: cose
title: DeepSpace Seed-Stress Decoder
---

_Which seed cell types and developmental stages are susceptible to deep-space stressors?_

Two reusable, FAIR computational tools (**DSRS** + **GSAD**), an integrated **MASTA** projection engine, and a single-cell **seed-susceptibility atlas** for plant space biology, built on _Arabidopsis thaliana_. Give the decoder a bulk transcriptomic signature; it recognises which space stressor the signature resembles and predicts its effect on the dry and germinating seed, cell type by cell type. Companion to a manuscript targeted at _npj Microgravity_.

[View Repository on GitHub](https://github.com/dr-richard-barker/deepspace-seed-stress-decoder){: .btn}
[Read npj Microgravity Manuscript (PDF)](https://github.com/dr-richard-barker/deepspace-seed-stress-decoder/blob/main/report/manuscript_npj_microgravity.pdf){: .btn}
[Stimuli Decoders Synthesis]({{ '/stimuli_decoders_synthesis' | relative_url }}){: .btn}

| 49 contrasts | 15 stressor families | 123 seed panels | 14 / 15 families hit the root cap |
|:---:|:---:|:---:|:---:|

![Concept workflow: a query transcriptomic signature feeds two tools — DSRS (which space stressor?) and GSAD (effect on the seed?) — whose outputs assemble into the DeepSpace seed-susceptibility atlas, with the headline that the radicle/root tip is a multi-stressor hotspot.]({{ '/assets/figures/F1_concept_workflow.png' | relative_url }})

*Figure 1 — Concept workflow. A query transcriptomic signature drives the dual-engine architecture: DSRS identifies which space stressor or environmental perturbation the query resembles across 49 contrasts and 15 families, while GSAD projects the query across 123 single-cell seed panels to resolve cell-type-, tissue-, and stage-specific susceptibility.*

---

## The Question

Deep-space exploration environments subject plants to an unprecedented combination of biophysical stressors: **microgravity**, chronic **galactic cosmic radiation (GCR)**, an altered or **near-null magnetic field (NMF)**, confined **exploration atmospheres** ($50\text{--}56.5\text{ kPa}$ hypobaria), and systemic **reactive oxygen species (ROS)** accumulation. Furthermore, the absence of a gravity vector disrupts the **gravitropic** set-point required for directional organ growth.

While adult plant responses to spaceflight are well cataloged, the vulnerability of the **dormant and germinating seed**—the developmental checkpoint that dictates whether an extraterrestrial crop establishes at all—remains critically understudied because flight missions routinely launch vegetative seedlings or adult plants. This project resolves that gap by establishing a cross-stage signature projection framework that maps bulk environmental perturbations onto a high-resolution single-cell seed reference.

---

## The Integrated Stimuli Decoders Ecosystem

In version **v0.2.0**, the decoder expands from a 27-contrast, 10-family model to a comprehensive **49-contrast, 15-family framework**, uniting three specialized laboratory computational assets:

1. **`arabidopsis_exploration_atmosphere` (TabPFN v2)**: Decouples barometric pressure ($P_{\text{total}}$) from oxygen partial pressure ($pO_2$) across 130 microarrays using prior-data fitted networks, isolating pure hypobaria and NASA Exploration Atmosphere conditions ($50\text{ kPa}$ Norm$O_2$ and Hypo$O_2$).
2. **`Redox_decoder` (32D CVAE)**: Disentangles reactive oxygen species (ROS) transcriptional states from developmental variation across 232 studies (4,332 samples), supplying genome-wide spaceflight ROS latent shift signatures validated across 38 NASA OSDR missions.
3. **`MASTA` (Max Planck MicroArray overlap Search Tool and Analysis)**: A systematic compendium of 592 microarray perturbation contrasts, contributing empirical ground-truth signatures for cold shock, mechanical wounding, drought, phytohormones (auxin, GA, cytokinin, brassinosteroid), and nutrient starvation.

For a full comparative breakdown of the models, see the [Stimuli Decoders Synthesis]({{ '/stimuli_decoders_synthesis' | relative_url }}).

---

## The Software Suite

The software suite provides command-line tools and a Python API to interrogate any transcriptomic signature.

| Tool / Command | Function | Core Question |
|---|---|---|
| **DSRS** (`deepspace dsrs`) | DeepSpace Stress-Recognition System: ranks query similarity against the 49-contrast reference library across 15 families. | _"Which space stressor or environmental perturbation does this signature resemble?"_ |
| **GSAD** (`deepspace gsad`) | Germinating-Seed AutoDecoder: projects query log<sub>2</sub>FC onto 123 single-cell seed panels to predict cell-type and stage vulnerability. | _"What does this perturbation do to the dormant and germinating seed?"_ |
| **MASTA Project** (`deepspace masta-project`) | Directly extract and project any of the 592 MASTA benchmark contrasts onto the seed atlas. | _"How does an empirical ground-truth stressor affect the seed?"_ |
| **MASTA List** (`deepspace masta-list`) | Search and browse the 592 MASTA microarray contrast identifiers. | _"What empirical contrasts are available in the compendium?"_ |

### Quickstart

Input is a two-column CSV containing gene identifiers (AGI / TAIR, e.g. `AT1G01010`) and log<sub>2</sub> fold-change values.

```bash
# Install the package in editable mode
git clone https://github.com/dr-richard-barker/deepspace-seed-stress-decoder.git
cd deepspace-seed-stress-decoder/tools && pip install -e .

# Which space stressor does my signature resemble?
deepspace dsrs my_signature.csv --out matches.csv

# Predict cell-type and stage susceptibility across the seed
deepspace gsad my_signature.csv --out seed_susceptibility.csv

# List available MASTA empirical contrasts
deepspace masta-list --filter "cold"

# Project a MASTA empirical contrast directly onto the seed atlas
deepspace masta-project "S851&cold_wt-wt_3h" --out cold_3h_seed.csv
```

```python
# Programmatic usage in Python
import deepspace

# 1. Stress recognition across 15 families
matches, fam_summary = deepspace.dsrs.recognize("my_signature.csv")
print(fam_summary.head())

# 2. Seed cell-type susceptibility decoding
seed_results = deepspace.gsad.decode("my_signature.csv")
print(seed_results["celltype"].head(10))

# 3. Project a MASTA contrast directly
from deepspace.masta import load_masta_contrast
masta_sig = load_masta_contrast("S851&cold_wt-wt_3h")
masta_seed = deepspace.gsad.decode(masta_sig)
```

> **Epistemic Notice**: Decoder outputs reflect **predicted concordance** via cross-stage signature transfer, not proven direct causation. Every claim is assigned an explicit evidence tier (Tier 1: Direct Seed Data; Tier 2: Reference Projection; Tier 3: Cross-Stressor Transfer; Tier 4: Theoretical / Biophysical) and accompanied by a falsification test.

---

## Validated Single-Cell Seed Reference

The baseline reference comprises a **123-panel library**:
- **122 single-cell marker panels** derived from the developmental seed atlas (**GSE295007**, snRNA-seq, 3, 5, and 7 days after pollination) and the germination atlas (**GSE182331**, scRNA-seq, 12, 24, and 48 hours post-imbibition).
- **1 bulk dry-seed anchor** capturing the mature quiescent transcriptome.

Panels faithfully reflect canonical developmental regulators (e.g., oleosins and cruciferins in the embryo, _BANYULS_ in the seed coat endothelium).

As an unbiased positive control, the projection engine was restricted strictly to embryonic transcriptomes to test whether it could reconstruct developmental trajectories without prior lineage knowledge. It autonomously recovers ground-truth developmental lineages:
- **Protoderm $\rightarrow$ Epidermis**
- **Hypophysis $\rightarrow$ Radicle Apical Meristem** (establishing the embryonic origin of the primary root growth point)
- **Vascular Primordium $\rightarrow$ Provasculature**
- **Inner Cotyledon $\rightarrow$ Cotyledon Mesophyll**, and **Cortical Initials $\rightarrow$ Hypocotyl Cortex**

![Seed reference and embryo-lineage validation heatmaps, showing developing-embryo states mapping onto the expected germinating-seed cell types.]({{ '/assets/figures/F3_seed_reference_embryo_lineage.png' | relative_url }})

*Figure 3 — Validated single-cell seed reference. Ground-truth recovery of established embryonic lineages confirms that the projection engine captures authentic biological programs rather than statistical artifacts.*

---

## The 49-Contrast Deep-Space Stress Library

The expanded library spans **15 stressor families** assembled from NASA OSDR, GEO, AtGenExpress, and specialized decoders. A major recurrent finding is that stressed adult tissues transcriptionally mimic the **early germination (12 h) state**, revealing a conserved stress-reactivation program shared between seed germination and vegetative adaptation.

| Stressor Family | Contrasts ($N$) | Representative Conditions | Key Sources |
|---|:---:|---|---|
| **Gravity** | 5 | Spaceflight microgravity (root & leaf, light & dark) + 2 g hypergravity | NASA OSD-120, OSD-678; GSE29787 |
| **Radiation** | 9 | GCR-relevant low-dose (40, 80 cGy), acute $\gamma$ time-course (100 Gy Co-60), low-dose Cs-137 (10, 100 cGy) | NASA OSD-658, OSD-498/502/508/510, OSD-782 |
| **Exploration Atmosphere** | 6 | Pure hypobaria, pure hypoxia, NASA exploration atmosphere ($50\text{ kPa}$ Norm$O_2$, $50\text{ kPa}$ Hypo$O_2$) | TabPFN v2 framework; 130 microarrays |
| **Redox / ROS** | 2 | Continuous CVAE spaceflight ROS latent shift ($\log_2 \text{err\_ratio}$), $H_2O_2$ oxidative stress | Redox_decoder (232 studies, 38 missions); MASTA |
| **Cold** | 2 | Cold shock time-course ($4^\circ\text{C}$ at 3 h and 24 h) | MASTA / AtGenExpress |
| **Wounding** | 1 | Mechanical leaf/tissue damage (1.5 h) | MASTA / AtGenExpress |
| **Auxin** | 1 | Indole-3-acetic acid (IAA, $1\,\mu\text{M}$ for 3 h) | MASTA / AtGenExpress |
| **Gibberellin** | 1 | $\text{GA}_3$ stimulation (1 h) | MASTA / AtGenExpress |
| **Cytokinin** | 1 | Zeatin stimulation (1 h) | MASTA / AtGenExpress |
| **Brassinosteroid** | 1 | Brassinolide (BL, $10\,\text{nM}$ for 3 h) | MASTA / AtGenExpress |
| **Nutrient Stress** | 2 | Nitrogen starvation, Phosphorus starvation | MASTA / AtGenExpress |
| **Tropism** | 4 | Gravitropic reorientation time-course, phototropism auxin gradient | GSE199142, GSE3847 |
| **Low-Oxygen** | 8 | Hypoxia, anoxia, complete submergence | GSE315308, GSE182724 |
| **Desiccation** | 2 | Seed maturation drying (21 vs 15 DAF) | GSE76015 |
| **Osmotic / Salt** | 2 | Mannitol osmotic stress, drought stress | GSE5622, MASTA |
| **Ethylene** | 1 | ACC precursor (4 h vs 0 h) | GSE193833 |
| **UV** | 1 | UV-B irradiation vs control | GSE5626 |
| **Magnetic / Null Field** | 1 | Near-null magnetic field ($<30\text{ nT}$ NMF) curated panel | Parmagnani/Maffei 2022; Agliassa/Maffei 2021 |

![DSRS stress-recognition library: enrichment fingerprints of the stressor contrasts across the seed panels.]({{ '/assets/figures/F2_stress_library.png' | relative_url }})

*Figure 2 — DSRS stress library fingerprints. Distinct enrichment signatures across the 123 seed panels provide the diagnostic basis for recognizing query stressor classes and families.*

![GSAD susceptibility matrix across germinating seed cell types.]({{ '/assets/figures/F4_gsad_susceptibility.png' | relative_url }})

*Figure 4 — GSAD susceptibility matrix. Unbiased cell-type susceptibility profiles across the 15 single-cell clusters for 49 deep-space and environmental perturbations.*

---

## Headline Result: The Radicle Apex is the Multi-Stressor Vulnerability Hotspot

To quantify cellular vulnerability without bias toward data-dense categories, each germinating-seed cell type was evaluated by family-level convergence: **how many of the 15 distinct stressor families significantly alter its transcriptional program ($|\text{NES}| \ge 1.5$, $\text{FDR} < 0.05$)**.

- **Columella / Root Cap (+QC) (cl4) — 14 of 15 Families (93.3% Convergence)**:
  Exhibits significant susceptibility across almost every environmental challenge, confirming that the root cap and quiescent center represent the primary sensory and protective boundary layer of the germinating seed.
- **Radicle Apical Meristem (cl14) — 10 of 15 Families (66.7% Convergence)**:
  Directly targeted by near-null magnetic field (expression localization $z = +7.96$, $P = 8.7 \times 10^{-16}$), microgravity, and decoupled hypobaria ($\text{NES} = +1.98$).
- **Radicle Epidermis (cl10) — 8 of 15 Families**:
  Forms an integrated, highly vulnerable root pole alongside the cap and meristem.
- **Cotyledon Mesophyll (cl13) — 13 of 15 Families** & **Hypocotyl Cortex (cl5, cl7, cl1) — 10–11 of 15 Families**:
  Represent secondary systemic metabolic hotspots, driven by radiation, oxidative stress, and nutrient deprivation.

![DeepSpace seed-susceptibility atlas heatmap: germinating-seed cell types against 15 stressor families, coloured by signed strength with significance stars, plus a convergence bar chart.]({{ '/assets/figures/F5_deepspace_atlas.png' | relative_url }})

*Figure 5 — The DeepSpace Seed-Susceptibility Atlas v8. Rows display the 15 germinating-seed cell types; columns display the 15 stressor families. Color indicates signed enrichment strength (NES / NMF z) with significance denoted by asterisks. The convergence bar chart (right) highlights the columella/root cap (14/15) and radicle apical meristem (10/15) as the convergence apex of spaceflight stress.*

---

## A Convergent Mechanistic Model & Falsification Tests

Integrating developmental lineage tracing, spaceflight multi-omics, atmospheric foundation modeling, and ROS latent representations reveals that deep-space stressors converge physically and molecularly on the **radicle growth point**:

1. **Near-Null Magnetic Field (NMF)**: Selectively triggers radicle apical meristem transcriptional programs ($z = +7.96$).
2. **Microgravity ($\mu g$)**: Represses radicle meristem proliferation programs in a light-gated manner.
3. **Decoupled Hypobaria**: Barosensory signaling directly engages radicle cap and meristem programs independently of oxygen tension.
4. **Redox / ROS Latent Remodeling**: Flight-induced oxidative cascades concentrate strongly in metabolically active root tip zones.
5. **Gravitropic & Hormonal Sensing**: Root cap columella cells host the statolith-driven gravitropic apparatus, which is constitutively perturbed in microgravity.

![Convergence model diagram: null magnetic field, microgravity, radiation/GCR, gravitropism, and the developmental origin all converge on the radicle growth point, with falsification tests H1 and H2.]({{ '/assets/figures/F6_convergence_model.png' | relative_url }})

*Figure 6 — Mechanistic convergence model and falsification tests. The radicle growth point (apical meristem and columella/root cap) serves as the priority cellular target for space agricultural engineering. Two high-priority falsifiable hypotheses are formulated:*
- ***Hypothesis 1 (H1 — NMF Cryptochrome Dependency)***: Near-null magnetic field ($<30\text{ nT}$) activates radicle meristem programs and delays germination via cryptochrome flavin redox intermediates; this transcriptional shift will be abolished in *cry1 cry2* double mutants.
- ***Hypothesis 2 (H2 — Light-Gated Microgravity Repression)***: Spaceflight microgravity represses radicle meristem proliferation in dark-imbibed seeds, but ambient red/far-red light signaling rescues meristematic activation via phytochrome-mediated systemic signaling.

---

## Reproducibility & Pipeline Architecture

All input datasets are open-access, and the computational pipeline is fully automated and deterministic:

1. **Environment**: Python $\ge 3.10$, R $\ge 4.4$ (SeuratObject for initial developmental snRNA-seq export), `pip install -e tools/`.
2. **Pipeline Execution**: Execute numbered scripts in sequence:
   - `scripts/01–19`: Seed reference assembly, single-cell marker extraction, embryo lineage positive controls, and initial stress projections.
   - `scripts/31–33`: Ingestion of decoupled atmosphere (TabPFN v2), spaceflight ROS latent shift (CVAE), and MASTA compendium contrasts.
   - `scripts/34–35`: Master v8 projection matrix assembly and atlas convergence calculation.
   - `scripts/20–22`: Generation of publication-grade figures (300 dpi PNG + SVG) and compilation of the *npj Microgravity* manuscript suite (PDF and DOCX).
3. **Determinism**: Random seeds are hardcoded (seed 42, 200 permutations in GSEA-prerank); gene identifiers are harmonized to TAIR/AGI locus tags.

See [REPRODUCE.md](https://github.com/dr-richard-barker/deepspace-seed-stress-decoder/blob/main/REPRODUCE.md) for step-by-step reproduction instructions and [PLANNING.md](https://github.com/dr-richard-barker/deepspace-seed-stress-decoder/blob/main/PLANNING.md) for the active development log.

---

## Data & Accession Provenance

All input accessions are cataloged in [`data/data_inventory.csv`](https://github.com/dr-richard-barker/deepspace-seed-stress-decoder/blob/main/data/data_inventory.csv).

| Stressor / Reference Role | Dataset Description | Accession / Resource | Platform / Repository |
|---|---|---|---|
| **Seed Reference (snRNA-seq)** | Developing seed atlas (3, 5, 7 DAP) | **GSE295007** | GEO · 10x Genomics |
| **Seed Reference (scRNA-seq)** | Germination atlas (12, 24, 48 h) | **GSE182331** / E-MTAB-12532 | GEO / ArrayExpress · 10x Genomics |
| **Gravity ($\mu g$)** | Spaceflight root & leaf (dark & light) | **OSD-120**, **OSD-678** | NASA OSDR · Illumina RNA-seq |
| **Gravity ($2\,g$)** | Hypergravity 2 g vs 1 g callus | **GSE29787** | GEO · Agilent GPL9020 |
| **Radiation (GCR)** | Whole seedling 40 & 80 cGy high-energy ions | **OSD-658** | NASA OSDR · RNA-seq |
| **Radiation (Acute $\gamma$)** | 100 Gy Co-60 gamma ray time-course | **OSD-498**, **OSD-502**, **OSD-508**, **OSD-510** | NASA OSDR · RNA-seq |
| **Radiation (Low-dose)** | 10 & 100 cGy Cs-137 irradiation | **OSD-782** | NASA OSDR · RNA-seq |
| **Atmosphere (Decoupled)** | TabPFN v2 pure hypobaria vs hypoxia (130 arrays) | `arabidopsis_exploration_atmosphere` | Model framework · GEO compendium |
| **Atmosphere (NASA Setpoints)** | $50\text{ kPa}$ Norm$O_2$ and Hypo$O_2$ profiles | `arabidopsis_exploration_atmosphere` | Model framework · Affymetrix ATH1 |
| **Redox / ROS (Latent Space)** | 32D CVAE spaceflight ROS latent shift | `Redox_decoder` | 232 studies, 38 NASA OSDR missions |
| **Empirical Multi-Stressor** | Cold, wounding, hormones, nutrient starvation | `MASTA` compendium | Max Planck Institute · 592 ATH1 contrasts |
| **Low-Oxygen** | Hypoxia, anoxia, submergence | **GSE315308**, **GSE182724** | GEO · RNA-seq |
| **Tropism** | Root gravitropism time-course, phototropism | **GSE199142**, **GSE3847** | GEO · RNA-seq / ATH1 GPL198 |
| **Desiccation** | Seed maturation drying (21 vs 15 DAF) | **GSE76015** | GEO · RNA-seq |
| **Osmotic / Salt** | Mannitol osmotic stress, drought | **GSE5622**, MASTA S851 | AtGenExpress / MASTA |
| **Ethylene** | ACC precursor treatment (4 h) | **GSE193833** | GEO · RNA-seq |
| **UV** | UV-B exposure vs control | **GSE5626** vs **GSE5620** | AtGenExpress · ATH1 GPL198 |
| **Magnetic / Null Field** | Curated near-null magnetic field ($<30\text{ nT}$) panel | Parmagnani/Maffei 2022 | Curated localization tier |

---

## Citation & License

The computational framework and curated datasets are released under the open-source **MIT License**. Machine-readable citation metadata is available in [CITATION.cff](https://github.com/dr-richard-barker/deepspace-seed-stress-decoder/blob/main/CITATION.cff).

```bibtex
@software{barker_deepspace_2026,
  author    = {Barker, Richard},
  title     = {{DeepSpace Plant-Stress to Germinating-Seed Decoder
               (DSRS + GSAD) and Seed-Susceptibility Atlas}},
  year      = {2026},
  version   = {0.2.0},
  license   = {MIT},
  publisher = {Zenodo},
  doi       = {10.5281/zenodo.0000000},
  url       = {https://github.com/dr-richard-barker/deepspace-seed-stress-decoder}
}
```

Companion manuscript (targeted at _npj Microgravity_):

```bibtex
@article{barker_seed_susceptibility_2026,
  author  = {Barker, Richard},
  title   = {{A cell-type-resolved atlas of deep-space stress susceptibility
             in the dry and germinating Arabidopsis seed}},
  year    = {2026},
  journal = {npj Microgravity},
  note    = {Manuscript targeted at npj Microgravity; version 0.2.0 compendium release}
}
```

**Author**: Richard Barker — Purdue University; The Collaborative Science Environment, PBC.  
**Correspondence**: `dr.richard.barker@gmail.com`

---

_All decoder outputs represent predicted concordance from cross-stage signature transfer, not proven direct causation; claims are categorized by evidence tiers and paired with explicit experimental falsification criteria._
