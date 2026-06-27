#!/usr/bin/env python
"""Combined environmental-perturbation decoder figure: micro-gravity + radiation (+NMF later)
across seed tissue & germination-state programs, columns grouped by stressor class."""
import os, numpy as np, pandas as pd
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
plt.rcParams.update({"font.family":"sans-serif","font.sans-serif":["Arial","Helvetica","DejaVu Sans"],"savefig.dpi":300,"svg.fonttype":"none","pdf.fonttype":42,"axes.linewidth":0.6})
ROOT=r"C:\Users\drric\Downloads\nmf_seed_decoder"; T=os.path.join(ROOT,"results","tables"); F=os.path.join(ROOT,"results","figures")
nes=pd.read_csv(os.path.join(T,"decoder_nes_matrix_v7.csv"),index_col=0)
fdr=pd.read_csv(os.path.join(T,"decoder_fdr_matrix_v7.csv"),index_col=0)
cls=pd.read_csv(os.path.join(T,"contrast_classes.csv"),index_col=0)["stressor_class"]
order={"microgravity":0,"partial_gravity":1,"hypergravity":2,"tropism_gravi":3,"tropism_photo":4,"low_oxygen":5,"desiccation":6,"osmotic":7,"ethylene":8,"temperature":9,"uv":10,"radiation_GCR":11,"radiation_lowdose":12,"radiation_acute":13,"magnetic":14}
cols=sorted([c for c in nes.columns if c in cls.index], key=lambda c:(order.get(cls[c],9),c))
rows=[i for i in nes.index if i.startswith("gehring_L1_tissue::")]+[i for i in nes.index if i.startswith("germ_state_time::")]
sub=nes.loc[rows,cols]; fsub=fdr.loc[rows,cols]
ccolors={"microgravity":"#4575b4","partial_gravity":"#74add1","hypergravity":"#08306b","tropism_gravi":"#08519c","tropism_photo":"#3690c0","low_oxygen":"#5e3c99","desiccation":"#8c510a","osmotic":"#dfc27d","ethylene":"#1b7837","temperature":"#fdb863","uv":"#c2a5cf","radiation_GCR":"#fdae61","radiation_lowdose":"#f46d43","radiation_acute":"#a50026","magnetic":"#5aae61"}
N=len(cols)
# 2x2 grid: class strip (top-left) + heatmap (bottom-left) SHARE one column => aligned x-axis;
# NES colorbar gets its OWN column so it never squeezes the heatmap.
fig=plt.figure(figsize=(12.5,6.6))
gs=fig.add_gridspec(2,2,width_ratios=[N,0.5],height_ratios=[0.55,len(rows)],wspace=0.015,hspace=0.05)
axc=fig.add_subplot(gs[0,0]); ax=fig.add_subplot(gs[1,0]); cbar_ax=fig.add_subplot(gs[1,1])
classes_present=sorted({cls[c] for c in cols}, key=lambda k:order.get(k,9))
cidx={k:i for i,k in enumerate(classes_present)}
# class strip, exactly spanning the heatmap columns
axc.imshow([[cidx[cls[c]] for c in cols]],aspect="auto",extent=[-0.5,N-0.5,0,1],
           cmap=matplotlib.colors.ListedColormap([ccolors[k] for k in classes_present]))
axc.set_xlim(-0.5,N-0.5); axc.set_ylim(0,1); axc.set_xticks([]); axc.set_yticks([])
axc.set_ylabel("stressor\nclass",fontsize=7,rotation=0,ha="right",va="center")
# class-group labels: centred over each block, rotated 45 deg, lifted ABOVE the strip
start=0
for i in range(1,N+1):
    if i==N or cls[cols[i]]!=cls[cols[start]]:
        k=cls[cols[start]]; ctr=(start+i-1)/2
        axc.text(ctr,1.35,k,rotation=45,ha="left",va="bottom",fontsize=8,fontweight="bold",
                 color=ccolors.get(k,"#333"),clip_on=False)
        start=i
vmax=np.nanmax(np.abs(sub.values))
im=ax.imshow(sub.values,cmap="RdBu_r",vmin=-vmax,vmax=vmax,aspect="auto",extent=[-0.5,N-0.5,len(rows)-0.5,-0.5])
ax.set_xlim(-0.5,N-0.5)
ax.set_xticks(range(N)); ax.set_xticklabels(cols,rotation=60,ha="right",fontsize=7)
ax.set_yticks(range(len(rows))); ax.set_yticklabels([r.split("::")[-1] for r in rows],fontsize=8)
for i in range(sub.shape[0]):
    for j in range(sub.shape[1]):
        v=sub.values[i,j]; q=fsub.values[i,j]
        if pd.notna(v): ax.text(j,i,f"{v:+.1f}{'*' if pd.notna(q) and q<0.25 else ''}",ha="center",va="center",
                                fontsize=5.5,color="white" if abs(v)>0.6*vmax else "black")
cb=fig.colorbar(im,cax=cbar_ax); cb.set_label("NES (induced + / suppressed -)",fontsize=8); cbar_ax.tick_params(labelsize=7)
fig.suptitle(f"DeepSpace perturbation decoder: micro-gravity + low-oxygen + tropism + radiation + hypergravity ({N} contrasts) → seed programs",
             fontsize=11,y=1.06)
fig.savefig(os.path.join(F,"decoder_combined_perturbation_heatmap.png"),dpi=200,bbox_inches="tight")
fig.savefig(os.path.join(F,"decoder_combined_perturbation_heatmap.svg"),bbox_inches="tight")
print("wrote decoder_combined_perturbation_heatmap;",sub.shape[1],"contrasts x",sub.shape[0],"programs")
