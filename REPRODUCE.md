# Reproduce — DeepSpace seed decoder (FAIR guide)

End-to-end reproduction. All inputs are public; accessions + provenance are in
[`data/data_inventory.csv`](data/data_inventory.csv) and [`data/download_manifest.md`](data/download_manifest.md).

## 1. Environment
- **Python ≥3.10**: `pip install -r requirements.txt` (scanpy, anndata, gseapy, statsmodels, openpyxl, …).
- **R ≥4.4 + SeuratObject** (only to open the Gehring `.rds` atlas and export counts).
- Tools: `cd tools && pip install -e .` (provides the `deepspace` CLI).

## 2. Data (download via accessions)
| input | accession | used for |
|---|---|---|
| Gehring developmental seed atlas | GEO **GSE295007** | seed cell-type panels (Tool 2 reference) |
| Germination atlas (matrix) | GEO **GSE182331** (mirror of ArrayExpress E-MTAB-12532) | dry→germinating state panels |
| Microgravity / radiation | NASA OSDR **OSD-120/678/658/498/502/508/510/782** | stressor contrasts |
| Low-oxygen | GEO **GSE315308** (hypoxia/anoxia), **GSE182724** (submergence) | stressor contrasts |
| Gravitropism / phototropism | GEO **GSE199142** / **GSE3847** (ATH1, GPL198) | stressor contrasts |
| NMF (null magnetic field) | Maffei 2021/2022 (panel only; full arrays on author request) | localization |

## 3. Pipeline (numbered scripts, run in order from repo root)
```
01_inspect_gehring.R / 02_export_gehring.R   # open atlas, export counts
03_build_panels.py  06_annotate_and_replot.py  26_dry_seed_panel.py
                                             # 123-panel seed reference (+ named germ clusters + dry_seed)
04_decoder_project.py                        # OSD microgravity/GCR -> seed panels (v1)
10_radiation_decoder.py 15_oxygen_stressors.py 16_gravity_stressors.py 17_phototropism.py 23_hypergravity.py 24_more_stressors.py
                                             # radiation/low-O2/gravity/photo/hypergravity/desiccation+osmotic+ethylene+temp+UV -> v7 (27 contrasts, 10 families)
08_nmf_localization.py  25_nmf2021_localization.py   # NMF localization (2022 oxidative + 2021 Sci Rep panels)
07/12/13/14_bridge*.py                       # shared-latent bridge + embryo-lineage validation
18_deepspace_atlas.py 19_atlas_tissue_stage.py   # susceptibility atlas (cell-type / tissue / stage)
11_combined_heatmap.py 20_manuscript_figures.py  # combined figure + npj F1-F6
09_build_report_pdf.py 21_build_manuscript_pdf.py 22_build_docx.py 27_build_supplementary.py  # report + manuscript + supplementary
```
Outputs: `panels/`, `results/tables/`, `results/figures/`, `report/`.
*(Reproducibility smoke-test 2026-06-27: all Python scripts compile; `deepspace` tools run end-to-end from
committed panels/tables; figure scripts regenerate from committed `results/tables/`.)*

## 4. Use the tools
```bash
deepspace dsrs your_signature.csv     # which space stressor does it resemble?
deepspace gsad your_signature.csv     # predicted effect on the dry/germinating seed
```
`your_signature.csv` = two columns: gene (AGI/TAIR) + log2FC. See `tools/examples/`.

## Notes
- Determinism: GSEA-prerank uses fixed seed=42, permutation_num=200.
- Gene IDs harmonized to **AGI/TAIR**; `data/raw/entrez_to_tair.csv` + GPL198 map handle GEO ID variants.
- All results are **predicted concordance** (signature transfer), not proven causation; claims carry
  Direct/Atlas/Literature/Hypothesis tiers + falsification tests.
