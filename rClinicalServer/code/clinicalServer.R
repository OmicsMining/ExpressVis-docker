library(plumber)
pr("plumber.R") %>%
  pr_run(host = "0.0.0.0", port = 8002)
