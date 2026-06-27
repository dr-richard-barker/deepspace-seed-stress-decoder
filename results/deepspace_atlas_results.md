# DeepSpace seed-susceptibility atlas — v1 (2026-06-27)

**The headline deliverable.** For each germinating-seed cell type, which of **5 deep-space stressor
families** significantly target it, and a multi-stressor **convergence** count.
Families: gravity (microgravity + partial-g), tropism (gravi + photo), low_oxygen (hypoxia/anoxia/
submergence), radiation (GCR + low + acute γ), magnetic_NMF (NMF localization).
Significance: |NES|≥1.5 & FDR<0.25 (decoder); |z|≥2 (NMF localization).
`scripts/18_deepspace_atlas.py` → `results/figures/deepspace_seed_atlas.png`,
`results/tables/deepspace_atlas_{nes,family,convergence}.csv`.

## Headline answer — YES, the radicle/root tip is a multi-stressor convergence hotspot
| germinating-seed cell type | organ | families | which |
|---|---|---|---|
| **radicle apical meristem (cl14)** | radicle | **4 / 5** | gravity, tropism, radiation, **magnetic/NMF** |
| columella / root cap +QC (cl4) | radicle | 4 / 5 | gravity, tropism, low_oxygen, radiation |
| cotyledon mesophyll (cl3) | cotyledon | 4 / 5 | gravity, low_oxygen, radiation, magnetic/NMF |
| radicle epidermis (cl10) | radicle | 3 / 5 | gravity, tropism, radiation |
| (unassigned cl8 / cl11) | — | 4–5 | soft — clusters lack a defined identity |

- **All three radicle/root-tip cell types (apical meristem, columella/root cap, epidermis) are top-ranked**
  for multi-stressor convergence → the **root tip is the most consistently deep-space-susceptible region**.
- The radicle apical meristem carries the strongest **magnetic/NMF** signal (localization z +7.96) plus
  gravity, tropism, and radiation — 4 of 5 independent families.
- Cotyledon mesophyll is the main non-root hotspot (photosynthetic programs hit by gravity/low-O₂/radiation/NMF).

## Why it's robust
- Uses **family-level** convergence (≥1 significant contrast per family), so radiation's 11 contrasts don't
  dominate; each family contributes one vote.
- Converges with independent evidence threads already established: NMF localization, light-gated µg,
  gravitropism (root-tip), and the developmental hypophysis→radicle-meristem lineage edge.

## Caveats
- "Unassigned" germ clusters (cl8/cl11) top the raw count but lack identity → report the radicle apical
  meristem (4/5) as the top **biologically-defined** hotspot.
- Mixed evidence tiers across families (NMF = localization; phototropism/hypoxia = microarray/translatome).
- Concordance, not causation; thresholds (|NES|≥1.5, FDR<0.25) are reported and adjustable.

---

## Tissue- and stage-level atlas (2026-06-27) — `scripts/19`, fig `deepspace_atlas_tissue_stage.png`

**Germination STAGE (the dry→germinating axis):**
- **12 hsl (early germination) = most multi-stressor stage: 4/5 families** (gravity, tropism, radiation,
  magnetic/NMF). 24 hsl = 3; 48 hsl = 3 (incl. strong NMF-up enrichment, z +3.9).
- → **early germination is the most deep-space-vulnerable window**, consistent with the cross-stressor
  "12 h attractor." (DRY/0 h is under-sampled — germination atlas starts at 12 hsl; flagged.)

**Developing-seed TISSUE (Gehring level_1):** signal is **diffuse / noisier than cell-type or stage**:
Ovule 4, Seed coat 3, Embryo 2, Endosperm 2, Funiculus 1. **Caveat:** Ovule is a tiny maternal tissue
(172 cells) and maternal tissues (ovule/seed-coat) over-weight here — treat tissue-level as supplementary.
The biologically meaningful resolution is **cell-type × stage**, not broad developmental tissue.

**Combined headline across resolutions:** the **radicle/root-tip cell types** (cell-type atlas) at the
**early-germination (12 h) stage** (stage atlas) are the DeepSpace convergence hotspot.
