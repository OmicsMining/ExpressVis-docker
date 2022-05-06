source("./client2server.utils.R")
source("./constructEset.R")
source("./diffAnalysis.utils.R")
source("./limma.R")
source("./deseq2.R")
library(rjson)


#* @param valuesDic
#* @param genes
#* @param annoLibrary
#* @param diffGroupPairs
#* @post /arrayMultipleDiffAnalysisWithValues
function(valuesDic, genes, annoLibrary, diffGroupPairs) {
  valuesMatrix  <- convertValuesList2matrix(valuesDic, genes)
  groupPairList <- convertDiffGroupPairs(diffGroupPairs)
  
  expressSet <- constructEsetFromExpressionMatrix(valuesMatrix)
  diffResults <- affyLimmaMultipleDiffGroupPairsDiffAnalysisFromClient(
    expressSet  = expressSet,
    annoLibrary = annoLibrary,
    diffGroupPairList = groupPairList,
  )
  
  return (rjson::toJSON(diffResults))
}

#* @param valuesDic
#* @param genes
#* @param annoLibrary
#* @param baseSamples
#* @param targetSamples
#* @post /arrayOneDiffGroupPairWithValues
function(valuesDic, genes, annoLibrary, baseSamples, targetSamples) {
  valuesMatrix <- convertValuesList2matrix(valuesDic, genes)
  expressSet <- constructEsetFromExpressionMatrix(valuesMatrix)
  
  diffResults <- affyLimmaOneDiffGroupPairDiffAnalysisFromClient(
    expressSet    = expressSet, 
    annoLibrary   = annoLibrary, 
    baseSamples   = baseSamples, 
    targetSamples = targetSamples,
  )
  
  return (rjson::toJSON(diffResults))
}

#* @param countsDic
#* @param genes
#* @param baseSamples
#* @param targetSamples
#* @post /rnaseqOneDiffGroupPairWithCounts
function(countsDic, genes, baseSamples, targetSamples) {
  countsMatrix = convertValuesList2matrix(countsDic, genes)
  
  diffResults = deseq2Diff(
    countsMatrix  = countsMatrix,
    baseSamples   = baseSamples,
    targetSamples = targetSamples
  )
  return (rjson::toJSON(diffResults))
}

#* @param countsDic
#* @param genes
#* @param diffGroupPairs
#* @post /rnaseqMultipleDiffGroupPairsWithCounts
function(countsDic, genes, diffGroupPairs) {
  countsMatrix  <- convertValuesList2matrix(countsDic, genes)
  groupPairList <- convertDiffGroupPairs(diffGroupPairs)

  diffResults <- deseq2DiffMultipleGroupParis(
    countsMatrix      = countsMatrix,
    diffGroupPairList = groupPairList
  )
  return (rjson::toJSON(diffResults))
}



#* @param a 
#* @param b
#* @post /sum
function(a, b) {
  sumResult = as.numeric(a) + as.numeric(b)
  return (sumResult)
}


#' @filter cors
cors <- function(req, res) {
  
  res$setHeader("Access-Control-Allow-Origin", "*")
  
  if (req$REQUEST_METHOD == "OPTIONS") {
    res$setHeader("Access-Control-Allow-Methods","*")
    res$setHeader("Access-Control-Allow-Headers", req$HTTP_ACCESS_CONTROL_REQUEST_HEADERS)
    res$status <- 200 
    return(list())
  } else {
    plumber::forward()
  }
}

#* @post /test
# function(baseSamples, targetSamples) {
#   # baseSamples is a string seperated with ,
#   baseSamples   = unlist(strsplit(baseSamples, ","))
#   targetSamples = unlist(strsplit(targetSamples, ","))
#   frame <- data.frame(a = c(1,3,4), b = c("h", "l", "h"))
#   return (list(frame, frame))
# }