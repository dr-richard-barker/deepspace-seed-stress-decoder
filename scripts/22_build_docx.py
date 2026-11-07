#!/usr/bin/env python3
"""
Build the manuscript-in-preparation Word document (.docx) with
figures F1-F6 and summary tables embedded in-line, formatted to Nature Portfolio guidelines.
"""

import os, re, shutil, zipfile
from pathlib import Path
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

ROOT = Path(__file__).resolve().parent.parent
MD_PATH = ROOT / "report" / "manuscript_npj_microgravity.md"
FIGURES_DIR = ROOT / "report" / "figures_npj"
OUT_DOCX = ROOT / "report" / "manuscript_npj_microgravity.docx"
DOCS_ASSETS_DOCX = ROOT / "docs" / "assets" / "manuscript_npj_microgravity.docx"

FIGURE_DATA = {
    "### A dual-tool architecture for multi-stimuli space decoding (Fig. 1)": (
        "F1_concept_workflow.png",
        "Fig. 1 | Two-tool framework and stimuli decoders integration.",
        "A single query transcriptomic signature drives the dual-engine architecture: DSRS identifies which space stressor or environmental perturbation the query resembles across 49 contrasts and 15 families, while GSAD projects the query across 123 single-cell seed panels to resolve cell-type-, tissue-, and stage-specific susceptibility."
    ),
    "### Assembly of the 49-contrast, 15-family master stress library (Fig. 2)": (
        "F2_stress_library.png",
        "Fig. 2 | DSRS 49-contrast reference stress library fingerprints.",
        "Enrichment profiles across the 123 reference seed panels for 49 perturbation contrasts grouped into 15 stressor families. Distinct transcriptional fingerprints provide the diagnostic basis for identifying space stressor classes."
    ),
    "### Positive control: Ground-truth embryo lineage recovery (Fig. 3)": (
        "F3_seed_reference_embryo_lineage.png",
        "Fig. 3 | Validated single-cell seed reference and autonomous embryo lineage recovery.",
        "Unbiased embryo lineage tracing independently recovers ground-truth developmental origins (protoderm → epidermis; hypophysis → radicle apical meristem; vascular primordium → provasculature), confirming that cross-stage projection captures authentic biological programs rather than statistical artifacts."
    ),
    "### Decoupling total pressure from hypoxia in seed cell types (Fig. 4)": (
        "F4_gsad_susceptibility.png",
        "Fig. 4 | GSAD single-cell susceptibility profiles across 49 deep-space stressors.",
        "Unbiased cell-type susceptibility profiles across 15 germinating seed clusters. Pure hypobaria and nominal exploration atmospheres selectively engage the radicle apical meristem and columella root cap independently of hypoxia."
    ),
    "### The DeepSpace Seed-Susceptibility Atlas v8: The root tip convergence apex (Fig. 5)": (
        "F5_deepspace_atlas.png",
        "Fig. 5 | The DeepSpace Seed-Susceptibility Atlas v8 and multi-stressor convergence.",
        "Heatmap of germinating seed cell types across 15 stressor families. Asterisks mark significant enrichment (|NES| ≥ 1.5, FDR < 0.25; NMF |z| ≥ 2.0). The convergence bar chart establishes the columella/root cap (14/15) and radicle apical meristem (10/15) as the multi-stressor convergence apex."
    ),
    "### Multi-stressor convergence model and falsification hypotheses (Fig. 6)": (
        "F6_convergence_model.png",
        "Fig. 6 | Radicle growth-point convergence model and testable falsification hypotheses.",
        "Seven biophysical and chemical vectors converge upon the radicle growth point. Hypotheses H1–H4 formulate explicit, testable experimental predictions for near-null magnetic fields, decoupled hypobaria, and oxidative cascades."
    ),
}

TOKEN_RE = re.compile(r"(\*\*.+?\*\*|\*.+?\*|`.+?`|\[.+?\]\(.+?\))")

def add_runs(paragraph, text, base_font_size=10.5):
    text = text.replace("\\*", "*").replace("\\", "")
    for tok in TOKEN_RE.split(text):
        if not tok:
            continue
        if tok.startswith("**") and tok.endswith("**"):
            r = paragraph.add_run(tok[2:-2])
            r.bold = True
            r.font.name = "Arial"
            r.font.size = Pt(base_font_size)
            r.font.color.rgb = RGBColor(15, 23, 42)
        elif tok.startswith("*") and tok.endswith("*"):
            r = paragraph.add_run(tok[1:-1])
            r.italic = True
            r.font.name = "Arial"
            r.font.size = Pt(base_font_size)
        elif tok.startswith("`") and tok.endswith("`"):
            r = paragraph.add_run(tok[1:-1])
            r.font.name = "Courier New"
            r.font.size = Pt(base_font_size - 1.0)
            r.font.color.rgb = RGBColor(30, 41, 59)
        elif tok.startswith("[") and "](" in tok:
            m = re.match(r"\[(.+?)\]", tok)
            r = paragraph.add_run(m.group(1) if m else tok)
            r.font.name = "Arial"
            r.font.size = Pt(base_font_size)
            r.font.color.rgb = RGBColor(2, 132, 199)
            r.underline = True
        else:
            r = paragraph.add_run(tok)
            r.font.name = "Arial"
            r.font.size = Pt(base_font_size)

def set_cell_borders(cell, top=None, bottom=None):
    tcPr = cell._tc.get_or_add_tcPr()
    tcBorders = parse_xml(f'''
        <w:tcBorders {nsdecls("w")}>
            <w:top w:val="{top.get("val", "none")}" w:sz="{top.get("sz", "0")}" w:space="0" w:color="{top.get("color", "auto")}"/>
            <w:bottom w:val="{bottom.get("val", "none")}" w:sz="{bottom.get("sz", "0")}" w:space="0" w:color="{bottom.get("color", "auto")}"/>
            <w:left w:val="none"/>
            <w:right w:val="none"/>
        </w:tcBorders>
    ''')
    tcPr.append(tcBorders)

def add_table_1(doc):
    p = doc.add_paragraph()
    r = p.add_run("Table 1 | The 49-contrast deep-space and environmental stress library organized across 15 families.")
    r.bold = True; r.font.name = "Arial"; r.font.size = Pt(9.5)
    
    data = [
        ("Gravity", "5", "Spaceflight µg (root & leaf, light & dark) + 2 g hypergravity", "NASA OSD-120, OSD-678; GSE29787"),
        ("Radiation", "9", "GCR low-dose (40, 80 cGy), acute γ (100 Gy Co-60), Cs-137", "NASA OSD-658, OSD-498, OSD-782"),
        ("Exploration Atmosphere", "6", "Pure hypobaria, pure hypoxia, NASA exploration atmosphere (50 kPa NormO₂, HypoO₂)", "TabPFN v2 (130 microarrays)"),
        ("Redox / ROS", "2", "Continuous CVAE spaceflight ROS shift (log₂ err_ratio), H₂O₂", "Redox_decoder (232 studies, 38 missions); MASTA"),
        ("Cold", "2", "Cold shock time-course (4 °C at 3 h and 24 h)", "MASTA / AtGenExpress"),
        ("Wounding", "1", "Mechanical leaf damage (1.5 h, launch vibration shear)", "MASTA / AtGenExpress"),
        ("Hormones", "4", "IAA (1 µM, 3 h), GA₃ (1 h), Zeatin (1 h), Brassinolide (10 nM)", "MASTA / AtGenExpress"),
        ("Nutrient Stress", "2", "Nitrogen starvation, Phosphorus starvation", "MASTA / AtGenExpress"),
        ("Tropism", "4", "Root gravistimulation time-course, phototropism gradient", "GSE199142, GSE3847"),
        ("Low-Oxygen", "8", "Hypoxia, anoxia, complete submergence", "GSE315308, GSE182724"),
        ("Desiccation & Osmotic", "4", "Seed maturation drying (21 vs 15 DAF), mannitol, drought", "GSE76015, GSE5622, MASTA"),
        ("Ethylene & UV", "2", "ACC precursor (4 h), UV-B irradiation vs control", "GSE193833, GSE5626"),
        ("Magnetic / Null Field", "1", "Near-null magnetic field (< 30 nT NMF) localization panel", "Parmagnani/Maffei 2022"),
    ]
    
    table = doc.add_table(rows=1, cols=4)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    
    hdr = table.rows[0].cells
    headers = ["Stressor Family", "Contrasts (N)", "Representative Conditions", "Key Sources"]
    col_widths = [Inches(1.8), Inches(1.0), Inches(2.3), Inches(1.4)]
    
    for i, h_text in enumerate(headers):
        hdr[i].text = h_text
        hdr[i].paragraphs[0].runs[0].font.bold = True
        hdr[i].paragraphs[0].runs[0].font.name = "Arial"
        hdr[i].paragraphs[0].runs[0].font.size = Pt(8.5)
        set_cell_borders(hdr[i], top={"val": "single", "sz": "12", "color": "0F172A"},
                                 bottom={"val": "single", "sz": "6", "color": "0F172A"})
    
    for row_idx, (fam, num, cond, src) in enumerate(data):
        row = table.add_row().cells
        for col_idx, val in enumerate([fam, num, cond, src]):
            row[col_idx].text = val
            r = row[col_idx].paragraphs[0].runs[0]
            r.font.name = "Arial"
            r.font.size = Pt(8.0)
            if col_idx == 0:
                r.font.bold = True
            is_last = (row_idx == len(data) - 1)
            b_val = "single" if is_last else "single"
            b_sz = "12" if is_last else "4"
            b_col = "0F172A" if is_last else "E2E8F0"
            set_cell_borders(row[col_idx], top={"val": "none"},
                                           bottom={"val": b_val, "sz": b_sz, "color": b_col})

def add_table_2(doc):
    p = doc.add_paragraph()
    r = p.add_run("Table 2 | Single-cell seed cell-type convergence ranking across 15 stressor families.")
    r.bold = True; r.font.name = "Arial"; r.font.size = Pt(9.5)
    
    data = [
        ("Columella / Root Cap (+QC) (cl4)", "Radicle (Root Pole)", "14 / 15", "93.3%", "Gravity, hypobaria, redox, GCR"),
        ("Cotyledon Mesophyll (cl13)", "Cotyledon", "13 / 15", "86.7%", "Radiation, hypobaria, redox, nutrients"),
        ("Hypocotyl Cortex (cl5)", "Hypocotyl", "11 / 15", "73.3%", "Radiation, hypobaria, hypoxia, redox"),
        ("Hypocotyl Cortex (cl7)", "Hypocotyl", "11 / 15", "73.3%", "Gravity, radiation, hypobaria, redox"),
        ("Radicle Apical Meristem (cl14)", "Radicle Growth Point", "10 / 15", "66.7%", "NMF (z = +7.96), hypobaria, µg"),
        ("Cotyledon Mesophyll (cl3)", "Cotyledon", "10 / 15", "66.7%", "Radiation, hypobaria, redox, cold"),
        ("Hypocotyl Cortex (cl1)", "Hypocotyl", "10 / 15", "66.7%", "Gravity, radiation, hypobaria, desiccation"),
        ("Provasculature (cl12)", "Vascular Stele", "9 / 15", "60.0%", "Radiation, hypobaria, redox, nutrients"),
        ("Radicle Epidermis (cl10)", "Radicle Surface", "8 / 15", "53.3%", "Gravity, radiation, hypobaria, redox"),
        ("Protophloem (cl15)", "Vascular Stele", "8 / 15", "53.3%", "Radiation, hypobaria, redox, nutrients"),
        ("Protoxylem (cl9)", "Vascular Stele", "7 / 15", "46.7%", "Radiation, hypobaria, redox, cold"),
    ]
    
    table = doc.add_table(rows=1, cols=5)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    
    hdr = table.rows[0].cells
    headers = ["Germinating Cell Type", "Organ / Zone", "Families", "Convergence", "Key Signatures"]
    
    for i, h_text in enumerate(headers):
        hdr[i].text = h_text
        hdr[i].paragraphs[0].runs[0].font.bold = True
        hdr[i].paragraphs[0].runs[0].font.name = "Arial"
        hdr[i].paragraphs[0].runs[0].font.size = Pt(8.5)
        set_cell_borders(hdr[i], top={"val": "single", "sz": "12", "color": "0F172A"},
                                 bottom={"val": "single", "sz": "6", "color": "0F172A"})
        
    for row_idx, row_data in enumerate(data):
        row = table.add_row().cells
        for col_idx, val in enumerate(row_data):
            row[col_idx].text = val
            r = row[col_idx].paragraphs[0].runs[0]
            r.font.name = "Arial"
            r.font.size = Pt(8.0)
            if col_idx == 0:
                r.font.bold = True
            is_last = (row_idx == len(data) - 1)
            b_val = "single" if is_last else "single"
            b_sz = "12" if is_last else "4"
            b_col = "0F172A" if is_last else "E2E8F0"
            set_cell_borders(row[col_idx], top={"val": "none"},
                                           bottom={"val": b_val, "sz": b_sz, "color": b_col})

def main():
    print(f"Reading manuscript markdown from {MD_PATH}...")
    doc = Document()
    
    # 1. Page Geometry (Nature Standard: 1-inch margins)
    section = doc.sections[0]
    section.page_width = Inches(8.5)
    section.page_height = Inches(11.0)
    section.top_margin = Inches(1.0)
    section.bottom_margin = Inches(1.0)
    section.left_margin = Inches(1.0)
    section.right_margin = Inches(1.0)
    
    # 2. Header and Footer
    header = section.header
    hp = header.paragraphs[0]
    hp.text = "npj Microgravity | Article Submission"
    hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    if hp.runs:
        hp.runs[0].font.name = "Arial"
        hp.runs[0].font.size = Pt(8.5)
        hp.runs[0].font.color.rgb = RGBColor(148, 163, 184)
        
    footer = section.footer
    fp = footer.paragraphs[0]
    fp.text = "Barker · DeepSpace Seed-Stress Decoder & Atlas v8"
    fp.alignment = WD_ALIGN_PARAGRAPH.LEFT
    if fp.runs:
        fp.runs[0].font.name = "Arial"
        fp.runs[0].font.size = Pt(8.5)
        fp.runs[0].font.color.rgb = RGBColor(148, 163, 184)

    # 3. Read Markdown
    lines = MD_PATH.read_text(encoding="utf-8").splitlines()
    
    # 4. Article Header Block
    p_brand = doc.add_paragraph()
    # Status line only: never stamp journal branding, acceptance dates, volume or an
    # unissued DOI on an unpublished manuscript (ABAI lesson L003).
    r1 = p_brand.add_run("MANUSCRIPT IN PREPARATION — formatted for submission to npj Microgravity (not peer reviewed, no DOI)")
    r1.bold = True; r1.font.name = "Arial"; r1.font.size = Pt(9.5); r1.font.color.rgb = RGBColor(200, 75, 49)
    p_brand.paragraph_format.space_after = Pt(8)
    
    # Title
    p_title = doc.add_paragraph()
    r_title = p_title.add_run("A cell-type-resolved atlas of deep-space stress susceptibility in the dry and germinating Arabidopsis seed")
    r_title.bold = True; r_title.font.name = "Arial"; r_title.font.size = Pt(17); r_title.font.color.rgb = RGBColor(15, 23, 42)
    p_title.paragraph_format.space_after = Pt(8)
    
    # Authors
    p_auth = doc.add_paragraph()
    r_auth = p_auth.add_run("Richard Barker¹ ²* (ORCID: 0000-0001-5681-9857)")
    r_auth.bold = True; r_auth.font.name = "Arial"; r_auth.font.size = Pt(10.5); r_auth.font.color.rgb = RGBColor(30, 41, 59)
    p_auth.paragraph_format.space_after = Pt(4)
    
    # Affiliations
    p_aff = doc.add_paragraph()
    add_runs(p_aff, "¹ Department of Agricultural and Biological Engineering, Purdue University, West Lafayette, IN, USA.\n² The Collaborative Science Environment, PBC, USA.\n*Correspondence: dr.richard.barker@gmail.com", base_font_size=9.0)
    p_aff.paragraph_format.space_after = Pt(6)
    
    # Tracking Dates
    p_track = doc.add_paragraph()
    r_tr = p_track.add_run("Status: manuscript in preparation. Preprint DOI: none yet. Software/data DOI: Zenodo deposit pending.")
    r_tr.font.name = "Arial"; r_tr.font.size = Pt(8.0); r_tr.font.color.rgb = RGBColor(100, 116, 139)
    p_track.paragraph_format.space_after = Pt(14)
    
    # 5. Parse remaining sections
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        # Skip the original markdown title and author lines
        if line.startswith("# ") or line.startswith("**Richard Barker**") or "Department of Agricultural" in line or "*Correspondence:" in line or "**Target journal:" in line:
            i += 1
            continue
            
        if line.startswith("## Abstract"):
            p_head = doc.add_heading("ABSTRACT", level=1)
            p_head.runs[0].font.name = "Arial"; p_head.runs[0].font.size = Pt(12); p_head.runs[0].font.bold = True; p_head.runs[0].font.color.rgb = RGBColor(15, 23, 42)
            i += 1
            abs_text = []
            while i < len(lines) and not lines[i].strip().startswith("## "):
                if lines[i].strip():
                    abs_text.append(lines[i].strip())
                i += 1
            p_abs = doc.add_paragraph()
            p_abs.paragraph_format.left_indent = Inches(0.2)
            p_abs.paragraph_format.right_indent = Inches(0.2)
            p_abs.paragraph_format.space_after = Pt(12)
            full_abs = "\n\n".join(abs_text)
            add_runs(p_abs, full_abs, base_font_size=10.0)
            continue
            
        if line.startswith("## "):
            sec_name = line[3:].strip().upper()
            p_h1 = doc.add_heading(sec_name, level=1)
            p_h1.runs[0].font.name = "Arial"; p_h1.runs[0].font.size = Pt(12); p_h1.runs[0].font.bold = True; p_h1.runs[0].font.color.rgb = RGBColor(15, 23, 42)
            p_h1.paragraph_format.space_before = Pt(14)
            p_h1.paragraph_format.space_after = Pt(4)
            i += 1
            continue
            
        if line.startswith("### "):
            sub_name = line[4:].strip()
            clean_sub = re.sub(r"\s*\(Fig\.\s*\d+\)", "", sub_name)
            p_h2 = doc.add_heading(clean_sub, level=2)
            p_h2.runs[0].font.name = "Arial"; p_h2.runs[0].font.size = Pt(11); p_h2.runs[0].font.bold = True; p_h2.runs[0].font.color.rgb = RGBColor(30, 41, 59)
            p_h2.paragraph_format.space_before = Pt(10)
            p_h2.paragraph_format.space_after = Pt(3)
            i += 1
            
            # Check for figure embeds
            if line in FIGURE_DATA:
                fig_file, fig_title, fig_cap = FIGURE_DATA[line]
                img_path = os.path.join(FIGURES_DIR, fig_file)
                if os.path.exists(img_path):
                    p_img = doc.add_paragraph()
                    p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
                    p_img.paragraph_format.space_before = Pt(8)
                    p_img.paragraph_format.space_after = Pt(2)
                    doc.add_picture(img_path, width=Inches(6.2))
                    doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
                    
                    p_cap = doc.add_paragraph()
                    p_cap.paragraph_format.left_indent = Inches(0.1)
                    p_cap.paragraph_format.right_indent = Inches(0.1)
                    p_cap.paragraph_format.space_after = Pt(10)
                    r_ct = p_cap.add_run(fig_title + " ")
                    r_ct.bold = True; r_ct.font.name = "Arial"; r_ct.font.size = Pt(8.5); r_ct.font.color.rgb = RGBColor(15, 23, 42)
                    r_cp = p_cap.add_run(fig_cap)
                    r_cp.italic = True; r_cp.font.name = "Arial"; r_cp.font.size = Pt(8.5); r_cp.font.color.rgb = RGBColor(51, 65, 85)
                    
                    if "Fig. 2" in fig_title:
                        add_table_1(doc)
                    elif "Fig. 5" in fig_title:
                        add_table_2(doc)
            continue
            
        if line.startswith("- **H1**:") or line.startswith("- **H2**:") or line.startswith("- **H3**:") or line.startswith("- **H4**:"):
            p_h = doc.add_paragraph(style="List Bullet")
            p_h.paragraph_format.space_after = Pt(3)
            add_runs(p_h, line[2:].strip(), base_font_size=10.0)
            i += 1
            continue
            
        if line.startswith("- "):
            p_li = doc.add_paragraph(style="List Bullet")
            p_li.paragraph_format.space_after = Pt(2)
            add_runs(p_li, line[2:].strip(), base_font_size=10.5)
            i += 1
            continue
            
        if re.match(r"^\d+\.\s", line):
            p_num = doc.add_paragraph(style="List Number")
            p_num.paragraph_format.space_after = Pt(2)
            add_runs(p_num, re.sub(r"^\d+\.\s", "", line), base_font_size=10.5)
            i += 1
            continue
            
        if line.startswith("---"):
            i += 1
            continue
            
        if line:
            p_body = doc.add_paragraph()
            p_body.paragraph_format.space_after = Pt(5)
            p_body.paragraph_format.line_spacing = 1.15
            add_runs(p_body, line, base_font_size=10.5)
            
        i += 1
        
    print(f"Saving Word document to {OUT_DOCX}...")
    doc.save(OUT_DOCX)
    
    # Patch python-docx w:zoom for OpenXML validator compliance
    with zipfile.ZipFile(OUT_DOCX, "r") as z:
        names = z.namelist()
        data = {n: z.read(n) for n in names}
    st = data["word/settings.xml"].decode("utf-8")
    st = re.sub(r"<w:zoom\s*/>", '<w:zoom w:percent="100"/>', st)
    st = re.sub(r'(<w:zoom\b(?![^>]*w:percent)[^>]*)/>', r'\1 w:percent="100"/>', st)
    data["word/settings.xml"] = st.encode("utf-8")
    tmp = str(OUT_DOCX) + ".tmp"
    with zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as z:
        for n in names:
            z.writestr(n, data[n])
    shutil.move(tmp, OUT_DOCX)
    
    size_kb = round(os.path.getsize(OUT_DOCX) / 1024)
    print(f"Successfully generated {OUT_DOCX} ({size_kb} KB, zoom patched)")
    
    # Synchronize to docs/assets/ for web download
    DOCS_ASSETS_DOCX.parent.mkdir(parents=True, exist_ok=True)
    DOCS_ASSETS_DOCX.write_bytes(OUT_DOCX.read_bytes())
    print(f"Synchronized Word DOCX to {DOCS_ASSETS_DOCX}")

if __name__ == "__main__":
    main()
