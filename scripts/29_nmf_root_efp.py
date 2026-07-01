#!/usr/bin/env python
"""NMF threat loci in the germinating-seed root: down-set companion + ePlant-style root pictograms.

Part 1: companion NMF-DOWN radicle set (mirror of script 28's up-set).
Part 2: map germinating-seed radicle cell types -> root anatomical compartments and render an
        eFP/ePlant-style root pictogram (expression level, log-CPM) for every NMF threat locus
        (up and down), plus a collective panel (up-set vs down-set vs net) to highlight zones of
        synergy (both concentrated) / antagonism (spatially divergent).

Data note: the "root map" is the germinating-seed single-cell radicle compartments (Liew/Lewsey
GSE182331), i.e. the seed's own root, NOT the mature-root Brady eFP. Compartment mapping below.

Outputs:
  results/tables/nmf_radicle_risk_genes_down.csv
  results/tables/nmf_root_zone_expression.csv
  results/figures/nmf_radicle_risk_heatmap_down.{png,svg}
  results/figures/nmf_root_efp_up.{png,svg}, nmf_root_efp_down.{png,svg}
  results/figures/nmf_root_efp_collective.{png,svg}
"""
import os, numpy as np, pandas as pd
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Ellipse
from matplotlib.colors import Normalize
from matplotlib import cm

ROOT=os.environ.get("DEEPSPACE_ROOT") or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW=os.path.join(ROOT,"data","raw"); NMF=os.path.join(RAW,"nmf_maffei")
PAN=os.path.join(ROOT,"panels"); T=os.path.join(ROOT,"results","tables"); F=os.path.join(ROOT,"results","figures")

TARGET="radicle apical meristem (cl14)"
SPEC_MIN=1.0

# ---------- NMF directions + gene symbols (Maffei source) ----------
direction=pd.read_csv(os.path.join(T,"nmf_gene_directions.csv"),index_col=0)["nmf_shoot_late_log2"]
nmf_up=set(direction[direction>0.1].index); nmf_dn=set(direction[direction<-0.1].index)

def parse_code(code):
    if not isinstance(code,str) or not code.strip(): return "",""
    parts=[p.strip().strip('"') for p in code.split(",") if p.strip()]
    if parts and len(parts[0])<=12 and " " not in parts[0] and not parts[0][0].islower():
        return parts[0], ", ".join(parts[1:])
    return "", code.strip()
sym={}; name={}
def add(t,s,n):
    if t not in sym and s: sym[t]=s
    if t not in name and n: name[t]=n
for _,r in pd.read_csv(os.path.join(NMF,"nmf_cluster_membership.csv")).iterrows():
    s,n=parse_code(r.get("gene_code")); add(r["tair_id"],s,n or str(r.get("gene_function") or "").strip())
for _,r in pd.read_csv(os.path.join(NMF,"nmf_h2o2_panel.csv")).drop_duplicates("tair_id").iterrows():
    s,n=parse_code(r.get("gene_code")); add(r["tair_id"],s,n)
for _,r in pd.read_csv(os.path.join(NMF,"nmf_polyphenol_gene_panel.csv")).drop_duplicates("tair_id").iterrows():
    add(r["tair_id"],"",str(r.get("gene_name") or "").strip())
label=lambda g: sym.get(g) or g

# ---------- germinating-seed pseudobulk: expression (log-CPM) + specificity (z) ----------
ann=pd.read_csv(os.path.join(PAN,"germination_cluster_annotations.csv")); ann["cluster"]=ann.cluster.astype(str)
cl2lab={c:f"{n} (cl{c})" for c,n in zip(ann.cluster,ann.cell_type)}
lab2org={cl2lab[c]:o for c,o in zip(ann.cluster,ann.organ)}
mat=pd.read_csv(os.path.join(RAW,"germination","GSE182331_expression_mat.csv.gz"),index_col=0)
meta=pd.read_csv(os.path.join(RAW,"germination","meta.tsv"),sep="\t")
meta["cellid"]=meta["sample"].astype(str)+"."+meta["Barcode"].astype(str)
meta["ct"]=meta["cluster"].astype(str).map(cl2lab)
meta=meta.set_index("cellid").reindex(mat.columns).dropna(subset=["ct"]); mat=mat[meta.index]
pb=mat.T.groupby(meta["ct"]).sum().T; pb=pb/pb.sum(0)*1e6; pb=np.log1p(pb)          # genes x ct log-CPM
spec=pb.sub(pb.mean(1),axis=0).div(pb.std(1).replace(0,np.nan),axis=0).dropna()

# ---------- Part 1: down-set table + heatmap (mirror of script 28) ----------
def risk_table(geneset):
    g=[x for x in geneset if x in spec.index]
    rad=spec.loc[g,TARGET].sort_values(ascending=False)
    keep=rad[rad>=SPEC_MIN].index.tolist()
    tab=pd.DataFrame({"TAIR_ID":keep,"gene_symbol":[sym.get(x,"") for x in keep],
                      "gene_name":[name.get(x,"") for x in keep],
                      "NMF_shoot_late_log2":[round(float(direction[x]),3) for x in keep],
                      "radicle_apical_meristem_spec_z":[round(float(spec.loc[x,TARGET]),2) for x in keep]})
    return tab.sort_values("radicle_apical_meristem_spec_z",ascending=False).reset_index(drop=True),keep

up_tab,up_genes=risk_table(nmf_up)
dn_tab,dn_genes=risk_table(nmf_dn)
dn_tab.to_csv(os.path.join(T,"nmf_radicle_risk_genes_down.csv"),index=False)
print(f"radicle-specific (z>={SPEC_MIN}): NMF-up {len(up_genes)}, NMF-down {len(dn_genes)}")

order=["cotyledon","hypocotyl","radicle","provasculature","unassigned"]
cols=sorted(spec.columns,key=lambda c:(order.index(lab2org.get(c,"unassigned")) if lab2org.get(c,"unassigned") in order else 9,c))
if dn_genes:
    H=spec.loc[dn_genes,cols]
    fig,ax=plt.subplots(figsize=(0.42*len(cols)+4.5,0.34*len(dn_genes)+1.8))
    vmax=np.nanpercentile(np.abs(H.values),98)
    im=ax.imshow(H.values,cmap="RdBu_r",vmin=-vmax,vmax=vmax,aspect="auto")
    ax.set_xticks(range(len(cols))); ax.set_xticklabels(cols,rotation=90,fontsize=7)
    ax.set_yticks(range(len(dn_genes))); ax.set_yticklabels([f"{label(g)}  {g}" for g in dn_genes],fontsize=6.5)
    tcol=cols.index(TARGET); ax.add_patch(Rectangle((tcol-0.5,-0.5),1,len(dn_genes),fill=False,edgecolor="black",lw=1.8))
    ax.set_title(f"NMF-DOWN genes specific to the root radicle\nspecificity (z); boxed = {TARGET}",fontsize=8)
    fig.colorbar(im,ax=ax,fraction=0.025,pad=0.02).set_label("specificity z",fontsize=7)
    fig.tight_layout(); fig.savefig(os.path.join(F,"nmf_radicle_risk_heatmap_down.png"),dpi=220); fig.savefig(os.path.join(F,"nmf_radicle_risk_heatmap_down.svg"))
    plt.close(fig)

# ---------- Part 2: root anatomical compartments <- germination clusters ----------
ZONES={"root cap":["columella/root cap (+QC) (cl4)"],
       "meristem (QC)":[TARGET],
       "epidermis":["radicle epidermis (cl10)"],
       "cortex/endodermis":["cortex/endodermis (cl2)"],
       "stele/vasculature":["provasculature (cl12)","provasculature: protoxylem (cl9)","provasculature: protophloem (cl15)"]}
ZONES={z:[c for c in cs if c in pb.columns] for z,cs in ZONES.items()}

def zone_expr(gene):
    return {z:float(pb.loc[gene,cs].mean()) for z,cs in ZONES.items()}

allg=up_genes+dn_genes
zexpr=pd.DataFrame({g:zone_expr(g) for g in allg}).T
zexpr.index.name="TAIR_ID"
zexpr.insert(0,"direction",["up"]*len(up_genes)+["down"]*len(dn_genes))
zexpr.insert(0,"gene_symbol",[sym.get(g,"") for g in allg])
zexpr.round(3).to_csv(os.path.join(T,"nmf_root_zone_expression.csv"))

# ---------- root pictogram drawing ----------
def draw_root(ax, vals, norm, cmap):
    """Draw a longitudinal root-tip schematic; colour each compartment by vals[zone]."""
    def col(z): return cmap(norm(vals[z]))
    cx=5.0
    # nested longitudinal layers (body y 6..15): epidermis>cortex>endodermis>stele
    for hw,zn in [(2.0,"epidermis"),(1.55,"cortex/endodermis"),(1.12,"cortex/endodermis"),(0.72,"stele/vasculature")]:
        ax.add_patch(Rectangle((cx-hw,6),2*hw,9,facecolor=col(zn),edgecolor="none"))
    # meristem band (y 3.9..6) full width
    ax.add_patch(Rectangle((cx-2.0,3.9),4.0,2.1,facecolor=col("meristem (QC)"),edgecolor="none"))
    # root cap dome (bottom tip)
    ax.add_patch(Ellipse((cx,3.2),4.0,3.6,facecolor=col("root cap"),edgecolor="none"))
    # outline
    ax.add_patch(Rectangle((cx-2.0,6),4.0,9,fill=False,edgecolor="0.35",lw=0.6))
    ax.add_patch(Ellipse((cx,3.2),4.0,3.6,fill=False,edgecolor="0.35",lw=0.6))
    ax.set_xlim(2,8); ax.set_ylim(0.5,15.5); ax.set_aspect("equal"); ax.axis("off")

def grid_pictograms(genes, fname, title):
    if not genes: return
    vmin=float(np.nanpercentile(pb.values,5)); vmax=float(np.nanpercentile(pb.values,99))
    norm=Normalize(vmin,vmax); cmap=plt.get_cmap("YlOrRd")
    ncol=4; nrow=int(np.ceil(len(genes)/ncol))
    fig,axes=plt.subplots(nrow,ncol,figsize=(ncol*1.7,nrow*2.0))
    axes=np.atleast_1d(axes).ravel()
    for i,g in enumerate(genes):
        draw_root(axes[i],zone_expr(g),norm,cmap)
        axes[i].set_title(f"{label(g)}\n{g}",fontsize=6.5,pad=1)
    for j in range(len(genes),len(axes)): axes[j].axis("off")
    fig.suptitle(title,fontsize=10,y=0.997)
    sm=cm.ScalarMappable(norm=norm,cmap=cmap); sm.set_array([])
    cb=fig.colorbar(sm,ax=axes.tolist(),fraction=0.02,pad=0.01); cb.set_label("expression (log-CPM)",fontsize=8)
    fig.savefig(os.path.join(F,fname+".png"),dpi=200,bbox_inches="tight"); fig.savefig(os.path.join(F,fname+".svg"),bbox_inches="tight")
    plt.close(fig)

grid_pictograms(up_genes,"nmf_root_efp_up","NMF-UP threat loci — root expression pictograms (germinating-seed radicle)")
grid_pictograms(dn_genes,"nmf_root_efp_down","NMF-DOWN loci — root expression pictograms (germinating-seed radicle)")

# ---------- collective: up-set vs down-set vs net + quantitative zone heatmap ----------
up_mean={z:float(pb.loc[up_genes,cs].mean().mean()) for z,cs in ZONES.items()} if up_genes else {}
dn_mean={z:float(pb.loc[dn_genes,cs].mean().mean()) for z,cs in ZONES.items()} if dn_genes else {}
net={z:up_mean.get(z,np.nan)-dn_mean.get(z,np.nan) for z in ZONES}
# specificity means (for the location-contrast heatmap)
up_specz={z:float(spec.loc[up_genes,cs].mean().mean()) for z,cs in ZONES.items()} if up_genes else {}
dn_specz={z:float(spec.loc[dn_genes,cs].mean().mean()) for z,cs in ZONES.items()} if dn_genes else {}

# collective roots coloured by SPECIFICITY z (localization, not abundance) so the
# synergy/antagonism of *where* each set concentrates is visible
netz={z:up_specz.get(z,np.nan)-dn_specz.get(z,np.nan) for z in ZONES}
svmax=max(np.nanmax(np.abs(list(up_specz.values()))),np.nanmax(np.abs(list(dn_specz.values()))))
snorm=Normalize(-svmax,svmax); scmap=plt.get_cmap("RdBu_r")

fig=plt.figure(figsize=(11,5.0))
axA=fig.add_axes([0.03,0.07,0.19,0.72]); draw_root(axA,up_specz,snorm,scmap); axA.set_title(f"NMF-UP set\n(n={len(up_genes)})",fontsize=9)
axB=fig.add_axes([0.24,0.07,0.19,0.72]); draw_root(axB,dn_specz,snorm,scmap); axB.set_title(f"NMF-DOWN set\n(n={len(dn_genes)})",fontsize=9)
sm=cm.ScalarMappable(norm=snorm,cmap=scmap); sm.set_array([])
fig.colorbar(sm,ax=[axA,axB],fraction=0.03,pad=0.01).set_label("mean specificity z",fontsize=8)
# quantitative synergy/antagonism heatmap: UP, DOWN, and NET specificity per zone
axH=fig.add_axes([0.60,0.16,0.34,0.60])
S=pd.DataFrame({"UP\n(spec z)":up_specz,"DOWN\n(spec z)":dn_specz,"NET\n(up−down)":netz}).reindex(list(ZONES))
hv=np.nanmax(np.abs(S.values))
axH.imshow(S.values,cmap="RdBu_r",vmin=-hv,vmax=hv,aspect="auto")
axH.set_xticks(range(3)); axH.set_xticklabels(S.columns,fontsize=8); axH.set_yticks(range(len(S))); axH.set_yticklabels(S.index,fontsize=8)
for i in range(S.shape[0]):
    for j in range(S.shape[1]):
        axH.text(j,i,f"{S.values[i,j]:+.1f}",ha="center",va="center",fontsize=8,
                 color="white" if abs(S.values[i,j])>0.6*hv else "black")
axH.set_title("collective localization (specificity z)\nboth columns + = synergy · opposite sign = antagonism",fontsize=8)
fig.suptitle("NMF threat loci in the germinating-seed root — collective localization",fontsize=12,y=0.98)
fig.text(0.03,0.01,"Root map = germinating-seed single-cell radicle compartments (GSE182331); NMF-up = ROS-producing peroxidase/oxidase battery, NMF-down = ROS scavengers (SOD1, MSRB7).",fontsize=6.5,color="0.4")
fig.savefig(os.path.join(F,"nmf_root_efp_collective.png"),dpi=200,bbox_inches="tight"); fig.savefig(os.path.join(F,"nmf_root_efp_collective.svg"),bbox_inches="tight")
plt.close(fig)
print("wrote: down table/heatmap, root zone expression, eFP pictograms (up/down/collective)")
print("\nNMF-DOWN radicle-specific genes:\n",dn_tab.to_string(index=False) if dn_genes else "(none at z>=1.0)")
print("\nZone specificity (up vs down):")
print(pd.DataFrame({"UP_specz":up_specz,"DOWN_specz":dn_specz}).round(2).to_string())
