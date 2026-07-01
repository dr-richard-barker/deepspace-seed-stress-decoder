#!/usr/bin/env python
"""Canonical mature-root eFP rendering of the NMF threat loci (Brady/Benfey root map, GSE8934).

Independent test of the seed-radicle finding: are the NMF-responsive loci meristem/tip-biased in the
*mature* Arabidopsis root too? Uses the Brady et al. 2007 high-resolution root spatiotemporal map
(GEO GSE8934, ATH1/GPL198): a longitudinal developmental axis (columella -> meristem x6 -> elongation x2
-> maturation x4) and 8 FACS-sorted stele/pericycle/hair-cell populations.

Outputs:
  results/tables/nmf_root_efp_longitudinal.csv, nmf_root_efp_celltype.csv
  results/figures/nmf_mature_root_efp_up.{png,svg}          (per-locus longitudinal pictograms)
  results/figures/nmf_mature_root_efp_collective.{png,svg}  (up/down profiles + tip-bias test)
  results/figures/nmf_mature_root_celltype_heatmap.{png,svg}
"""
import os, re, gzip, numpy as np, pandas as pd
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Ellipse
from matplotlib.colors import Normalize
from matplotlib import cm

ROOT=os.environ.get("DEEPSPACE_ROOT") or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW=os.path.join(ROOT,"data","raw"); T=os.path.join(ROOT,"results","tables"); F=os.path.join(ROOT,"results","figures")
MX=os.path.join(RAW,"root_efp","GSE8934_series_matrix.txt.gz")
GPL=os.path.join(RAW,"stressors_v2","GPL198_table.txt")

# ---------- probe -> AGI ----------
lines=open(GPL,encoding="latin-1").read().splitlines()
hdr=next(i for i,l in enumerate(lines) if l.startswith("ID\t"))
gpl=pd.read_csv(GPL,sep="\t",skiprows=hdr,dtype=str,low_memory=False)[["ID","AGI"]].dropna()
gpl["AGI"]=gpl["AGI"].str.split(" /// ").str[0].str.upper()
p2a=dict(zip(gpl["ID"],gpl["AGI"]))

# ---------- expression matrix (GSM cols) + title map ----------
raw=gzip.open(MX,"rt",encoding="latin-1").read()
titles=re.findall(r'"([^"]*)"', [l for l in raw.splitlines() if l.startswith("!Sample_title")][0])
gsms  =re.findall(r'"([^"]*)"', [l for l in raw.splitlines() if l.startswith("!Sample_geo_accession")][0])
gsm2title=dict(zip(gsms,titles))
df=pd.read_csv(MX,sep="\t",comment="!",index_col=0,compression="gzip")
df.index=[str(i).strip('"') for i in df.index]
df.columns=[gsm2title.get(c,c) for c in df.columns]
df["AGI"]=[p2a.get(i) for i in df.index]
g=np.log2(df.dropna(subset=["AGI"]).groupby("AGI").mean(numeric_only=True)+1)   # genes x samples, log2

# ---------- axes ----------
# longitudinal developmental zones (tip -> base); each section = mean of L#SB and Slice#JW replicates
ZONE_DEF=[("columella",["LCOLUMELLASB"])]+[
    (nm,[f"L{i}SB",f"Slice{i}JW"]) for i,nm in zip(range(1,13),
    ["merist 1","merist 2","merist 3","merist 4","merist 5","merist 6",
     "elong 1","elong 2","matur 1","matur 2","matur 3","matur 4"])]
long_expr=pd.DataFrame({nm:g[[c for c in cs if c in g.columns]].mean(1) for nm,cs in ZONE_DEF})
# radial FACS cell types (friendly names from GEO descriptions)
CELLS={"S17":"phloem pole pericycle","S32":"protophloem/metaphloem","COBL9":"hair cell (trichoblast)",
       "JO121":"xylem pole pericycle","S4":"protoxylem/metaxylem","SUC2":"phloem companion cell",
       "J2501":"stele (peri/xyl/phl)","RM1000":"lateral root primordia"}
cell_expr=g[[c for c in CELLS if c in g.columns]].rename(columns=CELLS)

# ---------- NMF loci (from scripts 28/29) + symbols ----------
up=pd.read_csv(os.path.join(T,"nmf_radicle_risk_genes.csv"))
dn=pd.read_csv(os.path.join(T,"nmf_radicle_risk_genes_down.csv"))
sym={r.TAIR_ID:(r.gene_symbol if isinstance(r.gene_symbol,str) and r.gene_symbol else r.TAIR_ID) for _,r in pd.concat([up,dn]).iterrows()}
up_g=[x for x in up.TAIR_ID if x in long_expr.index]; dn_g=[x for x in dn.TAIR_ID if x in long_expr.index]
print(f"loci in mature-root map: up {len(up_g)}/{len(up)}, down {len(dn_g)}/{len(dn)}")

long_expr.loc[up_g+dn_g].round(3).to_csv(os.path.join(T,"nmf_root_efp_longitudinal.csv"))
cell_expr.loc[up_g+dn_g].round(3).to_csv(os.path.join(T,"nmf_root_efp_celltype.csv"))
ZL=list(long_expr.columns)   # 13 zones tip->base

# ---------- longitudinal root pictogram ----------
def draw_long_root(ax, vals, norm, cmap):
    """vals = list of 13 zone values tip(columella)->base(maturation)."""
    cx=5.0; hw=1.7; y0=1.4; band=1.05
    # columella dome (tip)
    ax.add_patch(Ellipse((cx,y0-0.1),2*hw,2.3,facecolor=cmap(norm(vals[0])),edgecolor="none"))
    for k in range(1,13):
        y=y0+(k-1)*band
        ax.add_patch(Rectangle((cx-hw,y),2*hw,band,facecolor=cmap(norm(vals[k])),edgecolor="none"))
    ax.add_patch(Rectangle((cx-hw,y0),2*hw,12*band,fill=False,edgecolor="0.4",lw=0.6))
    ax.add_patch(Ellipse((cx,y0-0.1),2*hw,2.3,fill=False,edgecolor="0.4",lw=0.6))
    ax.set_xlim(2.5,7.5); ax.set_ylim(-0.6,y0+12*band+0.4); ax.set_aspect("equal"); ax.axis("off")

vmin,vmax=np.percentile(long_expr.loc[up_g+dn_g].values,[5,99])
norm=Normalize(vmin,vmax); cmap=plt.get_cmap("YlOrRd")

def grid(genes,fname,title):
    ncol=6; nrow=int(np.ceil(len(genes)/ncol))
    fig,axes=plt.subplots(nrow,ncol,figsize=(ncol*1.35,nrow*2.4)); axes=np.atleast_1d(axes).ravel()
    for i,gg in enumerate(genes):
        draw_long_root(axes[i],long_expr.loc[gg,ZL].values,norm,cmap)
        axes[i].set_title(f"{sym.get(gg,gg)}\n{gg}",fontsize=6,pad=1)
    for j in range(len(genes),len(axes)): axes[j].axis("off")
    fig.suptitle(title+"   (tip=columella ↓ … base=maturation ↑)",fontsize=10,y=0.999)
    sm=cm.ScalarMappable(norm=norm,cmap=cmap); sm.set_array([])
    fig.colorbar(sm,ax=axes.tolist(),fraction=0.02,pad=0.01).set_label("expression (log2)",fontsize=8)
    fig.savefig(os.path.join(F,fname+".png"),dpi=200,bbox_inches="tight"); fig.savefig(os.path.join(F,fname+".svg"),bbox_inches="tight"); plt.close(fig)

grid(up_g,"nmf_mature_root_efp_up","NMF-UP threat loci — mature-root eFP (Brady GSE8934)")

# ---------- collective: tip-bias test + up/down roots ----------
def zmean(genes):  # mean of per-gene z across zones (location pattern)
    z=long_expr.loc[genes,ZL].sub(long_expr.loc[genes,ZL].mean(1),axis=0).div(long_expr.loc[genes,ZL].std(1).replace(0,np.nan),axis=0)
    return z.mean(0)
up_z=zmean(up_g); dn_z=zmean(dn_g)
up_lvl=long_expr.loc[up_g,ZL].mean(0); dn_lvl=long_expr.loc[dn_g,ZL].mean(0)

fig=plt.figure(figsize=(12,5.2))
znorm=Normalize(-max(abs(up_z).max(),abs(dn_z).max()),max(abs(up_z).max(),abs(dn_z).max())); zc=plt.get_cmap("RdBu_r")
axU=fig.add_axes([0.02,0.06,0.13,0.82]); draw_long_root(axU,up_z.values,znorm,zc); axU.set_title(f"UP set\n(n={len(up_g)})",fontsize=9)
axD=fig.add_axes([0.16,0.06,0.13,0.82]); draw_long_root(axD,dn_z.values,znorm,zc); axD.set_title(f"DOWN set\n(n={len(dn_g)})",fontsize=9)
sm=cm.ScalarMappable(norm=znorm,cmap=zc); sm.set_array([]); fig.colorbar(sm,ax=[axU,axD],fraction=0.04,pad=0.02).set_label("mean specificity z",fontsize=8)
# profile line
axP=fig.add_axes([0.37,0.15,0.28,0.72])
axP.plot(range(13),up_z.values,"o-",color="#b2182b",label=f"UP (n={len(up_g)})")
axP.plot(range(13),dn_z.values,"s--",color="#2166ac",label=f"DOWN (n={len(dn_g)})")
axP.axhline(0,color="0.6",lw=0.7); axP.set_xticks(range(13)); axP.set_xticklabels(ZL,rotation=90,fontsize=7)
axP.set_ylabel("mean specificity z (across zones)",fontsize=8); axP.legend(fontsize=8)
axP.set_title("Longitudinal bias in the mature root",fontsize=9)
axP.axvspan(-0.5,6.5,color="#fff3cd",alpha=0.5,zorder=0)  # meristem+columella region
axP.text(3,axP.get_ylim()[1]*0.92,"meristem/tip",fontsize=7,ha="center",color="0.4")
# heatmap loci x zones (level) for a compact overview
axH=fig.add_axes([0.70,0.12,0.28,0.78])
M=long_expr.loc[up_g,ZL]
Mz=M.sub(M.mean(1),axis=0).div(M.std(1).replace(0,np.nan),axis=0)
im=axH.imshow(Mz.values,cmap="YlOrRd",aspect="auto")
axH.set_xticks(range(13)); axH.set_xticklabels(ZL,rotation=90,fontsize=6)
axH.set_yticks(range(len(up_g))); axH.set_yticklabels([sym.get(x,x) for x in up_g],fontsize=5)
axH.set_title("UP loci × zone (row-z)",fontsize=8)
fig.suptitle("NMF threat loci in the mature Arabidopsis root — Brady spatiotemporal map (GSE8934)",fontsize=11,y=0.99)
fig.text(0.02,0.005,"Data: Brady et al. 2007 root map (GEO GSE8934, ATH1/GPL198). In the MATURE root these loci are elongation/maturation-biased "
         "(tip/meristem z -0.24 vs maturation +0.35), NOT tip-biased as in the germinating-seed radicle — a developmental-context shift "
         "(class-III peroxidases act in the mature-root maturation zone).",fontsize=6.3,color="0.4")
fig.savefig(os.path.join(F,"nmf_mature_root_efp_collective.png"),dpi=200,bbox_inches="tight"); fig.savefig(os.path.join(F,"nmf_mature_root_efp_collective.svg"),bbox_inches="tight"); plt.close(fig)

# ---------- radial cell-type heatmap ----------
C=cell_expr.loc[up_g+dn_g]
Cz=C.sub(C.mean(1),axis=0).div(C.std(1).replace(0,np.nan),axis=0)
fig,ax=plt.subplots(figsize=(0.5*C.shape[1]+4,0.3*len(C)+2))
im=ax.imshow(Cz.values,cmap="RdBu_r",vmin=-2,vmax=2,aspect="auto")
ax.set_xticks(range(C.shape[1])); ax.set_xticklabels(C.columns,rotation=45,ha="right",fontsize=7)
ax.set_yticks(range(len(C))); ax.set_yticklabels([f"{sym.get(x,x)} ({'up' if x in up_g else 'down'})" for x in C.index],fontsize=6)
ax.set_title("NMF loci across sorted mature-root cell types (Brady GSE8934; row-z)",fontsize=9)
fig.colorbar(im,ax=ax,fraction=0.04,pad=0.02).set_label("row-z expression",fontsize=7)
fig.tight_layout(); fig.savefig(os.path.join(F,"nmf_mature_root_celltype_heatmap.png"),dpi=200); fig.savefig(os.path.join(F,"nmf_mature_root_celltype_heatmap.svg")); plt.close(fig)

print("wrote mature-root eFP figures + tables")
print("\nUP-set mean specificity z by zone (tip->base):")
print(up_z.round(2).to_string())
print(f"\ntip/meristem (columella+merist1-6) mean z: UP {up_z.iloc[:7].mean():+.2f}  vs  maturation (matur1-4) mean z: UP {up_z.iloc[-4:].mean():+.2f}")
