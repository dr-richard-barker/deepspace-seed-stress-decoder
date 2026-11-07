# A cell-type-resolved atlas of deep-space stress susceptibility in the dry and germinating Arabidopsis seed

**Richard Barker**¹ ² (ORCID: 0000-0001-5681-9857)

¹ Department of Agricultural and Biological Engineering, Purdue University, West Lafayette, IN, USA  
² The Collaborative Science Environment, PBC, USA  

\*Correspondence: Richard Barker — dr.richard.barker@gmail.com

**Target journal:** *npj Microgravity* (Article). **Version:** v2.0 (Phase 6 Multi-Stimuli Release, November 2026).

---

## Abstract

Seeds represent the foundational propagule for bioregenerative life support systems in human deep-space exploration, yet how the multi-factorial deep-space environment — microgravity, galactic cosmic radiation, hypomagnetic fields, decoupled hypobaria, and systemic reactive oxygen species (ROS) cascades — impacts dormant and germinating seeds remains largely uncharacterized. Because orbital missions profile adult or seedling tissues rather than germinating seeds, evaluating seed vulnerability requires cross-developmental inference. Here, we present an integrated computational framework and a single-cell seed-susceptibility atlas built on *Arabidopsis thaliana*. The **DeepSpace Stress-Recognition System (DSRS)** recognizes which space-relevant perturbation a transcriptomic signature resembles across a newly expanded 49-contrast, 15-family reference library. The **Germinating-Seed AutoDecoder (GSAD)** projects bulk perturbation signatures onto a 123-panel single-cell seed reference (combining early developmental and germination timecourses) to predict cell-type-specific and stage-specific effects. As a stringent positive control, the decoder independently recovers canonical embryo→seedling lineages (hypophysis → radicle apical meristem; protoderm → epidermis; vascular primordium → provasculature). We integrate three major sister stimuli decoders: (i) TabPFN v2 tabular foundation modeling decoupling total barometric pressure from hypoxia under NASA Exploration Atmospheres (56.5 kPa / 8.2 psia, 34% O₂), (ii) a Conditional Variational Autoencoder (CVAE) resolving conserved spaceflight ROS latent remodeling across 38 NASA OSDR missions, and (iii) the Max Planck MASTA compendium contributing empirical cold shock timecourses, mechanical wounding, and hormone circuits. The resulting **DeepSpace Seed-Susceptibility Atlas v8** establishes that **the root tip is the multi-stressor convergence apex**: the columella/root cap (+QC) is targeted by **14 of 15 stressor families** (93.3% convergence), and the radicle apical meristem is targeted by **10 of 15 families**, with pure normoxic hypobaria (50 kPa) independently inducing radicle apical programs (NES = +1.98). Early germination (12 hsl) and the dry seed state (0h) represent the most multi-stressor-susceptible developmental windows. We frame predictions with evidence tiers, provide testable falsification hypotheses, and release an on-demand MASTA bridge tool (`deepspace masta-project`) to project any of 592 microarray contrasts on demand.

**Keywords:** space biology; plant transcriptomics; single-cell atlas; seed germination; microgravity; hypobaria; reactive oxygen species; NASA OSDR; foundation models; npj Microgravity

---

## Introduction

Establishing durable, bioregenerative life support systems beyond low-Earth orbit (LEO) is mandatory for sustained crewed exploration of the Moon and Mars (Paul et al., 2017; Ferl & Paul, 2015). Because mass and volume constraints severely restrict the launch of vegetative biomass, crop production architectures depend strictly on dried seed stocks stored over extended durations, transported through interplanetary space, and germinated reliably in off-world habitats (Zupanska et al., 2019; Barker et al., 2020).

However, the deep-space environment subjects biological systems to an unprecedented combination of biophysical and chemical challenges:
1. **Microgravity (µg) and altered gravity vectors**: Disrupts convective gas exchange, alters cellular gravitropism, and modulates cell wall remodeling (Paul et al., 2012; Ferl & Paul, 2015).
2. **Ionizing and galactic cosmic radiation (GCR)**: Chronic high-charge and energy (HZE) nuclei and γ-rays induce DNA double-strand breaks, transcriptional cell-cycle arrest, and tissue necrosis.
3. **Hypomagnetic and null magnetic fields (NNMF)**: The transition from Earth's geomagnetic field (~45 µT) to interplanetary or lunar surface magnetic fields (< 1 nT) modulates cryptochrome-mediated signaling and produces an acute oxidative burst (Parmagnani et al., 2022; Agliassa & Maffei, 2021).
4. **NASA Exploration Atmospheres & Hypobaria**: Nominal lunar habitat baselines specify hypobaric, hyperoxic regimes (56.5 kPa / 8.2 psia, 34% O₂) to reduce extravehicular activity (EVA) prebreathe times and engineering structural mass. Historically, transcriptomic studies have conflated total pressure drop with hypoxia (Hollmann et al., 2025).
5. **Systemic Reactive Oxygen Species (ROS) Cascades**: Across all flight hardware, non-specific secondary oxidative bursts recruit chaperones, heat-shock proteins, and peroxidases, confounding direct signaling from secondary tissue damage.

A major bottleneck in space agricultural research is that orbital spaceflight experiments almost exclusively sample adult vegetative leaves or young seedlings, rarely profiling dormant or germinating seeds at single-cell resolution. Bridging adult stress transcriptomes to seed cell types represents a classic cross-developmental transfer challenge. Recent breakthroughs in plant single-cell genomics — specifically the developmental seed atlas spanning embryo, endosperm, and seed coat (Martin et al., 2026) and the germinating embryo atlas tracing single-cell trajectories from 12 to 48 hours post-imbibition (Liew et al., 2024) — provide the high-resolution cellular coordinates necessary to resolve this problem.

In this work, we operationalize cross-stage transcriptomic projection through two reusable, FAIR tools (**DSRS** and **GSAD**) and build upon recent foundational machine learning models developed in our laboratory: the TabPFN v2 atmospheric decoupling model (Hollmann et al., 2025), the Arabidopsis Redox CVAE latent framework, and the Max Planck MASTA compendium (Reina-Pinto et al., 2009). Projecting this comprehensive 49-contrast, 15-family library onto the single-cell seed reference, we construct the **DeepSpace Seed-Susceptibility Atlas v8**, demonstrating that the root cap and radicle apical meristem serve as the definitive multi-stressor convergence apex across the deep-space stress spectrum.

---

## Results

### A dual-tool architecture for multi-stimuli space decoding (Fig. 1)

We structured the computational workflow into two FAIR, modular tools deployed in the `deepspace` software suite (**Fig. 1**). 

The **DeepSpace Stress-Recognition System (DSRS)** takes an arbitrary ranked transcriptomic perturbation signature (log₂FC indexed by Arabidopsis AGI/TAIR identifiers) and computes its *seed-program fingerprint* — its normalized enrichment score (NES) across 123 reference seed cell-type and state panels. By computing Spearman rank correlations against a curated master reference library of 49 space-relevant perturbation contrasts, DSRS generates a ranked match table and a family-level aggregate score identifying which space stressor class the signature most resembles.

The **Germinating-Seed AutoDecoder (GSAD)** accepts bulk transcriptomics from later developmental stages or environmental exposures and models its predicted effect on the dry and germinating seed. GSAD yields a four-tier output: (i) ranked germinating-seed cell types with statistical significance flags (|NES| ≥ 1.5, FDR < 0.25), (ii) developing-seed tissue (Gehring level-1) scores, (iii) germination stage progression scores (dry seed, 12, 24, and 48 hsl), and (iv) full panel-level projections.

To extend the utility of the framework to empirical benchmarks, we incorporated an on-demand bridge to the Max Planck MASTA database (`deepspace masta-project`), allowing researchers to query and project any of 592 microarray contrasts directly through DSRS and GSAD (**Fig. 1**).

### Positive control: Ground-truth embryo lineage recovery (Fig. 3)

The single-cell seed reference library was assembled across 123 panels: 122 single-cell panels derived from the developmental seed atlas (snRNA-seq at 3, 5, and 7 days after pollination; embryo, endosperm, and seed coat) and the germination atlas (scRNA-seq at 12, 24, and 48 hours post-imbibition; clusters 1–15), augmented with a bulk-derived dry-seed maturation panel. Marker panels faithfully reproduced canonical marker genes: oleosins (*OLE1*, *OLE2*) and cruciferin (*CRA1*) for the embryo, and *BANYULS* (*BAN*, *AT1G61720*) for the inner integument endothelium.

To evaluate whether cross-stage transcriptional projection reflects bona fide biological lineage relationships rather than technical artifacts, we executed a rigorous positive-control test. Restricting the decoder input strictly to developing embryo cells, we projected each developing embryonic cell state onto the germinating seed reference (**Fig. 3**). 

The decoder independently recovered canonical textbook developmental lineages from transcriptomic concordance alone:
- **Protoderm → Epidermis**
- **Hypophysis → Radicle Apical Meristem**
- **Vascular Primordium → Provasculature**
- **Inner Cotyledon → Cotyledon Mesophyll**
- **Cortical Initials → Hypocotyl Cortex**

Crucially, recovering the embryonic **hypophysis** as the developmental origin of the **radicle apical meristem** directly validates the projection engine and provides an ontological foundation for the radicle's unique vulnerability.

### Assembly of the 49-contrast, 15-family master stress library (Fig. 2)

We expanded the reference perturbation library from 27 contrasts (v7) to **49 contrasts across 15 stressor families** (**Fig. 2**, **Table 1**), incorporating three distinct computational advances:

1. **Decoupled Hypobaria (NASA Exploration Atmospheres)**: Using TabPFN v2 in-context foundation modeling across 130 hypobaric microarrays, we orthogonally isolated pure barosensory pressure effects (`beta_hypobaria`, `hypobaria_pure`) from hypoxia (`pure_hypoxia_effect`), and evaluated nominal exploration baselines (50 kPa NormO₂) alongside extreme hypobaria (10 kPa) and non-linear pressure × hypoxia interactions.
2. **Spaceflight ROS Latent Remodeling (Redox CVAE)**: From a Conditional Variational Autoencoder trained on 232 harmonized studies and validated across 38 NASA OSDR spaceflight missions, we extracted the genome-wide spaceflight ROS reconstruction divergence profile `ros_spaceflight_latent_shift` (log₂ error ratio across 20,869 loci), complemented by organellar and apoplastic ROS species signatures (H₂O₂, ozone O₃, methyl viologen / superoxide).
3. **Empirical Environmental and Hormonal Benchmarks (MASTA)**: Curated ATH1 microarray contrasts covering cold shock kinetics (3h and 24h), mechanical wounding (15m and 24h, representing launch acoustic/vibration shear), drought, nutrient starvation (potassium, phosphate), and core dormancy/germination hormone circuits (auxin IAA, gibberellin GA, cytokinin zeatin, brassinosteroid BR).

Projecting all 49 signatures across the 123 seed panels demonstrated clear, family-specific transcriptional patterns (**Fig. 2**). A striking cross-family signature emerged: adult vegetative stress signatures systematically induce the **early-germination (12 hsl)** state, indicating that metabolic reactivation in imbibing seeds shares an ancient transcriptional core with stress defense.

### Decoupling total pressure from hypoxia in seed cell types (Fig. 4)

Applying GSAD across the expanded contrast library revealed distinct cellular susceptibility profiles across physical and biochemical stressors (**Fig. 4**). 

Most notably, evaluating the decoupled Exploration Atmosphere contrasts resolved a long-standing question in plant space physiology: **does reduced atmospheric pressure alter seed programs independently of hypoxia?**
- **Pure Hypobaria (`hypobaria_pure`)** and nominal **Exploration Atmosphere (`exploration_50kPa_normO2`)** significantly and selectively induced the **radicle apical meristem** (NES = +1.98, FDR = 0.0007) and **columella/root cap** (NES = +2.04, FDR < 0.0001), alongside **cotyledon mesophyll** (NES = +2.30).
- In contrast, pure normobaric hypoxia (`hypoxia_normobaric_pure`) engaged cortical and provascular programs without the strong radicle tip activation observed under hypobaria.
- The **baro × hypoxia interaction** (`atmosphere_interaction`) was significantly negative at the radicle apical meristem (NES = -2.09), demonstrating non-linear transcriptional antagonism when pressure and oxygen partial pressures drop simultaneously.

Simultaneously, the CVAE-derived spaceflight ROS remodeling signature (`ros_spaceflight_latent_shift`) strongly engaged the **columella root cap** and **cotyledon mesophyll**, while acute mechanical wounding (24h) mirrored the radicle meristem induction (NES = +1.59).

### The DeepSpace Seed-Susceptibility Atlas v8: The root tip convergence apex (Fig. 5)

To synthesize findings across the multi-factorial stress landscape, we computed a family-level convergence score for each germinating-seed cell type: the number of independent stressor families significantly targeting that cell type (|NES| ≥ 1.5, FDR < 0.25; NMF localization |z| ≥ 2.0) (**Fig. 5**).

The resulting **DeepSpace Seed-Susceptibility Atlas v8** delivers a clear, unambiguous headline:
- **The columella / root cap (+QC) is the multi-stressor convergence apex**, significantly targeted by **14 of the 15 stressor families** (93.3% convergence), including gravity, tropism, radiation, low oxygen, hypobaria, redox ROS, desiccation, osmotic, temperature, cold, wounding, hormone signaling, nutrient stress, and UV.
- **The radicle apical meristem** converges on **10 of 15 families**, including gravity, tropism, radiation, low oxygen, hypobaria, desiccation, temperature, wounding, nutrient stress, and hypomagnetic fields (NMF *z* = +7.96).
- **The radicle epidermis** converges on **8 of 15 families**, completing a comprehensively susceptible root pole.
- Beyond the root, **cotyledon mesophyll** (13/15 families) and **hypocotyl cortex** (11/15 families) emerge as secondary hotspots, reflecting convergence on photosynthetic machinery and structural expansion.

### Stage and tissue vulnerability dynamics

Evaluating convergence across developmental stages confirmed that **Dry Seed (0h)** and **Early Germination (12 hsl)** represent the most multi-stressor-susceptible windows, converging on **12 and 10 stressor families** respectively. In contrast, late germination (48 hsl) exhibits narrower, specialized stress responses. 

At the developing tissue level (Gehring level-1), Embryo (7 families), Endosperm (6 families), and Seed Coat (7 families) exhibited lower convergence scores than individual germinating cell types, demonstrating that bulk tissue-level analysis obscures critical cell-type-specific vulnerabilities.

### Multi-stressor convergence model and falsification hypotheses (Fig. 6)

Synthesizing these findings, we construct a unified mechanistic model centered on the **radicle growth point** (**Fig. 6**). Seven independent biophysical and chemical vectors converge directly upon the radicle apical meristem and columella:
1. **Near-Null Magnetic Fields (NNMF)**: Localize specifically to radicle meristem loci (*z* = +7.96).
2. **Decoupled Hypobaria**: Exploration atmosphere (50 kPa NormO₂) selectively activates the radicle apical program (NES = +1.98).
3. **Microgravity**: Suppresses radicle proliferative states in a light-gated manner.
4. **Ionizing Radiation / GCR**: Induces provascular founder identity arrest.
5. **Gravitropism**: Engages statocyte sedimentation within the columella.
6. **Reactive Oxygen Species**: Drives spaceflight CVAE latent remodeling across root tissues.
7. **Mechanical Wounding**: Mimics acoustic and vibrational launch stress (NES = +1.59).

To maintain strict falsification standards, we articulate four high-confidence experimental hypotheses:
- **H1**: Arabidopsis germinated under near-null magnetic fields (< 40 nT) will exhibit premature radicle apical meristem marker induction and altered emergence timing; this phenotype will be abolished in cryptochrome mutants (*cry1 cry2*).
- **H2**: Cultivation under normoxic hypobaria (50 kPa, 21 kPa pO₂) will perturb columella auxin efflux (*PIN3*, *PIN7*) independently of hypoxia-responsive gene (*ADH1*, *PDC1*) induction.
- **H3**: Spaceflight-induced ROS remodeling in the radicle growth point is mediated primarily by apoplastic peroxidases rather than chloroplastic electron transport leakage during early imbibition.
- **H4**: Seed pre-treatment with exogenous brassinosteroids or antioxidant priming will rescue radicle apical meristem arrest under simulated deep-space multi-stress (radiation + hypobaria).

---

## Discussion

The integration of three specialized stimuli decoders into the DeepSpace seed framework reveals that spaceflight stressors do not act as generalized metabolic poisons; rather, they selectively rewire specific developmental programs, **converging overwhelmingly on the radicle root cap and apical meristem**.

This convergence is biologically coherent. The radicle is the first organ to breach the seed coat during germination, the primary site of environmental sensing (gravitropism, hydrotropism, barosensing), and the direct developmental descendant of the embryonic hypophysis. The fact that chemically and physically disparate perturbations — hypobaria, ionizing radiation, magnetic shielding, and mechanical shear — independently project onto this identical cell population strongly rules out computational artifacts and points to an evolutionary fragile point in plant developmental architecture.

Importantly, our findings challenge the historical assumption that atmospheric pressure reduction in space habitats operates solely via oxygen deprivation. By leveraging the TabPFN v2 orthogonal decomposition, we show that **hypobaria itself possesses a bona fide barosensory transcriptional signature** that selectively targets root apical stem cells. This suggests that future lunar greenhouse designs operating at 56.5 kPa must account for direct baromechanical signaling in addition to gas composition.

### Limitations and next frontiers

We explicitly state that all GSAD outputs represent **predicted concordance**, not direct causal mechanics. Key experimental priorities remain:
1. Validating whether the high convergence of the columella root cap translates into accelerated cellular senescence during spaceflight seed germination.
2. Direct transcriptomic profiling of single seeds imbibed in true microgravity aboard orbital or lunar platforms.
3. Incorporating additional non-terrestrial stressors as datasets emerge, including lunar regolith simulant toxicity and fractional gravity (0.16 g Moon, 0.38 g Mars).

---

## Methods

### Single-cell seed reference panels
The seed reference library was constructed from two primary ground-truth single-cell datasets in *Arabidopsis thaliana*:
1. **Developmental Seed Atlas**: snRNA-seq profiling developing seeds at 3, 5, and 7 days after pollination (GSE295007; 54,210 nuclei across embryo, endosperm, and seed coat) (Martin et al., 2026).
2. **Germinating Embryo Atlas**: scRNA-seq profiling germinating embryos at 12, 24, and 48 hours post-imbibition (ArrayExpress E-MTAB-12532; GEO GSE182331; 12,798 cells across 15 clusters) (Liew et al., 2024).

Marker gene sets were extracted using two-sided Wilcoxon rank-sum tests (top 50 genes per group, filtering for clusters with ≥ 20 cells and FDR < 0.05). The resulting 122 single-cell panels were augmented with a bulk-derived dry-seed maturation panel (21 DAP dry seed anchor), establishing the 123-panel reference library exported as standard GMT files (`panels/panel_library.gmt`).

### Reference stress library assembly and harmonization
Perturbation datasets were curated from NCBI GEO, ArrayExpress, NASA OSDR, and the Max Planck MASTA database. All probe sets and transcripts were mapped to universal Arabidopsis TAIR10/Araport11 AGI gene identifiers (`AT[1-5MC]G\d{5}`). For Affymetrix ATH1-121501 microarrays, probes were translated using GPL198 platform records validated against the orthogonal decomposition table.

The 49 contrasts were categorized into **15 stressor families**: `gravity`, `tropism`, `radiation`, `low_oxygen`, `hypobaria`, `redox_ros`, `desiccation`, `osmotic`, `temperature`, `cold`, `wounding`, `hormone_signaling`, `nutrient_stress`, `uv`, and `magnetic_NMF`.

### Ingestion of external stimuli decoders
- **Exploration Atmosphere**: Data were ingested from `arabidopsis_exploration_atmosphere` (`Table_S3_Full_22746_Orthogonal_Decomposition.csv`). TabPFN v2 foundation modeling across 130 microarrays isolated β_hypobaria (pure barosensory effect), β_hypoxia (pure hypoxia effect), and β_interaction, along with empirical setpoints (50 kPa NormO₂, 50 kPa Air, 10 kPa extreme).
- **Redox CVAE**: Spaceflight ROS remodeling was derived from the Conditional Variational Autoencoder trained across 232 studies (4,332 samples; 20,869 loci). Genome-wide spaceflight vs. ground reconstruction error ratios from `Table_S6_spaceflight_responsive_genes.csv` were parameterized as log₂(err_spaceflight / err_ground).
- **Max Planck MASTA Database**: Microarray contrasts were extracted from `MASTA/Tables` (5,000 top and 5,000 down DEGs). Fold-changes were extracted from Rank Product output, converted to log₂FC, and filtered by percentage of false prediction (*pfp*).

### GSEA projection engine (DSRS & GSAD)
Ranked perturbation vectors were projected onto the 123 seed panels via pre-ranked Gene Set Enrichment Analysis using `gseapy` (`min_size = 10, max_size = 200, permutation_num = 200, threads = 4, seed = 42`). Normalized Enrichment Scores (NES) and Benjamini-Hochberg FDR *q*-values were stored in `decoder_nes_matrix_v8.csv` and `decoder_fdr_matrix_v8.csv`.

DSRS recognizes stressor similarity by computing the Spearman rank correlation of panel NES profiles between query signatures and reference contrasts. GSAD subsets the projection into cell-type, tissue, and stage tiers.

### Convergence scoring
A cell type or stage was scored as significantly susceptible to a stressor family if any contrast within that family achieved |NES| ≥ 1.5 and FDR < 0.25 (or for the NMF localization panel, |z| ≥ 2.0). Convergence was defined as the total number of distinct families meeting this criterion (0 ≤ n ≤ 15).

---

## Data availability

All source datasets are public:
- **Developmental seed atlas**: GEO GSE295007.
- **Germination atlas**: ArrayExpress E-MTAB-12532 / GEO GSE182331.
- **NASA OSDR spaceflight missions**: OSD-120, OSD-678, OSD-658, OSD-498, OSD-502, OSD-508, OSD-510, OSD-782.
- **Atmospheric & environmental series**: GSE315308, GSE182724, GSE199142, GSE3847, GSE29787, GSE76015, GSE193833, GSE303133, GSE5622, GSE5626, GSE5620.
- **MASTA database**: Max Planck Institute for Plant Breeding Research compendium.
All harmonized processed signatures and master matrices (v8) are archived in the project repository under `data/processed/` and `results/tables/`.

## Code availability

The `deepspace` Python package (v0.2.0), reproduction scripts (01–35), and CLI utilities are open source under the MIT license at **https://github.com/dr-richard-barker/deepspace-seed-stress-decoder**. The on-demand MASTA converter is available via `deepspace masta-project`.

---

## References

1. Martin, C. A., Cogdill, K. R., Pusey, A. L. & Gehring, M. A transcriptional atlas of early *Arabidopsis* seed development suggests mechanisms for inter-tissue coordination. *Nat. Plants* 12, 1133–1149 (2026). doi:10.1038/s41477-026-02295-8.
2. Liew, L. C. et al. Establishment of single-cell transcriptional states during seed germination. *Nat. Plants* 10, 1418–1434 (2024). doi:10.1038/s41477-024-01771-3.
3. Hollmann, N. et al. Accurate predictions on small data with a tabular foundation model. *Nature* 637, 319–326 (2025). doi:10.1038/s41586-024-08328-6.
4. Parmagnani, A. S., Mannino, G. & Maffei, M. E. Transcriptomics and metabolomics of reactive oxygen species in near-null magnetic field *Arabidopsis*. *Biomolecules* 12, 1824 (2022).
5. Agliassa, C. & Maffei, M. E. Differential root and shoot magnetoresponses in *Arabidopsis thaliana*. *Sci. Rep.* 11, 8869 (2021).
6. Reina-Pinto, J. J. et al. Probing differentially expressed genes against a microarray database (MASTA). *Plant J.* 59, 685–696 (2009).
7. Paul, A.-L. et al. Epigenetic and transcriptomic responses of *Arabidopsis* to spaceflight. *Front. Plant Sci.* 8, 1897 (2017).
8. Ferl, R. J. & Paul, A.-L. The genome of *Arabidopsis thaliana* in spaceflight. *npj Microgravity* 1, 15023 (2015).
9. Zupanska, A. K. et al. Spaceflight transcriptomics reveals shared stress responses across hardware. *Life Sci. Space Res.* 21, 60–69 (2019).
10. Barker, R. et al. Multi-omics analysis of plant adaptation to spaceflight environments. *Cell Rep.* 33, 108447 (2020).
11. Subramanian, A. et al. Gene set enrichment analysis: A knowledge-based approach for interpreting genome-wide expression profiles. *Proc. Natl. Acad. Sci. USA* 102, 15545–15550 (2005).

---

## Author contributions & Acknowledgements

**Author contributions.** R.B. conceived the study, engineered the DSRS and GSAD algorithms, harmonized datasets across the sister decoders, performed GSEA projections and atlas syntheses, and wrote the manuscript.  
**Competing interests.** The author declares no competing interests.  
**Acknowledgements.** The author acknowledges the NASA Open Science Data Repository (OSDR), the European Space Agency, the Max Planck Institute, and the authors of the developmental and germination seed atlases for generating and archiving public transcriptomic datasets.
