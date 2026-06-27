# deepspace — two tools for plant space-biology stress decoding

Distilled, reusable software behind the DeepSpace seed-susceptibility atlas.

| Tool | Module | What it does |
|---|---|---|
| **DSRS** — DeepSpace Stress-Recognition System | `deepspace.dsrs` | Given a transcriptomic perturbation signature, **recognize which space stressor it resembles** (microgravity, radiation, low-oxygen, tropism, magnetic/NMF…) by matching its seed-program fingerprint to a reference stressor library. |
| **GSAD** — Germinating-Seed AutoDecoder | `deepspace.gsad` | Given **bulk transcriptomics**, model its **predicted effect on the dry/germinating seed** — a per cell-type / tissue / stage susceptibility profile. |

Both share one projection engine: rank the query by log2FC and GSEA-project it onto the **122 seed
cell-type/state panels** (Gehring developmental + germination atlases).

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
deepspace export-gmt                                        # panel library -> standard GMT
```

**Input:** a CSV/TSV with two columns — gene (AGI/TAIR, e.g. `AT1G01010`) and log2FC — or pass
`--gene/--lfc` to name columns. Outputs are concordance scores with the project's evidence-tier framing
(predicted concordance, not proven causation).

See `examples/example_usage.py`.
