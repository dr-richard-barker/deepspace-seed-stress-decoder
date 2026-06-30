#!/usr/bin/env python
"""Phase 5.1 — add low-oxygen stressors (hypoxia, anoxia, submergence) to the perturbation model.

hypoxia + anoxia: GSE315308 O2 gradient (1% & 0% vs 21% normoxia), Entrez->TAIR mapped.
submergence:      GSE182724 'Sub vs. Air' sheet (AGI + Log2FC, ready).
Project each onto the 122 seed panels (GSEA-prerank); merge into decoder_nes_matrix_v3.
"""
import os, re, warnings
import numpy as np, pandas as pd, gseapy as gp
warnings.filterwarnings("ignore")
ROOT=os.environ.get("DEEPSPACE_ROOT") or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW=os.path.join(ROOT,"data","raw"); SV=os.path.join(RAW,"stressors_v2")
OUT=os.path.join(ROOT,"results","tables"); PAN=os.path.join(ROOT,"panels","panel_library.csv")

# panels
pl=pd.read_csv(PAN); pl["panel"]=pl.panel_source+"::"+pl.panel_group.astype(str)
gene_sets={p:g.gene.dropna().unique().tolist() for p,g in pl.groupby("panel")}

# Entrez(str, no .0) -> TAIR map from OSD DGE
osd=pd.read_csv(os.path.join(RAW,"osd","GLDS-120_DGE.csv"),usecols=["TAIR","ENTREZID"]).dropna()
osd["E"]=osd["ENTREZID"].astype(str).str.replace(r"\.0$","",regex=True)
e2t=osd.drop_duplicates("E").set_index("E")["TAIR"].to_dict()

def collapse_tair(series_by_gene):  # mean within duplicate TAIR
    return series_by_gene.groupby(level=0).mean()

# ---- GSE315308 hypoxia + anoxia ----
fp=pd.read_csv(os.path.join(SV,"GSE315308_fpkm.txt.gz"),sep="\t")
fp["TAIR"]=fp["gene_id"].astype(str).map(e2t)
fp=fp.dropna(subset=["TAIR"])
def cond_mean(pfx):
    cols=[c for c in fp.columns if c.startswith(pfx)]; return fp.set_index("TAIR")[cols].mean(1)
m21=collapse_tair(cond_mean("HIFRAP_21_")); m1=collapse_tair(cond_mean("HIFRAP_1_")); m0=collapse_tair(cond_mean("HIFRAP_0_"))
hyp=np.log2((m1+1)/(m21+1)).dropna()          # 1% vs 21%
ano=np.log2((m0+1)/(m21+1)).dropna()          # 0% vs 21%

# ---- GSE182724 submergence (ready Log2FC, AGI) ----
sub=pd.read_excel(os.path.join(SV,"GSE182724_Expr.xlsx"),sheet_name="Sub vs. Air")
idc=next(c for c in sub.columns if str(c).strip().lower() in ("gene id","gene_id"))
lfc=next(c for c in sub.columns if "fold change" in str(c).lower() and "log" in str(c).lower())
subs=sub[[idc,lfc]].dropna(); subs=subs[subs[idc].astype(str).str.startswith("AT")]
subsig=collapse_tair(subs.set_index(idc)[lfc].astype(float))

SIGS={"hypoxia_1pct":hyp,"anoxia_0pct":ano,"submergence":subsig}
nescol={}; fdrcol={}
for name,sig in SIGS.items():
    rnk=sig.sort_values(ascending=False)
    print(f"[{name}] {len(rnk)} genes (range {rnk.min():.2f}..{rnk.max():.2f})")
    res=gp.prerank(rnk=rnk.reset_index(),gene_sets=gene_sets,min_size=10,max_size=200,
                   permutation_num=200,threads=4,seed=42,no_plot=True,outdir=None).res2d
    res["NES"]=pd.to_numeric(res["NES"],errors="coerce"); res["FDR q-val"]=pd.to_numeric(res["FDR q-val"],errors="coerce")
    res=res.set_index("Term"); nescol[name]=res["NES"]; fdrcol[name]=res["FDR q-val"]

# merge into v3 (v2 + oxygen)
en=pd.read_csv(os.path.join(OUT,"decoder_nes_matrix_v2.csv"),index_col=0)
ef=pd.read_csv(os.path.join(OUT,"decoder_fdr_matrix_v2.csv"),index_col=0)
NES=en.join(pd.DataFrame(nescol),how="outer"); FDR=ef.join(pd.DataFrame(fdrcol),how="outer")
NES.to_csv(os.path.join(OUT,"decoder_nes_matrix_v3.csv")); FDR.to_csv(os.path.join(OUT,"decoder_fdr_matrix_v3.csv"))

# update classes
cls=pd.read_csv(os.path.join(OUT,"contrast_classes.csv"),index_col=0)["stressor_class"].to_dict()
for n in SIGS: cls[n]="low_oxygen"
pd.Series(cls,name="stressor_class").to_csv(os.path.join(OUT,"contrast_classes.csv"))

print("\ncombined model now:",NES.shape[1],"contrasts")
key=[i for i in NES.index if i.startswith("germ_state_time::") or i=="gehring_L1_tissue::Embryo"
     or i in ("germ_cluster::14",)]
print("\nlow-oxygen NES on key seed programs:")
print(NES.loc[[k for k in key if k in NES.index],list(SIGS)].round(2).to_string())
print("\nDONE")
