source("../constructEset.R")
library(testthat)

test_that("construct a eset", {
  samples      <- c("sample1", "sample2", "sample3")
  genes        <- c("gene1", "gene2")
  
  valuesMatrix <- matrix(c(1, 2, 1, 2, 1, 2), nrow = 2, byrow = TRUE)
  colnames(valuesMatrix) <- samples
  rownames(valuesMatrix) <- c("gene1", "gene2")
  
  resultEset <- constructEsetFromExpressionMatrix(valuesMatrix)
  expect_equal(featureNames(resultEset), genes)
})


