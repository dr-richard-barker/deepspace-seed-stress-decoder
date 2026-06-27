#!/usr/bin/env python
"""Phase 3 (c) — wire in NMF (null magnetic field) via expression-localization.

The Maffei NNMF panel (~194 genes) is too small for GSEA-prerank onto 50-gene marker panels
(0-4 gene overlap, documented). Instead we ask the tractable question:
  "Where in the dry/germinating seed are NMF-responsive genes expressed, and in which direction?"
by localizing NMF-up / NMF-down gene sets onto germinating-seed cell-type expression specificity.

Outputs: results/tables/nmf_gene_directions.csv, nmf_localization.csv, nmf_panel_overlap.csv
         results/figures/nmf_localization_heatmap.{png,svg}
"""
import os, numpy as np, pandas as pd
from scipy.stats import hypergeom
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt

ROOT=r"C:\Users\drric\Downloads\nmf_seed_decoder"
RAW=os.path.join(ROOT,"data","raw"); NMF=os.path.join(RAW,"nmf_maffei")
PAN=os.path.join(ROOT,"panels"); T=os.path.join(ROOT,"results","tables"); F=os.path.join(ROOT,"results","figures")
rng=np.random.default_rng(42)

# ---------- 1) build NMF gene set + direction (shoot, late timepoints = strongest) ----------
def late_dir(df, gcol="tair_id"):
    d=df.copy(); d["log2_ratio"]=pd.to_numeric(d["log2_ratio"],errors="coerce")
    d=d[d["tissue"].str.lower().eq("shoot")]
    # prefer 96h, else latest available per gene
    order={"4h":1,"24h":2,"48h":3,"96h":4,"10min":0,"1h":0.5}
    d["ord"]=d["time"].map(order).fillna(0)
    d=d.sort_values("ord").groupby(gcol).tail(1)
    return d.set_index(gcol)["log2_ratio"]

poly=late_dir(pd.read_csv(os.path.join(NMF,"nmf_polyphenol_gene_panel.csv")))
h2o2=late_dir(pd.read_csv(os.path.join(NMF,"nmf_h2o2_panel.csv")))
# cluster-membership genes: direction from their cluster's shoot-96h profile
mem=pd.read_csv(os.path.join(NMF,"nmf_cluster_membership.csv"))
prof=pd.read_csv(os.path.join(NMF,"nmf_cluster_profile.csv"))
prof["log2_ratio"]=pd.to_numeric(prof["mean_log2_ratio"],errors="coerce")
ps=prof[(prof.tissue.str.lower()=="shoot")].copy()
ps["ord"]=ps["time"].map({"4h":1,"24h":2,"48h":3,"96h":4,"10min":0,"1h":0.5}).fillna(0)
cl_dir=ps.sort_values("ord").groupby("cluster_letter").tail(1).set_index("cluster_letter")["log2_ratio"]
mem["clust_log2"]=mem["cluster_letter"].map(cl_dir)
mem_dir=mem.dropna(subset=["clust_log2"]).set_index("tair_id")["clust_log2"]

direction=pd.concat([poly,h2o2,mem_dir]).groupby(level=0).mean()  # per-gene NMF shoot-late log2 ratio
direction=direction[direction.index.str.startswith("AT")]
nmf_up=set(direction[direction>0.1].index); nmf_dn=set(direction[direction<-0.1].index)
direction.rename("nmf_shoot_late_log2").to_csv(os.path.join(T,"nmf_gene_directions.csv"))
print(f"NMF genes with direction: {len(direction)}  (up {len(nmf_up)}, down {len(nmf_dn)})")

# ---------- 2) germination pseudobulk per named cell type ----------
ann=pd.read_csv(os.path.join(PAN,"germination_cluster_annotations.csv")); ann["cluster"]=ann.cluster.astype(str)
cl2lab={c:f"{n} (cl{c})" for c,n in zip(ann.cluster,ann.cell_type)}
mat=pd.read_csv(os.path.join(RAW,"germination","GSE182331_expression_mat.csv.gz"),index_col=0)  # genes x cells
meta=pd.read_csv(os.path.join(RAW,"germination","meta.tsv"),sep="\t")
meta["cellid"]=meta["sample"].astype(str)+"."+meta["Barcode"].astype(str)
meta["ct"]=meta["cluster"].astype(str).map(cl2lab)
meta=meta.set_index("cellid").reindex(mat.columns).dropna(subset=["ct"])
mat=mat[meta.index]
pb=mat.groupby(meta["ct"],axis=1).sum()                     # genes x celltypes (summed counts)
pb=pb/pb.sum(0)*1e6; pb=np.log1p(pb)                        # CPM-log
spec=pb.sub(pb.mean(1),axis=0).div(pb.std(1).replace(0,np.nan),axis=0)  # z across cell types
spec=spec.dropna()
print("germ pseudobulk:",pb.shape)

# ---------- 3) localization with permutation null ----------
def localize(geneset):
    g=[x for x in geneset if x in spec.index]
    if len(g)<5: return None,None,len(g)
    obs=spec.loc[g].mean(0)
    null=np.array([spec.loc[rng.choice(spec.index,len(g),replace=False)].mean(0).values for _ in range(1000)])
    z=(obs.values-null.mean(0))/null.std(0)
    return obs, pd.Series(z,index=obs.index), len(g)

loc_up,z_up,n_up=localize(nmf_up); loc_dn,z_dn,n_dn=localize(nmf_dn)
L=pd.DataFrame({"NMF_up_localization_z":z_up,"NMF_down_localization_z":z_dn})
L.to_csv(os.path.join(T,"nmf_localization.csv"))
print(f"localized: up n={n_up}, down n={n_dn}")

# ---------- 4) overlap sparsity vs marker panels (documents the GSEA-infeasibility) ----------
pl=pd.read_csv(os.path.join(PAN,"panel_library_annotated.csv"))
bg=set(spec.index); allnmf=set(direction.index)&bg; M=len(bg); n=len(allnmf)
rows=[]
for (src,lab),g in pl.groupby(["panel_source","panel_label"]):
    pg=set(g.gene)&bg; k=len(pg&allnmf); K=len(pg)
    p=hypergeom.sf(k-1,M,n,K) if k>0 else 1.0
    rows.append(dict(panel_source=src,panel=lab,panel_size=K,nmf_overlap=k,hyper_p=p))
ov=pd.DataFrame(rows).sort_values("nmf_overlap",ascending=False)
ov.to_csv(os.path.join(T,"nmf_panel_overlap.csv"),index=False)
print(f"max NMF-marker overlap across {len(ov)} panels: {ov.nmf_overlap.max()} genes "
      f"(median {ov.nmf_overlap.median():.0f}) -> confirms GSEA-prerank infeasible")

# ---------- 5) figure ----------
order=["cotyledon","hypocotyl","radicle","provasculature","unassigned"]
o=dict(zip(ann.cluster,ann.organ)); lab2org={cl2lab[c]:o[c] for c in ann.cluster}
rows_sorted=sorted(L.index, key=lambda x:(order.index(lab2org.get(x,"unassigned")) if lab2org.get(x,"unassigned") in order else 9, x))
LS=L.loc[rows_sorted]
fig,ax=plt.subplots(figsize=(6.2,0.45*len(LS)+1.5))
vmax=np.nanmax(np.abs(LS.values))
im=ax.imshow(LS.values,cmap="BrBG",vmin=-vmax,vmax=vmax,aspect="auto")
ax.set_xticks([0,1]); ax.set_xticklabels(["NMF-up genes","NMF-down genes"],fontsize=9)
ax.set_yticks(range(len(LS))); ax.set_yticklabels(LS.index,fontsize=8)
for i in range(LS.shape[0]):
    for j in range(LS.shape[1]):
        v=LS.values[i,j]
        if pd.notna(v): ax.text(j,i,f"{v:+.1f}",ha="center",va="center",fontsize=7,
                                 color="white" if abs(v)>0.6*vmax else "black")
ax.set_title("NMF-responsive gene localization in germinating-seed cell types\n(z vs random gene sets)",fontsize=9)
fig.colorbar(im,ax=ax,fraction=0.046,pad=0.04)
fig.tight_layout(); fig.savefig(os.path.join(F,"nmf_localization_heatmap.png"),dpi=200); fig.savefig(os.path.join(F,"nmf_localization_heatmap.svg"))

print("\n==== NMF localization (top germinating-seed cell types) ====")
print("NMF-UP genes concentrated in:");  print(z_up.sort_values(ascending=False).head(4).round(2).to_string())
print("NMF-DOWN genes concentrated in:");print(z_dn.sort_values(ascending=False).head(4).round(2).to_string())
print("\nDONE")
