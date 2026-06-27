#!/usr/bin/env python
"""Phase 5.6 — npj Microgravity figure set F1-F6 (consistent style, no text/legend overlap).

F1 concept workflow (schematic) | F2 DSRS stress library | F3 seed reference + embryo-lineage validation
F4 GSAD seed susceptibility | F5 DeepSpace atlas | F6 convergence model (schematic).
Output: report/figures_npj/F{1..6}_*.png/.svg
"""
import os, shutil
import numpy as np, pandas as pd
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import matplotlib.colors as mcolors

ROOT=r"C:\Users\drric\Downloads\nmf_seed_decoder"
T=os.path.join(ROOT,"results","tables"); FIG=os.path.join(ROOT,"results","figures")
OUT=os.path.join(ROOT,"report","figures_npj"); os.makedirs(OUT,exist_ok=True)
plt.rcParams.update({"font.size":9,"font.family":"DejaVu Sans","savefig.dpi":300,"svg.fonttype":"none"})
FAMCOL={"gravity":"#4575b4","tropism":"#3690c0","low_oxygen":"#5e3c99","radiation":"#d73027","magnetic_NMF":"#1a9850"}

def box(ax,x,y,w,h,text,fc,ec="#333",fs=8.5,tc="black"):
    ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle="round,pad=0.02,rounding_size=0.08",
                 fc=fc,ec=ec,lw=1.2)); ax.text(x+w/2,y+h/2,text,ha="center",va="center",fontsize=fs,color=tc,wrap=True)
def arrow(ax,x1,y1,x2,y2,c="#333",lw=1.8):
    ax.add_patch(FancyArrowPatch((x1,y1),(x2,y2),arrowstyle="-|>",mutation_scale=16,lw=lw,color=c))

# ---------- F1: concept workflow ----------
fig,ax=plt.subplots(figsize=(9,5.2)); ax.set_xlim(0,10); ax.set_ylim(0,10); ax.axis("off")
ax.text(5,9.6,"DeepSpace plant-stress → germinating-seed decoding",ha="center",fontsize=13,fontweight="bold")
box(ax,0.3,4.4,2.1,1.4,"Query\ntranscriptomic\nsignature\n(log2FC, AGI)","#f0f0f0")
box(ax,3.2,6.4,3.3,1.8,"Tool 1 — DSRS\nStress-Recognition\nvs reference library\n(5 stressor families)","#dbe7f3")
box(ax,3.2,1.8,3.3,1.8,"Tool 2 — GSAD\nGerminating-Seed AutoDecoder\nvs 122 seed panels\n(Gehring dev + germination)","#ddf2e4")
box(ax,7.1,4.2,2.6,1.8,"DeepSpace seed-\nsusceptibility ATLAS\ncell-type × stressor\n+ convergence","#fde8d0")
arrow(ax,2.4,5.4,3.2,7.0); arrow(ax,2.4,4.8,3.2,2.9)
arrow(ax,6.5,7.0,7.3,5.7); arrow(ax,6.5,2.9,7.3,4.5)
ax.text(4.85,6.2,"“which space stressor?”",ha="center",fontsize=7.5,style="italic",color="#1c4a72")
ax.text(4.85,1.6,"“effect on the seed?”",ha="center",fontsize=7.5,style="italic",color="#1a7a3a")
box(ax,6.7,1.0,3.0,1.1,"Headline: radicle/root tip =\nmulti-stressor hotspot","#fff3bf",fs=8)
arrow(ax,8.4,4.2,8.2,2.1,c="#a06000")
fig.savefig(os.path.join(OUT,"F1_concept_workflow.png"),bbox_inches="tight"); fig.savefig(os.path.join(OUT,"F1_concept_workflow.svg"),bbox_inches="tight"); plt.close(fig)

# ---------- shared heatmap renderer (dedicated colorbar) ----------
def heat(MAT,FDR,rows,cols,title,fname,classbar=None,h_per=0.42,cbar_label="NES"):
    fig=plt.figure(figsize=(max(7,0.42*len(cols)+3),h_per*len(rows)+2.2))
    gs=fig.add_gridspec(2,2,width_ratios=[len(cols),0.5],height_ratios=[0.3,len(rows)],
                        wspace=0.06,hspace=0.04)
    axc=fig.add_subplot(gs[0,0]); ax=fig.add_subplot(gs[1,0]); cax=fig.add_subplot(gs[1,1])
    legend_handles=None
    if classbar is not None:
        fams=sorted({classbar[c] for c in cols},key=lambda k:list(FAMCOL).index(k) if k in FAMCOL else 9)
        cidx={k:i for i,k in enumerate(fams)}
        axc.imshow([[cidx[classbar[c]] for c in cols]],aspect="auto",
                   cmap=mcolors.ListedColormap([FAMCOL.get(k,"#999") for k in fams]))
        axc.set_xticks([]); axc.set_yticks([]); axc.set_ylabel("family",fontsize=7,rotation=0,ha="right",va="center")
        axc.set_title(title,fontsize=10,pad=6)                       # title ABOVE the family bar
        legend_handles=[plt.matplotlib.patches.Patch(color=FAMCOL.get(k,"#999"),label=k) for k in fams]
    else:
        axc.axis("off"); axc.set_title(title,fontsize=10,pad=6)
    vmax=np.nanmax(np.abs(MAT)) or 1
    im=ax.imshow(MAT,cmap="RdBu_r",vmin=-vmax,vmax=vmax,aspect="auto")
    ax.set_xticks(range(len(cols))); ax.set_xticklabels(cols,rotation=55,ha="right",fontsize=7)
    ax.set_yticks(range(len(rows))); ax.set_yticklabels(rows,fontsize=8)
    if FDR is not None:
        for i in range(len(rows)):
            for j in range(len(cols)):
                if pd.notna(FDR[i,j]) and FDR[i,j]<0.25: ax.text(j,i,"*",ha="center",va="center",fontsize=8)
    cb=fig.colorbar(im,cax=cax); cb.set_label(cbar_label,fontsize=8); cax.tick_params(labelsize=7)
    if legend_handles:   # family legend at the BOTTOM (below x labels) — no title collision
        fig.legend(handles=legend_handles,loc="lower center",ncol=len(legend_handles),
                   fontsize=7,frameon=False,bbox_to_anchor=(0.5,-0.04))
    fig.savefig(os.path.join(OUT,fname+".png"),bbox_inches="tight"); fig.savefig(os.path.join(OUT,fname+".svg"),bbox_inches="tight"); plt.close(fig)

nes=pd.read_csv(os.path.join(T,"decoder_nes_matrix_v6.csv"),index_col=0)
fdr=pd.read_csv(os.path.join(T,"decoder_fdr_matrix_v6.csv"),index_col=0)
cls=pd.read_csv(os.path.join(T,"contrast_classes.csv"),index_col=0)["stressor_class"].to_dict()
fam={c:("gravity" if cls.get(c) in("microgravity","partial_gravity","hypergravity") else
        "tropism" if cls.get(c) in("tropism_gravi","tropism_photo") else
        "low_oxygen" if cls.get(c)=="low_oxygen" else
        "radiation" if str(cls.get(c)).startswith("radiation") else cls.get(c,"?")) for c in nes.columns}
order=lambda c:(["gravity","tropism","low_oxygen","radiation"].index(fam[c]) if fam[c] in ["gravity","tropism","low_oxygen","radiation"] else 9,c)
cols=sorted(nes.columns,key=order)

# F2: DSRS stress library (key seed programs x all stressors)
prog=[i for i in nes.index if i.startswith("gehring_L1_tissue::")]+[i for i in nes.index if i.startswith("germ_state_time::")]
M=nes.loc[prog,cols].values; Fd=fdr.loc[prog,cols].values
heat(M,Fd,[r.split("::")[-1] for r in prog],cols,f"F2 — DSRS stress reference library ({len(cols)} contrasts → seed programs)",
     "F2_stress_library",classbar=fam,cbar_label="NES (induced + / suppressed -)")

# F4: GSAD germ cell-type susceptibility (germ cell types x stressors)
ann=pd.read_csv(os.path.join(ROOT,"panels","germination_cluster_annotations.csv")); ann["cluster"]=ann.cluster.astype(str)
cl2lab={c:f"{n} (cl{c})" for c,n in zip(ann.cluster,ann.cell_type)}
g=[i for i in nes.index if i.startswith("germ_cluster::")]
glab=[cl2lab[i.split("::")[1]] for i in g]
heat(nes.loc[g,cols].values,fdr.loc[g,cols].values,glab,cols,
     "F4 — GSAD: stressor → germinating-seed cell-type susceptibility","F4_gsad_susceptibility",
     classbar=fam,cbar_label="NES")

# F3, F5: bring in already-clean figures with consistent naming
shutil.copy(os.path.join(FIG,"embryo_lineage_heatmap.png"),os.path.join(OUT,"F3_seed_reference_embryo_lineage.png"))
shutil.copy(os.path.join(FIG,"embryo_lineage_heatmap.svg"),os.path.join(OUT,"F3_seed_reference_embryo_lineage.svg"))
shutil.copy(os.path.join(FIG,"deepspace_seed_atlas.png"),os.path.join(OUT,"F5_deepspace_atlas.png"))
shutil.copy(os.path.join(FIG,"deepspace_seed_atlas.svg"),os.path.join(OUT,"F5_deepspace_atlas.svg"))

# ---------- F6: convergence model ----------
fig,ax=plt.subplots(figsize=(8.5,6)); ax.set_xlim(0,10); ax.set_ylim(0,10); ax.axis("off")
ax.text(5,9.6,"F6 — Radicle growth-point: deep-space multi-stressor convergence",ha="center",fontsize=12,fontweight="bold")
# center node
box(ax,3.6,4.2,2.8,1.5,"RADICLE apical meristem\n/ root growth-point","#fff3bf",fs=9.5)
# four incoming families
srcs=[("Null magnetic field\n(NMF localization z=+7.96)","magnetic_NMF",1.0,7.6),
      ("Microgravity\n(light-gated)","gravity",1.0,5.0),
      ("Radiation / GCR","radiation",1.0,2.4),
      ("Gravitropism\n(root-tip response)","tropism",7.0,7.6)]
for txt,famk,x,y in srcs:
    box(ax,x,y-0.55,2.4,1.1,txt,mcolors.to_rgba(FAMCOL[famk],0.25),ec=FAMCOL[famk],fs=7.5)
    arrow(ax,x+2.4 if x<5 else x,y, 3.6 if x<5 else 6.4, 5.0, c=FAMCOL[famk])
# developmental origin
box(ax,6.6,2.2,2.9,1.2,"Developmental origin:\nembryonic hypophysis\n→ radicle meristem","#e8e8e8",fs=7.5)
arrow(ax,7.8,3.4,5.6,4.2,c="#666")
# falsification
box(ax,1.2,0.4,3.6,1.1,"H1: NNMF germination → radicle-\nmeristem marker induction (cry1cry2 abolishes)","#f7f7f7",fs=7)
box(ax,5.2,0.4,3.6,1.1,"H2: µg suppresses radicle proliferation\nin a light-gated manner","#f7f7f7",fs=7)
ax.text(5,1.75,"Falsification tests",ha="center",fontsize=8,style="italic",color="#555")
fig.savefig(os.path.join(OUT,"F6_convergence_model.png"),bbox_inches="tight"); fig.savefig(os.path.join(OUT,"F6_convergence_model.svg"),bbox_inches="tight"); plt.close(fig)

print("npj figure set written to",OUT)
for f in sorted(os.listdir(OUT)):
    if f.endswith(".png"): print("  ",f)
