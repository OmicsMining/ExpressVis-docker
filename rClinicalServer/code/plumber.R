source("./Surivial_ForestPlot_Batch.R")
source("./Surivial_Split_Batch.R")
library("tidyverse")
#* @param clinicalDic
#* @param expressionDic
#* @param patientIDs
#* @param endpointTimeCol
#* @param endpointStatusCol
#* @post /surivialSplitMaxStat
function(clinicalDic, expressionDic, patientIDs, endpointTimeCol, endpointStatusCol) {
  clinicalFrame <- as_tibble(clinicalDic)
  expressionFrame <- as_tibble(expressionDic)
  survivalFrame <- bind_cols(clinicalFrame, expressionFrame)
  survivalFrame["PatientID"] <- patientIDs
  expressionSplitResult <- maxStatSplit(
    survivalDF = survivalFrame, 
    patientID  = "PatientID",
    time       = endpointTimeCol,
    status     = endpointStatusCol,)
  return (rjson::toJSON(expressionSplitResult))
}

#* @param splitDic
#* @param patientIDcol
#* @param endpointTimeCol
#* @param endpointStatusCol
#* @post /obtainSurvivalAnnotationForForestPlot
function(splitDic, patientIDcol, endpointTimeCol, endpointStatusCol) {
  splitFrame <- as_tibble(splitDic)
  survivalAnno <- survivalAnnotation(
    splitDF   = splitFrame,
    patientID = patientIDcol, 
    time      = endpointTimeCol,
    status    = endpointStatusCol)
  return (rjson::toJSON(survivalAnno))
}


#* @param clinicalDic
#* @param expressionDic
#* @param patientIDs
#* @param endpointTimeCol
#* @param endpointStatusCol
#* @param minProb
#* @param maxProb
#* @post /surivialSplitMaxStatAndForestAnnotation
function(clinicalDic, expressionDic, patientIDs, endpointTimeCol, endpointStatusCol, minProb, maxProb) {
  clinicalFrame <- as_tibble(clinicalDic)
  expressionFrame <- as_tibble(expressionDic)
  survivalFrame <- bind_cols(clinicalFrame, expressionFrame)
  survivalFrame["PatientID"] <- patientIDs
  survivalSplitFrame <- maxStatSplit(
    survivalDF = survivalFrame, 
    patientID  = "PatientID",
    time       = endpointTimeCol,
    status     = endpointStatusCol,
    minProb    = minProb,
    maxProb    = maxProb)
  
  survivalAnno <-  survivalAnnotation(
    splitDF   = survivalSplitFrame,
    patientID = "PatientID", 
    time      = endpointTimeCol,
    status    = endpointStatusCol)

  resultList <- list(survivalSplit = survivalSplitFrame, survivalAnno = survivalAnno)
  return (rjson::toJSON(resultList))
}



#* @param clinicalDic
#* @param expressionDic
#* @param patientIDs
#* @param endpointTimeCol
#* @param endpointStatusCol
#* @param percentageThreshold
#* @post /surivialSplitPercentageAndForestAnnotation
function(clinicalDic, expressionDic, patientIDs, endpointTimeCol, endpointStatusCol, percentageThreshold) {
  clinicalFrame <- as_tibble(clinicalDic)
  expressionFrame <- as_tibble(expressionDic)
  survivalFrame <- bind_cols(clinicalFrame, expressionFrame)
  survivalFrame["PatientID"] <- patientIDs
  survivalSplitFrame <- percentageSplit(
    survivalDF = survivalFrame, 
    patientID  = "PatientID",
    time       = endpointTimeCol,
    status     = endpointStatusCol,
    percentageThreshold = 100 * percentageThreshold) # percentageThreshold from the client is like 0.5, should transform to 50
  
  survivalAnno <-  survivalAnnotation(
    splitDF   = survivalSplitFrame,
    patientID = "PatientID", 
    time      = endpointTimeCol,
    status    = endpointStatusCol)
  
  resultList <- list(survivalSplit = survivalSplitFrame, survivalAnno = survivalAnno)
  return (rjson::toJSON(resultList))
}


#* @param clinicalDic
#* @param expressionDic
#* @param patientIDs
#* @param endpointTimeCol
#* @param endpointStatusCol
#* @post /surivialSplitApproximativeMaxStatAndForestAnnotation
function(clinicalDic, expressionDic, patientIDs, endpointTimeCol, endpointStatusCol, minProb, maxProb) {
  clinicalFrame <- as_tibble(clinicalDic)
  expressionFrame <- as_tibble(expressionDic)
  survivalFrame <- bind_cols(clinicalFrame, expressionFrame)
  survivalFrame["PatientID"] <- patientIDs
  
  survivalSplitFrame <- maxStatSplitCoin(
    survivalDF = survivalFrame, 
    patientID  = "PatientID",
    time       = endpointTimeCol,
    status     = endpointStatusCol,
    minProp    = minProb,
    maxProp    = maxProb)
  
  survivalAnno <-  survivalAnnotation(
    splitDF   = survivalSplitFrame,
    patientID = "PatientID", 
    time      = endpointTimeCol,
    status    = endpointStatusCol)
  
  
  resultList <- list(survivalSplit = survivalSplitFrame, survivalAnno = survivalAnno)
  return (rjson::toJSON(resultList))
}










