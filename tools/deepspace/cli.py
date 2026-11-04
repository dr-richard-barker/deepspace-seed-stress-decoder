"""Command-line interface for the deepspace tools.

  python -m deepspace.cli dsrs  signature.csv [--out out.csv]
  python -m deepspace.cli gsad  signature.csv [--out out.csv]
  python -m deepspace.cli masta-project contrast_name [--out out.csv]
  python -m deepspace.cli masta-list [--category S|H|C|M|...]
  python -m deepspace.cli export-gmt
signature.csv: two columns (gene AGI/TAIR, log2FC) or specify --gene/--lfc.
"""
import argparse, sys
import pandas as pd
from . import dsrs, gsad, panels, masta
from .projection import load_signature


def main(argv=None):
    p = argparse.ArgumentParser(prog="deepspace")
    sub = p.add_subparsers(dest="cmd", required=True)
    for name in ("dsrs", "gsad"):
        sp = sub.add_parser(name)
        sp.add_argument("signature")
        sp.add_argument("--gene"); sp.add_argument("--lfc")
        sp.add_argument("--out")
    
    # MASTA commands
    sp_mp = sub.add_parser("masta-project", help="Project any MASTA contrast onto seed reference")
    sp_mp.add_argument("contrast", help="MASTA contrast name/prefix, e.g. S851&cold_wt-wt_3h")
    sp_mp.add_argument("--masta-dir", help="Path to MASTA directory (optional)")
    sp_mp.add_argument("--out", help="Optional output CSV path")

    sp_ml = sub.add_parser("masta-list", help="List available MASTA contrasts")
    sp_ml.add_argument("--category", "-c", help="Category filter: S (stress), H (hormone), C (chemical), M (mutant)")
    sp_ml.add_argument("--masta-dir", help="Path to MASTA directory (optional)")

    sub.add_parser("export-gmt")
    a = p.parse_args(argv)

    if a.cmd == "export-gmt":
        print("wrote", panels.export_gmt()); return
    elif a.cmd == "masta-list":
        contrasts = masta.list_masta_contrasts(masta_dir=a.masta_dir, category=a.category)
        print(f"Found {len(contrasts)} MASTA contrasts:")
        for c in contrasts:
            print(f"  {c}")
        return
    elif a.cmd == "masta-project":
        print(f"Loading MASTA contrast: {a.contrast} ...")
        sig = masta.load_masta_contrast(a.contrast, masta_dir=a.masta_dir)
        print(f"Loaded {len(sig)} genes (range {sig.min():.2f} .. {sig.max():.2f}).")
        top, fam = dsrs.recognize(sig)
        print("\n== DSRS: Top Stressor Matches ==\n", top.to_string(index=False))
        print("\n== DSRS: Family Aggregate ==\n", fam.round(3).to_string())
        r = gsad.decode(sig)
        print("\n== GSAD: Germinating-Seed Cell-Type Susceptibility (Top) ==\n",
              r["celltype"][["NES", "FDR", "organ", "significant"]].head(8).to_string())
        print("\n== GSAD: Germination Stage ==\n", r["stage"][["NES", "FDR", "significant"]].to_string())
        if a.out:
            r["celltype"].to_csv(a.out)
            print(f"\nWrote results to {a.out}")
        return

    sig = load_signature(a.signature, gene_col=a.gene, lfc_col=a.lfc)
    if a.cmd == "dsrs":
        top, fam = dsrs.recognize(sig)
        print("== top stressor matches ==\n", top.to_string(index=False))
        print("\n== family aggregate ==\n", fam.round(3).to_string())
        if a.out: top.to_csv(a.out, index=False)
    elif a.cmd == "gsad":
        r = gsad.decode(sig)
        print("== germinating-seed cell-type susceptibility (top) ==\n",
              r["celltype"][["NES", "FDR", "organ", "significant"]].head(8).to_string())
        print("\n== germination stage ==\n", r["stage"][["NES", "FDR", "significant"]].to_string())
        if a.out: r["celltype"].to_csv(a.out)


if __name__ == "__main__":
    main(sys.argv[1:])
