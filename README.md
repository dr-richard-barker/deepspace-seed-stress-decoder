# DeepSpace Plant-Stress → Germinating-Seed Decoder

*Which seed cell types and developmental stages are susceptible to deep-space stressors?*

Two reusable, FAIR tools + a single-cell **seed-susceptibility atlas** for plant space biology, built on
Arabidopsis. Companion to a manuscript targeted at *npj Microgravity*.

🌐 **Project site:** https://dr-richard-barker.github.io/deepspace-seed-stress-decoder/ — visual walkthrough of the two tools, the stress library, and the headline atlas result.

> **Status:** v0.2.0 — analysis, tools, atlas, figures, and manuscript updated. Reference stress library expanded to **49 contrasts / 15 families** integrating decoupled NASA Exploration Atmospheres (TabPFN v2), Redox Decoder (CVAE ROS latent space), and the Max Planck MASTA database. Full dev history: [`PLANNING.md`](PLANNING.md) · Synthesis: [`docs/stimuli_decoders_synthesis.md`](docs/stimuli_decoders_synthesis.md).

## The tools (`tools/deepspace/`)
| Tool / Command | What it does |
|---|---|
| **DSRS** — `deepspace dsrs` | Given a transcriptomic signature, recognize **which space stressor** it most resembles across the GSEA reference families (gravity, radiation, low-oxygen, hypobaria, redox_ros, cold, wounding, hormones, nutrients, desiccation, osmotic, temperature, UV). |
| **GSAD** — `deepspace gsad` | Given **bulk transcriptomics**, predict its **effect on the dry/germinating seed** — a per cell-type / tissue / stage susceptibility profile. |
| **MASTA** — `deepspace masta-project` | Given any contrast from the 592-contrast Max Planck MASTA database (e.g. `S851&cold_wt-wt_3h`), project it on-demand through both DSRS and GSAD. |

```bash
cd tools && pip install -e .
deepspace dsrs  my_signature.csv              # which space stressor?
deepspace gsad  my_signature.csv              # effect on the seed
deepspace masta-project "S851&cold_wt-wt_3h"   # on-demand MASTA projection
deepspace masta-list -c S                     # list available stress contrasts
```
Input = a 2-column CSV (gene AGI/TAIR, log2FC). See `tools/README.md` and `tools/examples/`.

## Headline result
Across an expanded **49-contrast / 15-family** deep-space stress model projected onto a 123-panel seed
reference (122 single-cell panels from the Gehring developmental + Liew/Lewsey germination atlases, plus a
bulk dry-seed anchor), the **columella / root cap (14/15 families) and radicle apical meristem (10/15 families)
remain the definitive multi-stressor convergence hotspot**, and **dry seed / early germination (12 h) is the most vulnerable stage**. The
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


## Key Results & Figures
*Figures and results are currently being compiled. Please refer to the repository data folders for early analysis outputs.*

