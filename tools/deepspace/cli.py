"""Command-line interface for the deepspace tools.

  python -m deepspace.cli dsrs  signature.csv [--out out.csv]
  python -m deepspace.cli gsad  signature.csv [--out out.csv]
  python -m deepspace.cli export-gmt
signature.csv: two columns (gene AGI/TAIR, log2FC) or specify --gene/--lfc.
"""
import argparse, sys
import pandas as pd
from . import dsrs, gsad, panels
from .projection import load_signature


def main(argv=None):
    p = argparse.ArgumentParser(prog="deepspace")
    sub = p.add_subparsers(dest="cmd", required=True)
    for name in ("dsrs", "gsad"):
        sp = sub.add_parser(name)
        sp.add_argument("signature")
        sp.add_argument("--gene"); sp.add_argument("--lfc")
        sp.add_argument("--out")
    sub.add_parser("export-gmt")
    a = p.parse_args(argv)

    if a.cmd == "export-gmt":
        print("wrote", panels.export_gmt()); return
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
