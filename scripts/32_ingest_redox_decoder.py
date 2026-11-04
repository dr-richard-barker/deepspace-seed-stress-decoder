#!/usr/bin/env python
"""Phase 6.2 — Ingest Redox Decoder signatures.

Source: /Users/drb_laptop/Documents/Redox_decoder/Table_S6_spaceflight_responsive_genes.csv
Derived from the CVAE framework trained across 232 harmonized transcriptomics studies
and projected across 38 NASA OSDR spaceflight missions (879 flight samples).

Extracts:
  ros_spaceflight_latent_shift : log2(err_spaceflight / err_ground) = log2(err_ratio)
  Representing the genome-wide spaceflight-induced ROS latent remodeling signature.

Outputs:
  data/processed/redox_decoder/ros_spaceflight_latent_shift.csv
"""
import os
import numpy as np
import pandas as pd

ROOT = os.environ.get("DEEPSPACE_ROOT") or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = "/Users/drb_laptop/Documents/Redox_decoder/Table_S6_spaceflight_responsive_genes.csv"
OUT_DIR = os.path.join(ROOT, "data", "processed", "redox_decoder")
os.makedirs(OUT_DIR, exist_ok=True)

print(f"Reading spaceflight responsive genes from:\n  {SRC}")
df = pd.read_csv(SRC)

# Filter for valid TAIR AGI loci
df = df[df["gene"].astype(str).str.startswith("AT")].copy()
df["gene"] = df["gene"].astype(str).str.strip().str.upper()

# Calculate log2(err_ratio) as signed response score
df["log2FC"] = np.log2(pd.to_numeric(df["err_ratio"], errors="coerce"))
sig = df[["gene", "log2FC"]].dropna().drop_duplicates(subset=["gene"]).sort_values("log2FC", ascending=False)

out_file = os.path.join(OUT_DIR, "ros_spaceflight_latent_shift.csv")
sig.to_csv(out_file, index=False)
print(f"[ros_spaceflight_latent_shift] {len(sig)} genes -> {out_file} (range {sig['log2FC'].min():.3f} .. {sig['log2FC'].max():.3f})")

manifest = [{
    "contrast": "ros_spaceflight_latent_shift",
    "source_file": "Table_S6_spaceflight_responsive_genes.csv",
    "n_genes": len(sig),
    "min_val": sig["log2FC"].min(),
    "max_val": sig["log2FC"].max(),
    "file": out_file
}]
pd.DataFrame(manifest).to_csv(os.path.join(OUT_DIR, "manifest.csv"), index=False)
print("Redox Decoder spaceflight signature ingestion complete.")
