
requiredPackages <- c("plumber", "rjson", "tidyverse", "survival","survminer", "maxstat")
packageSource = "https://mirrors.tuna.tsinghua.edu.cn/CRAN"  # change this to your nearest mirror
lapply(requiredPackages, function(packageName) {
  if (!requireNamespace(packageName, quietly = TRUE)) {
    install.packages(packageName, repo = packageSource)
  }
})