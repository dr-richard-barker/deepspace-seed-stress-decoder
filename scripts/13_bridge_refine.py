#!/usr/bin/env python
"""Phase 3 Layer-2 (v3) — bridge refinement: WITHIN-SOURCE per-axis scaling.

v2 z-scored each germ axis across dev(ssGSEA)+stress(NES) jointly -> PC1 separated by score-type, not
biology. v3 z-scores each axis WITHIN each source (dev separately, stress separately) before combining,
removing the source-type offset so cross-source comparison reflects relative seed-program profile.
Diagnostic: point-biserial corr of PC1 with source indicator, v2 vs v3 (should drop).

Outputs: results/tables/bridge_latent_v3.csv, bridge_assignments_v3.csv;
         results/figures/bridge_heatmap_v3.{png,svg}, bridge_embedding_v3.{png,svg}
"""
import os, numpy as np, pandas as pd
from sklearn.decomposition import PCA
import gseapy as gp
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt

ROOT=r"C:\Users\drric\Downloads\nmf_seed_decoder"
PAN=os.path.join(ROOT,"panels"); T=os.path.join(ROOT,"results","tables"); F=os.path.join(ROOT,"results","figures")

# germ axes
pla=pd.read_csv(os.path.join(PAN,"panel_library_annotated.csv"))
gpn=pla[pla.panel_source=="germ_cluster"]
germ_sets={lbl:g.gene.dropna().unique().tolist() for lbl,g in gpn.groupby("panel_label")}

# dev scores from CACHED pseudobulk (fast; no 1GB reload)
dev=pd.read_csv(os.path.join(T,"gehring_dev_pseudobulk.csv"),index_col=0)
ss=gp.ssgsea(data=dev,gene_sets=germ_sets,outdir=None,sample_norm_method="rank",
             min_size=5,max_size=500,threads=4,no_plot=True)
r=ss.res2d.copy(); r["NES"]=pd.to_numeric(r["NES"],errors="coerce")
dev_scores=r.pivot(index="Name",columns="Term",values="NES"); dev_scores.index=["dev: "+i for i in dev_scores.index]

# stress scores (v7 NES, all 27 contrasts incl hypergravity + desiccation/osmotic/ethylene/temp/UV)
nes=pd.read_csv(os.path.join(T,"decoder_nes_matrix_v7.csv"),index_col=0)
ann=pd.read_csv(os.path.join(PAN,"germination_cluster_annotations.csv")); ann["cluster"]=ann.cluster.astype(str)
cl2lab={c:f"{n} (cl{c})" for c,n in zip(ann.cluster,ann.cell_type)}
gr=nes.loc[[i for i in nes.index if i.startswith("germ_cluster::")]].copy()
gr.index=[cl2lab[i.split("::")[1]] for i in gr.index]
stress_scores=gr.T; stress_scores.index=["stress: "+i for i in stress_scores.index]

axes=[a for a in germ_sets if a in dev_scores.columns and a in stress_scores.columns]
zc=lambda d:(d[axes]-d[axes].mean(0))/d[axes].std(0).replace(0,1)   # per-axis z WITHIN source
Z3=pd.concat([zc(dev_scores),zc(stress_scores)],axis=0)
Z3.to_csv(os.path.join(T,"bridge_latent_v3.csv"))

clsmap=pd.read_csv(os.path.join(T,"contrast_classes.csv"),index_col=0)["stressor_class"].to_dict()
def cls_of(i): return "late_seed_dev" if i.startswith("dev: ") else clsmap.get(i.replace("stress: ",""),"stress")
src=[cls_of(i) for i in Z3.index]
asg=pd.DataFrame({"input":Z3.index,"class":src,"nearest_germ_celltype":Z3.idxmax(1),"score":Z3.max(1).round(2)})
asg.to_csv(os.path.join(T,"bridge_assignments_v3.csv"),index=False)

# ---- diagnostic: PC1 vs source for JOINT vs WITHIN-SOURCE scaling (same v6 data) ----
comb=pd.concat([dev_scores[axes],stress_scores[axes]],axis=0)
Zjoint=(comb-comb.mean(0))/comb.std(0).replace(0,1)
def pc1_src(Z):
    s=np.array([0 if i.startswith("dev: ") else 1 for i in Z.index],float)
    pc1=PCA(2).fit_transform(Z.values)[:,0]
    return abs(np.corrcoef(pc1,s)[0,1])
c_joint=pc1_src(Zjoint); c_v3=pc1_src(Z3)
print(f"PC1<->source |corr|:  joint={c_joint:.2f}   within-source={c_v3:.2f}   (lower=artifact removed)")

# ---- figures ----
corder={"late_seed_dev":0,"microgravity":1,"partial_gravity":2,"hypergravity":3,"tropism_gravi":4,
        "tropism_photo":5,"low_oxygen":6,"desiccation":7,"osmotic":8,"ethylene":9,"temperature":10,"uv":11,
        "radiation_GCR":12,"radiation_lowdose":13,"radiation_acute":14}
ordr=sorted(range(len(Z3.index)),key=lambda i:(corder.get(src[i],9),Z3.index[i])); Zs=Z3.iloc[ordr]
fig,ax=plt.subplots(figsize=(9,0.4*len(Zs)+1.8)); vmax=np.nanmax(np.abs(Zs.values))
im=ax.imshow(Zs.values,cmap="PuOr_r",vmin=-vmax,vmax=vmax,aspect="auto")
ax.set_xticks(range(Zs.shape[1])); ax.set_xticklabels(Zs.columns,rotation=45,ha="right",fontsize=7)
ax.set_yticks(range(len(Zs))); ax.set_yticklabels(Zs.index,fontsize=6.5)
ax.set_title("Bridge v3 (within-source scaling): inputs in germinating-seed score space",fontsize=10)
fig.colorbar(im,ax=ax,fraction=0.03,pad=0.02); fig.tight_layout()
fig.savefig(os.path.join(F,"bridge_heatmap_v3.png"),dpi=200,bbox_inches="tight"); fig.savefig(os.path.join(F,"bridge_heatmap_v3.svg"),bbox_inches="tight")

col={"late_seed_dev":"#d8b365","microgravity":"#4575b4","partial_gravity":"#74add1","hypergravity":"#08306b",
     "tropism_gravi":"#08519c","tropism_photo":"#3690c0","low_oxygen":"#5e3c99","desiccation":"#8c510a",
     "osmotic":"#dfc27d","ethylene":"#1b7837","temperature":"#fdb863","uv":"#c2a5cf",
     "radiation_GCR":"#fdae61","radiation_lowdose":"#f46d43","radiation_acute":"#a50026"}
p=PCA(2).fit_transform(Z3.values)
fig,ax=plt.subplots(figsize=(8,6.5))
for i,name in enumerate(Z3.index):
    ax.scatter(p[i,0],p[i,1],c=col.get(src[i],"#888"),s=70,edgecolor="k",lw=0.4)
    ax.annotate(name.split(": ",1)[1],(p[i,0],p[i,1]),fontsize=5.5,xytext=(3,3),textcoords="offset points")
import matplotlib.patches as mp
ax.legend(handles=[mp.Patch(color=col[k],label=k) for k in col],fontsize=7,loc="best")
ax.set_xlabel("PC1"); ax.set_ylabel("PC2"); ax.set_title(f"Shared latent v3 (within-source scaled); PC1<->source |r|={c_v3:.2f}",fontsize=10)
fig.tight_layout(); fig.savefig(os.path.join(F,"bridge_embedding_v3.png"),dpi=200); fig.savefig(os.path.join(F,"bridge_embedding_v3.svg"))

print("\n== v3 stress -> nearest germinating-seed cell type ==")
for _,x in asg[asg["class"]!="late_seed_dev"].sort_values("class").iterrows():
    print(f"  [{x['class']:17s}] {x.input.replace('stress: ',''):24s} -> {x.nearest_germ_celltype:30s} z={x.score:+.2f}")
print("\n== v3 late-seed-dev -> nearest germinating-seed cell type ==")
for _,x in asg[asg["class"]=="late_seed_dev"].iterrows():
    print(f"  {x.input.replace('dev: ',''):20s} -> {x.nearest_germ_celltype:30s} z={x.score:+.2f}")
print("\nDONE")
