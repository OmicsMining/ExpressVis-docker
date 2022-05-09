library(purrr)
library(dplyr)
library(plumber)
<<<<<<< HEAD
=======

>>>>>>> 80183f187c006f4ba3ea86984fff3e1427401daa
pr("plumber.R") %>%
  pr_run(host = "0.0.0.0", port = 8003)