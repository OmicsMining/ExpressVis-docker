source("./code/installPackages.R")

packagesFromBioconductor = c("limma", "DESeq2", "Biobase", "org.Hs.eg.db", "org.Mm.eg.db", "org.Rn.eg.db")
packagesFromCran = c("plumber", "dplyr", "purrr", "rjson")

lapply(packagesFromBioconductor, installOneBiocPackage)
lapply(packagesFromCran, installOnePackageNotFromBioconductor)

