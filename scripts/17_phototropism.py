#!/usr/bin/env python
"""Phase 5.1 — phototropism contrast (microarray-tier).

GSE3847 (Esmon tropic-stimulus, ATH1/GPL198): phototropism = shaded vs lit sides of the bending organ
(auxin accumulates on the shaded, faster-growing side). Probe->AGI via GPL198 table. Project onto panels.
"""
import os, re, gzip, warnings
from io import StringIO
import numpy as np, pandas as pd, gseapy as gp
warnings.filterwarnings("ignore")
ROOT=os.environ.get("DEEPSPACE_ROOT") or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SV=os.path.join(ROOT,"data","raw","stressors_v2"); OUT=os.path.join(ROOT,"results","tables")
pl=pd.read_csv(os.path.join(ROOT,"panels","panel_library.csv")); pl["panel"]=pl.panel_source+"::"+pl.panel_group.astype(str)
gene_sets={p:g.gene.dropna().unique().tolist() for p,g in pl.groupby("panel")}

# probe -> AGI from GPL198 table
hdr=None; rows=[]
with open(os.path.join(SV,"GPL198_table.txt"),encoding="utf-8",errors="ignore") as f:
    for l in f:
        if l.startswith(("#","^","!")): continue
        if hdr is None:
            if l.startswith("ID\t"): hdr=l.rstrip("\n").split("\t")
            continue
        rows.append(l.rstrip("\n").split("\t"))
gpl=pd.DataFrame(rows,columns=hdr)
def first_agi(x):
    for tok in str(x).split(" /// "):
        tok=tok.strip()
        if re.match(r"^AT[1-5]G\d{5}$",tok): return tok
    return None
gpl["AGI"]=gpl["AGI"].map(first_agi)
probe2agi=gpl.dropna(subset=["AGI"]).set_index("ID")["AGI"].to_dict()
print("probe->AGI map:",len(probe2agi))

# series matrix: title<->GSM, then data
raw=gzip.open(os.path.join(SV,"GSE3847_series_matrix.txt.gz"),"rt",encoding="utf-8",errors="ignore").read().split("\n")
def meta(tag):
    ln=next(l for l in raw if l.startswith(tag)); return [x.strip('"') for x in ln.split("\t")[1:]]
titles=meta("!Sample_title"); gsms=meta("!Sample_geo_accession")
t2g=dict(zip(titles,gsms))
shaded=[g for t,g in t2g.items() if "shaded" in t.lower()]
lit=[g for t,g in t2g.items() if re.search(r"\blit\b",t.lower())]
print("shaded:",shaded,"| lit:",lit)
data=[l for l in raw if l and not l.startswith("!")]
df=pd.read_csv(StringIO("\n".join(data)),sep="\t")
df=df.rename(columns={df.columns[0]:"probe"}).set_index("probe")
df.index=[str(i).strip('"') for i in df.index]
ms=df[shaded].apply(pd.to_numeric,errors="coerce").mean(1); ml=df[lit].apply(pd.to_numeric,errors="coerce").mean(1)
sig=np.log2((ms+1)/(ml+1)).dropna()
sig.index=pd.Series(sig.index).map(probe2agi).values
sig=sig[pd.notna(sig.index)]; sig=sig.groupby(level=0).mean().sort_values(ascending=False)
print(f"phototropism signature: {len(sig)} AGI genes (range {sig.min():.2f}..{sig.max():.2f})")

res=gp.prerank(rnk=sig.reset_index(),gene_sets=gene_sets,min_size=10,max_size=200,
               permutation_num=200,threads=4,seed=42,no_plot=True,outdir=None).res2d
res["NES"]=pd.to_numeric(res["NES"],errors="coerce"); res["FDR q-val"]=pd.to_numeric(res["FDR q-val"],errors="coerce")
res=res.set_index("Term")

en=pd.read_csv(os.path.join(OUT,"decoder_nes_matrix_v4.csv"),index_col=0)
ef=pd.read_csv(os.path.join(OUT,"decoder_fdr_matrix_v4.csv"),index_col=0)
en["phototropism"]=res["NES"]; ef["phototropism"]=res["FDR q-val"]
en.to_csv(os.path.join(OUT,"decoder_nes_matrix_v5.csv")); ef.to_csv(os.path.join(OUT,"decoder_fdr_matrix_v5.csv"))
cls=pd.read_csv(os.path.join(OUT,"contrast_classes.csv"),index_col=0)["stressor_class"].to_dict()
cls["phototropism"]="tropism_photo"; pd.Series(cls,name="stressor_class").to_csv(os.path.join(OUT,"contrast_classes.csv"))
print("\nmodel now:",en.shape[1],"contrasts")
key=[i for i in en.index if i.startswith("germ_state_time::") or i in ("gehring_L1_tissue::Embryo","germ_cluster::14","germ_cluster::6")]
print(en.loc[[k for k in key if k in en.index],["phototropism"]].round(2).to_string())
print("DONE")
