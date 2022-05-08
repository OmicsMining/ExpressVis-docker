library(purrr)
library(dplyr)
library(plumber)
<<<<<<< HEAD
=======

>>>>>>> 3e7dc60221e199caf6a7ae64e0934eacd5980d0d
pr("plumber.R") %>%
  pr_run(host = "0.0.0.0", port = 8003)