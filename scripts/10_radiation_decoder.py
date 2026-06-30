#!/usr/bin/env python
"""Phase 3 ext — add radiation/ROS (DNA-damage) treatments to the perturbation model.

WT irradiated-vs-control contrasts from OSDR (radiation_and_ros_cleaned.csv studies), projected onto
the 122 seed panels via GSEA-prerank, then merged with the existing micro-gravity/GCR decoder matrix.
"""
import os, re, warnings
import numpy as np, pandas as pd, gseapy as gp
warnings.filterwarnings("ignore")
ROOT=os.environ.get("DEEPSPACE_ROOT") or os.path.dirname(os.path.dirname(os.path.abspath(__file__))); OSD=os.path.join(ROOT,"data","raw","osd")
PAN=os.path.join(ROOT,"panels","panel_library.csv"); OUT=os.path.join(ROOT,"results","tables")
C="Log2fc_"
# contrast -> (file, column, sign, OSD, agent, dose, time, class)
RAD={
"rad_100Gy_co60_90m_a":  ("GLDS-498",C+"(90 minute & Cobalt-60 gamma radiation)v(90 minute & non-irradiated)",1,"OSD-498","Co-60","100Gy","90min","radiation_acute"),
"rad_100Gy_co60_1440m_a":("GLDS-498",C+"(1440 minute & Cobalt-60 gamma radiation)v(1440 minute & non-irradiated)",1,"OSD-498","Co-60","100Gy","1440min","radiation_acute"),
"rad_100Gy_co60_180m":   ("GLDS-502",C+"(Wild Type & Cobalt-60 gamma radiation)v(Wild Type & non-irradiated)",1,"OSD-502","Co-60","100Gy","180min","radiation_acute"),
"rad_100Gy_co60_90m_b":  ("GLDS-508",C+"(Wild Type & Cobalt-60 gamma radiation & 90 minute)v(Wild Type & non-irradiated & nan Not Applicable)",1,"OSD-508","Co-60","100Gy","90min","radiation_acute"),
"rad_100Gy_co60_1440m_b":("GLDS-508",C+"(Wild Type & Cobalt-60 gamma radiation & 1440 minute)v(Wild Type & non-irradiated & nan Not Applicable)",1,"OSD-508","Co-60","100Gy","1440min","radiation_acute"),
"rad_100Gy_co60_90m_c":  ("GLDS-510",C+"(Cobalt-60 gamma radiation & 90 minute & Wild Type)v(non-irradiated & nan Not Applicable & Wild Type)",1,"OSD-510","Co-60","100Gy","90min","radiation_acute"),
"rad_100Gy_co60_1440m_c":("GLDS-510",C+"(Cobalt-60 gamma radiation & 1440 minute & Wild Type)v(non-irradiated & nan Not Applicable & Wild Type)",1,"OSD-510","Co-60","100Gy","1440min","radiation_acute"),
"rad_10cGy_cs137_24h":   ("GLDS-679",C+"(cesium-137 gamma radiation & 10 centigray & 24 hour)v(non-irradiated & 0 centigray & 24 hour)",1,"OSD-782","Cs-137","10cGy","24h","radiation_lowdose"),
"rad_100cGy_cs137_24h":  ("GLDS-679",C+"(cesium-137 gamma radiation & 100 centigray & 24 hour)v(non-irradiated & 0 centigray & 24 hour)",1,"OSD-782","Cs-137","100cGy","24h","radiation_lowdose"),
}
pl=pd.read_csv(PAN); pl["panel"]=pl.panel_source+"::"+pl.panel_group.astype(str)
gene_sets={p:g.gene.dropna().unique().tolist() for p,g in pl.groupby("panel")}

def rnk(fn,col,sign):
    path=os.path.join(OSD,fn+"_DGE.csv"); hdr=pd.read_csv(path,nrows=0).columns.tolist()
    tgt=col if col in hdr else next((h for h in hdr if h.strip('"')==col),None)
    if tgt is None:
        nrm=lambda s:re.sub(r"\s+"," ",s.strip().strip('"')); tgt=next((h for h in hdr if nrm(h)==nrm(col)),None)
    if tgt is None: raise KeyError(f"{fn}: {col}")
    d=pd.read_csv(path,usecols=["TAIR",tgt]).dropna(subset=["TAIR",tgt]).drop_duplicates("TAIR")
    return (d.set_index("TAIR")[tgt].astype(float)*sign).sort_values(ascending=False)

nescol={}; fdrcol={}; man=[]
for name,(fn,col,sign,osd,ag,dose,tm,cls) in RAD.items():
    r=rnk(fn,col,sign); print(f"[{name}] {len(r)} genes ({fn})")
    res=gp.prerank(rnk=r.reset_index(),gene_sets=gene_sets,min_size=10,max_size=200,
                   permutation_num=200,threads=4,seed=42,no_plot=True,outdir=None).res2d
    res["NES"]=pd.to_numeric(res["NES"],errors="coerce"); res["FDR q-val"]=pd.to_numeric(res["FDR q-val"],errors="coerce")
    res=res.set_index("Term"); nescol[name]=res["NES"]; fdrcol[name]=res["FDR q-val"]
    man.append(dict(contrast=name,OSD_ID=osd,GLDS=fn,agent=ag,dose=dose,time=tm,genotype="Wild Type",stressor_class=cls))

radnes=pd.DataFrame(nescol); radfdr=pd.DataFrame(fdrcol)
# merge with existing ug/GCR matrix
en=pd.read_csv(os.path.join(OUT,"decoder_nes_matrix.csv"),index_col=0)
ef=pd.read_csv(os.path.join(OUT,"decoder_fdr_matrix.csv"),index_col=0)
NES=en.join(radnes,how="outer"); FDR=ef.join(radfdr,how="outer")
NES.to_csv(os.path.join(OUT,"decoder_nes_matrix_v2.csv")); FDR.to_csv(os.path.join(OUT,"decoder_fdr_matrix_v2.csv"))

# class map for ALL contrasts
cls_map={c:"microgravity" for c in en.columns if c.startswith("ug_")}
cls_map.update({c:"radiation_GCR" for c in en.columns if c.startswith("gcr_")})
cls_map.update({n:RAD[n][7] for n in RAD})
pd.DataFrame(man).to_csv(os.path.join(OUT,"radiation_contrasts_manifest.csv"),index=False)
pd.Series(cls_map,name="stressor_class").to_csv(os.path.join(OUT,"contrast_classes.csv"))

print("\n==== combined perturbation matrix:",NES.shape[1],"contrasts x",NES.shape[0],"panels ====")
print("classes:",pd.Series(cls_map).value_counts().to_dict())
# headline: radiation effect on key germination-state + embryo panels
key=[i for i in NES.index if i.startswith("germ_state_time::") or i=="gehring_L1_tissue::Embryo"]
print("\nRadiation NES on key seed programs:")
print(NES.loc[key,list(RAD.keys())].round(2).to_string())
print("\nDONE")
