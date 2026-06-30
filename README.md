# DeepSpace Plant-Stress → Germinating-Seed Decoder

*Which seed cell types and developmental stages are susceptible to deep-space stressors?*

Two reusable, FAIR tools + a single-cell **seed-susceptibility atlas** for plant space biology, built on
Arabidopsis. Companion to a manuscript targeted at *npj Microgravity*.

> **Status:** v0.1.0 — analysis, tools, atlas, figures and manuscript complete. The only pending input is
> genome-wide null-magnetic-field array data (author request out). Full dev history: [`PLANNING.md`](PLANNING.md).

## The two tools (`tools/deepspace/`)
| Tool | What it does |
|---|---|
| **DSRS** — DeepSpace Stress-Recognition System | Given a transcriptomic signature, recognize **which space stressor** it most resembles across the GSEA reference families (gravity, radiation, low-oxygen, tropism, desiccation, osmotic, ethylene, temperature, UV). *(Null-magnetic-field is a localization-tier family, not part of the DSRS reference — see Methods.)* |
| **GSAD** — Germinating-Seed AutoDecoder | Given **bulk transcriptomics**, predict its **effect on the dry/germinating seed** — a per cell-type / tissue / stage susceptibility profile. |

```bash
cd tools && pip install -e .
deepspace dsrs  my_signature.csv      # which space stressor?
deepspace gsad  my_signature.csv      # effect on the seed
```
Input = a 2-column CSV (gene AGI/TAIR, log2FC). See `tools/README.md` and `tools/examples/`.

## Headline result
Across a **27-contrast / 10-family** deep-space stress model projected onto a 123-panel seed
reference (122 single-cell panels from the Gehring developmental + Liew/Lewsey germination atlases, plus a
bulk dry-seed anchor), the **radicle / root apical tip is the
multi-stressor convergence hotspot**, and **early germination (12 h) is the most vulnerable stage**. The
pipeline is validated by a positive control: restricted to the embryo lineage it recovers textbook
developmental relationships (e.g. hypophysis → radicle apical meristem). All outputs are *predicted
concordance*, not causation, with evidence tiers and falsification tests.

## Repository layout
```
tools/         deepspace package (DSRS + GSAD) + CLI + examples
scripts/       numbered, reproducible pipeline (01–27)
panels/        seed cell-type/state marker panels (CSV + GMT)
results/        tables/ + figures/  (per-analysis result notes alongside)
report/         npj manuscript (.md/.pdf/.docx), figures_npj/ (F1–F6), cover letter, synthesis report
data/           data_inventory.csv + download_manifest.md  (raw/processed are gitignored — regenerate)
REPRODUCE.md    end-to-end reproduction guide   ·   PLANNING.md   full living dev log
```

## Data & reproducibility
All inputs are public; accessions and provenance are in [`data/data_inventory.csv`](data/data_inventory.csv).
Large raw/derived data are gitignored — see [`REPRODUCE.md`](REPRODUCE.md) to regenerate from accessions and
run scripts `01–27` in order.

## Citation & license
See [`CITATION.cff`](CITATION.cff). MIT licensed ([`LICENSE`](LICENSE)). Zenodo DOI to be minted on release.
Author: **Richard Barker** (Purdue University; The Collaborative Science Environment, PBC).
