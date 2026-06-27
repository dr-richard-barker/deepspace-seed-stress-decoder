#!/usr/bin/env python
"""Phase 2 — build cell-type / state marker panels from both seed atlases.

Outputs tidy long-format panel tables under panels/ :
  panel_source, panel_group, gene, rank, logfoldchanges, pvals_adj, score
"""
import os, gzip
import numpy as np, pandas as pd, scanpy as sc
from scipy.io import mmread
from scipy.sparse import csr_matrix

ROOT = r"C:\Users\drric\Downloads\nmf_seed_decoder"
PROC = os.path.join(ROOT, "data", "processed")
RAW  = os.path.join(ROOT, "data", "raw")
PAN  = os.path.join(ROOT, "panels")
os.makedirs(PAN, exist_ok=True)
sc.settings.verbosity = 1

TOP = 50
def top_markers(adata, groupby, source, min_cells=20):
    vc = adata.obs[groupby].value_counts()
    keep = vc[vc >= min_cells].index.tolist()
    a = adata[adata.obs[groupby].isin(keep)].copy()
    a.obs[groupby] = a.obs[groupby].astype("category")
    sc.tl.rank_genes_groups(a, groupby, method="wilcoxon", n_genes=TOP)
    r = a.uns["rank_genes_groups"]
    rows = []
    for grp in r["names"].dtype.names:
        for i in range(len(r["names"][grp])):
            rows.append(dict(panel_source=source, panel_group=str(grp), gene=r["names"][grp][i],
                             rank=i+1, logfoldchanges=float(r["logfoldchanges"][grp][i]),
                             pvals_adj=float(r["pvals_adj"][grp][i]), score=float(r["scores"][grp][i])))
    return pd.DataFrame(rows)

# ---------- Gehring developmental atlas ----------
def build_gehring():
    gd = os.path.join(PROC, "gehring")
    M = mmread(os.path.join(gd, "counts.mtx")).tocsr()          # genes x cells
    genes = [l.strip() for l in open(os.path.join(gd, "genes.txt"))]
    cells = [l.strip() for l in open(os.path.join(gd, "cells.txt"))]
    md = pd.read_csv(os.path.join(gd, "metadata.csv"), index_col=0)
    md = md.loc[cells]
    adata = sc.AnnData(X=csr_matrix(M.T), obs=md.copy(),
                       var=pd.DataFrame(index=genes))
    sc.pp.normalize_total(adata, target_sum=1e4); sc.pp.log1p(adata)
    out = []
    for col, src in [("level_1_annotation","gehring_L1_tissue"),
                     ("level_2_annotation","gehring_L2_celltype"),
                     ("level_3_annotation_abbr","gehring_L3_state")]:
        if col in adata.obs:
            out.append(top_markers(adata, col, src))
    df = pd.concat(out, ignore_index=True)
    df.to_csv(os.path.join(PAN, "gehring_markers.csv"), index=False)
    print("gehring panels:", df.groupby("panel_source")["panel_group"].nunique().to_dict())
    return df

# ---------- Germination atlas (GSE182331 matrix + ArrayExpress meta) ----------
def build_germination():
    gz = os.path.join(RAW, "germination", "GSE182331_expression_mat.csv.gz")
    mat = pd.read_csv(gz, index_col=0)                          # genes x cells
    meta = pd.read_csv(os.path.join(RAW, "germination", "meta.tsv"), sep="\t")
    meta["cellid"] = meta["sample"].astype(str) + "." + meta["Barcode"].astype(str)
    meta = meta.set_index("cellid")
    common = [c for c in mat.columns if c in meta.index]
    print(f"germination cells: matrix {mat.shape[1]}, meta {len(meta)}, matched {len(common)}")
    mat = mat[common]; meta = meta.loc[common]
    adata = sc.AnnData(X=csr_matrix(mat.T.values.astype(np.float32)),
                       obs=meta.copy(), var=pd.DataFrame(index=mat.index))
    adata.obs["cluster"] = adata.obs["cluster"].astype(str)
    adata.obs["time"] = adata.obs["time"].astype(str)
    sc.pp.normalize_total(adata, target_sum=1e4); sc.pp.log1p(adata)
    out = [top_markers(adata, "cluster", "germ_cluster"),
           top_markers(adata, "time", "germ_state_time")]
    df = pd.concat(out, ignore_index=True)
    df.to_csv(os.path.join(PAN, "germination_markers.csv"), index=False)
    print("germination panels:", df.groupby("panel_source")["panel_group"].nunique().to_dict())
    return df

if __name__ == "__main__":
    g = build_gehring()
    h = build_germination()
    lib = pd.concat([g, h], ignore_index=True)
    lib.to_csv(os.path.join(PAN, "panel_library.csv"), index=False)
    print("\nPANEL LIBRARY:", lib.shape[0], "rows;",
          lib["panel_source"].nunique(), "sources;",
          lib.groupby("panel_source")["panel_group"].nunique().sum(), "total panels")
