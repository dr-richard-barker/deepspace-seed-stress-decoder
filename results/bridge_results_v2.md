# Bridge / shared latent v2 — full perturbation panel (2026-06-27)

Extends bridge v1 to the **full 15-contrast perturbation panel** (microgravity + radiation) alongside the
late-seed-dev trajectory, in one germinating-seed score space (15 axes). **27 inputs × 15 axes.**
Outputs: `results/tables/bridge_latent_v2.csv`, `bridge_assignments_v2.csv`;
`results/figures/bridge_heatmap_v2.{png,svg}`, `bridge_embedding_v2.{png,svg}`.
Cached `results/tables/gehring_dev_pseudobulk.csv` for reuse.

## Stress → nearest germinating-seed cell type
| class | contrast | nearest germ cell type | z |
|---|---|---|---|
| microgravity | ug_root_dark | **radicle apical meristem** | +1.81 |
| microgravity | ug_leaf_dark | cotyledon mesophyll | +1.88 |
| microgravity | ug_root_light / ug_leaf_light | unassigned (cl8) | +1.18 / +1.50 |
| radiation_GCR | gcr_40cGy | hypocotyl cortex (late) | +1.82 |
| radiation_GCR | gcr_80cGy | unassigned (cl8) | +1.72 |
| radiation_lowdose | rad_10cGy_cs137_24h | radicle epidermis | +1.33 |
| radiation_lowdose | rad_100cGy_cs137_24h | cortex/endodermis | +1.41 |
| radiation_acute | rad_100Gy_1440m_b | columella/root cap (+QC) | +2.13 |
| radiation_acute | rad_100Gy_90m_b | provasculature | +1.55 |
| radiation_acute | rad_100Gy_1440m_c | provasculature: protophloem | +1.44 |
| radiation_acute | (others) | unassigned (cl8/cl11) | soft |

## Key reads
- **Convergence on the radicle growth-point:** µg-root-dark → radicle apical meristem here aligns with
  the NMF localization result (NMF-up genes → radicle apical meristem) and the SMF root/auxin literature —
  three perturbation types pointing at the radicle program.
- **Radiation favors root-pole / provascular identities** (columella, provasculature/protophloem,
  cortex-endodermis), echoing the decoder's radiation→provascular/embryo theme.
- **Late-seed-dev points cluster tightly and apart** from the perturbations.

## Caveats
- **Source-type axis:** in the PCA embedding, PC1 largely separates dev (ssGSEA) from stress (NES) —
  a score-type difference, not pure biology. Use the per-axis assignments (above), not cross-source
  distance, as the robust readout. (Within-source scaling is the queued refinement.)
- Several perturbations map to "unassigned" germ clusters (8/11) → soft, low-confidence hits.
- Concordance, not causation.
