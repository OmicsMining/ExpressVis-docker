source("./code/installPackages.R")

# human 
installHumanChipAnnoPackages <- function() {
  humanAnnoPackages <- obtainBioPackagesOfAspecies("./annoPackagesInfo/9606_human_chip_packages.txt")
  installMultplieBiocAnnotationPackage(packageNames = humanAnnoPackages)
}
# mouse
installMouseChipAnnoPackages <- function() {
  mouseAnnoPackages <- obtainBioPackagesOfAspecies("./annoPackagesInfo/10090_mouse_chip_packages.txt")
  installMultplieBiocAnnotationPackage(packageNames = mouseAnnoPackages)
}
# rat
installRatChipAnnoPackages <- function() {
  ratAnnoPackages <- obtainBioPackagesOfAspecies("./annoPackagesInfo/10116_rat_chip_packages.txt")
  installMultplieBiocAnnotationPackage(packageNames = ratAnnoPackages)
}


installHumanChipAnnoPackages()
installMouseChipAnnoPackages()
installRatChipAnnoPackages()







