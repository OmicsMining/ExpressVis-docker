library(testthat)
source("../deseq2.R")
library(jsonlite)


test_that("Differential analysis RNA-seq", {
  arrayID      <- "E-GEOD-51261"
  storeDir     <- "../../testData/rawData/"
  countsMatrix <- readCounts(arrayID  = arrayID, 
                             storeDir = storeDir) 
  diffGroupPairList = list(list(baseGroup = c("SRR1004852", "SRR1004853", "SRR1004854"), targetGroup = c("SRR1004855", "SRR1004856", "SRR1004857")), 
                           list(baseGroup = c("SRR1004855", "SRR1004856", "SRR1004857"), targetGroup = c("SRR1004852", "SRR1004853", "SRR1004854")))
  
  diffResultList <- deseq2DiffMultipleGroupParis( 
    countsMatrix      = countsMatrix,
    diffGroupPairList = diffGroupPairList
  )
  # diffResults  <- deseq2Diff(countsMatrix  = countsMatrix, 
  #                            baseSamples   = c("SRR1004852", "SRR1004853", "SRR1004854"), 
  #                            targetSamples = c("SRR1004855", "SRR1004856", "SRR1004857"))
  expect_equal(length(diffResultList), 2)
  # expect_equal(diffResults["ENSG00000000003", "padj"], 0.1014812)
})