source("../obtainEnrichedAnnotations.R")
library(testthat)

test_that("should obtain enriched annotations", {
  load(file=file.path(here::here(),"/testData/examplePathways.rda"))
  load(file=file.path(here::here(),"/testData/exampleRanks.rda"))
  
  print("geneset")
  print(examplePathways[1:5])
  print(examplePathways[["186574_Endocrine-committed_Ngn3+_progenitor_cells"]])
  print("rank")
  print(exampleRanks[1:5])
  fgseaRes <- gseaAnalysis(genset=examplePathways,
                           rank=exampleRanks,
                           minSize=3, 
                           maxSize=500, 
                           nperm=10000)
  print(dim(fgseaRes))
  
})