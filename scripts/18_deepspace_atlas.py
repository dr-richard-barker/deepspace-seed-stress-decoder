#!/usr/bin/env python
"""Phase 5.4 — DeepSpace seed-susceptibility ATLAS (headline deliverable).

For each germinating-seed cell type: which deep-space stressor FAMILIES significantly target it, and a
multi-stressor CONVERGENCE count. Answers: is the radicle apical tip hit by multiple stressor families?

Families (5): gravity (microgravity+partial-g), tropism (gravi+photo), low_oxygen, radiation (GCR+low+acute),
magnetic_NMF (NMF localization). Significance: NES |>=1.5| & FDR<0.25 ; NMF localization |z|>=2.
Outputs: results/tables/deepspace_atlas_{nes,family,convergence}.csv ; figures/deepspace_seed_atlas.{png,svg}
"""
import os, numpy as np, pandas as pd
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
ROOT=r"C:\Users\drric\Downloads\nmf_seed_decoder"; T=os.path.join(ROOT,"results","tables"); F=os.path.join(ROOT,"results","figures"); PAN=os.path.join(ROOT,"panels")
NES=pd.read_csv(os.path.join(T,"decoder_nes_matrix_v7.csv"),index_col=0)
FDR=pd.read_csv(os.path.join(T,"decoder_fdr_matrix_v7.csv"),index_col=0)
cls=pd.read_csv(os.path.join(T,"contrast_classes.csv"),index_col=0)["stressor_class"].to_dict()
ann=pd.read_csv(os.path.join(PAN,"germination_cluster_annotations.csv")); ann["cluster"]=ann.cluster.astype(str)
cl2lab={c:f"{n} (cl{c})" for c,n in zip(ann.cluster,ann.cell_type)}; organ=dict(zip([cl2lab[c] for c in ann.cluster],ann.organ))

# germ cell-type rows -> labels
g=[i for i in NES.index if i.startswith("germ_cluster::")]
A=NES.loc[g].copy(); Af=FDR.loc[g].copy()
A.index=[cl2lab[i.split("::")[1]] for i in A.index]; Af.index=A.index
A.to_csv(os.path.join(T,"deepspace_atlas_nes.csv"))

# NMF localization column (magnetic family)
nmf=pd.read_csv(os.path.join(T,"nmf_localization.csv"),index_col=0)["NMF_up_localization_z"]

# family map
fam={}
for c in A.columns:
    k=cls.get(c,"other")
    fam[c]=("gravity" if k in("microgravity","partial_gravity","hypergravity") else
            "tropism" if k in("tropism_gravi","tropism_photo") else
            "low_oxygen" if k=="low_oxygen" else
            "radiation" if k.startswith("radiation") else k)
families=["gravity","tropism","low_oxygen","desiccation","osmotic","ethylene","temperature","uv","radiation","magnetic_NMF"]
SIG_NES=1.5; SIG_FDR=0.25; SIG_NMFZ=2.0

# family susceptibility (binary) + signed strength
famhit=pd.DataFrame(0,index=A.index,columns=families)
famval=pd.DataFrame(0.0,index=A.index,columns=families)
for ct in A.index:
    for f_ in set(fam.values()):
        cols=[c for c in A.columns if fam[c]==f_]
        sig=[(abs(A.loc[ct,c])>=SIG_NES and Af.loc[ct,c]<SIG_FDR) for c in cols]
        if any(sig):
            famhit.loc[ct,f_]=1
            # signed strength = NES with max |NES| among significant
            best=max([A.loc[ct,c] for c,s in zip(cols,sig) if s], key=abs); famval.loc[ct,f_]=best
    # NMF (magnetic)
    z=nmf.get(ct,np.nan)
    if pd.notna(z) and abs(z)>=SIG_NMFZ: famhit.loc[ct,"magnetic_NMF"]=1; famval.loc[ct,"magnetic_NMF"]=z

conv=famhit.sum(1).sort_values(ascending=False)
out=pd.DataFrame({"cell_type":conv.index,"organ":[organ.get(c,"?") for c in conv.index],
                  "n_families":conv.values,
                  "families_hit":[", ".join([f for f in families if famhit.loc[c,f]]) for c in conv.index]})
out.to_csv(os.path.join(T,"deepspace_atlas_convergence.csv"),index=False)
famhit.to_csv(os.path.join(T,"deepspace_atlas_family.csv"))

# ---- figure: family susceptibility heatmap + convergence bar ----
order_org={"cotyledon":0,"hypocotyl":1,"radicle":2,"provasculature":3,"unassigned":4}
rows=sorted(famval.index,key=lambda c:(-conv[c], order_org.get(organ.get(c,"z"),9)))
V=famval.loc[rows,families]; vmax=np.nanmax(np.abs(V.values)) or 1
# 3-column layout: heatmap | dedicated colorbar | convergence bars (no overlap)
fig=plt.figure(figsize=(11.5,0.5*len(rows)+1.9))
gs=fig.add_gridspec(1,3,width_ratios=[len(families),0.4,2.0],wspace=0.45)
ax=fig.add_subplot(gs[0]); cax=fig.add_subplot(gs[1]); axb=fig.add_subplot(gs[2])
im=ax.imshow(V.values,cmap="RdBu_r",vmin=-vmax,vmax=vmax,aspect="auto")
ax.set_xticks(range(len(families))); ax.set_xticklabels(families,rotation=40,ha="right",fontsize=8)
ax.set_yticks(range(len(rows))); ax.set_yticklabels(rows,fontsize=8)
for i,ct in enumerate(rows):
    for j,f_ in enumerate(families):
        if famhit.loc[ct,f_]: ax.text(j,i,"*",ha="center",va="center",fontsize=12,fontweight="bold")
ax.set_title("DeepSpace seed-susceptibility atlas  (* = significant; color = signed strength)",fontsize=10)
cb=fig.colorbar(im,cax=cax); cb.set_label("signed strength (NES / NMF z)",fontsize=7); cax.tick_params(labelsize=7)
axb.barh(range(len(rows)),conv[rows].values,color="#555"); axb.invert_yaxis()
axb.set_ylim(len(rows)-0.5,-0.5); axb.set_yticks([]); axb.set_xlim(0,len(families)+0.5)
axb.set_xlabel(f"n families (/{len(families)})",fontsize=8); axb.set_title("convergence",fontsize=9)
for i,ct in enumerate(rows): axb.text(conv[ct]+0.15,i,str(int(conv[ct])),va="center",fontsize=7)
fig.savefig(os.path.join(F,"deepspace_seed_atlas.png"),dpi=200,bbox_inches="tight")
fig.savefig(os.path.join(F,"deepspace_seed_atlas.svg"),bbox_inches="tight")

print("==== DeepSpace seed-susceptibility atlas — convergence ranking ====")
print(out.to_string(index=False))
print("\nRADICLE check:")
for c in out.cell_type:
    if "radicle" in c.lower() or "columella" in c.lower():
        print(f"  {c}: {int(conv[c])} families -> {out.set_index('cell_type').loc[c,'families_hit']}")
print("\nDONE")
