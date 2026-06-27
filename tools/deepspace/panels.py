"""Panel library I/O — the seed cell-type / state marker panels (the decoder target space)."""
import pandas as pd
from . import config


def load_panels(path=None):
    """Return {panel_id: [genes]} from panel_library.csv (panel_id = source::group)."""
    df = pd.read_csv(path or config.PANEL_LIBRARY)
    df["panel"] = df["panel_source"] + "::" + df["panel_group"].astype(str)
    return {p: g["gene"].dropna().unique().tolist() for p, g in df.groupby("panel")}


def export_gmt(out_path=None, path=None):
    """Write the panel library as a standard GMT (interoperable gene-set format)."""
    sets = load_panels(path)
    out_path = out_path or config.PANEL_GMT
    with open(out_path, "w") as f:
        for name, genes in sets.items():
            f.write("\t".join([name, "deepspace_seed_panel", *genes]) + "\n")
    return out_path


def germ_celltype_labels(path=None):
    """{germ_cluster panel_id -> human cell-type label}."""
    ann = pd.read_csv(path or config.GERM_ANNOT)
    ann["cluster"] = ann["cluster"].astype(str)
    return {f"germ_cluster::{c}": f"{n} (cl{c})" for c, n in zip(ann["cluster"], ann["cell_type"])}, \
           dict(zip([f"{n} (cl{c})" for c, n in zip(ann.cluster, ann.cell_type)], ann["organ"]))
