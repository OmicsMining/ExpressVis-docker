requiredPackages <- c("plumber", "purrr", "dplyr", "tidyverse", "rjson")


packageSource = "https://mirror-hk.koddos.net/CRAN/"  # change this to your nearest mirror
lapply(requiredPackages, function(packageName) {
  if (!requireNamespace(packageName, quietly = TRUE)) {
    install.packages(packageName, repo = packageSource)
  }
})


packageSource = "https://mirror-hk.koddos.net/CRAN/"
bioSource     = "https://mirrors.tuna.tsinghua.edu.cn/bioconductor"


# options(BioC_mirror=bioSource) 
options(stringsAsFactors = F)

installOneBiocPackage <- function(packageName) {
  # options(BioC_mirror="https://mirrors.tuna.tsinghua.edu.cn/bioconductor")
  # Do not use tsinghua.edu mirror in Aliyun
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

installOneBiocPackage("sva")


