#!/usr/bin/env Rscript
# Phase 2 — inspect the Gehring developmental seed atlas (GSE295007) Seurat object.
# Goal: learn structure (assays, cell-type metadata cols, idents) WITHOUT full Seurat,
# so we can export counts + labels for marker-panel building in scanpy.

.libPaths("C:/Users/drric/R/win-library/4.6")
suppressMessages(library(SeuratObject))

rds <- "C:/Users/drric/Downloads/nmf_seed_decoder/data/raw/GSE295007_ATLAS_merged_annotated_sigmods.rds"
out <- "C:/Users/drric/Downloads/nmf_seed_decoder/results/tables/gehring_object_summary.txt"

con <- file(out, open = "wt"); sink(con); sink(con, type = "message")
cat("=== Gehring GSE295007 object inspection ===\n")
cat("file:", rds, "\n")
t0 <- Sys.time()
obj <- readRDS(rds)
cat("loaded in", round(difftime(Sys.time(), t0, units = "secs"), 1), "s\n")
cat("class:", paste(class(obj), collapse = ", "), "\n\n")

if (inherits(obj, "Seurat")) {
  cat("dim (features x cells):", paste(dim(obj), collapse = " x "), "\n")
  cat("assays:", paste(Assays(obj), collapse = ", "), "\n")
  cat("default assay:", DefaultAssay(obj), "\n")
  try({ cat("layers:", paste(Layers(obj), collapse = ", "), "\n") }, silent = TRUE)
  cat("reductions:", paste(Reductions(obj), collapse = ", "), "\n\n")
  md <- obj[[]]
  cat("meta.data columns (", ncol(md), "):\n", sep = "")
  print(colnames(md))
  cat("\n--- candidate annotation columns (factor/character, <100 levels) ---\n")
  for (c in colnames(md)) {
    v <- md[[c]]
    if (is.factor(v) || is.character(v)) {
      n <- length(unique(v))
      if (n <= 100) { cat("\n##", c, "(", n, "levels):\n"); print(sort(table(v), decreasing = TRUE)) }
    }
  }
  cat("\n--- Idents levels ---\n"); print(levels(Idents(obj)))
} else {
  cat("NOT a Seurat object; str():\n"); str(obj, max.level = 2)
}
sink(type = "message"); sink(); close(con)
cat("DONE -> ", out, "\n")
