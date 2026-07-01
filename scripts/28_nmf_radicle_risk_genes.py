#!/usr/bin/env python
"""Which NMF-responsive genes drive the null-magnetic-field 'risk' at the root radicle?

The NMF-up gene set localizes to the radicle apical meristem (cluster 14) with z = +7.96
(results/tables/nmf_localization.csv). This script identifies the individual genes responsible:
NMF-up genes that are specifically expressed in the radicle apical meristem, with their TAIR IDs
and gene symbols/names (from the Maffei source annotation).

Outputs:
  results/tables/nmf_radicle_risk_genes.csv
  results/figures/nmf_radicle_risk_heatmap.{png,svg}
"""
import os, numpy as np, pandas as pd
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt

ROOT=os.environ.get("DEEPSPACE_ROOT") or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW=os.path.join(ROOT,"data","raw"); NMF=os.path.join(RAW,"nmf_maffei")
PAN=os.path.join(ROOT,"panels"); T=os.path.join(ROOT,"results","tables"); F=os.path.join(ROOT,"results","figures")

TARGET="radicle apical meristem (cl14)"
SPEC_MIN=1.0      # a gene "belongs to the radicle risk" if its radicle specificity z >= this

# ---------- 1) NMF gene directions (built by script 08) ----------
direction=pd.read_csv(os.path.join(T,"nmf_gene_directions.csv"),index_col=0)["nmf_shoot_late_log2"]
nmf_up=set(direction[direction>0.1].index)

# ---------- 2) germinating-seed cell-type expression specificity (as in script 08) ----------
ann=pd.read_csv(os.path.join(PAN,"germination_cluster_annotations.csv")); ann["cluster"]=ann.cluster.astype(str)
cl2lab={c:f"{n} (cl{c})" for c,n in zip(ann.cluster,ann.cell_type)}
lab2org={cl2lab[c]:o for c,o in zip(ann.cluster,ann.organ)}
mat=pd.read_csv(os.path.join(RAW,"germination","GSE182331_expression_mat.csv.gz"),index_col=0)
meta=pd.read_csv(os.path.join(RAW,"germination","meta.tsv"),sep="\t")
meta["cellid"]=meta["sample"].astype(str)+"."+meta["Barcode"].astype(str)
meta["ct"]=meta["cluster"].astype(str).map(cl2lab)
meta=meta.set_index("cellid").reindex(mat.columns).dropna(subset=["ct"])
mat=mat[meta.index]
pb=mat.T.groupby(meta["ct"]).sum().T                       # genes x celltypes (summed counts)
pb=pb/pb.sum(0)*1e6; pb=np.log1p(pb)                       # CPM-log
spec=pb.sub(pb.mean(1),axis=0).div(pb.std(1).replace(0,np.nan),axis=0).dropna()

# ---------- 3) NMF-up genes expressed & specific to the radicle apical meristem ----------
genes=[g for g in nmf_up if g in spec.index]
rad=spec.loc[genes,TARGET].sort_values(ascending=False)
risk=rad[rad>=SPEC_MIN].index.tolist()
print(f"NMF-up genes expressed in germination data: {len(genes)}")
print(f"  -> {len(risk)} are specifically expressed in {TARGET} (spec z >= {SPEC_MIN})")

# ---------- 4) gene symbols / names from the Maffei source annotation ----------
def parse_code(code):
    """Split a 'SYMBOL, full name' style gene_code into (symbol, name).
    A symbol is short and space-free; otherwise it's treated as a description."""
    if not isinstance(code,str) or not code.strip(): return "",""
    parts=[p.strip().strip('"') for p in code.split(",") if p.strip()]
    if parts and len(parts[0])<=12 and " " not in parts[0] and not parts[0][0].islower():
        return parts[0], ", ".join(parts[1:])
    return "", code.strip()
sym={}; name={}
def add(tid,s,n):
    if tid not in sym and s: sym[tid]=s
    if tid not in name and n: name[tid]=n
mem=pd.read_csv(os.path.join(NMF,"nmf_cluster_membership.csv"))
for _,r in mem.iterrows():
    s,n=parse_code(r.get("gene_code")); add(r["tair_id"],s,n or str(r.get("gene_function") or "").strip())
h2o2=pd.read_csv(os.path.join(NMF,"nmf_h2o2_panel.csv")).drop_duplicates("tair_id")
for _,r in h2o2.iterrows():
    s,n=parse_code(r.get("gene_code")); add(r["tair_id"],s,n)
poly=pd.read_csv(os.path.join(NMF,"nmf_polyphenol_gene_panel.csv")).drop_duplicates("tair_id")
for _,r in poly.iterrows():
    add(r["tair_id"],"",str(r.get("gene_name") or "").strip())

# ---------- 5) table ----------
tab=pd.DataFrame({
    "TAIR_ID":risk,
    "gene_symbol":[sym.get(g,"") or "" for g in risk],
    "gene_name":[name.get(g,"") or "" for g in risk],
    "NMF_shoot_late_log2":[round(float(direction.get(g,np.nan)),3) for g in risk],
    "radicle_apical_meristem_spec_z":[round(float(spec.loc[g,TARGET]),2) for g in risk],
})
tab=tab.sort_values("radicle_apical_meristem_spec_z",ascending=False).reset_index(drop=True)
tab.to_csv(os.path.join(T,"nmf_radicle_risk_genes.csv"),index=False)
print("wrote table:",os.path.join(T,"nmf_radicle_risk_genes.csv"))

# ---------- 6) heatmap: risk genes x germinating-seed cell types (specificity z) ----------
order=["cotyledon","hypocotyl","radicle","provasculature","unassigned"]
cols=sorted(spec.columns,key=lambda c:(order.index(lab2org.get(c,"unassigned")) if lab2org.get(c,"unassigned") in order else 9,c))
H=spec.loc[risk,cols]
# row label = symbol (fallback TAIR)
rowlab=[f"{(sym.get(g) or g)}  {g}" for g in risk]
fig,ax=plt.subplots(figsize=(0.42*len(cols)+4.5,0.34*len(risk)+1.8))
vmax=np.nanpercentile(np.abs(H.values),98)
im=ax.imshow(H.values,cmap="RdBu_r",vmin=-vmax,vmax=vmax,aspect="auto")
ax.set_xticks(range(len(cols))); ax.set_xticklabels(cols,rotation=90,fontsize=7)
ax.set_yticks(range(len(risk))); ax.set_yticklabels(rowlab,fontsize=6.5)
# highlight the target column
tcol=cols.index(TARGET)
ax.add_patch(plt.Rectangle((tcol-0.5,-0.5),1,len(risk),fill=False,edgecolor="black",lw=1.8))
ax.set_title(f"Null-magnetic-field (NMF-up) genes localized to the root radicle\n"
             f"expression specificity (z) across germinating-seed cell types; boxed = {TARGET}",fontsize=8)
cb=fig.colorbar(im,ax=ax,fraction=0.025,pad=0.02); cb.set_label("specificity z",fontsize=7)
fig.tight_layout()
fig.savefig(os.path.join(F,"nmf_radicle_risk_heatmap.png"),dpi=220)
fig.savefig(os.path.join(F,"nmf_radicle_risk_heatmap.svg"))
print("wrote figure:",os.path.join(F,"nmf_radicle_risk_heatmap.png"))
print("\nTop risk genes:\n",tab.head(15).to_string(index=False))
