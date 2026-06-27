# Radiation / ROS perturbations added to the model (2026-06-26)

**Source.** `radiation_and_ros_cleaned.csv` (dr-richard-barker/Plant_response_to_radiation) → 5 OSDR
RNA-seq studies pulled as genome-wide DGE and projected onto the 122 seed panels (GSEA-prerank), then
merged with the existing micro-gravity/GCR decoder → **combined model: 15 contrasts × 122 panels**.

**Contrasts added (WT, irradiated-vs-control):**
| class | contrasts | studies |
|---|---|---|
| radiation_acute (100 Gy γ) | 7 (90 & 1440 min) | OSD-498, OSD-502, OSD-508, OSD-510 (Co-60) |
| radiation_lowdose (cGy γ) | 2 (10 & 100 cGy, 24 h) | OSD-782 (Cs-137) |
| (already in model) GCR | 2 (40, 80 cGy) | OSD-658 |
| (already) microgravity | 4 | OSD-120, OSD-678 |

`sog1-1` and `myb3r1` DNA-damage-response mutant contrasts are available in OSD-502/508/510 for
mechanistic follow-up; the model uses WT (environmental radiation effect).

## Findings (figure: `results/figures/decoder_combined_perturbation_heatmap.png`)
- **Acute 100 Gy γ at early time (90 min) strongly induces embryo + early-germination (12 h) programs**
  (e.g. OSD-498 90 min: Embryo +1.87, 12 hsl +2.12; OSD-508 90 min: Embryo +1.67) — a rapid
  DNA-damage/ROS transcriptional surge resembling the early-germination state, echoing the GCR-80 and
  µg "12 h attractor" signal. Convergent across stressor classes.
- **Time reversal:** by 1440 min (24 h) several programs flip sign (repair/resolution phase).
- **Low-dose (cGy) responses are weaker and dose-graded** (Cs-137 10 vs 100 cGy; GCR 40/80 cGy) — the
  space-relevant dose range, distinct from the acute 100 Gy mechanistic references.

## Caveats
- **100 Gy is a mechanistic DNA-damage dose, not space-relevant** (spaceflight GCR is cGy-scale). Treat
  acute-γ contrasts as DNA-damage/ROS references; the cGy studies (OSD-658, OSD-782) are the
  dose-relevant ones.
- **Study-level heterogeneity:** OSD-508 vs OSD-510 (companion sog1 studies) give partly opposite WT
  signs on some panels — different experiments/batches; interpret per-study, not pooled.
- Concordance, not causation (as throughout).
