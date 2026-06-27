"""Example: run DSRS + GSAD on a transcriptomic signature.

Usage: python example_usage.py  (run from tools/ with DEEPSPACE_ROOT set to the repo root)
Uses example_signature.csv (gene AGI, log2FC). Replace with your own two-column signature.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # tools/ on path
import deepspace

SIG = os.path.join(os.path.dirname(__file__), "example_signature.csv")

print("=== DSRS: which space stressor does this resemble? ===")
top, fam = deepspace.dsrs.recognize(SIG, top=6)
print(top.to_string(index=False))
print("\nfamily aggregate:\n", fam.round(3).to_string())

print("\n=== GSAD: predicted effect on the dry/germinating seed ===")
seed = deepspace.gsad.decode(SIG)
print("top germinating-seed cell-type susceptibility:")
print(seed["celltype"][["NES", "FDR", "organ", "significant"]].head(6).to_string())
