#!/usr/bin/env python
"""Phase 3 Layer-2 (v2) — shared 'germinating-seed score space' bridge with the FULL perturbation panel.

Axes = 15 named germinating-seed cell types. Inputs placed relative to the dry/germinating reference:
  - adult stress (ALL 15 contrasts: microgravity + radiation) -> decoder NES v2 across the 15 germ axes
  - late-seed-dev (Gehring tissue x timepoint) -> ssGSEA vs the 15 germ panels
Outputs: results/tables/bridge_latent_v2.csv, bridge_assignments_v2.csv;
         results/figures/bridge_heatmap_v2.{png,svg}, bridge_embedding_v2.{png,svg}
"""
import os, numpy as np, pandas as pd
from scipy.io import mmread; from scipy.sparse import csr_matrix
from sklearn.decomposition import PCA
import gseapy as gp
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt

ROOT=os.environ.get("DEEPSPACE_ROOT") or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROC=os.path.join(ROOT,"data","processed","gehring"); PAN=os.path.join(ROOT,"panels")
T=os.path.join(ROOT,"results","tables"); F=os.path.join(ROOT,"results","figures")

# germ panels (named) = axes
pla=pd.read_csv(os.path.join(PAN,"panel_library_annotated.csv"))
gpn=pla[pla.panel_source=="germ_cluster"]
germ_sets={lbl:g.gene.dropna().unique().tolist() for lbl,g in gpn.groupby("panel_label")}

# dev pseudobulk: level_1 x timepoint
genes=[l.strip() for l in open(os.path.join(PROC,"genes.txt"))]
cells=[l.strip() for l in open(os.path.join(PROC,"cells.txt"))]
md=pd.read_csv(os.path.join(PROC,"metadata.csv"),index_col=0).loc[cells]
md["grp"]=md["level_1_annotation"].astype(str)+"_"+md["timepoint"].astype(str)
M=mmread(os.path.join(PROC,"counts.mtx")).tocsr()
grps=[g for g,n in md["grp"].value_counts().items() if n>=50]
ind=pd.get_dummies(md["grp"]).reindex(columns=grps).fillna(0).values
pb=(M @ csr_matrix(ind)).toarray(); pb=pb/pb.sum(0,keepdims=True)*1e6; pb=np.log1p(pb)
dev=pd.DataFrame(pb,index=genes,columns=grps); dev=dev.loc[dev.var(1)>0]
dev.to_csv(os.path.join(T,"gehring_dev_pseudobulk.csv"))   # cache for reuse

ss=gp.ssgsea(data=dev,gene_sets=germ_sets,outdir=None,sample_norm_method="rank",
             min_size=5,max_size=500,threads=4,no_plot=True)
r=ss.res2d.copy(); r["NES"]=pd.to_numeric(r["NES"],errors="coerce")
dev_scores=r.pivot(index="Name",columns="Term",values="NES"); dev_scores.index=["dev: "+i for i in dev_scores.index]

# stress coords from v2 NES (ALL 15 contrasts)
nes=pd.read_csv(os.path.join(T,"decoder_nes_matrix_v2.csv"),index_col=0)
ann=pd.read_csv(os.path.join(PAN,"germination_cluster_annotations.csv")); ann["cluster"]=ann.cluster.astype(str)
cl2lab={c:f"{n} (cl{c})" for c,n in zip(ann.cluster,ann.cell_type)}
gr=nes.loc[[i for i in nes.index if i.startswith("germ_cluster::")]].copy()
gr.index=[cl2lab[i.split("::")[1]] for i in gr.index]
stress_scores=gr.T; stress_scores.index=["stress: "+i for i in stress_scores.index]

axes=[a for a in germ_sets if a in dev_scores.columns and a in stress_scores.columns]
comb=pd.concat([dev_scores[axes],stress_scores[axes]],axis=0)
Z=(comb-comb.mean(0))/comb.std(0).replace(0,1)
Z.to_csv(os.path.join(T,"bridge_latent_v2.csv"))

# class tags
clsmap=pd.read_csv(os.path.join(T,"contrast_classes.csv"),index_col=0)["stressor_class"].to_dict()
def cls_of(idx):
    if idx.startswith("dev: "): return "late_seed_dev"
    return clsmap.get(idx.replace("stress: ",""),"stress")
src=[cls_of(i) for i in Z.index]
asg=pd.DataFrame({"input":Z.index,"class":src,
                  "nearest_germ_celltype":Z.idxmax(1),"score":Z.max(1).round(2),
                  "most_suppressed_germ":Z.idxmin(1),"supp_score":Z.min(1).round(2)})
asg.to_csv(os.path.join(T,"bridge_assignments_v2.csv"),index=False)

# ordered heatmap
corder={"late_seed_dev":0,"microgravity":1,"radiation_GCR":2,"radiation_lowdose":3,"radiation_acute":4}
ordr=sorted(range(len(Z.index)),key=lambda i:(corder.get(src[i],9),Z.index[i]))
Zs=Z.iloc[ordr]
fig,ax=plt.subplots(figsize=(9,0.4*len(Zs)+1.8))
vmax=np.nanmax(np.abs(Zs.values))
im=ax.imshow(Zs.values,cmap="PuOr_r",vmin=-vmax,vmax=vmax,aspect="auto")
ax.set_xticks(range(Zs.shape[1])); ax.set_xticklabels(Zs.columns,rotation=45,ha="right",fontsize=7)
ax.set_yticks(range(Zs.shape[0])); ax.set_yticklabels(Zs.index,fontsize=6.5)
ax.set_title("Bridge v2: late-seed-dev + micro-gravity + radiation in germinating-seed score space (z)",fontsize=10)
fig.colorbar(im,ax=ax,fraction=0.03,pad=0.02)
fig.tight_layout(); fig.savefig(os.path.join(F,"bridge_heatmap_v2.png"),dpi=200,bbox_inches="tight")
fig.savefig(os.path.join(F,"bridge_heatmap_v2.svg"),bbox_inches="tight")

# embedding colored by class
col={"late_seed_dev":"#d8b365","microgravity":"#4575b4","radiation_GCR":"#fdae61",
     "radiation_lowdose":"#f46d43","radiation_acute":"#a50026"}
p=PCA(n_components=2).fit_transform(Z.values)
fig,ax=plt.subplots(figsize=(8,6.5))
for i,name in enumerate(Z.index):
    ax.scatter(p[i,0],p[i,1],c=col.get(src[i],"#888"),s=70,edgecolor="k",lw=0.4)
    ax.annotate(name.split(": ",1)[1],(p[i,0],p[i,1]),fontsize=5.5,xytext=(3,3),textcoords="offset points")
import matplotlib.patches as mp
ax.legend(handles=[mp.Patch(color=col[k],label=k) for k in col],fontsize=7,loc="best")
ax.set_xlabel("PC1"); ax.set_ylabel("PC2")
ax.set_title("Shared latent v2 (germinating-seed score space)",fontsize=10)
fig.tight_layout(); fig.savefig(os.path.join(F,"bridge_embedding_v2.png"),dpi=200); fig.savefig(os.path.join(F,"bridge_embedding_v2.svg"))

print("bridge v2:",Z.shape[0],"inputs x",Z.shape[1],"germ axes")
print("\n== stress -> nearest germinating-seed cell type (by class) ==")
for _,x in asg[asg["class"]!="late_seed_dev"].sort_values("class").iterrows():
    print(f"  [{x['class']:17s}] {x.input.replace('stress: ',''):24s} -> {x.nearest_germ_celltype:30s} z={x.score:+.2f}")
print("\nDONE")
