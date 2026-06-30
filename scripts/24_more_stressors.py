#!/usr/bin/env python
"""Phase 5.1 — add 5 environmental stressor families: desiccation, osmotic, ethylene, temperature, UV.

desiccation  GSE76015  seed maturation drying: WT ecotypes (Ws,Ler) 21 vs 15 DAF (CPM, AGI)
ethylene     GSE193833 Col-0 ACC 4h vs 0h (counts, AGI)
temperature  GSE303133 Col 27C vs 21C warm/thermomorphogenesis (TPM, AGI.Araport11)
osmotic      GSE5622 vs control GSE5620 (AtGenExpress, ATH1 shoot 3h, probe->AGI via GPL198)
uv           GSE5626 vs control GSE5620 (AtGenExpress, ATH1 shoot 6h, probe->AGI via GPL198)
Each -> GSEA-prerank onto 122 panels; appended to decoder_nes_matrix_v7.
"""
import os, re, gzip, warnings
from io import StringIO
import numpy as np, pandas as pd, gseapy as gp
warnings.filterwarnings("ignore")
ROOT=os.environ.get("DEEPSPACE_ROOT") or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SV=os.path.join(ROOT,"data","raw","stressors_v2"); OUT=os.path.join(ROOT,"results","tables")
pl=pd.read_csv(os.path.join(ROOT,"panels","panel_library.csv")); pl["panel"]=pl.panel_source+"::"+pl.panel_group.astype(str)
gene_sets={p:g.gene.dropna().unique().tolist() for p,g in pl.groupby("panel")}
def collapse(s): return s.groupby(level=0).mean()
def L2(num,den): return np.log2((num+1)/(den+1))

SIGS={}

# --- desiccation: GSE76015 CPM, WT ecotypes 21 vs 15 DAF ---
d=pd.read_csv(os.path.join(SV,"GSE76015_desic_cpm.csv.gz"),index_col=0)
d=d[d.index.astype(str).str.startswith("AT")]
rat=[L2(d[f"{e}21"],d[f"{e}15"]) for e in ("ws","ler") if f"{e}21" in d.columns and f"{e}15" in d.columns]
SIGS["desiccation_seed"]=("desiccation", collapse(pd.concat(rat,axis=1).mean(1)).dropna())

# --- ethylene: GSE193833 counts, Col0 ACC 4h vs 0h ---
e=pd.read_csv(os.path.join(SV,"GSE193833_ethylene.txt.gz"),sep="\t",index_col=0)
e=e[e.index.astype(str).str.startswith("AT")]
cpm=e/e.sum()*1e6
t=[c for c in cpm.columns if c.startswith("ACC.Col0.4h")]; c0=[c for c in cpm.columns if c.startswith("ACC.Col0.0h")]
SIGS["ethylene_ACC"]=("ethylene", collapse(L2(cpm[t].mean(1),cpm[c0].mean(1))).dropna())

# --- temperature: GSE303133 TPM, Col 27 vs 21 ---
h=pd.read_csv(os.path.join(SV,"GSE303133_heat_TPM.txt.gz"),sep="\t",index_col=0)
h.index=h.index.astype(str).str.split(".").str[0]; h=h[h.index.str.startswith("AT")]
w=[c for c in h.columns if c.startswith("Col_27")]; cc=[c for c in h.columns if c.startswith("Col_21")]
SIGS["temperature_warm"]=("temperature", collapse(L2(h[w].mean(1),h[cc].mean(1))).dropna())

# --- ATH1 probe->AGI (GPL198 AGI col) ---
hdr=None; p2a={}; agi=re.compile(r'^AT[1-5MC]G\d{5}$')
for line in open(os.path.join(SV,"GPL198_table.txt"),encoding="utf-8",errors="ignore"):
    if line.startswith(("#","^","!")): continue
    p=line.rstrip("\n").split("\t")
    if hdr is None and p[0]=="ID": hdr=p; ai=hdr.index("AGI"); continue
    if hdr is None: continue
    if len(p)>ai:
        a=p[ai].split(" /// ")[0].strip()
        if agi.match(a): p2a[p[0]]=a
def load_ath1(g):
    raw=gzip.open(os.path.join(SV,f"{g}_mat.txt.gz"),"rt",encoding="utf-8",errors="ignore").read().split("\n")
    data=[l for l in raw if l and not l.startswith("!")]
    df=pd.read_csv(StringIO("\n".join(data)),sep="\t"); df=df.rename(columns={df.columns[0]:"probe"}).set_index("probe")
    df.index=[str(i).strip('"') for i in df.index]; return df.apply(pd.to_numeric,errors="coerce")
ctrl=load_ath1("GSE5620")
def ath1_sig(g,treat_gsms,ctrl_gsms):
    tr=load_ath1(g)
    num=tr[treat_gsms].mean(1); den=ctrl[ctrl_gsms].mean(1)
    s=np.log2((num+1)/(den+1)); s.index=pd.Series(s.index).map(p2a).values
    return collapse(s[pd.notna(s.index)]).dropna()
# osmotic shoot 3h vs control shoot 3h ; UV-B shoot 6h vs control shoot 6h
SIGS["osmotic"]=("osmotic", ath1_sig("GSE5622",["GSM131291","GSM131292"],["GSM131239","GSM131240"]))
SIGS["uv_B"]   =("uv",      ath1_sig("GSE5626",["GSM131399","GSM131400"],["GSM131247","GSM131248"]))

# --- project all, append to v6 -> v7 ---
en=pd.read_csv(os.path.join(OUT,"decoder_nes_matrix_v6.csv"),index_col=0)
ef=pd.read_csv(os.path.join(OUT,"decoder_fdr_matrix_v6.csv"),index_col=0)
cls=pd.read_csv(os.path.join(OUT,"contrast_classes.csv"),index_col=0)["stressor_class"].to_dict()
for name,(klass,sig) in SIGS.items():
    sig=sig.sort_values(ascending=False)
    print(f"[{name}] {len(sig)} AGI genes (range {sig.min():.2f}..{sig.max():.2f})")
    res=gp.prerank(rnk=sig.reset_index(),gene_sets=gene_sets,min_size=10,max_size=200,
                   permutation_num=200,threads=4,seed=42,no_plot=True,outdir=None).res2d
    res["NES"]=pd.to_numeric(res["NES"],errors="coerce"); res["FDR q-val"]=pd.to_numeric(res["FDR q-val"],errors="coerce")
    res=res.set_index("Term"); en[name]=res["NES"]; ef[name]=res["FDR q-val"]; cls[name]=klass
en.to_csv(os.path.join(OUT,"decoder_nes_matrix_v7.csv")); ef.to_csv(os.path.join(OUT,"decoder_fdr_matrix_v7.csv"))
pd.Series(cls,name="stressor_class").to_csv(os.path.join(OUT,"contrast_classes.csv"))
print("\nmodel now:",en.shape[1],"contrasts; classes:",sorted(set(cls.values())))
key=[i for i in en.index if i.startswith("germ_state_time::") or i in("gehring_L1_tissue::Embryo","germ_cluster::14")]
print(en.loc[[k for k in key if k in en.index],list(SIGS)].round(2).to_string())
print("DONE")
