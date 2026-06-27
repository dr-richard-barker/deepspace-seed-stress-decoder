"""Shared projection engine: rank a query signature and GSEA-project onto the seed panels."""
import warnings
import numpy as np
import pandas as pd
import gseapy as gp
from .panels import load_panels

warnings.filterwarnings("ignore")


def load_signature(src, gene_col=None, lfc_col=None):
    """Accept a path (csv/tsv) or a pandas Series/DataFrame; return a ranked Series (gene->log2FC).
    For a DataFrame/file, gene_col + lfc_col select the columns (else first two)."""
    if isinstance(src, pd.Series):
        s = src.dropna()
    else:
        df = src if isinstance(src, pd.DataFrame) else pd.read_csv(
            src, sep="\t" if str(src).endswith((".tsv", ".txt")) else ",")
        gene_col = gene_col or df.columns[0]
        lfc_col = lfc_col or df.columns[1]
        s = df.dropna(subset=[gene_col, lfc_col]).drop_duplicates(gene_col) \
              .set_index(gene_col)[lfc_col].astype(float)
    return s.sort_values(ascending=False)


def project(signature, panels=None, permutation_num=200, min_size=10, max_size=200, seed=42):
    """Project a ranked signature onto the panels. Returns DataFrame indexed by panel with NES, FDR."""
    rnk = load_signature(signature)
    gene_sets = panels or load_panels()
    res = gp.prerank(rnk=rnk.reset_index(), gene_sets=gene_sets, min_size=min_size,
                     max_size=max_size, permutation_num=permutation_num, threads=4,
                     seed=seed, no_plot=True, outdir=None).res2d
    res["NES"] = pd.to_numeric(res["NES"], errors="coerce")
    res["FDR"] = pd.to_numeric(res["FDR q-val"], errors="coerce")
    return res.set_index("Term")[["NES", "FDR"]]
