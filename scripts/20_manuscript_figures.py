#!/usr/bin/env python
"""Phase 6.6 — npj Microgravity figure set F1-F6 v8 (49 contrasts, 15 families).

Generates submission-ready publication figures at 300 dpi (Arial, SVG + PNG):
  F1: Concept workflow schematic (dual tools + multi-stimuli decoders integration)
  F2: DSRS stress reference library (key seed programs x 49 contrasts across 15 families)
  F3: Seed reference + embryo-lineage validation (recovering textbook lineages)
  F4: GSAD seed cell-type susceptibility (15 germination cell types x 49 contrasts)
  F5: DeepSpace seed-susceptibility atlas v8 (cell-type x 15 families + convergence bars)
  F6: Multi-stressor convergence model & testable falsification hypotheses

Outputs:
  report/figures_npj/F{1..6}_*.{png,svg}
  docs/assets/figures/F{1..6}_*.{png,svg}
"""
import os
import shutil
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import matplotlib.colors as mcolors

ROOT = os.environ.get("DEEPSPACE_ROOT") or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
T = os.path.join(ROOT, "results", "tables")
FIG = os.path.join(ROOT, "results", "figures")
OUT = os.path.join(ROOT, "report", "figures_npj")
DOCS_FIG = os.path.join(ROOT, "docs", "assets", "figures")
os.makedirs(OUT, exist_ok=True)
os.makedirs(DOCS_FIG, exist_ok=True)

plt.rcParams.update({
    "font.size": 9,
    "font.family": "sans-serif",
    "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans"],
    "savefig.dpi": 300,
    "svg.fonttype": "none",
    "pdf.fonttype": 42,
    "axes.linewidth": 0.6
})

# 15 distinct family colors
FAMCOL = {
    "gravity": "#4575b4",
    "tropism": "#3690c0",
    "radiation": "#d73027",
    "low_oxygen": "#5e3c99",
    "hypobaria": "#3182bd",
    "redox_ros": "#e6550d",
    "desiccation": "#8c510a",
    "osmotic": "#dfc27d",
    "temperature": "#fdb863",
    "cold": "#74add1",
    "wounding": "#b2182b",
    "hormone_signaling": "#1b7837",
    "nutrient_stress": "#7b3294",
    "uv": "#c2a5cf",
    "magnetic_NMF": "#1a9850"
}

def box(ax, x, y, w, h, text, fc, ec="#333", fs=8.5, tc="black", fw="normal"):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.08",
                                fc=fc, ec=ec, lw=1.2))
    ax.text(x + w/2, y + h/2, text, ha="center", va="center", fontsize=fs, color=tc,
            fontweight=fw, wrap=True)

def arrow(ax, x1, y1, x2, y2, c="#333", lw=1.8):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle="-|>", mutation_scale=16, lw=lw, color=c))

# =========================================================================
# F1: Concept Workflow Schematic
# =========================================================================
fig, ax = plt.subplots(figsize=(10.5, 6.2))
ax.set_xlim(0, 11)
ax.set_ylim(0, 10.5)
ax.axis("off")

ax.text(5.5, 9.9, "DeepSpace Plant-Stress → Germinating-Seed Decoding Framework",
        ha="center", fontsize=13, fontweight="bold", color="#14304f")

# Multi-Stimuli Input Hub
box(ax, 0.4, 5.0, 2.4, 3.2,
    "Input Perturbation Signatures\n\n• Microgravity & GCR (OSDR)\n• Decoupled Hypobaria (TabPFN)\n• Redox Latent Remodeling (CVAE)\n• MASTA Microarrays (Cold, Wounds)\n• Hormone & Nutrient Circuits",
    "#f8f9fa", ec="#6c757d", fs=7.8)

# Tool 1: DSRS
box(ax, 3.5, 6.8, 3.8, 2.1,
    "Tool 1 — DSRS\nDeepSpace Stress-Recognition System\n\nMatches query seed-fingerprint against\n49 reference contrasts across 15 families\n(Gravity, Hypobaria, Radiation, Redox, Tropisms...)",
    "#dbe7f3", ec="#2b6cb0", fs=8)

# Tool 2: GSAD
box(ax, 3.5, 2.6, 3.8, 2.1,
    "Tool 2 — GSAD\nGerminating-Seed AutoDecoder\n\nProjects bulk transcriptomes onto\n123 single-cell seed panels\n(Gehring dev + Liew/Lewsey germination)",
    "#ddf2e4", ec="#276749", fs=8)

# Atlas Deliverable
box(ax, 8.0, 4.4, 2.6, 2.6,
    "DeepSpace Seed-\nSusceptibility Atlas v8\n\n• 15 Germination Cell Types\n• 49 Stressor Contrasts\n• 15 Stressor Families\n• Stage Axis: 0h→12h→24h→48h",
    "#fde8d0", ec="#c05621", fs=8)

# Arrows connecting components
arrow(ax, 2.8, 6.8, 3.5, 7.8)
arrow(ax, 2.8, 5.2, 3.5, 3.6)
arrow(ax, 7.3, 7.8, 8.0, 6.0)
arrow(ax, 7.3, 3.6, 8.0, 5.4)

ax.text(5.4, 6.5, "“Which space stressor does it resemble?”", ha="center", fontsize=7.5, style="italic", color="#1c4a72")
ax.text(5.4, 2.3, "“What effect does it have on the seed?”", ha="center", fontsize=7.5, style="italic", color="#1a7a3a")

# Headline callout box
box(ax, 7.4, 0.8, 3.4, 1.4,
    "Headline Result (v8):\nColumella / Root Cap = 14 / 15 families\nRadicle Apical Meristem = 10 / 15 families\nEarly Germination (12h) = Most Vulnerable",
    "#fff3bf", ec="#b7791f", fs=8, fw="bold")
arrow(ax, 9.3, 4.4, 9.1, 2.2, c="#b7791f")

# On-demand MASTA projection callout
box(ax, 0.4, 0.8, 2.8, 1.3,
    "On-Demand MASTA Bridge:\ndeepspace masta-project\nInstant projection of 592\nArabidopsis microarray contrasts",
    "#edf2f7", ec="#4a5568", fs=7.5)
arrow(ax, 3.2, 1.4, 3.5, 2.8, c="#4a5568")

fig.savefig(os.path.join(OUT, "F1_concept_workflow.png"), bbox_inches="tight")
fig.savefig(os.path.join(OUT, "F1_concept_workflow.svg"), bbox_inches="tight")
fig.savefig(os.path.join(DOCS_FIG, "F1_concept_workflow.png"), bbox_inches="tight")
fig.savefig(os.path.join(DOCS_FIG, "F1_concept_workflow.svg"), bbox_inches="tight")
plt.close(fig)

# =========================================================================
# Shared Heatmap Renderer
# =========================================================================
def render_heatmap(MAT, FDR, rows, cols, title, fname, classbar=None, h_per=0.42, cbar_label="NES"):
    N = len(cols)
    fig = plt.figure(figsize=(max(8.5, 0.30 * N + 3.5), h_per * len(rows) + 2.4))
    gs = fig.add_gridspec(2, 2, width_ratios=[N, 0.5], height_ratios=[0.35, len(rows)],
                          wspace=0.05, hspace=0.05)
    axc = fig.add_subplot(gs[0, 0])
    ax = fig.add_subplot(gs[1, 0])
    cax = fig.add_subplot(gs[1, 1])

    if classbar is not None:
        fams_in_order = []
        for c in cols:
            f = classbar.get(c, "other")
            if f not in fams_in_order:
                fams_in_order.append(f)
        cidx = {k: i for i, k in enumerate(fams_in_order)}
        axc.imshow([[cidx[classbar.get(c, "other")] for c in cols]], aspect="auto", extent=[-0.5, N-0.5, 0, 1],
                   cmap=mcolors.ListedColormap([FAMCOL.get(k, "#999") for k in fams_in_order]))
        axc.set_xlim(-0.5, N-0.5)
        axc.set_ylim(0, 1)
        axc.set_xticks([])
        axc.set_yticks([])
        axc.set_ylabel("family", fontsize=7.5, rotation=0, ha="right", va="center")

        start = 0
        for i in range(1, N + 1):
            if i == N or classbar.get(cols[i]) != classbar.get(cols[start]):
                k = classbar.get(cols[start])
                ctr = (start + i - 1) / 2
                axc.text(ctr, 1.35, k, rotation=45, ha="left", va="bottom", fontsize=7.5, fontweight="bold",
                         color=FAMCOL.get(k, "#333"), clip_on=False)
                start = i
        fig.suptitle(title, fontsize=11, y=1.05)
    else:
        axc.axis("off")
        axc.set_title(title, fontsize=10, pad=6)

    vmax = np.nanmax(np.abs(MAT)) or 1
    im = ax.imshow(MAT, cmap="RdBu_r", vmin=-vmax, vmax=vmax, aspect="auto", extent=[-0.5, N-0.5, len(rows)-0.5, -0.5])
    ax.set_xlim(-0.5, N-0.5)
    ax.set_xticks(range(N))
    ax.set_xticklabels(cols, rotation=60, ha="right", fontsize=7)
    ax.set_yticks(range(len(rows)))
    ax.set_yticklabels(rows, fontsize=8)

    if FDR is not None:
        for i in range(len(rows)):
            for j in range(N):
                if pd.notna(FDR[i, j]) and FDR[i, j] < 0.25:
                    ax.text(j, i, "*", ha="center", va="center", fontsize=8.5, fontweight="bold")

    cb = fig.colorbar(im, cax=cax)
    cb.set_label(cbar_label, fontsize=8)
    cax.tick_params(labelsize=7)

    fig.savefig(os.path.join(OUT, fname + ".png"), bbox_inches="tight")
    fig.savefig(os.path.join(OUT, fname + ".svg"), bbox_inches="tight")
    fig.savefig(os.path.join(DOCS_FIG, fname + ".png"), bbox_inches="tight")
    fig.savefig(os.path.join(DOCS_FIG, fname + ".svg"), bbox_inches="tight")
    plt.close(fig)

# Load v8 matrices
nes = pd.read_csv(os.path.join(T, "decoder_nes_matrix_v8.csv"), index_col=0)
fdr = pd.read_csv(os.path.join(T, "decoder_fdr_matrix_v8.csv"), index_col=0)
cls = pd.read_csv(os.path.join(T, "contrast_classes.csv"), index_col=0)["stressor_class"].to_dict()

def get_fam(c):
    c_class = cls.get(c, "other")
    if c_class in ("microgravity", "partial_gravity", "hypergravity"):
        return "gravity"
    if c_class in ("tropism_gravi", "tropism_photo"):
        return "tropism"
    if c_class in ("radiation_GCR", "radiation_acute", "radiation_lowdose"):
        return "radiation"
    if c_class in ("hormone_auxin", "hormone_ga", "hormone_cytokinin", "hormone_br", "ethylene"):
        return "hormone_signaling"
    return c_class

fam_map = {c: get_fam(c) for c in nes.columns}

# Logical order for plotting columns by family
fam_order = [
    "gravity", "tropism", "radiation", "low_oxygen", "hypobaria",
    "redox_ros", "desiccation", "osmotic", "temperature", "cold",
    "wounding", "hormone_signaling", "nutrient_stress", "uv"
]
cols = sorted(nes.columns, key=lambda c: (fam_order.index(fam_map[c]) if fam_map[c] in fam_order else 99, c))

# =========================================================================
# F2: DSRS Stress Library Heatmap (Key Seed Programs x 49 Contrasts)
# =========================================================================
prog = [i for i in nes.index if i.startswith("gehring_L1_tissue::")] + [i for i in nes.index if i.startswith("germ_state_time::")]
M = nes.loc[prog, cols].values
Fd = fdr.loc[prog, cols].values
render_heatmap(M, Fd, [r.split("::")[-1] for r in prog], cols,
               f"Figure 2. DSRS Stress Reference Library ({len(cols)} contrasts across 15 families → seed programs)",
               "F2_stress_library", classbar=fam_map, cbar_label="NES (induced + / suppressed -)")

# =========================================================================
# F4: GSAD Germ Cell-Type Susceptibility (15 Germ Cell Types x 49 Contrasts)
# =========================================================================
ann = pd.read_csv(os.path.join(ROOT, "panels", "germination_cluster_annotations.csv"))
ann["cluster"] = ann.cluster.astype(str)
cl2lab = {c: f"{n} (cl{c})" for c, n in zip(ann.cluster, ann.cell_type)}
g = [i for i in nes.index if i.startswith("germ_cluster::")]
glab = [cl2lab[i.split("::")[1]] for i in g]
render_heatmap(nes.loc[g, cols].values, fdr.loc[g, cols].values, glab, cols,
               "Figure 4. GSAD: Stressor → Germinating-Seed Cell-Type Susceptibility Profile",
               "F4_gsad_susceptibility", classbar=fam_map, cbar_label="NES")

# =========================================================================
# F3: Seed Reference & Embryo Lineage Validation
# =========================================================================
for ext in (".png", ".svg"):
    src_f3 = os.path.join(FIG, f"embryo_lineage_heatmap{ext}")
    if os.path.exists(src_f3):
        shutil.copy(src_f3, os.path.join(OUT, f"F3_seed_reference_embryo_lineage{ext}"))
        shutil.copy(src_f3, os.path.join(DOCS_FIG, f"F3_seed_reference_embryo_lineage{ext}"))

# =========================================================================
# F5: DeepSpace Atlas v8
# =========================================================================
for ext in (".png", ".svg"):
    src_f5 = os.path.join(FIG, f"deepspace_seed_atlas_v8{ext}")
    if os.path.exists(src_f5):
        shutil.copy(src_f5, os.path.join(OUT, f"F5_deepspace_atlas{ext}"))
        shutil.copy(src_f5, os.path.join(DOCS_FIG, f"F5_deepspace_atlas{ext}"))

# =========================================================================
# F6: Radicle Growth-Point Multi-Stressor Convergence Model
# =========================================================================
fig6, ax6 = plt.subplots(figsize=(9.2, 6.8))
ax6.set_xlim(0, 10.5)
ax6.set_ylim(0, 10.5)
ax6.axis("off")

ax6.text(5.25, 10.0, "Figure 6. Radicle Growth-Point: Deep-Space Multi-Stressor Convergence Model",
         ha="center", fontsize=11.5, fontweight="bold", color="#14304f")

# Central Hotspot Node
box(ax6, 3.6, 4.2, 3.3, 1.8,
    "RADICLE CONVERGENCE HOTSPOT\n\n• Columella / Root Cap (+QC): 14/15 families\n• Radicle Apical Meristem: 10/15 families\n• Radicle Epidermis: 8/15 families",
    "#fff3bf", ec="#b7791f", fs=8.2, fw="bold")

# Incoming Stress Vectors
stressors = [
    ("Null Magnetic Field\n(NMF z = +7.96)", "magnetic_NMF", 0.6, 7.8),
    ("Decoupled Hypobaria\n(50 kPa NormO2 NES=+1.98)", "hypobaria", 0.6, 5.6),
    ("Microgravity\n(light-gated response)", "gravity", 0.6, 3.4),
    ("Radiation / GCR\n(provascular induction)", "radiation", 0.6, 1.2),
    ("Gravitropism\n(root-tip sensor)", "tropism", 7.5, 7.8),
    ("Reactive Oxygen Species\n(CVAE spaceflight shift)", "redox_ros", 7.5, 5.6),
    ("Mechanical Wounding\n(vibration/shear NES=+1.59)", "wounding", 7.5, 3.4),
]

for txt, famk, x, y in stressors:
    box(ax6, x, y - 0.5, 2.4, 1.15, txt, mcolors.to_rgba(FAMCOL[famk], 0.20), ec=FAMCOL[famk], fs=7.5, fw="bold")
    if x < 5:
        arrow(ax6, x + 2.4, y + 0.05, 3.6, 5.1, c=FAMCOL[famk], lw=1.6)
    else:
        arrow(ax6, x, y + 0.05, 6.9, 5.1, c=FAMCOL[famk], lw=1.6)

# Developmental Origin Box
box(ax6, 7.3, 1.2, 2.8, 1.2,
    "Developmental Origin:\nEmbryonic Hypophysis\n→ Radicle Apical Meristem",
    "#edf2f7", ec="#718096", fs=7.5)
arrow(ax6, 8.2, 2.4, 6.5, 4.2, c="#718096")

# Falsification Hypotheses
box(ax6, 0.6, 0.1, 4.4, 0.9,
    "H1: NNMF germination induces radicle meristem markers; abolished in cry1cry2.",
    "#f7fafc", ec="#cbd5e0", fs=6.8)
box(ax6, 5.4, 0.1, 4.7, 0.9,
    "H2: Normoxic hypobaria (50 kPa) alters root columella auxin gradients.",
    "#f7fafc", ec="#cbd5e0", fs=6.8)

fig6.savefig(os.path.join(OUT, "F6_convergence_model.png"), bbox_inches="tight")
fig6.savefig(os.path.join(OUT, "F6_convergence_model.svg"), bbox_inches="tight")
fig6.savefig(os.path.join(DOCS_FIG, "F6_convergence_model.png"), bbox_inches="tight")
fig6.savefig(os.path.join(DOCS_FIG, "F6_convergence_model.svg"), bbox_inches="tight")
plt.close(fig6)

print(f"npj Microgravity figure set v8 successfully written to:\n  {OUT}\n  {DOCS_FIG}")
