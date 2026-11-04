#!/usr/bin/env python
"""Phase 6.3 — Ingest Max Planck MASTA database contrasts.

Source: /Users/drb_laptop/Documents/MASTA/Tables
RankProd 5000_topgenes and 5000_downgenes mapped from Affymetrix ATH1 to TAIR AGI via GPL198.

Extracts representative contrasts across key space-relevant axes:
  - Cold shock time-course: cold_wt_3h (S851), cold_wt_24h (S853)
  - Mechanical wounding: wounding_15m (S411), wounding_24h (S417)
  - Drought stress: drought_30m (S112)
  - Hormone signaling: auxin_IAA_30m (H511), auxin_IAA_3h (H513), ga_30m (H331), zeatin_3h (H218), br_1h (H832)
  - Nutrient starvation: potassium_starved (N414), phosphate_starved (N31)
  - Biochemical ROS (AtGenExpress): ros_oxidative_rt_3h (S623), ros_oxidative_sh_3h (S613), ros_ozone (S511)

Outputs:
  data/processed/masta/{contrast_name}.csv
"""
import os
import glob
import numpy as np
import pandas as pd

ROOT = os.environ.get("DEEPSPACE_ROOT") or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MASTA_TABLES = "/Users/drb_laptop/Documents/MASTA/Tables"
OUT_DIR = os.path.join(ROOT, "data", "processed", "masta")
os.makedirs(OUT_DIR, exist_ok=True)

# 1. Build ATH1 probe -> TAIR AGI dictionary from Exploration Atmosphere Table S3
EA_TABLE = "/Users/drb_laptop/Documents/Exploration_atmosphere_Biomni_lab_downloads_20261016_234156/arabidopsis_exploration_atmosphere/tables/Table_S3_Full_22746_Orthogonal_Decomposition.csv"
print(f"Loading probe -> TAIR annotation from:\n  {EA_TABLE}")
map_df = pd.read_csv(EA_TABLE, usecols=["ProbesetID", "TAIR"]).dropna()
probe2tair = {}
for p, t in zip(map_df["ProbesetID"], map_df["TAIR"]):
    # Handle single or pipe-delimited loci
    first_locus = str(t).split("|")[0].strip().upper()
    if first_locus.startswith("AT"):
        probe2tair[str(p).strip()] = first_locus

print(f"Loaded {len(probe2tair)} valid probe -> TAIR mappings.")

# 2. Selected MASTA contrasts
CONTRASTS = {
    "cold_wt_3h": "S851&cold_wt-wt_3h",
    "cold_wt_24h": "S853&cold_wt-wt_24h",
    "wounding_15m": "S411&wounding_sh_15m",
    "wounding_24h": "S417&wounding_sh_24h",
    "drought_30m": "S112&drought_sh_30m",
    "auxin_IAA_30m": "H511&IAA-mock_30m",
    "auxin_IAA_3h": "H513&IAA-mock_3h",
    "ga_treatment_30m": "H331&GA_ga1-mock_ga1_30m",
    "cytokinin_zeatin_3h": "H218&zeatin-mock_3h",
    "brassinosteroid_BR_1h": "H832&BR_det2-BR_wt_1h",
    "potassium_starved_shoot": "N414&Potassium_starved-c_sh",
    "phosphate_starved_leaves": "N31&791_phosph_leaves10d",
    "ros_oxidative_root_3h": "S623&oxidative_rt_3h",
    "ros_oxidative_shoot_3h": "S613&oxidative_sh_3h",
    "ros_ozone": "S511&ozone",
}

def load_masta_file(prefix, is_top=True):
    # Find matching file allowing whitespace variations
    pat = os.path.join(MASTA_TABLES, f"{prefix}*5000_{'top' if is_top else 'down'}genes*")
    matches = glob.glob(pat)
    if not matches:
        raise FileNotFoundError(f"No file matching {pat}")
    fp = matches[0]
    
    df = pd.read_csv(fp, sep=" ", index_col=0)
    df.index = [str(i).strip('"') for i in df.index]
    fc_col = "FC:(class1/class2)"
    fc = df[fc_col].astype(str).str.replace(",", ".").astype(float)
    pfp = df["pfp"].astype(str).str.replace(",", ".").astype(float)
    
    # Avoid log2(0) or infinite values
    fc = np.clip(fc, 1e-6, 1e6)
    l2 = np.log2(fc)
    
    res = pd.DataFrame({"probe": df.index, "log2FC": l2, "pfp": pfp})
    res["gene"] = res["probe"].map(probe2tair)
    return res.dropna(subset=["gene"])

manifest = []
for out_name, prefix in CONTRASTS.items():
    try:
        top = load_masta_file(prefix, is_top=True)
        down = load_masta_file(prefix, is_top=False)
        
        # Combine: order by statistical significance (lowest pfp first), keep best probe per gene
        comb = pd.concat([top, down]).sort_values("pfp").drop_duplicates(subset=["gene"])
        sig = comb[["gene", "log2FC"]].sort_values("log2FC", ascending=False)
        
        out_file = os.path.join(OUT_DIR, f"{out_name}.csv")
        sig.to_csv(out_file, index=False)
        print(f"[{out_name}] {len(sig)} genes -> {out_file} (range {sig['log2FC'].min():.2f} .. {sig['log2FC'].max():.2f})")
        
        manifest.append({
            "contrast": out_name,
            "masta_prefix": prefix,
            "n_genes": len(sig),
            "min_val": sig["log2FC"].min(),
            "max_val": sig["log2FC"].max(),
            "file": out_file
        })
    except Exception as e:
        print(f"Error processing {out_name} ({prefix}): {e}")

pd.DataFrame(manifest).to_csv(os.path.join(OUT_DIR, "manifest.csv"), index=False)
print(f"MASTA ingestion complete: {len(manifest)}/{len(CONTRASTS)} contrasts processed successfully.")
