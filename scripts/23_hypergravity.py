#!/usr/bin/env python
"""Phase 5.1 — hypergravity (true >1g) contrast, completing the gravity axis.

GSE29787 (Paul/Ferl/Herranz) LDC 2g vs 1g, callus, two-color Agilent GPL9020 (series-matrix log2 ratios).
Samples GSM738237/38/39 = 'MM2d LDC1g control vs MM2d LDC 2g' (3 replicates). Probe->AGI via GPL9020
GENE_SYMBOL. Microarray + callus tier; VALUE orientation assumed treatment(2g)-vs-control (documented).
Adds 'hypergravity_2g' to decoder_nes_matrix_v6 (class 'hypergravity', atlas family 'gravity').
"""
import os, re, gzip, warnings
from io import StringIO
import numpy as np, pandas as pd, gseapy as gp
warnings.filterwarnings("ignore")
ROOT=r"C:\Users\drric\Downloads\nmf_seed_decoder"
SV=os.path.join(ROOT,"data","raw","stressors_v2"); OUT=os.path.join(ROOT,"results","tables")
pl=pd.read_csv(os.path.join(ROOT,"panels","panel_library.csv")); pl["panel"]=pl.panel_source+"::"+pl.panel_group.astype(str)
gene_sets={p:g.gene.dropna().unique().tolist() for p,g in pl.groupby("panel")}

# probe (Agilent feature ID) -> AGI from GPL9020 GENE_SYMBOL
agi=re.compile(r'^AT[1-5MC]G\d{5}$'); hdr=None; p2a={}
with open(os.path.join(SV,"GPL9020_table.txt"),encoding="utf-8",errors="ignore") as f:
    for line in f:
        if line.startswith(("#","^","!")): continue
        parts=line.rstrip("\n").split("\t")
        if hdr is None and parts[0]=="ID": hdr=parts; gi=hdr.index("GENE_SYMBOL"); continue
        if hdr is None: continue
        if len(parts)>gi and agi.match(parts[gi].strip()): p2a[parts[0].strip()]=parts[gi].strip()
print("GPL9020 probe->AGI:",len(p2a))

# series matrix: ID_REF + the 3 LDC-2g arrays (download into project dir)
mp=os.path.join(SV,"GSE29787_series_matrix.txt.gz")
if not os.path.exists(mp):
    import urllib.request
    urllib.request.urlretrieve("https://ftp.ncbi.nlm.nih.gov/geo/series/GSE29nnn/GSE29787/matrix/GSE29787_series_matrix.txt.gz",mp)
raw=gzip.open(mp,"rt",encoding="utf-8",errors="ignore").read().split("\n")
data=[l for l in raw if l and not l.startswith("!")]
df=pd.read_csv(StringIO("\n".join(data)),sep="\t")
df=df.rename(columns={df.columns[0]:"probe"})
df["probe"]=df["probe"].astype(str).str.strip('"')
ldc=["GSM738237","GSM738238","GSM738239"]
df["m"]=df[ldc].apply(pd.to_numeric,errors="coerce").mean(1)
df["AGI"]=df["probe"].map(p2a)
sig=df.dropna(subset=["AGI","m"]).groupby("AGI")["m"].mean().sort_values(ascending=False)
print(f"hypergravity_2g signature: {len(sig)} AGI genes (range {sig.min():.2f}..{sig.max():.2f})")

res=gp.prerank(rnk=sig.reset_index(),gene_sets=gene_sets,min_size=10,max_size=200,
               permutation_num=200,threads=4,seed=42,no_plot=True,outdir=None).res2d
res["NES"]=pd.to_numeric(res["NES"],errors="coerce"); res["FDR q-val"]=pd.to_numeric(res["FDR q-val"],errors="coerce")
res=res.set_index("Term")

en=pd.read_csv(os.path.join(OUT,"decoder_nes_matrix_v5.csv"),index_col=0)
ef=pd.read_csv(os.path.join(OUT,"decoder_fdr_matrix_v5.csv"),index_col=0)
en["hypergravity_2g"]=res["NES"]; ef["hypergravity_2g"]=res["FDR q-val"]
en.to_csv(os.path.join(OUT,"decoder_nes_matrix_v6.csv")); ef.to_csv(os.path.join(OUT,"decoder_fdr_matrix_v6.csv"))
cls=pd.read_csv(os.path.join(OUT,"contrast_classes.csv"),index_col=0)["stressor_class"].to_dict()
cls["hypergravity_2g"]="hypergravity"; pd.Series(cls,name="stressor_class").to_csv(os.path.join(OUT,"contrast_classes.csv"))
print("\nmodel now:",en.shape[1],"contrasts")
key=[i for i in en.index if i.startswith("germ_state_time::") or i in ("gehring_L1_tissue::Embryo","germ_cluster::14")]
print(en.loc[[k for k in key if k in en.index],["hypergravity_2g"]].round(2).to_string())
print("DONE")
