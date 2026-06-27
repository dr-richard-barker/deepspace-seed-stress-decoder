#!/usr/bin/env Rscript
# Phase 2 — export Gehring GSE295007 counts + annotations for scanpy marker-calling.
.libPaths("C:/Users/drric/R/win-library/4.6")
suppressMessages({ library(SeuratObject); library(Matrix) })

rds <- "C:/Users/drric/Downloads/nmf_seed_decoder/data/raw/GSE295007_ATLAS_merged_annotated_sigmods.rds"
od  <- "C:/Users/drric/Downloads/nmf_seed_decoder/data/processed/gehring"
dir.create(od, recursive = TRUE, showWarnings = FALSE)

obj <- readRDS(rds)
cat("loaded:", paste(dim(obj), collapse = " x "), "\n")

cnt <- GetAssayData(obj, assay = "RNA", layer = "counts")   # genes x cells, sparse
cat("counts:", paste(dim(cnt), collapse = " x "), "class", class(cnt)[1], "\n")

writeMM(cnt, file.path(od, "counts.mtx"))
writeLines(rownames(cnt), file.path(od, "genes.txt"))
writeLines(colnames(cnt), file.path(od, "cells.txt"))

# keep the annotation + module-score columns we care about
md <- obj[[]]
keep <- c("orig.ident","bio_rep","timepoint","nCount_RNA","nFeature_RNA","Phase",
          "level_1_annotation","level_2_annotation","level_3_annotation_abbr")
keep <- keep[keep %in% colnames(md)]
mod  <- grep("_modsc", colnames(md), value = TRUE)
write.csv(md[, c(keep, mod)], file.path(od, "metadata.csv"), row.names = TRUE)

cat("DONE -> ", od, "\n")
cat("genes:", nrow(cnt), " cells:", ncol(cnt), " modscore_cols:", length(mod), "\n")
