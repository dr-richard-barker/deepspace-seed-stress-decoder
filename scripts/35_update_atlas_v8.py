#!/usr/bin/env python
"""Phase 6.5 — DeepSpace Seed-Susceptibility ATLAS v8 (Headline deliverable).

Integrates the expanded 49-contrast, 15-family reference library:
  - Physics: gravity, radiation, magnetic_NMF, tropism, uv
  - Atmosphere: hypobaria (Exploration Atmosphere decoupled), low_oxygen
  - Chemistry: redox_ros (Redox Decoder CVAE + specific species)
  - Environment: desiccation, osmotic/drought, temperature, cold
  - Injury & Physiology: wounding, hormone_signaling, nutrient_stress

Computes:
  1. Multi-stressor convergence ranking across all 15 germinating-seed cell types.
  2. Multi-stressor convergence across developmental stages (dry seed, 12hsl, 24hsl, 48hsl)
     and developing-seed tissues (Embryo, Endosperm, Seed Coat).
  3. Re-evaluates the core hypothesis: Does the radicle apical meristem / root cap remain
     the multi-stressor convergence apex under expanded physical & biochemical challenges?

Outputs:
  results/tables/deepspace_atlas_nes_v8.csv
  results/tables/deepspace_atlas_family_v8.csv
  results/tables/deepspace_atlas_convergence_v8.csv
  results/tables/deepspace_atlas_tissue_stage_convergence_v8.csv
  results/figures/deepspace_seed_atlas_v8.{png,svg}
  results/figures/deepspace_atlas_tissue_stage_v8.{png,svg}
"""
import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans"],
    "savefig.dpi": 300,
    "svg.fonttype": "none",
    "pdf.fonttype": 42,
    "axes.linewidth": 0.6
})

ROOT = os.environ.get("DEEPSPACE_ROOT") or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
T = os.path.join(ROOT, "results", "tables")
F = os.path.join(ROOT, "results", "figures")
PAN = os.path.join(ROOT, "panels")

# Load v8 matrices
NES = pd.read_csv(os.path.join(T, "decoder_nes_matrix_v8.csv"), index_col=0)
FDR = pd.read_csv(os.path.join(T, "decoder_fdr_matrix_v8.csv"), index_col=0)
cls = pd.read_csv(os.path.join(T, "contrast_classes.csv"), index_col=0)["stressor_class"].to_dict()

# Germination cluster annotations
ann = pd.read_csv(os.path.join(PAN, "germination_cluster_annotations.csv"))
ann["cluster"] = ann.cluster.astype(str)
cl2lab = {c: f"{n} (cl{c})" for c, n in zip(ann.cluster, ann.cell_type)}
organ = dict(zip([cl2lab[c] for c in ann.cluster], ann.organ))

# 1. Map contrasts to 15 stressor families
def map_family(contrast_name):
    c_class = cls.get(contrast_name, "other")
    if c_class in ("microgravity", "partial_gravity", "hypergravity"):
        return "gravity"
    if c_class in ("tropism_gravi", "tropism_photo"):
        return "tropism"
    if c_class in ("radiation_GCR", "radiation_acute", "radiation_lowdose"):
        return "radiation"
    if c_class in ("hormone_auxin", "hormone_ga", "hormone_cytokinin", "hormone_br", "ethylene"):
        return "hormone_signaling"
    return c_class

contrast_family_map = {c: map_family(c) for c in NES.columns}

families = [
    "gravity", "tropism", "radiation", "low_oxygen", "hypobaria",
    "redox_ros", "desiccation", "osmotic", "temperature", "cold",
    "wounding", "hormone_signaling", "nutrient_stress", "uv", "magnetic_NMF"
]

SIG_NES = 1.5
SIG_FDR = 0.25
SIG_NMFZ = 2.0

# NMF localization column
nmf_file = os.path.join(T, "nmf_localization.csv")
nmf = pd.read_csv(nmf_file, index_col=0)["NMF_up_localization_z"] if os.path.exists(nmf_file) else pd.Series(dtype=float)

# =========================================================================
# Part A: Cell-Type Atlas (Germination Clusters 1-15)
# =========================================================================
g = [i for i in NES.index if i.startswith("germ_cluster::")]
A = NES.loc[g].copy()
Af = FDR.loc[g].copy()
A.index = [cl2lab[i.split("::")[1]] for i in A.index]
Af.index = A.index
A.to_csv(os.path.join(T, "deepspace_atlas_nes_v8.csv"))

famhit = pd.DataFrame(0, index=A.index, columns=families)
famval = pd.DataFrame(0.0, index=A.index, columns=families)

for ct in A.index:
    for f_ in families:
        if f_ == "magnetic_NMF":
            z = nmf.get(ct, np.nan)
            if pd.notna(z) and abs(z) >= SIG_NMFZ:
                famhit.loc[ct, "magnetic_NMF"] = 1
                famval.loc[ct, "magnetic_NMF"] = z
            continue
            
        cols = [c for c in A.columns if contrast_family_map.get(c) == f_]
        if not cols:
            continue
        sig = [(abs(A.loc[ct, c]) >= SIG_NES and Af.loc[ct, c] < SIG_FDR) for c in cols]
        if any(sig):
            famhit.loc[ct, f_] = 1
            best = max([A.loc[ct, c] for c, s in zip(cols, sig) if s], key=abs)
            famval.loc[ct, f_] = best

conv = famhit.sum(1).sort_values(ascending=False)
out_conv = pd.DataFrame({
    "cell_type": conv.index,
    "organ": [organ.get(c, "?") for c in conv.index],
    "n_families": conv.values,
    "families_hit": [", ".join([f for f in families if famhit.loc[c, f]]) for c in conv.index]
})

out_conv.to_csv(os.path.join(T, "deepspace_atlas_convergence_v8.csv"), index=False)
famhit.to_csv(os.path.join(T, "deepspace_atlas_family_v8.csv"))

# --- Plot Cell-Type Atlas Heatmap + Convergence Bars ---
order_org = {"radicle": 0, "provasculature": 1, "hypocotyl": 2, "cotyledon": 3, "unassigned": 4}
rows = sorted(famval.index, key=lambda c: (-conv[c], order_org.get(organ.get(c, "z"), 9)))
V = famval.loc[rows, families]
vmax = np.nanmax(np.abs(V.values)) or 1

fig = plt.figure(figsize=(14, 0.45 * len(rows) + 2.2))
gs = fig.add_gridspec(1, 3, width_ratios=[len(families), 0.4, 2.2], wspace=0.35)
ax = fig.add_subplot(gs[0])
cax = fig.add_subplot(gs[1])
axb = fig.add_subplot(gs[2])

im = ax.imshow(V.values, cmap="RdBu_r", vmin=-vmax, vmax=vmax, aspect="auto")
ax.set_xticks(range(len(families)))
ax.set_xticklabels(families, rotation=45, ha="right", fontsize=9, fontweight="medium")
ax.set_yticks(range(len(rows)))
ax.set_yticklabels(rows, fontsize=8.5)

for i, ct in enumerate(rows):
    for j, f_ in enumerate(families):
        if famhit.loc[ct, f_]:
            ax.text(j, i, "*", ha="center", va="center", fontsize=13, fontweight="bold", color="black")

ax.set_title("DeepSpace Seed-Susceptibility Atlas v8 (49 contrasts, 15 families)\n* = significant hit (|NES| >= 1.5 & FDR < 0.25; NMF |z| >= 2)", fontsize=10.5, pad=12)
cb = fig.colorbar(im, cax=cax)
cb.set_label("Signed Strength (NES / NMF z)", fontsize=8)
cax.tick_params(labelsize=7.5)

# Convergence bars
colors = [
    "#c0392b" if "radicle" in organ.get(c, "") or "columella" in c.lower() else
    "#2980b9" if "provasculature" in organ.get(c, "") else
    "#27ae60" if "cotyledon" in organ.get(c, "") else
    "#8e44ad" if "hypocotyl" in organ.get(c, "") else "#7f8c8d"
    for c in rows
]
axb.barh(range(len(rows)), conv[rows].values, color=colors, height=0.7)
axb.invert_yaxis()
axb.set_ylim(len(rows) - 0.5, -0.5)
axb.set_yticks([])
axb.set_xlim(0, len(families) + 1.0)
axb.set_xlabel(f"Multi-Stressor Convergence (/{len(families)} families)", fontsize=8.5)
axb.set_title("Convergence Ranking", fontsize=9.5)

for i, ct in enumerate(rows):
    axb.text(conv[ct] + 0.25, i, f"{int(conv[ct])}", va="center", fontsize=8, fontweight="bold")

fig.savefig(os.path.join(F, "deepspace_seed_atlas_v8.png"), dpi=300, bbox_inches="tight")
fig.savefig(os.path.join(F, "deepspace_seed_atlas_v8.svg"), bbox_inches="tight")
plt.close(fig)

# =========================================================================
# Part B: Developmental Stage & Tissue Atlas
# =========================================================================
stage_rows = {
    "Dry Seed (0h)": "germ_state_time::dry_seed",
    "Early Germination (12 hsl)": "germ_state_time::12hsl",
    "Mid Germination (24 hsl)": "germ_state_time::24hsl",
    "Late Germination (48 hsl)": "germ_state_time::48hsl",
}
tissue_rows = {
    "Embryo": "gehring_L1_tissue::Embryo",
    "Endosperm": "gehring_L1_tissue::Endosperm",
    "Seed Coat": "gehring_L1_tissue::Seed coat",
    "Funiculus": "gehring_L1_tissue::Funiculus",
    "Ovule": "gehring_L1_tissue::Ovule",
}

combined_groups = {**stage_rows, **tissue_rows}
st_famhit = pd.DataFrame(0, index=list(combined_groups.keys()), columns=families)
st_famval = pd.DataFrame(0.0, index=list(combined_groups.keys()), columns=families)

for lab, row in combined_groups.items():
    if row not in NES.index:
        continue
    for f_ in families:
        if f_ == "magnetic_NMF":
            continue
        cols = [c for c in NES.columns if contrast_family_map.get(c) == f_]
        if not cols:
            continue
        sig = [(abs(NES.loc[row, c]) >= SIG_NES and FDR.loc[row, c] < SIG_FDR) for c in cols]
        if any(sig):
            st_famhit.loc[lab, f_] = 1
            st_famval.loc[lab, f_] = max([NES.loc[row, c] for c, s in zip(cols, sig) if s], key=abs)

st_conv = st_famhit.sum(1)
st_out = pd.DataFrame({
    "entity": st_conv.index,
    "category": ["Stage" if k in stage_rows else "Tissue" for k in st_conv.index],
    "n_families": st_conv.values,
    "families_hit": [", ".join([f for f in families if st_famhit.loc[c, f]]) for c in st_conv.index]
})
st_out.to_csv(os.path.join(T, "deepspace_atlas_tissue_stage_convergence_v8.csv"), index=False)

# Plot Stage & Tissue Atlas
fig_st, (ax_st, axb_st) = plt.subplots(1, 2, figsize=(13, 4.5), gridspec_kw={"width_ratios": [len(families), 3], "wspace": 0.3})
im_st = ax_st.imshow(st_famval.values, cmap="RdBu_r", vmin=-3.0, vmax=3.0, aspect="auto")
ax_st.set_xticks(range(len(families)))
ax_st.set_xticklabels(families, rotation=45, ha="right", fontsize=8.5)
ax_st.set_yticks(range(len(combined_groups)))
ax_st.set_yticklabels(list(combined_groups.keys()), fontsize=9)

for i, lab in enumerate(combined_groups.keys()):
    for j, f_ in enumerate(families):
        if st_famhit.loc[lab, f_]:
            ax_st.text(j, i, "*", ha="center", va="center", fontsize=12, fontweight="bold")

ax_st.set_title("Stage & Tissue Susceptibility v8", fontsize=10)

axb_st.barh(range(len(combined_groups)), st_conv.values, color="#34495e", height=0.6)
axb_st.invert_yaxis()
axb_st.set_yticks([])
axb_st.set_xlim(0, len(families) + 1.0)
axb_st.set_xlabel("n families hit", fontsize=8.5)
axb_st.set_title("Stage / Tissue Convergence", fontsize=9.5)
for i, lab in enumerate(combined_groups.keys()):
    axb_st.text(st_conv[lab] + 0.2, i, str(int(st_conv[lab])), va="center", fontsize=8, fontweight="bold")

fig_st.savefig(os.path.join(F, "deepspace_atlas_tissue_stage_v8.png"), dpi=300, bbox_inches="tight")
fig_st.savefig(os.path.join(F, "deepspace_atlas_tissue_stage_v8.svg"), bbox_inches="tight")
plt.close(fig_st)

print("==== DeepSpace Seed-Susceptibility Atlas v8: Convergence Ranking ====")
print(out_conv.to_string(index=False))

print("\n==== Stage & Tissue Convergence v8 ====")
print(st_out.to_string(index=False))

print("\nDONE")
