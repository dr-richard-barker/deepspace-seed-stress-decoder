---
layout: default
title: DeepSpace Seed-Stress Decoder
---

_Which seed cell types and developmental stages are susceptible to deep-space stressors?_

Two reusable, FAIR tools and a single-cell **seed-susceptibility atlas** for plant space biology, built on
_Arabidopsis_. Give the decoder a bulk transcriptomic signature; it recognises which space stressor the
signature resembles and predicts its effect on the dry and germinating seed, cell type by cell type.
Companion to a manuscript targeted at _npj Microgravity_.

[View the repository on GitHub](https://github.com/dr-richard-barker/deepspace-seed-stress-decoder){: .btn}

| 27 contrasts | 10 stressor families | 123 seed panels | 9 / 10 families hit the root cap |
|:---:|:---:|:---:|:---:|

![Concept workflow: a query transcriptomic signature feeds two tools — DSRS (which space stressor?) and GSAD (effect on the seed?) — whose outputs assemble into the DeepSpace seed-susceptibility atlas, with the headline that the radicle/root tip is a multi-stressor hotspot.]({{ '/assets/figures/F1_concept_workflow.png' | relative_url }})

*Figure 1 — Concept workflow. A single query signature drives both tools; their outputs assemble into the
cell-type × stressor susceptibility atlas and its convergence metric.*

---

## The question

Deep-space environments combine **microgravity**, chronic **ionizing radiation**, a near-absent or altered
**magnetic field**, and the confined, potentially hypoxic gas environment of flight hardware — and the loss of
a stable gravity vector removes the **gravitropic** set-point that organises seedling establishment. Each
stressor has documented effects on adult plant transcriptomes, but the consequences for the **dry/dormant and
germinating seed** — the stage that determines whether a crop establishes at all — are poorly resolved,
because spaceflight experiments sample seedlings and organs rather than seeds. This project bridges that gap by
projecting stressor signatures onto a single-cell seed reference.

---

## The two tools

Both tools rank a query signature by log<sub>2</sub> fold-change and project it onto the seed panels by
pre-ranked gene-set enrichment. They differ only in what they ask of the result.

| Tool | What it does | Question |
|---|---|---|
| **DSRS** — DeepSpace Stress-Recognition System | Recognise **which space stressor** a signature most resembles across the reference families (gravity, radiation, low-oxygen, tropism, desiccation, osmotic, ethylene, temperature, UV). | _"Which space stressor is this?"_ |
| **GSAD** — Germinating-Seed AutoDecoder | Predict a bulk transcriptome's **effect on the dry / germinating seed** — a per cell-type, per-tissue, per-stage susceptibility profile against the 123-panel reference. | _"What does it do to the seed?"_ |

Input is a two-column CSV: gene (AGI/TAIR, e.g. `AT1G01010`) and log<sub>2</sub>FC.

```bash
# install
cd tools && pip install -e .

# which space stressor does my signature resemble?
deepspace dsrs my_signature.csv --out matches.csv

# predicted effect on the dry / germinating seed
deepspace gsad my_signature.csv --out seed_susceptibility.csv
```

```python
# or from Python
import deepspace
top, fam = deepspace.dsrs.recognize("my_signature.csv")   # which stressor?
seed     = deepspace.gsad.decode("my_signature.csv")       # effect on the seed
seed["celltype"].head()                                    # ranked cell-type susceptibility
```

Outputs are _predicted concordance_ (signature transfer across tissue and stage), not proven causation —
every claim carries an evidence tier and a falsification test.

---

## A validated single-cell seed reference

The reference is a 123-panel library — 122 single-cell marker panels from the developmental seed atlas
(snRNA-seq, 3/5/7 days after pollination) and the germination atlas (scRNA-seq, 12/24/48 h post-imbibition),
plus a bulk dry-seed anchor. Panels reproduce canonical markers (oleosins and cruciferin for embryo,
_BANYULS_ for the inner-integument endothelium).

As a stringent positive control, the decoder was restricted to embryo cells and asked which germinating-seed
cell type each developing-embryo state maps onto. It independently recovers established developmental lineages
from transcriptomes alone:

- **protoderm → epidermis**
- **hypophysis → radicle apical meristem** — placing the embryonic hypophysis as the developmental origin of the radicle growth-point
- **vascular primordium → provasculature**
- **inner cotyledon → cotyledon mesophyll**, and **cortical initials → hypocotyl cortex**

![Seed reference and embryo-lineage validation heatmaps, showing developing-embryo states mapping onto the expected germinating-seed cell types.]({{ '/assets/figures/F3_seed_reference_embryo_lineage.png' | relative_url }})

*Figure 3 — Validated seed reference. Recovering ground-truth embryo→seedling lineages confirms the projection
machinery reflects real cell-type biology rather than artefact.*

---

## The deep-space stress library

Genome-wide signatures span ten stressor families, assembled from public NASA OSDR and GEO/AtGenExpress
datasets. A recurrent theme: stressed adult/vegetative tissue transcriptionally resembles the
**early-germination (12 h) state**, suggesting a shared stress-engaged program at the onset of germination.

| Family | Represented by |
|---|---|
| **Gravity** | spaceflight microgravity (root & leaf) + 2 g hypergravity — the µg↔1 g↔hypergravity axis |
| **Radiation** | GCR-relevant low-dose, acute γ |
| **Tropism** | gravitropism, phototropism |
| **Low-oxygen** | hypoxia, anoxia, submergence |
| **Desiccation** | seed maturation drying |
| **Osmotic** | mannitol |
| **Ethylene** | ACC |
| **Temperature** | warm / thermomorphogenesis |
| **UV** | UV-B |
| **Magnetic / null field** | curated NMF panel, handled by expression-localization (not GSEA) |

![DSRS stress-recognition library: enrichment fingerprints of the stressor contrasts across the seed panels.]({{ '/assets/figures/F2_stress_library.png' | relative_url }})

*Figure 2 — DSRS stress library. Each contrast's seed-program fingerprint across the reference panels; DSRS
matches a query to this library.*

---

## Headline result: the root tip is the multi-stressor convergence apex

Scoring each germinating-seed cell type by how many of the ten stressor _families_ significantly target it —
a family-level metric so no single data-rich family dominates — gives an unambiguous result.

- **Columella / root cap — 9 of 10 families.** Targeted by more stressor families than any other
  biologically-defined germinating-seed cell type.
- **Radicle apical meristem** — the specific null-magnetic-field target (localization z = +7.96); radicle
  epidermis completes a broadly susceptible root pole. Hypocotyl cortex and cotyledon mesophyll are secondary
  hotspots (6–7/10).

![DeepSpace seed-susceptibility atlas heatmap: germinating-seed cell types (rows) against ten stressor families (columns), coloured by signed strength with significance stars, plus a convergence bar chart. Columella/root cap scores 9 of 10 families; radicle apical meristem shows an intense magnetic/NMF signal.]({{ '/assets/figures/F5_deepspace_atlas.png' | relative_url }})

*Figure 5 — The DeepSpace seed-susceptibility atlas. Rows are germinating-seed cell types, columns the ten
stressor families; colour is signed strength (NES / NMF z) and \* marks significance. The right-hand bars count
how many families reach each cell type. Early germination (12 h) is the most multi-stressor-vulnerable
developmental window.*

---

## A convergent model centred on the radicle growth-point

Four independent lines converge on the radicle growth-point:

1. **Null magnetic field** — NMF-responsive genes localise to the radicle apical meristem (z = +7.96).
2. **Microgravity** — modulates the radicle-meristem program in a light-gated manner.
3. **Gravitropism** — itself a root-tip phenomenon, engages the same program.
4. **Development** — the structure is founded by the embryonic hypophysis, which the lineage analysis maps
   directly onto the radicle apical meristem.

![Convergence model diagram: null magnetic field, microgravity, radiation/GCR, gravitropism, and the developmental origin (embryonic hypophysis) all point at the radicle apical meristem / root growth-point, with falsification tests H1 and H2.]({{ '/assets/figures/F6_convergence_model.png' | relative_url }})

*Figure 6 — Convergent model & falsification tests. The radicle apical meristem is proposed as a priority
cellular target for deep-space seed performance, with two high-confidence, falsifiable predictions —
**H1:** near-null magnetic field induces radicle-meristem markers and alters radicle emergence, abolished in
_cry1 cry2_; **H2:** microgravity suppresses radicle proliferative programs in a light-gated manner.*

> All predictions are framed as **concordance, not causation**. GSAD performs signature transfer across tissue
> and developmental stage, so each claim carries an evidence tier (direct data / atlas projection / literature
> / hypothesis) and an explicit experiment that would refute it.

---

## Reproduce

Every input is public; the pipeline is numbered end-to-end.

1. **Environment.** Python ≥3.10 (`pip install -r requirements.txt`); R ≥4.4 + SeuratObject to open and export
   the developmental atlas; `cd tools && pip install -e .` for the `deepspace` CLI.
2. **Data.** Download from accessions in
   [`data/data_inventory.csv`](https://github.com/dr-richard-barker/deepspace-seed-stress-decoder/blob/main/data/data_inventory.csv)
   (see the table below).
3. **Pipeline.** Run the numbered scripts `01–30` in order — build panels → project each stressor family →
   NMF localization → bridge/lineage validation → atlas → figures → manuscript.
4. **Use the tools** on your own signature with `deepspace dsrs` / `deepspace gsad`.

Determinism: GSEA-prerank uses a fixed seed (42) and 200 permutations; gene IDs are harmonised to AGI/TAIR.
Full guide in
[REPRODUCE.md](https://github.com/dr-richard-barker/deepspace-seed-stress-decoder/blob/main/REPRODUCE.md);
the complete living dev log is in
[PLANNING.md](https://github.com/dr-richard-barker/deepspace-seed-stress-decoder/blob/main/PLANNING.md).

---

## Data & accessions

Full provenance is in
[`data/data_inventory.csv`](https://github.com/dr-richard-barker/deepspace-seed-stress-decoder/blob/main/data/data_inventory.csv).
The one exception is the genome-wide null-magnetic-field arrays, which are not publicly deposited — that arm
relies on a curated localization-tier gene panel while a request to the source authors is outstanding.

| Role | Dataset | Accession | Repository / platform |
|---|---|---|---|
| **Seed reference** | Developmental seed atlas (3/5/7 DAP) | **GSE295007** | GEO · snRNA-seq |
| **Seed reference** | Germination atlas (12/24/48 h) | **GSE182331** · E-MTAB-12532 | GEO / ArrayExpress · scRNA-seq |
| Gravity — microgravity | Spaceflight root; leaf | **OSD-120**; **OSD-678** | NASA OSDR · RNA-seq |
| Gravity — hypergravity | 2 g vs 1 g callus | **GSE29787** | GEO · Agilent GPL9020 |
| Radiation — GCR | Whole seedling 40/80 cGy | **OSD-658** | NASA OSDR · RNA-seq |
| Radiation — acute γ | 100 Gy Co-60 time-course | **OSD-498/502/508/510** | NASA OSDR · RNA-seq |
| Radiation — low-dose | Cs-137, 10 & 100 cGy | **OSD-782** | NASA OSDR · RNA-seq |
| Low-oxygen | Hypoxia/anoxia; submergence | **GSE315308**; **GSE182724** | GEO · RNA-seq |
| Tropism — gravitropism | Root gravistimulation time-course | **GSE199142** | GEO · RNA-seq |
| Tropism — phototropism | Auxin/tropic-growth gradient | **GSE3847** | GEO · ATH1 GPL198 |
| Desiccation | Seed maturation drying (21 vs 15 DAF) | **GSE76015** | GEO |
| Ethylene | ACC 4 h vs 0 h | **GSE193833** | GEO |
| Temperature | 27 vs 21 °C (thermomorphogenesis) | **GSE303133** | GEO |
| Osmotic; UV-B | Mannitol; UV-B vs control | **GSE5622**; **GSE5626** vs **GSE5620** | AtGenExpress · ATH1 GPL198 |
| Magnetic / null field | NNMF arrays (Parmagnani/Maffei 2022; Agliassa/Maffei 2021) | _not deposited — curated panel_ | Journal supplement · localization-tier |
| Cross-check | Mature-root eFP map (Brady et al. 2007) | **GSE8934** | GEO · ATH1 GPL198 |

---

## Cite

Released under the MIT license; a Zenodo DOI will be minted on deposit. Machine-readable metadata in
[CITATION.cff](https://github.com/dr-richard-barker/deepspace-seed-stress-decoder/blob/main/CITATION.cff).

Software / dataset (replace the Zenodo DOI once minted on deposit):

```bibtex
@software{barker_deepspace_2026,
  author    = {Barker, Richard},
  title     = {{DeepSpace Plant-Stress to Germinating-Seed Decoder
               (DSRS + GSAD) and seed-susceptibility atlas}},
  year      = {2026},
  version   = {0.1.0},
  license   = {MIT},
  publisher = {Zenodo},
  doi       = {10.5281/zenodo.0000000},
  url       = {https://github.com/dr-richard-barker/deepspace-seed-stress-decoder}
}
```

Companion manuscript (draft, targeted at _npj Microgravity_):

```bibtex
@article{barker_seed_susceptibility_2026,
  author  = {Barker, Richard},
  title   = {{A cell-type-resolved atlas of deep-space stress susceptibility
             in the dry and germinating Arabidopsis seed}},
  year    = {2026},
  journal = {npj Microgravity},
  note    = {Manuscript in preparation}
}
```

Author: **Richard Barker** — Purdue University; The Collaborative Science Environment, PBC.

---

_All decoder outputs are predicted concordance from cross-stage signature transfer, not proven causation;
claims carry evidence tiers and falsification tests. Manuscript draft targeted at npj Microgravity._
