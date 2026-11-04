# The Stimuli Decoders Ecosystem: Multi-Modal Integration of Space Biology Models

## Overview

Plant space biology investigates how terrestrial biological organisms adapt to non-terrestrial environments characterized by microgravity, cosmic ionizing radiation, altered atmospheric pressures, and systemic oxidative stress cascades. Over the course of recent research campaigns, our laboratory has developed specialized, complementary computational decoders addressing specific biological and biophysical axes:

1. **`deepspace-seed-stress-decoder` (This Framework)**: A single-cell resolution seed-susceptibility atlas and dual-tool software suite (**DSRS** + **GSAD**) that projects transcriptomic perturbation signatures onto dormant and germinating *Arabidopsis thaliana* seed programs.
2. **`Redox_decoder`**: A **Conditional Variational Autoencoder (CVAE)** framework trained on 232 harmonized transcriptomics studies (4,332 samples) that disentangles reactive oxygen species (ROS) transcriptional latent spaces from organ-level and developmental variation, validated across 38 NASA OSDR spaceflight missions.
3. **`arabidopsis_exploration_atmosphere`**: A tabular foundation modeling framework (**TabPFN v2**) that decouples barometric pressure (hypobaria) from oxygen partial pressure (hypoxia) across 130 microarrays to model plant responses to NASA Exploration Atmospheres ($56.5\text{ kPa} / 8.2\text{ psia}$, $34\%\ \text{O}_2$).
4. **`MASTA` (Max Planck MicroArray overlap Search Tool and Analysis)**: A systematic compendium of 592 microarray perturbation contrasts (cold shock, wounding, drought, auxin, gibberellin, cytokinin, brassinosteroid, and nutrient starvation) mapped via Affymetrix ATH1/GPL198.

---

## Architectural Synthesis

The table below delineates the mathematical, biological, and software roles of each component in the integrated ecosystem:

| Decoder / Resource | Core Machine Learning / Statistical Engine | Primary Biological Axis | Dimensionality / Scale | Role in the Ecosystem |
| :--- | :--- | :--- | :--- | :--- |
| **`deepspace-seed-stress-decoder`** | **GSEA Prerank / ssGSEA** onto 123 single-cell marker panels | Single-cell germinating seed susceptibility & multi-stressor convergence | 49 contrasts $\times$ 123 panels across 15 families | **The Master Reference Hub**: Maps any adult/vegetative or environmental perturbation onto developmental seed cell types and stages. |
| **`Redox_decoder`** | **Conditional VAE ($\beta=0.5$)** with 32D latent space | Continuous reactive oxygen species (ROS) disentanglement ($H_2O_2$, $^1\text{O}_2$, $O_3$, paraquat, chloroplast stress) | 20,869 genes across 4,332 samples | **The Biochemical Axis**: Provides genome-wide spaceflight ROS remodeling signatures ($\log_2 \text{err\_ratio}$) and discrete ROS species profiles. |
| **`arabidopsis_exploration_atmosphere`** | **TabPFN v2 (In-Context Prior-Data Fitted Network)** | Orthogonal decoupling of total pressure ($P_{\text{total}}$) from hypoxia ($pO_2$) | 22,746 genes across 130 hypobaric arrays | **The Atmospheric Axis**: Isolates pure barosensory mechanisms and NASA Exploration Atmosphere setpoints from normobaric hypoxia. |
| **`MASTA`** | **Rank Product (RankProd)** non-parametric meta-analysis | Comprehensive environmental, mechanical, hormonal, and nutrient perturbations | 592 contrasts (top/down 5,000 DEGs per contrast) | **The Empirical Benchmark Library**: Provides ground-truth signatures for cold shock, launch vibration/wounding, and plant hormone signaling. |

---

## Cross-Model Workflow

```
[Query Transcriptome (Bulk RNA-seq / Microarray)]
                     │
         ┌───────────┴───────────┐
         ▼                       ▼
  [Redox CVAE]          [TabPFN v2 Atmosphere]
   - Disentangle ROS     - Decouple Pressure vs O2
   - Latent shift (z)    - Beta hypobaria / hypoxia
         │                       │
         └───────────┬───────────┘
                     ▼
       [deepspace DSRS Engine]
        - Compares query seed-program fingerprint
          against the 49-contrast reference library
        - Recognizes stressor class & family
                     │
                     ▼
       [deepspace GSAD Engine]
        - Decodes query onto 15 single-cell clusters
        - Outputs cell-type susceptibility & stage
                     │
                     ▼
       [DeepSpace Seed Atlas v8]
        - Evaluates radicle-tip convergence
        - Tests stage (12h vs 24h vs 48h) vulnerability
```

---

## Headline Findings from the v8 Integration

1. **Radicle Root Cap & Meristem Remain the Multi-Stressor Hotspot**:
   - In the expanded 15-family model, `columella/root cap (+QC) (cl4)` converges on **14 of 15 stressor families**, and `radicle apical meristem (cl14)` converges on **10 of 15 families**.
   - The addition of pure hypobaria, NASA exploration atmosphere ($50\text{ kPa}$ Norm$O_2$), and mechanical wounding reinforces that physical boundary layers and active growth centers are the primary targets of spaceflight stress.
2. **Distinct Atmospheric Responses**:
   - `exploration_50kPa_normO2` significantly activates radicle apical meristem programs ($\text{NES} = +1.98$) and cotyledon mesophyll ($\text{NES} = +2.30$), demonstrating that hypobaria itself—independent of oxygen depletion—induces distinct developmental remodeling.
3. **Early Germination (12 hsl) and Dry Seed Vulnerability**:
   - Across the 15 families, the dry seed (0h) and early germination (12 hsl) stages exhibit susceptibility to 12 and 10 stressor families respectively, confirming that early metabolic reactivation is the most vulnerable window for deep-space agriculture.
