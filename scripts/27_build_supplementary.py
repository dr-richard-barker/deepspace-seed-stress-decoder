#!/usr/bin/env python
"""Render the Supplementary Materials markdown to PDF with Supplementary Figures S1-S5 embedded."""
import os, markdown
from xhtml2pdf import pisa
ROOT=os.environ.get("DEEPSPACE_ROOT") or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MD=os.path.join(ROOT,"report","supplementary_materials.md")
OUT=os.path.join(ROOT,"report","supplementary_materials.pdf")
FIG=os.path.join(ROOT,"results","figures")
body=markdown.markdown(open(MD,encoding="utf-8").read(),extensions=["tables","sane_lists","fenced_code"])
plates=[("decoder_combined_perturbation_heatmap.png","Fig S1. Combined 27-contrast perturbation model (10 families) -> seed programs."),
        ("bridge_heatmap_v3.png","Fig S2a. Shared-latent bridge (within-source scaled)."),
        ("bridge_embedding_v3.png","Fig S2b. Shared-latent bridge embedding (PCA)."),
        ("deepspace_atlas_tissue_stage.png","Fig S3. Atlas at tissue + germination-stage level (incl. dry-seed anchor)."),
        ("nmf_localization_heatmap.png","Fig S4. NMF-responsive gene localization (2022 oxidative panel)."),
        ("nmf_localization_2021v2022.png","Fig S5. NMF localization: 2022 oxidative panel vs 2021 Sci Rep NNMF DEGs."),
        ("nmf_radicle_risk_heatmap.png","Fig S6a. NMF-up radicle-risk genes (n=32): specificity across germinating-seed cell types."),
        ("nmf_radicle_risk_heatmap_down.png","Fig S6b. NMF-down radicle set (n=2): specificity across germinating-seed cell types."),
        ("nmf_root_efp_up.png","Fig S7. ePlant-style root pictograms per NMF-up threat locus (germinating-seed radicle compartments)."),
        ("nmf_root_efp_collective.png","Fig S8. Collective NMF localization: up vs down vs NET; meristem/QC = synergy hotspot."),
        ("nmf_mature_root_efp_up.png","Fig S9a. NMF-up loci in the mature-root eFP map (Brady GSE8934): per-locus longitudinal pictograms."),
        ("nmf_mature_root_efp_collective.png","Fig S9b. Mature-root collective profile: tip-bias is germination-specific (mature root = maturation-biased)."),
        ("nmf_mature_root_celltype_heatmap.png","Fig S9c. NMF loci across sorted mature-root cell types (Brady GSE8934).")]
figs="<h1>Supplementary Figures</h1>"
for fn,cap in plates:
    p=os.path.join(FIG,fn)
    if os.path.exists(p): figs+=f'<div class="plate"><img src="{p}" width="470"/><div class="cap">{cap}</div></div>'
css="""@page{size:A4;margin:1.6cm} body{font-family:Helvetica,Arial,sans-serif;font-size:9.5pt;line-height:1.35;color:#111}
h1{font-size:14pt;color:#14304f;border-bottom:1.5px solid #14304f;padding-bottom:3px;margin-top:13px}
h2{font-size:12pt;color:#1c4a72;margin-top:11px}
table{border-collapse:collapse;width:100%;font-size:8pt;margin:6px 0} th,td{border:0.5px solid #999;padding:3px 4px;text-align:left} th{background:#eef2f7}
code{background:#f2f2f2;font-size:8pt} .plate{margin:10px 0} .plate img{width:470px} .cap{font-size:8pt;color:#555;font-style:italic} hr{border:0;border-top:0.5px solid #ccc}"""
html=f"<html><head><meta charset='utf-8'><style>{css}</style></head><body>{body}<hr/>{figs}</body></html>"
with open(OUT,"wb") as f: err=pisa.CreatePDF(html,dest=f)
print("supplementary PDF:",OUT,"| errors:",err.err)
