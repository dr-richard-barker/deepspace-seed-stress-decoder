"""Tool 1 — DSRS: DeepSpace Stress-Recognition System.

Given a plant transcriptomic perturbation signature, recognize which known space stressor(s) it most
resembles, by comparing its seed-program fingerprint (NES across the 122 seed panels) to the reference
stressor library.
"""
import pandas as pd
from . import config
from .projection import project


def _classes():
    return pd.read_csv(config.CONTRAST_CLASS, index_col=0)["stressor_class"].to_dict()


def recognize(signature, panels=None, top=10, method="spearman"):
    """Return a ranked table of reference stressors most similar to the query signature.

    Output columns: stressor, stressor_class, similarity (rank-corr of seed-program fingerprints).
    Plus a per-family aggregate (mean of top similarities) for a coarse family call.
    """
    q = project(signature, panels=panels)["NES"]
    ref = pd.read_csv(config.REF_NES, index_col=0)
    common = q.index.intersection(ref.index)
    if len(common) < 10:
        raise ValueError(f"Only {len(common)} panels overlap; check signature gene IDs (need AGI/TAIR).")
    sim = ref.loc[common].corrwith(q.loc[common], method=method).sort_values(ascending=False)
    cls = _classes()
    out = pd.DataFrame({"stressor": sim.index,
                        "stressor_class": [cls.get(s, "?") for s in sim.index],
                        "similarity": sim.values})
    fam = out.groupby("stressor_class")["similarity"].mean().sort_values(ascending=False)
    return out.head(top).reset_index(drop=True), fam
