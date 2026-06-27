# Download manifest

Commands NOT yet executed — awaiting compute go-ahead. Target dir: `data/raw/`.

## Phase 2 — seed atlases (unblocked, both public)

### Gehring developmental atlas — GEO GSE295007 (Seurat .rds; needs R to open)
Base: `https://ftp.ncbi.nlm.nih.gov/geo/series/GSE295nnn/GSE295007/suppl/`

| File | Size | Need? |
|---|---|---|
| GSE295007_ATLAS_merged_annotated_sigmods.rds | 1.3 GB | **YES** — merged annotated atlas → cell-type markers |
| GSE295007_GSE2950073_merged_annotated_sigmods.rds | 3.9 GB | maybe (3 DAP detail) |
| GSE295007_GSE2950075_merged_annotated_sigmods.rds | 2.5 GB | maybe (5 DAP detail) |
| GSE295007_GSE2950077_merged_annotated_sigmods.rds | 2.0 GB | maybe (7 DAP detail) |
| GSE295007_RAW.tar | 348 MB | fallback (raw matrices if avoiding R) |
| filelist.txt | 1.7 KB | yes (index) |

Minimal pull = merged atlas (1.3 GB) + filelist. Full = ~10 GB.

```bash
cd data/raw
curl -O https://ftp.ncbi.nlm.nih.gov/geo/series/GSE295nnn/GSE295007/suppl/GSE295007_ATLAS_merged_annotated_sigmods.rds
curl -O https://ftp.ncbi.nlm.nih.gov/geo/series/GSE295nnn/GSE295007/suppl/filelist.txt
```

### Germination atlas — ArrayExpress E-MTAB-12532 (scRNA-seq)
Browse: `https://www.ebi.ac.uk/biostudies/arrayexpress/studies/E-MTAB-12532`
FTP: `https://ftp.ebi.ac.uk/biostudies/.../E-MTAB-12532/Files/` (resolve exact path before pull)
Companions: E-MTAB-12521 (bulk protoplasting controls), E-MTAB-13449 (TF-mutant RNA-seq)

## Phase 3 — bridge inputs (NASA OSDR; already in Biomni repo)
- OSD-120 / OSD-678 / OSD-658 → reuse Biomni-derived DE; re-download from OSDR only if raw needed.

## NMF (reframed Phase 1)
- Maffei 194-gene panel: already in Biomni repo (`long_NMF_Maffei2022.csv.gz`, S2 supplement). Pull from repo.
- GSE29787 (high-field comparator): GEO, ~microarray; pull only if used as labeled contrast.
- Full Maffei array: pending author request (see report/maffei_data_request_email.md).
