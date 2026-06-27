#!/usr/bin/env python
"""Phase 3 Layer-2 — shared 'germinating-seed score space' bridge.

Axes = 15 named germinating-seed cell types (germ panels).
Bridge input 1 (adult stress)      -> decoder NES across the 15 germ panels.
Bridge input 2 (late-seed-dev)     -> ssGSEA of Gehring tissue x timepoint pseudobulk vs germ panels.
Both placed into one space relative to the dry/germinating reference.

Outputs: results/tables/bridge_latent.csv, bridge_assignments.csv;
         results/figures/bridge_heatmap.{png,svg}, bridge_embedding.{png,svg}
"""
import os, numpy as np, pandas as pd
from scipy.io import mmread
from scipy.sparse import csr_matrix
from sklearn.decomposition import PCA
import gseapy as gp
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt

ROOT=r"C:\Users\drric\Downloads\nmf_seed_decoder"
PROC=os.path.join(ROOT,"data","processed","gehring"); PAN=os.path.join(ROOT,"panels")
T=os.path.join(ROOT,"results","tables"); F=os.path.join(ROOT,"results","figures")

# ---- germ panels (named) = latent axes ----
pla=pd.read_csv(os.path.join(PAN,"panel_library_annotated.csv"))
gp_panels=pla[pla.panel_source=="germ_cluster"]
germ_sets={lbl:g.gene.dropna().unique().tolist() for lbl,g in gp_panels.groupby("panel_label")}
print(f"{len(germ_sets)} germ axes")

# ---- Gehring dev pseudobulk: level_1 tissue x timepoint ----
genes=[l.strip() for l in open(os.path.join(PROC,"genes.txt"))]
cells=[l.strip() for l in open(os.path.join(PROC,"cells.txt"))]
md=pd.read_csv(os.path.join(PROC,"metadata.csv"),index_col=0).loc[cells]
md["grp"]=md["level_1_annotation"].astype(str)+"_"+md["timepoint"].astype(str)
M=mmread(os.path.join(PROC,"counts.mtx")).tocsr()      # genes x cells
grps=[g for g,n in md["grp"].value_counts().items() if n>=50]
ind=pd.get_dummies(md["grp"]).reindex(columns=grps).fillna(0).values   # cells x groups
pb=(M @ csr_matrix(ind)).toarray()                      # genes x groups (summed counts)
pb=pb/ pb.sum(0,keepdims=True)*1e6                      # CPM
pb=np.log1p(pb)
dev=pd.DataFrame(pb,index=genes,columns=grps)
dev=dev.loc[dev.var(1)>0]
print("dev pseudobulk:",dev.shape, "groups:",grps)

# ---- ssGSEA: dev tissue-timepoints vs germ axes ----
ss=gp.ssgsea(data=dev, gene_sets=germ_sets, outdir=None, sample_norm_method="rank",
             min_size=5, max_size=500, threads=4, no_plot=True)
r=ss.res2d.copy(); r["NES"]=pd.to_numeric(r["NES"],errors="coerce")
dev_scores=r.pivot(index="Name",columns="Term",values="NES")    # devgroups x germaxes
dev_scores.index=["dev: "+i for i in dev_scores.index]

# ---- stress coordinates from decoder NES (germ rows) ----
nes=pd.read_csv(os.path.join(T,"decoder_nes_matrix.csv"),index_col=0)
ann=pd.read_csv(os.path.join(PAN,"germination_cluster_annotations.csv")); ann["cluster"]=ann.cluster.astype(str)
cl2lab={c:f"{n} (cl{c})" for c,n in zip(ann.cluster,ann.cell_type)}
gr=nes.loc[[i for i in nes.index if i.startswith("germ_cluster::")]].copy()
gr.index=[cl2lab[i.split("::")[1]] for i in gr.index]
stress_scores=gr.T                                              # contrasts x germaxes
stress_scores.index=["stress: "+i for i in stress_scores.index]

# ---- align axes, combine, z-score per axis ----
axes=[a for a in germ_sets if a in dev_scores.columns and a in stress_scores.columns]
comb=pd.concat([dev_scores[axes], stress_scores[axes]],axis=0)
Z=(comb-comb.mean(0))/comb.std(0).replace(0,1)
Z.to_csv(os.path.join(T,"bridge_latent.csv"))

# ---- assignments: nearest germ axis per input ----
asg=pd.DataFrame({"input":Z.index,
                  "nearest_germ_celltype":Z.idxmax(1),
                  "score":Z.max(1).round(2),
                  "most_suppressed_germ":Z.idxmin(1),
                  "supp_score":Z.min(1).round(2)})
asg["source"]=["late_seed_dev" if i.startswith("dev:") else "adult_stress" for i in asg.input]
asg.to_csv(os.path.join(T,"bridge_assignments.csv"),index=False)

# ---- heatmap ----
fig,ax=plt.subplots(figsize=(8.5,0.42*len(Z)+1.8))
vmax=np.nanmax(np.abs(Z.values))
im=ax.imshow(Z.values,cmap="PuOr_r",vmin=-vmax,vmax=vmax,aspect="auto")
ax.set_xticks(range(Z.shape[1])); ax.set_xticklabels(Z.columns,rotation=45,ha="right",fontsize=7)
ax.set_yticks(range(Z.shape[0])); ax.set_yticklabels(Z.index,fontsize=7)
ax.set_title("Bridge: late-seed-dev + adult-stress in germinating-seed score space (z)",fontsize=10)
fig.colorbar(im,ax=ax,fraction=0.046,pad=0.04)
fig.tight_layout(); fig.savefig(os.path.join(F,"bridge_heatmap.png"),dpi=200); fig.savefig(os.path.join(F,"bridge_heatmap.svg"))

# ---- 2D embedding ----
p=PCA(n_components=2).fit_transform(Z.values)
fig,ax=plt.subplots(figsize=(7.5,6))
for i,name in enumerate(Z.index):
    dev_=name.startswith("dev:")
    ax.scatter(p[i,0],p[i,1],c=("#d8b365" if dev_ else "#5ab4ac"),s=70,edgecolor="k",lw=0.4)
    ax.annotate(name.split(": ",1)[1],(p[i,0],p[i,1]),fontsize=6,xytext=(3,3),textcoords="offset points")
ax.set_xlabel("PC1"); ax.set_ylabel("PC2")
ax.set_title("Shared latent: late-seed-dev (tan) vs adult-stress (teal)",fontsize=10)
fig.tight_layout(); fig.savefig(os.path.join(F,"bridge_embedding.png"),dpi=200); fig.savefig(os.path.join(F,"bridge_embedding.svg"))

print("\n==== BRIDGE ASSIGNMENTS ====")
for _,x in asg.iterrows():
    print(f"  {x.input:34s} -> {x.nearest_germ_celltype:30s} (z={x.score:+.2f})")
print("\nDONE")
