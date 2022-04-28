source("./code/installPackages.R")
# basic packages used in all server
packagesFromCran = c("plumber", "dplyr", "purrr", "rjson",  "tidyverse")

lapply(packagesFromCran, installOnePackageNotFromBioconductor)
