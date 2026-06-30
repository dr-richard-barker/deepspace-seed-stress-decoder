#!/usr/bin/env python
"""Phase 2 ext — anchor the dry/0h pole: add a 'dry_seed' state panel to the germination state axis.

The germination atlas starts at 12 hsl (dry/0h under-sampled). The mature dry seed (end of maturation) IS
the dormant dry-seed state at germination 0 h. Define a dry-seed marker panel from GSE76015 (seed
desiccation): genes up in mature dry seed (21 DAF) vs hydrated immature (15 DAF), averaged over 3 WT
ecotypes (Col-0, Ws, Ler). Append as germ_state_time::dry_seed so the state axis spans dry -> 12/24/48 hsl.
"""
import os, numpy as np, pandas as pd
ROOT=os.environ.get("DEEPSPACE_ROOT") or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SV=os.path.join(ROOT,"data","raw","stressors_v2"); PAN=os.path.join(ROOT,"panels")
cpm=pd.read_csv(os.path.join(SV,"GSE76015_desic_cpm.csv.gz"),index_col=0)
cpm=cpm[cpm.index.astype(str).str.startswith("AT")]
dry=cpm[["col021","ws21","ler21"]].mean(1)
hyd=cpm[["col015","ws15","ler15"]].mean(1)
lfc=np.log2((dry+1)/(hyd+1))
expr=dry>2                                  # require real expression in dry seed
sig=lfc[expr].sort_values(ascending=False)
TOP=50
panel=sig.head(TOP)
print(f"dry_seed panel: top {TOP} dry-up genes (log2 {panel.min():.2f}..{panel.max():.2f}); e.g. {list(panel.index[:6])}")

# append to panel_library.csv and panel_library_annotated.csv
rows=pd.DataFrame({"panel_source":"germ_state_time","panel_group":"dry_seed","gene":panel.index,
                   "rank":range(1,len(panel)+1),"logfoldchanges":panel.values,"pvals_adj":0.0,"score":panel.values})
pl=pd.read_csv(os.path.join(PAN,"panel_library.csv"))
pl=pl[~((pl.panel_source=="germ_state_time")&(pl.panel_group=="dry_seed"))]   # idempotent
pl=pd.concat([pl,rows],ignore_index=True); pl.to_csv(os.path.join(PAN,"panel_library.csv"),index=False)
pla=pd.read_csv(os.path.join(PAN,"panel_library_annotated.csv"))
pla=pla[~((pla.panel_source=="germ_state_time")&(pla.panel_group=="dry_seed"))]
rows2=rows.copy(); rows2["panel_label"]="dry_seed"
pla=pd.concat([pla,rows2],ignore_index=True); pla.to_csv(os.path.join(PAN,"panel_library_annotated.csv"),index=False)
print("appended germ_state_time::dry_seed to panel_library (+annotated). total panels:",
      pl.assign(p=pl.panel_source+"::"+pl.panel_group).p.nunique())
