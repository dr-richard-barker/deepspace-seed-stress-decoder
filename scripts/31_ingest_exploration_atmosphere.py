#!/usr/bin/env python
"""Phase 6.1 — Ingest NASA Exploration Atmosphere decoupled hypobaria / hypoxia signatures.

Source: arabidopsis_exploration_atmosphere / Table_S3_Full_22746_Orthogonal_Decomposition.csv
Derived from TabPFN v2 foundation modeling across 130 hypobaric/hypoxic microarrays.

Extracts:
  1. hypobaria_pure          : beta_hypobaria / pure_barosensory_effect (barosensory response isolated from hypoxia)
  2. exploration_50kPa_normO2: dlog2_50kPa_NormO2 (NASA nominal Exploration Atmosphere: 50 kPa, normoxic pO2)
  3. hypobaria_50kPa_air     : dlog2_50kPa_Air (hypobaria under ambient air)
  4. hypoxia_normobaric_pure : beta_hypoxia / pure_hypoxia_effect (hypoxia isolated from hypobaria)
  5. atmosphere_interaction  : beta_interaction (non-linear pressure x hypoxia interaction)
  6. hypobaria_extreme_10kPa : dlog2_10kPa_Air (extreme hypobaria)

Outputs:
  data/processed/exploration_atmosphere/{contrast_name}.csv
"""
import os
import pandas as pd

ROOT = os.environ.get("DEEPSPACE_ROOT") or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = "/Users/drb_laptop/Documents/Exploration_atmosphere_Biomni_lab_downloads_20261016_234156/arabidopsis_exploration_atmosphere/tables/Table_S3_Full_22746_Orthogonal_Decomposition.csv"
OUT_DIR = os.path.join(ROOT, "data", "processed", "exploration_atmosphere")
os.makedirs(OUT_DIR, exist_ok=True)

print(f"Reading Exploration Atmosphere decomposition from:\n  {SRC}")
df = pd.read_csv(SRC)

# Filter for valid TAIR AGI loci
df = df[df["TAIR"].astype(str).str.startswith("AT")].copy()
df["TAIR"] = df["TAIR"].astype(str).str.strip().str.upper()

contrasts = {
    "hypobaria_pure": "pure_barosensory_effect",
    "exploration_50kPa_normO2": "dlog2_50kPa_NormO2",
    "hypobaria_50kPa_air": "dlog2_50kPa_Air",
    "hypoxia_normobaric_pure": "pure_hypoxia_effect",
    "atmosphere_interaction": "beta_interaction",
    "hypobaria_extreme_10kPa": "dlog2_10kPa_Air",
}

manifest = []
for name, col in contrasts.items():
    if col not in df.columns:
        print(f"Warning: {col} not found in columns! Skipping.")
        continue
    sub = df[["TAIR", col]].dropna().drop_duplicates(subset=["TAIR"]).copy()
    sub.columns = ["gene", "log2FC"]
    sub["log2FC"] = pd.to_numeric(sub["log2FC"], errors="coerce")
    sub = sub.dropna().sort_values("log2FC", ascending=False)
    
    out_file = os.path.join(OUT_DIR, f"{name}.csv")
    sub.to_csv(out_file, index=False)
    print(f"[{name}] {len(sub)} genes -> {out_file} (range {sub['log2FC'].min():.3f} .. {sub['log2FC'].max():.3f})")
    manifest.append({
        "contrast": name,
        "source_col": col,
        "n_genes": len(sub),
        "min_val": sub["log2FC"].min(),
        "max_val": sub["log2FC"].max(),
        "file": out_file
    })

pd.DataFrame(manifest).to_csv(os.path.join(OUT_DIR, "manifest.csv"), index=False)
print("Exploration Atmosphere ingestion complete.")
