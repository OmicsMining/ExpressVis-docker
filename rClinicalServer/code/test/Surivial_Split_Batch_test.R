library(testthat)
library(tidyverse)
source("../Surivial_Split_Batch.R")
# 
# test_that("surivial split; maxStat", {
#   survivalDF = read_csv("../../testData/SH+cohort-SurvivalAnalysis-Proteomics.csv")
#   patientIDColumn <- "PatientID"; endpointStatus <- "OS Status";endpointTime <- "OS"
#   minProb=0.1;maxProb=0.9;percentageThreshold=20
#   survivalRes <- percentageSplit(
#     survivalDF = survivalDF, 
#     patientID  = patientIDColumn,
#     time       = endpointTime,
#     status     = endpointStatus,
#     percentageThreshold = percentageThreshold)
#   print(survivalRes, n = 10)
# })
# 


test_that("surivial split; maxStat", {
  survivalDF = read_csv("../../testData/SH+cohort-SurvivalAnalysis-Proteomics.csv")
  patientIDColumn <- "PatientID"
  endpointStatus <- "OS Status"
  endpointTime <- "OS"
  minProb=0.1 
  maxProb=0.9
  
  print(survivalDF[,1:10], n = 10)
  survivalRes <- maxStatSplitCoin(
    survivalDF = survivalDF[, 1:10],
    patientID  = patientIDColumn,
    time       = endpointTime,
    status     = endpointStatus,
    minProp    = minProb,
    maxProp    = maxProb)
  print(survivalRes, n = 10)
})



