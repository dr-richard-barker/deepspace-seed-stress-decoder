#!/usr/bin/env python
"""Phase 5.1 — gravity-axis stressors (RNA-seq, genome-wide).

gravitropism: GSE199142 gravistimulation time-course (Col-0, 12h & 24h vs Ref).
OSD-758/GLDS-664 gravity-dose: in-flight microgravity (uG vs in-flight 1G centrifuge = gold-standard
  microgravity), + partial gravity Moon(0.33G) & Mars(0.66G) vs uG.
Project onto 122 seed panels; merge into decoder_nes_matrix_v4.
"""
import os, re, warnings
import numpy as np, pandas as pd, gseapy as gp
warnings.filterwarnings("ignore")
ROOT=os.environ.get("DEEPSPACE_ROOT") or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW=os.path.join(ROOT,"data","raw"); SV=os.path.join(RAW,"stressors_v2"); OSDp=os.path.join(RAW,"osd")
OUT=os.path.join(ROOT,"results","tables")
pl=pd.read_csv(os.path.join(ROOT,"panels","panel_library.csv")); pl["panel"]=pl.panel_source+"::"+pl.panel_group.astype(str)
gene_sets={p:g.gene.dropna().unique().tolist() for p,g in pl.groupby("panel")}
def prerank(rnk):
    res=gp.prerank(rnk=rnk.reset_index(),gene_sets=gene_sets,min_size=10,max_size=200,
                   permutation_num=200,threads=4,seed=42,no_plot=True,outdir=None).res2d
    res["NES"]=pd.to_numeric(res["NES"],errors="coerce"); res["FDR q-val"]=pd.to_numeric(res["FDR q-val"],errors="coerce")
    return res.set_index("Term")["NES"], res.set_index("Term")["FDR q-val"]

nescol={}; fdrcol={}; cls={}

# ---- gravitropism GSE199142 ----
c=pd.read_csv(os.path.join(SV,"GSE199142_counts.txt.gz"),sep="\t")
c["TAIR"]=c["Gene"].astype(str).str.split("|").str[0]; c=c[c["TAIR"].str.startswith("AT")].set_index("TAIR")
def grp(rgx): return [x for x in c.columns if re.search(rgx,x)]
ref=grp(r"^Col-0.*_Ref");
def cpmlog(cols): m=c[cols].apply(pd.to_numeric,errors="coerce"); return np.log1p(m/m.sum()*1e6).mean(1)
ref_e=cpmlog(ref)
for tp in ["12h","24h"]:
    cols=[x for x in grp(r"^Col-0.*"+tp) if "Ref" not in x]
    sig=(cpmlog(cols)-ref_e).dropna().sort_values(ascending=False)
    n=f"gravitropism_{tp}"; nescol[n],fdrcol[n]=prerank(sig); cls[n]="tropism_gravi"
    print(f"[{n}] {len(sig)} genes, {len(cols)} treat cols")

# NOTE: OSD-758/GLDS-664 dropped — it is a MOUSE artificial-gravity study (ENSMUSG ids), not Arabidopsis.
# Plant fractional-gravity (EMCS centrifuge, Frontiers 2019) to be sourced separately if wanted.

# ---- merge into v4 ----
en=pd.read_csv(os.path.join(OUT,"decoder_nes_matrix_v3.csv"),index_col=0)
ef=pd.read_csv(os.path.join(OUT,"decoder_fdr_matrix_v3.csv"),index_col=0)
NES=en.join(pd.DataFrame(nescol),how="outer"); FDR=ef.join(pd.DataFrame(fdrcol),how="outer")
NES.to_csv(os.path.join(OUT,"decoder_nes_matrix_v4.csv")); FDR.to_csv(os.path.join(OUT,"decoder_fdr_matrix_v4.csv"))
allcls=pd.read_csv(os.path.join(OUT,"contrast_classes.csv"),index_col=0)["stressor_class"].to_dict()
allcls.update(cls); pd.Series(allcls,name="stressor_class").to_csv(os.path.join(OUT,"contrast_classes.csv"))
print("\ncombined model now:",NES.shape[1],"contrasts; classes:",pd.Series(allcls).value_counts().to_dict())
key=[i for i in NES.index if i.startswith("germ_state_time::") or i in ("gehring_L1_tissue::Embryo","germ_cluster::14")]
print(NES.loc[[k for k in key if k in NES.index],list(nescol)].round(2).to_string())
print("DONE")
