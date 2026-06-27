#!/usr/bin/env python
"""Phase 1 ext — second NMF localization panel from Maffei/Paponov 2021 (Sci Rep s41598-021-88695-6).

Parses the 2021 supplementary S7 workbook (per-timepoint NNMF DEG lists; direction in the column left of
the AGI id). Builds a near-null NNMF up/down gene set distinct from the 2022 oxidative panel, then localizes
it onto germinating-seed cell-type expression specificity (same method as scripts/08). Compares 2021 vs 2022.
NOTE: this is the 2021 *published supplementary DEG lists*; the full genome-wide arrays remain pending the
Maffei author reply (see README).
Outputs: results/tables/nmf2021_gene_directions.csv, nmf2021_localization.csv;
         results/figures/nmf_localization_2021v2022.{png,svg}
"""
import os, re, warnings
import numpy as np, pandas as pd
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
plt.rcParams.update({"font.family":"sans-serif","font.sans-serif":["Arial","Helvetica","DejaVu Sans"],"savefig.dpi":300,"svg.fonttype":"none","pdf.fonttype":42})
warnings.filterwarnings("ignore")
rng=np.random.default_rng(42)
ROOT=r"C:\Users\drric\Downloads\nmf_seed_decoder"
RAW=os.path.join(ROOT,"data","raw"); NMF=os.path.join(RAW,"nmf_maffei")
T=os.path.join(ROOT,"results","tables"); F=os.path.join(ROOT,"results","figures"); PAN=os.path.join(ROOT,"panels")
AGI=re.compile(r'^AT[1-5MC]G\d{5}$')

# ---- parse 2021 supplement: (AGI, direction) across timepoint sheets ----
xl=pd.ExcelFile(os.path.join(NMF,"maffei2021_MOESM2.xlsx"))
tp=[s for s in xl.sheet_names if "exposure" in str(xl.parse(s,header=None,nrows=1).iloc[0,0]).lower()] \
   if False else [s for s in xl.sheet_names if s not in ("Summary",)]
rec=[]
for sh in tp:
    d=xl.parse(sh,header=None)
    agicols=[c for c in range(d.shape[1]) if d[c].astype(str).str.match(AGI).sum()>10]
    for c in agicols:
        m=d[c].astype(str).str.match(AGI)
        for r in d.index[m]:
            a=str(d.iat[r,c]).strip(); dirn=str(d.iat[r,c-1]).strip().lower()
            if dirn in ("up","down"): rec.append((a,dirn,sh))
rec=pd.DataFrame(rec,columns=["AGI","dir","tp"])
agg=rec.groupby("AGI")["dir"].agg(lambda s:(s=="up").sum()-(s=="down").sum())  # net up(+)/down(-)
up=set(agg[agg>0].index); dn=set(agg[agg<0].index)
rec.drop_duplicates().to_csv(os.path.join(T,"nmf2021_gene_directions.csv"),index=False)
print(f"2021 NNMF DEGs: {agg.size} genes (net up {len(up)}, net down {len(dn)}); records {len(rec)}")

# ---- germination cell-type specificity (same as scripts/08) ----
ann=pd.read_csv(os.path.join(PAN,"germination_cluster_annotations.csv")); ann["cluster"]=ann.cluster.astype(str)
cl2lab={c:f"{n} (cl{c})" for c,n in zip(ann.cluster,ann.cell_type)}
mat=pd.read_csv(os.path.join(RAW,"germination","GSE182331_expression_mat.csv.gz"),index_col=0)
meta=pd.read_csv(os.path.join(RAW,"germination","meta.tsv"),sep="\t")
meta["cellid"]=meta["sample"].astype(str)+"."+meta["Barcode"].astype(str)
meta["ct"]=meta["cluster"].astype(str).map(cl2lab)
meta=meta.set_index("cellid").reindex(mat.columns).dropna(subset=["ct"]); mat=mat[meta.index]
pb=mat.groupby(meta["ct"],axis=1).sum(); pb=np.log1p(pb/pb.sum()*1e6)
spec=pb.sub(pb.mean(1),axis=0).div(pb.std(1).replace(0,np.nan),axis=0).dropna()

def localize(geneset):
    g=[x for x in geneset if x in spec.index]
    if len(g)<5: return pd.Series(np.nan,index=spec.columns), len(g)
    obs=spec.loc[g].mean(0)
    null=np.array([spec.loc[rng.choice(spec.index,len(g),replace=False)].mean(0).values for _ in range(1000)])
    return pd.Series((obs.values-null.mean(0))/null.std(0),index=obs.index), len(g)

# direction split from this formatted workbook is unreliable (up-blocks not in the col-1 layout) ->
# the robust panel is the UNDIRECTED union of NNMF-responsive DEGs; also keep the well-captured down set.
allset=up|dn
z_all,n_all=localize(allset); z_dn,n_dn=localize(dn)
out=pd.DataFrame({"NMF2021_all_localization_z":z_all,"NMF2021_down_localization_z":z_dn})
out.to_csv(os.path.join(T,"nmf2021_localization.csv"))
print(f"localized 2021: undirected n={n_all}, down n={n_dn} (direction split unreliable - see caveat)")

# ---- compare 2021 (all NNMF DEGs) vs 2022 (NMF-up oxidative panel) ----
nmf22=pd.read_csv(os.path.join(T,"nmf_localization.csv"),index_col=0)["NMF_up_localization_z"]
cmp=pd.DataFrame({"2022 NMF-up (oxidative panel)":nmf22,"2021 NNMF DEGs (undirected)":z_all}).dropna()
order={"cotyledon":0,"hypocotyl":1,"radicle":2,"provasculature":3,"unassigned":4}
o={f"{n} (cl{c})":organ for c,n,organ in zip(ann.cluster,ann.cell_type,ann.organ)}
cmp=cmp.loc[sorted(cmp.index,key=lambda x:(order.get(o.get(x,"z"),9),x))]
fig,ax=plt.subplots(figsize=(5.4,0.46*len(cmp)+1.4)); vmax=np.nanmax(np.abs(cmp.values))
im=ax.imshow(cmp.values,cmap="BrBG",vmin=-vmax,vmax=vmax,aspect="auto")
ax.set_xticks([0,1]); ax.set_xticklabels(cmp.columns,rotation=20,ha="right",fontsize=8)
ax.set_yticks(range(len(cmp))); ax.set_yticklabels(cmp.index,fontsize=8)
for i in range(cmp.shape[0]):
    for j in range(2): ax.text(j,i,f"{cmp.values[i,j]:+.1f}",ha="center",va="center",fontsize=7,
                               color="white" if abs(cmp.values[i,j])>0.6*vmax else "black")
ax.set_title("NMF-responsive gene localization in germinating seed\n2022 oxidative panel vs 2021 NNMF DEGs (z vs random)",fontsize=9)
fig.colorbar(im,ax=ax,fraction=0.05,pad=0.03); fig.tight_layout()
fig.savefig(os.path.join(F,"nmf_localization_2021v2022.png"),bbox_inches="tight"); fig.savefig(os.path.join(F,"nmf_localization_2021v2022.svg"),bbox_inches="tight")

print("\n2021 NNMF (undirected) localization (top germinating-seed cell types):")
print(z_all.sort_values(ascending=False).head(5).round(2).to_string())
r=cmp.corr().iloc[0,1]; print(f"\n2021 vs 2022 localization correlation across cell types: r={r:.2f}")
print("DONE")
