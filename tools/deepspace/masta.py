"""MASTA database integration module.

Provides programmatic utilities to search, load, and convert microarray perturbation contrasts
from the Max Planck MASTA database (592 contrasts) into ranked signatures (gene -> log2FC)
for projection with DSRS and GSAD.
"""
import os
import glob
from pathlib import Path
import numpy as np
import pandas as pd

from . import config

DEFAULT_MASTA_DIR = Path("/Users/drb_laptop/Documents/MASTA")

_PROBE2TAIR = None


def get_probe_map():
    """Return dictionary mapping Affymetrix ATH1 probe IDs to Arabidopsis TAIR AGI IDs."""
    global _PROBE2TAIR
    if _PROBE2TAIR is None:
        ea_table = config.ROOT / "data" / "raw" / "stressors_v2" / "GPL198_table.txt"
        ea_alt = Path("/Users/drb_laptop/Documents/Exploration_atmosphere_Biomni_lab_downloads_20261016_234156/arabidopsis_exploration_atmosphere/tables/Table_S3_Full_22746_Orthogonal_Decomposition.csv")
        
        mapping = {}
        if ea_alt.exists():
            df = pd.read_csv(ea_alt, usecols=["ProbesetID", "TAIR"]).dropna()
            for p, t in zip(df["ProbesetID"], df["TAIR"]):
                first_locus = str(t).split("|")[0].strip().upper()
                if first_locus.startswith("AT"):
                    mapping[str(p).strip()] = first_locus
        elif ea_table.exists():
            for line in open(ea_table, encoding="utf-8", errors="ignore"):
                if line.startswith(("#", "^", "!")):
                    continue
                p = line.rstrip("\n").split("\t")
                if len(p) >= 2 and p[1].startswith("AT"):
                    mapping[p[0]] = p[1].split(" /// ")[0].strip()
        _PROBE2TAIR = mapping
    return _PROBE2TAIR


def list_masta_contrasts(masta_dir=None, category=None):
    """List available contrast names in the MASTA database.
    
    Parameters:
      masta_dir: Path to MASTA directory (default /Users/drb_laptop/Documents/MASTA)
      category: Optional category filter (e.g. 'S' for Stress, 'H' for Hormones, 'C' for Chemicals)
    """
    m_dir = Path(masta_dir or DEFAULT_MASTA_DIR) / "Tables"
    if not m_dir.exists():
        return []
    
    files = [f.name for f in m_dir.glob("*5000_topgenes*")]
    contrasts = sorted(list(set(f.split(" 5000_topgenes")[0] for f in files)))
    if category:
        contrasts = [c for c in contrasts if c.startswith(category)]
    return contrasts


def load_masta_contrast(contrast_prefix, masta_dir=None):
    """Load a MASTA contrast by prefix/name and return a ranked Series (TAIR AGI -> log2FC).
    
    Parameters:
      contrast_prefix: e.g. 'S851&cold_wt-wt_3h' or 'cold_wt-wt_3h' or 'H511'
      masta_dir: Path to MASTA directory
    """
    m_dir = Path(masta_dir or DEFAULT_MASTA_DIR) / "Tables"
    if not m_dir.exists():
        raise FileNotFoundError(f"MASTA Tables directory not found at {m_dir}")
    
    probe2tair = get_probe_map()
    
    # Locate top and down files
    top_matches = list(m_dir.glob(f"*{contrast_prefix}*5000_topgenes*"))
    down_matches = list(m_dir.glob(f"*{contrast_prefix}*5000_downgenes*"))
    
    if not top_matches or not down_matches:
        raise FileNotFoundError(f"Could not find matching top/down files for MASTA contrast: {contrast_prefix}")
    
    def parse_file(fp):
        df = pd.read_csv(fp, sep=" ", index_col=0)
        df.index = [str(i).strip('"') for i in df.index]
        fc_col = "FC:(class1/class2)"
        fc = df[fc_col].astype(str).str.replace(",", ".").astype(float)
        pfp = df["pfp"].astype(str).str.replace(",", ".").astype(float)
        fc = np.clip(fc, 1e-6, 1e6)
        l2 = np.log2(fc)
        res = pd.DataFrame({"probe": df.index, "log2FC": l2, "pfp": pfp})
        res["gene"] = res["probe"].map(probe2tair)
        return res.dropna(subset=["gene"])
    
    top = parse_file(top_matches[0])
    down = parse_file(down_matches[0])
    
    comb = pd.concat([top, down]).sort_values("pfp").drop_duplicates(subset=["gene"])
    sig = comb.set_index("gene")["log2FC"].sort_values(ascending=False)
    return sig
