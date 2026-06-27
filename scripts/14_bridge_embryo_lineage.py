#!/usr/bin/env python
"""Phase 3 Layer-2 (v4) — EMBRYO-LINEAGE-ONLY dev bridge.

Rationale: only the embryo lineage persists development -> dry/dormant -> germination (seed coat, endosperm,
funiculus, ovule are terminal/maternal). So restrict the dev side to Gehring EMBRYO cells, pseudobulk by
embryo cell-STATE (level_3), and map developing-embryo states onto germinating-embryo cell types.
Within-source scaling (v3 method). Produces a directed embryo-state -> germinating-cell-type lineage map.

Outputs: results/tables/embryo_lineage_map.csv, bridge_latent_v4_embryo.csv;
         results/figures/embryo_lineage_heatmap.{png,svg}, bridge_embryo_embedding.{png,svg}
"""
import os, numpy as np, pandas as pd
from scipy.io import mmread; from scipy.sparse import csr_matrix
from sklearn.decomposition import PCA
import gseapy as gp
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt

ROOT=r"C:\Users\drric\Downloads\nmf_seed_decoder"
PROC=os.path.join(ROOT,"data","processed","gehring"); PAN=os.path.join(ROOT,"panels")
T=os.path.join(ROOT,"results","tables"); F=os.path.join(ROOT,"results","figures")

# germ axes
pla=pd.read_csv(os.path.join(PAN,"panel_library_annotated.csv"))
gpn=pla[pla.panel_source=="germ_cluster"]
germ_sets={lbl:g.gene.dropna().unique().tolist() for lbl,g in gpn.groupby("panel_label")}

# load Gehring counts + metadata; subset to EMBRYO cells
genes=[l.strip() for l in open(os.path.join(PROC,"genes.txt"))]
cells=[l.strip() for l in open(os.path.join(PROC,"cells.txt"))]
md=pd.read_csv(os.path.join(PROC,"metadata.csv"),index_col=0).loc[cells].reset_index(drop=True)
emb=md["level_1_annotation"].astype(str).eq("Embryo").values
print("embryo cells:",emb.sum(),"of",len(emb))
state=md.loc[emb,"level_3_annotation_abbr"].astype(str)
# keep embryo states with >=40 cells
keep=[s for s,n in state.value_counts().items() if n>=40 and s.lower()!="nan"]
print("embryo states kept (>=40 cells):",len(keep))
M=mmread(os.path.join(PROC,"counts.mtx")).tocsr()[:,emb]      # genes x embryo cells
ind=pd.get_dummies(state).reindex(columns=keep).fillna(0).values
pb=(M @ csr_matrix(ind)).toarray(); pb=pb/pb.sum(0,keepdims=True)*1e6; pb=np.log1p(pb)
embpb=pd.DataFrame(pb,index=genes,columns=keep); embpb=embpb.loc[embpb.var(1)>0]
embpb.to_csv(os.path.join(T,"gehring_embryo_state_pseudobulk.csv"))

# ssGSEA embryo states vs germ axes
ss=gp.ssgsea(data=embpb,gene_sets=germ_sets,outdir=None,sample_norm_method="rank",
             min_size=5,max_size=500,threads=4,no_plot=True)
r=ss.res2d.copy(); r["NES"]=pd.to_numeric(r["NES"],errors="coerce")
emb_scores=r.pivot(index="Name",columns="Term",values="NES")

# stress scores (v2 NES germ rows)
nes=pd.read_csv(os.path.join(T,"decoder_nes_matrix_v2.csv"),index_col=0)
ann=pd.read_csv(os.path.join(PAN,"germination_cluster_annotations.csv")); ann["cluster"]=ann.cluster.astype(str)
cl2lab={c:f"{n} (cl{c})" for c,n in zip(ann.cluster,ann.cell_type)}
gr=nes.loc[[i for i in nes.index if i.startswith("germ_cluster::")]].copy()
gr.index=[cl2lab[i.split("::")[1]] for i in gr.index]
stress_scores=gr.T

axes=[a for a in germ_sets if a in emb_scores.columns and a in stress_scores.columns]
zc=lambda d:(d[axes]-d[axes].mean(0))/d[axes].std(0).replace(0,1)   # within-source z
embZ=zc(emb_scores); strZ=zc(stress_scores)

# ---- directed embryo-state -> germinating-cell-type lineage map ----
lin=pd.DataFrame({"embryo_state":embZ.index,
                  "nearest_germ_celltype":embZ.idxmax(1),"z":embZ.max(1).round(2),
                  "2nd":embZ.apply(lambda row:row.nlargest(2).index[-1],axis=1)})
lin.to_csv(os.path.join(T,"embryo_lineage_map.csv"),index=False)

# combined latent (embryo-dev + stress) for embedding
embZ.index=["emb: "+i for i in embZ.index]; strZ.index=["stress: "+i for i in strZ.index]
Z=pd.concat([embZ,strZ],axis=0); Z.to_csv(os.path.join(T,"bridge_latent_v4_embryo.csv"))

# ---- lineage heatmap (embryo states x germ axes) ----
H=embZ.copy(); H.index=[i.replace("emb: ","") for i in H.index]
fig,ax=plt.subplots(figsize=(8.5,0.5*len(H)+1.6)); vmax=np.nanmax(np.abs(H.values))
im=ax.imshow(H.values,cmap="PuOr_r",vmin=-vmax,vmax=vmax,aspect="auto")
ax.set_xticks(range(H.shape[1])); ax.set_xticklabels(H.columns,rotation=45,ha="right",fontsize=7.5)
ax.set_yticks(range(len(H))); ax.set_yticklabels(H.index,fontsize=8)
for i in range(H.shape[0]):
    j=int(np.argmax(H.values[i])); ax.add_patch(plt.Rectangle((j-0.5,i-0.5),1,1,fill=False,edgecolor="k",lw=1.6))
ax.set_title("Embryo-lineage bridge: developing-embryo state -> germinating-seed cell type\n(within-source z; boxed = top match)",fontsize=9)
fig.colorbar(im,ax=ax,fraction=0.04,pad=0.03); fig.tight_layout()
fig.savefig(os.path.join(F,"embryo_lineage_heatmap.png"),dpi=200,bbox_inches="tight")
fig.savefig(os.path.join(F,"embryo_lineage_heatmap.svg"),bbox_inches="tight")

# ---- embedding: embryo-dev vs perturbations ----
clsmap=pd.read_csv(os.path.join(T,"contrast_classes.csv"),index_col=0)["stressor_class"].to_dict()
def cl(i): return "embryo_dev" if i.startswith("emb: ") else clsmap.get(i.replace("stress: ",""),"stress")
src=[cl(i) for i in Z.index]
col={"embryo_dev":"#1a9850","microgravity":"#4575b4","radiation_GCR":"#fdae61","radiation_lowdose":"#f46d43","radiation_acute":"#a50026"}
p=PCA(2).fit_transform(Z.values)
fig,ax=plt.subplots(figsize=(8,6.5))
for i,name in enumerate(Z.index):
    ax.scatter(p[i,0],p[i,1],c=col.get(src[i],"#888"),s=70,edgecolor="k",lw=0.4)
    ax.annotate(name.split(": ",1)[1],(p[i,0],p[i,1]),fontsize=5.5,xytext=(3,3),textcoords="offset points")
import matplotlib.patches as mp
ax.legend(handles=[mp.Patch(color=col[k],label=k) for k in col],fontsize=7,loc="best")
ax.set_xlabel("PC1"); ax.set_ylabel("PC2"); ax.set_title("Embryo-lineage dev + perturbations (within-source scaled)",fontsize=10)
fig.tight_layout(); fig.savefig(os.path.join(F,"bridge_embryo_embedding.png"),dpi=200); fig.savefig(os.path.join(F,"bridge_embryo_embedding.svg"))

print("\n==== developing-embryo state -> germinating-seed cell type ====")
for _,x in lin.sort_values("z",ascending=False).iterrows():
    print(f"  {x.embryo_state:28s} -> {x.nearest_germ_celltype:30s} z={x.z:+.2f}  (2nd: {x['2nd']})")
print("\nDONE")
