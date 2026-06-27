#!/usr/bin/env python
"""Phase 3 — bridge decoder (projection backbone).

Project genome-wide stressor signatures (OSD microgravity + GCR) onto the 122 seed
cell-type/state panels via GSEA-prerank.
  NES > 0  -> seed program concordantly INDUCED by the stressor
  NES < 0  -> seed program concordantly SUPPRESSED by the stressor

Output: results/tables/decoder_{nes,fdr}_matrix.csv + decoder_long.csv
NMF (Maffei 194-gene) is intentionally deferred: too few genes to project (documented).
"""
import os, re, warnings
import numpy as np, pandas as pd, gseapy as gp
warnings.filterwarnings("ignore")

ROOT = r"C:\Users\drric\Downloads\nmf_seed_decoder"
OSD  = os.path.join(ROOT, "data", "raw", "osd")
PAN  = os.path.join(ROOT, "panels", "panel_library.csv")
OUT  = os.path.join(ROOT, "results", "tables")
os.makedirs(OUT, exist_ok=True)

# contrast -> (file, exact Log2fc column, sign)  ; sign=-1 flips GC-v-SF into SF-effect
C = "Log2fc_"
CONTRASTS = {
 "ug_root_dark":  ("GLDS-120_DGE.csv", C+"(Col-0 & Ground Control & Dark Treatment)v(Col-0 & Space Flight & Dark Treatment)", -1),
 "ug_root_light": ("GLDS-120_DGE.csv", C+"(Col-0 & Ground Control & Light Treatment)v(Col-0 & Space Flight & Light Treatment)", -1),
 "ug_leaf_dark":  ("GLDS-612_DGE.csv", C+"(Col-0 & Wild Type & Ground Control & Dark Treatment)v(Col-0 & Wild Type & Space Flight & Dark Treatment)", -1),
 "ug_leaf_light": ("GLDS-612_DGE.csv", C+"(Col-0 & Wild Type & Ground Control & Light Treatment)v(Col-0 & Wild Type & Space Flight & Light Treatment)", -1),
 "gcr_40cGy":     ("GLDS-603_DGE.csv", C+"(mixed radiation & 40 centigray)v(non-irradiated & nan Not Applicable)", 1),
 "gcr_80cGy":     ("GLDS-603_DGE.csv", C+"(mixed radiation & 80 centigray)v(non-irradiated & nan Not Applicable)", 1),
}

# ---- panels -> gene_sets dict ----
pl = pd.read_csv(PAN)
pl["panel"] = pl["panel_source"] + "::" + pl["panel_group"].astype(str)
gene_sets = {p: g["gene"].dropna().unique().tolist() for p, g in pl.groupby("panel")}
print(f"{len(gene_sets)} panels loaded")

def rnk_for(fname, col, sign):
    path = os.path.join(OSD, fname)
    # read only TAIR + the one log2fc column (match exact, fallback to stripped)
    hdr = pd.read_csv(path, nrows=0).columns.tolist()
    target = col if col in hdr else next((h for h in hdr if h.strip('"') == col), None)
    if target is None:
        norm = lambda s: re.sub(r"\s+"," ",s.strip().strip('"'))
        target = next((h for h in hdr if norm(h)==norm(col)), None)
    if target is None:
        raise KeyError(f"column not found in {fname}: {col}")
    df = pd.read_csv(path, usecols=["TAIR", target])
    df = df.dropna(subset=["TAIR", target]).drop_duplicates("TAIR")
    s = (df.set_index("TAIR")[target].astype(float)) * sign
    return s.sort_values(ascending=False)

nes_cols, fdr_cols, longrows = {}, {}, []
for name, (fname, col, sign) in CONTRASTS.items():
    rnk = rnk_for(fname, col, sign)
    print(f"\n[{name}] ranked genes: {len(rnk)} (from {fname})")
    res = gp.prerank(rnk=rnk.reset_index(), gene_sets=gene_sets,
                     min_size=10, max_size=200, permutation_num=200,
                     threads=4, seed=42, no_plot=True, outdir=None)
    r = res.res2d.copy()
    r["NES"] = pd.to_numeric(r["NES"], errors="coerce")
    r["FDR q-val"] = pd.to_numeric(r["FDR q-val"], errors="coerce")
    r = r.set_index("Term")
    nes_cols[name] = r["NES"]; fdr_cols[name] = r["FDR q-val"]
    for term, row in r.iterrows():
        longrows.append(dict(contrast=name, panel=term, NES=row["NES"],
                             FDR=row["FDR q-val"], lead_genes=row.get("Lead_genes","")))

nes = pd.DataFrame(nes_cols); fdr = pd.DataFrame(fdr_cols)
nes.to_csv(os.path.join(OUT, "decoder_nes_matrix.csv"))
fdr.to_csv(os.path.join(OUT, "decoder_fdr_matrix.csv"))
pd.DataFrame(longrows).to_csv(os.path.join(OUT, "decoder_long.csv"), index=False)

print("\n==== HEADLINE: significant seed-program concordances (FDR<0.25) ====")
ld = pd.DataFrame(longrows)
sig = ld[ld.FDR < 0.25].copy()
for name in CONTRASTS:
    s = sig[sig.contrast==name].sort_values("NES")
    up = s[s.NES>0].nlargest(3,"NES"); dn = s[s.NES<0].nsmallest(3,"NES")
    print(f"\n{name}:  (sig panels: {len(s)})")
    for _,x in dn.iterrows(): print(f"   SUPPRESSED {x.panel:38s} NES={x.NES:+.2f} FDR={x.FDR:.3f}")
    for _,x in up.iterrows(): print(f"   INDUCED    {x.panel:38s} NES={x.NES:+.2f} FDR={x.FDR:.3f}")
print("\nDONE")
