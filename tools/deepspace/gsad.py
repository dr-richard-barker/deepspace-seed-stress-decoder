"""Tool 2 — GSAD: Germinating-Seed AutoDecoder.

Given bulk transcriptomics (or a signature) from later developmental-stage tissue, model its predicted
effect on the dry/germinating seed: a per cell-type / tissue / stage susceptibility profile.
"""
import pandas as pd
from .projection import project
from .panels import germ_celltype_labels


def decode(signature, panels=None, sig_nes=1.5, sig_fdr=0.25):
    """Return the seed susceptibility profile for a query signature.

    Returns dict with:
      'celltype' : germinating-seed cell types ranked by NES (+ FDR, organ, significant flag)
      'tissue'   : developing-seed tissue (Gehring L1) NES
      'stage'    : germination-stage (12/24/48 hsl) NES
      'all'      : full per-panel projection
    """
    proj = project(signature, panels=panels)
    lab, organ = germ_celltype_labels()

    def subset(prefix, relabel=False):
        rows = [i for i in proj.index if i.startswith(prefix)]
        t = proj.loc[rows].copy()
        if relabel:
            t.index = [lab.get(i, i) for i in t.index]
            t["organ"] = [organ.get(i, "?") for i in t.index]
        t["significant"] = (t["NES"].abs() >= sig_nes) & (t["FDR"] < sig_fdr)
        return t.sort_values("NES", ascending=False)

    return {
        "celltype": subset("germ_cluster::", relabel=True),
        "tissue":   subset("gehring_L1_tissue::"),
        "stage":    subset("germ_state_time::"),
        "all":      proj,
    }
