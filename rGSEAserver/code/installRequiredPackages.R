requiredPackages <- c("plumber", "rjson", "purrr", "dplyr", "tidyverse")

packageSource = "https://mirrors.tuna.tsinghua.edu.cn/CRAN"  # change this to your nearest mirror
lapply(requiredPackages, function(packageName) {
  if (!requireNamespace(packageName, quietly = TRUE)) {
    install.packages(packageName, repo = packageSource)
  }
})



packageSource = "https://mirrors.tuna.tsinghua.edu.cn/CRAN"
bioSource     = "https://mirrors.tuna.tsinghua.edu.cn/bioconductor"


options(BioC_mirror="https://mirrors.tuna.tsinghua.edu.cn/bioconductor") 
options(stringsAsFactors =  F)

installOneBiocPackage <- function(packageName) {
  # options(BioC_mirror="https://mirrors.tuna.tsinghua.edu.cn/bioconductor")
  if (!requireNamespace("BiocManager", quietly = TRUE)) {
    install.packages("BiocManager", repo = packageSource)   
  }
  if ((packageName %in% rownames(installed.packages())) == FALSE) {
    BiocManager::install(packageName)
    cat(packageName)
    cat("\n")
  } else {
    cat("Has been installed\n")
  }
}

installOneBiocPackage("fgsea")

