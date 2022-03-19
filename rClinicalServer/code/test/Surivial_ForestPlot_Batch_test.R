library(testthat)
library(tidyverse)
source("../Surivial_ForestPlot_Batch.R")

test_that("Forest plot, test", {
  splitDF <- read_csv(file = "../../testData/Proteomics_SurvivalSplit_TestFile-HighLowSplit.csv")
  splitDF <- splitDF[, 1:10]
  patientIDcol <- "PatientID"; endpointStatusCol <- "OS Status"; endpointTimeCol <- "OS"
  coxRes <- survivalAnnotation(splitDF = splitDF, patientID = patientIDcol,time = endpointTimeCol,status = endpointStatusCol)
  # print(colnames(coxRes))
  print(coxRes[,c("Wald test p-value", "Variable")], n = 3)
  })
# 