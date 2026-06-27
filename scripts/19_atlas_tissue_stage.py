#!/usr/bin/env python
"""Phase 5.4b — DeepSpace atlas at TISSUE and STAGE level.

Same 5-family convergence as the cell-type atlas, applied to:
  - developing-seed TISSUES (Gehring level_1: embryo/endosperm/seed-coat/funiculus/ovule)
  - germination STAGES (germ_state_time: 12/24/48 hsl)
NMF (magnetic) family added by localizing NMF-up genes onto tissue/stage expression specificity.
Outputs: results/tables/deepspace_atlas_tissue_stage_convergence.csv ; figures/deepspace_atlas_tissue_stage.{png,svg}
"""
import os, numpy as np, pandas as pd
from scipy.io import mmread  # noqa
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
ROOT=r"C:\Users\drric\Downloads\nmf_seed_decoder"; T=os.path.join(ROOT,"results","tables"); F=os.path.join(ROOT,"results","figures"); RAW=os.path.join(ROOT,"data","raw")
rng=np.random.default_rng(42)
NES=pd.read_csv(os.path.join(T,"decoder_nes_matrix_v6.csv"),index_col=0)
FDR=pd.read_csv(os.path.join(T,"decoder_fdr_matrix_v6.csv"),index_col=0)
cls=pd.read_csv(os.path.join(T,"contrast_classes.csv"),index_col=0)["stressor_class"].to_dict()
fam={c:("gravity" if cls.get(c) in("microgravity","partial_gravity","hypergravity") else
        "tropism" if cls.get(c) in("tropism_gravi","tropism_photo") else
        "low_oxygen" if cls.get(c)=="low_oxygen" else
        "radiation" if str(cls.get(c)).startswith("radiation") else cls.get(c,"other")) for c in NES.columns}
families=["gravity","tropism","low_oxygen","radiation","magnetic_NMF"]
SIG_NES=1.5; SIG_FDR=0.25; SIG_NMFZ=2.0
nmf_dir=pd.read_csv(os.path.join(T,"nmf_gene_directions.csv"),index_col=0).iloc[:,0]
nmf_up=set(nmf_dir[nmf_dir>0.1].index)

def localize(pb):  # pb: genes x groups (log-CPM) -> NMF-up localization z per group
    spec=pb.sub(pb.mean(1),axis=0).div(pb.std(1).replace(0,np.nan),axis=0).dropna()
    g=[x for x in nmf_up if x in spec.index]
    if len(g)<5: return pd.Series(np.nan,index=pb.columns)
    obs=spec.loc[g].mean(0)
    null=np.array([spec.loc[rng.choice(spec.index,len(g),replace=False)].mean(0).values for _ in range(1000)])
    return pd.Series((obs.values-null.mean(0))/null.std(0),index=pb.columns)

# ---- TISSUE: Gehring level_1 ----
dev=pd.read_csv(os.path.join(T,"gehring_dev_pseudobulk.csv"),index_col=0)   # cols Embryo_3DAP...
L1=dev.groupby(dev.columns.str.rsplit("_",n=1).str[0],axis=1).mean()        # -> Embryo/Endosperm/...
nmf_tissue=localize(L1)
tissue_rows={t:f"gehring_L1_tissue::{t}" for t in L1.columns}

# ---- STAGE: germination 12/24/48 hsl ----
mat=pd.read_csv(os.path.join(RAW,"germination","GSE182331_expression_mat.csv.gz"),index_col=0)
meta=pd.read_csv(os.path.join(RAW,"germination","meta.tsv"),sep="\t"); meta["cellid"]=meta["sample"].astype(str)+"."+meta["Barcode"].astype(str)
meta=meta.set_index("cellid").reindex(mat.columns).dropna(subset=["time"])
mat=mat[meta.index]
pbt=mat.groupby(meta["time"],axis=1).sum(); pbt=np.log1p(pbt/pbt.sum()*1e6)
nmf_stage=localize(pbt)
stage_rows={s:f"germ_state_time::{s}" for s in ["12hsl","24hsl","48hsl"]}

# ---- assemble convergence for a set of (label,row,nmf_z) ----
def build(rowmap,nmfz):
    famval=pd.DataFrame(0.0,index=list(rowmap),columns=families); famhit=pd.DataFrame(0,index=list(rowmap),columns=families)
    for lab,row in rowmap.items():
        if row not in NES.index: continue
        for f_ in set(fam.values()):
            if f_ not in families: continue
            cols=[c for c in NES.columns if fam[c]==f_]
            sig=[(abs(NES.loc[row,c])>=SIG_NES and FDR.loc[row,c]<SIG_FDR) for c in cols]
            if any(sig): famhit.loc[lab,f_]=1; famval.loc[lab,f_]=max([NES.loc[row,c] for c,s in zip(cols,sig) if s],key=abs)
        z=nmfz.get(lab,np.nan)
        if pd.notna(z) and abs(z)>=SIG_NMFZ: famhit.loc[lab,"magnetic_NMF"]=1; famval.loc[lab,"magnetic_NMF"]=z
    return famval,famhit

tv,th=build(tissue_rows,nmf_tissue); sv,sh=build(stage_rows,nmf_stage)
tv["level"]="tissue"; sv["level"]="stage"
conv=pd.concat([th.sum(1).rename("n_families"),sh.sum(1).rename("n_families")])
allval=pd.concat([tv,sv]); allhit=pd.concat([th,sh])
summary=pd.DataFrame({"node":conv.index,"level":["tissue"]*len(th)+["stage"]*len(sh),
                      "n_families":conv.values,
                      "families_hit":[", ".join([f for f in families if allhit.loc[n,f]]) for n in conv.index]}).sort_values(["level","n_families"],ascending=[True,False])
summary.to_csv(os.path.join(T,"deepspace_atlas_tissue_stage_convergence.csv"),index=False)

# ---- figure: heatmap | dedicated colorbar | convergence bars (no overlap) ----
rows=list(tissue_rows)+["(stage)"]+list(stage_rows)
M=np.array([[np.nan]*5 if r=="(stage)" else allval.loc[r,families].values.astype(float) for r in rows],float)
vmax=np.nanmax(np.abs(M)) or 1
fig=plt.figure(figsize=(9.4,0.55*len(rows)+2.0))
gs=fig.add_gridspec(1,3,width_ratios=[5,0.22,1.5],wspace=0.5)
ax=fig.add_subplot(gs[0]); cax=fig.add_subplot(gs[1]); axb=fig.add_subplot(gs[2])
im=ax.imshow(M,cmap="RdBu_r",vmin=-vmax,vmax=vmax,aspect="auto")
ax.set_xticks(range(5)); ax.set_xticklabels(families,rotation=40,ha="right",fontsize=8)
ax.set_yticks(range(len(rows))); ax.set_yticklabels(rows,fontsize=8)
for i,r in enumerate(rows):
    if r=="(stage)": continue
    for j,f_ in enumerate(families):
        if allhit.loc[r,f_]: ax.text(j,i,"*",ha="center",va="center",fontsize=12,fontweight="bold")
ax.set_title("DeepSpace atlas — tissue & germination-stage level  (* significant; color = signed strength)",fontsize=9)
cb=fig.colorbar(im,cax=cax); cb.set_label("signed strength (NES / NMF z)",fontsize=7); cax.tick_params(labelsize=7)
vals=[0 if r=="(stage)" else conv[r] for r in rows]
axb.barh(range(len(rows)),vals,color="#555"); axb.invert_yaxis()
axb.set_ylim(len(rows)-0.5,-0.5); axb.set_yticks([]); axb.set_xlim(0,5.3)
axb.set_xlabel("n families",fontsize=8); axb.set_title("convergence",fontsize=9)
for i,r in enumerate(rows):
    if r!="(stage)": axb.text(vals[i]+0.1,i,str(int(conv[r])),va="center",fontsize=7)
fig.savefig(os.path.join(F,"deepspace_atlas_tissue_stage.png"),dpi=200,bbox_inches="tight"); fig.savefig(os.path.join(F,"deepspace_atlas_tissue_stage.svg"),bbox_inches="tight")

print("==== tissue + stage convergence ===="); print(summary.to_string(index=False))
print("\nNMF localization z — tissue:",{k:round(v,1) for k,v in nmf_tissue.items()})
print("NMF localization z — stage:",{k:round(v,1) for k,v in nmf_stage.items()})
print("\nNOTE: germination atlas starts at 12 hsl -> the truly DRY/0h stage is under-sampled.")
print("DONE")
