#!/usr/bin/env python
"""Phase 3 — visualize decoder NES (seed program x stressor), marking FDR<0.25 with *."""
import os
import numpy as np, pandas as pd
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = os.environ.get("DEEPSPACE_ROOT") or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
T = os.path.join(ROOT, "results", "tables"); F = os.path.join(ROOT, "results", "figures")
os.makedirs(F, exist_ok=True)
nes = pd.read_csv(os.path.join(T, "decoder_nes_matrix.csv"), index_col=0)
fdr = pd.read_csv(os.path.join(T, "decoder_fdr_matrix.csv"), index_col=0)

def heat(rows, title, fname, h=None):
    sub = nes.loc[[r for r in rows if r in nes.index]]
    fsub = fdr.loc[sub.index]
    fig, ax = plt.subplots(figsize=(7, h or max(3, 0.42*len(sub)+1.5)))
    vmax = np.nanmax(np.abs(sub.values)) or 2.0
    im = ax.imshow(sub.values, cmap="RdBu_r", vmin=-vmax, vmax=vmax, aspect="auto")
    ax.set_xticks(range(sub.shape[1])); ax.set_xticklabels(sub.columns, rotation=45, ha="right", fontsize=9)
    ax.set_yticks(range(sub.shape[0])); ax.set_yticklabels([r.split("::")[-1] for r in sub.index], fontsize=8)
    for i in range(sub.shape[0]):
        for j in range(sub.shape[1]):
            v=sub.values[i,j]; q=fsub.values[i,j]
            if pd.notna(v):
                star="*" if (pd.notna(q) and q<0.25) else ""
                ax.text(j,i,f"{v:+.1f}{star}",ha="center",va="center",fontsize=7,
                        color="white" if abs(v)>0.6*vmax else "black")
    ax.set_title(title, fontsize=11)
    cb=fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04); cb.set_label("NES (induced + / suppressed -)", fontsize=8)
    fig.tight_layout(); fig.savefig(os.path.join(F,fname), dpi=200); fig.savefig(os.path.join(F,fname.replace(".png",".svg")))
    print("wrote", fname, sub.shape)

L1 = [i for i in nes.index if i.startswith("gehring_L1_tissue::")]
L2 = [i for i in nes.index if i.startswith("gehring_L2_celltype::")]
GT = [i for i in nes.index if i.startswith("germ_state_time::")]
heat(L1+GT, "Decoder: stressor -> seed tissue & germination-state programs", "decoder_L1_state_heatmap.png")
heat(L2, "Decoder: stressor -> seed cell-type (Gehring L2) programs", "decoder_L2_celltype_heatmap.png")
print("DONE")
