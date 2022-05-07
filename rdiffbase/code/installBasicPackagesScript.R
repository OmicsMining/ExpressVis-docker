source("./code/installPackages.R")

packagesFromBioconductor = c("limma", "DESeq2", "Biobase")
packagesFromCran = c("plumber", "dplyr", "purrr", "rjson")

lapply(packagesFromBioconductor, installOneBiocPackage)
lapply(packagesFromCran, installOnePackageNotFromBioconductor)

