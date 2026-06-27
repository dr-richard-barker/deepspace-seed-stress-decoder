# Phase 0 — Feasibility note (2026-06-26)

Accession resolution complete. Headline: **the seed-atlas side is strong; the genome-wide NMF side is
the binding constraint.**

## Resolved accessions
- **Gehring developmental seed atlas** → GEO **GSE295007** (snRNA-seq, 3/5/7 DAP; embryo/endosperm/seed
  coat). Public, multi-replicate. Confirmed via NCBI esummary (title matches DOI 10.1038/s41477-026-02295-8).
- **Germination atlas** → ArrayExpress **E-MTAB-12532** (scRNA-seq) + **E-MTAB-12521** (bulk
  protoplasting controls) + **E-MTAB-13449** (TF-mutant RNA-seq). Public.
- **Bridge inputs** → NASA OSDR **OSD-120 / OSD-678 / OSD-658** (already characterized in Biomni repo).

## The NMF constraint (important, decision-forcing)
- **TWO Maffei/Agliassa NNMF microarray studies exist** (verified by reading both data-availability
  statements — both say *"data are available as supplementary tables and further data can be provided
  upon request"*, i.e. **NO GEO/ArrayExpress/BioStudies deposit** for either):
  - **2022 Biomolecules** (PMC9775259) — NNMF single-condition time-course (10 min–96 h), Agilent 4×44K
    2-color. Public artifact = 194-gene oxidative supplement (already in Biomni repo).
  - **2021 Sci Rep "Differential root and shoot magnetoresponses"** (PMC8080623) — magnetic **dose-
    response** from **240 nT / 40 nT (near-null)** through 41 µT (GMF) to ~60 µT, root & shoot. This is
    the **best author-request target** (a gradient including the null end). NEW this sweep.
  - Confirmed NOT in GEO (author "Agliassa" = 0 hits) or ArrayExpress (magnetoresponse search = unrelated).
  - The full arrays for BOTH require an **author data request** (email updated to ask for both).
- Cross-species: a **hypomagnetic-field transcriptome in human neuroblastoma** (Sci China Life Sci 2014,
  doi 10.1007/s11427-014-4644-z) exists — optional cross-kingdom comparator only.
- The 2018 "root mineral nutrition" NNMF paper (ScienceDirect S2214552418300671) = ionomics + qPCR,
  **not genome-wide** → literature support only.
- **Paul & Ferl callus (GSE29787)** is public BUT uses a **strong-gradient superconducting magnet**
  (variable-g) — that is a **HIGH-field perturbation, the opposite of null/hypomagnetic**. Per our
  exclusion rule it is **not an NMF dataset**; usable only as a clearly-labeled magnetic *comparator*.
- Remaining hypomagnetic literature (flowering 2018, lipid/nutrient) is **qPCR-only** → not usable for
  genome-wide meta-analysis.

### Repository search completeness (comprehensive sweep 2026-06-26)
Swept **GEO (gds), SRA, BioProject, and ArrayExpress/BioStudies** with all relevant terms (near-null,
hypomagnetic, geomagnetic, magnetic field exposure, magnetoreception, weak magnetic field):
- **ZERO deposited null/near-null/hypomagnetic Arabidopsis transcriptomes** in any repository.
- The bare term "magnetic" is dominated by **magnetic-bead RNA-prep** noise (NEBNext/MagJET/Dynabead),
  not field exposure — must be filtered out.
- **All deposited magnetic-FIELD Arabidopsis datasets are HIGH-field comparators**, not null:
  - GEO **GSE29787** — callus, diamagnetic levitation 10–16.5 T (Paul/Ferl).
  - SRA **PRJNA529956** — Jin 2019 SMF 600 mT (root/auxin).
  - ENA **PRJEB65433** — *ultra-high 33 T on DRIED seeds*, "DNA stability" (likely DNA/structural, not
    RNA-seq → verify data type; on-target dry-seed tissue but extreme field).
- Therefore genome-wide **null-field** data = ONLY the two undeposited Maffei arrays (2021 + 2022) +
  the public 194-gene supplement. The author request remains the only route to genome-wide NMF.

### Consequence for Phase 1
A genome-wide NMF *meta-analysis* across many studies is **not currently supported by public data**.
Realistic options to put to the user:
1. **Author request** for the full Maffei NNMF array (best path to genome-wide NMF). 
2. **Reframe Phase 1** around the 194-gene NNMF panel as the anchor + GSE29787 as a labeled high-field
   contrast + qPCR literature as directional support — honest "evidence-synthesis" rather than
   genome-wide meta-analysis.
3. **Broaden taxonomically** (hypomagnetic transcriptomes in other species / cell systems) if
   cross-species inference is acceptable.

The **decoder (Phases 2–3) is unaffected** — both seed atlases are fully public and downloadable.

## Next decisions for the user
- Pick a Phase 1 path (1/2/3 above).
- Confirm compute env for atlas-scale snRNA `h5ad` downloads (Phase 2).
