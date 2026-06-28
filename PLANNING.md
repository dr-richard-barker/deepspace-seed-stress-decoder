# DeepSpace Plant-Stress → Germinating-Seed Decoder  ·  (→ npj Microgravity)

**Living planning & progress document.** This README is the single source of truth for project
thoughts, decisions, status, and continuity across sessions. Update it at the end of every working
session (see Changelog).

> **STATUS — v0.1.0 COMPLETE & PUSHED (2026-06-27).** All phases 0–5 done (see §8 audit for the
> authoritative per-phase status). Delivered: two FAIR tools (**DSRS** + **GSAD**), a **27-contrast /
> 10-family** DeepSpace stress model, the **seed-susceptibility atlas** (cell-type/tissue/stage), npj
> figures **F1–F6** (Arial/300 dpi), and the **npj Microgravity manuscript** (.md/.pdf/.docx). Repo live
> (private): **github.com/dr-richard-barker/deepspace-seed-decoder**.
> **Only external items remain:** genome-wide NMF (Maffei author reply) and the Zenodo DOI + public flip
> at submission. §1 below = original goal (now the methodological core of Tool 2); §1A = the vision it grew into.

---

## 1. Goal

A **new standalone project** with two coupled aims:

1. **Comprehensive meta-analysis** of Arabidopsis transcriptional datasets under **null / near-null /
   hypomagnetic magnetic fields (NMF)**.
2. A **dry- and germinating-seed tissue-specific "decoder"** that takes RNA-seq from *later
   developmental-stage tissues* and projects/predicts how those signatures map onto the developmental
   biology of the **dormant and germinating seed**.

The decoder is a **bridge**: it accepts BOTH (a) adult/vegetative stress-tissue signatures (OSD + NMF)
AND (b) late-seed-development signatures, and projects both onto a single **dry/germinating seed
reference**.

> **Framing discipline (carry over from the Biomni repo):** outputs are *predicted concordance*
> (signature/label transfer across tissue and developmental stage), **not proven causation**. Every
> claim carries an evidence tier: **Direct data / Atlas projection / Literature / Hypothesis**, and
> hypotheses ship with a falsification test.

---

## 1A. CONSOLIDATION VISION → npj Microgravity (2 tools + DeepSpace seed atlas)

**One-line thesis.** *Which seed cell types and developmental stages are susceptible to deep-space
stressors?* We answer it by recognizing space-stress transcriptional signatures and decoding them onto a
single-cell dry/germinating-seed reference — and we ship the machinery as two reusable tools.

### The two tools (the distilled software)

**Tool 1 — DSRS: DeepSpace Stress-Recognition System** *(stress pattern recognition for plant space biology)*
- **Input:** any plant transcriptomic perturbation signature (ranked log2FC, or DE table).
- **Core:** a curated **stress reference library** (gene-set panels + signed signatures per stressor class)
  spanning microgravity, ionizing radiation/GCR, null magnetic field (NMF), hypoxia, anoxia, hypergravity,
  and tropisms; GSEA/ssGSEA projection + a nearest-signature classifier with confidence + tier.
- **Output:** "which space stressor(s) does this signature resemble?" + per-class scores + novelty flag.
- **Built from:** scripts 04/10 (projection engine) generalized; panel/signature library versioned as GMT.

**Tool 2 — GSAD: Germinating-Seed AutoDecoder** *(bulk transcriptomics → modeled effect on the seed)*
- **Input:** bulk (or pseudobulk) transcriptomics / a signature from later developmental stages.
- **Core:** projection + within-source-scaled latent onto the **122-panel seed reference** (Gehring dev +
  germination atlas), with the embryo-lineage backbone as positive control.
- **Output:** predicted **seed cell-type / state susceptibility profile** (which dry/germinating programs
  are concordantly perturbed), with tiers + falsification.
- **Built from:** scripts 03/05/06/07/12/13/14 (panels, decoder, bridge, embryo lineage).

**Manuscript workflow:** DSRS characterizes each space-stressor signature → GSAD decodes it onto seed cell
types → combine into the **DeepSpace seed-susceptibility atlas**.

### DeepSpace seed-susceptibility atlas (the headline deliverable)
A matrix **[seed cell type / developmental stage] × [space stressor]** of concordance scores, plus a
**multi-stressor convergence score** per cell type (how many independent stressors significantly target it).
Key questions it must answer:
- **Is the radicle (root) apical tip susceptible to MULTIPLE space stimuli?** (working hypothesis: yes —
  NMF z+7.96, light-gated µg, SMF auxin, hypophysis developmental origin already converge there).
- Which **other tissues / developmental stages** (dry vs 12/24/48 h germinating; embryo lineage) are most
  deep-space-responsive, and which are robust?

### Stressor panel — FINAL (27 contrasts, 10 families; all in `decoder_nes_matrix_v7.csv`)
| stressor family | status | data |
|---|---|---|
| gravity (µg / partial-g / hypergravity) | ✅ | OSD-120 root, OSD-678 leaf; hypergravity GSE29787 LDC 2 g |
| ionizing radiation / GCR | ✅ | OSD-658 (40/80 cGy) + OSD-498/502/508/510 (100 Gy γ) + OSD-782 (Cs-137 cGy) |
| low-oxygen (hypoxia / anoxia / submergence) | ✅ | GSE315308 (1%/0% O₂) + GSE182724 (submergence) |
| desiccation | ✅ | GSE76015 (seed 21 vs 15 DAF) |
| osmotic | ✅ | AtGenExpress GSE5622 (mannitol) vs GSE5620 |
| ethylene / CO₂ | ✅ | GSE193833 (ACC 4 h vs 0 h) |
| temperature | ✅ | GSE303133 (27 vs 21 °C) |
| UV | ✅ | AtGenExpress GSE5626 (UV-B) vs GSE5620 |
| tropism (gravitropism / phototropism) | ✅ | GSE199142 (gravistim) + GSE3847 (phototropic) |
| null magnetic field (NMF) | ◐ localization (2 panels) | 2022 oxidative panel + 2021 Sci Rep DEG lists (S7) localized; genome-wide arrays **pending Maffei reply** |
| high static magnetic field | ⚪ comparator (not integrated) | GSE29787 (10–16.5 T), PRJNA529956 (600 mT) |

### Tropisms — RESOLVED
gravitropism (GSE199142) and phototropism (GSE3847) **integrated** as contrasts. **hydrotropism** and
**thigmotropism/touch** had no usable transcriptome (0 GEO RNA-seq) → **dropped** (per user: unreliable).

### Other deep-space stimuli — status
Integrated: desiccation, osmotic, ethylene/CO₂, temperature, UV (all ✅, v7). **Future/optional** (not in
v0.1.0): plant fractional gravity (EMCS Moon/Mars), cold, rehydration, clinostat/RPM, mechanical/vibration,
combined-stress.

### FAIR + reproducibility plan (GitHub + Zenodo)
- **Findable:** all inputs in `data/data_inventory.csv` with accessions; archived release → **Zenodo DOI**.
- **Accessible:** public GitHub repo; only public data (NMF arrays cited as restricted-until-deposited).
- **Interoperable:** standard formats — AnnData/`.h5ad`, CSV, **AGI/TAIR** gene IDs, **GMT** panel library,
  signed-signature tables; evidence-tier + falsification metadata on every claim.
- **Reusable:** OSI license, pinned envs (`requirements.txt` + R `sessionInfo`), numbered reproducible
  scripts (01–N) → optionally a Snakemake/Makefile `reproduce` target; example notebooks for each tool;
  deterministic seeds.
- **Tools packaged** as a small Python package: `dsrs` (Tool 1) + `gsad` (Tool 2) CLIs/modules + docs.

### Figure plan (npj Microgravity)
- **F1** Conceptual: 2-tool workflow (signature → DSRS recognition → GSAD seed decode → atlas).
- **F2** DSRS stress reference library: combined perturbation heatmap across ALL stressor classes.
- **F3** Seed reference + validation: atlas overview + embryo-lineage positive control (textbook lineages).
- **F4** GSAD: stressor → seed cell-type susceptibility heatmap (within-source scaled).
- **F5** DeepSpace seed-susceptibility **atlas**: cell-type × stressor matrix + multi-stressor convergence
  (radicle-tip highlight).
- **F6** Convergence model + falsification hypotheses (radicle growth-point; hypophysis origin).
- **Supp:** data inventory, methods, NMF localization, per-stressor detail, tier audit.

### Manuscript outline (npj Microgravity)
Title → Abstract → Intro (space stressors × seed/germination knowledge gap) → Results (Tool 1, Tool 2,
Atlas, convergence) → Discussion → Methods (FAIR pipeline) → Data Availability (accessions + Zenodo DOI) →
Code Availability (GitHub + Zenodo). Author line per user (Barker et al.); relate to [[osd767-manuscript]].

---

## 2. Key decisions (locked 2026-06-26)

| Decision | Choice | Rationale |
|---|---|---|
| Decoder input | **Both, as a bridge** | Adult/vegetative (OSD+NMF) AND late-seed-dev signatures both projected onto dry/germinating reference |
| Seed reference atlas | **Both atlases** | Gehring developmental atlas for tissue markers + germination atlas for the dry→germinating state axis |
| Project scope | **New standalone project** | Cites the Biomni integrated analysis as prior context; does not modify it |

---

## 3. Source materials

### Prior work (context, read-only)
- **Biomni integrated analysis** — `kritipatra25-cpu/phyD-spaceflight-analysis/tree/main/Biomni`
  (GitHub). Completed systems-biology synthesis of Arabidopsis germination under µg / GCR / NMF.
  - Integrates OSD-120 (root µg), OSD-678 (shoot µg), OSD-658 (GCR), Maffei et al. 2022 NMF panel.
  - Has pathway scores, cross-dataset meta-enrichment, gene–gene network, NMF cluster A–E analysis,
    autoencoder latent, master-regulator + vulnerable-cell rankings, 9-tissue reachability matrix,
    and a Direct/Atlas/Literature/Hypothesis tier system.
  - **Limitation 1:** NMF = only the Maffei **194-gene oxidative panel** (not genome-wide); 0–4 gene
    overlap with cell-type markers → NMF cell-type enrichment was infeasible there. **← our Phase 1 gap.**
  - **Limitation 2:** embryo/endosperm/seed-coat/radicle are **literature-only (T3)** — no
    seed-resolved data. **← our Phase 2 gap.**

### Target seed atlases
- **Developmental seed atlas** — Martin, Cogdill, Pusey, … Gehring. *"A transcriptional atlas of early
  Arabidopsis seed development…"* **Nature Plants 2026**, DOI 10.1038/s41477-026-02295-8.
  snRNA-seq at **3, 5, 7 DAP**; embryo / endosperm / seed coat of the *developing* seed.
  Role: **embryo/endosperm/seed-coat cell-type marker panels**. (NOTE: developmental, not
  dry/germinating — used for tissue markers, not the state axis.)
- **Germination atlas** — *"Establishment of single-cell transcriptional states during seed
  germination."* **Nature Plants 2024**, DOI 10.1038/s41477-024-01771-3. Single-cell germinating
  embryo, dry → imbibed → germinated. Role: **the dry→germinating state axis** (the actual decoder target).

### NMF transcriptomic landscape — RESOLVED 2026-06-26 (genome-wide is the binding constraint)
- Maffei / Agliassa **NNMF microarray time-course** (root + shoot, 10 min–96 h) — **NOT deposited** in
  GEO or ArrayExpress. Only the **194-gene oxidative supplement (S2)** is public = the subset the Biomni
  repo already used. Full array needs an **author request**. ← Phase 1's real bottleneck.
- Paul & Ferl **callus** (GEO **GSE29787**) — public, BUT a **strong-gradient magnet (HIGH-field)**, the
  opposite of null. Use only as a labeled magnetic *comparator*, not as NMF.
- Jin et al. 2019 **SMF root** (SRA **PRJNA529956**; Sci Rep 9:14384) — **600 mT static (HIGH) field**, NOT
  null. Include as a labeled comparator: it's a RARE *public genome-wide* magnetic transcriptome and its
  auxin (PIN3/AUX1) / nitrate / cell-wall / flavonoid biology overlaps the repo's core axes. Raw FASTQ
  only → needs reprocessing. VERIFY N0/N180 = orientation (both 600 mT), not a null condition.
- (optional) Differential root/shoot magnetoresponses, Sci Rep 2021 (s41598-021-88695-6) — further
  magnetic comparator if broader coverage wanted; resolve accession before use.
- Flowering (2018) / lipid / nutrient hypomagnetic studies — **qPCR-only** → not usable for genome-wide meta.
- **Hard exclusion:** high-field studies (opposite perturbation; dominate keyword searches).
- **See [`notes/phase0_feasibility.md`](notes/phase0_feasibility.md) and [`data/data_inventory.csv`](data/data_inventory.csv).**

### Bridge input (adult/vegetative)
- OSD-120 / OSD-678 / OSD-658 (already characterized in the Biomni repo).

---

## 4. Plan & status

Legend: ☐ todo · ◐ in progress · ☑ done. **Authoritative current status: §8 completion audit.** The
per-phase notes below are the working history (kept for continuity).

### Phase 0 — Scaffold + data inventory  ✅ essentially complete
- ☑ Create project tree
- ☑ Establish this README as living planning doc
- ☑ Resolve accessions (GEO / ArrayExpress / OSDR) for all inputs → `data/data_inventory.csv`
  - Gehring dev atlas = **GSE295007**; germination atlas = **E-MTAB-12532** (+12521/13449);
    bridge inputs = **OSD-120/678/658**.
- ☑ Feasibility note → `notes/phase0_feasibility.md`
  - **KEY FINDING:** genome-wide NNMF data is NOT public (Maffei array undeposited; only 194-gene
    supplement). GSE29787 is high-field, not null. Phase 1 needs a path decision (see Open Questions).
- ☑ Path confirmed (`C:\Users\drric\Downloads\nmf_seed_decoder`); compute = LOCAL; repo on GitHub.

### Phase 1 — NMF transcriptional meta-analysis  ◐ REFRAMED (externally blocked)
Genome-wide NNMF is not publicly deposited (audited GEO/SRA/BioProject/ArrayExpress; both Maffei 2021/2022
arrays "supp tables + on request"). **Delivered via expression-localization, TWO panels:**
- 2022 oxidative panel (`scripts/08`) → NMF-up genes localize to the **radicle apical meristem (z +7.96)**.
- 2021 Sci Rep S7 DEG lists (`scripts/25`, `results/nmf2021_results.md`) → undirected NNMF DEGs localize to
  **cotyledon mesophyll + hypocotyl cortex** (radicle-meristem NOT reproduced; r=0.35 vs 2022). → the
  radicle signal is **oxidative-NNMF-gene-specific**, an honest qualifier.

> **⏳ AWAITING MAFFEI REPLY (emailed 2× ; expected ~Mon).** When he sends the genome-wide 2021+2022 array
> data link: download → reprocess to AGI DE → add as **full GSEA decoder contrasts** (replacing the
> localization-tier panels) → re-run decoder/atlas/bridge/manuscript. Author-request draft:
> `report/maffei_data_request_email.md`. **Update this README + inventory + manuscript when it arrives.**

### Phase 2 — Seed reference ("decoder target space")  ☑ COMPLETE
- ☑ Toolchain: Python env (scanpy 1.12.1 / anndata / gseapy / statsmodels) + R 4.6.0 + SeuratObject
  (user lib `C:/Users/drric/R/win-library/4.6`).
- ☑ Gehring atlas downloaded (`data/raw/GSE295007_ATLAS_merged_annotated_sigmods.rds`, 1.3 GB).
- ☑ Germination matrix sourced via **GEO mirror GSE182331** (ArrayExpress had annotations only, no matrix).
  `data/raw/germination/`: expression_mat (13501 genes × 12798 cells), meta.tsv (cluster 1–15 + time
  12/24/48 hsl), genes.tsv, barcodes, tsne. **Caveat:** earliest tp = 12 hsl → dry/0h under-sampled.
- ☑ Inspected Gehring object → `results/tables/gehring_object_summary.txt`. Structure: 23374 genes ×
  54210 cells; annotation hierarchy level_1 (5 tissues: Seed coat/Endosperm/Embryo/Funiculus/Ovule) →
  level_2 (13 cell types) → level_3 (85 marker-named states); +43 GO module-score columns.
- ☑ Exported Gehring counts+labels → `data/processed/gehring/` (counts.mtx, genes, cells, metadata).
- ☑ **Built panel library** → `panels/panel_library.csv` (6100 rows, 122 panels, 5 sources):
  Gehring L1 tissue (5), L2 celltype (13), L3 state (86); germination cluster (15), time (3).
  All 12798 germination cells matched. VALIDATED: Embryo=OLE1/2/3,CRA1,2S-albumin; ii1=BAN(AT1G61720);
  germ-12h carries residual storage transcripts. Wilcoxon, top-50/group, min 20 cells.
- ☑ **Labeled germination clusters** with cell-type names from paper open-access text (clusters 9/14
  in-situ validated; 3/6/15 confirmed by my markers) → `panels/germination_cluster_annotations.csv` +
  `panels/panel_library_annotated.csv`. Map: cotyledon mesophyll (3,13); hypocotyl cortex (1,5,7) +
  epidermis (6) + cortex/endodermis (2); radicle epidermis (10) + apical meristem (14) + columella (4);
  provasculature protophloem (15)/protoxylem (9)/provasc (12); unassigned (8,11).
- ☑ Harmonize → shared latent (pseudobulk co-embedding) — done in Phase 3 bridge (scripts 07/12/13/14).

### Phase 3 — Bridge decoder  ☑ COMPLETE
- ☑ Backbone: GSEA-prerank projection of genome-wide stressor signatures onto 122 panels →
  `scripts/04_decoder_project.py`. Pulled OSD DGE from NASA OSDR (GLDS-120/612/603, TAIR IDs).
  Result: `results/decoder_results_v1.md` + `results/tables/decoder_*` + `results/figures/decoder_*`.
  Headline: stressed adult tissue ~ early-germination (12 hsl) state; GCR-80 induces embryo/provascular;
  proliferative seed states suppressed; strong light-dependence.
- ☑ **Layer 2 shared latent (v1)** — `scripts/07_bridge_latent.py`: germinating-seed score space (15
  axes); adult-stress placed via decoder NES, late-seed-dev placed via ssGSEA of Gehring tissue×timepoint
  pseudobulk. → `results/tables/bridge_{latent,assignments}.csv`, `results/figures/bridge_*`,
  `results/bridge_results_v1.md`. KEY FINDING: dev→germination bridge is weak/lineage-limited (only embryo
  persists; seed coat/endosperm terminal); adult-stress→germ-state mappings strong.
- ☑ Added late-seed-dev (Gehring tissue×timepoint trajectory) as second bridge input (in 07).
- ☑ Refined bridge: within-source scaling (scripts/13, artifact→0.00) + embryo-lineage map (scripts/14,
  recovers textbook lineages). Re-run on full v7 (27 contrasts).
- ☑ **NMF wired in (c) via expression-localization** — `scripts/08_nmf_localization.py`. GSEA-prerank
  infeasible (max 7-gene overlap of NMF panel with marker panels, median 0), so instead localized NMF-up
  (198 genes) / NMF-down onto germinating-seed cell-type expression specificity. **Result: NMF-induced
  genes concentrate sharply in the radicle apical meristem (z +7.96)**, then cotyledon mesophyll /
  cortex-endodermis. → `results/tables/nmf_*`, `results/figures/nmf_localization_heatmap.*`,
  `results/nmf_results_v1.md`. Genome-wide NMF (full Maffei 2021+2022 arrays) still pending author request.
- ☑ Falsification hypotheses (H1–H6) + D/A/L/H tier framing — in the synthesis report & manuscript.

### Phase 4 — Synthesis + report  ☑ COMPLETE
- ☑ Figures: decoder L1/state + named germination heatmaps, bridge heatmap/embedding, NMF localization.
- ☑ **Synthesis report** pulling decoder + bridge + NMF localization with evidence tiers (D/A/L/H) and
  6 falsification hypotheses → `report/phase4_synthesis_report.md` + `.pdf` (kept current; ~12 pp).
  Renderer: `scripts/09_build_report_pdf.py` (markdown + xhtml2pdf).
- ☑ Reproducibility via numbered scripts 01–24 + `REPRODUCE.md` (notebooks not needed). Report refreshes
  when genome-wide NMF arrives.

### Phase 5 — Consolidation → 2 tools + DeepSpace atlas + npj manuscript (NEW, 2026-06-27)
**5.1 Data expansion** (see §1A tables)
- ☑ **Hypoxia + anoxia** — GSE315308 O2 gradient (1% & 0% vs 21%); Entrez→TAIR mapped → 2 contrasts
- ☑ **Submergence** — GSE182724 'Sub vs. Air' (AGI + Log2FC) → 1 contrast
  → **combined model now 18 contrasts** (`decoder_nes_matrix_v3.csv`; new class `low_oxygen`).
  `scripts/15_oxygen_stressors.py`; reusable `data/raw/entrez_to_tair.csv`. Combined figure refreshed.
- ☑ **Gravitropism** — GSE199142 gravistimulation RNA-seq (Col-0 12h & 24h vs Ref) → 2 contrasts
  (`scripts/16`). **Model now v4 = 20 contrasts.** gravitropism_12h → radicle apical meristem (+1.54).
- ✗ OSD-758/GLDS-664 REJECTED — it is a MOUSE study (ENSMUSG), not Arabidopsis (verified). Plant
  fractional-gravity = EMCS centrifuge study (source separately if wanted).
- ☑ RESOLVED (microarray/panel-tier data reality): phototropism (GSE3847 ATH1) ✅ added; hypergravity
  (GSE29787 2 g) ✅ added; hydrotropism ✗ dropped (no public transcriptome). *(see ☑ items below)*
- ☑ **Phototropism** — GSE3847 (Esmon ATH1, shaded vs lit) via GPL198 probe→AGI → contrast
  (`scripts/17`). **Model v5 = 21 contrasts** (class tropism_photo). Hypergravity HELD (two-color);
  hydrotropism DROPPED (unreliable, per user).
- ☑ **Hypergravity** — GSE29787 LDC 2 g vs 1 g (`scripts/23`, GPL9020 probe→AGI) → **decoder_nes_matrix_v6
  = 22 contrasts** (class hypergravity, atlas family gravity). Lands on provascular/cotyledon programs.
- ☑ **5 more stressor families** (`scripts/24`) → **decoder_nes_matrix_v7 = 27 contrasts, 10 families**:
  desiccation (GSE76015 seed 21v15 DAF), osmotic (AtGenExpress GSE5622), ethylene (GSE193833 ACC),
  temperature (GSE303133 27v21°C), UV-B (GSE5626) — AGI-mapped (ATH1/GPL198 for AtGenExpress).
- ☑ **Bridge + atlas + F-set re-run on full v7** (`scripts/11/13/18/19/20`); within-source artifact
  joint 0.38 → 0.00. Atlas now 10 families → **columella/root cap 9/10 (top); radicle apical meristem 6/10;
  hypocotyl cortex + cotyledon mesophyll 6–7/10 (secondary)** — root tip remains the apex.
- ☐ (optional) plant fractional-gravity (EMCS); rehydration; cold; combined-stress

**5.4 DeepSpace seed-susceptibility atlas — ☑ v1 BUILT** (`scripts/18_deepspace_atlas.py`)
- Germ cell type × 5 stressor families + convergence count → `deepspace_seed_atlas.png`,
  `deepspace_atlas_{convergence,family,nes}.csv`, `results/deepspace_atlas_results.md`.
- **HEADLINE: YES — the radicle/root tip is the multi-stressor hotspot.** Radicle apical meristem = 4/5
  families (gravity, tropism, radiation, magnetic/NMF); columella/root-cap 4/5; radicle epidermis 3/5.
  Cotyledon mesophyll = main non-root hotspot (4/5). (Unassigned cl8/cl11 score high but soft.)
- ☑ **Atlas at tissue + stage level** (`scripts/19`): STAGE — **12 hsl (early germination) most
  multi-stressor: 4/5 families**; 24/48 hsl = 3. TISSUE (Gehring L1) diffuse/noisier (Ovule 4 but tiny
  maternal; Embryo 2) → cell-type × stage is the meaningful resolution. Fig `deepspace_atlas_tissue_stage.png`.
  Combined headline: **radicle/root-tip cell types at early germination (12 h) = the convergence hotspot.**
**5.2/5.3 Tools packaged — ☑** `tools/deepspace/` installable package:
- **DSRS** (`deepspace.dsrs.recognize`) — signature → which space stressor (validated: recognizes
  submergence as low_oxygen). **GSAD** (`deepspace.gsad.decode`) — bulk → seed cell-type susceptibility.
  Shared `projection.py`; `panels.py` (+GMT export); `cli.py` (`deepspace dsrs|gsad|export-gmt`);
  `pyproject.toml`, `tools/README.md`, `examples/`. Smoke-tested end-to-end.
**5.5 FAIR repo — ☑** LICENSE (MIT), CITATION.cff, .zenodo.json, .gitignore, REPRODUCE.md,
  `panels/panel_library.gmt` (interoperable). Data provenance in `data/data_inventory.csv`.
- ☑ **Figure overlap fixed** — atlas figs (18/19) use a dedicated colorbar axis (heatmap|cbar|bars).
**5.6 npj figure set F1–F6 — ☑ BUILT & POLISHED** (`scripts/20_manuscript_figures.py` → `report/figures_npj/`):
  - **F1** concept workflow (schematic: signature → DSRS/GSAD → atlas → radicle headline)
  - **F2** DSRS stress reference library (27 contrasts × seed programs; family labels rotated above strip)
  - **F3** seed reference + embryo-lineage validation (positive control)
  - **F4** GSAD stressor → germinating-seed cell-type susceptibility
  - **F5** DeepSpace seed-susceptibility atlas (headline; dedicated colorbar)
  - **F6** convergence model (schematic: radicle growth-point; 4 families + hypophysis origin + H1/H2)
  Consistent style (300 dpi, .png+.svg), no text/legend overlap.
- ☑ **npj manuscript** — `report/manuscript_npj_microgravity.{md,pdf,docx}` (renderers `scripts/21`/`22`,
  F1–F6 embedded; .docx **validated PASSED**): Abstract/Intro/Results(F1–F6)/Discussion/Methods/Data+Code
  availability/refs. Updated to 27 contrasts / 10 families. Headline = root tip is the convergence apex
  (columella/root cap 9/10 families). Author: Richard Barker (Purdue; Collaborative Science Environment, PBC).
- ☑ **Repo GitHub/Zenodo-ready** — committable footprint ~25 MB (data/raw 3.1 GB + data/processed 1.1 GB
  gitignored); no >5 MB stray files; LICENSE/CITATION.cff/.zenodo.json/.gitignore/REPRODUCE.md present; no
  .git yet (user runs git init + push + Zenodo).
- ☑ Author/affiliation set: **Richard Barker** — Purdue University; The Collaborative Science Environment,
  PBC (in manuscript .md/.docx/.pdf, CITATION.cff, .zenodo.json). docx builder now auto-patches w:zoom.
- ☑ **Pushed to GitHub** (private): github.com/dr-richard-barker/deepspace-seed-decoder.
- ☐ **Zenodo DOI** (user: cut a release → connect Zenodo → paste DOI into .zenodo.json/CITATION/manuscript);
  flip repo public at submission. *(only remaining repo step)*

---

## 5. Risks / watch-list
- ✔ RESOLVED — tropisms (gravitropism+phototropism integrated; hydro/thigmo dropped) and hypergravity
  (GSE29787 2 g, microarray-tier, labeled).
- **Mixed evidence tiers** — osmotic/UV/phototropism = ATH1 microarray; hypergravity = two-color/callus;
  desiccation = seed-maturation proxy; NMF = localization. All labeled; flagged in manuscript limitations.
- **Cross-stressor comparability** — heterogeneous platforms/doses/tissues; mitigated by rank-based
  projection + family-level convergence voting (one vote per family).
- **Cross-stage transfer is correlative** — kept inside the tier + falsification framework.
- **Stage mismatch** — Gehring atlas is *developmental* (3–7 DAP), NOT dry/germinating; the germination
  atlas (12/24/48 h) is the state axis; dry/0 h pole under-sampled.

---

## 6. Decisions resolved (2026-06-26)
- **Phase 1 NMF path = DO BOTH.** Reframe now as evidence synthesis (Maffei 194-gene panel anchor +
  GSE29787 labeled high-field contrast + qPCR literature) AND send the author request for the full
  Maffei array in parallel (draft: `report/maffei_data_request_email.md`). Upgrade Phase 1 if it arrives.
- **Compute = LOCAL.** This machine: 64 GB RAM (38 free), 164 GB free disk, Python 3.13. More than
  enough (heaviest object 3.9 GB). **Only gap: no R** — the Gehring GSE295007 atlas is Seurat `.rds`.
  Plan: install R+Seurat once to export annotated markers/pseudobulk → CSV/h5ad, then all decoder work
  in Python. (Alt: re-annotate raw matrices in scanpy — rejected, loses authors' labels.)

### Resolved
- Project path confirmed; R+Seurat installed; atlases downloaded; all built — see §8 audit.

---

## 8. Completion audit (2026-06-27)
- **Phase 0** data inventory + accessions — ✅ COMPLETE.
- **Phase 1** NMF meta-analysis — ◑ REFRAMED: genome-wide NMF not publicly deposited (audited GEO/SRA/
  BioProject/ArrayExpress; author request sent). Delivered NMF localization (→ radicle apical meristem,
  z +7.96). Upgrades to full GSEA when arrays arrive. *(externally blocked, not a loose end)*
- **Phase 2** seed reference — ✅ COMPLETE (122 panels, named germination clusters, marker-validated).
- **Phase 3** decoder + bridge + NMF + embryo-lineage — ✅ COMPLETE; bridge on full 22-contrast model;
  falsification H1–H6 + D/A/L/H tiers in report.
- **Phase 4** synthesis report — ✅ COMPLETE (12 pp). Reproducible notebooks superseded by numbered
  scripts 01–23 + `REPRODUCE.md`.
- **Phase 5** consolidation — ✅ tools (DSRS/GSAD, installable, validated), FAIR scaffold, atlas
  (cell-type/tissue/stage), F1–F6, manuscript (.md/.pdf/.docx), **pushed to GitHub**. **Stressor panel:
  27 contrasts / 10 families** — gravity (µg/partial/hypergravity), tropism (gravi/photo), low-oxygen
  (hypoxia/anoxia/submergence), desiccation, osmotic, ethylene, temperature, UV, radiation (GCR/low/acute),
  magnetic/NMF. (hydrotropism dropped — unreliable.)
- **Parked (external / user-side):** genome-wide NMF arrays (author reply); **Zenodo DOI** (user mints from
  a GitHub release → paste into `.zenodo.json`/`CITATION.cff`/manuscript); flip repo public at submission.
- **Done since:** desiccation/osmotic/ethylene/temperature/UV stressors (v7); dry/0 h pole anchored
  (bulk-tier `dry_seed` panel); npj cover letter (`report/cover_letter.md`); supplementary; smoke-test;
  public README + PLANNING split.
- **Optional / future:** plant fractional-gravity (EMCS Moon/Mars); cold; clinostat/RPM; combined-stress;
  single-cell dry-seed data (current dry anchor is bulk-tier); sog1/myb3r mechanistic radiation arm.

---

## 7. Changelog
- **2026-06-27 (ee)** — **Dry/0h pole anchored + repo polish (cover letter, public README, supplementary, smoke-test).**
  Added `germ_state_time::dry_seed` panel (GSE76015 mature dry seed 21 vs 15 DAP, 3 WT ecotypes; `scripts/26`)
  → re-ran full decoder chain → **decoder_nes_matrix_v7 now 123 panels × 27 contrasts**; state axis spans
  dry→12→24→48 h. Sanity: **desiccation INDUCES dry-seed program (+3.45), ethylene SUPPRESSES it (−1.40)**
  (dormancy logic). Stage atlas (`scripts/19`) includes dry_seed (7/10 families). Re-ran heatmap/atlas/F-set/
  report/manuscript. Cell-type headline stable: columella/root cap 9/10, radicle apical meristem 6/10.
  **Repo:** split long planning doc → `PLANNING.md` (this file) + concise public `README.md`; drafted
  `report/cover_letter.md`; built supplementary; ran reproducibility smoke-test.
- **2026-06-27 (dd)** — **2nd NMF localization panel (Maffei 2021 Sci Rep S7).** Pulled public 2021
  supplementary DEG lists (MOESM2.xlsx, per-timepoint NNMF) → `scripts/25` → undirected 2499-gene panel
  localized onto germinating-seed cell types. Result: localizes to **cotyledon mesophyll + hypocotyl
  cortex**, does NOT reproduce the 2022 radicle-apical-meristem signal (r=0.35) → radicle signal is
  **oxidative-panel-specific** (honest qualifier; added to manuscript §4.4). Caveat: workbook direction
  unreliable → undirected. Fig `nmf_localization_2021v2022.png`; note `results/nmf2021_results.md`.
  **README/Phase 1 now flags ⏳ AWAITING MAFFEI REPLY → upgrade to full GSEA arrays when the data link arrives.**
- **2026-06-27 (cc)** — **Added 5 stressor families → 27 contrasts / 10 families; full re-analysis +
  manuscript update.** desiccation (GSE76015), osmotic (GSE5622), ethylene (GSE193833), temperature
  (GSE303133), UV-B (GSE5626) via `scripts/24` → decoder_nes_matrix_v7. Re-ran heatmap/atlas (cell-type +
  tissue/stage)/bridge/F-set on v7 (10-family atlas). **Headline updated:** columella/root cap = 9/10
  families (top); radicle apical meristem 6/10; hypocotyl cortex + cotyledon mesophyll 6–7/10 secondary —
  root tip remains the convergence apex. Manuscript (.md/.pdf/.docx, validated) + phase4 report + captions
  updated to 27/10. osmotic/UV = AtGenExpress ATH1 (GPL198) microarray-tier; desiccation = seed-maturation proxy.
- **2026-06-27 (bb)** — **Hypergravity added (gravity axis complete) + full-model re-run + loose-ends audit.**
  GSE29787 LDC 2 g → `scripts/23` → decoder_nes_matrix_v6 (22 contrasts). Re-ran heatmap/atlas/tissue-stage/
  bridge/F-set + report + manuscript (.md/.pdf/.docx, validated) on v6; propagated "22 contrasts" + hypergravity
  into all text/captions. Bridge re-run on full model (within-source artifact 0.48→0.00). Atlas headline
  unchanged (radicle apical meristem 4/5 families). Added §8 completion audit. Local commits ready to push.
- **2026-06-27 (aa)** — Fixed combined-heatmap (Fig 0, `scripts/11`): class strip now aligns exactly with
  the heatmap x-axis (NES colorbar moved to its own gridspec column so it no longer squeezes the heatmap);
  class names rotated 45° and lifted above the strip; legend removed (redundant). Report re-rendered.
  **Local git commit done** (`git init` + commit; 137 files, ~25 MB, data/raw+processed excluded, no >5 MB
  files). **Push blocked: `gh` CLI not installed + no remote/credentials → user must create remote + push**
  (commands below). Zenodo metadata verified valid.
- **2026-06-27 (z)** — **Manuscript .docx (submission format) + repo readiness check.**
  `report/manuscript_npj_microgravity.docx` via `scripts/22` (python-docx, 6 figs embedded), validated
  PASSED (patched python-docx w:zoom quirk). Repo audited GitHub/Zenodo-ready: ~25 MB committable
  (data/raw+processed 4.2 GB gitignored), no stray >5 MB files, all FAIR files present, no .git yet.
- **2026-06-27 (y)** — **npj Microgravity manuscript drafted** (`report/manuscript_npj_microgravity.md` +
  `.pdf`, 7pp, F1–F6 embedded; renderer `scripts/21`). Full structure with abstract, results tied to F1–F6,
  methods, data/code availability (all accessions + Zenodo placeholder), selected refs, falsification H1/H2.
  Headline: radicle growth-point = deep-space multi-stressor convergence hotspot. TODO: authors/affiliations,
  .docx for submission, outward git/Zenodo.
- **2026-06-27 (x)** — **npj figure set F1–F6 built & polished** (`scripts/20` → `report/figures_npj/`):
  F1 concept workflow + F6 convergence model (new schematics), F2 stress library, F4 GSAD susceptibility
  (re-rendered, dedicated colorbar + title/legend de-collided), F3 embryo-lineage + F5 atlas (clean, brought
  in). Consistent 300-dpi png+svg, no overlap. Remaining: npj manuscript draft + outward FAIR (git/Zenodo).
- **2026-06-27 (w)** — **Tools packaged + FAIR repo + figure-overlap fix.** Built installable
  `tools/deepspace` package: **DSRS** (stress recognition; validated self-recognition of submergence→
  low_oxygen) + **GSAD** (bulk→seed susceptibility) + shared projection engine + CLI + GMT export +
  pyproject + README + example; smoke-tested. FAIR scaffold: LICENSE/CITATION.cff/.zenodo.json/.gitignore/
  REPRODUCE.md + panel_library.gmt. **Fixed colorbar-overlaps-barplot** in atlas figs (18/19) via dedicated
  colorbar axis (heatmap|cbar|bars); report re-rendered. Next: full F1–F6 polish + F1 concept diagram.
- **2026-06-27 (v)** — **Atlas extended to tissue + stage level** (`scripts/19`). STAGE: 12 hsl (early
  germination) = most multi-stressor (4/5 families); TISSUE (Gehring L1): diffuse/noisier, Ovule top but
  tiny maternal (flagged). Combined headline: radicle/root-tip cell types at early germination (12 h) =
  DeepSpace convergence hotspot. Fig `deepspace_atlas_tissue_stage.png`; note appended to
  `results/deepspace_atlas_results.md`.
- **2026-06-27 (u)** — **Phototropism added** (GSE3847 ATH1 shaded-vs-lit, GPL198 probe→AGI) → v5 = 21
  contrasts; hydrotropism DROPPED (user: unreliable), hypergravity HELD. **DeepSpace seed-susceptibility
  ATLAS v1 built** (`scripts/18`): germ cell type × 5 stressor families + convergence. **HEADLINE: radicle
  apical meristem hit by 4/5 families (gravity, tropism, radiation, magnetic/NMF); root-tip region
  (meristem+columella+epidermis) is the top multi-stressor hotspot** → answers the radicle question YES.
  `deepspace_seed_atlas.png` + `results/deepspace_atlas_results.md`.
- **2026-06-27 (t)** — **Gravitropism added** (GSE199142 gravistimulation RNA-seq, Col-0 12h+24h vs Ref) →
  `scripts/16` → **decoder_nes_matrix_v4 (20 contrasts)**, class `tropism_gravi`. gravitropism_12h →
  radicle apical meristem (+1.54) — reinforces radicle convergence. Combined heatmap → v4. **OSD-758/GLDS-664
  REJECTED (mouse, not Arabidopsis — caught by organism check).** Remaining requested stressors are
  microarray/panel-tier: phototropism (GSE3847 ATH1, doable), hypergravity (GSE29787 2g two-color, heavy),
  hydrotropism (no transcriptome → tiny MIZ1 panel). Inventory updated.
- **2026-06-27 (s)** — **Phase 5.1 low-oxygen stressors added.** hypoxia (1% O2) + anoxia (0% O2) from
  GSE315308 O2-gradient (Entrez→TAIR via new `entrez_to_tair.csv`) + submergence from GSE182724 ('Sub vs.
  Air', AGI+Log2FC). `scripts/15_oxygen_stressors.py` → **decoder_nes_matrix_v3 (18 contrasts)**, class
  `low_oxygen`. Combined heatmap refreshed (script 11 → v3). Hypoxia/anoxia induce embryo+12h programs
  (consistent with cross-stressor 12h attractor). Inventory updated. NEXT: hypergravity (OSDR) + gravitropism.
- **2026-06-27 (r)** — **MAJOR replan → consolidation for npj Microgravity.** New vision (§1A): distill
  into 2 FAIR tools (**DSRS** stress-recognition + **GSAD** germinating-seed autodecoder) + a **DeepSpace
  seed-susceptibility atlas** (which seed cell types/stages respond to which space stressors; radicle-tip
  multi-stressor hypothesis). Added Phase 5 (data expansion: hypoxia/anoxia/hypergravity/tropisms +
  suggestions; tool packaging; atlas; FAIR GitHub+Zenodo; figures; manuscript). Scouted candidate data:
  hypoxia 19 / anoxia 21 GEO RNA-seq (ample); hypergravity 0 GEO RNA-seq (OSDR/microarray); tropisms sparse
  (flagged). Title/scope updated; original NMF+decoder work preserved as Tool-2 core.
- **2026-06-27 (q)** — **Embryo-lineage-only dev bridge** (`scripts/14_bridge_embryo_lineage.py`):
  restricted dev side to Gehring embryo cells (5683), pseudobulked by embryo level_3 state, mapped onto
  germinating cell types. **Recovers TEXTBOOK lineages** (protoderm→epidermis, hypophysis→radicle apical
  meristem z+2.14, vascular primordium→provasculature, inner cotyledon→cotyledon mesophyll, cortical
  initials→hypocotyl cortex) = positive control validating the pipeline. Reinforces radicle convergence
  (hypophysis founds the radicle meristem). Outputs `embryo_lineage_map.csv`, `embryo_lineage_heatmap.png`,
  `results/embryo_lineage_results.md`. Report→11pp (new §4.3b + Fig 3c + exec bullet 4b).
- **2026-06-27 (p)** — **Bridge refinement v3 (within-source scaling)** = CANONICAL bridge
  (`scripts/13_bridge_refine.py`). Z-scores each germ axis within source (dev/stress) → removes score-type
  artifact: **PC1↔source |corr| 0.56→0.00**. Now interpretable: Embryo 3DAP→hypocotyl cortex early,
  5DAP→mid (dev progression). Outputs `bridge_*_v3.*`, `results/bridge_results_v3.md`. Report→11pp.
  Honesty: perturbation→cell-type argmax is scaling-sensitive (suggestive); robust magnetic→seed signal =
  NMF→radicle apical meristem localization (z+7.96, scaling-independent).
- **2026-06-27 (o)** — **Bridge extended to v2** (`scripts/12_bridge_latent_v2.py`): all 15 perturbation
  contrasts (microgravity + radiation) + late-seed-dev co-embedded in germinating-seed score space
  (27 inputs). Outputs `bridge_{latent,assignments}_v2.csv`, `bridge_{heatmap,embedding}_v2.*`,
  `results/bridge_results_v2.md`; cached `gehring_dev_pseudobulk.csv`. Convergence: µg-root-dark →
  radicle apical meristem (aligns w/ NMF localization); radiation → root-pole/provascular. Report → 10pp.
  Caveat: embedding PC1 = dev(ssGSEA) vs stress(NES) score-type artifact; use per-axis assignments.
- **2026-06-27 (n)** — **Radiation/ROS perturbations integrated.** Parsed user table
  `radiation_and_ros_cleaned.csv` (158 samples, OSD_IDs+GSMs) → pulled 5 OSDR RNA-seq DGE tables
  (GLDS-498/502/508/510/679) → 9 WT irradiated-vs-control contrasts via GSEA-prerank → merged into
  **combined 15-contrast model** (`decoder_nes_matrix_v2.csv`; classes: microgravity×4, GCR×2, low-dose
  γ×2, acute 100Gy γ×7). Scripts 10–11; figure `decoder_combined_perturbation_heatmap.png`; note
  `results/radiation_results_v1.md`. Report refreshed to 9pp. Finding: acute γ (90min) induces embryo+12h
  programs (converges with µg/GCR "12h attractor"); 100Gy = mechanistic DNA-damage dose, cGy studies =
  space-relevant. sog1-1/myb3r1 mutant arms available for follow-up.
- **2026-06-26 (m)** — Verified PRJEB65433 = **WGS/genomic** (not transcriptome) → EXCLUDED from decoder
  (genotoxicity context only). Finalized Maffei author-request email as **send-ready** (verified contact
  massimo.maffei@unito.it + corrected 2021 citation Sci Rep 11:9195). Email = `report/maffei_data_request_email.md`
  (user must send; Claude cannot email). This is the only route to genome-wide NMF.
- **2026-06-26 (l)** — **Comprehensive repository sweep** (GEO/SRA/BioProject/ArrayExpress, all magnetic
  terminologies). Confirmed ZERO deposited null/hypomagnetic Arabidopsis transcriptomes; "magnetic" =
  mostly magnetic-bead prep noise. New high-field comparator found: ENA **PRJEB65433** (33 T on dried
  seeds, "DNA stability" — verify data type). Null-field genome-wide remains the 2 undeposited Maffei
  arrays only. Logged in `data/data_inventory.csv` (search-completeness row) + `notes/phase0_feasibility.md`.
- **2026-06-26 (k)** — **Phase 4 synthesis report** built: `report/phase4_synthesis_report.{md,pdf}`
  (8 pages) integrating decoder + bridge + NMF localization with D/A/L/H evidence tiers, an integrated
  model, limitations, and 6 falsification hypotheses (H1/H2 High confidence). Renderer
  `scripts/09_build_report_pdf.py`. Project Phases 0–4 now complete end-to-end (NMF arm pending
  genome-wide data).
- **2026-06-26 (j)** — (c) **NMF wired in** via expression-localization (`scripts/08_nmf_localization.py`):
  NMF-up genes localize to radicle apical meristem (z +7.96). Also a deeper NNMF dataset sweep (user
  prompt): confirmed BOTH Maffei arrays (2022 NNMF time-course PMC9775259 + 2021 dose-response PMC8080623,
  incl. 240/40 nT near-null) are NOT deposited ("supp tables + on request"); added both to inventory +
  author-request email; logged 2014 human-cell hypomagnetic transcriptome (cross-species) and confirmed
  2018 root-mineral paper is qPCR/ionomics only. Updated `notes/phase0_feasibility.md`.
- **2026-06-26 (i)** — **Layer-2 shared latent (bridge) built**. `scripts/07_bridge_latent.py` placed
  adult-stress (decoder NES) + late-seed-dev (Gehring tissue×timepoint ssGSEA) into one germinating-seed
  score space. Outputs + `results/bridge_results_v1.md`. Finding: dev→germination bridge weak & embryo-
  lineage-limited (maternal/endosperm terminal); stress→germ mappings strong. Noted scale-artifact +
  refinement TODOs.
- **2026-06-26 (h)** — Labeled germination clusters from paper open-access full text (PMC11410669);
  cross-checked with own markers (3/6/15 confirmed). Wrote `panels/germination_cluster_annotations.csv`,
  `panels/panel_library_annotated.csv`, `scripts/06_annotate_and_replot.py`, and named figure
  `results/figures/decoder_germination_named_heatmap.{png,svg}`. Decoder germ rows now read as cell types.
- **2026-06-26 (g)** — **Phase 3 decoder v1 (end-to-end)**. Found gene-level DE absent from Biomni repo
  (only pathway aggregates) → pulled genome-wide OSD DGE from NASA OSDR (GLDS-120/612/603). Built
  GSEA-prerank projection of 6 µg/GCR contrasts onto 122 seed panels. Coherent result (12hsl induced;
  GCR-80→embryo/provascular; proliferative states suppressed; light-dependence; matches repo vascular
  theme). Figures + tables + `results/decoder_results_v1.md` written. NMF column deferred to genome-wide
  data (194-gene panel too small). Next: label germ clusters, add NMF when available, learned latent.
- **2026-06-26 (f)** — Phase 2 milestone: **panel library built + validated**. Exported Gehring
  counts.mtx (23374×54210, 43 modscore cols), ran `scripts/03_build_panels.py` → `panels/panel_library.csv`
  (6100 rows, 122 panels). Bio sanity check passed (OLE/CRA/2S in Embryo; BAN in ii1). Next: (a) get
  germination cluster→cell-type names from paper Table S, (b) Phase 2 shared latent / pseudobulk
  co-embedding, then (c) Phase 3 decoder (singscore/ssGSEA projection of NMF+OSD signatures onto panels).
- **2026-06-26 (e)** — Phase 2 kickoff. Installed Python sci stack + R 4.6.0 + SeuratObject (user lib).
  Downloaded Gehring atlas (1.3 GB .rds). Found ArrayExpress E-MTAB-12532 has NO matrix → switched
  germination matrix source to **GEO mirror GSE182331** (expression_mat 13501×12798, +meta cluster/time).
  Wrote `scripts/01_inspect_gehring.R` (running). Next: read inspection → export Gehring counts+labels →
  build marker panels for both atlases. TODO: get germination cluster→cell-type name map from paper Table.
- **2026-06-26 (d)** — User flagged Jin et al. 2019 SMF paper (s41598-019-50970-y). Resolved → SRA
  **PRJNA529956** (no GEO series). Classified as HIGH static-field (600 mT) comparator, NOT core NMF, but
  added because it's a rare public genome-wide magnetic transcriptome overlapping the repo's
  auxin/polyphenol axes. Added to inventory (+ optional 2021 sibling). Caveat logged: verify N0/N180 =
  orientation not null; raw FASTQ needs reprocessing.
- **2026-06-26 (c)** — Decisions: Phase 1 = do-both (reframe + author request); compute = local
  (64 GB RAM, Python 3.13; gap = no R for Gehring .rds). Staged parallel paths: drafted
  `report/maffei_data_request_email.md`, `data/download_manifest.md`, `requirements.txt`. Checked atlas
  footprints (GSE295007 merged atlas 1.3 GB; full ~10 GB). Next (on go-ahead): install R+Seurat, pull
  the two atlases, begin Phase 2 marker-panel extraction.
- **2026-06-26 (b)** — Phase 0 accession resolution done. Resolved GSE295007 (Gehring dev),
  E-MTAB-12532/12521/13449 (germination), OSD-120/678/658 (bridge inputs). Wrote
  `data/data_inventory.csv` + `notes/phase0_feasibility.md`. **Key finding:** genome-wide NNMF data is
  not publicly deposited (Maffei array undeposited → only 194-gene supplement; GSE29787 is high-field).
  Phase 1 now needs a path decision (Open Q1). Next: user picks Phase 1 path + compute, then start
  Phase 2 atlas downloads (unblocked).
- **2026-06-26 (a)** — Project created. Repo + both papers + NMF landscape assessed. Three scoping
  decisions locked (bridge input / both atlases / standalone). Scaffold + this living README written.
