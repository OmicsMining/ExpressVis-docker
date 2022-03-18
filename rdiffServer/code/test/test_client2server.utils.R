source("../client2server.utils.R")

library(testthat)

test_that("should return a matrix containing row names and column names", {
  valuesList <- list( sample1 = c(1, 3, 4), 
                      sample2 = c(5, 2, 1),
                      sample3 = c(1, 2, 1))
  genes <- c("gene1", "gene3", "gene2")

  valuesMatrix <- convertValuesList2matrix(valuesList, genes)

  expect_equal(colnames(valuesMatrix), c("sample1", "sample2", "sample3"))
})

test_that("should return a diff group pair list", {
  
})