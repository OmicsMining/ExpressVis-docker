library(purrr)
library(dplyr)
library(plumber)

pr("plumber.R") %>%
  pr_run(port=8003)