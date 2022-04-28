# use tuna mirrors if used in China Mainland
# Change mirrors if needed

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


installOnePackageNotFromBioconductor <- function(packageName){
  if (!requireNamespace(packageName, quietly = TRUE)) {
    install.packages(packageName, repo = packageSource)
  }
}


installMultplieBiocAnnotationPackage <- function(packageNames) {
  installedPackages <- rownames(installed.packages())
  notInstalledPackages <- unique(setdiff(packageNames, installedPackages))
  cat(notInstalledPackages)
  while (length(notInstalledPackages) >= 1) {
    lapply(notInstalledPackages, installOneBiocPackage)
    installedPackages <- rownames(installed.packages())
    notInstalledPackages <- unique(setdiff(packageNames, installedPackages))
  }
}

# main
obtainBioPackagesOfAspecies <- function(filePath) {
  packageNames <- read.delim(filePath, header =  T) $ Package
  return (packageNames)
}

obtainBioPackagesInfoOfAspecies <- function (filePath) {
  packagesInfo <- read.delim(filePath, header =  T)
  return (packagesInfo)
}








