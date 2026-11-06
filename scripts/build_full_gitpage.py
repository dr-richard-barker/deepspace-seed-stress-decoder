#!/usr/bin/env python3
"""
Build the integrated GitHub Pages site (docs/index.md and docs/manuscript/index.md)
so that the complete npj Microgravity manuscript can be read directly on the gitpage,
as well as via the dedicated /manuscript route.

Ensures zero raw LaTeX math or unrendered escaping syntax throughout.
"""

from pathlib import Path

MANUSCRIPT_SOURCE = Path("report/manuscript_npj_microgravity.md")
DOCS_INDEX = Path("docs/index.md")
DOCS_MANUSCRIPT_DIR = Path("docs/manuscript")
DOCS_MANUSCRIPT_INDEX = DOCS_MANUSCRIPT_DIR / "index.md"

PDF_VIEWER_BLOCK = """
<div id="pdf-viewer" class="pdf-viewer-card" style="margin: 2rem 0; border: 1px solid var(--line, #22304f); border-radius: 8px; overflow: hidden; background: #0c1226;">
  <div class="pdf-toolbar" style="padding: 12px 18px; background: #111a33; border-bottom: 1px solid var(--line, #22304f); display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px;">
    <div style="display: flex; align-items: center; gap: 8px;">
      <span style="font-size: 1.1rem;">📄</span>
      <strong style="color: #eef2fb; font-size: 0.95rem;">npj Microgravity Interactive Article Viewer</strong>
      <span style="font-size: 0.75rem; padding: 2px 8px; border-radius: 4px; background: #1c4a72; color: #6ea8ff; font-weight: 600;">300 DPI Publication PDF</span>
    </div>
    <div style="display: flex; gap: 8px; flex-wrap: wrap;">
      <a href="{{ '/assets/manuscript_npj_microgravity.pdf' | relative_url }}" target="_blank" class="btn btn-sm" style="font-size: 0.8rem; padding: 5px 12px;">Open Fullscreen ↗</a>
      <a href="{{ '/assets/manuscript_npj_microgravity.pdf' | relative_url }}" download class="btn btn-sm primary" style="font-size: 0.8rem; padding: 5px 12px;">Download PDF ↓</a>
      <a href="{{ '/assets/manuscript_npj_microgravity.docx' | relative_url }}" download class="btn btn-sm" style="font-size: 0.8rem; padding: 5px 12px;">Download Word (.docx) ↓</a>
    </div>
  </div>
  <div class="pdf-frame-wrapper" style="position: relative; width: 100%; height: 860px; min-height: 500px; background: #1a2236;">
    <object data="{{ '/assets/manuscript_npj_microgravity.pdf' | relative_url }}" type="application/pdf" width="100%" height="100%">
      <iframe src="{{ '/assets/manuscript_npj_microgravity.pdf' | relative_url }}" width="100%" height="100%" style="border: none;">
        <div style="padding: 30px; text-align: center; color: #a7b2cf;">
          <p style="font-size: 1.1rem; margin-bottom: 15px;">Your browser does not support embedded PDF viewing.</p>
          <a href="{{ '/assets/manuscript_npj_microgravity.pdf' | relative_url }}" class="btn primary">Download the Publication PDF (3.0 MB)</a>
        </div>
      </iframe>
    </object>
  </div>
</div>
"""

FIGURE_CARDS = {
    "### A dual-tool architecture for multi-stimuli space decoding (Fig. 1)": (
        "\n\n![Figure 1: Concept workflow]({{ '/assets/figures/F1_concept_workflow.png' | relative_url }})\n\n"
        "*Figure 1 — Concept workflow. A single query transcriptomic signature drives the dual-engine architecture: "
        "DSRS recognizes the space stressor class across 49 contrasts and 15 families, while GSAD projects the query "
        "across 123 single-cell seed panels. [[High-Res Vector SVG]({{ '/assets/figures/F1_concept_workflow.svg' | relative_url }})]*\n"
    ),
    "### Positive control: Ground-truth embryo lineage recovery (Fig. 3)": (
        "\n\n![Figure 3: Seed reference and embryo-lineage validation]({{ '/assets/figures/F3_seed_reference_embryo_lineage.png' | relative_url }})\n\n"
        "*Figure 3 — Validated single-cell seed reference. Unbiased embryo lineage tracing independently recovers ground-truth "
        "developmental origins (protoderm → epidermis; hypophysis → radicle apical meristem; vascular primordium → provasculature), "
        "confirming that cross-stage projection captures authentic biological programs. [[High-Res Vector SVG]({{ '/assets/figures/F3_seed_reference_embryo_lineage.svg' | relative_url }})]*\n"
    ),
    "### Assembly of the 49-contrast, 15-family master stress library (Fig. 2)": (
        "\n\n![Figure 2: DSRS stress library fingerprints]({{ '/assets/figures/F2_stress_library.png' | relative_url }})\n\n"
        "*Figure 2 — DSRS stress-recognition library. Distinct enrichment fingerprints across the 123 seed panels provide the diagnostic basis "
        "for identifying space stressor classes and families. [[High-Res Vector SVG]({{ '/assets/figures/F2_stress_library.svg' | relative_url }})]*\n"
    ),
    "### Decoupling total pressure from hypoxia in seed cell types (Fig. 4)": (
        "\n\n![Figure 4: GSAD susceptibility matrix]({{ '/assets/figures/F4_gsad_susceptibility.png' | relative_url }})\n\n"
        "*Figure 4 — GSAD susceptibility matrix across seed cell types. Unbiased single-cell susceptibility profiles across the 15 "
        "germinating clusters for 49 deep-space and environmental perturbations. [[High-Res Vector SVG]({{ '/assets/figures/F4_gsad_susceptibility.svg' | relative_url }})]*\n"
    ),
    "### The DeepSpace Seed-Susceptibility Atlas v8: The root tip convergence apex (Fig. 5)": (
        "\n\n![Figure 5: DeepSpace Seed-Susceptibility Atlas v8]({{ '/assets/figures/F5_deepspace_atlas.png' | relative_url }})\n\n"
        "*Figure 5 — The DeepSpace Seed-Susceptibility Atlas v8. Rows display 15 germinating-seed cell types; columns display 15 stressor families. "
        "Asterisks denote statistical significance (|NES| ≥ 1.5, FDR < 0.25; NMF |z| ≥ 2.0). The right-hand convergence bar chart establishes the "
        "columella/root cap (14/15) and radicle apical meristem (10/15) as the multi-stressor convergence apex. [[High-Res Vector SVG]({{ '/assets/figures/F5_deepspace_atlas.svg' | relative_url }})]*\n"
    ),
    "### Multi-stressor convergence model and falsification hypotheses (Fig. 6)": (
        "\n\n![Figure 6: Convergence model and falsification tests]({{ '/assets/figures/F6_convergence_model.png' | relative_url }})\n\n"
        "*Figure 6 — Mechanistic convergence model & falsification hypotheses. Seven physical and chemical vectors converge upon the "
        "radicle growth point. Hypotheses H1–H4 formulate explicit, falsifiable experimental tests for near-null magnetic fields, normoxic hypobaria, "
        "and oxidative cascades. [[High-Res Vector SVG]({{ '/assets/figures/F6_convergence_model.svg' | relative_url }})]*\n"
    ),
}

TABLE_STRESS_LIBRARY = """
| Stressor Family | Contrasts (*N*) | Representative Conditions | Key Sources |
|---|:---:|---|---|
| **Gravity** | 5 | Spaceflight microgravity (root & leaf, light & dark) + 2 g hypergravity | NASA OSD-120, OSD-678; GSE29787 |
| **Radiation** | 9 | GCR-relevant low-dose (40, 80 cGy), acute γ time-course (100 Gy Co-60), low-dose Cs-137 (10, 100 cGy) | NASA OSD-658, OSD-498/502/508/510, OSD-782 |
| **Exploration Atmosphere** | 6 | Pure hypobaria, pure hypoxia, NASA exploration atmosphere (50 kPa NormO₂, 50 kPa HypoO₂) | TabPFN v2 framework; 130 microarrays |
| **Redox / ROS** | 2 | Continuous CVAE spaceflight ROS latent shift (log₂ error ratio), H₂O₂ oxidative stress | Redox_decoder (232 studies, 38 missions); MASTA |
| **Cold** | 2 | Cold shock time-course (4 °C at 3 h and 24 h) | MASTA / AtGenExpress |
| **Wounding** | 1 | Mechanical leaf/tissue damage (1.5 h) | MASTA / AtGenExpress |
| **Auxin** | 1 | Indole-3-acetic acid (IAA, 1 µM for 3 h) | MASTA / AtGenExpress |
| **Gibberellin** | 1 | GA₃ stimulation (1 h) | MASTA / AtGenExpress |
| **Cytokinin** | 1 | Zeatin stimulation (1 h) | MASTA / AtGenExpress |
| **Brassinosteroid** | 1 | Brassinolide (BL, 10 nM for 3 h) | MASTA / AtGenExpress |
| **Nutrient Stress** | 2 | Nitrogen starvation, Phosphorus starvation | MASTA / AtGenExpress |
| **Tropism** | 4 | Gravitropic reorientation time-course, phototropism auxin gradient | GSE199142, GSE3847 |
| **Low-Oxygen** | 8 | Hypoxia, anoxia, complete submergence | GSE315308, GSE182724 |
| **Desiccation** | 2 | Seed maturation drying (21 vs 15 DAF) | GSE76015 |
| **Osmotic / Salt** | 2 | Mannitol osmotic stress, drought stress | GSE5622, MASTA |
| **Ethylene** | 1 | ACC precursor (4 h vs 0 h) | GSE193833 |
| **UV** | 1 | UV-B irradiation vs control | GSE5626 |
| **Magnetic / Null Field** | 1 | Near-null magnetic field (< 30 nT NMF) curated panel | Parmagnani/Maffei 2022; Agliassa/Maffei 2021 |
"""

TABLE_CONVERGENCE = """
| Single-Cell Cluster / Cell Type | Organ / Tissue Zone | Significant Families (*N* / 15) | Convergence Percentage | Primary Spaceflight Targets |
|---|---|:---:|:---:|---|
| **Columella / Root Cap (+QC) (cl4)** | Radicle (Root Pole) | **14 / 15** | **93.3%** | Gravity, radiation, hypobaria, redox, hypoxia, cold, wounding, hormones, nutrients, UV |
| **Cotyledon Mesophyll (cl13)** | Cotyledon | **13 / 15** | **86.7%** | Radiation, hypobaria, redox ROS, nutrients, cold, wounding, osmotic |
| **Hypocotyl Cortex (cl5)** | Hypocotyl | **11 / 15** | **73.3%** | Radiation, hypobaria, hypoxia, redox, cold, wounding, hormones |
| **Hypocotyl Cortex (cl7)** | Hypocotyl | **11 / 15** | **73.3%** | Gravity, radiation, hypobaria, redox, cold, wounding, osmotic |
| **Radicle Apical Meristem (cl14)** | Radicle (Root Growth Center) | **10 / 15** | **66.7%** | Near-null magnetic field (*z* = +7.96), microgravity, pure hypobaria (NES = +1.98), wounding |
| **Cotyledon Mesophyll (cl3)** | Cotyledon | **10 / 15** | **66.7%** | Radiation, hypobaria, redox ROS, cold, wounding, desiccation |
| **Hypocotyl Cortex (cl1)** | Hypocotyl | **10 / 15** | **66.7%** | Gravity, radiation, hypobaria, redox ROS, desiccation, cold, wounding |
| **Provasculature (cl12)** | Vascular Stele | **9 / 15** | **60.0%** | Radiation, hypobaria, redox ROS, nutrients, wounding, osmotic |
| **Radicle Epidermis (cl10)** | Radicle (Root Surface) | **8 / 15** | **53.3%** | Gravity, radiation, hypobaria, redox ROS, cold, wounding |
| **Protophloem (cl15)** | Vascular Stele | **8 / 15** | **53.3%** | Radiation, hypobaria, redox ROS, nutrients, cold, wounding |
| **Protoxylem (cl9)** | Vascular Stele | **7 / 15** | **46.7%** | Radiation, hypobaria, redox ROS, nutrients, cold |
| **Cortex / Endodermis (cl2)** | Hypocotyl | **7 / 15** | **46.7%** | Radiation, hypobaria, redox ROS, cold, wounding |
| **Epidermis (cl6)** | Hypocotyl Surface | **7 / 15** | **46.7%** | Radiation, hypobaria, redox ROS, cold, wounding |
"""

def prepare_manuscript_body(raw_text: str) -> str:
    lines = raw_text.splitlines()
    body_lines = []
    in_body = False
    for line in lines:
        if line.startswith("## Abstract"):
            in_body = True
        if in_body:
            body_lines.append(line)

    body_text = "\n".join(body_lines)

    # Insert figures
    for section_header, fig_markup in FIGURE_CARDS.items():
        if section_header in body_text:
            body_text = body_text.replace(section_header, section_header + fig_markup)

    # Insert tables
    if "### Assembly of the 49-contrast, 15-family master stress library (Fig. 2)" in body_text:
        body_text = body_text.replace(
            "### Assembly of the 49-contrast, 15-family master stress library (Fig. 2)",
            "### Assembly of the 49-contrast, 15-family master stress library (Fig. 2)\n" + TABLE_STRESS_LIBRARY
        )

    if "### The DeepSpace Seed-Susceptibility Atlas v8: The root tip convergence apex (Fig. 5)" in body_text:
        body_text = body_text.replace(
            "### The DeepSpace Seed-Susceptibility Atlas v8: The root tip convergence apex (Fig. 5)",
            "### The DeepSpace Seed-Susceptibility Atlas v8: The root tip convergence apex (Fig. 5)\n" + TABLE_CONVERGENCE
        )

    return body_text

def build_index():
    raw_manuscript = MANUSCRIPT_SOURCE.read_text(encoding="utf-8")
    manuscript_body = prepare_manuscript_body(raw_manuscript)

    index_content = f"""---
layout: cose
title: DeepSpace Seed-Stress Decoder
description: A cell-type-resolved atlas of deep-space stress susceptibility in the dry and germinating Arabidopsis seed. Two FAIR tools (DSRS + GSAD) and a 49-contrast multi-stimuli space atlas.
---

_Which seed cell types and developmental stages are susceptible to deep-space stressors?_

Welcome to the **DeepSpace Seed-Stress Decoder** portal. Here you can explore the complete research manuscript targeted at *npj Microgravity*, interrogate the **49-contrast, 15-family** space stress library, and access the **DSRS** and **GSAD** computational tools.

[Read Interactive PDF Below](#pdf-viewer){{: .btn .btn-primary}}
[Read Full Web Article](#manuscript-full-text){{: .btn}}
[Download PDF (300 DPI)]({{{{ '/assets/manuscript_npj_microgravity.pdf' | relative_url }}}}){{: .btn}}
[Download Word DOCX]({{{{ '/assets/manuscript_npj_microgravity.docx' | relative_url }}}}){{: .btn}}
[Stimuli Decoders Synthesis]({{{{ '/stimuli_decoders_synthesis' | relative_url }}}}){{: .btn}}
[Dedicated Article Route]({{{{ '/manuscript/' | relative_url }}}}){{: .btn}}
[GitHub Code & Data](https://github.com/dr-richard-barker/deepspace-seed-stress-decoder){{: .btn}}

| 49 contrasts | 15 stressor families | 123 seed panels | 14 / 15 families hit the root cap | Target: npj Microgravity |
|:---:|:---:|:---:|:---:|:---:|

---

## Interactive Software Quickstart

The `deepspace` package provides command-line tools and a Python API to project any bulk transcriptomic signature onto the single-cell seed atlas.

| Tool / Command | Function | Core Question |
|---|---|---|
| **DSRS** (`deepspace dsrs`) | DeepSpace Stress-Recognition System: ranks query similarity against the 49-contrast reference library across 15 families. | _"Which space stressor or environmental perturbation does this signature resemble?"_ |
| **GSAD** (`deepspace gsad`) | Germinating-Seed AutoDecoder: projects query log₂FC onto 123 single-cell seed panels to predict cell-type and stage vulnerability. | _"What does this perturbation do to the dormant and germinating seed?"_ |
| **MASTA Project** (`deepspace masta-project`) | Directly extract and project any of the 592 MASTA benchmark contrasts onto the seed atlas. | _"How does an empirical ground-truth stressor affect the seed?"_ |
| **MASTA List** (`deepspace masta-list`) | Search and browse the 592 MASTA microarray contrast identifiers. | _"What empirical contrasts are available in the compendium?"_ |

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

---

## npj Microgravity Interactive Article Viewer

Read the camera-ready, publication-formatted manuscript with all 6 figures and tables integrated in-line below, or proceed to the full-text responsive web version.

{PDF_VIEWER_BLOCK}

---

<div id="manuscript-full-text"></div>

# A cell-type-resolved atlas of deep-space stress susceptibility in the dry and germinating Arabidopsis seed

**Richard Barker**¹ ² (ORCID: [0000-0001-5681-9857](https://orcid.org/0000-0001-5681-9857))

¹ Department of Agricultural and Biological Engineering, Purdue University, West Lafayette, IN, USA  
² The Collaborative Science Environment, PBC, USA  

**Correspondence:** Richard Barker — `dr.richard.barker@gmail.com`  
**Target Journal:** *npj Microgravity* (Article) · **Version:** v2.0 (Phase 6 Multi-Stimuli Release, November 2026)

[Download Manuscript PDF (300 DPI)]({{{{ '/assets/manuscript_npj_microgravity.pdf' | relative_url }}}}){{: .btn .btn-primary}}
[Download Word DOCX]({{{{ '/assets/manuscript_npj_microgravity.docx' | relative_url }}}}){{: .btn}}
[Stimuli Decoders Synthesis]({{{{ '/stimuli_decoders_synthesis' | relative_url }}}}){{: .btn}}
[Dedicated Article View]({{{{ '/manuscript/' | relative_url }}}}){{: .btn}}

---

## On-Page Table of Contents
- [Abstract](#abstract)
- [Introduction](#introduction)
- [Results](#results)
  - [A dual-tool architecture for multi-stimuli space decoding](#a-dual-tool-architecture-for-multi-stimuli-space-decoding-fig-1)
  - [Positive control: Ground-truth embryo lineage recovery](#positive-control-ground-truth-embryo-lineage-recovery-fig-3)
  - [Assembly of the 49-contrast, 15-family master stress library](#assembly-of-the-49-contrast-15-family-master-stress-library-fig-2)
  - [Decoupling total pressure from hypoxia in seed cell types](#decoupling-total-pressure-from-hypoxia-in-seed-cell-types-fig-4)
  - [The DeepSpace Seed-Susceptibility Atlas v8: The root tip convergence apex](#the-deepspace-seed-susceptibility-atlas-v8-the-root-tip-convergence-apex-fig-5)
  - [Stage and tissue vulnerability dynamics](#stage-and-tissue-vulnerability-dynamics)
  - [Multi-stressor convergence model and falsification hypotheses](#multi-stressor-convergence-model-and-falsification-hypotheses-fig-6)
- [Discussion](#discussion)
  - [Limitations and next frontiers](#limitations-and-next-frontiers)
- [Methods](#methods)
- [Data & Code Availability](#data-availability)
- [References](#references)
- [Author Contributions & Acknowledgements](#author-contributions--acknowledgements)
- [Citation & License](#citation--license)

---

{manuscript_body}

---

## Citation & License

The computational framework and curated datasets are released under the open-source **MIT License**. Machine-readable citation metadata is available in [CITATION.cff](https://github.com/dr-richard-barker/deepspace-seed-stress-decoder/blob/main/CITATION.cff).

```bibtex
@software{{barker_deepspace_2026,
  author    = {{Barker, Richard}},
  title     = {{{{DeepSpace Plant-Stress to Germinating-Seed Decoder
               (DSRS + GSAD) and Seed-Susceptibility Atlas}}}},
  year      = {{2026}},
  version   = {{0.2.0}},
  license   = {{MIT}},
  publisher = {{Zenodo}},
  doi       = {{10.5281/zenodo.0000000}},
  url       = {{https://github.com/dr-richard-barker/deepspace-seed-stress-decoder}}
}}
```

Companion manuscript (targeted at _npj Microgravity_):

```bibtex
@article{{barker_seed_susceptibility_2026,
  author  = {{Barker, Richard}},
  title   = {{{{A cell-type-resolved atlas of deep-space stress susceptibility
             in the dry and germinating Arabidopsis seed}}}},
  year    = {{2026}},
  journal = {{npj Microgravity}},
  note    = {{Manuscript targeted at npj Microgravity; version 0.2.0 compendium release}}
}}
```

**Author**: Richard Barker — Purdue University; The Collaborative Science Environment, PBC.  
**Correspondence**: `dr.richard.barker@gmail.com`

---

_All decoder outputs represent predicted concordance from cross-stage signature transfer, not proven direct causation; claims are categorized by evidence tiers and paired with explicit experimental falsification criteria._
"""

    DOCS_INDEX.write_text(index_content, encoding="utf-8")
    print(f"Generated {DOCS_INDEX} ({len(index_content)} bytes).")

def build_manuscript_standalone():
    DOCS_MANUSCRIPT_DIR.mkdir(parents=True, exist_ok=True)
    raw_manuscript = MANUSCRIPT_SOURCE.read_text(encoding="utf-8")
    manuscript_body = prepare_manuscript_body(raw_manuscript)

    standalone_content = f"""---
layout: cose
title: "A cell-type-resolved atlas of deep-space stress susceptibility in the dry and germinating Arabidopsis seed"
permalink: /manuscript/
description: "Full research manuscript targeted at npj Microgravity presenting the DeepSpace Seed-Stress Decoder, stimuli decoders integration, and single-cell seed susceptibility atlas v8."
---

# A cell-type-resolved atlas of deep-space stress susceptibility in the dry and germinating Arabidopsis seed

**Richard Barker**¹ ² (ORCID: [0000-0001-5681-9857](https://orcid.org/0000-0001-5681-9857))

¹ Department of Agricultural and Biological Engineering, Purdue University, West Lafayette, IN, USA  
² The Collaborative Science Environment, PBC, USA  

**Correspondence:** Richard Barker — `dr.richard.barker@gmail.com`  
**Target Journal:** *npj Microgravity* (Article) · **Version:** v2.0 (Phase 6 Multi-Stimuli Release, November 2026)

[Read Interactive PDF Below](#pdf-viewer){{: .btn .btn-primary}}
[Download Manuscript PDF (300 DPI)]({{{{ '/assets/manuscript_npj_microgravity.pdf' | relative_url }}}}){{: .btn}}
[Download Word DOCX]({{{{ '/assets/manuscript_npj_microgravity.docx' | relative_url }}}}){{: .btn}}
[Back to Overview Portal]({{{{ '/' | relative_url }}}}){{: .btn}}
[Stimuli Decoders Synthesis]({{{{ '/stimuli_decoders_synthesis' | relative_url }}}}){{: .btn}}
[GitHub Repository](https://github.com/dr-richard-barker/deepspace-seed-stress-decoder){{: .btn}}

| 49 contrasts | 15 stressor families | 123 seed panels | 14 / 15 families hit the root cap | Target: npj Microgravity |
|:---:|:---:|:---:|:---:|:---:|

---

## npj Microgravity Interactive Article Viewer

Read the camera-ready publication PDF directly in the interactive viewer below, or navigate to the web sections in the table of contents.

{PDF_VIEWER_BLOCK}

---

## On-Page Navigation
- [Abstract](#abstract)
- [Introduction](#introduction)
- [Results](#results)
  - [A dual-tool architecture for multi-stimuli space decoding](#a-dual-tool-architecture-for-multi-stimuli-space-decoding-fig-1)
  - [Positive control: Ground-truth embryo lineage recovery](#positive-control-ground-truth-embryo-lineage-recovery-fig-3)
  - [Assembly of the 49-contrast, 15-family master stress library](#assembly-of-the-49-contrast-15-family-master-stress-library-fig-2)
  - [Decoupling total pressure from hypoxia in seed cell types](#decoupling-total-pressure-from-hypoxia-in-seed-cell-types-fig-4)
  - [The DeepSpace Seed-Susceptibility Atlas v8: The root tip convergence apex](#the-deepspace-seed-susceptibility-atlas-v8-the-root-tip-convergence-apex-fig-5)
  - [Stage and tissue vulnerability dynamics](#stage-and-tissue-vulnerability-dynamics)
  - [Multi-stressor convergence model and falsification hypotheses](#multi-stressor-convergence-model-and-falsification-hypotheses-fig-6)
- [Discussion](#discussion)
  - [Limitations and next frontiers](#limitations-and-next-frontiers)
- [Methods](#methods)
- [Data & Code Availability](#data-availability)
- [References](#references)
- [Author Contributions & Acknowledgements](#author-contributions--acknowledgements)

---

{manuscript_body}
"""

    DOCS_MANUSCRIPT_INDEX.write_text(standalone_content, encoding="utf-8")
    # Also write docs/manuscript.md for backwards compatibility
    Path("docs/manuscript.md").write_text(standalone_content, encoding="utf-8")
    print(f"Generated {DOCS_MANUSCRIPT_INDEX} and docs/manuscript.md ({len(standalone_content)} bytes).")

def verify_zero_latex():
    for p in [DOCS_INDEX, DOCS_MANUSCRIPT_INDEX, Path("docs/manuscript.md")]:
        content = p.read_text(encoding="utf-8")
        dollars = [line for line in content.splitlines() if "$" in line and not line.strip().startswith("$")]
        if dollars:
            print(f"ERROR: {p} has {len(dollars)} dollar lines:")
            for d in dollars:
                print("  ", d)
            raise ValueError(f"Found raw LaTeX in {p}")
        for kw in [r"\text", "_{", r"\ge", r"\le", r"\mu"]:
            if kw in content:
                raise ValueError(f"Found '{kw}' in {p}")
    print("Verification passed: ZERO LaTeX math or unrendered escaping syntax in docs!")

def main():
    build_index()
    build_manuscript_standalone()
    verify_zero_latex()

if __name__ == "__main__":
    main()
