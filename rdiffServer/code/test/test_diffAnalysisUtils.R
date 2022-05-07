library(testthat)
source("../diffAnalysis.utils.R")

test_that("format GEO series directory", {
  geoSeries1 <- "GSE999"
  subdir1    <- formatGEOfilePath(geoSeriesAcc = geoSeries1)
  expect_equal(subdir1, "GSEnnn")

  geoSeries2 <- "GSE12345"
  subdir2 <- formatGEOfilePath(geoSeriesAcc = geoSeries2)
  expect_equal(subdir2, "GSE12nnn")
})