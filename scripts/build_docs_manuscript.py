#!/usr/bin/env python3
"""
Generate docs/manuscript.md from report/manuscript_npj_microgravity.md for GitHub Pages.
Adds responsive Jekyll navigation, table of contents, figure embeds (PNG + SVG),
and action buttons while ensuring zero raw LaTeX math syntax.
"""

from pathlib import Path

SOURCE = Path("report/manuscript_npj_microgravity.md")
DEST = Path("docs/manuscript.md")

FIGURE_INSERTS = {
    "### A dual-tool architecture for multi-stimuli space decoding (Fig. 1)": (
        "\n\n![Figure 1: Concept workflow]({{ '/assets/figures/F1_concept_workflow.png' | relative_url }})\n\n"
        "*Figure 1 — Concept workflow. A single query transcriptomic signature drives the dual-engine architecture: "
        "DSRS recognizes the space stressor class across 49 contrasts and 15 families, while GSAD projects the query "
        "across 123 single-cell seed panels. [[Vector SVG]({{ '/assets/figures/F1_concept_workflow.svg' | relative_url }})]*\n"
    ),
    "### Positive control: Ground-truth embryo lineage recovery (Fig. 3)": (
        "\n\n![Figure 3: Seed reference and embryo-lineage validation]({{ '/assets/figures/F3_seed_reference_embryo_lineage.png' | relative_url }})\n\n"
        "*Figure 3 — Validated single-cell seed reference. Unbiased embryo lineage tracing independently recovers ground-truth "
        "developmental origins (protoderm → epidermis; hypophysis → radicle apical meristem; vascular primordium → provasculature), "
        "confirming that cross-stage projection captures authentic biological programs. [[Vector SVG]({{ '/assets/figures/F3_seed_reference_embryo_lineage.svg' | relative_url }})]*\n"
    ),
    "### Assembly of the 49-contrast, 15-family master stress library (Fig. 2)": (
        "\n\n![Figure 2: DSRS stress library fingerprints]({{ '/assets/figures/F2_stress_library.png' | relative_url }})\n\n"
        "*Figure 2 — DSRS stress-recognition library. Distinct enrichment fingerprints across the 123 seed panels provide the diagnostic basis "
        "for identifying space stressor classes and families. [[Vector SVG]({{ '/assets/figures/F2_stress_library.svg' | relative_url }})]*\n"
    ),
    "### Decoupling total pressure from hypoxia in seed cell types (Fig. 4)": (
        "\n\n![Figure 4: GSAD susceptibility matrix]({{ '/assets/figures/F4_gsad_susceptibility.png' | relative_url }})\n\n"
        "*Figure 4 — GSAD susceptibility matrix across seed cell types. Unbiased single-cell susceptibility profiles across the 15 "
        "germinating clusters for 49 deep-space and environmental perturbations. [[Vector SVG]({{ '/assets/figures/F4_gsad_susceptibility.svg' | relative_url }})]*\n"
    ),
    "### The DeepSpace Seed-Susceptibility Atlas v8: The root tip convergence apex (Fig. 5)": (
        "\n\n![Figure 5: DeepSpace Seed-Susceptibility Atlas v8]({{ '/assets/figures/F5_deepspace_atlas.png' | relative_url }})\n\n"
        "*Figure 5 — The DeepSpace Seed-Susceptibility Atlas v8. Rows display 15 germinating-seed cell types; columns display 15 stressor families. "
        "Asterisks denote statistical significance (|NES| ≥ 1.5, FDR < 0.25; NMF |z| ≥ 2.0). The right-hand convergence bar chart establishes the "
        "columella/root cap (14/15) and radicle apical meristem (10/15) as the multi-stressor convergence apex. [[Vector SVG]({{ '/assets/figures/F5_deepspace_atlas.svg' | relative_url }})]*\n"
    ),
    "### Multi-stressor convergence model and falsification hypotheses (Fig. 6)": (
        "\n\n![Figure 6: Convergence model and falsification tests]({{ '/assets/figures/F6_convergence_model.png' | relative_url }})\n\n"
        "*Figure 6 — Mechanistic convergence model & falsification hypotheses. Seven physical and chemical vectors converge upon the "
        "radicle growth point. Hypotheses H1–H4 formulate explicit, falsifiable experimental tests for near-null magnetic fields, normoxic hypobaria, "
        "and oxidative cascades. [[Vector SVG]({{ '/assets/figures/F6_convergence_model.svg' | relative_url }})]*\n"
    ),
}

def main():
    raw = SOURCE.read_text(encoding="utf-8")
    lines = raw.splitlines()

    # Frontmatter and metadata header
    header = """---
layout: cose
title: "A cell-type-resolved atlas of deep-space stress susceptibility in the dry and germinating Arabidopsis seed"
description: "Full research manuscript targeted at npj Microgravity presenting the DeepSpace Seed-Stress Decoder, stimuli decoders integration, and single-cell seed susceptibility atlas v8."
---

# A cell-type-resolved atlas of deep-space stress susceptibility in the dry and germinating Arabidopsis seed

**Richard Barker**¹ ² (ORCID: [0000-0001-5681-9857](https://orcid.org/0000-0001-5681-9857))

¹ Department of Agricultural and Biological Engineering, Purdue University, West Lafayette, IN, USA  
² The Collaborative Science Environment, PBC, USA  

**Correspondence:** Richard Barker — `dr.richard.barker@gmail.com`  
**Target Journal:** *npj Microgravity* (Article) · **Version:** v2.0 (Phase 6 Multi-Stimuli Release, November 2026)

[Download Manuscript PDF (300 DPI)](https://github.com/dr-richard-barker/deepspace-seed-stress-decoder/blob/main/report/manuscript_npj_microgravity.pdf){: .btn .btn-primary}
[Download Word DOCX](https://github.com/dr-richard-barker/deepspace-seed-stress-decoder/blob/main/report/manuscript_npj_microgravity.docx){: .btn}
[Overview Showcase]({{ '/' | relative_url }}){: .btn}
[Stimuli Decoders Synthesis]({{ '/stimuli_decoders_synthesis' | relative_url }}){: .btn}
[GitHub Repository](https://github.com/dr-richard-barker/deepspace-seed-stress-decoder){: .btn}

| 49 contrasts | 15 stressor families | 123 seed panels | 14 / 15 families hit the root cap |
|:---:|:---:|:---:|:---:|

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
"""

    # Skip the original title/author block up to ## Abstract
    body_lines = []
    in_body = False
    for line in lines:
        if line.startswith("## Abstract"):
            in_body = True
        if in_body:
            body_lines.append(line)

    body_text = "\n".join(body_lines)

    # Insert figures under their section headers
    for section_header, fig_markup in FIGURE_INSERTS.items():
        if section_header in body_text:
            body_text = body_text.replace(section_header, section_header + fig_markup)
        else:
            print(f"WARNING: Section header not found for figure insert: {section_header}")

    full_doc = header + "\n" + body_text

    # Safety check for raw LaTeX dollar signs
    dollars = [line for line in full_doc.splitlines() if "$" in line and not line.strip().startswith("$")]
    if dollars:
        print(f"ERROR: Found {len(dollars)} lines with '$' in generated manuscript:")
        for d in dollars:
            print("  ", d)
        raise ValueError("Raw LaTeX math remains in generated document!")

    DEST.write_text(full_doc, encoding="utf-8")
    print(f"Successfully generated {DEST} ({len(full_doc)} bytes).")

if __name__ == "__main__":
    main()
