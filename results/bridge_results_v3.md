# Bridge / shared latent v3 — within-source scaling (CANONICAL, supersedes v1/v2) — 2026-06-27

**Refinement.** Each germinating-seed axis is now z-scored **within each source** (dev ssGSEA separately,
stress NES separately) before combining, removing the score-type offset that dominated v2.
**Diagnostic:** point-biserial |corr| of PC1 with the dev-vs-stress source indicator dropped from
**0.56 (v2 joint) → 0.00 (v3 within-source)** — the source-type artifact is eliminated; the embedding now
reflects biology. `scripts/13_bridge_refine.py`. Outputs `bridge_latent_v3.csv`, `bridge_assignments_v3.csv`,
`bridge_{heatmap,embedding}_v3.{png,svg}`.

## Late-seed-dev → germinating-seed (now interpretable)
- **Embryo 3 DAP → hypocotyl cortex (early); Embryo 5 DAP → hypocotyl cortex (mid)** — a developmental
  progression toward germinating hypocotyl-cortex states (the embryo lineage that carries into germination).
- Funiculus/Ovule → provasculature (vascular strand identity); maternal Seed coat/Endosperm → mixed/unassigned
  (terminal tissues, as expected).

## Perturbation → germinating-seed (within-source scaled)
- microgravity: ug_root_dark → cortex/endodermis; ug_leaf_dark → cotyledon mesophyll.
- GCR: 40 & 80 cGy → hypocotyl cortex (late) (consistent).
- low-dose γ: 10 cGy → radicle epidermis; 100 cGy → cortex/endodermis.
- acute 100 Gy γ → provasculature / protophloem / columella (root-pole & vascular), strongest
  rad_100Gy_1440m_b → columella/root cap (z +2.64).

## Honesty note — method sensitivity
The **perturbation→germ argmax shifts across scaling versions** (v1/v2/v3), so bridge-level stress→cell-type
assignments are **suggestive, not robust**; v3 (within-source) is the methodologically preferred version and
supersedes v1/v2. By contrast, the **NMF-up → radicle apical meristem localization (z +7.96)** is robust
(direct expression specificity, not scaling-dependent) and remains the strongest single magnetic→seed signal.
Several inputs still map to "unassigned" germ clusters (8/11) = soft hits. Concordance, not causation.
