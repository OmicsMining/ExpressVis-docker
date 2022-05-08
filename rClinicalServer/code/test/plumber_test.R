library(testthat)
library(httr)
library(tidyverse)
# 
# test_that("test_surivialSplitStat", {
#   survivalDF = read_csv("../../testData/SH+cohort-SurvivalAnalysis-Proteomics.csv")
#   patientIDColumn <- "PatientID"; endpointStatus <- "OS Status";endpointTime <- "OS"
#   clinicalFrame <- survivalDF[,c("OS", "OS Status")]
#   expressionFrame <- survivalDF[, c("GNL2", "BDH1", "SEPTIN1")]
#   
#   clinicalDic   <- as.list(clinicalFrame)
#   expressionDic <- as.list(expressionFrame)
#   patientIDs    <- survivalDF["PatientID"]
#   endpointTimeCol   <- "OS"
#   endpointStatusCol <- "OS Status"
# 
#   result <- httr::POST("http://127.0.0.1:8002/surivialSplitMaxStatAndForestAnnotation",
#                        body = list(clinicalDic    = clinicalDic,
#                                    expressionDic  = expressionDic,
#                                    patientIDs     = patientIDs,
#                                    endpointTimeCol   = endpointTimeCol,
#                                    endpointStatusCol = endpointStatusCol),
#                        encode = "json")
# 
#   resultValue <- httr::content(result, encoding = "UTF8")[[1]]
#   print(resultValue)
# })

test_that("test surivialSplitApproximativeMaxStatAndForestAnnotation", {
  survivalDF = read_csv("../../testData/SH+cohort-SurvivalAnalysis-Proteomics.csv")
  patientIDColumn <- "PatientID"; endpointStatus <- "OS Status";endpointTime <- "OS"
  clinicalFrame <- survivalDF[,c("OS", "OS Status")]
  expressionFrame <- survivalDF[, c("GNL2", "BDH1", "SEPTIN1")]

  clinicalDic   <- as.list(clinicalFrame)
  expressionDic <- as.list(expressionFrame)
  patientIDs    <- survivalDF["PatientID"]
  endpointTimeCol   <- "OS"
  endpointStatusCol <- "OS Status"
  
  result <- httr::POST("http://127.0.0.1:8002/surivialSplitApproximativeMaxStatAndForestAnnotation",
                       body = list(clinicalDic    = clinicalDic,
                                   expressionDic  = expressionDic,
                                   patientIDs     = patientIDs,
                                   endpointTimeCol   = endpointTimeCol,
                                   endpointStatusCol = endpointStatusCol,
                                   minProb  = 0.2,
                                   maxProb  = 0.8),
                       encode = "json")
  
  resultValue <- httr::content(result, encoding = "UTF8")[[1]]
  print(resultValue)
  
})
