# Bridge / shared-latent v1 (2026-06-26)

**Layer-2 design.** A single "germinating-seed score space": the 15 named germinating-seed cell types
are the latent axes. Both bridge inputs are placed into it relative to the dry/germinating reference:
- **Adult stress** (OSD µg/GCR) → coordinates = decoder NES across the 15 germ cell types.
- **Late-seed-dev** (Gehring) → coordinates = ssGSEA of each tissue×timepoint pseudobulk vs the 15 germ panels.
Columns z-scored across all inputs. Outputs: `results/tables/bridge_latent.csv`,
`bridge_assignments.csv`; `results/figures/bridge_heatmap.{png,svg}`, `bridge_embedding.{png,svg}`.

## Findings

### Adult stress → germinating-seed state (strong, z 1.4–2.1)
- µg_leaf_dark → **hypocotyl cortex (mid, cl7)** (z +2.05)
- µg_root_dark → **cortex/endodermis (cl2)** (z +1.96)
- gcr_40cGy → **epidermis (cl6)** (z +2.00); gcr_80cGy & µg_*_light → **unassigned (cl8/cl11)**
  (caveat: unassigned clusters lack a clear identity — treat those hits cautiously).

### Late-seed-dev → germinating-seed state (WEAK, z 0.37–0.68) — itself the key result
- Developmental seed tissues map only **weakly and non-specifically** onto germinating-embryo cell types.
- The mappings that do appear concentrate on root-pole identities (columella/root cap, protoxylem,
  radicle epidermis) for embryo/endosperm 3–7 DAP.
- **Interpretation:** this is biologically expected — only the **embryo lineage** persists from
  development through dry/dormant into germination; the **maternal seed coat and endosperm are terminal**
  tissues with no germinating-embryo counterpart. So the dev→germination bridge is real but lineage-limited.

## Caveats / refinements (next pass)
1. **Scale artifact in the heatmap.** Stress NES has larger spread than dev ssGSEA-NES, so column z-scoring
   makes dev rows look washed out. The per-input argmax (assignments table) is the robust readout. Fix:
   z-score *within source*, or rank-normalize, before the joint figure.
2. **Restrict dev to embryo lineage** (Gehring EMB level_2/level_3) for a cleaner dev→germination bridge —
   maternal/endosperm tissues dilute the signal.
3. **Dry/0 h pole** still under-sampled (germ earliest = 12 hsl).
4. Still a **concordance/label-transfer** statement, not causation.
