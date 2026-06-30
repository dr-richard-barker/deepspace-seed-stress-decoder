#!/usr/bin/env python
"""Phase 2/3 — apply germination cluster->cell-type names, re-render named decoder heatmap.

- annotate panel_library germ_cluster panels with cell-type names
- relabel decoder NES/FDR germ_cluster rows -> named cell types (grouped by organ)
- render results/figures/decoder_germination_named_heatmap.{png,svg}
"""
import os
import numpy as np, pandas as pd
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = os.environ.get("DEEPSPACE_ROOT") or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAN  = os.path.join(ROOT, "panels"); T = os.path.join(ROOT,"results","tables"); F = os.path.join(ROOT,"results","figures")

ann = pd.read_csv(os.path.join(PAN, "germination_cluster_annotations.csv"))
ann["cluster"] = ann["cluster"].astype(str)
name = dict(zip(ann.cluster, ann.cell_type)); organ = dict(zip(ann.cluster, ann.organ))
# organ ordering for readability
order = {"cotyledon":0,"hypocotyl":1,"radicle":2,"provasculature":3,"unassigned":4}

# 1) annotate panel library
pl = pd.read_csv(os.path.join(PAN,"panel_library.csv"))
def lbl(row):
    if row.panel_source=="germ_cluster":
        c=str(row.panel_group); return f"{name.get(c,c)} (cl{c})"
    return row.panel_group
pl["panel_label"] = pl.apply(lbl, axis=1)
pl.to_csv(os.path.join(PAN,"panel_library_annotated.csv"), index=False)

# 2) relabel decoder germ_cluster rows + render
nes = pd.read_csv(os.path.join(T,"decoder_nes_matrix.csv"), index_col=0)
fdr = pd.read_csv(os.path.join(T,"decoder_fdr_matrix.csv"), index_col=0)
rows=[i for i in nes.index if i.startswith("germ_cluster::")]
def keyfn(i):
    c=i.split("::")[1]; return (order.get(organ.get(c,"unassigned"),9), c)
rows=sorted(rows, key=keyfn)
labels=[f"{name.get(i.split('::')[1], i)} (cl{i.split('::')[1]})" for i in rows]
sub=nes.loc[rows]; fsub=fdr.loc[rows]

fig,ax=plt.subplots(figsize=(7.5, 0.45*len(rows)+1.5))
vmax=np.nanmax(np.abs(sub.values)) or 2.0
im=ax.imshow(sub.values,cmap="RdBu_r",vmin=-vmax,vmax=vmax,aspect="auto")
ax.set_xticks(range(sub.shape[1])); ax.set_xticklabels(sub.columns,rotation=45,ha="right",fontsize=9)
ax.set_yticks(range(len(rows))); ax.set_yticklabels(labels,fontsize=8)
for i in range(sub.shape[0]):
    for j in range(sub.shape[1]):
        v=sub.values[i,j]; q=fsub.values[i,j]
        if pd.notna(v):
            star="*" if (pd.notna(q) and q<0.25) else ""
            ax.text(j,i,f"{v:+.1f}{star}",ha="center",va="center",fontsize=7,
                    color="white" if abs(v)>0.6*vmax else "black")
ax.set_title("Decoder: stressor -> germinating-seed cell types (named)",fontsize=11)
cb=fig.colorbar(im,ax=ax,fraction=0.046,pad=0.04); cb.set_label("NES (induced + / suppressed -)",fontsize=8)
fig.tight_layout(); fig.savefig(os.path.join(F,"decoder_germination_named_heatmap.png"),dpi=200)
fig.savefig(os.path.join(F,"decoder_germination_named_heatmap.svg"))
print("wrote decoder_germination_named_heatmap; panels annotated ->", pl.shape[0],"rows")
print("named clusters:", {k:name[k] for k in sorted(name, key=int)})
