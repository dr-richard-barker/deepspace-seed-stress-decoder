"""Default paths for the deepspace tools (overridable)."""
import os
from pathlib import Path

# repo root = two levels up from this file (tools/deepspace/config.py -> repo root)
ROOT = Path(os.environ.get("DEEPSPACE_ROOT", Path(__file__).resolve().parents[2]))
PANEL_LIBRARY = ROOT / "panels" / "panel_library.csv"
PANEL_GMT     = ROOT / "panels" / "panel_library.gmt"
GERM_ANNOT    = ROOT / "panels" / "germination_cluster_annotations.csv"
# stress reference library (panels x stressor contrasts) + classes
REF_NES       = ROOT / "results" / "tables" / "decoder_nes_matrix_v5.csv"
REF_FDR       = ROOT / "results" / "tables" / "decoder_fdr_matrix_v5.csv"
CONTRAST_CLASS= ROOT / "results" / "tables" / "contrast_classes.csv"
