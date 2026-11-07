#!/usr/bin/env python3
"""
Build the manuscript-in-preparation PDF, formatted for npj Microgravity submission.
It must never stamp journal branding, acceptance dates, volume numbers or a DOI that
has not been issued (see ABAI lesson L003).
Includes:
- 'Manuscript in preparation' status banner (no journal branding)
- Author metadata block (Authors, Affiliations, Correspondence, status)
- Styled Abstract callout block
- In-line figure integration (Figs. 1-6) with bold Nature captions (Fig. 1 | Title. Caption...)
- Clean three-line Nature publication tables
- Running headers and footers with draft status and page numbers
- Clean typography and complete entity safety for chemical/math symbols
"""

import os, re
from pathlib import Path
from xhtml2pdf import pisa

ROOT = Path(__file__).resolve().parent.parent
MD_PATH = ROOT / "report" / "manuscript_npj_microgravity.md"
FIGURES_DIR = ROOT / "report" / "figures_npj"
OUT_PDF = ROOT / "report" / "manuscript_npj_microgravity.pdf"
DOCS_ASSETS_PDF = ROOT / "docs" / "assets" / "manuscript_npj_microgravity.pdf"

FIGURE_DATA = {
    "Fig. 1": {
        "file": "F1_concept_workflow.png",
        "title": "Two-tool framework and stimuli decoders integration.",
        "caption": "A single query transcriptomic signature drives the dual-engine architecture: DSRS identifies which space stressor or environmental perturbation the query resembles across 49 contrasts and 15 families, while GSAD projects the query across 123 single-cell seed panels to resolve cell-type-, tissue-, and stage-specific susceptibility.",
        "marker": "### A dual-tool architecture for multi-stimuli space decoding (Fig. 1)",
    },
    "Fig. 2": {
        "file": "F2_stress_library.png",
        "title": "DSRS 49-contrast reference stress library fingerprints.",
        "caption": "Enrichment profiles across the 123 reference seed panels for 49 perturbation contrasts grouped into 15 stressor families. Distinct transcriptional fingerprints provide the diagnostic basis for identifying space stressor classes.",
        "marker": "### Assembly of the 49-contrast, 15-family master stress library (Fig. 2)",
    },
    "Fig. 3": {
        "file": "F3_seed_reference_embryo_lineage.png",
        "title": "Validated single-cell seed reference and autonomous embryo lineage recovery.",
        "caption": "Unbiased embryo lineage tracing independently recovers ground-truth developmental origins (protoderm -&gt; epidermis; hypophysis -&gt; radicle apical meristem; vascular primordium -&gt; provasculature), confirming that cross-stage projection captures authentic biological programs rather than statistical artifacts.",
        "marker": "### Positive control: Ground-truth embryo lineage recovery (Fig. 3)",
    },
    "Fig. 4": {
        "file": "F4_gsad_susceptibility.png",
        "title": "GSAD single-cell susceptibility profiles across 49 deep-space stressors.",
        "caption": "Unbiased cell-type susceptibility profiles across 15 germinating seed clusters. Pure hypobaria and nominal exploration atmospheres selectively engage the radicle apical meristem and columella root cap independently of hypoxia.",
        "marker": "### Decoupling total pressure from hypoxia in seed cell types (Fig. 4)",
    },
    "Fig. 5": {
        "file": "F5_deepspace_atlas.png",
        "title": "The DeepSpace Seed-Susceptibility Atlas v8 and multi-stressor convergence.",
        "caption": "Heatmap of germinating seed cell types across 15 stressor families. Asterisks mark significant enrichment (|NES| &gt;= 1.5, FDR &lt; 0.25; NMF |z| &gt;= 2.0). The convergence bar chart establishes the columella/root cap (14/15) and radicle apical meristem (10/15) as the multi-stressor convergence apex.",
        "marker": "### The DeepSpace Seed-Susceptibility Atlas v8: The root tip convergence apex (Fig. 5)",
    },
    "Fig. 6": {
        "file": "F6_convergence_model.png",
        "title": "Radicle growth-point convergence model and testable falsification hypotheses.",
        "caption": "Seven biophysical and chemical vectors converge upon the radicle growth point. Hypotheses H1-H4 formulate explicit, testable experimental predictions for near-null magnetic fields, decoupled hypobaria, and oxidative cascades.",
        "marker": "### Multi-stressor convergence model and falsification hypotheses (Fig. 6)",
    },
}

TABLE_1_HTML = """
<div style="margin: 12px 0; page-break-inside: avoid;">
  <div style="font-family: Arial, Helvetica, sans-serif; font-size: 8pt; font-weight: bold; color: #0f172a; margin-bottom: 4px;">
    Table 1 | The 49-contrast deep-space and environmental stress library organized across 15 families.
  </div>
  <table style="width: 100%; border-collapse: collapse; font-family: Arial, Helvetica, sans-serif; font-size: 7.5pt; line-height: 1.3;">
    <thead>
      <tr style="border-top: 1.5px solid #0f172a; border-bottom: 1px solid #0f172a; background: #f8fafc;">
        <th style="padding: 4px 6px; text-align: left; font-weight: bold; width: 22%;">Stressor Family</th>
        <th style="padding: 4px 6px; text-align: center; font-weight: bold; width: 10%;">Contrasts (<i>N</i>)</th>
        <th style="padding: 4px 6px; text-align: left; font-weight: bold; width: 44%;">Representative Conditions</th>
        <th style="padding: 4px 6px; text-align: left; font-weight: bold; width: 24%;">Key Sources</th>
      </tr>
    </thead>
    <tbody>
      <tr style="border-bottom: 0.5px solid #e2e8f0;"><td style="padding: 3px 6px; font-weight: bold;">Gravity</td><td style="padding: 3px 6px; text-align: center;">5</td><td style="padding: 3px 6px;">Spaceflight micro-g (root &amp; leaf, light &amp; dark) + 2 g hypergravity</td><td style="padding: 3px 6px;">NASA OSD-120, OSD-678; GSE29787</td></tr>
      <tr style="border-bottom: 0.5px solid #e2e8f0; background: #fafafa;"><td style="padding: 3px 6px; font-weight: bold;">Radiation</td><td style="padding: 3px 6px; text-align: center;">9</td><td style="padding: 3px 6px;">GCR low-dose (40, 80 cGy), acute gamma (100 Gy Co-60), Cs-137 (10, 100 cGy)</td><td style="padding: 3px 6px;">NASA OSD-658, OSD-498, OSD-782</td></tr>
      <tr style="border-bottom: 0.5px solid #e2e8f0;"><td style="padding: 3px 6px; font-weight: bold;">Exploration Atmosphere</td><td style="padding: 3px 6px; text-align: center;">6</td><td style="padding: 3px 6px;">Pure hypobaria, pure hypoxia, NASA exploration atmosphere (50 kPa NormO<sub>2</sub>, HypoO<sub>2</sub>)</td><td style="padding: 3px 6px;">TabPFN v2 (130 microarrays)</td></tr>
      <tr style="border-bottom: 0.5px solid #e2e8f0; background: #fafafa;"><td style="padding: 3px 6px; font-weight: bold;">Redox / ROS</td><td style="padding: 3px 6px; text-align: center;">2</td><td style="padding: 3px 6px;">Continuous CVAE spaceflight ROS shift (log<sub>2</sub> err_ratio), H<sub>2</sub>O<sub>2</sub> stress</td><td style="padding: 3px 6px;">Redox_decoder (232 studies, 38 missions); MASTA</td></tr>
      <tr style="border-bottom: 0.5px solid #e2e8f0;"><td style="padding: 3px 6px; font-weight: bold;">Cold</td><td style="padding: 3px 6px; text-align: center;">2</td><td style="padding: 3px 6px;">Cold shock time-course (4 &deg;C at 3 h and 24 h)</td><td style="padding: 3px 6px;">MASTA / AtGenExpress</td></tr>
      <tr style="border-bottom: 0.5px solid #e2e8f0; background: #fafafa;"><td style="padding: 3px 6px; font-weight: bold;">Wounding</td><td style="padding: 3px 6px; text-align: center;">1</td><td style="padding: 3px 6px;">Mechanical leaf damage (1.5 h, mimicking launch vibration shear)</td><td style="padding: 3px 6px;">MASTA / AtGenExpress</td></tr>
      <tr style="border-bottom: 0.5px solid #e2e8f0;"><td style="padding: 3px 6px; font-weight: bold;">Hormones (Aux/GA/CK/BR)</td><td style="padding: 3px 6px; text-align: center;">4</td><td style="padding: 3px 6px;">IAA (1 &micro;M, 3 h), GA<sub>3</sub> (1 h), Zeatin (1 h), Brassinolide (10 nM, 3 h)</td><td style="padding: 3px 6px;">MASTA / AtGenExpress</td></tr>
      <tr style="border-bottom: 0.5px solid #e2e8f0; background: #fafafa;"><td style="padding: 3px 6px; font-weight: bold;">Nutrient Stress</td><td style="padding: 3px 6px; text-align: center;">2</td><td style="padding: 3px 6px;">Nitrogen starvation, Phosphorus starvation</td><td style="padding: 3px 6px;">MASTA / AtGenExpress</td></tr>
      <tr style="border-bottom: 0.5px solid #e2e8f0;"><td style="padding: 3px 6px; font-weight: bold;">Tropism</td><td style="padding: 3px 6px; text-align: center;">4</td><td style="padding: 3px 6px;">Root gravistimulation time-course, phototropism gradient</td><td style="padding: 3px 6px;">GSE199142, GSE3847</td></tr>
      <tr style="border-bottom: 0.5px solid #e2e8f0; background: #fafafa;"><td style="padding: 3px 6px; font-weight: bold;">Low-Oxygen</td><td style="padding: 3px 6px; text-align: center;">8</td><td style="padding: 3px 6px;">Hypoxia, anoxia, complete submergence</td><td style="padding: 3px 6px;">GSE315308, GSE182724</td></tr>
      <tr style="border-bottom: 0.5px solid #e2e8f0;"><td style="padding: 3px 6px; font-weight: bold;">Desiccation &amp; Osmotic</td><td style="padding: 3px 6px; text-align: center;">4</td><td style="padding: 3px 6px;">Seed maturation drying (21 vs 15 DAF), mannitol, drought</td><td style="padding: 3px 6px;">GSE76015, GSE5622, MASTA</td></tr>
      <tr style="border-bottom: 0.5px solid #e2e8f0; background: #fafafa;"><td style="padding: 3px 6px; font-weight: bold;">Ethylene &amp; UV</td><td style="padding: 3px 6px; text-align: center;">2</td><td style="padding: 3px 6px;">ACC precursor (4 h vs 0 h), UV-B irradiation vs control</td><td style="padding: 3px 6px;">GSE193833, GSE5626</td></tr>
      <tr style="border-bottom: 1.5px solid #0f172a;"><td style="padding: 3px 6px; font-weight: bold;">Magnetic / Null Field</td><td style="padding: 3px 6px; text-align: center;">1</td><td style="padding: 3px 6px;">Near-null magnetic field (&lt; 30 nT NMF) curated localization panel</td><td style="padding: 3px 6px;">Parmagnani/Maffei 2022</td></tr>
    </tbody>
  </table>
</div>
"""

TABLE_2_HTML = """
<div style="margin: 12px 0; page-break-inside: avoid;">
  <div style="font-family: Arial, Helvetica, sans-serif; font-size: 8pt; font-weight: bold; color: #0f172a; margin-bottom: 4px;">
    Table 2 | Single-cell seed cell-type convergence ranking across 15 stressor families.
  </div>
  <table style="width: 100%; border-collapse: collapse; font-family: Arial, Helvetica, sans-serif; font-size: 7.5pt; line-height: 1.3;">
    <thead>
      <tr style="border-top: 1.5px solid #0f172a; border-bottom: 1px solid #0f172a; background: #f8fafc;">
        <th style="padding: 4px 6px; text-align: left; font-weight: bold; width: 32%;">Germinating Cell Type / Cluster</th>
        <th style="padding: 4px 6px; text-align: left; font-weight: bold; width: 18%;">Organ / Zone</th>
        <th style="padding: 4px 6px; text-align: center; font-weight: bold; width: 15%;">Families (<i>N</i> / 15)</th>
        <th style="padding: 4px 6px; text-align: center; font-weight: bold; width: 15%;">Convergence</th>
        <th style="padding: 4px 6px; text-align: left; font-weight: bold; width: 20%;">Key Signatures</th>
      </tr>
    </thead>
    <tbody>
      <tr style="border-bottom: 0.5px solid #e2e8f0; font-weight: bold; background: #fff1f2;"><td style="padding: 3px 6px; color: #be123c;">Columella / Root Cap (+QC) (cl4)</td><td style="padding: 3px 6px;">Radicle (Root Pole)</td><td style="padding: 3px 6px; text-align: center;">14 / 15</td><td style="padding: 3px 6px; text-align: center;">93.3%</td><td style="padding: 3px 6px;">Gravity, hypobaria, redox, GCR</td></tr>
      <tr style="border-bottom: 0.5px solid #e2e8f0;"><td style="padding: 3px 6px; font-weight: bold;">Cotyledon Mesophyll (cl13)</td><td style="padding: 3px 6px;">Cotyledon</td><td style="padding: 3px 6px; text-align: center;">13 / 15</td><td style="padding: 3px 6px; text-align: center;">86.7%</td><td style="padding: 3px 6px;">Radiation, hypobaria, redox, nutrients</td></tr>
      <tr style="border-bottom: 0.5px solid #e2e8f0; background: #fafafa;"><td style="padding: 3px 6px; font-weight: bold;">Hypocotyl Cortex (cl5)</td><td style="padding: 3px 6px;">Hypocotyl</td><td style="padding: 3px 6px; text-align: center;">11 / 15</td><td style="padding: 3px 6px; text-align: center;">73.3%</td><td style="padding: 3px 6px;">Radiation, hypobaria, hypoxia, redox</td></tr>
      <tr style="border-bottom: 0.5px solid #e2e8f0;"><td style="padding: 3px 6px; font-weight: bold;">Hypocotyl Cortex (cl7)</td><td style="padding: 3px 6px;">Hypocotyl</td><td style="padding: 3px 6px; text-align: center;">11 / 15</td><td style="padding: 3px 6px; text-align: center;">73.3%</td><td style="padding: 3px 6px;">Gravity, radiation, hypobaria, redox</td></tr>
      <tr style="border-bottom: 0.5px solid #e2e8f0; font-weight: bold; background: #eff6ff;"><td style="padding: 3px 6px; color: #1d4ed8;">Radicle Apical Meristem (cl14)</td><td style="padding: 3px 6px;">Radicle Growth Point</td><td style="padding: 3px 6px; text-align: center;">10 / 15</td><td style="padding: 3px 6px; text-align: center;">66.7%</td><td style="padding: 3px 6px;">NMF (<i>z</i> = +7.96), hypobaria, &micro;g</td></tr>
      <tr style="border-bottom: 0.5px solid #e2e8f0;"><td style="padding: 3px 6px;">Cotyledon Mesophyll (cl3)</td><td style="padding: 3px 6px;">Cotyledon</td><td style="padding: 3px 6px; text-align: center;">10 / 15</td><td style="padding: 3px 6px; text-align: center;">66.7%</td><td style="padding: 3px 6px;">Radiation, hypobaria, redox, cold</td></tr>
      <tr style="border-bottom: 0.5px solid #e2e8f0; background: #fafafa;"><td style="padding: 3px 6px;">Hypocotyl Cortex (cl1)</td><td style="padding: 3px 6px;">Hypocotyl</td><td style="padding: 3px 6px; text-align: center;">10 / 15</td><td style="padding: 3px 6px; text-align: center;">66.7%</td><td style="padding: 3px 6px;">Gravity, radiation, hypobaria, desiccation</td></tr>
      <tr style="border-bottom: 0.5px solid #e2e8f0;"><td style="padding: 3px 6px;">Provasculature (cl12)</td><td style="padding: 3px 6px;">Vascular Stele</td><td style="padding: 3px 6px; text-align: center;">9 / 15</td><td style="padding: 3px 6px; text-align: center;">60.0%</td><td style="padding: 3px 6px;">Radiation, hypobaria, redox, nutrients</td></tr>
      <tr style="border-bottom: 0.5px solid #e2e8f0; background: #fafafa;"><td style="padding: 3px 6px; font-weight: bold;">Radicle Epidermis (cl10)</td><td style="padding: 3px 6px;">Radicle Surface</td><td style="padding: 3px 6px; text-align: center;">8 / 15</td><td style="padding: 3px 6px; text-align: center;">53.3%</td><td style="padding: 3px 6px;">Gravity, radiation, hypobaria, redox</td></tr>
      <tr style="border-bottom: 0.5px solid #e2e8f0;"><td style="padding: 3px 6px;">Protophloem (cl15)</td><td style="padding: 3px 6px;">Vascular Stele</td><td style="padding: 3px 6px; text-align: center;">8 / 15</td><td style="padding: 3px 6px; text-align: center;">53.3%</td><td style="padding: 3px 6px;">Radiation, hypobaria, redox, nutrients</td></tr>
      <tr style="border-bottom: 1.5px solid #0f172a;"><td style="padding: 3px 6px;">Protoxylem (cl9)</td><td style="padding: 3px 6px;">Vascular Stele</td><td style="padding: 3px 6px; text-align: center;">7 / 15</td><td style="padding: 3px 6px; text-align: center;">46.7%</td><td style="padding: 3px 6px;">Radiation, hypobaria, redox, cold</td></tr>
    </tbody>
  </table>
</div>
"""

CSS = """
@page first_page {
    size: a4 portrait;
    margin-left: 1.8cm;
    margin-right: 1.8cm;
    margin-top: 1.2cm;
    margin-bottom: 1.8cm;
    @frame footer {
        -pdf-frame-content: footerContent;
        bottom: 0.6cm;
        left: 1.8cm;
        right: 1.8cm;
        height: 1.1cm;
    }
}

@page regular_page {
    size: a4 portrait;
    margin-left: 1.8cm;
    margin-right: 1.8cm;
    margin-top: 2.2cm;
    margin-bottom: 1.8cm;
    @frame header {
        -pdf-frame-content: headerContent;
        top: 0.8cm;
        left: 1.8cm;
        right: 1.8cm;
        height: 0.9cm;
    }
    @frame footer {
        -pdf-frame-content: footerContent;
        bottom: 0.6cm;
        left: 1.8cm;
        right: 1.8cm;
        height: 1.1cm;
    }
}

body {
    font-family: Arial, Helvetica, sans-serif;
    font-size: 8.8pt;
    line-height: 1.42;
    color: #1e293b;
}

h1 {
    font-family: Arial, Helvetica, sans-serif;
    font-size: 11pt;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    color: #0f172a;
    margin-top: 16px;
    margin-bottom: 6px;
    border-bottom: 1px solid #e2e8f0;
    padding-bottom: 2px;
}

h2 {
    font-family: Arial, Helvetica, sans-serif;
    font-size: 9.8pt;
    font-weight: bold;
    color: #1e293b;
    margin-top: 12px;
    margin-bottom: 4px;
}

h3 {
    font-family: Arial, Helvetica, sans-serif;
    font-size: 9pt;
    font-weight: bold;
    color: #334155;
    margin-top: 10px;
    margin-bottom: 3px;
}

p {
    margin-bottom: 7px;
    text-align: justify;
}

ul, ol {
    margin-top: 2px;
    margin-bottom: 7px;
    padding-left: 16px;
}

li {
    margin-bottom: 3px;
    text-align: justify;
}

strong {
    color: #0f172a;
}

code {
    font-family: "Courier New", Courier, monospace;
    font-size: 8pt;
    background: #f1f5f9;
    padding: 1px 3px;
    color: #0f172a;
}

.figure-plate {
    margin: 12px 0;
    text-align: center;
    page-break-inside: avoid;
}

.figure-plate img {
    width: 480px;
}

.figure-caption {
    font-size: 7.8pt;
    line-height: 1.35;
    color: #334155;
    text-align: justify;
    margin-top: 4px;
}

.hypothesis-box {
    background: #f8fafc;
    border-left: 3px solid #2563eb;
    padding: 6px 10px;
    margin: 8px 0;
    font-size: 8.2pt;
    line-height: 1.35;
}

.references-list ol {
    padding-left: 14px;
    font-size: 7.8pt;
    line-height: 1.35;
}

.references-list li {
    margin-bottom: 4px;
}
"""

def clean_html_entities(text: str) -> str:
    # Convert special characters into clean HTML-safe ASCII equivalents for Helvetica
    replacements = [
        ("→", " -&gt; "),
        ("&rarr;", " -&gt; "),
        ("γ-rays", "gamma-rays"),
        ("γ", "gamma"),
        ("&gamma;", "gamma"),
        ("µg", "micro-g"),
        ("µT", "micro-T"),
        ("µM", "&mu;M"),
        ("β_hypobaria", "beta_hypobaria"),
        ("β_hypoxia", "beta_hypoxia"),
        ("β_interaction", "beta_interaction"),
        ("β = 0.5", "beta = 0.5"),
        ("β", "beta"),
        ("&beta;", "beta"),
        ("≥", "&gt;="),
        ("&ge;", "&gt;="),
        ("≤", "&lt;="),
        ("&le;", "&lt;="),
        ("×", "x"),
        ("&times;", "x"),
        ("°C", "&deg;C"),
        ("H₂O₂", "H<sub>2</sub>O<sub>2</sub>"),
        ("¹O₂", "<sup>1</sup>O<sub>2</sub>"),
        ("O₃", "O<sub>3</sub>"),
        ("NormO₂", "NormO<sub>2</sub>"),
        ("HypoO₂", "HypoO<sub>2</sub>"),
        ("pO₂", "<i>p</i>O<sub>2</sub>"),
        ("(*p*O₂)", "(<i>p</i>O<sub>2</sub>)"),
        ("(*P*<sub>total</sub>)", "(<i>P</i><sub>total</sub>)"),
        ("log₂FC", "log<sub>2</sub>FC"),
        ("log₂ error ratio", "log<sub>2</sub>(err_spaceflight / err_ground)"),
        ("log₂(err_spaceflight / err_ground)", "log<sub>2</sub>(err_spaceflight / err_ground)"),
        ("GA₃", "GA<sub>3</sub>"),
        ("10⁻¹⁶", "10<sup>-16</sup>"),
        ("₂", "<sub>2</sub>"),
        ("₃", "<sub>3</sub>"),
        ("—", " - "),
        ("&mdash;", " - "),
        ("–", "-"),
        ("&ndash;", "-"),
    ]
    for old, new in replacements:
        text = text.replace(old, new)

    # Convert markdown inline styling to HTML
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"(?<!\*)\*([^\*]+?)\*(?!\*)", r"<i>\1</i>", text)
    text = re.sub(r"`([^`]+?)`", r"<code>\1</code>", text)
    return text

def parse_markdown_to_npj_html(md_text: str) -> str:
    md_text = clean_html_entities(md_text)
    lines = md_text.splitlines()

    # Extract Title, Abstract, etc.
    title = "A cell-type-resolved atlas of deep-space stress susceptibility in the dry and germinating Arabidopsis seed"
    
    # Process text into sections
    content_html = []
    abstract_text = ""
    in_abstract = False
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        if line.startswith("## Abstract"):
            in_abstract = True
            i += 1
            abs_lines = []
            while i < len(lines) and not lines[i].strip().startswith("## "):
                if lines[i].strip():
                    abs_lines.append(lines[i].strip())
                i += 1
            abstract_text = " ".join([l for l in abs_lines if not l.startswith("**Keywords:")])
            keywords_text = next((l for l in abs_lines if l.startswith("**Keywords:")), "")
            
            # Add Page 1 Nature Header Banner + Metadata + Abstract
            p1_html = f"""
<div class="first-page-container">
  <div style="font-family: Arial, Helvetica, sans-serif; font-size: 9pt; font-weight: bold; color: #c84b31; margin-bottom: 6px;">
    MANUSCRIPT IN PREPARATION &mdash; formatted for submission to npj Microgravity (not peer reviewed, not accepted, no DOI)
  </div>
  <div style="border-bottom: 2px solid #c84b31; margin-bottom: 12px;"></div>

  <div style="font-family: Arial, Helvetica, sans-serif; font-size: 15.5pt; font-weight: bold; line-height: 1.25; color: #0f172a; margin-bottom: 10px;">
    {title}
  </div>

  <div style="font-family: Arial, Helvetica, sans-serif; font-size: 9.5pt; font-weight: bold; color: #1e293b; margin-bottom: 6px;">
    Richard Barker<sup>1,2*</sup>
  </div>

  <div style="font-family: Arial, Helvetica, sans-serif; font-size: 7.8pt; line-height: 1.35; color: #475569; margin-bottom: 10px;">
    <sup>1</sup>Department of Agricultural and Biological Engineering, Purdue University, West Lafayette, IN, USA.<br/>
    <sup>2</sup>The Collaborative Science Environment, PBC, USA.<br/>
    <sup>*</sup>email: dr.richard.barker@gmail.com
  </div>

  <div style="font-family: Arial, Helvetica, sans-serif; font-size: 7.2pt; color: #64748b; margin-bottom: 14px; border-top: 0.5px solid #cbd5e1; border-bottom: 0.5px solid #cbd5e1; padding: 3px 0;">
    Status: manuscript in preparation. Preprint DOI: none yet. Software/data DOI: Zenodo deposit pending.
  </div>

  <div style="background: #f8fafc; border-left: 3.5px solid #c84b31; padding: 9px 12px; margin-bottom: 14px;">
    <div style="font-family: Arial, Helvetica, sans-serif; font-size: 8pt; font-weight: bold; color: #c84b31; text-transform: uppercase; margin-bottom: 3px; letter-spacing: 0.5px;">Abstract</div>
    <div style="font-family: Arial, Helvetica, sans-serif; font-size: 8.3pt; line-height: 1.42; color: #1e293b; text-align: justify;">
      {abstract_text}
    </div>
    <div style="font-family: Arial, Helvetica, sans-serif; font-size: 7.5pt; color: #64748b; margin-top: 6px;">
      {keywords_text}
    </div>
  </div>
</div>
<pdf:nexttemplate name="regular_page"/>
"""
            content_html.append(p1_html)
            continue

        if line.startswith("## "):
            sec_title = line[3:].strip()
            content_html.append(f"<h1>{sec_title}</h1>")
            i += 1
            continue

        if line.startswith("### "):
            sub_title = line[4:].strip()
            # Clean heading marker (e.g. remove "(Fig. 1)")
            clean_sub = re.sub(r"\s*\(Fig\.\s*\d+\)", "", sub_title)
            content_html.append(f"<h2>{clean_sub}</h2>")
            i += 1
            
            # Check if this section has an associated figure or table
            for fig_key, fig_info in FIGURE_DATA.items():
                if fig_info["marker"] == line:
                    img_path = os.path.join(FIGURES_DIR, fig_info["file"])
                    fig_html = f"""
<div class="figure-plate">
  <img src="{img_path}" />
  <div class="figure-caption">
    <strong>{fig_key} | {fig_info["title"]}</strong> {fig_info["caption"]}
  </div>
</div>
"""
                    content_html.append(fig_html)
                    if fig_key == "Fig. 2":
                        content_html.append(TABLE_1_HTML)
                    elif fig_key == "Fig. 5":
                        content_html.append(TABLE_2_HTML)
            continue

        if line.startswith("- **H1**:") or line.startswith("- **H2**:") or line.startswith("- **H3**:") or line.startswith("- **H4**:"):
            # Format testable hypotheses nicely
            h_clean = line[2:].strip()
            content_html.append(f'<div class="hypothesis-box">{h_clean}</div>')
            i += 1
            continue

        if line.startswith("- "):
            item_text = line[2:].strip()
            content_html.append(f"<ul><li>{item_text}</li></ul>")
            i += 1
            continue

        if re.match(r"^\d+\.\s", line):
            num_match = re.match(r"^(\d+)\.\s*(.*)$", line)
            num = num_match.group(1)
            item_text = num_match.group(2)
            content_html.append(f'<div style="margin-left: 14px; margin-bottom: 4px; text-align: justify;"><strong>{num}.</strong> {item_text}</div>')
            i += 1
            continue

        if line.startswith("---"):
            i += 1
            continue

        if line:
            content_html.append(f"<p>{line}</p>")

        i += 1

    body_html = "\n".join(content_html)
    return body_html

def main():
    print(f"Reading manuscript from {MD_PATH}...")
    md_text = MD_PATH.read_text(encoding="utf-8")

    body_html = parse_markdown_to_npj_html(md_text)

    full_html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>A cell-type-resolved atlas of deep-space stress susceptibility in the dry and germinating Arabidopsis seed</title>
<style>
{CSS}
</style>
</head>
<body>
<div id="headerContent" style="font-family: Arial, Helvetica, sans-serif; font-size: 7.2pt; color: #64748b;">
  <table style="width: 100%; border: none; border-collapse: collapse;">
    <tr>
      <td style="border: none; text-align: left; padding: 0;">Barker &mdash; manuscript in preparation (2026)</td>
      <td style="border: none; text-align: right; padding: 0;">github.com/dr-richard-barker/deepspace-seed-stress-decoder</td>
    </tr>
  </table>
  <div style="border-bottom: 0.5px solid #cbd5e1; margin-top: 3px;"></div>
</div>

<div id="footerContent" style="font-family: Arial, Helvetica, sans-serif; font-size: 7.2pt; color: #64748b;">
  <div style="border-top: 0.5px solid #cbd5e1; margin-bottom: 3px;"></div>
  <table style="width: 100%; border: none; border-collapse: collapse;">
    <tr>
      <td style="border: none; text-align: left; padding: 0;">Draft &mdash; not peer reviewed</td>
      <td style="border: none; text-align: right; padding: 0;">Page <pdf:pagenumber> of <pdf:pagecount></td>
    </tr>
  </table>
</div>

{body_html}
</body>
</html>
"""

    print(f"Compiling PDF to {OUT_PDF}...")
    with open(OUT_PDF, "wb") as f:
        pisa_status = pisa.CreatePDF(full_html, dest=f)

    if pisa_status.err:
        print(f"ERROR compiling PDF: {pisa_status.err}")
        return

    size_kb = round(os.path.getsize(OUT_PDF) / 1024)
    print(f"Successfully generated {OUT_PDF} ({size_kb} KB, errors: {pisa_status.err})")

    # Also copy to docs/assets/ for mounting on GitHub Pages
    DOCS_ASSETS_PDF.parent.mkdir(parents=True, exist_ok=True)
    DOCS_ASSETS_PDF.write_bytes(OUT_PDF.read_bytes())
    print(f"Synchronized PDF to {DOCS_ASSETS_PDF}")

if __name__ == "__main__":
    main()
