#renv::load("/media/thudxz/Research/process/bioinformatics_tools/angular_django_time_series/r-clinical")
library(plumber)
pr("plumber.R") %>%
  pr_run(host = "0.0.0.0", port=8002)
# use pr_run(host = "0.0.0.0", port = 8002) when used in container
