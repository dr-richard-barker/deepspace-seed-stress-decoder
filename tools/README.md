# deepspace — two tools for plant space-biology stress decoding

Distilled, reusable software behind the DeepSpace seed-susceptibility atlas.

| Tool | Module | What it does |
|---|---|---|
| **DSRS** — DeepSpace Stress-Recognition System | `deepspace.dsrs` | Given a transcriptomic perturbation signature, **recognize which space stressor it resembles** across 49 contrasts and 15 families (gravity, radiation, low-oxygen, hypobaria, redox_ros, cold, wounding, hormone signaling, nutrients, desiccation, osmotic, temperature, UV). |
| **GSAD** — Germinating-Seed AutoDecoder | `deepspace.gsad` | Given **bulk transcriptomics**, model its **predicted effect on the dry/germinating seed** — a per cell-type / tissue / stage susceptibility profile. |
| **MASTA** — Microarray Overlap Search Bridge | `deepspace.masta` | Programmatic and CLI bridge to query, load, and project any of the 592 contrasts from the Max Planck MASTA database directly through DSRS and GSAD. |

Both share one projection engine: rank the query by log2FC and GSEA-project it onto the **123 seed
cell-type/state panels** (122 single-cell panels from the Gehring developmental + germination atlases,
plus a bulk dry-seed anchor).

## Install
```bash
cd tools && pip install -e .
# requires the repo's panels/ and results/tables/ (the panel library + stress reference) alongside.
# set DEEPSPACE_ROOT to point elsewhere if needed.
```

## Use (Python)
```python
import deepspace
top, fam = deepspace.dsrs.recognize("my_signature.csv")     # which stressor?
seed = deepspace.gsad.decode("my_signature.csv")            # effect on the seed
seed["celltype"].head()                                     # ranked seed cell-type susceptibility
```

## Use (CLI)
```bash
deepspace dsrs my_signature.csv --out matches.csv
deepspace gsad my_signature.csv --out seed_susceptibility.csv
deepspace masta-project "S851&cold_wt-wt_3h" --out cold_seed_profile.csv
deepspace masta-list -c S                                     # list available stress contrasts
deepspace export-gmt                                          # panel library -> standard GMT
```

**Input:** a CSV/TSV with two columns — gene (AGI/TAIR, e.g. `AT1G01010`) and log2FC — or pass
`--gene/--lfc` to name columns. Outputs are concordance scores with the project's evidence-tier framing
(predicted concordance, not proven causation).

See `examples/example_usage.py`.
