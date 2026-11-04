#!/usr/bin/env python
"""Phase 6.4 — Build Master Decoder Model v8 (49 contrasts across 16 families).

Combines:
  - 27 existing reference contrasts from decoder_nes_matrix_v7.csv
  - 6 Exploration Atmosphere decoupled hypobaria / hypoxia contrasts
  - 1 Redox Decoder spaceflight latent ROS remodeling contrast
  - 15 Max Planck MASTA contrasts (cold, wounding, drought, auxin, GA, cytokinin, BR, nutrients, ROS)

Projects all new signatures using GSEA-prerank onto the 122+ panels in panels/panel_library.csv.

Outputs:
  results/tables/decoder_nes_matrix_v8.csv
  results/tables/decoder_fdr_matrix_v8.csv
  results/tables/contrast_classes.csv (updated)
"""
import os
import glob
import warnings
import numpy as np
import pandas as pd
import gseapy as gp

warnings.filterwarnings("ignore")

ROOT = os.environ.get("DEEPSPACE_ROOT") or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TABLES = os.path.join(ROOT, "results", "tables")
PANELS = os.path.join(ROOT, "panels")

# Load existing v7 model
en_v7_file = os.path.join(TABLES, "decoder_nes_matrix_v7.csv")
ef_v7_file = os.path.join(TABLES, "decoder_fdr_matrix_v7.csv")
cls_file = os.path.join(TABLES, "contrast_classes.csv")

print(f"Loading existing v7 reference matrices from {TABLES}...")
en = pd.read_csv(en_v7_file, index_col=0)
ef = pd.read_csv(ef_v7_file, index_col=0)
cls = pd.read_csv(cls_file, index_col=0)["stressor_class"].to_dict()

print(f"v7 baseline: {en.shape[1]} contrasts, {en.shape[0]} panels.")

# Load panel library
pl = pd.read_csv(os.path.join(PANELS, "panel_library.csv"))
pl["panel"] = pl.panel_source + "::" + pl.panel_group.astype(str)
gene_sets = {p: g.gene.dropna().unique().tolist() for p, g in pl.groupby("panel")}
print(f"Loaded {len(gene_sets)} panels for GSEA projection.")

# Define new contrasts to project with their assigned class
NEW_CONTRASTS = [
    # 1. Exploration Atmosphere (6)
    ("hypobaria_pure", "data/processed/exploration_atmosphere/hypobaria_pure.csv", "hypobaria"),
    ("exploration_50kPa_normO2", "data/processed/exploration_atmosphere/exploration_50kPa_normO2.csv", "hypobaria"),
    ("hypobaria_50kPa_air", "data/processed/exploration_atmosphere/hypobaria_50kPa_air.csv", "hypobaria"),
    ("hypobaria_extreme_10kPa", "data/processed/exploration_atmosphere/hypobaria_extreme_10kPa.csv", "hypobaria"),
    ("atmosphere_interaction", "data/processed/exploration_atmosphere/atmosphere_interaction.csv", "hypobaria"),
    ("hypoxia_normobaric_pure", "data/processed/exploration_atmosphere/hypoxia_normobaric_pure.csv", "low_oxygen"),

    # 2. Redox Decoder (1)
    ("ros_spaceflight_latent_shift", "data/processed/redox_decoder/ros_spaceflight_latent_shift.csv", "redox_ros"),

    # 3. MASTA database (15)
    ("cold_wt_3h", "data/processed/masta/cold_wt_3h.csv", "cold"),
    ("cold_wt_24h", "data/processed/masta/cold_wt_24h.csv", "cold"),
    ("wounding_15m", "data/processed/masta/wounding_15m.csv", "wounding"),
    ("wounding_24h", "data/processed/masta/wounding_24h.csv", "wounding"),
    ("drought_30m", "data/processed/masta/drought_30m.csv", "osmotic"),
    ("auxin_IAA_30m", "data/processed/masta/auxin_IAA_30m.csv", "hormone_auxin"),
    ("auxin_IAA_3h", "data/processed/masta/auxin_IAA_3h.csv", "hormone_auxin"),
    ("ga_treatment_30m", "data/processed/masta/ga_treatment_30m.csv", "hormone_ga"),
    ("cytokinin_zeatin_3h", "data/processed/masta/cytokinin_zeatin_3h.csv", "hormone_cytokinin"),
    ("brassinosteroid_BR_1h", "data/processed/masta/brassinosteroid_BR_1h.csv", "hormone_br"),
    ("potassium_starved_shoot", "data/processed/masta/potassium_starved_shoot.csv", "nutrient_stress"),
    ("phosphate_starved_leaves", "data/processed/masta/phosphate_starved_leaves.csv", "nutrient_stress"),
    ("ros_oxidative_root_3h", "data/processed/masta/ros_oxidative_root_3h.csv", "redox_ros"),
    ("ros_oxidative_shoot_3h", "data/processed/masta/ros_oxidative_shoot_3h.csv", "redox_ros"),
    ("ros_ozone", "data/processed/masta/ros_ozone.csv", "redox_ros"),
]

print(f"\nBeginning GSEA-prerank projection for {len(NEW_CONTRASTS)} new contrasts...")

for idx, (name, rel_path, klass) in enumerate(NEW_CONTRASTS, 1):
    full_path = os.path.join(ROOT, rel_path)
    if not os.path.exists(full_path):
        print(f"[{idx}/{len(NEW_CONTRASTS)}] WARNING: {full_path} not found! Skipping.")
        continue
    
    df = pd.read_csv(full_path)
    # Ensure 2 columns: gene, log2FC
    sig = df.set_index(df.columns[0])[df.columns[1]].astype(float).dropna()
    sig = sig.sort_values(ascending=False)
    
    print(f"[{idx}/{len(NEW_CONTRASTS)}] {name} ({klass}) | {len(sig)} genes (range {sig.min():.2f}..{sig.max():.2f}) ...", end=" ", flush=True)
    
    res = gp.prerank(
        rnk=sig.reset_index(),
        gene_sets=gene_sets,
        min_size=10,
        max_size=200,
        permutation_num=200,
        threads=4,
        seed=42,
        no_plot=True,
        outdir=None
    ).res2d
    
    res["NES"] = pd.to_numeric(res["NES"], errors="coerce")
    res["FDR q-val"] = pd.to_numeric(res["FDR q-val"], errors="coerce")
    res = res.set_index("Term")
    
    en[name] = res["NES"]
    ef[name] = res["FDR q-val"]
    cls[name] = klass
    
    # Quick sanity check on radicle apical meristem (cl14)
    nes_cl14 = res["NES"].get("germ_cluster::14", np.nan)
    print(f"DONE. (Radicle cl14 NES: {nes_cl14:+.2f})")

# Save v8 master matrices
out_en_file = os.path.join(TABLES, "decoder_nes_matrix_v8.csv")
out_ef_file = os.path.join(TABLES, "decoder_fdr_matrix_v8.csv")
en.to_csv(out_en_file)
ef.to_csv(out_ef_file)

pd.Series(cls, name="stressor_class").to_csv(cls_file)

print(f"\n================ SUCCESS ================")
print(f"Master Decoder Model v8 compiled successfully!")
print(f"Total contrasts: {en.shape[1]} (was {pd.read_csv(en_v7_file, index_col=0).shape[1]})")
print(f"Total panels: {en.shape[0]}")
print(f"Distinct stressor classes ({len(set(cls.values()))}):\n  {sorted(set(cls.values()))}")
print(f"Saved to:")
print(f"  {out_en_file}")
print(f"  {out_ef_file}")
print(f"  {cls_file}")
