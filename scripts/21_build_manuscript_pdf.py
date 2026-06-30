#!/usr/bin/env python
"""Render the npj Microgravity manuscript markdown to PDF with F1-F6 embedded."""
import os, markdown
from xhtml2pdf import pisa
ROOT=os.environ.get("DEEPSPACE_ROOT") or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MD=os.path.join(ROOT,"report","manuscript_npj_microgravity.md")
OUT=os.path.join(ROOT,"report","manuscript_npj_microgravity.pdf")
NPJ=os.path.join(ROOT,"report","figures_npj")
body=markdown.markdown(open(MD,encoding="utf-8").read(),extensions=["tables","sane_lists","fenced_code"])
plates=[("F1_concept_workflow.png","Figure 1. Two-tool framework: signature → DSRS / GSAD → DeepSpace atlas."),
        ("F2_stress_library.png","Figure 2. DSRS stress reference library — 27 contrasts (10 families) → seed programs."),
        ("F3_seed_reference_embryo_lineage.png","Figure 3. Seed reference validation — developing-embryo state → germinating cell type recovers textbook lineages."),
        ("F4_gsad_susceptibility.png","Figure 4. GSAD — stressor → germinating-seed cell-type susceptibility."),
        ("F5_deepspace_atlas.png","Figure 5. DeepSpace seed-susceptibility atlas — cell-type × stressor family + convergence (radicle tip hotspot)."),
        ("F6_convergence_model.png","Figure 6. Radicle growth-point: deep-space multi-stressor convergence model + falsification tests.")]
figs="<h1>Figures</h1>"
for fn,cap in plates:
    p=os.path.join(NPJ,fn)
    if os.path.exists(p): figs+=f'<div class="plate"><img src="{p}" width="470"/><div class="cap">{cap}</div></div>'
css="""@page{size:A4;margin:1.7cm} body{font-family:Georgia,serif;font-size:10pt;line-height:1.4;color:#111}
h1{font-size:15pt;color:#14304f;border-bottom:1.5px solid #14304f;padding-bottom:3px;margin-top:14px}
h2{font-size:12.5pt;color:#1c4a72;margin-top:12px} h3{font-size:11pt;color:#333}
table{border-collapse:collapse;width:100%;font-size:8.5pt} th,td{border:0.5px solid #999;padding:3px 4px;text-align:left} th{background:#eef2f7}
.plate{margin:12px 0} .plate img{width:470px} .cap{font-size:8.5pt;color:#555;font-style:italic;margin-top:2px} hr{border:0;border-top:0.5px solid #ccc}"""
html=f"<html><head><meta charset='utf-8'><style>{css}</style></head><body>{body}<hr/>{figs}</body></html>"
with open(OUT,"wb") as f: err=pisa.CreatePDF(html,dest=f)
print("manuscript PDF:",OUT,"| errors:",err.err)
