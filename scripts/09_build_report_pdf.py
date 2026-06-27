#!/usr/bin/env python
"""Phase 4 — render the synthesis report markdown to PDF, with figure plates."""
import os, markdown
from xhtml2pdf import pisa

ROOT=r"C:\Users\drric\Downloads\nmf_seed_decoder"
MD=os.path.join(ROOT,"report","phase4_synthesis_report.md")
OUT=os.path.join(ROOT,"report","phase4_synthesis_report.pdf")
FIG=os.path.join(ROOT,"results","figures")

body=markdown.markdown(open(MD,encoding="utf-8").read(),
                       extensions=["tables","fenced_code","sane_lists"])

plates=[("deepspace_seed_atlas.png","Fig 5 (HEADLINE). DeepSpace seed-susceptibility atlas: germinating-seed cell type x stressor family + multi-stressor convergence (radicle tip = top hotspot)."),
        ("deepspace_atlas_tissue_stage.png","Fig 5b. DeepSpace atlas at tissue + germination-stage level (12h = most multi-stressor stage)."),
        ("decoder_combined_perturbation_heatmap.png","Fig 0. Combined DeepSpace perturbation model: 10 stressor families, 27 contrasts -> seed programs."),
        ("decoder_L1_state_heatmap.png","Fig 1. Decoder: stressor -> seed tissue & germination-state programs (NES)."),
        ("decoder_germination_named_heatmap.png","Fig 2. Decoder: stressor -> named germinating-seed cell types."),
        ("bridge_heatmap_v3.png","Fig 3. Shared latent v3 (within-source scaled): late-seed-dev + micro-gravity + radiation in germinating-seed score space."),
        ("bridge_embedding_v3.png","Fig 3b. Shared latent v3 embedding (PCA); PC1<->source |r|=0.00 (artifact removed)."),
        ("embryo_lineage_heatmap.png","Fig 3c. Embryo-lineage bridge: developing-embryo state -> germinating-seed cell type (boxed = top match)."),
        ("nmf_localization_heatmap.png","Fig 4. NMF-responsive gene localization across germinating-seed cell types.")]
figs_html="<h1>Figure plates</h1>"
for fn,cap in plates:
    p=os.path.join(FIG,fn)
    if os.path.exists(p):
        figs_html+=f'<div class="plate"><img src="{p}" width="450"/><div class="cap">{cap}</div></div>'

css="""
@page { size: A4; margin: 1.6cm; }
body { font-family: Helvetica, Arial, sans-serif; font-size: 9.5pt; line-height: 1.35; color:#111; }
h1 { font-size: 15pt; color:#14304f; border-bottom:2px solid #14304f; padding-bottom:3px; margin-top:14px;}
h2 { font-size: 12pt; color:#1c4a72; margin-top:12px;}
h3 { font-size: 10.5pt; color:#333; }
table { border-collapse: collapse; width:100%; font-size:8pt; margin:6px 0;}
th,td { border:0.5px solid #999; padding:3px 4px; text-align:left;}
th { background:#eef2f7;}
code { background:#f2f2f2; font-size:8pt;}
.plate { margin:10px 0; }
.plate { -pdf-keep-with-next: true; }
.cap { font-size:8pt; color:#555; font-style:italic; margin-top:2px;}
hr { border:0; border-top:0.5px solid #ccc;}
"""
html=f"<html><head><meta charset='utf-8'><style>{css}</style></head><body>{body}<hr/>{figs_html}</body></html>"

with open(OUT,"wb") as f:
    err=pisa.CreatePDF(html, dest=f)
print("PDF written:" , OUT, "| errors:", err.err)
