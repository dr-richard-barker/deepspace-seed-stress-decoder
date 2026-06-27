"""deepspace — two FAIR tools for plant space-biology stress decoding.

DSRS (dsrs.recognize): recognize which space stressor a transcriptomic signature resembles.
GSAD (gsad.decode):    model a bulk transcriptome's predicted effect on the dry/germinating seed.
"""
from . import config, panels, projection, dsrs, gsad  # noqa: F401

__version__ = "0.1.0"
__all__ = ["config", "panels", "projection", "dsrs", "gsad"]
